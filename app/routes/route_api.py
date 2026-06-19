"""
路线 API 路由 — 查询和推荐
"""
import re
from flask import Blueprint, jsonify, request
from app.db import execute_query, DatabaseContext

route_bp = Blueprint('route_api', __name__)


@route_bp.route('/api/routes')
def get_routes():
    """获取所有路线"""
    routes = execute_query('SELECT * FROM routes')
    return jsonify(routes)


@route_bp.route('/api/routes/<int:route_id>')
def get_route(route_id):
    """获取单个路线（含景点详情）"""
    def _query(conn):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM routes WHERE id = ?', (route_id,))
        row = cursor.fetchone()
        if not row:
            return None

        route = dict(row)
        attraction_names = route.get('attractions_list', '').split(',')
        attractions = []
        for name in attraction_names:
            name = name.strip()
            if name:
                cursor.execute('SELECT * FROM attractions WHERE name = ?', (name,))
                attr_row = cursor.fetchone()
                if attr_row:
                    attractions.append(dict(attr_row))
        route['attractions'] = attractions
        return route

    with DatabaseContext() as conn:
        route = _query(conn)

    if not route:
        return jsonify({'error': '路线不存在'}), 404
    return jsonify(route)


@route_bp.route('/api/routes/recommend', methods=['POST'])
def recommend_route():
    """智能推荐路线"""
    data = request.get_json() or {}
    days = data.get('days', 3)
    preference = data.get('preference', '')

    if preference:
        routes = execute_query("SELECT * FROM routes WHERE route_type LIKE ?", ('%' + preference + '%',))
    else:
        routes = execute_query('SELECT * FROM routes')

    def _match_days(route_duration, target_days):
        """从路线时长中提取天数并精确匹配，例如 '3天2晚' → 3"""
        match = re.search(r'(\d+)\s*天', route_duration or '')
        if match:
            return int(match.group(1)) == target_days
        return False

    recommended = [r for r in routes if _match_days(r.get('duration', ''), days)]
    if not recommended:
        recommended = routes[:3]

    return jsonify(recommended)
