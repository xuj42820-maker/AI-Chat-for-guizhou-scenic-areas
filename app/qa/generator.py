"""
回答生成模块 — 根据意图和检索结果生成回答

职责：
- 根据意图选择回答模板
- 用景点数据填充模板
- 生成追问建议

新增意图的回答只需：
1. 在 generate() 中添加一个 elif 分支
"""

from app.qa.intent import match_city


class AnswerGenerator:
    """回答生成器"""

    def __init__(self, restaurants=None, travel_tips=None, routes=None):
        """
        Args:
            restaurants: 城市→餐厅列表 字典
            travel_tips: 旅行贴士字典
            routes: 路线列表
        """
        self.restaurants = restaurants or {}
        self.travel_tips = travel_tips or {}
        self.routes = routes or []

    def generate(self, query, intent, results):
        """
        根据意图和检索结果生成回答

        Args:
            query: 原始查询
            intent: 意图字符串
            results: 检索到的景点列表

        Returns:
            回答文本字符串
        """
        if not results:
            return "抱歉，没有找到相关信息。您可以尝试询问贵州的景点、门票、开放时间、交通等问题。"

        top = results[0]

        # 每个意图对应一个生成方法
        handlers = {
            'ticket':    self._gen_ticket,
            'hours':     self._gen_hours,
            'address':   self._gen_address,
            'transport': self._gen_transport,
            'phone':     self._gen_phone,
            'season':    self._gen_season,
            'free':      self._gen_free,
            'recommend': self._gen_recommend,
            'food':      self._gen_food,
            'route':     self._gen_route,
            'duration':  self._gen_duration,
            'nearby':    self._gen_nearby,
            'photo':     self._gen_photo,
            'tips':      self._gen_tips,
            'culture':   self._gen_culture,
            'safety':    self._gen_safety,
        }

        handler = handlers.get(intent, self._gen_general)
        return handler(results, top)

    def generate_suggestions(self, query, results):
        """生成相关追问建议"""
        suggestions = []
        if results:
            name = results[0].get('name') or ''
            suggestions.append(f"{name}门票多少钱？")
            suggestions.append(f"{name}怎么去？")
            suggestions.append(f"{name}最佳游玩季节？")
        suggestions.extend([
            "贵州有哪些免费景点？",
            "贵州最佳旅游季节是什么时候？",
            "贵州有什么特色美食？",
            "贵州旅行需要注意什么？",
            "贵州有什么民族文化体验？"
        ])
        return suggestions[:4]

    # ==================== 各意图的生成方法 ====================

    def _gen_ticket(self, results, top):
        if len(results) == 1:
            return f"{top['name']}的门票价格是{top.get('ticket_price', '暂无信息')}。"
        lines = "以下是相关景点的门票信息：\n"
        for a in results[:3]:
            lines += f"- {a['name']}：{a.get('ticket_price', '暂无')}\n"
        return lines

    def _gen_hours(self, results, top):
        if len(results) == 1:
            return f"{top['name']}的开放时间是{top.get('opening_hours', '暂无信息')}。"
        lines = "以下是相关景点的开放时间：\n"
        for a in results[:3]:
            lines += f"- {a['name']}：{a.get('opening_hours', '暂无')}\n"
        return lines

    def _gen_address(self, results, top):
        if len(results) == 1:
            return f"{top['name']}位于{top.get('address', '暂无信息')}。"
        lines = "以下是相关景点的地址：\n"
        for a in results[:3]:
            lines += f"- {a['name']}：{a.get('address', '暂无')}\n"
        return lines

    def _gen_transport(self, results, top):
        if len(results) == 1:
            return f"前往{top['name']}的交通方式：{top.get('transportation', '暂无信息')}。"
        lines = "以下是相关景点的交通信息：\n"
        for a in results[:3]:
            lines += f"- {a['name']}：{a.get('transportation', '暂无')}\n"
        return lines

    def _gen_phone(self, results, top):
        if len(results) == 1:
            return f"{top['name']}的联系电话是{top.get('phone', '暂无信息')}。"
        lines = "以下是相关景点的联系电话：\n"
        for a in results[:3]:
            lines += f"- {a['name']}：{a.get('phone', '暂无')}\n"
        return lines

    def _gen_season(self, results, top):
        if len(results) == 1:
            return f"{top['name']}的最佳游玩季节是{top.get('best_season', '全年')}。"
        lines = "以下是相关景点的最佳游玩季节：\n"
        for a in results[:3]:
            lines += f"- {a['name']}：{a.get('best_season', '全年')}\n"
        return lines

    def _gen_free(self, results, top):
        from app.db import execute_query
        free = [a for a in results if '免费' in (a.get('ticket_price') or '')]
        if not free:
            free = execute_query("SELECT * FROM attractions WHERE ticket_price LIKE '%免费%'")
        if free:
            lines = f"共找到 {len(free)} 个免费景点：\n"
            for a in free[:8]:
                lines += f"- {a['name']}：{a.get('address', '')}\n"
            return lines
        return "抱歉，暂未找到免费景点信息。"

    def _gen_recommend(self, results, top):
        lines = "为您推荐以下贵州景点：\n"
        for i, a in enumerate(results[:5], 1):
            desc = (a.get('description') or '')[:50]
            lines += f"{i}. {a['name']}（评分 {a.get('rating', '无')}）- {desc}...\n"
        return lines

    def _gen_food(self, results, top):
        lines = ""
        city = match_city(top.get('address'))
        city_restaurants = self._get_city_restaurants(city)
        if city_restaurants:
            lines += f"📍 {city}特色餐厅推荐：\n"
            for r in city_restaurants:
                lines += f"- {r['name']}：招牌{r['specialty']}，人均{r['avg_price']}，地址{r['address']}\n"
            lines += "\n"

        if self.travel_tips.get('food_highlights'):
            lines += "🍜 贵州特色美食：\n"
            for item in self.travel_tips['food_highlights']:
                lines += f"- {item}\n"
        elif not city_restaurants:
            lines += "贵州特色美食推荐：\n"
            lines += "- 酸汤鱼（凯里、黔东南）\n"
            lines += "- 羊肉粉（遵义）\n"
            lines += "- 花溪牛肉粉（贵阳）\n"
            lines += "- 丝娃娃（贵阳）\n"
            lines += "- 裹卷（安顺）\n"
            lines += "- 豆花面（遵义）\n"

        if top.get('nearby_restaurants'):
            lines += f"\n{top['name']}附近美食：{top['nearby_restaurants']}\n"
        return lines

    def _gen_route(self, results, top):
        """生成路线推荐回答（不包含美食推荐）"""
        import re
        from app.db import execute_query

        # 从查询中提取天数
        query = top.get('_query', '') if isinstance(top, dict) else ''
        days_match = re.search(r'(\d+)\s*日', query)
        target_days = int(days_match.group(1)) if days_match else None

        # 查询路线数据
        if target_days:
            routes = execute_query("SELECT * FROM routes WHERE duration LIKE ?", (f'%{target_days}天%',))
        else:
            routes = execute_query("SELECT * FROM routes")

        if not routes:
            routes = execute_query("SELECT * FROM routes LIMIT 3")

        if not routes:
            return "抱歉，暂无路线推荐信息。您可以尝试询问具体的景点信息。"

        lines = f"🧭 为您推荐以下贵州旅游路线：\n\n"
        for i, route in enumerate(routes[:3], 1):
            lines += f"**{i}. {route['name']}**\n"
            lines += f"   📝 {route.get('description', '')}\n"
            lines += f"   🕐 时长：{route.get('duration', '待定')} | 💰 预算：{route.get('budget', '待定')} | 📊 难度：{route.get('difficulty', '简单')}\n"

            # 显示景点列表（不包含美食推荐）
            attractions_list = route.get('attractions_list', '')
            if attractions_list:
                attractions = [a.strip() for a in attractions_list.split(',') if a.strip()]
                # 过滤掉美食相关的景点
                attractions = [a for a in attractions if not any(food_kw in a for food_kw in ['小吃', '美食', '餐厅', '粉', '面', '酸汤'])]
                if attractions:
                    lines += f"   📍 景点：{' → '.join(attractions)}\n"
            lines += "\n"

        return lines

    def _gen_duration(self, results, top):
        if len(results) == 1:
            return f"{top['name']}建议游玩时长为{top.get('suggested_duration', '半天至一天')}。"
        lines = "以下是相关景点的建议游玩时长：\n"
        for a in results[:3]:
            lines += f"- {a['name']}：{a.get('suggested_duration', '半天至一天')}\n"
        return lines

    def _gen_nearby(self, results, top):
        nearby = top.get('nearby_attractions') or ''
        answer = f"{top['name']}附近景点：{nearby if nearby else '暂无数据'}。"
        if top.get('nearby_restaurants'):
            answer += f"\n附近美食：{top['nearby_restaurants']}"
        if top.get('nearby_hotels'):
            answer += f"\n附近住宿：{top['nearby_hotels']}"
        return answer

    def _gen_photo(self, results, top):
        spots = top.get('best_photo_spots') or ''
        answer = f"{top['name']}的拍照推荐：{spots if spots else '景区内各处均可拍照留念'}。"
        if top.get('photography_tips'):
            answer += f"\n摄影小贴士：{top['photography_tips']}"
        return answer

    def _gen_tips(self, results, top):
        lines = "📋 贵州旅行实用贴士：\n"
        if self.travel_tips.get('best_time'):
            lines += "\n🕐 最佳旅行时间：\n"
            for season, info in self.travel_tips['best_time'].items():
                lines += f"  - {info}\n"
        if self.travel_tips.get('accommodation'):
            lines += "\n🏨 住宿建议：\n"
            for level, info in self.travel_tips['accommodation'].items():
                lines += f"  - {info}\n"
        if self.travel_tips.get('transportation'):
            lines += "\n🚗 交通信息：\n"
            for key, info in self.travel_tips['transportation'].items():
                lines += f"  - {info}\n"
        return lines

    def _gen_culture(self, results, top):
        lines = "🎭 贵州民族文化体验：\n"
        if self.travel_tips.get('cultural_experiences'):
            for exp in self.travel_tips['cultural_experiences']:
                lines += f"- {exp}\n"
        else:
            lines += "- 苗族长桌宴 — 西江千户苗寨\n"
            lines += "- 侗族大歌 — 肇兴侗寨\n"
            lines += "- 蜡染制作 — 黔东南各地\n"
            lines += "- 银饰制作 — 雷山县\n"
            lines += "- 地戏表演 — 安顺屯堡\n"
        if top.get('history_culture'):
            lines += f"\n{top['name']}文化背景：{top['history_culture']}"
        return lines

    def _gen_safety(self, results, top):
        lines = "⚠️ 贵州旅行安全提示：\n"
        if self.travel_tips.get('safety_tips'):
            for tip in self.travel_tips['safety_tips']:
                lines += f"- {tip}\n"
        else:
            lines += "- 山区道路弯多，注意晕车\n"
            lines += "- 溶洞内温度低，带外套\n"
            lines += "- 漂流注意安全，听从工作人员指挥\n"
            lines += "- 尊重少数民族习俗\n"
            lines += "- 旺季提前预订门票和住宿\n"
        return lines

    def _gen_general(self, results, top):
        if len(results) == 1:
            a = results[0]
            answer = f"**{a['name']}**\n\n"
            answer += f"📍 地址：{a.get('address') or '暂无'}\n"
            answer += f"🎫 门票：{a.get('ticket_price') or '暂无'}\n"
            answer += f"⏰ 开放时间：{a.get('opening_hours') or '暂无'}\n"
            answer += f"⭐ 评分：{a.get('rating') or '暂无'}\n"
            answer += f"\n{a.get('description') or ''}"
            return answer

        answer = "为您找到以下相关景点：\n\n"
        for i, a in enumerate(results[:5], 1):
            answer += f"{i}. **{a['name']}**\n"
            answer += f"   门票：{a.get('ticket_price') or '暂无'} | 评分：{a.get('rating') or '暂无'}\n"
            answer += f"   {(a.get('description') or '')[:60]}...\n\n"
        return answer

    # ==================== 辅助方法 ====================

    def _get_city_restaurants(self, city):
        """获取指定城市的餐厅列表"""
        if not city:
            return []
        for key in self.restaurants:
            if key in city or city in key:
                return self.restaurants[key]
        return []
