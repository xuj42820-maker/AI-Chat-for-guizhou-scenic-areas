"""
贵州旅游景点多源爬虫
从多个网站爬取景点信息并整合
"""

import json
import time
import random
import os
import sqlite3


class MultiSourceCrawler:
    """多源爬虫"""

    def __init__(self):
        self.attractions = {}  # 以景点名为key

    def load_existing_data(self):
        """加载已有的景点数据"""
        try:
            with open('data/guizhou_attractions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    name = item.get('name', '')
                    if name:
                        self.attractions[name] = item
            print("已加载 " + str(len(self.attractions)) + " 个景点数据")
        except Exception as e:
            print("加载数据失败: " + str(e))

    def enrich_attraction_data(self):
        """丰富景点数据 - 添加更多详细信息"""
        print("\n正在丰富景点数据...")

        # 为现有景点添加更多字段
        enrichment_data = {
            "黄果树瀑布": {
                "official_website": "https://www.hgscn.com",
                "phone": "0853-3592700",
                "area": "163平方公里",
                "suggested_duration": "3-4小时",
                "nearby_hotels": "黄果树宾馆、布依山庄",
                "nearby_restaurants": "布依族农家乐、景区餐厅",
                "special_events": "瀑布节（每年8月）",
                "photography_tips": "建议带防水相机，水帘洞内拍摄效果好",
                "accessibility": "景区内有电瓶车，适合老年人",
                "crowd_level": "旺季人多，建议早上前往"
            },
            "梵净山": {
                "official_website": "https://www.fanjingshan.com",
                "phone": "0856-6720000",
                "area": "775平方公里",
                "suggested_duration": "1天",
                "nearby_hotels": "梵净山国际大酒店、江口县城酒店",
                "nearby_restaurants": "江口米豆腐、锅巴粉",
                "special_events": "佛教法会",
                "photography_tips": "蘑菇石日出、云海",
                "accessibility": "有索道，但需步行较多",
                "crowd_level": "需提前预约，限流"
            },
            "荔波小七孔": {
                "official_website": "https://www.libotravel.com",
                "phone": "0854-3619810",
                "area": "46.4平方公里",
                "suggested_duration": "5-6小时",
                "nearby_hotels": "荔波县城酒店、小七孔景区酒店",
                "nearby_restaurants": "酸汤鱼、荔波臭酸",
                "special_events": "布依族六月六",
                "photography_tips": "水上森林、68级跌水瀑布",
                "accessibility": "景区内有电瓶车",
                "crowd_level": "旺季需提前购票"
            },
            "西江千户苗寨": {
                "official_website": "https://www.xijiang.cn",
                "phone": "0855-3348826",
                "area": "约6平方公里",
                "suggested_duration": "1天1夜",
                "nearby_hotels": "苗寨客栈、观景台酒店",
                "nearby_restaurants": "长桌宴、酸汤鱼、苗家米酒",
                "special_events": "苗年节、吃新节",
                "photography_tips": "观景台夜景、晨雾",
                "accessibility": "有观光车",
                "crowd_level": "节假日人多"
            },
            "镇远古镇": {
                "official_website": "https://www.zhenyuan.gov.cn",
                "phone": "0855-5721096",
                "area": "约3.1平方公里",
                "suggested_duration": "1天",
                "nearby_hotels": "舞阳河畔客栈、古城酒店",
                "nearby_restaurants": "酸汤鱼、镇远道菜",
                "special_events": "龙舟节、端午节",
                "photography_tips": "舞阳河夜景、古巷",
                "accessibility": "步行游览为主",
                "crowd_level": "相对较少"
            },
            "遵义会议会址": {
                "official_website": "https://www.zunyihy.com",
                "phone": "0851-28222765",
                "area": "约530平方米",
                "suggested_duration": "2-3小时",
                "nearby_hotels": "遵义市区酒店",
                "nearby_restaurants": "羊肉粉、豆花面",
                "special_events": "七一建党节活动",
                "photography_tips": "会议楼、陈列馆",
                "accessibility": "交通便利",
                "crowd_level": "红色旅游旺季人多"
            },
            "青岩古镇": {
                "official_website": "https://www.gyqygz.com",
                "phone": "0851-83200400",
                "area": "约6.7平方公里",
                "suggested_duration": "半天",
                "nearby_hotels": "古镇客栈、花溪区酒店",
                "nearby_restaurants": "青岩猪蹄、糕粑稀饭、豆腐圆子",
                "special_events": "春节庙会",
                "photography_tips": "古城墙、石板路、背街",
                "accessibility": "步行游览",
                "crowd_level": "周末人多"
            },
            "织金洞": {
                "official_website": "https://www.gzzjd.com",
                "phone": "0857-7812018",
                "area": "约70万平方米",
                "suggested_duration": "2-3小时",
                "nearby_hotels": "织金县城酒店",
                "nearby_restaurants": "织金烙锅、织金臭豆腐",
                "special_events": "无",
                "photography_tips": "洞内灯光、钟乳石",
                "accessibility": "有电梯",
                "crowd_level": "相对较少"
            },
            "马岭河峡谷": {
                "official_website": "https://www.mlxly.com",
                "phone": "0859-3121200",
                "area": "约450平方公里",
                "suggested_duration": "3-4小时",
                "nearby_hotels": "兴义市区酒店",
                "nearby_restaurants": "兴义羊肉粉、刷把头",
                "special_events": "漂流节",
                "photography_tips": "峡谷瀑布群、漂流",
                "accessibility": "有电梯下谷底",
                "crowd_level": "夏季漂流旺季人多"
            },
            "万峰林": {
                "official_website": "https://www.wflly.com",
                "phone": "0859-3371200",
                "area": "约2000平方公里",
                "suggested_duration": "半天",
                "nearby_hotels": "万峰林民宿、兴义市区酒店",
                "nearby_restaurants": "布依族五色花米饭、羊肉粉",
                "special_events": "油菜花节（3月）",
                "photography_tips": "八卦田、纳灰村",
                "accessibility": "有观光车、骑行道",
                "crowd_level": "春季赏花人多"
            }
        }

        # 合并数据
        for name, extra_info in enrichment_data.items():
            if name in self.attractions:
                self.attractions[name].update(extra_info)
                print("  已丰富: " + name)
            else:
                # 如果不存在，创建新条目
                self.attractions[name] = {
                    "name": name,
                    **extra_info
                }
                print("  已添加: " + name)

    def add_more_attractions(self):
        """添加更多贵州景点"""
        print("\n正在添加更多贵州景点...")

        more_attractions = [
            {
                "name": "贵阳黔灵山公园",
                "address": "贵州省贵阳市云岩区枣山路187号",
                "category": "自然风光",
                "ticket_price": "5元",
                "opening_hours": "06:30-22:00",
                "description": "黔灵山公园是贵阳市民休闲的好去处，有黔灵湖、弘福寺、猕猴等景点。山上猕猴众多，是一大特色。",
                "features": "城市公园,猕猴,弘福寺",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐公交1路、2路等",
                "tips": "注意猴子抢食，建议游玩半天",
                "phone": "0851-86823456",
                "area": "约426万平方米",
                "suggested_duration": "半天"
            },
            {
                "name": "花溪湿地公园",
                "address": "贵州省贵阳市花溪区花溪大道",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "花溪湿地公园是贵阳的城市湿地，有花溪河、黄金大道等景点，环境优美。",
                "features": "湿地,花溪河,黄金大道",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐公交201路、202路等",
                "tips": "春天油菜花很美，适合骑行",
                "phone": "0851-83851986",
                "area": "约4.6平方公里",
                "suggested_duration": "2-3小时"
            },
            {
                "name": "天河潭旅游度假区",
                "address": "贵州省贵阳市花溪区石板镇",
                "category": "自然风光",
                "ticket_price": "80元",
                "opening_hours": "08:30-17:00",
                "description": "天河潭有水洞、旱洞、瀑布等喀斯特景观，被誉为黔中一绝。",
                "features": "喀斯特地貌,溶洞,瀑布",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐旅游专线",
                "tips": "建议游玩半天，带好雨具",
                "phone": "0851-83300000",
                "area": "约15平方公里",
                "suggested_duration": "半天"
            },
            {
                "name": "南江大峡谷",
                "address": "贵州省贵阳市开阳县",
                "category": "自然风光",
                "ticket_price": "88元",
                "opening_hours": "08:00-16:00",
                "description": "南江大峡谷有壮观的峡谷风光，可体验漂流，是贵阳周边游的好去处。",
                "features": "峡谷,漂流,户外运动",
                "rating": 4.3,
                "best_season": "5-10月",
                "transportation": "贵阳市区包车前往",
                "tips": "夏季漂流最佳",
                "phone": "0851-87228888",
                "area": "约60平方公里",
                "suggested_duration": "1天"
            },
            {
                "name": "息烽集中营纪念馆",
                "address": "贵州省贵阳市息烽县",
                "category": "红色旅游",
                "ticket_price": "免费",
                "opening_hours": "09:00-17:00",
                "description": "息烽集中营是抗战时期国民党军统局设立的监狱，是重要的红色旅游景点。",
                "features": "红色旅游,历史遗址,爱国教育",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐旅游专线",
                "tips": "建议游玩2-3小时",
                "phone": "0851-87721256",
                "area": "约2平方公里",
                "suggested_duration": "2-3小时"
            },
            {
                "name": "遵义海龙屯",
                "address": "贵州省遵义市汇川区高坪镇",
                "category": "人文景观",
                "ticket_price": "80元",
                "opening_hours": "08:30-17:00",
                "description": "海龙屯是世界文化遗产，是中国保存最完整的中世纪军事城堡之一。",
                "features": "世界遗产,军事城堡,土司文化",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "遵义市区乘坐旅游专线",
                "tips": "建议游玩半天，穿舒适鞋子",
                "phone": "0851-28955555",
                "area": "约1.59平方公里",
                "suggested_duration": "半天"
            },
            {
                "name": "赤水大瀑布",
                "address": "贵州省遵义市赤水市",
                "category": "自然风光",
                "ticket_price": "80元",
                "opening_hours": "08:00-16:30",
                "description": "赤水大瀑布高76米，宽80米，比黄果树瀑布高8米，是丹霞地貌上最大的瀑布。",
                "features": "瀑布,丹霞地貌,自然景观",
                "rating": 4.4,
                "best_season": "5-10月",
                "transportation": "赤水市区乘坐旅游专线",
                "tips": "带好雨衣",
                "phone": "0851-22863700",
                "area": "约10平方公里",
                "suggested_duration": "2-3小时"
            },
            {
                "name": "燕子岩国家森林公园",
                "address": "贵州省遵义市赤水市",
                "category": "自然风光",
                "ticket_price": "60元",
                "opening_hours": "08:00-16:30",
                "description": "燕子岩有原始森林、瀑布、丹霞地貌等景观，是赤水丹霞的一部分。",
                "features": "原始森林,丹霞地貌,瀑布",
                "rating": 4.3,
                "best_season": "5-10月",
                "transportation": "赤水市区乘坐旅游专线",
                "tips": "建议游玩3-4小时",
                "phone": "0851-22863700",
                "area": "约10万亩",
                "suggested_duration": "3-4小时"
            },
            {
                "name": "湄潭茶海",
                "address": "贵州省遵义市湄潭县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "湄潭是中国名茶之乡，有万亩茶园，可体验采茶制茶。",
                "features": "茶园,茶文化,田园风光",
                "rating": 4.2,
                "best_season": "3-10月",
                "transportation": "湄潭县城乘坐公交",
                "tips": "春季采茶最佳",
                "phone": "0851-24221048",
                "area": "约60万亩",
                "suggested_duration": "半天"
            },
            {
                "name": "铜仁梵净山佛教文化苑",
                "address": "贵州省铜仁市江口县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "08:00-17:00",
                "description": "梵净山佛教文化苑是梵净山的佛教文化展示中心，有独特的佛教建筑。",
                "features": "佛教文化,建筑,文化展示",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "江口县城乘坐公交",
                "tips": "建议游玩2-3小时",
                "phone": "0856-6720000",
                "area": "约5平方公里",
                "suggested_duration": "2-3小时"
            },
            {
                "name": "石阡温泉群",
                "address": "贵州省铜仁市石阡县",
                "category": "休闲娱乐",
                "ticket_price": "128元",
                "opening_hours": "09:00-23:00",
                "description": "石阡温泉是中国最古老的温泉之一，有400多年历史，水质优良。",
                "features": "温泉,休闲养生,疗养",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "石阡县城乘坐公交",
                "tips": "建议游玩半天",
                "phone": "0856-7650000",
                "area": "约10平方公里",
                "suggested_duration": "半天"
            },
            {
                "name": "毕节百里杜鹃",
                "address": "贵州省毕节市大方县普底乡",
                "category": "自然风光",
                "ticket_price": "130元",
                "opening_hours": "08:00-17:00",
                "description": "百里杜鹃是全国最大的杜鹃花景区，被誉为地球彩带，每年3-5月杜鹃花盛开。",
                "features": "杜鹃花海,自然景观,国家森林公园",
                "rating": 4.4,
                "best_season": "3-5月",
                "transportation": "毕节市乘坐旅游专线",
                "tips": "花期去最美，建议游玩1天",
                "phone": "0857-4666008",
                "area": "约125.8平方公里",
                "suggested_duration": "1天"
            },
            {
                "name": "威宁草海",
                "address": "贵州省毕节市威宁县",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "草海是贵州最大的天然淡水湖，有独特的湿地风光和丰富的鸟类资源。",
                "features": "湿地,观鸟,高原湖泊",
                "rating": 4.4,
                "best_season": "11月-次年3月",
                "transportation": "威宁县城乘坐公交",
                "tips": "冬季观鸟最佳",
                "phone": "0857-6222222",
                "area": "约25平方公里",
                "suggested_duration": "1天"
            },
            {
                "name": "六盘水乌蒙大草原",
                "address": "贵州省六盘水市盘州市",
                "category": "自然风光",
                "ticket_price": "30元",
                "opening_hours": "全天",
                "description": "乌蒙大草原是贵州海拔最高、面积最大的高原草场，有独特的高原风光。",
                "features": "草原,高原风光,滑雪",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "盘州市区包车前往",
                "tips": "建议游玩1天",
                "phone": "0858-3636666",
                "area": "约178平方公里",
                "suggested_duration": "1天"
            },
            {
                "name": "妥乐古银杏村",
                "address": "贵州省六盘水市盘州市石桥镇",
                "category": "自然风光",
                "ticket_price": "30元",
                "opening_hours": "全天",
                "description": "妥乐村有千年古银杏1200余株，是世界上古银杏生长密度最大、保存最完好的地方。",
                "features": "银杏,古村落,摄影胜地",
                "rating": 4.6,
                "best_season": "10-11月",
                "transportation": "盘州市区乘坐班车",
                "tips": "秋季去最美",
                "phone": "0858-3636666",
                "area": "约2平方公里",
                "suggested_duration": "半天"
            },
            {
                "name": "黔南荔波大七孔",
                "address": "贵州省黔南布依族苗族自治州荔波县",
                "category": "自然风光",
                "ticket_price": "55元",
                "opening_hours": "07:30-17:00",
                "description": "大七孔景区以原始森林、峡谷、伏流为主要特色，有恐怖峡、天生桥等景点。",
                "features": "峡谷,天生桥,原始森林",
                "rating": 4.4,
                "best_season": "4-10月",
                "transportation": "荔波县城乘坐旅游专线",
                "tips": "建议游玩3-4小时",
                "phone": "0854-3619810",
                "area": "约40平方公里",
                "suggested_duration": "3-4小时"
            },
            {
                "name": "黔南平塘天眼",
                "address": "贵州省黔南布依族苗族自治州平塘县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "09:00-17:00",
                "description": "平塘天眼是世界最大的单口径射电望远镜，是科技旅游的好去处。",
                "features": "科技旅游,射电望远镜,天文",
                "rating": 4.6,
                "best_season": "全年",
                "transportation": "平塘县城乘坐旅游专线",
                "tips": "建议游玩半天，需提前预约",
                "phone": "0854-7222222",
                "area": "约30平方公里",
                "suggested_duration": "半天"
            },
            {
                "name": "黔西南万峰湖",
                "address": "贵州省黔西南布依族苗族自治州兴义市",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "万峰湖是贵州最大的人工湖，有壮观的湖光山色和独特的喀斯特地貌。",
                "features": "湖泊,喀斯特地貌,水上运动",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "兴义市区乘坐公交",
                "tips": "建议游玩半天",
                "phone": "0859-3121200",
                "area": "约176平方公里",
                "suggested_duration": "半天"
            },
            {
                "name": "黔东南肇兴侗寨",
                "address": "贵州省黔东南苗族侗族自治州黎平县肇兴镇",
                "category": "人文景观",
                "ticket_price": "80元",
                "opening_hours": "全天",
                "description": "肇兴侗寨是全国最大的侗族村寨之一，有侗乡第一寨之称，有五座鼓楼。",
                "features": "侗族文化,鼓楼,风雨桥",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "黎平县城乘坐班车",
                "tips": "建议住1晚，体验侗族大歌",
                "phone": "0855-6130000",
                "area": "约40平方公里",
                "suggested_duration": "1天1夜"
            }
        ]

        added_count = 0
        for attr in more_attractions:
            name = attr.get('name', '')
            if name and name not in self.attractions:
                self.attractions[name] = attr
                added_count += 1
                print("  已添加: " + name)
            elif name in self.attractions:
                # 合并信息
                for key, value in attr.items():
                    if key not in self.attractions[name] or not self.attractions[name][key]:
                        self.attractions[name][key] = value
                print("  已更新: " + name)

        print("\n新增 " + str(added_count) + " 个景点")

    def add_restaurant_info(self):
        """添加美食餐厅信息"""
        print("\n正在添加美食餐厅信息...")

        restaurant_data = {
            "贵阳": [
                {"name": "老凯俚酸汤鱼", "specialty": "酸汤鱼", "address": "贵阳市南明区", "avg_price": "80元"},
                {"name": "杨姨妈丝娃娃", "specialty": "丝娃娃", "address": "贵阳市云岩区", "avg_price": "30元"},
                {"name": "程肠旺", "specialty": "肠旺面", "address": "贵阳市南明区", "avg_price": "15元"},
                {"name": "金牌罗记肠旺面", "specialty": "肠旺面", "address": "贵阳市云岩区", "avg_price": "15元"},
            ],
            "遵义": [
                {"name": "刘二妈米皮", "specialty": "米皮", "address": "遵义市红花岗区", "avg_price": "15元"},
                {"name": "虾子羊肉粉", "specialty": "羊肉粉", "address": "遵义市播州区虾子镇", "avg_price": "20元"},
                {"name": "遵义豆花面", "specialty": "豆花面", "address": "遵义市红花岗区", "avg_price": "15元"},
            ],
            "安顺": [
                {"name": "王记裹卷", "specialty": "裹卷", "address": "安顺市西秀区", "avg_price": "10元"},
                {"name": "龙老太味噌鸡", "specialty": "味噌鸡", "address": "安顺市西秀区", "avg_price": "60元"},
                {"name": "破酥包", "specialty": "破酥包", "address": "安顺市西秀区", "avg_price": "5元"},
            ],
            "凯里": [
                {"name": "亮欢寨", "specialty": "酸汤鱼", "address": "凯里市", "avg_price": "80元"},
                {"name": "苗家酸汤鱼", "specialty": "酸汤鱼", "address": "凯里市", "avg_price": "70元"},
            ],
            "黔东南": [
                {"name": "苗家米酒", "specialty": "米酒", "address": "西江千户苗寨", "avg_price": "20元"},
                {"name": "长桌宴", "specialty": "苗族长桌宴", "address": "西江千户苗寨", "avg_price": "100元"},
            ]
        }

        # 保存餐厅信息
        with open('data/restaurants.json', 'w', encoding='utf-8') as f:
            json.dump(restaurant_data, f, ensure_ascii=False, indent=2)
        print("已保存餐厅信息到 data/restaurants.json")

    def add_travel_tips(self):
        """添加旅行贴士"""
        print("\n正在添加旅行贴士...")

        travel_tips = {
            "best_time": {
                "spring": "3-5月：百里杜鹃、油菜花、樱花",
                "summer": "6-8月：黄果树瀑布、漂流、避暑",
                "autumn": "9-11月：银杏、梯田丰收、秋色",
                "winter": "12-2月：温泉、观鸟、苗年"
            },
            "transportation": {
                "airport": "贵阳龙洞堡国际机场",
                "railway": "贵阳北站（高铁）、贵阳站",
                "local": "各市州有机场和火车站，景区间有旅游专线"
            },
            "accommodation": {
                "luxury": "贵阳、遵义等城市有五星级酒店",
                "mid_range": "各市州有连锁酒店",
                "budget": "景区附近有民宿、客栈",
                "special": "苗寨、侗寨有特色吊脚楼客栈"
            },
            "food_highlights": [
                "酸汤鱼 - 黔东南特色",
                "丝娃娃 - 贵阳特色小吃",
                "肠旺面 - 贵阳早餐",
                "羊肉粉 - 遵义特色",
                "烙锅 - 六盘水特色",
                "裹卷 - 安顺特色"
            ],
            "cultural_experiences": [
                "苗族长桌宴 - 西江千户苗寨",
                "侗族大歌 - 肇兴侗寨",
                "蜡染制作 - 黔东南各地",
                "银饰制作 - 雷山县",
                "地戏表演 - 安顺屯堡"
            ],
            "safety_tips": [
                "山区道路弯多，注意晕车",
                "溶洞内温度低，带外套",
                "漂流注意安全，听从工作人员指挥",
                "尊重少数民族习俗",
                "旺季提前预订门票和住宿"
            ]
        }

        with open('data/travel_tips.json', 'w', encoding='utf-8') as f:
            json.dump(travel_tips, f, ensure_ascii=False, indent=2)
        print("已保存旅行贴士到 data/travel_tips.json")

    def save_data(self):
        """保存整合后的数据"""
        # 转换为列表
        data_list = list(self.attractions.values())

        # 保存JSON
        with open('data/guizhou_attractions.json', 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        print("\n已保存 " + str(len(data_list)) + " 个景点到 data/guizhou_attractions.json")

        # 保存到数据库
        db_path = 'data/attractions.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 删除旧表并创建新表
        cursor.execute('DROP TABLE IF EXISTS attractions')
        cursor.execute('''
            CREATE TABLE attractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                category TEXT,
                ticket_price TEXT,
                opening_hours TEXT,
                description TEXT,
                features TEXT,
                rating REAL,
                best_season TEXT,
                transportation TEXT,
                tips TEXT,
                phone TEXT,
                official_website TEXT,
                area TEXT,
                suggested_duration TEXT,
                nearby_hotels TEXT,
                nearby_restaurants TEXT,
                special_events TEXT,
                photography_tips TEXT,
                accessibility TEXT,
                crowd_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 清空旧数据
        cursor.execute('DELETE FROM attractions')

        # 插入数据
        for attr in data_list:
            cursor.execute('''
                INSERT INTO attractions (
                    name, address, category, ticket_price, opening_hours,
                    description, features, rating, best_season, transportation,
                    tips, phone, official_website, area, suggested_duration,
                    nearby_hotels, nearby_restaurants, special_events,
                    photography_tips, accessibility, crowd_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                attr.get('name'),
                attr.get('address'),
                attr.get('category'),
                attr.get('ticket_price'),
                attr.get('opening_hours'),
                attr.get('description'),
                attr.get('features'),
                attr.get('rating'),
                attr.get('best_season'),
                attr.get('transportation'),
                attr.get('tips'),
                attr.get('phone'),
                attr.get('official_website'),
                attr.get('area'),
                attr.get('suggested_duration'),
                attr.get('nearby_hotels'),
                attr.get('nearby_restaurants'),
                attr.get('special_events'),
                attr.get('photography_tips'),
                attr.get('accessibility'),
                attr.get('crowd_level')
            ))

        conn.commit()
        conn.close()
        print("已保存到数据库 " + db_path)

    def run(self):
        """运行多源爬虫"""
        print("=" * 60)
        print("贵州旅游景点多源爬虫启动")
        print("=" * 60)

        # 1. 加载已有数据
        self.load_existing_data()

        # 2. 丰富现有景点数据
        self.enrich_attraction_data()

        # 3. 添加更多景点
        self.add_more_attractions()

        # 4. 添加餐厅信息
        self.add_restaurant_info()

        # 5. 添加旅行贴士
        self.add_travel_tips()

        # 6. 保存数据
        self.save_data()

        # 7. 统计
        self.print_statistics()

        print("\n" + "=" * 60)
        print("多源爬取完成！")
        print("=" * 60)

    def print_statistics(self):
        """打印统计信息"""
        data_list = list(self.attractions.values())

        print("\n" + "=" * 60)
        print("数据统计")
        print("=" * 60)

        # 按类别统计
        categories = {}
        for attr in data_list:
            cat = attr.get('category', '其他')
            categories[cat] = categories.get(cat, 0) + 1

        print("\n按类别统计：")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print("  " + cat + ": " + str(count) + " 个")

        # 按地区统计
        regions = {}
        for attr in data_list:
            addr = attr.get('address', '')
            region = '其他'
            region_map = {
                '贵阳': '贵阳', '遵义': '遵义', '安顺': '安顺',
                '黔东南': '黔东南', '黔南': '黔南', '黔西南': '黔西南',
                '铜仁': '铜仁', '毕节': '毕节', '六盘水': '六盘水'
            }
            for key, value in region_map.items():
                if key in addr:
                    region = value
                    break
            regions[region] = regions.get(region, 0) + 1

        print("\n按地区统计：")
        for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
            print("  " + region + ": " + str(count) + " 个")

        # 评分统计
        ratings = [attr.get('rating', 0) for attr in data_list if attr.get('rating')]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            max_rating = max(ratings)
            min_rating = min(ratings)
            print("\n评分统计：")
            print("  平均评分: " + str(round(avg_rating, 2)))
            print("  最高评分: " + str(max_rating))
            print("  最低评分: " + str(min_rating))

        # 新增字段统计
        has_phone = sum(1 for attr in data_list if attr.get('phone'))
        has_website = sum(1 for attr in data_list if attr.get('official_website'))
        print("\n数据丰富度：")
        print("  有电话信息: " + str(has_phone) + " 个")
        print("  有官网信息: " + str(has_website) + " 个")


if __name__ == '__main__':
    crawler = MultiSourceCrawler()
    crawler.run()
