"""
爬取真实景区照片
使用百度图片搜索
"""

import json
import os
import time
import random
import requests
import sqlite3
from urllib.parse import quote


class RealImageCrawler:
    """真实照片爬虫"""

    def __init__(self):
        self.image_dir = os.path.join(os.path.dirname(__file__), 'static', 'images', 'attractions')
        os.makedirs(self.image_dir, exist_ok=True)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def search_baidu_images(self, keyword, count=2):
        """从百度图片搜索"""
        images = []
        try:
            # 使用百度图片搜索API
            encoded_keyword = quote(keyword)
            url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&word={encoded_keyword}&pn=0&rn={count}&ie=utf-8'

            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'data' in data:
                        for item in data['data']:
                            if isinstance(item, dict):
                                # 尝试不同的图片URL字段
                                img_url = item.get('thumbURL') or item.get('middleURL') or item.get('objURL')
                                if img_url:
                                    images.append(img_url)
                except Exception as e:
                    print(f'  解析失败: {e}')
        except Exception as e:
            print(f'  搜索失败: {e}')

        return images[:count]

    def search_sogou_images(self, keyword, count=2):
        """从搜狗图片搜索"""
        images = []
        try:
            encoded_keyword = quote(keyword)
            url = f'https://pic.sogou.com/pics?query={encoded_keyword}&mode=1&start=0&reqType=ajax&tn=0'

            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'items' in data:
                        for item in data['items'][:count]:
                            if 'picUrl' in item:
                                images.append(item['picUrl'])
                except:
                    pass
        except Exception as e:
            print(f'  搜狗搜索失败: {e}')

        return images[:count]

    def download_image(self, url, filename):
        """下载图片"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            if response.status_code == 200 and len(response.content) > 1000:
                filepath = os.path.join(self.image_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
        except Exception as e:
            print(f'  下载失败: {e}')
        return None

    def crawl_attraction_images(self, attr_id, name):
        """爬取单个景点的真实照片"""
        print(f'爬取: {name}')

        # 搜索关键词
        search_keyword = f'{name} 贵州 旅游 风景'

        # 尝试百度图片
        images = self.search_baidu_images(search_keyword, count=2)

        # 如果百度没找到，尝试搜狗
        if not images:
            print(f'  百度未找到，尝试搜狗...')
            images = self.search_sogou_images(search_keyword, count=2)

        if not images:
            print(f'  未找到真实照片')
            return []

        # 下载图片
        downloaded = []
        for i, img_url in enumerate(images):
            filename = f'{attr_id}_real_{i+1}.jpg'
            filepath = self.download_image(img_url, filename)

            if filepath:
                downloaded.append({
                    'filename': filename,
                    'url': f'/static/images/attractions/{filename}'
                })
                print(f'  下载成功: {filename}')
            else:
                print(f'  下载失败')

            time.sleep(random.uniform(0.5, 1.5))

        return downloaded

    def crawl_all(self):
        """爬取所有景点的真实照片"""
        # 读取景点数据
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'guizhou_attractions.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            attractions = json.load(f)

        print(f'开始爬取 {len(attractions)} 个景点的真实照片')
        print('=' * 50)

        # 连接数据库
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'guizhou_travel.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 获取已有图片
        cursor.execute('SELECT attraction_id, image_url FROM images WHERE image_url LIKE "%real%"')
        existing = {row[0]: row[1] for row in cursor.fetchall()}

        success_count = 0
        for i, attr in enumerate(attractions):
            name = attr.get('name', '')
            attr_id = i + 1

            # 跳过已有真实照片的景点
            if attr_id in existing:
                print(f'跳过: {name} (已有真实照片)')
                success_count += 1
                continue

            # 爬取真实照片
            images = self.crawl_attraction_images(attr_id, name)

            if images:
                # 删除旧图片
                cursor.execute('DELETE FROM images WHERE attraction_id = ?', (attr_id,))

                # 插入新图片
                for img in images:
                    cursor.execute('''
                        INSERT INTO images (attraction_id, image_url, image_type, description, is_primary)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (attr_id, img['url'], 'real', name + '真实照片', 1))

                success_count += 1
            else:
                # 保留原有图片
                pass

            # 每10个景点休息一下
            if (i + 1) % 10 == 0:
                print(f'\n已处理 {i+1}/{len(attractions)} 个景点\n')
                time.sleep(random.uniform(2, 4))

        conn.commit()
        conn.close()

        print('=' * 50)
        print(f'爬取完成！成功: {success_count}/{len(attractions)}')


if __name__ == '__main__':
    crawler = RealImageCrawler()

    print('贵州景点真实照片爬虫')
    print('=' * 50)

    # 爬取真实照片
    crawler.crawl_all()

    print('\n完成！')
