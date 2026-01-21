# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re
import time
from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from qwen_agent.log import logger
from qwen_agent.settings import DEFAULT_MAX_REF_TOKEN, DEFAULT_PARSER_PAGE_SIZE, DEFAULT_WORKSPACE
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.tools.simple_doc_parser import PARAGRAPH_SPLIT_SYMBOL, SimpleDocParser, get_plain_doc
from qwen_agent.tools.storage import KeyNotExistsError, Storage
from qwen_agent.utils.tokenization_qwen import count_tokens, tokenizer
from qwen_agent.utils.utils import get_basename_from_url, hash_sha256


class Chunk(BaseModel):
    content: str
    metadata: dict
    token: int

    def __init__(self, content: str, metadata: dict, token: int):
        super().__init__(content=content, metadata=metadata, token=token)

    def to_dict(self) -> dict:
        return {'content': self.content, 'metadata': self.metadata, 'token': self.token}


class Record(BaseModel):
    url: str
    raw: List[Chunk]
    title: str

    def __init__(self, url: str, raw: List[Chunk], title: str):
        super().__init__(url=url, raw=raw, title=title)

    def to_dict(self) -> dict:
        return {'url': self.url, 'raw': [x.to_dict() for x in self.raw], 'title': self.title}


@register_tool('doc_parser')
class DocParser(BaseTool):
    description = '对一个文件进行内容提取和分块、返回分块后的文件内容'
    parameters = {
        'type': 'object',
        'properties': {
            'url': {
                'description': '待解析的文件的路径，可以是一个本地路径或可下载的http(s)链接',
                'type': 'string',
            }
        },
        'required': ['url'],
    }

    def __init__(self, cfg: Optional[Dict] = None):
        super().__init__(cfg)
        self.max_ref_token: int = self.cfg.get('max_ref_token', DEFAULT_MAX_REF_TOKEN)
        self.parser_page_size: int = self.cfg.get('parser_page_size', DEFAULT_PARSER_PAGE_SIZE)

        self.data_root = self.cfg.get('path', os.path.join(DEFAULT_WORKSPACE, 'tools', self.name))
        self.db = Storage({'storage_root_path': self.data_root})

        self.doc_extractor = SimpleDocParser({'structured_doc': True})

    def call(self, params: Union[str, dict], **kwargs) -> dict:
        """提取和分块文档

        返回:
            解析文档为以下块格式:
              {
                'url': '这是此文件的URL',
                'title': '这是此文件提取出的标题',
                'raw': [
                        {
                            'content': '这是一个块',
                            'token': '令牌数量',
                            'metadata': {}  # 此块的一些信息
                        },
                        ...,
                      ]
             }
        """

        params = self._verify_json_format_args(params)
        # 兼容 qwen-agent 版本 <= 0.0.3 的参数传递方式
        max_ref_token = kwargs.get('max_ref_token', self.max_ref_token)
        parser_page_size = kwargs.get('parser_page_size', self.parser_page_size)

        url = params['url']

        cached_name_chunking = f'{hash_sha256(url)}_{str(parser_page_size)}'
        try:
            # 直接加载已分块的文档
            record = self.db.get(cached_name_chunking)
            record = json.loads(record)
            logger.info(f'从缓存中读取 {url} 的分块内容.')
            return record
        except KeyNotExistsError:
            doc = self.doc_extractor.call({'url': url})

        total_token = 0
        for page in doc:
            for para in page['content']:
                total_token += para['token']

        if doc and 'title' in doc[0]:
            title = doc[0]['title']
        else:
            title = get_basename_from_url(url)

        logger.info(f'开始对 {url} ({title}) 进行分块...')
        time1 = time.time()
        # if total_token <= max_ref_token: # 原来的
        if total_token <= 10:
            # 整个文档作为一个块
            content = [
                Chunk(content=get_plain_doc(doc),
                      metadata={
                          'source': url,
                          'title': title,
                          'chunk_id': 0
                      },
                      token=total_token)
            ]
            cached_name_chunking = f'{hash_sha256(url)}_without_chunking'
        else:
            content = self.split_doc_to_chunk(doc, url, title=title, parser_page_size=parser_page_size)

        time2 = time.time()
        logger.info(f'完成对 {url} ({title}) 的分块. 耗时: {time2 - time1} 秒.')

        # 保存文档数据
        new_record = Record(url=url, raw=content, title=title).to_dict()
        new_record_str = json.dumps(new_record, ensure_ascii=False)
        self.db.put(cached_name_chunking, new_record_str)
        return new_record

    def split_doc_to_chunk(self,
                           doc: List[dict],
                           path: str,
                           title: str = '',
                           parser_page_size: int = DEFAULT_PARSER_PAGE_SIZE) -> List[Chunk]:
        res = []
        chunk = []
        available_token = parser_page_size
        has_para = False
        for page in doc:
            page_num = page['page_num']
            if not chunk or f'[page: {str(page_num)}]' != chunk[0]:
                chunk.append(f'[page: {str(page_num)}]')
            idx = 0
            len_para = len(page['content'])
            while idx < len_para:
                if not chunk:
                    chunk.append(f'[page: {str(page_num)}]')
                para = page['content'][idx]
                txt = para.get('text', para.get('table'))
                token = para['token']
                if token <= available_token:
                    available_token -= token
                    chunk.append([txt, page_num])
                    has_para = True
                    idx += 1
                else:
                    if has_para:
                        # 记录一个块
                        if isinstance(chunk[-1], str) and re.fullmatch(r'^\[page: \d+\]$', chunk[-1]) is not None:
                            chunk.pop()  # 冗余的页面信息
                        res.append(
                            Chunk(content=PARAGRAPH_SPLIT_SYMBOL.join(
                                [x if isinstance(x, str) else x[0] for x in chunk]),
                                  metadata={
                                      'source': path,
                                      'title': title,
                                      'chunk_id': len(res)
                                  },
                                  token=parser_page_size - available_token))

                        # 定义新块
                        overlap_txt = self._get_last_part(chunk)
                        if overlap_txt.strip():
                            chunk = [f'[page: {str(chunk[-1][1])}]', overlap_txt]
                            has_para = False
                            available_token = parser_page_size - count_tokens(overlap_txt)
                        else:
                            chunk = []
                            has_para = False
                            available_token = parser_page_size
                    else:
                        # 存在过长的段落
                        # 将段落分割为句子
                        _sentences = re.split(r'\. |。', txt)
                        sentences = []
                        for s in _sentences:
                            token = count_tokens(s)
                            if not s.strip() or token == 0:
                                continue
                            if token <= available_token:
                                sentences.append([s, token])
                            else:
                                # 限制句子长度为块大小
                                token_list = tokenizer.tokenize(s)
                                for si in range(0, len(token_list), available_token):
                                    ss = tokenizer.convert_tokens_to_string(
                                        token_list[si:min(len(token_list), si + available_token)])
                                    sentences.append([ss, min(available_token, len(token_list) - si)])
                        sent_index = 0
                        while sent_index < len(sentences):
                            s = sentences[sent_index][0]
                            token = sentences[sent_index][1]
                            if not chunk:
                                chunk.append(f'[page: {str(page_num)}]')

                            if token <= available_token or (not has_para):
                                # 确保至少添加一个句子
                                # (not has_para) 是之前句子分割的补丁
                                available_token -= token
                                chunk.append([s, page_num])
                                has_para = True
                                sent_index += 1
                            else:
                                assert has_para
                                if isinstance(chunk[-1], str) and re.fullmatch(r'^\[page: \d+\]$',
                                                                               chunk[-1]) is not None:
                                    chunk.pop()  # 冗余的页面信息
                                res.append(
                                    Chunk(content=PARAGRAPH_SPLIT_SYMBOL.join(
                                        [x if isinstance(x, str) else x[0] for x in chunk]),
                                          metadata={
                                              'source': path,
                                              'title': title,
                                              'chunk_id': len(res)
                                          },
                                          token=parser_page_size - available_token))

                                overlap_txt = self._get_last_part(chunk)
                                if overlap_txt.strip():
                                    chunk = [f'[page: {str(chunk[-1][1])}]', overlap_txt]
                                    has_para = False
                                    available_token = parser_page_size - count_tokens(overlap_txt)
                                else:
                                    chunk = []
                                    has_para = False
                                    available_token = parser_page_size
                        # 已按句子拆分此段落
                        idx += 1
        if has_para:
            if isinstance(chunk[-1], str) and re.fullmatch(r'^\[page: \d+\]$', chunk[-1]) is not None:
                chunk.pop()  # 冗余的页面信息
            res.append(
                Chunk(content=PARAGRAPH_SPLIT_SYMBOL.join([x if isinstance(x, str) else x[0] for x in chunk]),
                      metadata={
                          'source': path,
                          'title': title,
                          'chunk_id': len(res)
                      },
                      token=parser_page_size - available_token))

        return res

    def _get_last_part(self, chunk: list) -> str:
        overlap = ''
        need_page = chunk[-1][1]  # 只需要此页面来前置
        available_len = 150
        for i in range(len(chunk) - 1, -1, -1):
            if not (isinstance(chunk[i], list) and len(chunk[i]) == 2):
                continue
            if chunk[i][1] != need_page:
                return overlap
            para = chunk[i][0]
            if len(para) <= available_len:
                if overlap:
                    overlap = f'{para}{PARAGRAPH_SPLIT_SYMBOL}{overlap}'
                else:
                    overlap = f'{para}'
                available_len -= len(para)
                continue
            sentence_split_symbol = '. '
            if '。' in para:
                sentence_split_symbol = '。'
            sentences = re.split(r'\. |。', para)
            sentences = [sentence.strip() for sentence in sentences if sentence]
            for j in range(len(sentences) - 1, -1, -1):
                sent = sentences[j]
                if not sent.strip():
                    continue
                if len(sent) <= available_len:
                    if overlap:
                        overlap = f'{sent}{sentence_split_symbol}{overlap}'
                    else:
                        overlap = f'{sent}'
                    available_len -= len(sent)
                else:
                    return overlap
        return overlap