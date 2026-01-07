"""
questions_processing - 问题处理器

Author: lsy
Date: 2026/1/7
"""
from pathlib import Path
from src.retrieval import VectorRetriever

class QuestionsProcessor:
    def __init__(
        self,
        llm_ranking:bool=False,
        api_provider:str="dashscope",
        answering_model:str="qwen-turbo-lastest",
        vector_index_path:Path=None,
        metadata_path:Path=None,
    ):
        self.llm_ranking = llm_ranking
        self.api_provider = api_provider
        self.answering_model = answering_model
        self.vector_index_path = vector_index_path
        self.metadata_path = metadata_path

    def __format_retrieval_results(self, retrieval_results) -> str:
        """将检索结果转化为RAG上下文字符串，优化大模型理解"""
        context_parts = []

        # 遍历检索出的每一个块
        for idx, chunk in enumerate(retrieval_results):
            # 1. 提取关键信息
            score = chunk.get('distance', 0)
            file_name = chunk.get('file_origin', '未知文件')
            page_range = chunk.get('page_range', [])
            text_content = chunk.get('text', '')

            # 2. 格式化页码信息 (例如：P34-35)
            page_info = f"P{page_range[0]}" if page_range else "未知页码"
            if len(page_range) > 1:
                page_info += f"-{page_range[-1]}"

            # 3. 构建每个块的展示文本
            # 使用 >>> 符号作为视觉分隔符，帮助模型区分不同引用块
            chunk_text = f"""
[参考文档 {idx + 1}] (相关度: {score})
📂 来源文件: {file_name}
📄 页码: {page_info}
---------------
{text_content}
"""
            context_parts.append(chunk_text)

        # 4. 拼接所有块，作为整体上下文
        rag_text = "\n".join(context_parts)
        return rag_text


    def process_single_question(self,question:str,kind:str) -> dict:
        """单条问题推理，返回结构化答案"""
        # retrieval=Hybridretrieval()
        retrieval=VectorRetriever(vector_index_path=self.vector_index_path,metadata_path=self.metadata_path)

        relevant_chunks=retrieval.get_relevant_chunks(question=question,top_n=20)
        rag_context = self.__format_retrieval_results(relevant_chunks)
        print(rag_context)

