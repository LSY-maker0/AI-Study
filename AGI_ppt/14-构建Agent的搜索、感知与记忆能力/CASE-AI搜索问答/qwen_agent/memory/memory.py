# 版权所有 2023 The Qwen 团队, Alibaba Group。保留所有权利。
#
# 根据 Apache 许可证 2.0 版（许可证）授权；
# 除非符合许可证，否则您不得使用此文件。
# 您可以在以下网址获得许可证的副本：
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# 除非适用法律要求或书面同意，否则根据许可证分发的软件以"按原样"方式分发，
# 不附带任何明示或暗示的保证或条件。请参阅许可证了解具体的语言管理权限和
# 许可证限制。

import json
from importlib import import_module
from typing import Dict, Iterator, List, Optional, Union

import json5

from qwen_agent import Agent
from qwen_agent.llm import BaseChatModel
from qwen_agent.llm.schema import ASSISTANT, DEFAULT_SYSTEM_MESSAGE, USER, Message
from qwen_agent.log import logger
from qwen_agent.settings import (DEFAULT_MAX_REF_TOKEN, DEFAULT_PARSER_PAGE_SIZE, DEFAULT_RAG_KEYGEN_STRATEGY,
                                 DEFAULT_RAG_SEARCHERS)
from qwen_agent.tools import BaseTool
from qwen_agent.tools.simple_doc_parser import PARSER_SUPPORTED_FILE_TYPES
from qwen_agent.utils.utils import extract_files_from_messages, extract_text_from_message, get_file_type
from qwen_agent.tools.es_retrieval import ESRetrievalTool


class Memory(Agent):
    """Memory 是一个用于文件管理的特殊代理。

    默认情况下，此内存可以使用检索工具进行 RAG。
    """

    def __init__(self,
                 function_list: Optional[List[Union[str, Dict, BaseTool]]] = None,
                 llm: Optional[Union[Dict, BaseChatModel]] = None,
                 system_message: Optional[str] = DEFAULT_SYSTEM_MESSAGE,
                 files: Optional[List[str]] = None,
                 rag_cfg: Optional[Dict] = None):
        """初始化内存。

        Args:
            rag_cfg: RAG 的配置。一个例子是：
              {
                'max_ref_token': 4000,
                'parser_page_size': 500,
                'rag_keygen_strategy': 'SplitQueryThenGenKeyword',
                'rag_searchers': ['keyword_search', 'front_page_search']
              }
              上述是默认设置。
        """
        self.cfg = rag_cfg or {}
        print(f'我的rag{self.cfg}')
        self.max_ref_token: int = self.cfg.get('max_ref_token', DEFAULT_MAX_REF_TOKEN)
        self.parser_page_size: int = self.cfg.get('parser_page_size', DEFAULT_PARSER_PAGE_SIZE)
        self.rag_searchers = self.cfg.get('rag_searchers', DEFAULT_RAG_SEARCHERS)
        self.rag_keygen_strategy = self.cfg.get('rag_keygen_strategy', DEFAULT_RAG_KEYGEN_STRATEGY)
        if not llm:
            # 没有适合关键词生成的模型
            self.rag_keygen_strategy = 'none'

        # --- 新增：根据配置选择 RAG 后端 ---
        self.rag_backend = self.cfg.get('rag_backend', 'default')  # 默认为原始实现

        function_list = function_list or []

        if self.rag_backend == 'elasticsearch':
            # 如果配置为 elasticsearch，则加载我们自定义的 ES 检索工具
            print("[Memory] 使用 Elasticsearch 后端进行检索。")
            retrieval_tool = ESRetrievalTool(cfg=self.cfg)
            # 将其实例添加到 function_list 中，它会因为同名'retrieval'而自动覆盖
            function_list.append(retrieval_tool)
        else:
            # 保持默认行为，加载原始的内存检索工具
            print("[Memory] 使用默认的内存后端进行检索。")
            function_list.append({
                'name': 'retrieval',
                'max_ref_token': self.max_ref_token,
                'parser_page_size': self.parser_page_size,
                'rag_searchers': self.rag_searchers,
            })

        # 加载 doc_parser，两个后端模式都需要它
        function_list.append({
            'name': 'doc_parser',
            'max_ref_token': self.max_ref_token,
            'parser_page_size': self.parser_page_size,
        })

        super().__init__(function_list=function_list,
                         llm=llm,
                         system_message=system_message)

        self.system_files = files or []

    def _run(self, messages: List[Message], lang: str = 'en', **kwargs) -> Iterator[List[Message]]:
        """此代理负责处理消息中的输入文件。

         此方法将文件存储在知识库中，然后根据查询检索相关部分并将其返回。
         当前支持的文件类型包括：.pdf、.docx、.pptx、.txt、.csv、.tsv、.xlsx、.xls 和 html。

         Args:
             messages: 消息列表。
             lang: 语言。

        Yields:
            检索文档的消息。
        """
        # 处理消息中的文件
        rag_files = self.get_rag_files(messages)

        if not rag_files:
            yield [Message(role=ASSISTANT, content='', name='memory')]
        else:
            query = ''
            # 仅根据最后一个用户查询进行检索（如果存在）
            if messages and messages[-1].role == USER:
                query = extract_text_from_message(messages[-1], add_upload_info=False)

            # 关键词生成
            if query and self.rag_keygen_strategy.lower() != 'none':
                module_name = 'qwen_agent.agents.keygen_strategies'
                module = import_module(module_name)
                cls = getattr(module, self.rag_keygen_strategy)
                keygen = cls(llm=self.llm)
                response = keygen.run([Message(USER, query)], files=rag_files)
                last = None
                for last in response:
                    continue
                if last:
                    keyword = last[-1].content.strip()
                else:
                    keyword = ''

                if keyword.startswith('```json'):
                    keyword = keyword[len('```json'):]
                if keyword.endswith('```'):
                    keyword = keyword[:-3]
                try:
                    keyword_dict = json5.loads(keyword)
                    if 'text' not in keyword_dict:
                        keyword_dict['text'] = query
                    query = json.dumps(keyword_dict, ensure_ascii=False)
                    logger.info(query)
                except Exception:
                    query = query

            content = self.function_map['retrieval'].call(
                {
                    'query': query,
                    'files': rag_files
                },
                **kwargs,
            )
            if not isinstance(content, str):
                content = json.dumps(content, ensure_ascii=False, indent=4)

            yield [Message(role=ASSISTANT, content=content, name='memory')]

    def get_rag_files(self, messages: List[Message]):
        session_files = extract_files_from_messages(messages, include_images=False)
        files = self.system_files + session_files
        rag_files = []
        for file in files:
            f_type = get_file_type(file)
            if f_type in PARSER_SUPPORTED_FILE_TYPES and file not in rag_files:
                rag_files.append(file)
        return rag_files