"""
es_search - Elasticsearch 文档检索完整示例

Author: lsy
Date: 2026/1/20
"""
from elasticsearch import Elasticsearch
from pathlib import Path, PosixPath
import json

# ==================== 配置部分 ====================
ES_PORT = 9200
ES_USER = 'elastic'
ES_PASSWORD = ''

INDEX_NAME = 'insurance_docs'
DOCS_DIR = './docs'


# ==================== 1. 连接到 ES ====================
def connect_to_es():
    """连接到 Elasticsearch"""
    print("\n【步骤 1】连接到 Elasticsearch")
    print("-" * 50)

    es = Elasticsearch(
        hosts=[{'host': 'localhost', 'port': ES_PORT, 'scheme': 'https'}],
        basic_auth=(ES_USER, ES_PASSWORD),
        verify_certs=False,  # 仅用于本地测试
        request_timeout=30
    )

    if es.ping():
        print("✅ 连接成功")
        return es
    else:
        print("❌ 连接失败")
        raise Exception("无法连接到 Elasticsearch")


# ==================== 2. 创建索引 ====================
def create_index(es):
    """创建索引"""
    print("\n【步骤 2】创建索引")
    print("-" * 50)

    # 删除旧索引
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print("已删除旧索引")

    # 定义 mapping
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "file_name": {"type": "keyword"}
            }
        }
    }

    # 创建索引
    es.indices.create(index=INDEX_NAME, body=mapping)
    print(f"✅ 索引 '{INDEX_NAME}' 创建成功")


# ==================== 3. 索引文档 ====================
def index_documents(es):
    """批量索引文档"""
    print("\n【步骤 3】索引文档")
    print("-" * 50)

    docs_path = Path(DOCS_DIR)

    if not docs_path.exists():
        print(f"❌ 文档目录不存在: {DOCS_DIR}")
        return

    # 遍历文档
    files = [f for f in docs_path.iterdir() if f.is_file()]
    print(files)
    files=[PosixPath('docs/3-平安企业团体综合意外险.txt'),PosixPath('docs/6-财产一切险.txt')]
    print(f"找到 {len(files)} 个文档")

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        if not file_content.strip():
            raise ValueError('文档内容为空')

        # 将整个文件作为一个文档进行索引
        doc = {
                "content": file_content,
                "file_name": file_path.name
              }
        es.index(index=INDEX_NAME, document=doc,refresh=True)
        print(f"  ✅ 已索引: {file_path.name}")

    # 刷新索引
    es.indices.refresh(index=INDEX_NAME)
    print("✅ 索引刷新完成")


# ==================== 4. 执行搜索 ====================
def search_documents(es, query):
    """执行搜索"""
    print(f"\n【步骤 4】执行搜索")
    print("-" * 50)
    print(f"  搜索查询: {query}")

    # 执行搜索
    search_body = {
        "query": {
            "match": {
                "content": query
            }
        }
    }
    response = es.search(index=INDEX_NAME, body=search_body,size=2)
    hits = response['hits']['hits']
    print("✅搜索完成")
    for i, hit in enumerate(hits):
        print(f"\\n--- 结果 {i + 1} ---")
        print(f"得分 (Score): {hit['_score']}")
        print(f"内容预览: {hit['_source']['content'][:300]}...")

# ==================== 主程序 ====================
def main():
    """主程序"""
    print("=" * 50)
    print("Elasticsearch 文档检索系统")
    print("=" * 50)

    # 1. 连接
    es = connect_to_es()

    # 2. 创建索引
    create_index(es)

    # 3. 索引文档
    index_documents(es)

    # 4. 执行搜索
    query = "平安企业团体综合意外险有哪些特色"
    search_documents(es, query)


    print("\n" + "=" * 50)
    print("✅ 执行完成")
    print("=" * 50)


# 运行主程序
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback

        traceback.print_exc()
