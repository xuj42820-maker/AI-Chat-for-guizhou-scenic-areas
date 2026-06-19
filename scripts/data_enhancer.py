"""
贵州景点数据增强器
添加更多景点 + 丰富字段信息
"""

import json
import sqlite3
import os


class DataEnhancer:
    """数据增强器"""

    def __init__(self):
        self.attractions = {}

    def load_data(self):
        """加载现有数据"""
        try:
            with open('data/guizhou_attractions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    name = item.get('name', '')
                    if name:
                        self.attractions[name] = item
            print("已加载 " + str(len(self.attractions)) + " 个景点")
        except Exception as e:
            print("加载失败: " + str(e))

    def add_secret_spots(self):
        """添加小众秘境"""
        print("\n正在添加小众秘境...")

        secret_spots = [
            {
                "name": "加榜梯田",
                "address": "贵州省黔东南苗族侗族自治州从江县加榜乡",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "加榜梯田是中国最好的梯田之一，梯田中散落着苗族吊脚楼，景色如诗如画。日出日落时分，梯田水面反射光芒，美不胜收。",
                "features": "梯田,苗族村寨,田园风光,摄影胜地",
                "rating": 4.7,
                "best_season": "4-6月,9-10月",
                "transportation": "从江县城包车前往，约2小时",
                "tips": "建议住1-2晚，日出日落很美",
                "phone": "0855-6410000",
                "area": "约1万亩",
                "suggested_duration": "1-2天",
                "ticket_booking": "无需预约",
                "discount_policy": "免费开放",
                "weather_tips": "山区多雾，早晚温差大",
                "clothing_tips": "穿舒适运动鞋，带外套",
                "must_bring": "相机、三脚架、保暖衣物",
                "nearby_attractions": "占里侗寨、小黄侗寨",
                "history_culture": "苗族先民开垦千年",
                "best_photo_spots": "加车村观景台、党扭村",
                "night_activities": "星空摄影、苗寨篝火",
                "family_friendly": "适合，需注意安全",
                "team_activities": "可团建、徒步"
            },
            {
                "name": "堂安侗寨",
                "address": "贵州省黔东南苗族侗族自治州黎平县肇兴镇",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "堂安侗寨是中国唯一的侗族生态博物馆，有壮观的梯田和保存完好的侗族建筑。从肇兴徒步到堂安，沿途风景优美。",
                "features": "侗族村寨,梯田,生态博物馆,徒步路线",
                "rating": 4.6,
                "best_season": "4-10月",
                "transportation": "肇兴侗寨步行或包车，约3公里",
                "tips": "建议从肇兴徒步前往，沿途风景好",
                "phone": "0855-6130000",
                "area": "约2平方公里",
                "suggested_duration": "半天",
                "ticket_booking": "无需预约",
                "discount_policy": "免费开放",
                "weather_tips": "山区多雨，带雨具",
                "clothing_tips": "穿防滑鞋",
                "must_bring": "雨具、水、干粮",
                "nearby_attractions": "肇兴侗寨、厦格侗寨",
                "history_culture": "侗族生态博物馆，保存完整",
                "best_photo_spots": "寨门观景台、梯田边",
                "night_activities": "侗族大歌表演",
                "family_friendly": "适合，需注意体力",
                "team_activities": "徒步、摄影团"
            },
            {
                "name": "占里侗寨",
                "address": "贵州省黔东南苗族侗族自治州从江县高增乡",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "占里侗寨有独特的换花草文化和神秘的生育文化，是中国人口文化第一村。这里几乎家家一男一女，被称为计划生育第一村。",
                "features": "侗族村寨,换花草,人口文化,神秘文化",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "从江县城包车前往，约1.5小时",
                "tips": "尊重当地习俗，不要随意打听",
                "phone": "0855-6410000",
                "area": "约1平方公里",
                "suggested_duration": "半天",
                "ticket_booking": "无需预约",
                "discount_policy": "免费开放",
                "weather_tips": "山区气候，带外套",
                "clothing_tips": "穿舒适鞋子",
                "must_bring": "相机、尊重当地文化",
                "nearby_attractions": "小黄侗寨、高增侗寨",
                "history_culture": "换花草传说，神秘生育文化",
                "best_photo_spots": "鼓楼、花桥、禾仓",
                "night_activities": "侗族大歌",
                "family_friendly": "适合",
                "team_activities": "文化考察"
            },
            {
                "name": "小黄侗寨",
                "address": "贵州省黔东南苗族侗族自治州从江县高增乡",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "小黄侗寨是侗族大歌的发源地，被誉为侗歌之乡。这里人人会唱侗歌，有独特的侗族音乐文化。",
                "features": "侗族大歌,音乐文化,非遗,侗歌之乡",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "从江县城包车前往，约1小时",
                "tips": "可请当地村民唱侗歌",
                "phone": "0855-6410000",
                "area": "约1.5平方公里",
                "suggested_duration": "半天",
                "ticket_booking": "无需预约",
                "discount_policy": "免费开放",
                "weather_tips": "山区气候，带外套",
                "clothing_tips": "穿舒适鞋子",
                "must_bring": "录音设备、相机",
                "nearby_attractions": "占里侗寨、高增侗寨",
                "history_culture": "侗族大歌发源地，国家级非遗",
                "best_photo_spots": "鼓楼、歌堂、禾仓",
                "night_activities": "侗族大歌表演",
                "family_friendly": "适合",
                "team_activities": "音乐采风、文化体验"
            },
            {
                "name": "岜沙苗寨",
                "address": "贵州省黔东南苗族侗族自治州从江县丙妹镇",
                "category": "人文景观",
                "ticket_price": "60元",
                "opening_hours": "全天",
                "description": "岜沙苗寨是中国最后一个枪手部落，男子至今仍佩戴火枪，有独特的苗族文化。这里保留着古老的生活方式和习俗。",
                "features": "枪手部落,苗族文化,镰刀剃头,火枪",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "从江县城乘坐班车，约20分钟",
                "tips": "观看表演时不要随意拍照",
                "phone": "0855-6410000",
                "area": "约2平方公里",
                "suggested_duration": "半天",
                "ticket_booking": "现场购票",
                "discount_policy": "学生半价",
                "weather_tips": "山区气候，带外套",
                "clothing_tips": "穿舒适鞋子",
                "must_bring": "相机、现金",
                "nearby_attractions": "从江县城、加榜梯田",
                "history_culture": "最后一个枪手部落，古老习俗",
                "best_photo_spots": "寨门、芦笙堂、古树",
                "night_activities": "苗族歌舞表演",
                "family_friendly": "适合",
                "team_activities": "文化体验、摄影"
            },
            {
                "name": "隆里古城",
                "address": "贵州省黔东南苗族侗族自治州锦屏县隆里乡",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "隆里古城是中国历史文化名城，有600多年历史，是明代军事古城。古城保存完好，有独特的花脸龙文化。",
                "features": "古城,明代军事城堡,花脸龙,历史文化",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "锦屏县城乘坐班车，约30分钟",
                "tips": "春节期间有花脸龙表演",
                "phone": "0855-7220000",
                "area": "约4.8万平方米",
                "suggested_duration": "半天",
                "ticket_booking": "无需预约",
                "discount_policy": "免费开放",
                "weather_tips": "气候温和",
                "clothing_tips": "穿舒适鞋子",
                "must_bring": "相机",
                "nearby_attractions": "锦屏县城、清水江",
                "history_culture": "明代军事古城，600年历史",
                "best_photo_spots": "古城墙、古街、龙标书院",
                "night_activities": "古城夜景",
                "family_friendly": "适合",
                "team_activities": "文化考察、摄影"
            },
            {
                "name": "施秉云台山",
                "address": "贵州省黔东南苗族侗族自治州施秉县",
                "category": "自然风光",
                "ticket_price": "120元",
                "opening_hours": "08:00-16:00",
                "description": "云台山是世界自然遗产，以白云岩喀斯特地貌为主，有云台山、黑冲等多个景区。云海日出是最大看点。",
                "features": "喀斯特地貌,世界遗产,云海,日出",
                "rating": 4.6,
                "best_season": "4-10月",
                "transportation": "施秉县城乘坐旅游专线",
                "tips": "建议早起看云海日出",
                "phone": "0855-4220000",
                "area": "约200平方公里",
                "suggested_duration": "1天",
                "ticket_booking": "美团/携程预约",
                "discount_policy": "学生半价",
                "weather_tips": "山区多雨，带雨具",
                "clothing_tips": "穿防滑鞋，带外套",
                "must_bring": "雨具、保暖衣物、相机",
                "nearby_attractions": "施秉县城、舞阳河",
                "history_culture": "世界自然遗产，地质奇观",
                "best_photo_spots": "云台山观景台、黑冲",
                "night_activities": "星空摄影",
                "family_friendly": "适合，需注意安全",
                "team_activities": "徒步、摄影"
            },
            {
                "name": "镇远舞阳河",
                "address": "贵州省黔东南苗族侗族自治州镇远县",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "舞阳河是镇远古镇的母亲河，河水清澈，两岸风光秀丽。可乘船游览，欣赏两岸古建筑和自然风光。",
                "features": "河流,古镇风光,乘船游览,夜景",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "镇远古镇步行可达",
                "tips": "晚上夜景很美，可乘船游览",
                "phone": "0855-5721096",
                "area": "约10公里河段",
                "suggested_duration": "2-3小时",
                "ticket_booking": "现场购票",
                "discount_policy": "游船另收费",
                "weather_tips": "夏季多雨",
                "clothing_tips": "穿舒适鞋子",
                "must_bring": "相机、防晒用品",
                "nearby_attractions": "镇远古镇、青龙洞",
                "history_culture": "古镇母亲河，千年历史",
                "best_photo_spots": "舞阳河大桥、古码头",
                "night_activities": "夜游舞阳河",
                "family_friendly": "适合",
                "team_activities": "乘船游览"
            },
            {
                "name": "荔波茂兰喀斯特森林",
                "address": "贵州省黔南布依族苗族自治州荔波县",
                "category": "自然风光",
                "ticket_price": "50元",
                "opening_hours": "08:00-16:00",
                "description": "茂兰是中国南方喀斯特世界自然遗产的核心区域，有原始森林、溶洞、暗河等。是户外探险和徒步的好去处。",
                "features": "喀斯特森林,世界遗产,徒步,原始森林",
                "rating": 4.5,
                "best_season": "4-10月",
                "transportation": "荔波县城包车前往，约1小时",
                "tips": "建议请当地向导，带足水和食物",
                "phone": "0854-3619810",
                "area": "约200平方公里",
                "suggested_duration": "1天",
                "ticket_booking": "现场购票",
                "discount_policy": "学生半价",
                "weather_tips": "森林多雨，带雨具",
                "clothing_tips": "穿防滑登山鞋",
                "must_bring": "雨具、水、食物、急救包",
                "nearby_attractions": "荔波小七孔、大七孔",
                "history_culture": "世界自然遗产，生物多样性",
                "best_photo_spots": "青龙潭、金狮洞",
                "night_activities": "无",
                "family_friendly": "不适合幼童",
                "team_activities": "徒步、探险、团建"
            },
            {
                "name": "安顺格凸河",
                "address": "贵州省安顺市紫云苗族布依族自治县",
                "category": "自然风光",
                "ticket_price": "60元",
                "opening_hours": "08:00-16:00",
                "description": "格凸河有壮观的喀斯特地貌，有燕子洞、穿上洞等景点，是户外探险的好去处。有蜘蛛人攀岩表演。",
                "features": "喀斯特地貌,溶洞,攀岩,蜘蛛人",
                "rating": 4.4,
                "best_season": "4-10月",
                "transportation": "紫云县城乘坐班车",
                "tips": "观看蜘蛛人攀岩表演需提前确认时间",
                "phone": "0853-5230000",
                "area": "约70平方公里",
                "suggested_duration": "1天",
                "ticket_booking": "现场购票",
                "discount_policy": "学生半价",
                "weather_tips": "夏季多雨",
                "clothing_tips": "穿防滑鞋",
                "must_bring": "雨具、相机、水",
                "nearby_attractions": "紫云县城、布依族村寨",
                "history_culture": "苗族布依族文化，蜘蛛人传说",
                "best_photo_spots": "燕子洞、穿上洞、格凸河",
                "night_activities": "无",
                "family_friendly": "适合，需注意安全",
                "team_activities": "探险、摄影"
            }
        ]

        added = 0
        for spot in secret_spots:
            name = spot.get('name', '')
            if name and name not in self.attractions:
                self.attractions[name] = spot
                added += 1
                print("  + " + name)
            elif name in self.attractions:
                for key, value in spot.items():
                    if key not in self.attractions[name] or not self.attractions[name][key]:
                        self.attractions[name][key] = value
                print("  ~ " + name)

        print("新增 " + str(added) + " 个小众秘境")

    def enrich_existing_data(self):
        """丰富现有景点数据"""
        print("\n正在丰富现有景点数据...")

        enrichment = {
            "黄果树瀑布": {
                "ticket_booking": "美团/携程/官网预约",
                "discount_policy": "学生半价、1.2米以下儿童免费、60岁以上老人半价",
                "weather_tips": "夏季多雨，瀑布水量大时带雨衣",
                "clothing_tips": "穿防滑鞋，带雨衣",
                "must_bring": "雨衣、防水手机套、防晒霜",
                "nearby_attractions": "天星桥、陡坡塘瀑布、龙宫",
                "history_culture": "明代徐霞客曾到此游览，被誉为中华第一瀑",
                "best_photo_spots": "瀑布正面、水帘洞内、犀牛潭边",
                "night_activities": "无",
                "family_friendly": "适合，有电瓶车",
                "team_activities": "可团建"
            },
            "梵净山": {
                "ticket_booking": "官网预约，需提前1天",
                "discount_policy": "学生半价、1.4米以下儿童免费",
                "weather_tips": "山顶天气多变，带雨具和保暖衣物",
                "clothing_tips": "穿登山鞋，带外套",
                "must_bring": "雨具、保暖衣物、登山杖、水",
                "nearby_attractions": "亚木沟、寨沙侗寨、凤凰古城",
                "history_culture": "佛教名山，弥勒菩萨道场，世界自然遗产",
                "best_photo_spots": "蘑菇石、金顶、红云金顶",
                "night_activities": "无",
                "family_friendly": "不适合幼童和老人",
                "team_activities": "登山、徒步"
            },
            "荔波小七孔": {
                "ticket_booking": "美团/携程预约",
                "discount_policy": "学生半价、1.2米以下儿童免费",
                "weather_tips": "夏季多雨，景区内湿滑",
                "clothing_tips": "穿防滑凉鞋或溯溪鞋",
                "must_bring": "防晒霜、驱蚊水、换洗衣物",
                "nearby_attractions": "大七孔、茂兰喀斯特森林",
                "history_culture": "世界自然遗产，喀斯特地貌典范",
                "best_photo_spots": "小七孔古桥、68级跌水瀑布、水上森林",
                "night_activities": "无",
                "family_friendly": "适合，有电瓶车",
                "team_activities": "可团建"
            },
            "西江千户苗寨": {
                "ticket_booking": "美团/携程预约",
                "discount_policy": "学生半价、1.2米以下儿童免费",
                "weather_tips": "山区多雨，带雨具",
                "clothing_tips": "穿舒适鞋子，可租苗族服饰拍照",
                "must_bring": "相机、充电宝、现金",
                "nearby_attractions": "朗德苗寨、雷山县城",
                "history_culture": "中国最大苗族聚居村寨，千年历史",
                "best_photo_spots": "观景台、苗族博物馆、风雨桥",
                "night_activities": "观景台夜景、苗族歌舞表演、篝火晚会",
                "family_friendly": "适合，有观光车",
                "team_activities": "长桌宴、苗族文化体验"
            },
            "镇远古镇": {
                "ticket_booking": "无需预约",
                "discount_policy": "古镇免费，部分景点收费",
                "weather_tips": "气候温和，夏季多雨",
                "clothing_tips": "穿舒适鞋子",
                "must_bring": "相机、防晒用品",
                "nearby_attractions": "舞阳河、青龙洞、铁溪",
                "history_culture": "2000多年历史，明清古城，太极古城",
                "best_photo_spots": "祝圣桥、青龙洞、舞阳河夜景",
                "night_activities": "夜游舞阳河、古城夜景",
                "family_friendly": "适合",
                "team_activities": "古城漫步、文化体验"
            },
            "遵义会议会址": {
                "ticket_booking": "微信公众号预约",
                "discount_policy": "免费开放",
                "weather_tips": "遵义气候温和",
                "clothing_tips": "穿着得体",
                "must_bring": "身份证、相机",
                "nearby_attractions": "红军山、遵义古城、海龙屯",
                "history_culture": "遵义会议是中国革命的重要转折点",
                "best_photo_spots": "会议楼、陈列馆、红军山",
                "night_activities": "遵义古城夜景",
                "family_friendly": "适合，爱国教育",
                "team_activities": "党建活动、红色教育"
            },
            "青岩古镇": {
                "ticket_booking": "无需预约",
                "discount_policy": "古镇免费，部分景点联票60元",
                "weather_tips": "贵阳气候宜人",
                "clothing_tips": "穿舒适鞋子",
                "must_bring": "相机、现金",
                "nearby_attractions": "花溪公园、天河潭",
                "history_culture": "始建于明代，600多年历史，贵州四大古镇之一",
                "best_photo_spots": "古城墙、石板路、背街、万寿宫",
                "night_activities": "古镇夜景",
                "family_friendly": "适合",
                "team_activities": "美食之旅、文化体验"
            },
            "织金洞": {
                "ticket_booking": "美团/携程预约",
                "discount_policy": "学生半价、1.2米以下儿童免费",
                "weather_tips": "洞内恒温14-16度，带外套",
                "clothing_tips": "穿防滑鞋，带外套",
                "must_bring": "外套、相机",
                "nearby_attractions": "织金古城、织金大峡谷",
                "history_culture": "世界地质公园，岩溶博物馆",
                "best_photo_spots": "霸王盔、银雨树、水晶宫",
                "night_activities": "无",
                "family_friendly": "适合，有电梯",
                "team_activities": "可团建"
            },
            "马岭河峡谷": {
                "ticket_booking": "美团/携程预约",
                "discount_policy": "学生半价、1.2米以下儿童免费",
                "weather_tips": "夏季多雨，峡谷内凉爽",
                "clothing_tips": "穿防滑鞋，带雨衣",
                "must_bring": "雨衣、防水手机套、换洗衣物",
                "nearby_attractions": "万峰林、万峰湖",
                "history_culture": "被誉为地球上最美丽的伤疤",
                "best_photo_spots": "峡谷瀑布群、漂流途中",
                "night_activities": "无",
                "family_friendly": "适合，有电梯下谷底",
                "team_activities": "漂流、探险"
            },
            "万峰林": {
                "ticket_booking": "美团/携程预约",
                "discount_policy": "学生半价、1.2米以下儿童免费",
                "weather_tips": "兴义气候宜人，四季如春",
                "clothing_tips": "穿舒适鞋子，带防晒用品",
                "must_bring": "相机、防晒霜、水",
                "nearby_attractions": "马岭河峡谷、万峰湖、双乳峰",
                "history_culture": "徐霞客曾到此，赞为天下山峰何其多，唯有此处峰成林",
                "best_photo_spots": "八卦田、纳灰村、观景台",
                "night_activities": "无",
                "family_friendly": "适合，有观光车和骑行道",
                "team_activities": "骑行、摄影、团建"
            }
        }

        updated = 0
        for name, extra in enrichment.items():
            if name in self.attractions:
                self.attractions[name].update(extra)
                updated += 1
                print("  ~ " + name)

        print("丰富 " + str(updated) + " 个景点数据")

    def save_data(self):
        """保存数据"""
        data_list = list(self.attractions.values())

        # 保存JSON
        with open('data/guizhou_attractions.json', 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        print("\n已保存 " + str(len(data_list)) + " 个景点到 JSON")

        # 保存到数据库
        db_path = 'data/attractions.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 删除旧表创建新表
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
                ticket_booking TEXT,
                discount_policy TEXT,
                weather_tips TEXT,
                clothing_tips TEXT,
                must_bring TEXT,
                nearby_attractions TEXT,
                nearby_hotels TEXT,
                nearby_restaurants TEXT,
                history_culture TEXT,
                best_photo_spots TEXT,
                night_activities TEXT,
                family_friendly TEXT,
                team_activities TEXT,
                special_events TEXT,
                photography_tips TEXT,
                accessibility TEXT,
                crowd_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 插入数据
        for attr in data_list:
            cursor.execute('''
                INSERT INTO attractions (
                    name, address, category, ticket_price, opening_hours,
                    description, features, rating, best_season, transportation,
                    tips, phone, official_website, area, suggested_duration,
                    ticket_booking, discount_policy, weather_tips, clothing_tips,
                    must_bring, nearby_attractions, nearby_hotels, nearby_restaurants,
                    history_culture, best_photo_spots, night_activities,
                    family_friendly, team_activities, special_events,
                    photography_tips, accessibility, crowd_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                attr.get('ticket_booking'),
                attr.get('discount_policy'),
                attr.get('weather_tips'),
                attr.get('clothing_tips'),
                attr.get('must_bring'),
                attr.get('nearby_attractions'),
                attr.get('nearby_hotels'),
                attr.get('nearby_restaurants'),
                attr.get('history_culture'),
                attr.get('best_photo_spots'),
                attr.get('night_activities'),
                attr.get('family_friendly'),
                attr.get('team_activities'),
                attr.get('special_events'),
                attr.get('photography_tips'),
                attr.get('accessibility'),
                attr.get('crowd_level')
            ))

        conn.commit()
        conn.close()
        print("已保存到数据库")

    def print_statistics(self):
        """打印统计"""
        data_list = list(self.attractions.values())
        total = len(data_list)

        print("\n" + "=" * 60)
        print("数据统计")
        print("=" * 60)

        # 按类别
        categories = {}
        for attr in data_list:
            cat = attr.get('category', '其他')
            categories[cat] = categories.get(cat, 0) + 1

        print("\n按类别：")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print("  " + cat + ": " + str(count) + " 个")

        # 按地区
        regions = {}
        for attr in data_list:
            addr = attr.get('address', '')
            region = '其他'
            for key in ['贵阳', '遵义', '安顺', '黔东南', '黔南', '黔西南', '铜仁', '毕节', '六盘水']:
                if key in addr:
                    region = key
                    break
            regions[region] = regions.get(region, 0) + 1

        print("\n按地区：")
        for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
            print("  " + region + ": " + str(count) + " 个")

        # 字段丰富度
        fields = ['phone', 'ticket_booking', 'discount_policy', 'weather_tips',
                  'clothing_tips', 'must_bring', 'nearby_attractions',
                  'history_culture', 'best_photo_spots', 'night_activities',
                  'family_friendly', 'team_activities']

        print("\n字段丰富度：")
        for field in fields:
            count = sum(1 for attr in data_list if attr.get(field))
            print("  " + field + ": " + str(count) + " 个")

        print("\n总计: " + str(total) + " 个景点")

    def run(self):
        """运行"""
        print("=" * 60)
        print("贵州景点数据增强器")
        print("=" * 60)

        self.load_data()
        self.add_secret_spots()
        self.enrich_existing_data()
        self.save_data()
        self.print_statistics()

        print("\n" + "=" * 60)
        print("数据增强完成！")
        print("=" * 60)


if __name__ == '__main__':
    enhancer = DataEnhancer()
    enhancer.run()
