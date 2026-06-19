"""
搜索模块 — TF-IDF 向量索引 + 余弦相似度检索

职责：
- 对景点文本分词并构建 TF-IDF 索引
- 接收查询，返回按相似度排序的景点列表
"""

import math
import re
from collections import defaultdict


class SearchIndex:
    """TF-IDF 向量检索引擎"""

    # 用于索引的景点文本字段
    INDEX_FIELDS = [
        'name', 'address', 'category', 'description', 'features',
        'tips', 'best_season', 'history_culture', 'nearby_attractions'
    ]

    # 停用词
    STOPWORDS = {
        '的', '了', '是', '在', '和', '有', '也', '都', '就', '不',
        '这', '那', '到', '被', '把', '会', '能', '可以', '去', '来',
        '一个', '什么', '怎么', '多少', '哪', '吗', '呢', '啊', '吧',
        '以及', '或', '等', '位于', '地处', '属于', '其中', '进行'
    }

    def __init__(self):
        self.attractions = []
        self.corpus_tokens = []
        self.vocab = {}
        self.idf = {}
        self.tfidf_matrix = []

    def build(self, attractions):
        """
        用景点列表构建索引

        Args:
            attractions: 景点字典列表
        """
        self.attractions = attractions
        self.corpus_tokens = []
        self.tfidf_matrix = []

        # 1. 对每个景点分词
        for attr in attractions:
            text = self._doc_text(attr)
            tokens = self._tokenize(text)
            self.corpus_tokens.append(tokens)

        # 2. 构建词表 & 计算 DF
        df = defaultdict(int)
        for tokens in self.corpus_tokens:
            seen = set(tokens)
            for w in seen:
                df[w] += 1

        n = len(self.corpus_tokens)
        self.vocab = {w: i for i, w in enumerate(df)}
        self.idf = {w: math.log((n + 1) / (count + 1)) + 1 for w, count in df.items()}

        # 3. 计算每个文档的 TF-IDF 向量
        for tokens in self.corpus_tokens:
            tf = defaultdict(int)
            for w in tokens:
                tf[w] += 1
            vec = {}
            for w, count in tf.items():
                if w in self.idf:
                    vec[w] = (count / len(tokens)) * self.idf[w]
            self.tfidf_matrix.append(vec)

        return len(self.vocab), n

    def search(self, query, top_k=5):
        """
        检索与查询最相关的景点

        Args:
            query: 用户查询文本
            top_k: 返回数量

        Returns:
            list of (score, attraction_dict)
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # 构建 query 的 TF-IDF 向量
        tf = defaultdict(int)
        for w in query_tokens:
            tf[w] += 1
        query_vec = {}
        for w, count in tf.items():
            if w in self.idf:
                query_vec[w] = (count / len(query_tokens)) * self.idf[w]

        # 余弦相似度
        scores = []
        for i, doc_vec in enumerate(self.tfidf_matrix):
            sim = self._cosine_sim(query_vec, doc_vec)
            if sim > 0:
                scores.append((sim, self.attractions[i]))

        # 额外加分：名称精确匹配、类别匹配
        query_lower = query.lower()
        boosted = []
        for sim, attr in scores:
            bonus = 0.0
            name = (attr.get('name') or '').lower()
            category = (attr.get('category') or '').lower()

            # 名称直接包含 query 或 query 包含名称 → 强加分
            if query_lower in name or name in query_lower:
                bonus += 0.5
            # 关键词在名称/类别中
            for kw in query_tokens:
                if kw in name:
                    bonus += 0.15
                if kw in category:
                    bonus += 0.05

            boosted.append((sim + bonus, attr))

        boosted.sort(key=lambda x: x[0], reverse=True)
        return boosted[:top_k]

    def _doc_text(self, attr):
        """拼接一个景点的全部文本字段用于索引"""
        parts = []
        for f in self.INDEX_FIELDS:
            val = attr.get(f)
            if val:
                parts.append(str(val))
        return ' '.join(parts)

    @staticmethod
    def _tokenize(text):
        """中文 n-gram 分词（无需 jieba），去掉停用词和单字符"""
        if not text:
            return []
        # 去掉标点和特殊字符，只保留中文、字母、数字
        cleaned = re.sub(r'[^一-龥a-zA-Z0-9]', ' ', text)
        # 生成 bi-gram 和 tri-gram
        tokens = []
        for seg in cleaned.split():
            for i in range(len(seg)):
                if i + 1 < len(seg):
                    tokens.append(seg[i:i+2])
                if i + 2 < len(seg):
                    tokens.append(seg[i:i+3])
        # 去停用词和单字符
        return [w for w in tokens if len(w) > 1 and w not in SearchIndex.STOPWORDS]

    @staticmethod
    def _cosine_sim(vec_a, vec_b):
        """计算两个稀疏向量的余弦相似度"""
        common = set(vec_a.keys()) & set(vec_b.keys())
        if not common:
            return 0.0
        dot = sum(vec_a[w] * vec_b[w] for w in common)
        norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
        norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
