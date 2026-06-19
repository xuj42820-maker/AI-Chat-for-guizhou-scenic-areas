"""
统计 API 路由 — 数据统计
"""
from flask import Blueprint, jsonify
from app.db import with_db

stats_bp = Blueprint('stats', __name__)

# 贵州省 9 个市/州（单一来源，避免重复定义）
REGIONS = ['贵阳', '遵义', '安顺', '黔东南', '黔南', '黔西南', '铜仁', '毕节', '六盘水']


@stats_bp.route('/api/statistics')
def get_statistics():
    """获取统计数据"""
    def _query(conn):
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM attractions')
        total = cursor.fetchone()[0]

        cursor.execute('SELECT category, COUNT(*) as count FROM attractions GROUP BY category')
        categories = {row['category']: row['count'] for row in cursor.fetchall()}

        regions = {}
        for region in REGIONS:
            cursor.execute("SELECT COUNT(*) FROM attractions WHERE address LIKE ?", ('%' + region + '%',))
            regions[region] = cursor.fetchone()[0]

        cursor.execute('SELECT AVG(rating), MAX(rating), MIN(rating) FROM attractions WHERE rating IS NOT NULL')
        avg_rating, max_rating, min_rating = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM attractions WHERE ticket_price LIKE '%免费%'")
        free_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM routes')
        routes_count = cursor.fetchone()[0]

        return {
            'total': total,
            'categories': categories,
            'regions': regions,
            'avg_rating': round(avg_rating, 2) if avg_rating else 0,
            'max_rating': max_rating,
            'min_rating': min_rating,
            'free_count': free_count,
            'routes_count': routes_count
        }

    return jsonify(with_db(_query))
