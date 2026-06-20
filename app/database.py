"""
数据库模型 - 景点表、图片表、攻略表
"""

import json
import os
import re
import logging

from app.db import DatabaseContext, DB_PATH

logger = logging.getLogger(__name__)


def create_tables():
    """创建数据库表"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with DatabaseContext() as conn:
        cursor = conn.cursor()

        # 景点表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                address TEXT,
                category TEXT,
                ticket_price TEXT,
                opening_hours TEXT,
                description TEXT,
                features TEXT,
                rating REAL,
                best_season TEXT,
                transportation TEXT,
                tips TEXT,
                phone TEXT,
                official_website TEXT,
                area TEXT,
                suggested_duration TEXT,
                ticket_booking TEXT,
                discount_policy TEXT,
                weather_tips TEXT,
                clothing_tips TEXT,
                must_bring TEXT,
                nearby_attractions TEXT,
                nearby_hotels TEXT,
                nearby_restaurants TEXT,
                history_culture TEXT,
                best_photo_spots TEXT,
                night_activities TEXT,
                family_friendly TEXT,
                team_activities TEXT,
                latitude REAL,
                longitude REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 图片表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attraction_id INTEGER,
                image_url TEXT,
                image_type TEXT,
                description TEXT,
                is_primary INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (attraction_id) REFERENCES attractions(id)
            )
        ''')

        # 攻略表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attraction_id INTEGER,
                title TEXT,
                content TEXT,
                guide_type TEXT,
                season TEXT,
                duration TEXT,
                budget TEXT,
                tips TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (attraction_id) REFERENCES attractions(id)
            )
        ''')

        # 路线表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                duration TEXT,
                difficulty TEXT,
                season TEXT,
                budget TEXT,
                attractions_list TEXT,
                route_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 收藏表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                attraction_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (attraction_id) REFERENCES attractions(id),
                UNIQUE(user_id, attraction_id)
            )
        ''')

    print("数据库表创建完成")


def import_attractions():
    """导入景点数据（仅在表为空时导入，避免覆盖管理后台的编辑）"""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'guizhou_attractions.json')

    with DatabaseContext() as conn:
        cursor = conn.cursor()

        # 检查是否已有数据，有则跳过导入
        cursor.execute('SELECT COUNT(*) FROM attractions')
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"景点表已有 {count} 条数据，跳过导入")
            # 清理孤立的收藏记录（引用了不存在的景点）
            cursor.execute('''DELETE FROM favorites WHERE attraction_id NOT IN
                (SELECT id FROM attractions)''')
            return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with DatabaseContext() as conn:
        cursor = conn.cursor()

        # 导入数据

        # 导入数据
        for attr in data:
            cursor.execute('''
                INSERT INTO attractions (
                    name, address, category, ticket_price, opening_hours,
                    description, features, rating, best_season, transportation,
                    tips, phone, official_website, area, suggested_duration,
                    ticket_booking, discount_policy, weather_tips, clothing_tips,
                    must_bring, nearby_attractions, nearby_hotels, nearby_restaurants,
                    history_culture, best_photo_spots, night_activities,
                    family_friendly, team_activities, latitude, longitude
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                attr.get('name'),
                attr.get('address'),
                attr.get('category'),
                attr.get('ticket_price'),
                attr.get('opening_hours'),
                attr.get('description'),
                attr.get('features'),
                attr.get('rating'),
                attr.get('best_season'),
                attr.get('transportation'),
                attr.get('tips'),
                attr.get('phone'),
                attr.get('official_website'),
                attr.get('area'),
                attr.get('suggested_duration'),
                attr.get('ticket_booking'),
                attr.get('discount_policy'),
                attr.get('weather_tips'),
                attr.get('clothing_tips'),
                attr.get('must_bring'),
                attr.get('nearby_attractions'),
                attr.get('nearby_hotels'),
                attr.get('nearby_restaurants'),
                attr.get('history_culture'),
                attr.get('best_photo_spots'),
                attr.get('night_activities'),
                attr.get('family_friendly'),
                attr.get('team_activities'),
                attr.get('latitude'),
                attr.get('longitude')
            ))

    print("导入 " + str(len(data)) + " 个景点数据")


def import_images():
    """导入图片数据 - 优先使用本地真实图片，无本地图片时回退到占位图"""
    import glob as glob_mod

    images_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'attractions')

    with DatabaseContext() as conn:
        cursor = conn.cursor()

        # 检查是否已有数据，有则跳过
        cursor.execute('SELECT COUNT(*) FROM images')
        if cursor.fetchone()[0] > 0:
            print("图片表已有数据，跳过导入")
            return

        # 清空旧数据
        cursor.execute('DELETE FROM images')

        # 扫描本地图片，按景点ID分组: {attraction_id: [file1, file2, ...]}
        local_images = {}
        if os.path.isdir(images_dir):
            for filepath in glob_mod.glob(os.path.join(images_dir, '*.jpg')):
                filename = os.path.basename(filepath)
                # 文件名格式: {attraction_id}_{n}.jpg 或 {attraction_id}_real_{n}.jpg
                match = re.match(r'^(\d+)_', filename)
                if match:
                    aid = int(match.group(1))
                    local_images.setdefault(aid, []).append('/static/images/attractions/' + filename)

        # 获取所有景点
        cursor.execute('SELECT id, name, category FROM attractions')
        attractions = cursor.fetchall()

        imported_count = 0
        for attr_id, name, category in attractions:
            if attr_id in local_images:
                # 使用本地真实图片
                for i, img_url in enumerate(sorted(local_images[attr_id])):
                    cursor.execute('''
                        INSERT INTO images (attraction_id, image_url, image_type, description, is_primary)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (attr_id, img_url, 'main', name + '图片' + str(i + 1), 1 if i == 0 else 0))
                    imported_count += 1
            else:
                # 无本地图片，使用占位图
                image_url = 'https://picsum.photos/400/300?random=' + str(attr_id)
                cursor.execute('''
                    INSERT INTO images (attraction_id, image_url, image_type, description, is_primary)
                    VALUES (?, ?, ?, ?, ?)
                ''', (attr_id, image_url, 'main', name + '主图', 1))

    print(f"导入图片数据完成：{imported_count} 张本地图片，{len(attractions) - len(local_images)} 个占位图")


def import_guides():
    """导入攻略数据"""
    with DatabaseContext() as conn:
        cursor = conn.cursor()

        # 检查是否已有数据，有则跳过
        cursor.execute('SELECT COUNT(*) FROM guides')
        if cursor.fetchone()[0] > 0:
            print("攻略表已有数据，跳过导入")
            return

        # 清空旧数据
        cursor.execute('DELETE FROM guides')

        # 获取所有景点
        cursor.execute('SELECT id, name, description, tips, best_season, suggested_duration, ticket_price FROM attractions')
        attractions = cursor.fetchall()

        for attr_id, name, desc, tips, season, duration, price in attractions:
            # 生成攻略内容
            guide_content = f"""## {name}游玩攻略

### 景点介绍
{desc}

### 最佳游玩时间
{season if season else '全年皆宜'}

### 建议游玩时长
{duration if duration else '半天'}

### 门票信息
{price if price else '免费'}

### 游玩建议
{tips if tips else '请提前查看天气预报，做好出行准备'}

### 交通指南
可乘坐公共交通或自驾前往，建议提前查询路线。

### 注意事项
1. 请遵守景区规定，文明旅游
2. 注意安全，听从工作人员指挥
3. 保护环境，不乱扔垃圾
4. 尊重当地民族习俗
"""

            cursor.execute('''
                INSERT INTO guides (attraction_id, title, content, guide_type, season, duration, budget)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (attr_id, name + '游玩攻略', guide_content, 'basic', season, duration, price))

    print("导入攻略数据完成")


def import_routes():
    """导入路线数据（从 routes.json 加载）"""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'routes.json')

    with DatabaseContext() as conn:
        cursor = conn.cursor()

        # 检查是否已有数据，有则跳过
        cursor.execute('SELECT COUNT(*) FROM routes')
        if cursor.fetchone()[0] > 0:
            print("路线表已有数据，跳过导入")
            return

    with open(json_path, 'r', encoding='utf-8') as f:
        routes = json.load(f)

    with DatabaseContext() as conn:
        cursor = conn.cursor()

        # 导入数据

        for route in routes:
            cursor.execute('''
                INSERT INTO routes (name, description, duration, difficulty, season, budget, attractions_list, route_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                route.get('name', ''),
                route.get('description', ''),
                route.get('duration', ''),
                route.get('difficulty', ''),
                route.get('season', ''),
                route.get('budget', ''),
                route.get('attractions_list', ''),
                route.get('route_type', '')
            ))

    print("导入 " + str(len(routes)) + " 条路线数据")


if __name__ == '__main__':
    create_tables()
    import_attractions()
    import_images()
    import_guides()
    import_routes()
    print("\n数据库初始化完成！")
