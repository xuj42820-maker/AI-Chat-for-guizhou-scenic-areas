# -*- coding: utf-8 -*-
"""
下载缺失或错误的景点图片
"""

import os
import requests
import sys
from urllib.parse import quote

# 设置控制台编码
sys.stdout.reconfigure(encoding='utf-8')

# 图片保存目录
IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'attractions')

# 需要下载图片的景点信息
# 格式: {景点ID: (景点名称, 搜索关键词)}
MISSING_IMAGES = {
    50: ("梵净山温泉", "梵净山温泉"),
    86: ("黔南布依族织锦体验", "布依族织锦"),
}

WRONG_IMAGES = {
    7: ("织金洞", "织金洞 溶洞"),
    20: ("黄平旧州古镇", "黄平旧州古镇"),
    28: ("隆里古镇", "隆里古镇"),
    31: ("韭菜坪", "韭菜坪 贵州"),
    39: ("紫云格凸河穿洞", "格凸河 穿洞"),
    87: ("黔西南布依族八音坐唱", "布依族 八音坐唱"),
    93: ("毕节草海", "威宁草海"),
    95: ("铜仁梵净山佛教文化苑", "梵净山 佛教文化苑"),
    99: ("黔西南万峰湖", "万峰湖"),
}

def search_image_url(keyword):
    """
    搜索图片URL - 使用百度图片搜索
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 使用百度图片搜索API
    search_url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&word={quote(keyword)}&pn=0&rn=5"

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

def process_missing_images():
    """
    处理缺少图片的景点
    """
    print("=" * 60)
    print("处理缺少图片的景点")
    print("=" * 60)

    for attr_id, (name, keyword) in MISSING_IMAGES.items():
        print(f"\n景点 ID {attr_id}: {name}")
        print(f"  搜索关键词: {keyword}")

        # 检查是否已经存在 _1.jpg 或 _1.png
        jpg_path = os.path.join(IMAGE_DIR, f"{attr_id}_1.jpg")
        png_path = os.path.join(IMAGE_DIR, f"{attr_id}_1.png")

        if os.path.exists(jpg_path) or os.path.exists(png_path):
            print(f"  已存在图片，跳过")
            continue

        # 搜索图片
        image_url = search_image_url(keyword)
        if image_url:
            print(f"  找到图片: {image_url[:50]}...")
            # 下载图片
            save_path = jpg_path
            if download_image(image_url, save_path):
                file_size = os.path.getsize(save_path)
                print(f"  下载成功: {save_path} ({file_size} bytes)")
            else:
                print(f"  下载失败")
        else:
            print(f"  未找到图片")

def process_wrong_images():
    """
    处理图片不匹配的景点
    """
    print("\n" + "=" * 60)
    print("处理图片不匹配的景点")
    print("=" * 60)

    for attr_id, (name, keyword) in WRONG_IMAGES.items():
        print(f"\n景点 ID {attr_id}: {name}")
        print(f"  搜索关键词: {keyword}")

        # 检查当前图片
        current_jpg = os.path.join(IMAGE_DIR, f"{attr_id}_1.jpg")
        current_png = os.path.join(IMAGE_DIR, f"{attr_id}_1.png")

        # 备份当前图片
        if os.path.exists(current_jpg):
            backup_path = os.path.join(IMAGE_DIR, f"{attr_id}_1_old.jpg")
            os.rename(current_jpg, backup_path)
            print(f"  备份原图片: {backup_path}")
        elif os.path.exists(current_png):
            backup_path = os.path.join(IMAGE_DIR, f"{attr_id}_1_old.png")
            os.rename(current_png, backup_path)
            print(f"  备份原图片: {backup_path}")

        # 搜索图片
        image_url = search_image_url(keyword)
        if image_url:
            print(f"  找到图片: {image_url[:50]}...")
            # 下载图片
            save_path = current_jpg
            if download_image(image_url, save_path):
                file_size = os.path.getsize(save_path)
                print(f"  下载成功: {save_path} ({file_size} bytes)")
            else:
                print(f"  下载失败")
        else:
            print(f"  未找到图片")

def main():
    """
    主函数
    """
    print("贵州旅游景点图片下载工具")
    print("=" * 60)

    # 处理缺少图片的景点
    process_missing_images()

    # 处理图片不匹配的景点
    process_wrong_images()

    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
