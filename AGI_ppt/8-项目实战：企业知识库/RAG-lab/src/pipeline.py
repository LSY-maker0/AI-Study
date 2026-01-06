"""
pipeline - 系统主流程调度，pdf解析，分块，向量化，问题处理等

Author: lsy
Date: 2026/1/7
"""
from pyprojroot import here
from src.text_splitter import TextSplitter
from pathlib import Path

class Pipeline:
    def __init__(self):
        pass

    def chunk_reports(self):
        """将pdf解析后的报告进行分块处理，存储页码以及后面向量化"""
        text_splitter = TextSplitter()
        print('开始分割文档...')
        all_report_dir = Path('../data/stock_data/debug_data')
        output_dir = Path('../data/stock_data/databases/chunked_reports')
        text_splitter.split_all_reports(
            all_report_dir=all_report_dir,
            output_dir=output_dir,
        )

if __name__ == '__main__':
    root_path=here()/"data"/"stock_data"
    # 初始化主流程，使用推荐的配置
    print(root_path)
    pipeline = Pipeline()

    # 1. 解析pdf，并转化为markdown

    # 2. 分块，输出到 database/chunked_reports/对应文件名.json
    pipeline.chunk_reports()

    # 3. 从分块报告中创建向量数据库，输出到 database/vector_dbs/对应文件名.faiss

    # 4. 处理问题并生成答案
