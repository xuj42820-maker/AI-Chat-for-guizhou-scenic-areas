"""
贵州旅游景点问答助手 - 主应用

职责：
1. 创建 Flask 应用实例
2. 注册 Blueprints
3. 初始化数据库和问答系统
"""

from flask import Flask, jsonify, request, send_from_directory
import os
import threading

from app.database import create_tables, import_attractions, import_images, import_guides, import_routes
from app.qa import RAGQuestionAnswer
from app.admin import admin_bp
from app.routes import pages_bp, attractions_bp, route_bp, favorites_bp, stats_bp


def create_app():
    """应用工厂函数"""
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))

    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        import secrets as _secrets
        secret_key = _secrets.token_hex(32)
        import warnings
        warnings.warn(
            "未设置 SECRET_KEY 环境变量，已生成随机密钥。重启后所有 session 将失效。\n"
            "请在生产环境中设置 SECRET_KEY 环境变量。",
            UserWarning,
            stacklevel=2
        )
    app.secret_key = secret_key
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # CORS 已移除：Flask 同源服务前端和 API，无需跨域支持。
    # 如需外部前端访问，应显式指定允许的来源：
    # CORS(app, origins=["http://localhost:3000"])

    # 注册 Blueprints
    app.register_blueprint(pages_bp)        # 页面路由
    app.register_blueprint(attractions_bp)  # 景点 API
    app.register_blueprint(route_bp)        # 路线 API
    app.register_blueprint(favorites_bp)    # 收藏 API
    app.register_blueprint(stats_bp)        # 统计 API
    app.register_blueprint(admin_bp)        # 管理后台

    # 问答接口（保留在 main 中，因为依赖全局 qa_system 实例）
    qa_system = None
    qa_system_lock = threading.Lock()

    def get_qa_system():
        nonlocal qa_system
        if qa_system is None:
            with qa_system_lock:
                # 双重检查锁定模式
                if qa_system is None:
                    qa_system = RAGQuestionAnswer()
        return qa_system

    @app.route('/api/chat', methods=['POST'])
    def chat():
        """问答接口"""
        data = request.get_json()
        if not data:
            return jsonify({'error': '请输入问题'}), 400
        message = data.get('message', '')
        if not message:
            return jsonify({'error': '请输入问题'}), 400
        qa = get_qa_system()
        return jsonify(qa.answer_question(message))

    # 静态数据文件服务
    @app.route('/data/<path:filename>')
    def serve_data(filename):
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        return send_from_directory(data_dir, filename)

    return app, get_qa_system


# 全局 app 实例（供 run.py 和外部使用）
app, _get_qa_system = create_app()


def init_app():
    """初始化应用（数据库 + 问答系统）"""
    print("正在初始化数据库...")
    create_tables()
    import_attractions()
    import_images()
    import_guides()
    import_routes()
    print("数据库初始化完成")

    print("正在加载问答系统...")
    _get_qa_system()
    print("问答系统加载完成")
