# qwen_agent/searcher/elasticsearch_searcher.py
import os
import json
import hashlib
import logging
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import BadRequestError  # 导入特定的异常
from qwen_agent.tools.doc_parser import DocParser
from openai import OpenAI

# 为此模块设置一个日志记录器
logger = logging.getLogger(__name__)

class ElasticsearchSearcher:
    """一个使用 Elasticsearch 进行文档索引和搜索的搜索器。"""

    def __init__(self, cfg):
        self.cfg = cfg
        es_cfg = cfg.get('es', {})
        self.host = es_cfg.get('host', 'http://localhost')
        self.port = es_cfg.get('port', 9200)
        self.user = es_cfg.get('user')
        self.password = es_cfg.get('password')
        self.index_name = es_cfg.get('index_name', 'qwen_agent_rag_idx')
        self.search_type = es_cfg.get('search_type', 'keywords')
        self.embedding_client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        # DocParser 用于解析和分块文档
        self.parser = DocParser(cfg=self.cfg)

        self.client = self._connect()
        if self.client:
            logger.info("成功连接到 Elasticsearch！")
            self._create_index_if_not_exists()
        else:
            logger.error("连接 Elasticsearch 失败。请检查您的配置、网络和 ES 服务状态。")

    def _connect(self) -> Elasticsearch:
        """建立并返回到 Elasticsearch 的连接。"""
        try:
            # 根据提供的配置构建连接参数
            es_args = {
                'hosts': [{
                    'host': self.host.replace('https://', '').replace('http://', ''),
                    'port': self.port,
                    'scheme': 'https' if 'https' in self.host else 'http',
                }],
                'verify_certs': False,  # 在生产环境中应设为 True 并提供证书
                'request_timeout': 60,
            }
            if self.user and self.password:
                es_args['basic_auth'] = (self.user, self.password)

            client = Elasticsearch(**es_args)

            # 检查连接
            if not client.ping():
                raise ConnectionError("Elasticsearch ping 失败。")

            return client
        except Exception as e:
            logger.error(f"无法连接到 Elasticsearch：{e}")
            return None

    def _create_index_if_not_exists(self):
        """
        如果索引不存在，则创建它。
        优先尝试使用 IK 中文分词器，如果失败则回退到标准分词器。
        """
        try:
            if not self.client.indices.exists(index=self.index_name):
                logger.info(f"索引 '{self.index_name}' 不存在，正在创建...")

                # 优先尝试使用 IK 分词器的配置
                ik_index_settings = {
                    "settings": {"analysis": {"analyzer": {"default": {"type": "ik_max_word"}}}},
                    "mappings": {
                        "properties": {
                            "content": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_smart"},
                            "source": {"type": "keyword"},
                            "token": {"type": "integer"},
                            # 添加向量字段
                            "vector_content": {
                                "type": "dense_vector",
                                "dims": 1024,  # 根据你用的模型维度调整
                                "index": True,
                                "similarity": "cosine"
                            }
                        }
                    }
                }

                try:
                    # 首次尝试使用 IK 创建
                    self.client.indices.create(index=self.index_name, body=ik_index_settings)
                    logger.info(f"成功使用 IK 分词器创建索引 '{self.index_name}'。")
                except BadRequestError as e:
                    # 捕获因分词器不存在导致的错误
                    if 'Unknown analyzer type [ik_max_word]' in str(e):
                        logger.warning(
                            "未能找到 'ik_max_word' 分词器。这通常是因为 Elasticsearch 未安装 IK 中文分词插件。")
                        logger.warning("将回退使用标准分词器。对于中文搜索，强烈建议安装 IK 插件以获得更好效果。")

                        # 回退配置：使用标准分词器
                        standard_index_settings = {
                            "mappings": {
                                "properties": {
                                    "content": {"type": "text"},  # 使用默认的标准分词器
                                    "source": {"type": "keyword"},
                                    # 添加向量字段
                                    "vector_content": {
                                        "type": "dense_vector",
                                        "dims": 1024,  # 根据你用的模型维度调整
                                        "index": True,
                                        "similarity": "cosine"
                                    }
                                }
                            }
                        }
                        # 再次尝试使用标准配置创建
                        self.client.indices.create(index=self.index_name, body=standard_index_settings)
                        logger.info(f"成功使用标准分词器创建索引 '{self.index_name}'。")
                    else:
                        # 如果是其他类型的请求错误，则重新引发异常
                        raise e
            else:
                logger.info(f"索引 '{self.index_name}' 已存在。")
        except Exception as e:
            logger.error(f"创建或检查索引 '{self.index_name}' 时发生严重错误: {e}")

    def _get_embedding(self, text: str) -> list:
        """使用 Dashscope 的 text-embedding-v4 模型为文本生成向量。"""
        print('111111')
        try:
            # 确保文本不为空
            if not text.strip():
                return []

            response = self.embedding_client.embeddings.create(
                model="text-embedding-v4",
                input=text,
                dimensions=1024,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"  - 获取 embedding 时出错: {e}")
            return []

    def index_files(self, files: list):
        """
        高效地索引文件列表。
        它首先获取所有文件的所有文本块，然后通过一次 mget 请求过滤掉已存在的块，
        最后通过一次 bulk 请求批量索引所有新块。
        """
        if not self.client:
            logger.error("Elasticsearch 客户端不可用，无法执行索引。")
            return

        logger.info(f"开始处理 {len(files)} 个文件以进行索引...")
        chunks = self._get_chunks(files)
        print(f"从文件中总共提取了 {len(chunks)} 个内容块。")

        if not chunks:
            logger.warning("未能从文件中提取任何内容块，索引过程终止。")
            return

        print(' hi啊师大',chunks)

        # 高效地筛选出需要索引的新块
        new_chunks = self._filter_existing_chunks_efficiently(chunks)

        for chunk in new_chunks:
            # TODO: 接入 embedding 模型生成向量
            chunk['vector'] = self._get_embedding(chunk['content'])

        if new_chunks:
            logger.info(f'发现 {len(new_chunks)} 个新的文档块，开始向 Elasticsearch 批量索引...')
            actions = [{
                "_op_type": "index",
                "_index": self.index_name,
                "_id": chunk['id'],
                "_source": {
                    "content": chunk['content'],
                    "source": chunk['metadata']['source'],
                    "token": chunk.get('token', 0),
                    "vector_content": chunk['vector']  # 添加向量数据
                },
            } for chunk in new_chunks]

            try:
                successes, errors = helpers.bulk(self.client, actions, refresh=True, raise_on_error=False)
                logger.info(f"成功索引 {successes} 个新文档块。")
                if errors:
                    logger.error(f"批量索引过程中发生 {len(errors)} 个错误。第一个错误详情: {errors[0]}")
            except helpers.BulkIndexError as e:
                logger.error(f"批量索引时发生严重错误: {len(e.errors)} 个文档索引失败。")
        else:
            logger.info("所有文件内容均已在 Elasticsearch 中建立索引，无需更新。")

    def _get_chunks(self, files: list) -> list:
        """从文件列表中提取并返回所有文本块。"""
        all_chunks = []
        for file_path in files:
            try:
                # 1. 准备 JSON 字符串参数
                params_str = json.dumps({'url': file_path})

                # 2. 调用 DocParser，它会返回一个 JSON 字符串
                parsed_content_str = self.parser.call(
                    params=params_str,
                    use_cache=False  # 强制重新解析，忽略缓存
                )

                # 3. 解析返回的 JSON 字符串
                parsed_record = parsed_content_str

                # 检查解析后的记录是否出错
                if 'error' in parsed_record:
                    logger.error(f"解析文件 '{file_path}' 时返回错误: {parsed_record['error']}")
                    continue

                # 从记录中提取 'raw' 块
                chunks_data = parsed_record.get('raw', [])

                # 为每个块添加源文件信息
                for chunk in chunks_data:
                    if 'metadata' in chunk and 'source' not in chunk['metadata']:
                        chunk['metadata']['source'] = os.path.basename(file_path)
                    all_chunks.append(chunk)

            except Exception as e:
                logger.error(f"处理文件 '{file_path}' 时出错: {e}", exc_info=True)
        return all_chunks

    def _filter_existing_chunks_efficiently(self, chunks: list) -> list:
        """
        使用 mget 高效地从块列表中筛选出尚未在ES中索引的块。
        """
        if not chunks:
            return []

        # 1. 为所有块生成 ID
        for chunk in chunks:
            chunk_content = chunk.get('content', '')
            chunk_source = chunk.get('source', 'unknown')
            sha256 = hashlib.sha256()
            sha256.update(chunk_content.encode('utf-8'))
            sha256.update(chunk_source.encode('utf-8'))
            chunk['id'] = sha256.hexdigest()

        doc_ids = [chunk['id'] for chunk in chunks]

        # 2. 使用 mget 一次性检查所有 ID 是否存在
        try:
            response = self.client.mget(index=self.index_name, body={'ids': doc_ids})
            existing_ids = {doc['_id'] for doc in response['docs'] if doc['found']}
            logger.info(f"在 Elasticsearch 中发现 {len(existing_ids)} 个已存在的文档块。")
        except Exception as e:
            logger.error(f"使用 mget 检查文档是否存在时出错: {e}。将假定所有块都是新的。")
            existing_ids = set()

        # 3. 筛选出新块
        new_chunks = [chunk for chunk in chunks if chunk['id'] not in existing_ids]
        # new_chunks = chunks
        logger.info(f"筛选出 {len(new_chunks)} 个新块需要索引。")
        return new_chunks

    def print_hits(self,query,hits):
        # ===== 🖨️ 打印所有检索结果 =====
        print("\n" + "=" * 80)
        print(f"🔍 [ES 搜索器] 查询词: '{query}'")
        print(f"📊 命中总数: {len(hits)}")
        print("=" * 80)

        for idx, item in enumerate(hits, 1):
            source = item['_source']

            # 提取各个字段
            content = source.get('content', '')
            source_file = source.get('source', '未知来源')
            token_count = source.get('token', 0)
            score = item.get('_score', 0)

            content_full = content[:100] if content else "(无内容)"

            print(f"\n  结果 #{idx}")
            print(f"  ┌────────────────────────────────────────────────────")
            print(f"  │ Score:  {score:.4f}")
            print(f"  │ Token:   {token_count}")
            print(f"  │ 来源:    {source_file}")
            print(f"  │ Content: \n{content_full}")  # 这里打印全部内容
            print(f"  └────────────────────────────────────────────────────")

        print("=" * 80 + "\n")
        # ================================

    def search(self, query: str, max_ref_token: int) -> list:
        """
        在 Elasticsearch 中执行搜索，根据 search_type 选择不同的查询方式。
        """
        if not self.client:
            logger.error("❌ Elasticsearch 客户端不可用，无法执行搜索。")
            return []

        logger.info(f"🔍 正在使用查询语句在 Elasticsearch 中搜索: '{query}'，检索模式: {self.search_type}")

        hits = []

        if self.search_type == 'keyword':
            # ========== 模式1: 纯关键词搜索 ==========
            logger.info(f"🔤 使用【关键词搜索】模式...")

            search_body = {
                "query": {
                    "match": {
                        "content": query
                    }
                },
                "size": 6
            }

            try:
                response = self.client.search(index=self.index_name, body=search_body)
                hits = response['hits']['hits']
            except Exception as e:
                logger.error(f"❌ Elasticsearch 搜索失败: {e}")
                return []

        elif self.search_type == 'vector':
            # ========== 模式2: 纯向量搜索 ==========
            logger.info(f"🧠 使用【语义向量搜索】模式...")

            # 为查询生成向量
            query_vector = self._get_embedding(query)
            if not query_vector:
                logger.warning("⚠️ 无法生成查询向量，回退到关键词搜索。")
                # 回退到关键词搜索
                search_body = {
                    "query": {
                        "match": {
                            "content": query
                        }
                    },
                    "size": 6
                }
                response = self.client.search(index=self.index_name, body=search_body)
                hits = response['hits']['hits']
            else:
                search_body = {
                    "knn": {
                        "field": "vector_content",  # 指定字段名
                        "query_vector": query_vector,  # 指定向量
                        "k": 6,
                        "num_candidates": 1000
                    },
                    "size": 6
                }

                try:
                    response = self.client.search(index=self.index_name, body=search_body)
                    hits = response['hits']['hits']
                except Exception as e:
                    logger.error(f"❌ 向量搜索失败: {e}，回退到关键词搜索。")
                    # 回退到关键词搜索
                    search_body = {
                        "query": {
                            "match": {
                                "content": query
                            }
                        },
                        "size": 6
                    }
                    response = self.client.search(index=self.index_name, body=search_body)
                    hits = response['hits']['hits']


        elif self.search_type == 'hybrid':

            # ========== 模式3: 混合搜索（手动 RRF 版）带详细评分 ==========

            logger.info(f"🔀 使用【混合搜索（手动 RRF）】模式...")

            query_vector = self._get_embedding(query)

            # 如果向量生成失败，纯回退
            if not query_vector:
                logger.warning("⚠️ 无法生成查询向量，回退到关键词搜索。")
                search_body = {"query": {"match": {"content": query}}, "size": 6}
                response = self.client.search(index=self.index_name, body=search_body)
                hits = response['hits']['hits']
            else:
                # --- 第一步：单独跑关键词搜索 ---
                bm25_search_body = {"query": {"match": {"content": query}}, "size": 6}
                try:
                    bm25_response = self.client.search(index=self.index_name, body=bm25_search_body)
                    bm25_hits = bm25_response['hits']['hits']
                except Exception as e:
                    logger.error(f"❌ 关键词子查询失败: {e}")
                    bm25_hits = []

                # --- 第二步：单独跑向量搜索 ---
                knn_search_body = {
                    "knn": {
                        "field": "vector_content",
                        "query_vector": query_vector,
                        "k": 6,
                        "num_candidates": 1000
                    },
                    "size": 6
                }
                try:
                    knn_response = self.client.search(index=self.index_name, body=knn_search_body)
                    knn_hits = knn_response['hits']['hits']
                except Exception as e:
                    logger.error(f"❌ 向量子查询失败: {e}")
                    knn_hits = []
                # --- 第三步：手动执行加权 RRF (Reciprocal Rank Fusion) ---

                # 1. 平衡模式 (推荐)：关键词和向量五五开，兼顾精确匹配和语义理解
                MODE_BALANCED = {"k": 60, "bm25": 0.5, "knn": 0.5}

                # 2. 偏向量模式：优先语义相似，适合模糊查询或找“相关内容”
                MODE_TOWARD_VECTOR = {"k": 20, "bm25": 0.3, "knn": 0.7}

                # 3. 偏关键词模式：优先精确匹配，适合搜人名、代码、专有名词
                MODE_TOWARD_KEYWORD = {"k": 100, "bm25": 0.7, "knn": 0.3}

                # 👇👇👇 【在这里选择模式】 👇👇👇
                current_mode = MODE_TOWARD_VECTOR  # 修改这里切换模式：MODE_BALANCED / MODE_TOWARD_VECTOR / MODE_TOWARD_KEYWORD

                # 提取参数
                k_constant = current_mode["k"]
                bm25_weight = current_mode["bm25"]
                knn_weight = current_mode["knn"]

                logger.info(f"⚙️  当前混合搜索模式配置: K={k_constant}, BM25权重={bm25_weight}, KNN权重={knn_weight}")

                rrf_scores = {}

                # 👇 打印并计算关键词评分
                print("\n" + "=" * 30 + " 📊 关键词评分 (BM25) " + "=" * 30)
                for rank, hit in enumerate(bm25_hits):
                    doc_id = hit['_id']
                    content_preview = hit['_source'].get('content', '')[:15].replace('\n', ' ')

                    # ✅ 修改点1：应用权重系数 (weight / (k + rank))
                    score = (bm25_weight / (k_constant + rank + 1))
                    rrf_scores[doc_id] = {"score": score, "hit": hit}

                    print(
                        f"  Rank {rank}: ID:{doc_id[:6]}... | '{content_preview}...' | (+{score:.4f} 分) [权重:{bm25_weight}]")

                # 👇 打印并计算向量评分
                print("\n" + "=" * 30 + " 🧠 向量评分 (KNN) " + "=" * 30)
                for rank, hit in enumerate(knn_hits):
                    doc_id = hit['_id']
                    content_preview = hit['_source'].get('content', '')[:15].replace('\n', ' ')

                    # ✅ 修改点2：应用权重系数 (weight / (k + rank))
                    score = (knn_weight / (k_constant + rank + 1))

                    if doc_id in rrf_scores:
                        # 双料冠军：分数累加
                        rrf_scores[doc_id]["score"] += score
                        print(
                            f"  Rank {rank}: ID:{doc_id[:6]}... | '{content_preview}...' | (+{score:.4f} 分) ⭐ 双料冠军！总分: {rrf_scores[doc_id]['score']:.4f}")
                    else:
                        # 单打独斗
                        rrf_scores[doc_id] = {"score": score, "hit": hit}
                        print(
                            f"  Rank {rank}: ID:{doc_id[:6]}... | '{content_preview}...' | (+{score:.4f} 分) [权重:{knn_weight}]")

                # --- 第四步：按 RRF 得分排序并取前 6 ---
                sorted_hits = sorted(
                    rrf_scores.values(),
                    key=lambda x: x["score"],
                    reverse=True
                )

                # 👇 打印最终融合排行榜
                print("\n" + "=" * 30 + " 🏆 最终融合榜单 (Top 6) " + "=" * 30)
                hits = []
                for i, item in enumerate(sorted_hits[:6]):
                    hit = item["hit"]
                    score = item["score"]
                    hit['_score'] = score  # 更新 _score 供后续使用
                    hits.append(hit)

                    content_preview = hit['_source'].get('content', '')[:15].replace('\n', ' ')
                    print(f"  No.{i + 1} | ID:{hit['_id'][:6]}... | '{content_preview}...' | 总分: {score:.4f}")

                print("=" * 80 + "\n")

                logger.info(f"🧩 RRF 融合完成：BM25 {len(bm25_hits)} 条 + KNN {len(knn_hits)} 条 -> 最终 {len(hits)} 条")


        else:
            # 未知的检索模式，回退到关键词搜索
            logger.warning(f"⚠️ 未知的检索模式: {self.search_type}，使用默认的关键词搜索。")
            search_body = {
                "query": {
                    "match": {
                        "content": query
                    }
                },
                "size": 6
            }
            response = self.client.search(index=self.index_name, body=search_body)
            hits = response['hits']['hits']

        # 打印结果
        self.print_hits(query, hits)

        # 根据 max_ref_token 筛选结果
        selected_hits = []
        total_tokens = 0
        for hit in hits:
            token_count = hit['_source'].get('token', 1000)
            if total_tokens + token_count > max_ref_token:
                logger.info(f'⏱️  已达到 max_ref_token ({max_ref_token}) 的上限，停止添加更多结果。')
                break
            selected_hits.append(hit)
            total_tokens += token_count

        logger.info(
            f"✅ 搜索完成，从 {len(hits)} 个候选中筛选出 {len(selected_hits)} 个结果 (总计 {total_tokens} tokens)。")
        return selected_hits