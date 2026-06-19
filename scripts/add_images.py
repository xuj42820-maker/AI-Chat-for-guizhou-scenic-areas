"""
添加景区图片
"""

import sqlite3
import os


def add_attraction_images():
    """为景点添加图片"""
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'guizhou_travel.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 清空旧图片
    cursor.execute('DELETE FROM images')

    # 获取所有景点
    cursor.execute('SELECT id, name, category, features FROM attractions')
    attractions = cursor.fetchall()

    # 根据景点类型选择emoji图标
    emoji_map = {
        '瀑布': '💧',
        '古镇': '🏘️',
        '苗寨': '🏘️',
        '侗寨': '🏘️',
        '溶洞': '🕳️',
        '山': '⛰️',
        '峰': '⛰️',
        '河': '🏞️',
        '湖': '🏞️',
        '峡谷': '🏞️',
        '草原': '🌿',
        '森林': '🌲',
        '温泉': '♨️',
        '寺': '🛕',
        '庙': '🛕',
        '楼': '🏛️',
        '塔': '🏛️',
        '桥': '🌉',
        '公园': '🌳',
        '湿地': '🌿',
        '梯田': '🌾',
        '花': '🌸',
        '银杏': '🍂',
        '杜鹃': '🌺',
        '樱花': '🌸',
        '美食': '🍜',
        '小吃': '🍜',
        '酒': '🍺',
        '茶': '🍵',
        '博物馆': '🏛️',
        '纪念馆': '🏛️',
        '红色': '🏳️',
        '革命': '🏳️',
        '红军': '🏳️',
        '屯堡': '🏘️',
        '古城': '🏰',
        '城堡': '🏰',
        '大草原': '🌿',
        '滑雪': '⛷️',
        '漂流': '🚣',
        '攀岩': '🧗',
        '徒步': '🥾',
        '摄影': '📸',
        '观鸟': '🐦',
        '天文': '🔭',
        '科技': '🔬',
        '射电望远镜': '🔭',
    }

    # 为每个景点添加图片
    for attr_id, name, category, features in attractions:
        # 根据名称和特征选择emoji
        emoji = '🏔️'  # 默认

        for key, icon in emoji_map.items():
            if key in name or key in str(features) or key in str(category):
                emoji = icon
                break

        # 生成图片URL（使用免费的图片服务）
        # 使用Unsplash的免费图片API
        search_term = name.replace('贵州', '').replace('公园', '').replace('古镇', '')[:4]

        # 使用placeholder.com生成带文字的图片
        image_url = f"https://placehold.co/400x300/1c2333/4a9e8e?text={emoji}+{name[:6]}"

        cursor.execute('''
            INSERT INTO images (attraction_id, image_url, image_type, description, is_primary)
            VALUES (?, ?, ?, ?, ?)
        ''', (attr_id, image_url, 'main', name + '图片', 1))

    conn.commit()
    conn.close()

    print("已为 " + str(len(attractions)) + " 个景点添加图片")


def update_attraction_images():
    """更新景点详情页的图片显示"""
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'attraction_detail.html')

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 更新图片显示逻辑
    old_code = '''// 加载景点详情
        fetch(`/api/attractions/${attractionId}`)
            .then(response => response.json())
            .then(data => {
                attractionData = data;
                renderAttraction(data);
                checkFavorite();
            })
            .catch(error => {
                console.error('加载失败:', error);
            });'''

    new_code = '''// 加载景点详情
        fetch(`/api/attractions/${attractionId}`)
            .then(response => response.json())
            .then(data => {
                attractionData = data;
                renderAttraction(data);
                checkFavorite();

                // 加载图片
                if (data.images && data.images.length > 0) {
                    const img = data.images[0];
                    document.getElementById('attractionImage').innerHTML =
                        `<img src="${img.image_url}" alt="${data.name}" style="width:100%;height:100%;object-fit:cover;border-radius:16px;">`;
                }
            })
            .catch(error => {
                console.error('加载失败:', error);
            });'''

    content = content.replace(old_code, new_code)

    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("已更新景点详情页图片显示")


if __name__ == '__main__':
    add_attraction_images()
    update_attraction_images()
    print("\n图片添加完成！")
