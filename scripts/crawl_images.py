"""
贵州景点图片爬虫 — Wikimedia Commons（限速友好版）

策略：每次只处理几个景点，避免被限速。
可多次运行，自动跳过已有图片的景点。

用法: python scripts/crawl_images.py [--force] [--limit N]
  --force: 强制替换已有图片
  --limit N: 最多处理 N 个（默认 20）
"""

import os
import re
import sqlite3
import sys
import time
import requests


IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'attractions')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'guizhou_travel.db')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://commons.wikimedia.org/',
}

SEARCH_KEYWORDS = {
    '黄果树瀑布': 'Huangguoshu Waterfall',
    '梵净山': 'Fanjingshan mountain',
    '荔波小七孔': 'Libo small arch',
    '西江千户苗寨': 'Xijiang Miao village',
    '镇远古镇': 'Zhenyuan town Guizhou',
    '遵义会议会址': 'Zunyi Conference',
    '青岩古镇': 'Qingyan ancient town',
    '织金洞': 'Zhijin cave',
    '马岭河峡谷': 'Malinghe canyon',
    '万峰林': 'Wanfenglin peaks',
    '赤水大瀑布': 'Chishui waterfall',
    '百里杜鹃': 'Baili azalea',
    '威宁草海': 'Caohai lake',
    '肇兴侗寨': 'Zhaoxing Dong village',
    '平塘天眼': 'FAST telescope',
    '黔灵山公园': 'Qianlingshan park',
    '花溪湿地公园': 'Huaxi wetland',
    '天河潭': 'Tianhetan Guizhou',
    '南江大峡谷': 'Nanjing canyon Guizhou',
    '海龙屯': 'Hailongtun fortress',
    '加榜梯田': 'Jiabang rice terrace',
    '下司古镇': 'Xiasi ancient town',
    '朗德苗寨': 'Langde Miao village',
    '岜沙苗寨': 'Basha Miao village',
    '隆里古城': 'Longli ancient city',
    '甲秀楼': 'Jiaxiu Tower',
    '龙宫': 'Dragon Palace cave Guizhou',
    '茅台镇': 'Maotai town',
    '韭菜坪': 'Jiucaping',
    '平坝樱花': 'Pingba cherry blossom',
    '荔波大七孔': 'Libo big arch',
    '镇远舞阳河': 'Wuyang River',
    '赤水丹霞': 'Chishui Danxia',
    '燕子岩国家森林公园': 'Yanziyan forest',
    '石阡温泉': 'Shiqian hot spring',
    '妥乐古银杏村': 'Tuole ginkgo village',
    '万峰湖': 'Wanfeng lake',
    '铜仁大峡谷': 'Tongren canyon',
    '施秉云台山': 'Yuntai mountain Shibing',
    '晴隆二十四道拐': 'Qinglong 24 turns',
    '湄潭茶海': 'Meitan tea plantation',
    '乌蒙大草原': 'Wumeng grassland',
    '花江大峡谷': 'Huajiang canyon',
    '格凸河': 'Getuhe river',
    '旧州古镇': 'Jiuzhou ancient town',
    '大同古镇': 'Datong ancient town Guizhou',
    '丙安古镇': 'Bingan ancient town',
    '土城古镇': 'Tucheng ancient town',
    '天龙屯堡': 'Tianlong tunpu',
    '凯里民族博物馆': 'Kaili museum',
    '遵义古城': 'Zunyi old city',
    '遵义红军山': 'Zunyi Red Army',
    '贵阳文昌阁': 'Guiyang Wenchang Pavilion',
    '六盘水梅花山': 'Meihuishan',
    '六盘水野玉海': 'Yeyuhai',
    '龙里大草原': 'Longli grassland',
    '北盘江大桥': 'Beipanjiang bridge',
    '三宝侗寨': 'Sanbao Dong village',
    '堂安侗寨': "Tang'an Dong village",
    '小黄侗寨': 'Xiaohuang Dong village',
    '大利侗寨': 'Dali Dong village',
    '黄岗侗寨': 'Huanggang Dong village',
    '高坡苗乡': 'Gaopo Miao',
    '鲍家屯': 'Baojia tunpu',
    '本寨': 'Benzhai village',
    '云山屯': 'Yunshan tun',
    '思南温泉': 'Sinan hot spring',
    '息烽集中营纪念馆': 'Xifeng prison memorial',
    '安龙招堤': 'Anlong Zhaodi',
    '双乳峰': 'Shuangru peaks',
    '铜仁梵净山佛教文化苑': 'Fanjingshan temple',
    '铜仁苗王城': 'Miaowang city',
    '贵阳森林公园': 'Guiyang forest park',
    '贵阳阳明祠': 'Yangming temple Guiyang',
    '惠水好花红': 'Haohuahong village',
}


def get_attractions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM attractions ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    return rows


def has_images(attraction_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM images WHERE attraction_id = ?', (attraction_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def clear_images(attraction_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM images WHERE attraction_id = ?', (attraction_id,))
    conn.commit()
    conn.close()


def search_wikimedia(query, limit=3):
    params = {
        'action': 'query', 'generator': 'search',
        'gsrsearch': f'File:{query}', 'gsrlimit': str(limit),
        'prop': 'imageinfo', 'iiprop': 'url|size', 'iiurlwidth': '800',
        'format': 'json',
    }
    try:
        r = requests.get('https://commons.wikimedia.org/w/api.php',
                         params=params, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            pages = data.get('query', {}).get('pages', {})
            return [
                p.get('imageinfo', [{}])[0].get('url')
                for p in pages.values()
                if p.get('imageinfo', [{}])[0].get('url')
                and p.get('imageinfo', [{}])[0].get('size', 0) > 5000
            ]
    except Exception:
        pass
    return []


def download_image(url, save_path):
    for attempt in range(2):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                ct = r.headers.get('Content-Type', '')
                if 'image' in ct and len(r.content) > 5000:
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with open(save_path, 'wb') as f:
                        f.write(r.content)
                    return True
            time.sleep(3)
        except Exception:
            time.sleep(2)
    return False


def save_record(attraction_id, local_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO images (attraction_id, image_url, image_type, is_primary)
        VALUES (?, ?, 'main', 1)
    ''', (attraction_id, local_path))
    conn.commit()
    conn.close()


def main():
    force = '--force' in sys.argv
    limit = 20
    for arg in sys.argv[1:]:
        if arg.startswith('--limit'):
            if '=' in arg:
                limit = int(arg.split('=')[1])
            else:
                idx = sys.argv.index(arg)
                if idx + 1 < len(sys.argv):
                    limit = int(sys.argv[idx + 1])

    print("=" * 50)
    print("贵州景点图片爬虫 (Wikimedia)")
    print("=" * 50)

    os.makedirs(IMAGES_DIR, exist_ok=True)
    attractions = get_attractions()
    print(f"景点总数: {len(attractions)}")

    if force:
        todo = attractions[:limit]
        print(f"强制模式, 本批处理: {len(todo)} 个")
    else:
        todo = [(aid, name) for aid, name in attractions if not has_images(aid)][:limit]
        print(f"待处理: {len(todo)} 个 (本批最多 {limit})")

    if not todo:
        print("无需处理")
        return

    total = 0
    failed = []

    for aid, name in todo:
        print(f"  {name} ...", end=" ", flush=True)

        if force:
            clear_images(aid)

        query = SEARCH_KEYWORDS.get(name, name)
        urls = search_wikimedia(query)
        if not urls and query != name:
            urls = search_wikimedia(name)

        if not urls:
            print("skip")
            failed.append(name)
            time.sleep(3)
            continue

        safe = re.sub(r'[^\w一-龥]', '_', name)
        filename = f"{safe}.jpg"
        save_path = os.path.join(IMAGES_DIR, filename)

        ok = download_image(urls[0], save_path)
        if ok:
            size = os.path.getsize(save_path)
            rel = f"/static/images/attractions/{filename}"
            save_record(aid, rel)
            total += 1
            print(f"OK ({size // 1024}KB)")
        else:
            print("fail")
            failed.append(name)

        time.sleep(5)  # 每次间隔 5 秒，避免限速

    print(f"\n本批完成: 成功 {total}, 失败 {len(failed)}")
    if failed:
        print("失败列表:", ", ".join(failed[:10]))
    print("再次运行可继续下载剩余景点")


if __name__ == '__main__':
    main()
