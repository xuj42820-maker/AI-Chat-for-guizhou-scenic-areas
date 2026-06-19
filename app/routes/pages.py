"""
页面路由 — 渲染 HTML 模板
"""
from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    """主页"""
    return render_template('index.html')


@pages_bp.route('/attractions')
def attractions():
    """景点大全页面"""
    return render_template('attractions.html')


@pages_bp.route('/routes')
def routes():
    """路线推荐页面"""
    return render_template('routes.html')


@pages_bp.route('/visualization')
def visualization():
    """可视化页面"""
    return render_template('visualization.html')


@pages_bp.route('/attraction/<int:attraction_id>')
def attraction_detail(attraction_id):
    """景点详情页"""
    return render_template('attraction_detail.html', attraction_id=attraction_id)


@pages_bp.route('/map')
def map_view():
    """地图页面"""
    return render_template('map.html')
