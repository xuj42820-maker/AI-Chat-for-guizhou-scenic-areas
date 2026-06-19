"""
回答生成模块测试
"""
import pytest
from app.qa.generator import AnswerGenerator


@pytest.fixture
def generator():
    """测试用回答生成器"""
    return AnswerGenerator(
        restaurants={
            '贵阳': [
                {'name': '老凯里酸汤鱼', 'specialty': '酸汤鱼', 'avg_price': '80元', 'address': '贵阳市'}
            ]
        },
        travel_tips={
            'food_highlights': ['酸汤鱼', '羊肉粉', '花溪牛肉粉'],
            'safety_tips': ['山路弯多', '溶洞温度低'],
            'cultural_experiences': ['苗族长桌宴', '侗族大歌'],
        }
    )


@pytest.fixture
def sample_results():
    """测试用景点数据"""
    return [
        {
            'name': '黄果树瀑布',
            'address': '安顺市镇宁县',
            'ticket_price': '180元',
            'opening_hours': '07:00-18:00',
            'rating': 4.8,
            'description': '中国最大的瀑布',
            'transportation': '贵阳有直达大巴',
            'best_season': '6-10月',
            'suggested_duration': '1天',
            'nearby_attractions': '天星桥、陡坡塘瀑布',
        },
        {
            'name': '西江千户苗寨',
            'address': '黔东南州雷山县',
            'ticket_price': '100元',
            'rating': 4.6,
            'description': '世界最大的苗族聚居村寨',
        },
    ]


class TestAnswerGenerator:
    """测试回答生成"""

    def test_ticket_single(self, generator, sample_results):
        """测试单个景点门票回答"""
        answer = generator.generate("门票", "ticket", [sample_results[0]])
        assert "黄果树瀑布" in answer
        assert "180元" in answer

    def test_ticket_multiple(self, generator, sample_results):
        """测试多个景点门票回答"""
        answer = generator.generate("门票", "ticket", sample_results)
        assert "黄果树瀑布" in answer
        assert "西江千户苗寨" in answer

    def test_hours(self, generator, sample_results):
        """测试开放时间回答"""
        answer = generator.generate("开放时间", "hours", [sample_results[0]])
        assert "07:00-18:00" in answer

    def test_address(self, generator, sample_results):
        """测试地址回答"""
        answer = generator.generate("在哪", "address", [sample_results[0]])
        assert "安顺市镇宁县" in answer

    def test_transport(self, generator, sample_results):
        """测试交通回答"""
        answer = generator.generate("怎么去", "transport", [sample_results[0]])
        assert "贵阳有直达大巴" in answer

    def test_season(self, generator, sample_results):
        """测试季节回答"""
        answer = generator.generate("什么时候去", "season", [sample_results[0]])
        assert "6-10月" in answer

    def test_duration(self, generator, sample_results):
        """测试时长回答"""
        answer = generator.generate("玩多久", "duration", [sample_results[0]])
        assert "1天" in answer

    def test_nearby(self, generator, sample_results):
        """测试附近景点回答"""
        answer = generator.generate("附近", "nearby", [sample_results[0]])
        assert "天星桥" in answer

    def test_recommend(self, generator, sample_results):
        """测试推荐回答"""
        answer = generator.generate("推荐", "recommend", sample_results)
        assert "黄果树瀑布" in answer
        assert "4.8" in answer

    def test_food_with_city(self, generator, sample_results):
        """测试美食回答（有城市匹配）"""
        answer = generator.generate("美食", "food", [sample_results[0]])
        assert "酸汤鱼" in answer

    def test_safety(self, generator, sample_results):
        """测试安全提示回答"""
        answer = generator.generate("安全", "safety", sample_results)
        assert "山路弯多" in answer

    def test_culture(self, generator, sample_results):
        """测试文化回答"""
        answer = generator.generate("文化", "culture", sample_results)
        assert "苗族长桌宴" in answer

    def test_general_single(self, generator, sample_results):
        """测试通用回答（单个景点）"""
        answer = generator.generate("黄果树", "general", [sample_results[0]])
        assert "黄果树瀑布" in answer
        assert "180元" in answer

    def test_general_multiple(self, generator, sample_results):
        """测试通用回答（多个景点）"""
        answer = generator.generate("贵州", "general", sample_results)
        assert "黄果树瀑布" in answer
        assert "西江千户苗寨" in answer

    def test_suggestions(self, generator, sample_results):
        """测试追问建议生成"""
        suggestions = generator.generate_suggestions("黄果树", sample_results)
        assert len(suggestions) <= 4
        assert any("黄果树" in s for s in suggestions)
