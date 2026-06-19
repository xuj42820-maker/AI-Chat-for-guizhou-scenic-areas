"""
贵州景点图片爬虫 v2
使用多个图片来源
"""

import json
import os
import sqlite3
import requests
import time
import random
from urllib.parse import quote


class ImageCrawlerV2:
    """图片爬虫 v2"""

    def __init__(self):
        self.image_dir = os.path.join(os.path.dirname(__file__), 'static', 'images', 'attractions')
        os.makedirs(self.image_dir, exist_ok=True)

        # 景点图片映射（使用免费图片服务）
        self.image_sources = {
            # 使用Unsplash的免费图片，按景点类型分类
            '瀑布': [
                'https://images.unsplash.com/photo-1432405972618-c6b0cfba8b28?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop',
            ],
            '古镇': [
                'https://images.unsplash.com/photo-1528164344705-47542687000d?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=400&h=300&fit=crop',
            ],
            '苗寨': [
                'https://images.unsplash.com/photo-1528164344705-47542687000d?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=400&h=300&fit=crop',
            ],
            '山': [
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop',
            ],
            '溶洞': [
                'https://images.unsplash.com/photo-1520262494112-9fe481d36ec3?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=300&fit=crop',
            ],
            '河': [
                'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400&h=300&fit=crop',
            ],
            '湖': [
                'https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=400&h=300&fit=crop',
            ],
            '峡谷': [
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=300&fit=crop',
            ],
            '草原': [
                'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400&h=300&fit=crop',
            ],
            '温泉': [
                'https://images.unsplash.com/photo-1545579133-99bb5ab189bd?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1515362656316-cd1009e07c24?w=400&h=300&fit=crop',
            ],
            '寺': [
                'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1528164344705-47542687000d?w=400&h=300&fit=crop',
            ],
            '楼': [
                'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1528164344705-47542687000d?w=400&h=300&fit=crop',
            ],
            '公园': [
                'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400&h=300&fit=crop',
            ],
            '梯田': [
                'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400&h=300&fit=crop',
            ],
            '花': [
                'https://images.unsplash.com/photo-1490750967868-88aa4f44baee?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1490750967868-88aa4f44baee?w=400&h=300&fit=crop',
            ],
            '美食': [
                'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop',
            ],
            '博物馆': [
                'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1528164344705-47542687000d?w=400&h=300&fit=crop',
            ],
            '红色': [
                'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1528164344705-47542687000d?w=400&h=300&fit=crop',
            ],
            ' default': [
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop',
            ]
        }

    def get_image_urls(self, name, features):
        """根据景点名称和特征获取图片URL"""
        # 首先尝试精确匹配
        for keyword, urls in self.image_sources.items():
            if keyword in name or keyword in str(features):
                return urls

        # 默认图片
        return self.image_sources[' default']

    def download_image(self, url, filename):
        """下载图片"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                filepath = os.path.join(self.image_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
        except Exception as e:
            print(f'  下载失败: {e}')
        return None

    def process_all(self):
        """处理所有景点"""
        # 读取景点数据
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'guizhou_attractions.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            attractions = json.load(f)

        print(f'开始处理 {len(attractions)} 个景点的图片')
        print('=' * 50)

        # 连接数据库
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'guizhou_travel.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 清空旧图片
        cursor.execute('DELETE FROM images')

        success_count = 0
        for i, attr in enumerate(attractions):
            name = attr.get('name', '')
            features = attr.get('features', '')
            attr_id = i + 1

            print(f'处理: {name}')

            # 获取图片URL
            image_urls = self.get_image_urls(name, features)

            # 下载图片
            downloaded = []
            for j, url in enumerate(image_urls[:2]):  # 每个景点最多2张图片
                filename = f'{attr_id}_{j+1}.jpg'
                filepath = self.download_image(url, filename)

                if filepath:
                    downloaded.append({
                        'filename': filename,
                        'url': f'/static/images/attractions/{filename}'
                    })
                    print(f'  下载成功: {filename}')
                else:
                    # 使用占位图
                    emoji = self.get_emoji(name)
                    placeholder_url = f"https://placehold.co/400x300/1c2333/4a9e8e?text={emoji}+{name[:6]}"
                    downloaded.append({
                        'filename': None,
                        'url': placeholder_url
                    })
                    print(f'  使用占位图')

                time.sleep(random.uniform(0.2, 0.5))

            # 保存到数据库
            for img in downloaded:
                cursor.execute('''
                    INSERT INTO images (attraction_id, image_url, image_type, description, is_primary)
                    VALUES (?, ?, ?, ?, ?)
                ''', (attr_id, img['url'], 'main', name + '图片', 1))

            success_count += 1

            # 每20个景点休息一下
            if (i + 1) % 20 == 0:
                print(f'\n已处理 {i+1}/{len(attractions)} 个景点\n')
                time.sleep(random.uniform(1, 2))

        conn.commit()
        conn.close()

        print('=' * 50)
        print(f'处理完成！共处理 {success_count}/{len(attractions)} 个景点')

    def get_emoji(self, name):
        """根据景点名称获取emoji"""
        emoji_map = {
            '瀑布': '💧', '古镇': '🏘️', '苗寨': '🏘️', '侗寨': '🏘️',
            '溶洞': '🕳️', '山': '⛰️', '峰': '⛰️', '河': '🏞️',
            '湖': '🏞️', '峡谷': '🏞️', '草原': '🌿', '森林': '🌲',
            '温泉': '♨️', '寺': '🛕', '庙': '🛕', '楼': '🏛️',
            '桥': '🌉', '公园': '🌳', '梯田': '🌾', '花': '🌸',
        }

        for key, emoji in emoji_map.items():
            if key in name:
                return emoji
        return '🏔️'


if __name__ == '__main__':
    crawler = ImageCrawlerV2()

    print('贵州景点图片爬虫 v2')
    print('=' * 50)

    # 处理图片
    crawler.process_all()

    print('\n完成！')
