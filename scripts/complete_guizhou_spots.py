"""
贵州景点大全 - 尽量找完所有景点
"""

import json
import sqlite3


def add_all_guizhou_spots():
    """添加贵州所有景点"""

    # 加载现有数据
    with open('data/guizhou_attractions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing_names = set(attr.get('name', '') for attr in data)
    print("现有景点: " + str(len(data)) + " 个")

    # 贵州所有景点列表
    all_spots = [
        # ==================== 贵阳市 ====================
        {
            "name": "黔灵山公园",
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
            "phone": "0851-86823456"
        },
        {
            "name": "花溪公园",
            "address": "贵州省贵阳市花溪区花溪大道",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "花溪公园是贵阳的著名公园，有花溪河、黄金大道等景点，环境优美。",
            "features": "城市公园,花溪河,黄金大道",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "贵阳市区乘坐公交201路、202路等",
            "tips": "春天油菜花很美，适合骑行",
            "phone": "0851-83851986"
        },
        {
            "name": "天河潭",
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
            "phone": "0851-83300000"
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
            "phone": "0851-87228888"
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
            "phone": "0851-87721256"
        },
        {
            "name": "贵阳森林公园",
            "address": "贵州省贵阳市南明区",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "贵阳森林公园是贵阳的城市绿肺，有茂密的森林和清新的空气。",
            "features": "森林公园,徒步,休闲",
            "rating": 4.0,
            "best_season": "全年",
            "transportation": "贵阳市区乘坐公交",
            "tips": "适合晨练和散步",
            "phone": "0851-85500000"
        },
        {
            "name": "贵阳文昌阁",
            "address": "贵州省贵阳市云岩区",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "09:00-17:00",
            "description": "文昌阁是贵阳的古建筑，始建于明代，是贵阳的文化地标。",
            "features": "古建筑,历史文化,明代",
            "rating": 4.0,
            "best_season": "全年",
            "transportation": "贵阳市区步行可达",
            "tips": "建议游玩1小时",
            "phone": "0851-85800000"
        },
        {
            "name": "贵阳阳明祠",
            "address": "贵州省贵阳市云岩区",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "09:00-17:00",
            "description": "阳明祠是纪念明代哲学家王阳明的祠堂，有深厚的文化底蕴。",
            "features": "历史文化,王阳明,明代",
            "rating": 4.1,
            "best_season": "全年",
            "transportation": "贵阳市区步行可达",
            "tips": "建议游玩1小时",
            "phone": "0851-85800000"
        },

        # ==================== 遵义市 ====================
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
            "phone": "0851-28955555"
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
            "phone": "0851-22863700"
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
            "phone": "0851-22863700"
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
            "phone": "0851-24221048"
        },
        {
            "name": "遵义红军山",
            "address": "贵州省遵义市红花岗区",
            "category": "红色旅游",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "红军山是遵义的红色旅游景点，有红军烈士纪念碑和陈列馆。",
            "features": "红色旅游,烈士纪念碑,爱国教育",
            "rating": 4.4,
            "best_season": "全年",
            "transportation": "遵义市区乘坐公交",
            "tips": "建议游玩2小时",
            "phone": "0851-28222765"
        },
        {
            "name": "遵义古城",
            "address": "贵州省遵义市红花岗区",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "遵义古城有明清古建筑，是遵义的历史文化街区。",
            "features": "古城,明清建筑,历史文化",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "遵义市区步行可达",
            "tips": "晚上夜景很美",
            "phone": "0851-28200000"
        },
        {
            "name": "四渡赤水纪念馆",
            "address": "贵州省遵义市习水县",
            "category": "红色旅游",
            "ticket_price": "免费",
            "opening_hours": "09:00-17:00",
            "description": "四渡赤水纪念馆展示了红军四渡赤水的历史，是重要的红色旅游景点。",
            "features": "红色旅游,历史遗址,爱国教育",
            "rating": 4.4,
            "best_season": "全年",
            "transportation": "习水县城乘坐公交",
            "tips": "建议游玩2-3小时",
            "phone": "0851-22520000"
        },
        {
            "name": "茅台镇",
            "address": "贵州省遵义市仁怀市",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "茅台镇是中国酱酒圣地，有茅台酒厂、中国酒文化城等景点。",
            "features": "酒文化,茅台酒,古镇",
            "rating": 4.3,
            "best_season": "全年",
            "transportation": "仁怀市区乘坐公交",
            "tips": "可品尝茅台酒",
            "phone": "0851-22330000"
        },

        # ==================== 安顺市 ====================
        {
            "name": "天龙屯堡",
            "address": "贵州省安顺市平坝区天龙镇",
            "category": "人文景观",
            "ticket_price": "60元",
            "opening_hours": "08:00-17:30",
            "description": "天龙屯堡是明代屯堡文化的代表，有独特的地戏表演和石头建筑。",
            "features": "屯堡文化,地戏,石头建筑",
            "rating": 4.3,
            "best_season": "全年",
            "transportation": "安顺市区乘坐旅游专线",
            "tips": "建议游玩半天，看地戏表演",
            "phone": "0853-3420000"
        },
        {
            "name": "旧州古镇",
            "address": "贵州省安顺市西秀区旧州镇",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "旧州古镇是安顺的历史文化名镇，有600多年历史，有独特的屯堡文化。",
            "features": "古镇,屯堡文化,地戏",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "安顺市区乘坐公交",
            "tips": "建议游玩半天",
            "phone": "0853-3220000"
        },
        {
            "name": "格凸河",
            "address": "贵州省安顺市紫云县",
            "category": "自然风光",
            "ticket_price": "60元",
            "opening_hours": "08:00-16:00",
            "description": "格凸河有壮观的喀斯特地貌，有燕子洞、穿上洞等景点，是户外探险的好去处。",
            "features": "喀斯特地貌,溶洞,攀岩,蜘蛛人",
            "rating": 4.4,
            "best_season": "4-10月",
            "transportation": "紫云县城乘坐班车",
            "tips": "观看蜘蛛人攀岩表演",
            "phone": "0853-5230000"
        },
        {
            "name": "花江大峡谷",
            "address": "贵州省安顺市关岭县",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "花江大峡谷是贵州最大的峡谷之一，有壮观的峡谷风光和独特的布依族文化。",
            "features": "峡谷,布依族文化,漂流",
            "rating": 4.3,
            "best_season": "5-10月",
            "transportation": "关岭县城包车前往",
            "tips": "建议游玩1天",
            "phone": "0853-7220000"
        },
        {
            "name": "平坝樱花",
            "address": "贵州省安顺市平坝区",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "平坝农场有万亩樱花，是全国最大的樱花基地，每年3月樱花盛开，美不胜收。",
            "features": "樱花,花海,摄影胜地",
            "rating": 4.3,
            "best_season": "3月",
            "transportation": "安顺市区乘坐公交",
            "tips": "花期人多，建议早去",
            "phone": "0853-3420000"
        },

        # ==================== 黔东南州 ====================
        {
            "name": "朗德苗寨",
            "address": "贵州省黔东南苗族侗族自治州雷山县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "朗德苗寨是全国第一个民俗风情村寨，有独特的苗族歌舞表演和拦门酒。",
            "features": "苗族村寨,歌舞表演,拦门酒",
            "rating": 4.4,
            "best_season": "全年",
            "transportation": "凯里市乘坐班车",
            "tips": "建议游玩半天，体验苗族风情",
            "phone": "0855-3320000"
        },
        {
            "name": "反排苗寨",
            "address": "贵州省黔东南苗族侗族自治州台江县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "反排苗寨是木鼓舞的发源地，有独特的苗族舞蹈和文化。",
            "features": "苗族村寨,木鼓舞,非遗",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "台江县城乘坐班车",
            "tips": "建议游玩半天",
            "phone": "0855-5320000"
        },
        {
            "name": "控拜苗寨",
            "address": "贵州省黔东南苗族侗族自治州雷山县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "控拜苗寨是银匠村，有独特的苗族银饰锻造技艺，可体验银饰制作。",
            "features": "苗族村寨,银饰,非遗",
            "rating": 4.1,
            "best_season": "全年",
            "transportation": "雷山县城乘坐班车",
            "tips": "可体验银饰制作",
            "phone": "0855-3320000"
        },
        {
            "name": "大利侗寨",
            "address": "贵州省黔东南苗族侗族自治州榕江县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "大利侗寨有保存完好的侗族建筑和独特的侗族文化，是体验侗族生活的好去处。",
            "features": "侗族村寨,侗族建筑,侗族文化",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "榕江县城乘坐班车",
            "tips": "建议游玩半天",
            "phone": "0855-6620000"
        },
        {
            "name": "三宝侗寨",
            "address": "贵州省黔东南苗族侗族自治州榕江县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "三宝侗寨有千户侗寨之称，有独特的侗族鼓楼和风雨桥，是侗族文化的重要展示地。",
            "features": "侗族村寨,鼓楼,风雨桥",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "榕江县城乘坐公交",
            "tips": "建议游玩半天",
            "phone": "0855-6620000"
        },
        {
            "name": "黄岗侗寨",
            "address": "贵州省黔东南苗族侗族自治州黎平县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "黄岗侗寨有独特的侗族大歌和拦路歌，是体验侗族音乐文化的好去处。",
            "features": "侗族村寨,侗族大歌,拦路歌",
            "rating": 4.1,
            "best_season": "全年",
            "transportation": "黎平县城包车前往",
            "tips": "建议游玩半天",
            "phone": "0855-6220000"
        },
        {
            "name": "麻塘革家寨",
            "address": "贵州省黔东南苗族侗族自治州黄平县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "麻塘革家寨是革家人聚居的村寨，有独特的革家文化和服饰。",
            "features": "革家文化,民族服饰,蜡染",
            "rating": 4.0,
            "best_season": "全年",
            "transportation": "黄平县城乘坐班车",
            "tips": "建议游玩半天",
            "phone": "0855-2420000"
        },
        {
            "name": "凯里民族博物馆",
            "address": "贵州省黔东南苗族侗族自治州凯里市",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "09:00-17:00",
            "description": "凯里民族博物馆展示了黔东南各民族的历史文化，是了解苗侗文化的好去处。",
            "features": "博物馆,民族文化,苗族,侗族",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "凯里市区步行可达",
            "tips": "建议游玩2小时",
            "phone": "0855-8220000"
        },

        # ==================== 黔南州 ====================
        {
            "name": "平塘天眼",
            "address": "贵州省黔南布依族苗族自治州平塘县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "09:00-17:00",
            "description": "平塘天眼是世界最大的单口径射电望远镜，是科技旅游的好去处。",
            "features": "科技旅游,射电望远镜,天文",
            "rating": 4.6,
            "best_season": "全年",
            "transportation": "平塘县城乘坐旅游专线",
            "tips": "需提前预约，不能带电子设备",
            "phone": "0854-7222222"
        },
        {
            "name": "都匀毛尖茶文化园",
            "address": "贵州省黔南布依族苗族自治州都匀市",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "09:00-17:00",
            "description": "都匀毛尖茶文化园展示了都匀毛尖茶的历史和文化，可体验采茶制茶。",
            "features": "茶文化,都匀毛尖,体验",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "都匀市区乘坐公交",
            "tips": "春季采茶最佳",
            "phone": "0854-8220000"
        },
        {
            "name": "荔波大七孔",
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
            "phone": "0854-3619810"
        },
        {
            "name": "茂兰喀斯特森林",
            "address": "贵州省黔南布依族苗族自治州荔波县",
            "category": "自然风光",
            "ticket_price": "50元",
            "opening_hours": "08:00-16:00",
            "description": "茂兰是中国南方喀斯特世界自然遗产的核心区域，有原始森林、溶洞、暗河等。",
            "features": "喀斯特森林,世界遗产,徒步",
            "rating": 4.5,
            "best_season": "4-10月",
            "transportation": "荔波县城包车前往",
            "tips": "建议请向导，带足水和食物",
            "phone": "0854-3619810"
        },
        {
            "name": "惠水好花红",
            "address": "贵州省黔南布依族苗族自治州惠水县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "好花红是布依族村寨，有独特的布依族文化和美丽的田园风光。",
            "features": "布依族文化,田园风光,民歌",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "惠水县城乘坐班车",
            "tips": "建议游玩半天",
            "phone": "0854-6220000"
        },

        # ==================== 黔西南州 ====================
        {
            "name": "万峰湖",
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
            "phone": "0859-3121200"
        },
        {
            "name": "双乳峰",
            "address": "贵州省黔西南布依族苗族自治州贞丰县",
            "category": "自然风光",
            "ticket_price": "80元",
            "opening_hours": "08:00-17:00",
            "description": "双乳峰被誉为天下奇观，两座形似乳房的山峰栩栩如生，是贞丰的标志性景点。",
            "features": "奇峰,地质奇观,布依族文化",
            "rating": 4.3,
            "best_season": "全年",
            "transportation": "贞丰县城乘坐班车",
            "tips": "建议游玩2-3小时",
            "phone": "0859-6610000"
        },
        {
            "name": "晴隆二十四道拐",
            "address": "贵州省黔西南布依族苗族自治州晴隆县",
            "category": "红色旅游",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "二十四道拐是抗战公路，有24个急弯，是中美盟军抗日战争的见证。",
            "features": "抗战公路,历史遗址,盘山公路",
            "rating": 4.4,
            "best_season": "全年",
            "transportation": "晴隆县城乘坐班车",
            "tips": "建议游玩1-2小时",
            "phone": "0859-7610000"
        },
        {
            "name": "贞丰三岔河",
            "address": "贵州省黔西南布依族苗族自治州贞丰县",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "三岔河有壮观的峡谷风光和独特的布依族文化，是户外运动的好去处。",
            "features": "峡谷,布依族文化,户外运动",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "贞丰县城乘坐班车",
            "tips": "建议游玩半天",
            "phone": "0859-6610000"
        },
        {
            "name": "安龙招堤",
            "address": "贵州省黔西南布依族苗族自治州安龙县",
            "category": "人文景观",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "安龙招堤是贵州著名的水利工程，有悠久的历史和美丽的风光。",
            "features": "水利工程,历史,荷花",
            "rating": 4.1,
            "best_season": "6-8月",
            "transportation": "安龙县城乘坐公交",
            "tips": "夏季荷花盛开",
            "phone": "0859-5210000"
        },

        # ==================== 铜仁市 ====================
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
            "phone": "0856-6720000"
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
            "phone": "0856-7650000"
        },
        {
            "name": "铜仁大峡谷",
            "address": "贵州省铜仁市碧江区",
            "category": "自然风光",
            "ticket_price": "100元",
            "opening_hours": "08:00-16:00",
            "description": "铜仁大峡谷集峻、隐、幽、旷、奇、险于一体，以原始的峡谷风光和瀑布群著称。",
            "features": "峡谷,瀑布,玻璃栈道",
            "rating": 4.4,
            "best_season": "5-10月",
            "transportation": "铜仁市区乘坐旅游专线",
            "tips": "建议游玩3-4小时",
            "phone": "0856-5210000"
        },
        {
            "name": "思南温泉",
            "address": "贵州省铜仁市思南县",
            "category": "休闲娱乐",
            "ticket_price": "98元",
            "opening_hours": "09:00-23:00",
            "description": "思南温泉是贵州最大的温泉之一，有独特的温泉文化和美丽的乌江风光。",
            "features": "温泉,乌江风光,休闲养生",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "思南县城乘坐公交",
            "tips": "建议游玩半天",
            "phone": "0856-7220000"
        },
        {
            "name": "苗王城",
            "address": "贵州省铜仁市松桃县",
            "category": "人文景观",
            "ticket_price": "100元",
            "opening_hours": "08:00-17:00",
            "description": "苗王城是苗族的文化遗址，有独特的苗族建筑和文化。",
            "features": "苗族文化,苗王城,历史遗址",
            "rating": 4.3,
            "best_season": "全年",
            "transportation": "松桃县城乘坐班车",
            "tips": "建议游玩半天",
            "phone": "0856-2830000"
        },

        # ==================== 毕节市 ====================
        {
            "name": "百里杜鹃",
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
            "phone": "0857-4666008"
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
            "phone": "0857-6222222"
        },
        {
            "name": "韭菜坪",
            "address": "贵州省毕节市赫章县",
            "category": "自然风光",
            "ticket_price": "50元",
            "opening_hours": "08:00-17:00",
            "description": "韭菜坪有贵州屋脊之称，海拔2900.6米，是贵州最高峰，有万亩韭菜花海。",
            "features": "高山草甸,韭菜花海,日出",
            "rating": 4.5,
            "best_season": "8-10月",
            "transportation": "赫章县城包车前往",
            "tips": "建议游玩1天，带保暖衣物",
            "phone": "0857-3220000"
        },
        {
            "name": "百草坪",
            "address": "贵州省毕节市威宁县",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "百草坪是贵州最大的高山草场，有壮观的草原风光和独特的彝族文化。",
            "features": "高山草场,彝族文化,户外运动",
            "rating": 4.3,
            "best_season": "6-9月",
            "transportation": "威宁县城包车前往",
            "tips": "建议游玩1天",
            "phone": "0857-6222222"
        },

        # ==================== 六盘水市 ====================
        {
            "name": "乌蒙大草原",
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
            "phone": "0858-3636666"
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
            "phone": "0858-3636666"
        },
        {
            "name": "北盘江大桥",
            "address": "贵州省六盘水市水城县",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "北盘江大桥是世界第一高桥，桥面到江面垂直距离565米，有壮观的峡谷风光。",
            "features": "世界第一高桥,峡谷,工程奇迹",
            "rating": 4.5,
            "best_season": "全年",
            "transportation": "自驾或包车",
            "tips": "建议游玩1-2小时",
            "phone": "0858-8220000"
        },
        {
            "name": "梅花山",
            "address": "贵州省六盘水市钟山区",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "梅花山是六盘水的著名景点，有壮观的峡谷风光和独特的喀斯特地貌。",
            "features": "峡谷,喀斯特地貌,户外运动",
            "rating": 4.3,
            "best_season": "全年",
            "transportation": "六盘水市区乘坐公交",
            "tips": "建议游玩半天",
            "phone": "0858-8220000"
        },
        {
            "name": "野玉海",
            "address": "贵州省六盘水市水城县",
            "category": "自然风光",
            "ticket_price": "免费",
            "opening_hours": "全天",
            "description": "野玉海有壮观的高山草甸和独特的彝族文化，是体验彝族风情的好去处。",
            "features": "高山草甸,彝族文化,户外运动",
            "rating": 4.2,
            "best_season": "全年",
            "transportation": "水城县城乘坐公交",
            "tips": "建议游玩1天",
            "phone": "0858-8220000"
        }
    ]

    # 添加新景点
    added = 0
    for spot in all_spots:
        name = spot.get('name', '')
        if name and name not in existing_names:
            data.append(spot)
            existing_names.add(name)
            added += 1
            print("  + " + name)

    # 保存数据
    with open('data/guizhou_attractions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n新增 " + str(added) + " 个景点")
    print("总计 " + str(len(data)) + " 个景点")

    # 更新数据库
    conn = sqlite3.connect('data/attractions.db')
    cursor = conn.cursor()

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

    for attr in data:
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
    print("数据库已更新")

    # 统计
    categories = {}
    regions = {}
    for attr in data:
        cat = attr.get('category', '其他')
        categories[cat] = categories.get(cat, 0) + 1

        addr = attr.get('address', '')
        region = '其他'
        for key in ['贵阳', '遵义', '安顺', '黔东南', '黔南', '黔西南', '铜仁', '毕节', '六盘水']:
            if key in addr:
                region = key
                break
        regions[region] = regions.get(region, 0) + 1

    print("\n按类别统计：")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print("  " + cat + ": " + str(count) + " 个")

    print("\n按地区统计：")
    for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        print("  " + region + ": " + str(count) + " 个")


if __name__ == '__main__':
    add_all_guizhou_spots()
