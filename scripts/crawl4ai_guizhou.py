"""
贵州旅游景点爬虫 — 基于 crawl4ai

功能：
1. 爬取景点信息（名称、门票、开放时间等）
2. 爬取景点图片并下载到本地
3. 保存到数据库和 JSON
"""

import asyncio
import json
import os
import re
import sqlite3
import aiohttp
from urllib.parse import urljoin, urlparse
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, CacheMode


# 目标网站（景点详情页，更容易拿到图片）
TARGET_URLS = [
    "https://you.ctrip.com/sight/guizhou122/s0-p1.html",
    "https://you.ctrip.com/sight/guiyang21/s0-p1.html",
    "https://you.ctrip.com/sight/anshun152/s0-p1.html",
]

# 图片保存目录
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'attractions')


def get_db_path():
    return os.path.join(os.path.dirname(__file__), '..', 'data', 'guizhou_travel.db')


def ensure_db():
    """确保数据库和表存在"""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 景点表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
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
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 图片表（一个景点可以有多张图）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attraction_id INTEGER,
            image_url TEXT,
            local_path TEXT,
            is_primary INTEGER DEFAULT 0,
            FOREIGN KEY (attraction_id) REFERENCES attractions(id)
        )
    ''')

    conn.commit()
    conn.close()
    return db_path


def extract_images_from_html(html_text, page_url):
    """从 HTML 中提取图片 URL"""
    images = []
    # 匹配 <img> 标签中的 src
    img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
    for match in img_pattern.finditer(html_text):
        src = match.group(1)
        # 跳过小图标、logo、base64 图片
        if 'base64' in src or 'logo' in src.lower() or 'icon' in src.lower():
            continue
        if src.endswith(('.jpg', '.jpeg', '.png', '.webp')) or 'photo' in src.lower() or 'image' in src.lower():
            full_url = urljoin(page_url, src)
            images.append(full_url)

    # 也匹配 CSS 背景图
    bg_pattern = re.compile(r'url\(["\']?([^"\')]+)["\']?\)', re.IGNORECASE)
    for match in bg_pattern.finditer(html_text):
        src = match.group(1)
        if src.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            full_url = urljoin(page_url, src)
            images.append(full_url)

    return list(set(images))  # 去重


def extract_attractions_from_html(html_text, page_url):
    """从 HTML 中解析景点信息"""
    attractions = []

    # 携程景点列表页的模式
    # 景点名称通常在 <a> 标签中
    name_pattern = re.compile(r'<a[^>]*href="/sight/[^"]*"[^>]*>([^<]{2,20})</a>')
    names = list(set(name_pattern.findall(html_text)))

    # 贵州景点关键词过滤
    guizhou_keywords = [
        '黄果树', '梵净山', '荔波', '西江', '苗寨', '镇远', '遵义', '青岩',
        '织金洞', '马岭河', '万峰林', '赤水', '百里杜鹃', '草海', '肇兴',
        '天眼', '黔灵', '花溪', '天河潭', '海龙屯', '加榜', '下司',
        '朗德', '岜沙', '隆里', '旧州', '飞云崖', '韭菜坪',
    ]

    for name in names:
        name = name.strip()
        if not name or len(name) < 2:
            continue
        # 只保留包含贵州景点关键词的
        if any(kw in name for kw in guizhou_keywords):
            attractions.append({
                'name': name,
                'source_url': page_url,
            })

    # 尝试提取门票信息
    ticket_pattern = re.compile(r'([一-龥]{2,10})[^。，]*?(\d+元|免费)')
    for match in ticket_pattern.finditer(html_text):
        spot_name = match.group(1)
        ticket = match.group(2)
        for attr in attractions:
            if attr['name'] in spot_name or spot_name in attr['name']:
                attr['ticket_price'] = ticket

    return attractions


def extract_markdown_images(md_text, page_url):
    """从 Markdown 文本中提取图片"""
    images = []
    # Markdown 图片语法: ![alt](url)
    md_img_pattern = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
    for match in md_img_pattern.finditer(md_text):
        src = match.group(1)
        if not src.startswith('data:'):
            full_url = urljoin(page_url, src)
            images.append(full_url)
    return list(set(images))


async def download_image(session, url, save_path):
    """下载单张图片"""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status == 200:
                content_type = resp.headers.get('Content-Type', '')
                if 'image' in content_type:
                    data = await resp.read()
                    if len(data) > 1024:  # 跳过太小的图（可能是占位符）
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        with open(save_path, 'wb') as f:
                            f.write(data)
                        return True
    except Exception as e:
        pass
    return False


async def crawl_and_extract(crawler, url, config):
    """爬取页面并提取信息"""
    print(f"  正在爬取: {url}")
    try:
        result = await crawler.arun(url=url, config=config)
        if result.success:
            html = result.html or ''
            md = result.markdown_v2.raw_markdown if result.markdown_v2 else ''

            # 提取景点
            attractions = extract_attractions_from_html(html, url)

            # 提取图片（HTML + Markdown 两种方式）
            images = extract_images_from_html(html, url)
            images.extend(extract_markdown_images(md, url))
            images = list(set(images))

            print(f"  ✓ {url} → {len(attractions)} 个景点, {len(images)} 张图片")
            return attractions, images
        else:
            print(f"  ✗ 失败: {url} - {result.error_message}")
            return [], []
    except Exception as e:
        print(f"  ✗ 异常: {url} - {e}")
        return [], []


def save_attractions_to_db(attractions):
    """保存景点到数据库"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    saved = 0
    for attr in attractions:
        name = attr.get('name', '')
        if not name:
            continue
        # 检查是否已存在
        cursor.execute('SELECT id FROM attractions WHERE name = ?', (name,))
        if cursor.fetchone():
            continue

        cursor.execute('''
            INSERT INTO attractions (name, address, category, ticket_price, opening_hours,
                                     description, rating, features, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            attr.get('address', ''),
            attr.get('category', '自然风光'),
            attr.get('ticket_price', ''),
            attr.get('opening_hours', ''),
            attr.get('description', ''),
            attr.get('rating'),
            attr.get('features', ''),
            attr.get('image_url', ''),
        ))
        saved += 1

    conn.commit()
    conn.close()
    return saved


def save_images_to_db(attraction_name, image_urls, local_paths):
    """保存图片记录到数据库"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 找到景点 ID
    cursor.execute('SELECT id FROM attractions WHERE name = ?', (attraction_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return 0

    attraction_id = row[0]
    saved = 0
    for i, (url, local) in enumerate(zip(image_urls, local_paths)):
        cursor.execute('''
            INSERT INTO images (attraction_id, image_url, local_path, is_primary)
            VALUES (?, ?, ?, ?)
        ''', (attraction_id, url, local, 1 if i == 0 else 0))
        saved += 1

    # 更新景点的主图
    if local_paths:
        cursor.execute('UPDATE attractions SET image_url = ? WHERE id = ?',
                       (local_paths[0], attraction_id))

    conn.commit()
    conn.close()
    return saved


def url_to_filename(url, attraction_name, index):
    """将图片 URL 转换为本地文件名"""
    ext = '.jpg'
    lower = url.lower()
    if '.png' in lower:
        ext = '.png'
    elif '.webp' in lower:
        ext = '.webp'
    safe_name = re.sub(r'[^\w一-龥]', '_', attraction_name)
    return f"{safe_name}_{index}{ext}"


async def main():
    """主函数"""
    print("=" * 60)
    print("贵州旅游景点爬虫 (crawl4ai) - 含图片爬取")
    print("=" * 60)

    # 1. 确保数据库存在
    db_path = ensure_db()
    os.makedirs(IMAGES_DIR, exist_ok=True)
    print(f"数据库: {db_path}")
    print(f"图片目录: {IMAGES_DIR}")

    # 2. 配置浏览器
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        cache_mode=CacheMode.BYPASS,
    )

    all_attractions = []
    all_images = {}  # {page_url: [image_urls]}

    # 3. 爬取各个网站
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in TARGET_URLS:
            attractions, images = await crawl_and_extract(crawler, url, run_config)
            all_attractions.extend(attractions)
            if images:
                all_images[url] = images

    # 4. 去重景点
    seen = set()
    unique = []
    for attr in all_attractions:
        name = attr.get('name', '')
        if name and name not in seen:
            seen.add(name)
            unique.append(attr)
    print(f"\n共爬取到 {len(unique)} 个唯一景点")

    # 5. 保存景点到数据库
    if unique:
        saved = save_attractions_to_db(unique)
        print(f"新增 {saved} 个景点")

    # 6. 下载图片
    total_images = 0
    async with aiohttp.ClientSession() as session:
        for page_url, image_urls in all_images.items():
            for img_url in image_urls[:5]:  # 每个页面最多下载5张
                # 尝试匹配到景点名
                attr_name = "未知景点"
                for attr in unique:
                    if attr['name'] in img_url or any(kw in img_url for kw in attr['name'][:2]):
                        attr_name = attr['name']
                        break

                filename = url_to_filename(img_url, attr_name, total_images + 1)
                save_path = os.path.join(IMAGES_DIR, filename)

                ok = await download_image(session, img_url, save_path)
                if ok:
                    # 保存到数据库
                    rel_path = f"static/images/attractions/{filename}"
                    save_images_to_db(attr_name, [img_url], [rel_path])
                    total_images += 1
                    print(f"  ✓ 下载: {filename}")

    # 7. 保存原始数据到 JSON
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'crawled_data.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'attractions': unique,
            'images': {k: v[:5] for k, v in all_images.items()},
        }, f, ensure_ascii=False, indent=2)

    # 8. 统计
    print("\n" + "=" * 60)
    print(f"爬取完成！")
    print(f"  景点: {len(unique)} 个")
    print(f"  图片: {total_images} 张")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
