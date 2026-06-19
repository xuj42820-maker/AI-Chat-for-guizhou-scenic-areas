"""
数据库连接管理 — 统一的数据库访问层
所有模块通过此模块获取数据库连接，不再各自管理连接生命周期。
"""

import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

# 数据库路径（单一来源）
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'guizhou_travel.db')


def get_db():
    """获取数据库连接（设置了 Row factory）"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def close_db(conn):
    """安全关闭数据库连接"""
    if conn:
        try:
            conn.close()
        except Exception as e:
            logger.warning(f"关闭数据库连接失败: {e}")


class DatabaseContext:
    """
    数据库上下文管理器 — 自动管理连接生命周期

    用法:
        with DatabaseContext() as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM attractions')
            rows = cursor.fetchall()
    """

    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            try:
                if exc_type is None:
                    self.conn.commit()
                else:
                    self.conn.rollback()
                self.conn.close()
            except Exception as e:
                logger.warning(f"关闭数据库连接失败: {e}")
        return False  # 不吞掉异常


def with_db(query_fn):
    """
    装饰器/辅助函数 — 在一个连接内执行查询函数

    用法:
        def get_all_attractions(conn):
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attractions')
            return [dict(row) for row in cursor.fetchall()]

        result = with_db(get_all_attractions)
    """
    with DatabaseContext() as conn:
        return query_fn(conn)


def execute_query(sql, params=None, fetch_one=False):
    """
    执行查询并返回结果

    用法:
        attractions = execute_query('SELECT * FROM attractions WHERE category = ?', ('自然',))
        count = execute_query('SELECT COUNT(*) FROM attractions', fetch_one=True)
    """
    with DatabaseContext() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        if fetch_one:
            row = cursor.fetchone()
            return dict(row) if row else None
        return [dict(row) for row in cursor.fetchall()]


def execute_write(sql, params=None):
    """
    执行写操作（INSERT/UPDATE/DELETE）

    用法:
        execute_write('INSERT INTO favorites (user_id, attraction_id) VALUES (?, ?)', ('user1', 5))
    """
    with DatabaseContext() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        return cursor.lastrowid
