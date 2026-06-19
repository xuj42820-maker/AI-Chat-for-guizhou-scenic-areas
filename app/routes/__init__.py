"""
路由模块 — 按功能拆分的 Flask Blueprints
"""
from app.routes.pages import pages_bp
from app.routes.attractions import attractions_bp
from app.routes.route_api import route_bp
from app.routes.favorites import favorites_bp
from app.routes.stats import stats_bp

__all__ = ['pages_bp', 'attractions_bp', 'route_bp', 'favorites_bp', 'stats_bp']
