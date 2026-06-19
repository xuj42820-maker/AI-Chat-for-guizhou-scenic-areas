# -*- coding: utf-8 -*-
"""
修复黄果树瀑布图片
"""

import os
import requests
from urllib.parse import quote

# 图片保存目录
IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'attractions')

def search_image_url(keyword):
    """
    搜索图片URL - 使用百度图片搜索
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 使用百度图片搜索API
    search_url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&word={quote(keyword)}&pn=0&rn=10"

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                for item in data['data']:
                    if 'thumbURL' in item:
                        return item['thumbURL']
    except Exception as e:
        print(f"  搜索失败: {e}")

    return None

def download_image(url, save_path):
    """
    下载图片
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://image.baidu.com/'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"  下载失败: {e}")

    return False

def main():
    print("=" * 60)
    print("修复黄果树瀑布图片")
    print("=" * 60)

    # 搜索关键词
    keyword = "黄果树瀑布 安顺 贵州"
    print(f"搜索关键词: {keyword}")

    # 搜索图片
    image_url = search_image_url(keyword)
    if image_url:
        print(f"找到图片: {image_url[:60]}...")

        # 备份当前图片
        current_png = os.path.join(IMAGE_DIR, "1_1.png")
        if os.path.exists(current_png):
            backup_path = os.path.join(IMAGE_DIR, "1_1_old.png")
            os.rename(current_png, backup_path)
            print(f"备份原图片: {backup_path}")

        # 下载新图片
        save_path = os.path.join(IMAGE_DIR, "1_1.jpg")
        if download_image(image_url, save_path):
            file_size = os.path.getsize(save_path)
            print(f"下载成功: {save_path} ({file_size} bytes)")
        else:
            print("下载失败")
    else:
        print("未找到图片")

    print("=" * 60)

if __name__ == "__main__":
    main()
