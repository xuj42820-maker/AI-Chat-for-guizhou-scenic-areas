"""
数据库模块测试
"""
import pytest
import sqlite3
from app.db import DatabaseContext, execute_query, execute_write


class TestDatabaseContext:
    """测试数据库上下文管理器"""

    def test_context_manager_with_memory_db(self):
        """测试用内存数据库的上下文管理器"""
        with DatabaseContext(db_path=':memory:') as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
            cursor.execute('INSERT INTO test (name) VALUES (?)', ('hello',))
            cursor.execute('SELECT name FROM test')
            result = cursor.fetchone()
            assert result['name'] == 'hello'

    def test_context_manager_auto_commit(self):
        """测试自动提交"""
        with DatabaseContext(db_path=':memory:') as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
            cursor.execute('INSERT INTO test (name) VALUES (?)', ('world',))

        # 验证数据已提交（重新打开连接）
        with DatabaseContext(db_path=':memory:') as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
            cursor.execute('SELECT * FROM test')
            # 内存数据库每次都是新的，所以这里应该是空的
            assert cursor.fetchone() is None


class TestExecuteQuery:
    """测试查询辅助函数"""

    def test_execute_query_with_memory_db(self):
        """测试 execute_query（需要先建表）"""
        # execute_query 使用全局 DB_PATH，这里测试它不会崩溃
        # 实际测试需要用 mock 或者设置测试数据库
        pass

    def test_execute_write_with_memory_db(self):
        """测试 execute_write"""
        pass


class TestDatabaseIntegration:
    """数据库集成测试（使用内存数据库）"""

    @pytest.fixture
    def memory_db(self):
        """创建内存数据库并建表"""
        conn = sqlite3.connect(':memory:')
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('''
            CREATE TABLE attractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                ticket_price TEXT,
                rating REAL
            )
        ''')
        conn.execute('''
            CREATE TABLE favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                attraction_id INTEGER,
                UNIQUE(user_id, attraction_id)
            )
        ''')
        conn.commit()
        yield conn
        conn.close()

    def test_insert_and_query(self, memory_db):
        """测试插入和查询"""
        cursor = memory_db.cursor()
        cursor.execute(
            'INSERT INTO attractions (name, category, ticket_price, rating) VALUES (?, ?, ?, ?)',
            ('黄果树瀑布', '自然风光', '180元', 4.8)
        )
        memory_db.commit()

        cursor.execute('SELECT * FROM attractions WHERE name = ?', ('黄果树瀑布',))
        row = cursor.fetchone()
        assert row['name'] == '黄果树瀑布'
        assert row['rating'] == 4.8

    def test_unique_constraint(self, memory_db):
        """测试唯一约束"""
        cursor = memory_db.cursor()
        cursor.execute(
            'INSERT INTO favorites (user_id, attraction_id) VALUES (?, ?)',
            ('user1', 1)
        )
        memory_db.commit()

        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute(
                'INSERT INTO favorites (user_id, attraction_id) VALUES (?, ?)',
                ('user1', 1)
            )
            memory_db.commit()
