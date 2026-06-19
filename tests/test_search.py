"""
搜索索引模块测试
"""
import pytest
from app.qa.search import SearchIndex


@pytest.fixture
def sample_attractions():
    """测试用景点数据"""
    return [
        {
            'id': 1,
            'name': '黄果树瀑布',
            'address': '安顺市镇宁县',
            'category': '自然风光',
            'description': '中国最大的瀑布，气势磅礴',
            'features': '大瀑布、水帘洞、天星桥',
            'rating': 4.8
        },
        {
            'id': 2,
            'name': '西江千户苗寨',
            'address': '黔东南州雷山县',
            'category': '人文景观',
            'description': '世界最大的苗族聚居村寨',
            'features': '苗族文化、吊脚楼、长桌宴',
            'rating': 4.6
        },
        {
            'id': 3,
            'name': '梵净山',
            'address': '铜仁市江口县',
            'category': '自然风光',
            'description': '佛教名山，世界自然遗产',
            'features': '蘑菇石、金顶、云海',
            'rating': 4.7
        },
    ]


@pytest.fixture
def search_index(sample_attractions):
    """构建好的搜索索引"""
    index = SearchIndex()
    index.build(sample_attractions)
    return index


class TestSearchIndex:
    """测试搜索索引"""

    def test_build_index(self, search_index):
        """测试索引构建"""
        assert len(search_index.attractions) == 3
        assert len(search_index.tfidf_matrix) == 3
        assert len(search_index.vocab) > 0

    def test_search_by_name(self, search_index):
        """测试按名称搜索"""
        results = search_index.search("黄果树瀑布", top_k=1)
        assert len(results) > 0
        assert results[0][1]['name'] == '黄果树瀑布'

    def test_search_by_description(self, search_index):
        """测试按描述搜索"""
        results = search_index.search("苗族村寨", top_k=1)
        assert len(results) > 0
        assert results[0][1]['name'] == '西江千户苗寨'

    def test_search_by_category(self, search_index):
        """测试按类别搜索"""
        results = search_index.search("自然风光", top_k=5)
        assert len(results) >= 2  # 黄果树和梵净山都是自然风光

    def test_search_empty_query(self, search_index):
        """测试空查询"""
        results = search_index.search("", top_k=5)
        assert results == []

    def test_search_top_k(self, search_index):
        """测试返回数量限制"""
        results = search_index.search("贵州", top_k=2)
        assert len(results) <= 2

    def test_tokenize(self):
        """测试分词"""
        tokens = SearchIndex._tokenize("黄果树瀑布门票多少钱")
        assert len(tokens) > 0
        # 停用词应该被过滤
        assert "的" not in tokens

    def test_tokenize_empty(self):
        """测试空文本分词"""
        assert SearchIndex._tokenize("") == []
        assert SearchIndex._tokenize(None) == []

    def test_cosine_sim(self):
        """测试余弦相似度"""
        vec_a = {'a': 1.0, 'b': 2.0}
        vec_b = {'a': 1.0, 'b': 2.0}
        assert SearchIndex._cosine_sim(vec_a, vec_b) == pytest.approx(1.0)

        vec_c = {'c': 1.0}
        assert SearchIndex._cosine_sim(vec_a, vec_c) == 0.0
