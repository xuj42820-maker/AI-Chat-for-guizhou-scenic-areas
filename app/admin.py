"""
管理员后台 — Blueprint
"""
import os
import json
import hmac
import sqlite3
from functools import wraps
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

from app.db import get_db, close_db, DatabaseContext, execute_query, execute_write, with_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'guizhou_attractions.json')


# ==================== 简易登录验证 ====================

import secrets

ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS')

if not ADMIN_PASS:
    # 未设置环境变量时，生成随机密码并在首次使用时警告
    ADMIN_PASS = secrets.token_urlsafe(16)
    import warnings
    warnings.warn(
        f"未设置 ADMIN_PASS 环境变量，已生成临时密码: {ADMIN_PASS}\n"
        "请在生产环境中设置 ADMIN_PASS 环境变量。",
        UserWarning,
        stacklevel=2
    )


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


# ==================== 页面路由 ====================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if hmac.compare_digest(username, ADMIN_USER) and hmac.compare_digest(password, ADMIN_PASS):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        return render_template('admin/login.html', error='用户名或密码错误')
    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


@admin_bp.route('/')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/attractions')
@login_required
def attractions():
    return render_template('admin/attractions.html')


@admin_bp.route('/routes')
@login_required
def routes():
    return render_template('admin/routes.html')


# ==================== API: 统计 ====================

@admin_bp.route('/api/stats')
@login_required
def api_stats():
    def _query(conn):
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM attractions')
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM attractions WHERE ticket_price LIKE '%免费%'")
        free = cur.fetchone()[0]
        cur.execute('SELECT AVG(rating) FROM attractions WHERE rating > 0')
        avg_rating = cur.fetchone()[0] or 0
        cur.execute('SELECT COUNT(DISTINCT category) FROM attractions')
        categories = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM routes')
        route_count = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM favorites')
        fav_count = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM images')
        img_count = cur.fetchone()[0]

        # 分类统计
        cur.execute('SELECT category, COUNT(*) as cnt FROM attractions GROUP BY category ORDER BY cnt DESC')
        cat_stats = [dict(r) for r in cur.fetchall()]

        # 地区统计
        cur.execute("""SELECT CASE
            WHEN address LIKE '%贵阳%' THEN '贵阳'
            WHEN address LIKE '%遵义%' THEN '遵义'
            WHEN address LIKE '%安顺%' THEN '安顺'
            WHEN address LIKE '%黔东南%' THEN '黔东南'
            WHEN address LIKE '%黔南%' THEN '黔南'
            WHEN address LIKE '%黔西南%' THEN '黔西南'
            WHEN address LIKE '%铜仁%' THEN '铜仁'
            WHEN address LIKE '%毕节%' THEN '毕节'
            WHEN address LIKE '%六盘水%' THEN '六盘水'
            ELSE '其他' END as region, COUNT(*) as cnt
            FROM attractions GROUP BY region ORDER BY cnt DESC""")
        region_stats = [dict(r) for r in cur.fetchall()]

        # 评分分布
        cur.execute("""SELECT CASE
            WHEN rating >= 4.5 THEN '4.5+'
            WHEN rating >= 4.0 THEN '4.0-4.4'
            WHEN rating >= 3.5 THEN '3.5-3.9'
            ELSE '3.5以下' END as range, COUNT(*) as cnt
            FROM attractions GROUP BY range ORDER BY range DESC""")
        rating_stats = [dict(r) for r in cur.fetchall()]

        return {
            'total': total, 'free': free, 'avg_rating': round(avg_rating, 1),
            'categories': categories, 'routes': route_count,
            'favorites': fav_count, 'images': img_count,
            'cat_stats': cat_stats, 'region_stats': region_stats,
            'rating_stats': rating_stats
        }

    return jsonify(with_db(_query))


# ==================== API: 景点 CRUD ====================

@admin_bp.route('/api/attractions')
@login_required
def api_attractions():
    rows = execute_query('SELECT * FROM attractions ORDER BY id')
    return jsonify(rows)


@admin_bp.route('/api/attractions/<int:aid>', methods=['GET'])
@login_required
def api_attraction_get(aid):
    row = execute_query('SELECT * FROM attractions WHERE id=?', (aid,), fetch_one=True)
    if not row:
        return jsonify({'error': 'not found'}), 404
    return jsonify(row)


def _safe_float(value, default=0.0):
    """安全地将值转换为浮点数，失败时返回默认值"""
    if value is None or value == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


@admin_bp.route('/api/attractions', methods=['POST'])
@login_required
def api_attraction_create():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name required'}), 400

    new_id = execute_write(
        '''INSERT INTO attractions (name, address, category, ticket_price, opening_hours,
        description, features, rating, best_season, transportation, tips, phone, official_website,
        latitude, longitude) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (
            data.get('name'), data.get('address', ''), data.get('category', ''),
            data.get('ticket_price', ''), data.get('opening_hours', ''),
            data.get('description', ''), data.get('features', ''),
            _safe_float(data.get('rating')), data.get('best_season', ''),
            data.get('transportation', ''), data.get('tips', ''),
            data.get('phone', ''), data.get('official_website', ''),
            _safe_float(data.get('latitude')), _safe_float(data.get('longitude'))
        )
    )
    return jsonify({'id': new_id, 'message': 'created'})


@admin_bp.route('/api/attractions/<int:aid>', methods=['PUT'])
@login_required
def api_attraction_update(aid):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'no data'}), 400

    fields = ['name', 'address', 'category', 'ticket_price', 'opening_hours',
              'description', 'features', 'rating', 'best_season', 'transportation',
              'tips', 'phone', 'official_website', 'latitude', 'longitude']
    updates = []
    values = []
    for f in fields:
        if f in data:
            updates.append(f'{f}=?')
            values.append(data[f])
    if not updates:
        return jsonify({'error': 'no fields to update'}), 400
    values.append(aid)

    def _update(conn):
        conn.cursor().execute(f'UPDATE attractions SET {", ".join(updates)} WHERE id=?', values)

    with DatabaseContext() as conn:
        _update(conn)
    return jsonify({'message': 'updated'})


@admin_bp.route('/api/attractions/<int:aid>', methods=['DELETE'])
@login_required
def api_attraction_delete(aid):
    def _delete(conn):
        cur = conn.cursor()
        cur.execute('DELETE FROM images WHERE attraction_id=?', (aid,))
        cur.execute('DELETE FROM guides WHERE attraction_id=?', (aid,))
        cur.execute('DELETE FROM favorites WHERE attraction_id=?', (aid,))
        cur.execute('DELETE FROM attractions WHERE id=?', (aid,))

    with DatabaseContext() as conn:
        _delete(conn)
    return jsonify({'message': 'deleted'})


# ==================== API: 路线 CRUD ====================

@admin_bp.route('/api/routes')
@login_required
def api_routes():
    rows = execute_query('SELECT * FROM routes ORDER BY id')
    return jsonify(rows)


@admin_bp.route('/api/routes', methods=['POST'])
@login_required
def api_route_create():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name required'}), 400

    new_id = execute_write(
        '''INSERT INTO routes (name, description, duration, difficulty, season,
        budget, attractions_list, route_type) VALUES (?,?,?,?,?,?,?,?)''',
        (
            data.get('name'), data.get('description', ''), data.get('duration', ''),
            data.get('difficulty', ''), data.get('season', ''),
            data.get('budget', ''), data.get('attractions_list', ''),
            data.get('route_type', '')
        )
    )
    return jsonify({'id': new_id, 'message': 'created'})


@admin_bp.route('/api/routes/<int:rid>', methods=['PUT'])
@login_required
def api_route_update(rid):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'no data'}), 400

    fields = ['name', 'description', 'duration', 'difficulty', 'season',
              'budget', 'attractions_list', 'route_type']
    updates, values = [], []
    for f in fields:
        if f in data:
            updates.append(f'{f}=?')
            values.append(data[f])
    if not updates:
        return jsonify({'error': 'no fields'}), 400
    values.append(rid)

    def _update(conn):
        conn.cursor().execute(f'UPDATE routes SET {", ".join(updates)} WHERE id=?', values)

    with DatabaseContext() as conn:
        _update(conn)
    return jsonify({'message': 'updated'})


@admin_bp.route('/api/routes/<int:rid>', methods=['DELETE'])
@login_required
def api_route_delete(rid):
    execute_write('DELETE FROM routes WHERE id=?', (rid,))
    return jsonify({'message': 'deleted'})
