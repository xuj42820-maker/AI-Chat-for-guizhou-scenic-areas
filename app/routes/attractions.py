"""
景点 API 路由 — 查询、搜索、筛选
"""
from flask import Blueprint, jsonify, request
from app.db import execute_query, DatabaseContext, with_db

attractions_bp = Blueprint('attractions', __name__)


@attractions_bp.route('/api/attractions')
def get_attractions():
    """获取所有景点（含主图）"""
    attractions = execute_query('''
        SELECT a.*, i.image_url
        FROM attractions a
        LEFT JOIN images i ON a.id = i.attraction_id AND i.is_primary = 1
        ORDER BY a.rating DESC
    ''')
    return jsonify(attractions)


@attractions_bp.route('/api/attractions/<int:attraction_id>')
def get_attraction(attraction_id):
    """获取单个景点（含图片和攻略）"""
    def _query(conn):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM attractions WHERE id = ?', (attraction_id,))
        row = cursor.fetchone()
        if not row:
            return None

        attraction = dict(row)
        cursor.execute('SELECT * FROM images WHERE attraction_id = ? ORDER BY is_primary DESC', (attraction_id,))
        attraction['images'] = [dict(img) for img in cursor.fetchall()]
        cursor.execute('SELECT * FROM guides WHERE attraction_id = ?', (attraction_id,))
        attraction['guides'] = [dict(guide) for guide in cursor.fetchall()]
        return attraction

    with DatabaseContext() as conn:
        attraction = _query(conn)

    if not attraction:
        return jsonify({'error': '景点不存在'}), 404
    return jsonify(attraction)


@attractions_bp.route('/api/attractions/category/<category>')
def get_attractions_by_category(category):
    """按类别获取景点"""
    attractions = execute_query('SELECT * FROM attractions WHERE category = ?', (category,))
    return jsonify(attractions)


@attractions_bp.route('/api/attractions/region/<region>')
def get_attractions_by_region(region):
    """按地区获取景点"""
    attractions = execute_query("SELECT * FROM attractions WHERE address LIKE ?", ('%' + region + '%',))
    return jsonify(attractions)


@attractions_bp.route('/api/attractions/search')
def search_attractions():
    """搜索景点"""
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify([])

    attractions = execute_query(
        "SELECT * FROM attractions WHERE name LIKE ? OR description LIKE ? OR features LIKE ? LIMIT 10",
        ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
    )
    return jsonify(attractions)


@attractions_bp.route('/api/attractions/top')
def get_top_attractions():
    """获取评分最高的景点（含主图）"""
    limit = request.args.get('limit', 10, type=int)

    def _query(conn):
        cursor = conn.cursor()
        # 使用 LEFT JOIN 一次性查询景点和主图，避免 N+1 查询
        cursor.execute('''
            SELECT a.*, i.image_url
            FROM attractions a
            LEFT JOIN images i ON a.id = i.attraction_id AND i.is_primary = 1
            WHERE a.rating IS NOT NULL
            ORDER BY a.rating DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    return jsonify(with_db(_query))


@attractions_bp.route('/api/attractions/free')
def get_free_attractions():
    """获取免费景点"""
    attractions = execute_query("SELECT * FROM attractions WHERE ticket_price LIKE '%免费%'")
    return jsonify(attractions)


@attractions_bp.route('/api/attractions/coordinates')
def get_attraction_coordinates():
    """获取所有景点坐标（用于地图）"""
    attractions = execute_query(
        'SELECT id, name, address, category, ticket_price, rating, description, features, latitude, longitude FROM attractions'
    )
    return jsonify(attractions)
