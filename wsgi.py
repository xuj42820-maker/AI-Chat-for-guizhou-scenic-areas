"""
WSGI 入口文件 — 供 gunicorn / 生产环境使用

用法: gunicorn wsgi:app
"""
import sys
import os

# 确保项目根目录在路径中
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app, init_app

# 启动时初始化数据库和问答系统
init_app()

if __name__ == '__main__':
    app.run()
