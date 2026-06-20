"""
意图识别模块 — 基于关键词的用户意图分类

职责：
- 将用户查询分类为 15 种意图之一
- 提取城市名等实体信息

新增意图只需：
1. 在 INTENTS 字典中添加关键词列表
2. 在 generator.py 中添加对应的回答模板
"""

# 意图定义：意图名 → 关键词列表
# 新增意图只需在这里加一行
# 注意：route 意图必须在 recommend 之前，因为"推荐路线"应该优先识别为路线推荐
INTENTS = {
    'ticket':     ['门票', '多少钱', '价格', '票价', '收费', '费用'],
    'hours':      ['开放', '时间', '几点', '营业', '关门', '开门'],
    'address':    ['地址', '在哪', '位置', '怎么找', '地方'],
    'transport':  ['交通', '怎么去', '坐车', '自驾', '高铁', '飞机', '到达'],
    'phone':      ['电话', '联系', '客服', '咨询'],
    'season':     ['季节', '什么时候', '几月', '最佳时间', '适合'],
    'free':       ['免费', '不要钱', '免票'],
    'route':      ['路线', '行程', '日游', '几日游', '旅游路线', '自由行', '跟团'],
    'recommend':  ['推荐', '好玩', '值得', '必去', '最好'],
    'food':       ['美食', '好吃', '小吃', '特色菜', '酸汤', '粉', '餐厅', '饭店', '推荐吃', '吃什么'],
    'duration':   ['玩多久', '几天', '时长', '时间够'],
    'nearby':     ['附近', '周边', '旁边'],
    'photo':      ['拍照', '摄影', '照片', '打卡'],
    'tips':       ['贴士', '攻略', '注意', '建议', '准备', '行李', '住宿', '酒店'],
    'culture':    ['文化', '民俗', '民族', '习俗', '体验', '非遗', '苗族', '侗族'],
    'safety':     ['安全', '危险', '提醒', '避坑', '防骗'],
}

# 贵州省主要城市（单一来源）
CITIES = ['贵阳', '遵义', '安顺', '凯里', '黔东南', '黔南', '黔西南', '铜仁', '毕节', '六盘水']


def detect_intent(query):
    """
    识别用户查询意图

    Args:
        query: 用户输入的查询文本

    Returns:
        意图字符串，如 'ticket', 'hours', 'general' 等
    """
    q = query.lower()
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            if kw in q:
                return intent
    return 'general'


def match_city(address):
    """
    从地址中匹配城市名

    Args:
        address: 景点地址文本

    Returns:
        城市名字符串，或 None
    """
    if not address:
        return None
    for city in CITIES:
        if city in address:
            return city
    return None
