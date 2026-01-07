"""
retrieval - 检索器，检索出对应问题的块

Author: lsy
Date: 2026/1/7
"""
import os
from typing import List,Dict
from pathlib import Path
import json
import faiss
import dashscope
import numpy as np

class VectorRetriever:
    def __init__(self,vector_index_path:Path, metadata_path:Path,embedding_provider:str="dashscope"):
        """
        :param vector_index_path: FAISS向量索引文件路径
        :param metadata_path: 文档元数据文件路径
        """
        self.vector_index_path=vector_index_path
        self.metadata_path=metadata_path
        self.embedding_provider=embedding_provider
        self._set_up_llm() # 设置大模型提供商

        # 定义实例变量但不赋值，用于后续缓存
        self._index = None
        self._metadata_list = None
        self.load()

    def load(self):
        """显式加载资源，也可以在首次搜索时自动触发"""
        if self._index is None:
            self._load_index()
        if self._metadata_list is None:
            self._load_metadata()
        return self

    def _load_index(self):
        """加载 FAISS 索引"""
        if not self.vector_index_path.exists():
            raise FileNotFoundError(f"向量索引文件不存在: {self.vector_index_path}")

        # faiss.read_index 是读取磁盘上预训练好的索引的标准方法
        self._index = faiss.read_index(str(self.vector_index_path))

    def _load_metadata(self):
        """
        加载元数据
        假设元数据是用 pickle 存储的 List[Dict] 或 DataFrame
        """
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"元数据文件不存在: {self.metadata_path}")

        with open(self.metadata_path, 'rb') as f:
            self._metadata_list = json.load(f)

    def _set_up_llm(self):
        if self.embedding_provider=="dashscope":
            dashscope.api_key=os.getenv('DASHSCOPE_API_KEY')

    def _get_embedding(self,text:str):
        resp = dashscope.TextEmbedding.call(
            model='text-embedding-v1',
            input=[text],
        )
        embedding = resp.output['embeddings'][0]['embedding']  # List[float]
        vec = np.array(embedding, dtype='float32')
        # L2 归一化
        # 这一步让向量长度变为 1，以便与库里同样归一化的向量进行余弦相似度计算
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def get_relevant_chunks(self, question:str, top_n:int = 20) -> List[Dict]:
        # 检索出与问题相关的块，返回全部块

        # 获取query的embedding，支持dashscope
        embedding_question = self._get_embedding(question)
        # print(embedding_question,len(embedding_question),f'{question}的向量表表示')
        embedding_array = embedding_question.reshape(1, -1) # 变为二维
        k = min(top_n, self._index.ntotal)
        # print(self._metadata_list,'元数据')
        distances, indices = self._index.search(x=embedding_array,k=k)

        retrieval_results = []
        # print('distances:',distances)
        # print('indices:',indices)
        for distance, index in zip(distances[0], indices[0]):
            distance = round(float(distance),4)
            chunk=self._metadata_list[index]

            result = {
                "distance": distance,
                "page_range": chunk["page_range"],
                "file_origin": chunk["file_origin"],
                "text": chunk["text"],
            }
            retrieval_results.append(result)
        return retrieval_results


