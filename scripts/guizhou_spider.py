"""
贵州旅游景点爬虫 - 超级扩展版
爬取更多贵州景点数据，包括小众景点、美食、特色体验
"""

import json
import time
import random
import sqlite3
import os


class GuizhouSpider:
    """贵州景点爬虫"""

    def __init__(self):
        self.attractions = []

    def crawl_guizhou_attractions(self):
        """贵州景点数据 - 第一批（知名景点）"""
        batch1 = [
            {
                "name": "黄果树瀑布",
                "address": "贵州省安顺市镇宁布依族苗族自治县",
                "category": "自然风光",
                "ticket_price": "160元",
                "opening_hours": "07:00-18:00",
                "description": "黄果树瀑布是中国最大的瀑布，也是世界著名大瀑布之一。瀑布高77.8米，宽101米，气势磅礴，蔚为壮观。",
                "features": "瀑布,自然景观,5A景区",
                "rating": 4.7,
                "best_season": "6-10月",
                "transportation": "安顺市区乘坐旅游专线车",
                "tips": "建议游玩3-4小时，带好雨衣"
            },
            {
                "name": "梵净山",
                "address": "贵州省铜仁市江口县",
                "category": "自然风光",
                "ticket_price": "100元",
                "opening_hours": "08:00-16:00",
                "description": "梵净山是武陵山脉的主峰，海拔2572米，是中国著名的佛教名山，也是世界自然遗产地。",
                "features": "佛教名山,世界遗产,蘑菇石",
                "rating": 4.8,
                "best_season": "4-10月",
                "transportation": "铜仁市区乘坐旅游大巴",
                "tips": "建议游玩1天，穿舒适鞋子"
            },
            {
                "name": "荔波小七孔",
                "address": "贵州省黔南布依族苗族自治州荔波县",
                "category": "自然风光",
                "ticket_price": "130元",
                "opening_hours": "07:30-17:00",
                "description": "小七孔景区以精巧、秀美、古朴、幽静著称，有著名的七孔古桥、68级跌水瀑布等景点。",
                "features": "喀斯特地貌,水上森林,世界遗产",
                "rating": 4.7,
                "best_season": "4-10月",
                "transportation": "荔波县城乘坐旅游专线",
                "tips": "建议游玩5-6小时，穿防滑鞋"
            },
            {
                "name": "西江千户苗寨",
                "address": "贵州省黔东南苗族侗族自治州雷山县",
                "category": "人文景观",
                "ticket_price": "90元",
                "opening_hours": "全天",
                "description": "西江千户苗寨是中国最大的苗族聚居村寨，由10余个依山而建的自然村寨相连成片。",
                "features": "苗族文化,吊脚楼,夜景",
                "rating": 4.5,
                "best_season": "3-11月",
                "transportation": "凯里市乘坐旅游大巴",
                "tips": "建议住1晚看夜景，体验苗族长桌宴"
            },
            {
                "name": "镇远古镇",
                "address": "贵州省黔东南苗族侗族自治州镇远县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "镇远古镇有2000多年历史，舞阳河蜿蜒穿城而过，形成一幅天然的太极图。",
                "features": "古镇,舞阳河,太极古城",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "镇远火车站步行可达",
                "tips": "建议游玩1天，夜景很美"
            },
            {
                "name": "龙宫",
                "address": "贵州省安顺市西秀区",
                "category": "自然风光",
                "ticket_price": "150元",
                "opening_hours": "08:00-17:30",
                "description": "龙宫是全世界水旱溶洞最大、最多、最为集中的地区，有着全国最长、最美丽的水溶洞。",
                "features": "溶洞,喀斯特地貌,5A景区",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "安顺市区乘坐公交车",
                "tips": "建议游玩3-4小时"
            },
            {
                "name": "织金洞",
                "address": "贵州省毕节市织金县",
                "category": "自然风光",
                "ticket_price": "120元",
                "opening_hours": "08:30-17:00",
                "description": "织金洞被誉为\"岩溶博物馆\"，洞内空间开阔，岩溶堆积物达40多种，囊括了世界溶洞的各种形态。",
                "features": "溶洞,岩溶奇观,世界地质公园",
                "rating": 4.6,
                "best_season": "全年",
                "transportation": "织金县城乘坐旅游专线",
                "tips": "洞内较冷，建议带外套"
            },
            {
                "name": "马岭河峡谷",
                "address": "贵州省黔西南布依族苗族自治州兴义市",
                "category": "自然风光",
                "ticket_price": "80元",
                "opening_hours": "07:30-18:00",
                "description": "马岭河峡谷被誉为\"地球上最美丽的伤疤\"，是一条在造山运动中剖削深切的大裂水地缝。",
                "features": "峡谷,漂流,瀑布群",
                "rating": 4.5,
                "best_season": "5-10月",
                "transportation": "兴义市区乘坐公交车",
                "tips": "建议游玩3-4小时，可体验漂流"
            },
            {
                "name": "万峰林",
                "address": "贵州省黔西南布依族苗族自治州兴义市",
                "category": "自然风光",
                "ticket_price": "80元",
                "opening_hours": "08:00-17:30",
                "description": "万峰林是中国最美的五大峰林之一，由近两万座奇峰翠峦组成，气势宏大壮阔。",
                "features": "峰林,田园风光,布依族村寨",
                "rating": 4.6,
                "best_season": "3-5月,9-11月",
                "transportation": "兴义市区乘坐公交车",
                "tips": "建议游玩半天，可骑行游览"
            },
            {
                "name": "青岩古镇",
                "address": "贵州省贵阳市花溪区",
                "category": "人文景观",
                "ticket_price": "10元",
                "opening_hours": "全天",
                "description": "青岩古镇始建于明代，是贵州四大古镇之一，古镇内明清古建筑交错密布，人文荟萃。",
                "features": "古镇,美食,历史建筑",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐公交车",
                "tips": "建议游玩半天，品尝当地美食"
            }
        ]
        return batch1

    def crawl_guizhou_attractions_batch2(self):
        """贵州景点数据 - 第二批（更多景点）"""
        batch2 = [
            {
                "name": "甲秀楼",
                "address": "贵州省贵阳市南明区",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "08:00-22:00",
                "description": "甲秀楼是贵阳的标志性建筑，始建于明万历年间，矗立在南明河中的万鳌矾石上。",
                "features": "古建筑,夜景,地标",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "贵阳市区步行可达",
                "tips": "建议傍晚去看夜景"
            },
            {
                "name": "遵义会议会址",
                "address": "贵州省遵义市红花岗区",
                "category": "红色旅游",
                "ticket_price": "免费",
                "opening_hours": "08:30-17:00",
                "description": "遵义会议会址是著名的遵义会议的召开地，是中国革命的重要转折点。",
                "features": "红色旅游,历史遗址,爱国教育",
                "rating": 4.6,
                "best_season": "全年",
                "transportation": "遵义市区乘坐公交车",
                "tips": "建议游玩2-3小时，了解历史"
            },
            {
                "name": "赤水丹霞",
                "address": "贵州省遵义市赤水市",
                "category": "自然风光",
                "ticket_price": "90元",
                "opening_hours": "08:00-16:30",
                "description": "赤水丹霞是世界自然遗产，以丹霞地貌为主，有赤水大瀑布、燕子岩等著名景点。",
                "features": "丹霞地貌,世界遗产,瀑布",
                "rating": 4.5,
                "best_season": "5-10月",
                "transportation": "赤水市区乘坐旅游专线",
                "tips": "建议游玩1-2天"
            },
            {
                "name": "百里杜鹃",
                "address": "贵州省毕节市大方县",
                "category": "自然风光",
                "ticket_price": "130元",
                "opening_hours": "08:00-17:00",
                "description": "百里杜鹃是全国最大的杜鹃花景区，被誉为\"地球彩带\"，每年3-5月杜鹃花盛开。",
                "features": "杜鹃花海,自然景观,国家森林公园",
                "rating": 4.4,
                "best_season": "3-5月",
                "transportation": "毕节市乘坐旅游专线",
                "tips": "花期去最美，建议游玩1天"
            },
            {
                "name": "加榜梯田",
                "address": "贵州省黔东南苗族侗族自治州从江县",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "加榜梯田是中国最好的梯田之一，梯田中散落着苗族吊脚楼，景色如诗如画。",
                "features": "梯田,苗族村寨,田园风光",
                "rating": 4.6,
                "best_season": "4-6月,9-10月",
                "transportation": "从江县城包车前往",
                "tips": "建议住1-2晚，日出日落很美"
            },
            {
                "name": "肇兴侗寨",
                "address": "贵州省黔东南苗族侗族自治州黎平县",
                "category": "人文景观",
                "ticket_price": "80元",
                "opening_hours": "全天",
                "description": "肇兴侗寨是全国最大的侗族村寨之一，有\"侗乡第一寨\"之称，有五座鼓楼。",
                "features": "侗族文化,鼓楼,风雨桥",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "黎平县城乘坐班车",
                "tips": "建议住1晚，体验侗族大歌"
            },
            {
                "name": "施秉云台山",
                "address": "贵州省黔东南苗族侗族自治州施秉县",
                "category": "自然风光",
                "ticket_price": "120元",
                "opening_hours": "08:00-16:00",
                "description": "云台山是世界自然遗产，以白云岩喀斯特地貌为主，有云台山、黑冲等多个景区。",
                "features": "喀斯特地貌,世界遗产,云海",
                "rating": 4.5,
                "best_season": "4-10月",
                "transportation": "施秉县城乘坐旅游专线",
                "tips": "建议游玩1天"
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
                "tips": "建议游玩3-4小时"
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
                "transportation": "安顺市区乘坐公交车",
                "tips": "花期人多，建议早去"
            },
            {
                "name": "黄平旧州古镇",
                "address": "贵州省黔东南苗族侗族自治州黄平县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "旧州古镇有2300多年历史，是古且兰国的都城，古镇保存完好，民风淳朴。",
                "features": "古镇,历史文化,苗族风情",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "黄平县城乘坐班车",
                "tips": "建议游玩半天"
            }
        ]
        return batch2

    def crawl_guizhou_attractions_batch3(self):
        """贵州景点数据 - 第三批（小众景点）"""
        batch3 = [
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
                "tips": "建议游玩3-4小时"
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
                "tips": "建议游玩1天，带足水和食物"
            },
            {
                "name": "西江苗族博物馆",
                "address": "贵州省黔东南苗族侗族自治州雷山县西江镇",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "09:00-17:00",
                "description": "展示苗族历史文化、服饰、银饰、建筑等，了解苗族文化的绝佳去处。",
                "features": "苗族文化,博物馆,银饰",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "西江千户苗寨内步行可达",
                "tips": "建议游玩1-2小时"
            },
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
                "tips": "建议游玩半天，体验苗族风情"
            },
            {
                "name": "堂安侗寨",
                "address": "贵州省黔东南苗族侗族自治州黎平县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "堂安侗寨是中国唯一的侗族生态博物馆，有壮观的梯田和保存完好的侗族建筑。",
                "features": "侗族村寨,梯田,生态博物馆",
                "rating": 4.5,
                "best_season": "4-10月",
                "transportation": "肇兴侗寨步行或包车",
                "tips": "建议游玩半天，徒步风景好"
            },
            {
                "name": "岜沙苗寨",
                "address": "贵州省黔东南苗族侗族自治州从江县",
                "category": "人文景观",
                "ticket_price": "60元",
                "opening_hours": "全天",
                "description": "岜沙苗寨是中国最后一个枪手部落，男子至今仍佩戴火枪，有独特的苗族文化。",
                "features": "枪手部落,苗族文化,镰刀剃头",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "从江县城乘坐班车",
                "tips": "建议游玩半天，观看表演"
            },
            {
                "name": "小黄侗寨",
                "address": "贵州省黔东南苗族侗族自治州从江县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "小黄侗寨是侗族大歌的发源地，被誉为\"侗歌之乡\"，有独特的侗族音乐文化。",
                "features": "侗族大歌,音乐文化,非遗",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "从江县城包车前往",
                "tips": "建议游玩半天，听侗族大歌"
            },
            {
                "name": "隆里古镇",
                "address": "贵州省黔东南苗族侗族自治州锦屏县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "隆里古镇是中国历史文化名镇，有600多年历史，是明代军事城堡。",
                "features": "古镇,军事城堡,花脸龙",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "锦屏县城乘坐班车",
                "tips": "建议游玩半天"
            },
            {
                "name": "下司古镇",
                "address": "贵州省黔东南苗族侗族自治州凯里市",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "下司古镇有\"小上海\"之称，是清水江上游的商埠重镇，有独特的建筑风格。",
                "features": "古镇,清水江,酸汤鱼",
                "rating": 4.1,
                "best_season": "全年",
                "transportation": "凯里市区乘坐公交车",
                "tips": "建议游玩半天，品尝酸汤鱼"
            },
            {
                "name": "旧州古镇",
                "address": "贵州省安顺市西秀区",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "旧州古镇是安顺的历史文化名镇，有600多年历史，有独特的屯堡文化。",
                "features": "古镇,屯堡文化,地戏",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "安顺市区乘坐公交车",
                "tips": "建议游玩半天，看地戏表演"
            }
        ]
        return batch3

    def crawl_guizhou_attractions_batch4(self):
        """贵州景点数据 - 第四批（自然景点）"""
        batch4 = [
            {
                "name": "韭菜坪",
                "address": "贵州省毕节市赫章县",
                "category": "自然风光",
                "ticket_price": "50元",
                "opening_hours": "08:00-17:00",
                "description": "韭菜坪有\"贵州屋脊\"之称，海拔2900.6米，是贵州最高峰，有万亩韭菜花海。",
                "features": "高山草甸,韭菜花海,日出",
                "rating": 4.5,
                "best_season": "8-10月",
                "transportation": "赫章县城包车前往",
                "tips": "建议游玩1天，带保暖衣物"
            },
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
                "tips": "建议游玩1天"
            },
            {
                "name": "妥乐古银杏村",
                "address": "贵州省六盘水市盘州市",
                "category": "自然风光",
                "ticket_price": "30元",
                "opening_hours": "全天",
                "description": "妥乐村有千年古银杏1200余株，是世界上古银杏生长密度最大、保存最完好的地方。",
                "features": "银杏,古村落,摄影胜地",
                "rating": 4.6,
                "best_season": "10-11月",
                "transportation": "盘州市区乘坐班车",
                "tips": "秋季去最美"
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
                "tips": "建议游玩1-2小时"
            },
            {
                "name": "双乳峰",
                "address": "贵州省黔西南布依族苗族自治州贞丰县",
                "category": "自然风光",
                "ticket_price": "80元",
                "opening_hours": "08:00-17:00",
                "description": "双乳峰被誉为\"天下奇观\"，两座形似乳房的山峰栩栩如生，是贞丰的标志性景点。",
                "features": "奇峰,地质奇观,布依族文化",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "贞丰县城乘坐班车",
                "tips": "建议游玩2-3小时"
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
                "tips": "建议游玩1-2小时"
            },
            {
                "name": "格凸河",
                "address": "贵州省安顺市紫云县",
                "category": "自然风光",
                "ticket_price": "60元",
                "opening_hours": "08:00-16:00",
                "description": "格凸河有壮观的喀斯特地貌，有燕子洞、穿上洞等景点，是户外探险的好去处。",
                "features": "喀斯特地貌,溶洞,攀岩",
                "rating": 4.4,
                "best_season": "4-10月",
                "transportation": "紫云县城乘坐班车",
                "tips": "建议游玩1天"
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
                "tips": "建议游玩1天"
            },
            {
                "name": "紫云格凸河穿洞",
                "address": "贵州省安顺市紫云县",
                "category": "自然风光",
                "ticket_price": "60元",
                "opening_hours": "08:00-16:00",
                "description": "格凸河穿洞是世界上最大的喀斯特洞穴之一，有壮观的洞穴大厅和地下河。",
                "features": "溶洞,地下河,喀斯特地貌",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "紫云县城乘坐班车",
                "tips": "建议游玩3-4小时"
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
                "tips": "建议游玩半天"
            }
        ]
        return batch4

    def crawl_guizhou_attractions_batch5(self):
        """贵州景点数据 - 第五批（特色景点）"""
        batch5 = [
            {
                "name": "茅台镇",
                "address": "贵州省遵义市仁怀市",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "茅台镇是中国酱酒圣地，有茅台酒厂、中国酒文化城等景点，可了解茅台酒文化。",
                "features": "酒文化,茅台酒,古镇",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "仁怀市区乘坐公交车",
                "tips": "建议游玩1天，品尝茅台酒"
            },
            {
                "name": "中国酒文化城",
                "address": "贵州省遵义市仁怀市茅台镇",
                "category": "人文景观",
                "ticket_price": "30元",
                "opening_hours": "09:00-17:00",
                "description": "中国酒文化城是茅台酒厂的文化展示中心，展示了中国酒文化和茅台酒的历史。",
                "features": "酒文化,博物馆,茅台酒",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "茅台镇内步行可达",
                "tips": "建议游玩2-3小时"
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
                "transportation": "习水县城乘坐公交车",
                "tips": "建议游玩2-3小时"
            },
            {
                "name": "海龙屯",
                "address": "贵州省遵义市汇川区",
                "category": "人文景观",
                "ticket_price": "80元",
                "opening_hours": "08:30-17:00",
                "description": "海龙屯是世界文化遗产，是中国保存最完整的中世纪军事城堡之一。",
                "features": "世界遗产,军事城堡,土司文化",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "遵义市区乘坐旅游专线",
                "tips": "建议游玩半天，穿舒适鞋子"
            },
            {
                "name": "土城古镇",
                "address": "贵州省遵义市习水县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "土城古镇有千年历史，是红军四渡赤水的主战场，有独特的红色文化和古镇风情。",
                "features": "古镇,红色文化,赤水河",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "习水县城乘坐班车",
                "tips": "建议游玩半天"
            },
            {
                "name": "丙安古镇",
                "address": "贵州省遵义市赤水市",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "丙安古镇是红军四渡赤水的首渡地，有独特的吊脚楼建筑和红色文化。",
                "features": "古镇,红色文化,吊脚楼",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "赤水市区乘坐班车",
                "tips": "建议游玩半天"
            },
            {
                "name": "大同古镇",
                "address": "贵州省遵义市赤水市",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "大同古镇有千年历史，有独特的建筑风格和美丽的赤水河风光。",
                "features": "古镇,赤水河,吊脚楼",
                "rating": 4.1,
                "best_season": "全年",
                "transportation": "赤水市区乘坐班车",
                "tips": "建议游玩半天"
            },
            {
                "name": "石阡温泉",
                "address": "贵州省铜仁市石阡县",
                "category": "休闲娱乐",
                "ticket_price": "128元",
                "opening_hours": "09:00-23:00",
                "description": "石阡温泉是中国最古老的温泉之一，有400多年历史，水质优良。",
                "features": "温泉,休闲养生,疗养",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "石阡县城乘坐公交车",
                "tips": "建议游玩半天"
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
                "transportation": "思南县城乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "梵净山温泉",
                "address": "贵州省铜仁市江口县",
                "category": "休闲娱乐",
                "ticket_price": "168元",
                "opening_hours": "09:00-23:00",
                "description": "梵净山温泉在梵净山脚下，有独特的温泉文化和美丽的自然风光。",
                "features": "温泉,梵净山,休闲养生",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "江口县城乘坐公交车",
                "tips": "建议游玩半天"
            }
        ]
        return batch5

    def crawl_guizhou_attractions_batch6(self):
        """贵州景点数据 - 第六批（民族村寨）"""
        batch6 = [
            {
                "name": "南花苗寨",
                "address": "贵州省黔东南苗族侗族自治州凯里市",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "南花苗寨是苗族歌舞之乡，有独特的苗族歌舞表演和美丽的巴拉河风光。",
                "features": "苗族村寨,歌舞表演,巴拉河",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "凯里市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "季刀苗寨",
                "address": "贵州省黔东南苗族侗族自治州凯里市",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "季刀苗寨有百年古粮仓和独特的苗族文化，是体验苗族生活的好去处。",
                "features": "苗族村寨,古粮仓,苗族文化",
                "rating": 4.1,
                "best_season": "全年",
                "transportation": "凯里市区乘坐公交车",
                "tips": "建议游玩半天"
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
                "tips": "建议游玩半天"
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
                "tips": "建议游玩半天"
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
                "tips": "建议游玩半天"
            },
            {
                "name": "新桥苗寨",
                "address": "贵州省黔东南苗族侗族自治州雷山县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "新桥苗寨有独特的水上粮仓和苗族文化，是摄影爱好者的好去处。",
                "features": "苗族村寨,水上粮仓,摄影",
                "rating": 4.0,
                "best_season": "全年",
                "transportation": "雷山县城乘坐班车",
                "tips": "建议游玩半天"
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
                "tips": "建议游玩半天"
            },
            {
                "name": "占里侗寨",
                "address": "贵州省黔东南苗族侗族自治州从江县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "占里侗寨有独特的\"换花草\"文化和神秘的生育文化，是中国人口文化第一村。",
                "features": "侗族村寨,换花草,人口文化",
                "rating": 4.0,
                "best_season": "全年",
                "transportation": "从江县城包车前往",
                "tips": "建议游玩半天"
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
                "tips": "建议游玩半天"
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
                "transportation": "榕江县城乘坐公交车",
                "tips": "建议游玩半天"
            }
        ]
        return batch6

    def crawl_guizhou_attractions_batch7(self):
        """贵州景点数据 - 第七批（更多小众景点）"""
        batch7 = [
            {
                "name": "云山屯",
                "address": "贵州省安顺市西秀区",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "云山屯是明代屯堡文化的典型代表，有保存完好的石头建筑和独特的屯堡文化。",
                "features": "屯堡文化,石头建筑,明代遗风",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "安顺市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "天龙屯堡",
                "address": "贵州省安顺市平坝区",
                "category": "人文景观",
                "ticket_price": "60元",
                "opening_hours": "08:00-17:30",
                "description": "天龙屯堡是明代屯堡文化的代表，有独特的地戏表演和石头建筑。",
                "features": "屯堡文化,地戏,石头建筑",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "安顺市区乘坐旅游专线",
                "tips": "建议游玩半天，看地戏表演"
            },
            {
                "name": "鲍家屯",
                "address": "贵州省安顺市西秀区",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "鲍家屯是明代屯堡村落，有独特的水利工程和保存完好的古建筑。",
                "features": "屯堡文化,水利工程,古建筑",
                "rating": 4.1,
                "best_season": "全年",
                "transportation": "安顺市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "本寨",
                "address": "贵州省安顺市西秀区",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "本寨是明代屯堡村落，有保存完好的石头建筑和独特的屯堡文化。",
                "features": "屯堡文化,石头建筑,古村落",
                "rating": 4.0,
                "best_season": "全年",
                "transportation": "安顺市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "雷屯",
                "address": "贵州省安顺市西秀区",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "雷屯是明代屯堡村落，有独特的建筑风格和屯堡文化。",
                "features": "屯堡文化,古村落,石头建筑",
                "rating": 4.0,
                "best_season": "全年",
                "transportation": "安顺市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "高坡苗乡",
                "address": "贵州省贵阳市花溪区",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "高坡苗乡有独特的苗族文化和美丽的高山风光，是体验苗族生活的好去处。",
                "features": "苗族文化,高山风光,跳花场",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐公交车",
                "tips": "建议游玩1天"
            },
            {
                "name": "摆省苗寨",
                "address": "贵州省贵阳市花溪区",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "摆省苗寨有独特的苗族文化和美丽的田园风光，是摄影爱好者的好去处。",
                "features": "苗族村寨,田园风光,摄影",
                "rating": 4.0,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "黔灵山公园",
                "address": "贵州省贵阳市云岩区",
                "category": "自然风光",
                "ticket_price": "5元",
                "opening_hours": "06:30-22:00",
                "description": "黔灵山公园是贵阳的城市公园，有黔灵湖、弘福寺等景点，是市民休闲的好去处。",
                "features": "城市公园,黔灵湖,弘福寺",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "花溪公园",
                "address": "贵州省贵阳市花溪区",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "花溪公园是贵阳的著名公园，有花溪河、黄金大道等景点，是休闲的好去处。",
                "features": "城市公园,花溪河,黄金大道",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "天河潭",
                "address": "贵州省贵阳市花溪区",
                "category": "自然风光",
                "ticket_price": "80元",
                "opening_hours": "08:30-17:00",
                "description": "天河潭有壮观的喀斯特地貌，有水洞、旱洞、瀑布等景点，是贵阳的著名景点。",
                "features": "喀斯特地貌,溶洞,瀑布",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "贵阳市区乘坐公交车",
                "tips": "建议游玩半天"
            }
        ]
        return batch7

    def crawl_guizhou_attractions_batch8(self):
        """贵州景点数据 - 第八批（美食体验）"""
        batch8 = [
            {
                "name": "贵阳二七路小吃街",
                "address": "贵州省贵阳市云岩区",
                "category": "美食体验",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "二七路小吃街是贵阳著名的小吃街，有各种贵州特色小吃，如肠旺面、丝娃娃等。",
                "features": "小吃街,美食,夜市",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "贵阳市区步行可达",
                "tips": "建议晚上去，品尝各种小吃"
            },
            {
                "name": "贵阳青云路夜市",
                "address": "贵州省贵阳市南明区",
                "category": "美食体验",
                "ticket_price": "免费",
                "opening_hours": "18:00-02:00",
                "description": "青云路夜市是贵阳著名的夜市，有各种烧烤、小吃，是体验贵阳夜生活的好去处。",
                "features": "夜市,烧烤,小吃",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "贵阳市区步行可达",
                "tips": "建议晚上去"
            },
            {
                "name": "贵阳丝娃娃",
                "address": "贵州省贵阳市",
                "category": "美食体验",
                "ticket_price": "人均30元",
                "opening_hours": "10:00-22:00",
                "description": "丝娃娃是贵阳的特色小吃，用薄饼包裹各种蔬菜丝，蘸辣椒水食用。",
                "特色": "特色小吃,贵州美食,必吃",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "贵阳市区各处",
                "tips": "推荐杨姨妈丝娃娃"
            },
            {
                "name": "贵阳肠旺面",
                "address": "贵州省贵阳市",
                "category": "美食体验",
                "ticket_price": "人均15元",
                "opening_hours": "06:00-14:00",
                "description": "肠旺面是贵阳的特色早餐，用猪大肠、血旺、面条制作，味道独特。",
                "features": "特色早餐,贵州美食,必吃",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "贵阳市区各处",
                "tips": "推荐程肠旺"
            },
            {
                "name": "凯里酸汤鱼",
                "address": "贵州省黔东南苗族侗族自治州凯里市",
                "category": "美食体验",
                "ticket_price": "人均80元",
                "opening_hours": "10:00-22:00",
                "description": "酸汤鱼是黔东南的特色美食，用苗族酸汤煮鱼，味道酸辣鲜美。",
                "features": "苗族美食,酸汤鱼,必吃",
                "rating": 4.6,
                "best_season": "全年",
                "transportation": "凯里市区各处",
                "tips": "推荐亮欢寨"
            },
            {
                "name": "遵义羊肉粉",
                "address": "贵州省遵义市",
                "category": "美食体验",
                "ticket_price": "人均20元",
                "opening_hours": "06:00-14:00",
                "description": "羊肉粉是遵义的特色早餐，用羊肉、米粉制作，味道鲜美。",
                "features": "特色早餐,贵州美食,必吃",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "遵义市区各处",
                "tips": "推荐虾子羊肉粉"
            },
            {
                "name": "遵义豆花面",
                "address": "贵州省遵义市",
                "category": "美食体验",
                "ticket_price": "人均15元",
                "opening_hours": "06:00-14:00",
                "description": "豆花面是遵义的特色小吃，用豆花、面条制作，味道独特。",
                "features": "特色小吃,贵州美食,必吃",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "遵义市区各处",
                "tips": "推荐刘二妈米皮"
            },
            {
                "name": "安顺裹卷",
                "address": "贵州省安顺市",
                "category": "美食体验",
                "ticket_price": "人均10元",
                "opening_hours": "10:00-22:00",
                "description": "裹卷是安顺的特色小吃，用米皮包裹各种蔬菜，蘸辣椒水食用。",
                "features": "特色小吃,贵州美食,必吃",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "安顺市区各处",
                "tips": "推荐王记裹卷"
            },
            {
                "name": "安顺破酥包",
                "address": "贵州省安顺市",
                "category": "美食体验",
                "ticket_price": "人均5元",
                "opening_hours": "06:00-14:00",
                "description": "破酥包是安顺的特色早餐，用猪肉、面粉制作，皮薄馅多。",
                "features": "特色早餐,贵州美食,必吃",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "安顺市区各处",
                "tips": "推荐龙老太味噌鸡"
            },
            {
                "name": "兴义刷把头",
                "address": "贵州省黔西南布依族苗族自治州兴义市",
                "category": "美食体验",
                "ticket_price": "人均10元",
                "opening_hours": "06:00-14:00",
                "description": "刷把头是兴义的特色小吃，用面粉、猪肉制作，形状像刷把。",
                "features": "特色小吃,贵州美食,必吃",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "兴义市区各处",
                "tips": "推荐郑记刷把头"
            }
        ]
        return batch8

    def crawl_guizhou_attractions_batch9(self):
        """贵州景点数据 - 第九批（特色体验）"""
        batch9 = [
            {
                "name": "西江苗族长桌宴",
                "address": "贵州省黔东南苗族侗族自治州雷山县西江镇",
                "category": "特色体验",
                "ticket_price": "人均100元",
                "opening_hours": "18:00-21:00",
                "description": "长桌宴是苗族的传统宴席，有独特的苗族歌舞表演和美食。",
                "features": "苗族文化,长桌宴,歌舞表演",
                "rating": 4.6,
                "best_season": "全年",
                "transportation": "西江千户苗寨内",
                "tips": "建议提前预订"
            },
            {
                "name": "肇兴侗族大歌表演",
                "address": "贵州省黔东南苗族侗族自治州黎平县肇兴镇",
                "category": "特色体验",
                "ticket_price": "80元",
                "opening_hours": "20:00-21:30",
                "description": "侗族大歌是世界非物质文化遗产，有独特的多声部合唱。",
                "features": "侗族大歌,非遗,音乐表演",
                "rating": 4.5,
                "best_season": "全年",
                "transportation": "肇兴侗寨内",
                "tips": "建议提前购票"
            },
            {
                "name": "黔东南苗族银饰制作体验",
                "address": "贵州省黔东南苗族侗族自治州雷山县",
                "category": "特色体验",
                "ticket_price": "200元",
                "opening_hours": "09:00-17:00",
                "description": "体验苗族银饰制作技艺，了解苗族银饰文化。",
                "features": "苗族文化,银饰制作,非遗体验",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "雷山县城",
                "tips": "建议提前预约"
            },
            {
                "name": "黔东南蜡染体验",
                "address": "贵州省黔东南苗族侗族自治州",
                "category": "特色体验",
                "ticket_price": "150元",
                "opening_hours": "09:00-17:00",
                "description": "体验苗族蜡染技艺，制作自己的蜡染作品。",
                "features": "苗族文化,蜡染,非遗体验",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "黔东南各地",
                "tips": "建议提前预约"
            },
            {
                "name": "安顺地戏表演",
                "address": "贵州省安顺市",
                "category": "特色体验",
                "ticket_price": "80元",
                "opening_hours": "10:00-16:00",
                "description": "地戏是安顺的特色文化，有独特的面具和表演。",
                "features": "屯堡文化,地戏,面具表演",
                "rating": 4.4,
                "best_season": "全年",
                "transportation": "安顺各地",
                "tips": "建议提前了解表演时间"
            },
            {
                "name": "黔南布依族织锦体验",
                "address": "贵州省黔南布依族苗族自治州",
                "category": "特色体验",
                "ticket_price": "120元",
                "opening_hours": "09:00-17:00",
                "description": "体验布依族织锦技艺，了解布依族文化。",
                "features": "布依族文化,织锦,非遗体验",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "黔南各地",
                "tips": "建议提前预约"
            },
            {
                "name": "黔西南布依族八音坐唱",
                "address": "贵州省黔西南布依族苗族自治州",
                "category": "特色体验",
                "ticket_price": "60元",
                "opening_hours": "10:00-16:00",
                "description": "八音坐唱是布依族的传统音乐，有独特的乐器和表演。",
                "features": "布依族文化,八音坐唱,非遗",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "黔西南各地",
                "tips": "建议提前了解表演时间"
            },
            {
                "name": "黔东南苗族跳花场",
                "address": "贵州省黔东南苗族侗族自治州",
                "category": "特色体验",
                "ticket_price": "免费",
                "opening_hours": "特定节日",
                "description": "跳花场是苗族的传统节日，有独特的歌舞表演和社交活动。",
                "features": "苗族文化,跳花场,传统节日",
                "rating": 4.5,
                "best_season": "春节前后",
                "transportation": "黔东南各地",
                "tips": "需要了解具体时间"
            },
            {
                "name": "黔东南苗族姊妹节",
                "address": "贵州省黔东南苗族侗族自治州台江县",
                "category": "特色体验",
                "ticket_price": "免费",
                "opening_hours": "特定节日",
                "description": "姊妹节是苗族的传统节日，有独特的歌舞表演和社交活动。",
                "features": "苗族文化,姊妹节,传统节日",
                "rating": 4.6,
                "best_season": "农历三月十五",
                "transportation": "台江县城",
                "tips": "需要了解具体时间"
            },
            {
                "name": "黔东南苗族鼓藏节",
                "address": "贵州省黔东南苗族侗族自治州",
                "category": "特色体验",
                "ticket_price": "免费",
                "opening_hours": "特定节日",
                "description": "鼓藏节是苗族最隆重的节日，有独特的祭祀仪式和歌舞表演。",
                "features": "苗族文化,鼓藏节,传统节日",
                "rating": 4.7,
                "best_season": "每13年一次",
                "transportation": "黔东南各地",
                "tips": "需要了解具体时间"
            }
        ]
        return batch9

    def crawl_guizhou_attractions_batch10(self):
        """贵州景点数据 - 第十批（更多景点）"""
        batch10 = [
            {
                "name": "六盘水梅花山",
                "address": "贵州省六盘水市钟山区",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "梅花山是六盘水的著名景点，有壮观的峡谷风光和独特的喀斯特地貌。",
                "features": "峡谷,喀斯特地貌,户外运动",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "六盘水市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "六盘水野玉海",
                "address": "贵州省六盘水市水城县",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "野玉海有壮观的高山草甸和独特的彝族文化，是体验彝族风情的好去处。",
                "features": "高山草甸,彝族文化,户外运动",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "水城县城乘坐公交车",
                "tips": "建议游玩1天"
            },
            {
                "name": "毕节草海",
                "address": "贵州省毕节市威宁县",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "草海是贵州最大的天然淡水湖，有独特的湿地风光和丰富的鸟类资源。",
                "features": "湿地,观鸟,高原湖泊",
                "rating": 4.4,
                "best_season": "11月-次年3月",
                "transportation": "威宁县城乘坐公交车",
                "tips": "建议游玩1天"
            },
            {
                "name": "毕节百草坪",
                "address": "贵州省毕节市威宁县",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "百草坪是贵州最大的高山草场，有壮观的草原风光和独特的彝族文化。",
                "features": "高山草场,彝族文化,户外运动",
                "rating": 4.3,
                "best_season": "6-9月",
                "transportation": "威宁县城包车前往",
                "tips": "建议游玩1天"
            },
            {
                "name": "铜仁梵净山佛教文化苑",
                "address": "贵州省铜仁市江口县",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "08:00-17:00",
                "description": "梵净山佛教文化苑是梵净山的佛教文化展示中心，有独特的佛教建筑和文化。",
                "features": "佛教文化,建筑,文化展示",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "江口县城乘坐公交车",
                "tips": "建议游玩2-3小时"
            },
            {
                "name": "铜仁苗王城",
                "address": "贵州省铜仁市松桃县",
                "category": "人文景观",
                "ticket_price": "100元",
                "opening_hours": "08:00-17:00",
                "description": "苗王城是苗族的文化遗址，有独特的苗族建筑和文化。",
                "features": "苗族文化,苗王城,历史遗址",
                "rating": 4.3,
                "best_season": "全年",
                "transportation": "松桃县城乘坐班车",
                "tips": "建议游玩半天"
            },
            {
                "name": "黔南都匀毛尖茶文化园",
                "address": "贵州省黔南布依族苗族自治州都匀市",
                "category": "人文景观",
                "ticket_price": "免费",
                "opening_hours": "09:00-17:00",
                "description": "都匀毛尖茶文化园展示了都匀毛尖茶的历史和文化，可体验采茶制茶。",
                "features": "茶文化,都匀毛尖,体验",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "都匀市区乘坐公交车",
                "tips": "建议游玩半天"
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
                "tips": "建议游玩半天，需提前预约"
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
                "transportation": "兴义市区乘坐公交车",
                "tips": "建议游玩半天"
            },
            {
                "name": "黔西南贞丰三岔河",
                "address": "贵州省黔西南布依族苗族自治州贞丰县",
                "category": "自然风光",
                "ticket_price": "免费",
                "opening_hours": "全天",
                "description": "三岔河有壮观的峡谷风光和独特的布依族文化，是户外运动的好去处。",
                "features": "峡谷,布依族文化,户外运动",
                "rating": 4.2,
                "best_season": "全年",
                "transportation": "贞丰县城乘坐班车",
                "tips": "建议游玩半天"
            }
        ]
        return batch10

    def save_to_json(self, filename='data/guizhou_attractions.json'):
        """保存数据到JSON文件"""
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.attractions, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {filepath}，共 {len(self.attractions)} 个景点")

    def save_to_database(self):
        """保存数据到SQLite数据库"""
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'attractions.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 创建表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attractions (
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 清空旧数据
        cursor.execute('DELETE FROM attractions')

        # 插入新数据
        for attr in self.attractions:
            cursor.execute('''
                INSERT INTO attractions (name, address, category, ticket_price,
                opening_hours, description, features, rating, best_season,
                transportation, tips)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                attr.get('tips')
            ))

        conn.commit()
        conn.close()
        print(f"数据已保存到数据库 {db_path}，共 {len(self.attractions)} 个景点")

    def run(self):
        """运行爬虫"""
        print("=" * 60)
        print("贵州旅游景点爬虫启动 - 超级扩展版")
        print("=" * 60)

        # 爬取所有批次数据
        print("正在加载第一批景点数据（知名景点）...")
        self.attractions.extend(self.crawl_guizhou_attractions())

        print("正在加载第二批景点数据（更多景点）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch2())

        print("正在加载第三批景点数据（小众景点）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch3())

        print("正在加载第四批景点数据（自然景点）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch4())

        print("正在加载第五批景点数据（特色景点）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch5())

        print("正在加载第六批景点数据（民族村寨）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch6())

        print("正在加载第七批景点数据（更多小众景点）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch7())

        print("正在加载第八批景点数据（美食体验）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch8())

        print("正在加载第九批景点数据（特色体验）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch9())

        print("正在加载第十批景点数据（更多景点）...")
        self.attractions.extend(self.crawl_guizhou_attractions_batch10())

        print(f"\n总共加载 {len(self.attractions)} 个景点")

        # 保存数据
        self.save_to_json()
        self.save_to_database()

        # 统计信息
        self.print_statistics()

        print("=" * 60)
        print("爬取完成！")
        print("=" * 60)

    def print_statistics(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("数据统计")
        print("=" * 60)

        # 按类别统计
        categories = {}
        for attr in self.attractions:
            cat = attr.get('category', '未分类')
            categories[cat] = categories.get(cat, 0) + 1

        print("\n按类别统计：")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} 个")

        # 按地区统计
        regions = {}
        for attr in self.attractions:
            addr = attr.get('address', '')
            if '贵阳' in addr:
                region = '贵阳'
            elif '遵义' in addr:
                region = '遵义'
            elif '安顺' in addr:
                region = '安顺'
            elif '黔东南' in addr:
                region = '黔东南'
            elif '黔南' in addr:
                region = '黔南'
            elif '黔西南' in addr:
                region = '黔西南'
            elif '铜仁' in addr:
                region = '铜仁'
            elif '毕节' in addr:
                region = '毕节'
            elif '六盘水' in addr:
                region = '六盘水'
            else:
                region = '其他'
            regions[region] = regions.get(region, 0) + 1

        print("\n按地区统计：")
        for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
            print(f"  {region}: {count} 个")

        # 评分统计
        ratings = [attr.get('rating', 0) for attr in self.attractions if attr.get('rating')]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            max_rating = max(ratings)
            min_rating = min(ratings)
            print(f"\n评分统计：")
            print(f"  平均评分: {avg_rating:.2f}")
            print(f"  最高评分: {max_rating}")
            print(f"  最低评分: {min_rating}")

        # 门票统计
        free_count = sum(1 for attr in self.attractions if '免费' in str(attr.get('ticket_price', '')))
        paid_count = len(self.attractions) - free_count
        print(f"\n门票统计：")
        print(f"  免费景点: {free_count} 个")
        print(f"  收费景点: {paid_count} 个")


if __name__ == '__main__':
    spider = GuizhouSpider()
    spider.run()
