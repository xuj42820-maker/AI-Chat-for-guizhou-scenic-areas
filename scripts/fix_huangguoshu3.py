# -*- coding: utf-8 -*-
"""
修复黄果树瀑布图片 - 使用更精确的关键词
"""

import os
import requests
from urllib.parse import quote

# 图片保存目录
IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'attractions')

def search_image_urls(keyword, count=10):
    """
    搜索多个图片URL
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    search_url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&word={quote(keyword)}&pn=0&rn={count}"

    urls = []
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                for item in data['data']:
                    if 'thumbURL' in item:
                        urls.append(item['thumbURL'])
    except Exception as e:
        print(f"  搜索失败: {e}")

    return urls

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
    print("修复黄果树瀑布图片 - 亚洲最大瀑布")
    print("=" * 60)

    # 更精确的搜索关键词
    keywords = [
        "黄果树大瀑布 亚洲最大",
        "黄果树瀑布 水帘洞",
        "黄果树瀑布 安顺 镇宁",
    ]

    all_urls = []
    for keyword in keywords:
        print(f"\n搜索关键词: {keyword}")
        urls = search_image_urls(keyword, 5)
        all_urls.extend(urls)
        print(f"  找到 {len(urls)} 张图片")

    print(f"\n总共找到 {len(all_urls)} 张候选图片")

    # 备份当前图片
    current_jpg = os.path.join(IMAGE_DIR, "1_1.jpg")
    if os.path.exists(current_jpg):
        backup_path = os.path.join(IMAGE_DIR, "1_1_current2.jpg")
        os.rename(current_jpg, backup_path)
        print(f"备份当前图片: {backup_path}")

    # 下载第一张图片
    if all_urls:
        print(f"\n下载第一张图片: {all_urls[0][:60]}...")
        save_path = os.path.join(IMAGE_DIR, "1_1.jpg")
        if download_image(all_urls[0], save_path):
            file_size = os.path.getsize(save_path)
            print(f"下载成功: {save_path} ({file_size} bytes)")
        else:
            print("下载失败")

    print("=" * 60)

if __name__ == "__main__":
    main()
