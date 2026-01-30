"""
reranking - 重排

Author: lsy
Date: 2026/1/15
"""
import os
import re
import src.prompts as prompts
from concurrent.futures import ThreadPoolExecutor

class LLMReranker:
    def __init__(self):
        self.system_prompt_rerank_multiple_blocks = prompts.RerankingPrompt.system_prompt_rerank_multiple_blocks

        import dashscope
        dashscope.api_key=os.getenv("DASHSCOPE_API_KEY")
        self.llm = dashscope

    def _parse_rankings(self, content: str, total_blocks: int):
        """
        解析 LLM 返回的评分文本，提取每个块的 ID 和分数。

        Args:
            content (str): LLM 返回的 content 字符串
            total_blocks (int): 预期的块总数（用于验证）

        Returns:
            list: [{'block_id': int, 'relevance_score': float}, ...]
        """
        if not content:
            return []

        # 匹配模式：
        # 1. "块 1 评分" -> 提取 ID
        # 2. "相关性分数" -> 提取冒号后的数字 (0.6)
        pattern = re.compile(
            r'块\s*(\d+)\s*评分.*?相关性分数[^0-9]*?([0-9.]+)',
            re.DOTALL | re.IGNORECASE
        )

        matches = pattern.findall(content)

        results = []
        if matches:
            for match in matches:
                try:
                    block_id = int(match[0])
                    score = float(match[1])

                    # 确保分数在 0-1 之间
                    if 0 <= score <= 1:
                        results.append({
                            'block_id': block_id,
                            'relevance_score': score
                        })
                except (ValueError, IndexError):
                    continue
        else:
            print("⚠️ 警告：未能从 LLM 返回结果中解析出分数。")
            print(f"原始内容: {content[:200]}...")

        # 按分数从高到低排序
        results.sort(key=lambda x: x['relevance_score'], reverse=True)

        return results

    def get_rank_for_multiple_blocks(self, question, texts):
        """
        针对多个文本块，批量调用 LLM 进行相关性评分。

        Args:
            question (str): 查询问题
            texts (list): 待评分的文本块列表

        Returns:
            list: [{'block_id': int, 'relevance_score': float}, ...]
        """
        # 格式化 prompt
        formatted_blocks = "\n\n---\n\n".join(
            [f'块 {i + 1}:\n\n"""\n{text}\n"""' for i, text in enumerate(texts)]
        )

        user_prompt = (
            f"这是查询内容：\"{question}\"\n\n"
            "以下是检索到的文本块：\n\n"
            f"{formatted_blocks}\n\n"
            f"你需要提供恰好 {len(texts)} 个排名，按顺序排列。"
        )

        messages = [
            {"role": "system", "content": self.system_prompt_rerank_multiple_blocks},
            {"role": "user", "content": user_prompt},
        ]

        # 调用 LLM
        rsp = self.llm.Generation.call(
            model="qwen-turbo",
            messages=messages,
            temperature=0,
            result_format='message'
        )

        # 检查返回格式
        if 'output' in rsp and 'choices' in rsp['output']:
            content = rsp['output']['choices'][0]['message']['content']
            # 解析并返回结构化结果
            rankings = self._parse_rankings(content, len(texts))
            return rankings
        else:
            raise RuntimeError(f"DashScope返回格式异常: {rsp}")

    def rerank_chunks(self, question, retrieved_chunks, top_n, rerank_batch_size):
        """
        使用多线程并行方式对多个文档进行重排。

        Args:
            question (str): 查询语句
            retrieved_chunks (list): 待重排的文档列表，每个元素是 {'text': str, 'final_score': float}
            top_n (int): 重排后返回的块个数
            rerank_batch_size (int): 每批处理的块数量

        Returns:
            list: 重排后的块列表，按相关性分数从高到低排序
        """
        if not retrieved_chunks:
            return []

        # 按批次分组
        chunk_batches = [retrieved_chunks[i:i+rerank_batch_size]
                        for i in range(0, len(retrieved_chunks), rerank_batch_size)]

        print(f"共 {len(retrieved_chunks)} 个块，分为 {len(chunk_batches)} 批进行重排...")

        # 处理每一批
        def process_chunk(batch):
            texts = [chunk['text'] for chunk in batch]
            # 调用 LLM 获取评分
            rankings = self.get_rank_for_multiple_blocks(question, texts)

            # 将评分结果关联到原始 chunks
            results = []
            for rank_item in rankings:
                block_id = rank_item['block_id'] - 1  # block_id 是从 1 开始的，list 索引从 0 开始
                if 0 <= block_id < len(batch):
                    results.append({
                        'text': batch[block_id]['text'],
                        'relevance_score': rank_item['relevance_score'],
                        # 保留原有的 final_score 作为备用
                        'original_score': batch[block_id].get('final_score', 0)
                    })

            return results

        # 使用多线程处理（max_workers=1 串行调用，避免 QPS 超限）
        with ThreadPoolExecutor(max_workers=1) as executor:
            batch_results = list(executor.map(process_chunk, chunk_batches))

        # 扁平化所有批次的结果
        all_results = []
        for batch in batch_results:
            all_results.extend(batch)

        # 按 relevance_score 从高到低排序
        if all_results:
            all_results.sort(key=lambda x: x['relevance_score'], reverse=True)

        print(f"重排完成，取前 {min(top_n, len(all_results))} 个块")

        # 返回 top_n 个结果
        return all_results[:top_n]
        # print(all_results)
