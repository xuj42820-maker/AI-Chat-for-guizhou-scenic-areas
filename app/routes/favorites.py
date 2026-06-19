"""
收藏 API 路由 — 添加、删除、查询

用户身份通过 Flask session 管理，首次访问时自动分配唯一 ID，
不再信任客户端传入的 user_id，防止越权操作。
"""
import uuid
import sqlite3
from flask import Blueprint, jsonify, request, session
from app.db import execute_query, execute_write

favorites_bp = Blueprint('favorites', __name__)


def _get_user_id():
    """获取当前用户的唯一标识（基于 session）"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']


@favorites_bp.route('/api/favorites')
def get_favorites():
    """获取当前用户的收藏"""
    user_id = _get_user_id()
    favorites = execute_query('''
        SELECT a.* FROM attractions a
        JOIN favorites f ON a.id = f.attraction_id
        WHERE f.user_id = ?
    ''', (user_id,))
    return jsonify(favorites)


@favorites_bp.route('/api/favorites', methods=['POST'])
def add_favorite():
    """添加收藏"""
    user_id = _get_user_id()
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少参数'}), 400
    attraction_id = data.get('attraction_id')

    if not attraction_id:
        return jsonify({'error': '缺少景点ID'}), 400

    try:
        execute_write('INSERT INTO favorites (user_id, attraction_id) VALUES (?, ?)',
                      (user_id, attraction_id))
        return jsonify({'message': '收藏成功'})
    except sqlite3.IntegrityError:
        return jsonify({'message': '已经收藏过了'})


@favorites_bp.route('/api/favorites', methods=['DELETE'])
def remove_favorite():
    """取消收藏"""
    user_id = _get_user_id()
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少参数'}), 400
    attraction_id = data.get('attraction_id')

    if not attraction_id:
        return jsonify({'error': '缺少景点ID'}), 400

    execute_write('DELETE FROM favorites WHERE user_id = ? AND attraction_id = ?',
                  (user_id, attraction_id))
    return jsonify({'message': '取消收藏成功'})
