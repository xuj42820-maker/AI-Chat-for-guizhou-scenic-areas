"""
从百度百科爬取景区真实照片
"""

import json
import os
import time
import random
import requests
import sqlite3
from lxml import etree


class BaikeImageCrawler:
    """百度百科图片爬虫"""

    def __init__(self):
        self.image_dir = os.path.join(os.path.dirname(__file__), 'static', 'images', 'attractions')
        os.makedirs(self.image_dir, exist_ok=True)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def search_baike_page(self, keyword):
        """搜索百度百科页面"""
        try:
            # 使用百度百科搜索API
            url = f'https://baike.baidu.com/search?word={keyword}'
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                html = etree.HTML(response.text)
                # 获取第一个搜索结果的链接
                links = html.xpath('//a[contains(@class, "result-title")]/@href')
                if links:
                    return links[0]
        except Exception as e:
            print(f'  搜索失败: {e}')

        return None

    def get_baike_images(self, page_url):
        """从百度百科页面获取图片"""
        images = []
        try:
            response = requests.get(page_url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                html = etree.HTML(response.text)

                # 获取图片
                img_elements = html.xpath('//img[contains(@class, "picture")]')
                for img in img_elements[:3]:
                    src = img.get('src') or img.get('data-src')
                    if src and src.startswith('http'):
                        images.append(src)

                # 如果没找到，尝试其他选择器
                if not images:
                    img_elements = html.xpath('//div[contains(@class, "summary-pic")]//img')
                    for img in img_elements[:3]:
                        src = img.get('src') or img.get('data-src')
                        if src and src.startswith('http'):
                            images.append(src)

        except Exception as e:
            print(f'  获取页面失败: {e}')

        return images

    def download_image(self, url, filename):
        """下载图片"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            if response.status_code == 200 and len(response.content) > 5000:
                filepath = os.path.join(self.image_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
        except Exception as e:
            print(f'  下载失败: {e}')
        return None

    def crawl_attraction_images(self, attr_id, name):
        """爬取单个景点的百科图片"""
        print(f'爬取: {name}')

        # 搜索百科页面
        page_url = self.search_baike_page(name)

        if not page_url:
            print(f'  未找到百科页面')
            return []

        # 获取图片URL
        images = self.get_baike_images(page_url)

        if not images:
            print(f'  未找到图片')
            return []

        # 下载图片
        downloaded = []
        for i, img_url in enumerate(images[:2]):
            filename = f'{attr_id}_baike_{i+1}.jpg'
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
        """爬取所有景点的百科图片"""
        # 读取景点数据
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'guizhou_attractions.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            attractions = json.load(f)

        print(f'开始爬取 {len(attractions)} 个景点的百科图片')
        print('=' * 50)

        # 连接数据库
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'guizhou_travel.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 获取已有图片
        cursor.execute('SELECT attraction_id, image_url FROM images WHERE image_url LIKE "%baike%"')
        existing = {row[0]: row[1] for row in cursor.fetchall()}

        success_count = 0
        for i, attr in enumerate(attractions):
            name = attr.get('name', '')
            attr_id = i + 1

            # 跳过已有百科图片的景点
            if attr_id in existing:
                print(f'跳过: {name} (已有百科图片)')
                success_count += 1
                continue

            # 爬取百科图片
            images = self.crawl_attraction_images(attr_id, name)

            if images:
                # 删除旧图片
                cursor.execute('DELETE FROM images WHERE attraction_id = ?', (attr_id,))

                # 插入新图片
                for img in images:
                    cursor.execute('''
                        INSERT INTO images (attraction_id, image_url, image_type, description, is_primary)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (attr_id, img['url'], 'baike', name + '百科图片', 1))

                success_count += 1
            else:
                # 保留原有图片
                pass

            # 每5个景点休息一下
            if (i + 1) % 5 == 0:
                print(f'\n已处理 {i+1}/{len(attractions)} 个景点\n')
                time.sleep(random.uniform(2, 4))

        conn.commit()
        conn.close()

        print('=' * 50)
        print(f'爬取完成！成功: {success_count}/{len(attractions)}')


if __name__ == '__main__':
    crawler = BaikeImageCrawler()

    print('贵州景点百科图片爬虫')
    print('=' * 50)

    # 爬取百科图片
    crawler.crawl_all()

    print('\n完成！')
