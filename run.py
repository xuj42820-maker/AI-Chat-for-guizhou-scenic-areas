"""
贵州旅游景点问答助手 - 启动脚本
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app, init_app


def main():
    """主函数"""
    print("=" * 60)
    print("贵州旅游景点问答助手")
    print("=" * 60)

    # 初始化应用
    init_app()

    print("\n" + "=" * 60)
    print("启动成功！")
    print("=" * 60)
    print("\n访问地址：")
    print("  主页: http://localhost:5000")
    print("  可视化: http://localhost:5000/visualization")
    print("  景点详情: http://localhost:5000/attraction/1")
    print("  地图: http://localhost:5000/map")
    print("  管理后台: http://localhost:5000/admin")
    print("\nAPI接口：")
    print("  问答: POST http://localhost:5000/api/chat")
    print("  景点列表: GET http://localhost:5000/api/attractions")
    print("  景点详情: GET http://localhost:5000/api/attractions/{id}")
    print("  路线推荐: GET http://localhost:5000/api/routes")
    print("  收藏: POST http://localhost:5000/api/favorites")
    print("\n" + "=" * 60)

    # 启动Flask应用
    app.run(debug=False, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
