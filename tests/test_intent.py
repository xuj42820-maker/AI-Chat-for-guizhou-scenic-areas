"""
意图识别模块测试
"""
import pytest
from app.qa.intent import detect_intent, match_city


class TestDetectIntent:
    """测试意图识别"""

    def test_ticket_intent(self):
        assert detect_intent("黄果树瀑布门票多少钱") == "ticket"
        assert detect_intent("梵净山票价") == "ticket"
        assert detect_intent("收费多少") == "ticket"

    def test_hours_intent(self):
        assert detect_intent("几点开门") == "hours"
        assert detect_intent("开放时间") == "hours"
        assert detect_intent("营业到几点") == "hours"

    def test_address_intent(self):
        assert detect_intent("黄果树在哪里") == "address"
        assert detect_intent("地址是什么") == "address"

    def test_transport_intent(self):
        assert detect_intent("怎么去西江苗寨") == "transport"
        assert detect_intent("坐高铁到梵净山") == "transport"
        assert detect_intent("自驾路线") == "transport"

    def test_food_intent(self):
        assert detect_intent("贵州有什么好吃的") == "food"
        assert detect_intent("酸汤鱼") == "food"
        assert detect_intent("附近有什么餐厅") == "food"

    def test_recommend_intent(self):
        assert detect_intent("有什么好玩的") == "recommend"
        assert detect_intent("值得去吗") == "recommend"

    def test_season_intent(self):
        assert detect_intent("什么时候去最好") == "season"
        assert detect_intent("几月去合适") == "season"

    def test_free_intent(self):
        assert detect_intent("有免费景点吗") == "free"
        assert detect_intent("免票入园") == "free"

    def test_culture_intent(self):
        assert detect_intent("苗族文化体验") == "culture"
        assert detect_intent("有什么民俗") == "culture"

    def test_general_intent(self):
        assert detect_intent("贵州怎么样") == "general"
        assert detect_intent("hello") == "general"


class TestMatchCity:
    """测试城市匹配"""

    def test_match_guiyang(self):
        assert match_city("贵阳市南明区") == "贵阳"

    def test_match_zunyi(self):
        assert match_city("遵义市红花岗区") == "遵义"

    def test_match_anshun(self):
        assert match_city("安顺市镇宁县") == "安顺"

    def test_no_match(self):
        assert match_city("北京市朝阳区") is None

    def test_empty_address(self):
        assert match_city("") is None
        assert match_city(None) is None
