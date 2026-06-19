"""
RAG 问答系统 — 门面模块

组合三个子模块：
- SearchIndex: TF-IDF 向量检索
- IntentClassifier: 意图识别
- AnswerGenerator: 回答生成

对外接口保持不变：RAGQuestionAnswer.answer_question(query)
"""

import json
import os
import logging

from app.db import execute_query
from app.qa.search import SearchIndex
from app.qa.intent import detect_intent
from app.qa.generator import AnswerGenerator

logger = logging.getLogger(__name__)


class RAGQuestionAnswer:
    """RAG 问答系统 — 组合搜索、意图识别、回答生成"""

    def __init__(self, db_path=None, data_dir=None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'guizhou_travel.db')
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'data')

        # 三个子模块
        self.search_index = SearchIndex()
        self.answer_generator = AnswerGenerator()

        # 数据
        self.attractions = []
        self.restaurants = {}
        self.travel_tips = {}

        # 初始化
        self._load_all_data()

    def _load_all_data(self):
        """加载所有数据并构建索引"""
        self._load_attractions()
        self._load_restaurants()
        self._load_travel_tips()

        # 更新 generator 的数据
        self.answer_generator.restaurants = self.restaurants
        self.answer_generator.travel_tips = self.travel_tips

        # 构建搜索索引
        vocab_size, doc_count = self.search_index.build(self.attractions)
        logger.info(f"TF-IDF 索引构建完成：词汇量 {vocab_size}，文档数 {doc_count}")

    def _load_attractions(self):
        """从数据库加载景点数据"""
        self.attractions = execute_query('SELECT * FROM attractions')
        logger.info(f"加载 {len(self.attractions)} 个景点数据")

    def _load_restaurants(self):
        """加载餐厅数据"""
        path = os.path.join(self.data_dir, 'restaurants.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.restaurants = json.load(f)
            total = sum(len(v) for v in self.restaurants.values())
            logger.info(f"加载 {total} 家餐厅数据（{len(self.restaurants)} 个城市）")
        except Exception as e:
            logger.warning(f"加载餐厅数据失败: {e}")

    def _load_travel_tips(self):
        """加载旅行贴士数据"""
        path = os.path.join(self.data_dir, 'travel_tips.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.travel_tips = json.load(f)
            logger.info("加载旅行贴士数据完成")
        except Exception as e:
            logger.warning(f"加载旅行贴士数据失败: {e}")

    # ==================== 主接口 ====================

    def answer_question(self, query):
        """
        主入口：检索 + 意图识别 + 生成回答

        Args:
            query: 用户查询文本

        Returns:
            dict with keys: answer, attractions, suggestions
        """
        # 1. 检索
        results = self.search_index.search(query, top_k=5)

        if not results:
            return {
                "answer": "抱歉，没有找到相关信息。您可以尝试询问贵州的景点、门票、开放时间、交通等问题。",
                "attractions": [],
                "suggestions": ["贵州有哪些免费景点？", "黄果树瀑布门票多少钱？", "西江千户苗寨怎么去？"]
            }

        # 2. 意图识别
        intent = detect_intent(query)
        attractions = [attr for _, attr in results]

        # 3. 生成回答
        answer = self.answer_generator.generate(query, intent, attractions)

        return {
            "answer": answer,
            "attractions": attractions[:3],
            "suggestions": self.answer_generator.generate_suggestions(query, attractions)
        }

    # ==================== 兼容旧接口 ====================

    def search(self, query, top_k=5):
        """兼容旧接口：返回 (score, attr) 列表"""
        return self.search_index.search(query, top_k)

    def detect_intent(self, query):
        """兼容旧接口"""
        return detect_intent(query)

    def get_attraction_detail(self, attraction_name):
        """获取景点详情"""
        for attr in self.attractions:
            if attr.get('name') == attraction_name:
                return attr
        return None

    def get_all_attractions(self):
        """获取所有景点"""
        return self.attractions

    def get_attractions_by_category(self, category):
        """按类别获取景点"""
        return [a for a in self.attractions if a.get('category') == category]

    def get_attractions_by_region(self, region):
        """按地区获取景点"""
        return [a for a in self.attractions if region in (a.get('address') or '')]

    def get_top_attractions(self, limit=10):
        """获取评分最高的景点"""
        return sorted(self.attractions, key=lambda x: x.get('rating') or 0, reverse=True)[:limit]
