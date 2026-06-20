"""
Vercel 入口文件
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app, init_app

# 初始化数据库和问答系统
init_app()
