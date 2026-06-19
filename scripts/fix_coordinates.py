"""
修复景点坐标 - 使用免费地理编码API获取真实经纬度

使用方式：
    python scripts/fix_coordinates.py

默认使用 Nominatim（OpenStreetMap），完全免费，无需注册或Key。
如需更高精度，可配置高德地图Key（见下方说明）。
"""

import json
import os
import time
import urllib.request
import urllib.parse

# ============================================================
#  地理编码服务配置
#
#  默认: Nominatim (OpenStreetMap) — 完全免费，无需Key
#  备选: 高德地图 — 需要注册免费Key，精度更高
#        获取方式: https://console.amap.com → 应用管理 → 添加Key → 服务类型选"Web服务"
# ============================================================
AMAP_KEY = '22bf99ec10a857f24da0e7b18d50d1f8'  # 高德Web服务Key

# Nominatim要求至少间隔1秒
NOMINATIM_INTERVAL = 1.2
# 高德REST API间隔
AMAP_INTERVAL = 0.3


# ==================== Nominatim (OpenStreetMap) ====================

def geocode_nominatim(query):
    """
    使用Nominatim（OpenStreetMap）进行地理编码
    完全免费，无需Key，限制每秒1次请求
    """
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({
        'q': query,
        'format': 'json',
        'limit': 1,
        'accept-language': 'zh',
        'countrycodes': 'cn',  # 限定中国
    })
    req = urllib.request.Request(url, headers={
        'User-Agent': 'GuizhouTravelAssistant/1.0 (student project)'
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if data:
            return float(data[0]['lon']), float(data[0]['lat'])
    except Exception as e:
        print(f'  [Nominatim异常] {e}')
    return None, None


# ==================== 高德地图 ====================

def geocode_amap_address(address):
    """高德地理编码API - 通过地址"""
    if not AMAP_KEY:
        return None, None
    url = 'https://restapi.amap.com/v3/geocode/geo?' + urllib.parse.urlencode({
        'key': AMAP_KEY,
        'address': address,
    })
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if data.get('status') == '1' and data.get('geocodes'):
            location = data['geocodes'][0].get('location', '')
            if location:
                lng, lat = location.split(',')
                return float(lng), float(lat)
    except Exception as e:
        print(f'  [高德地址编码异常] {e}')
    return None, None


def geocode_amap_poi(name, city=''):
    """高德POI关键字搜索"""
    if not AMAP_KEY:
        return None, None
    keywords = name
    for prefix in ['贵阳', '遵义', '安顺', '铜仁', '毕节', '六盘水',
                    '黔东南', '黔南', '黔西南']:
        if keywords.startswith(prefix):
            keywords = keywords[len(prefix):]
            break
    params = {
        'key': AMAP_KEY,
        'keywords': keywords,
        'city': city or '贵州',
        'offset': 5,
    }
    url = 'https://restapi.amap.com/v3/place/text?' + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if data.get('status') == '1' and data.get('pois'):
            location = data['pois'][0].get('location', '')
            if location:
                lng, lat = location.split(',')
                return float(lng), float(lat)
    except Exception as e:
        print(f'  [高德POI异常] {e}')
    return None, None


# ==================== 工具函数 ====================

def extract_city(address):
    """从地址中提取城市名"""
    if not address:
        return ''
    for city in ['贵阳', '遵义', '安顺', '铜仁', '毕节', '六盘水',
                 '黔东南', '黔南', '黔西南', '凯里', '都匀', '兴义']:
        if city in address:
            return city
    return ''


def build_search_queries(name, address):
    """构造多种搜索关键词，按优先级排列"""
    queries = []
    city = extract_city(address)

    # 策略1: 景点名 + 贵州
    queries.append(f'{name} 贵州')

    # 策略2: 景点名 + 城市
    if city:
        queries.append(f'{name} {city}')

    # 策略3: 直接用地址
    if address and address != name:
        queries.append(address)

    return queries


# ==================== 主流程 ====================

def geocode_one(name, address):
    """
    对一个景点进行地理编码
    优先级: 高德地址编码 → 高德POI搜索 → Nominatim（多种关键词）
    """
    # --- 高德方案 ---
    if AMAP_KEY:
        # 高德地址编码
        lng, lat = geocode_amap_address(address or name)
        if lng is not None:
            return lng, lat, '高德-地址编码'

        time.sleep(AMAP_INTERVAL)

        # 高德POI搜索
        city = extract_city(address)
        lng, lat = geocode_amap_poi(name, city)
        if lng is not None:
            return lng, lat, '高德-POI搜索'

        time.sleep(AMAP_INTERVAL)

    # --- Nominatim方案（多种关键词尝试） ---
    queries = build_search_queries(name, address)
    for q in queries:
        time.sleep(NOMINATIM_INTERVAL)
        lng, lat = geocode_nominatim(q)
        if lng is not None:
            return lng, lat, f'Nominatim'

    return None, None, '失败'


def main():
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'guizhou_attractions.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    service = '高德地图' if AMAP_KEY else 'Nominatim (OpenStreetMap)'
    print(f'地理编码服务: {service}')
    print(f'景点总数: {len(data)}')
    print(f'预计耗时: {len(data) * 1.5 / 60:.1f} 分钟' if not AMAP_KEY else
          f'预计耗时: {len(data) * 0.6 / 60:.1f} 分钟')
    print('=' * 70)

    success_count = 0
    fail_count = 0
    changed_count = 0
    failed_list = []

    for i, attr in enumerate(data):
        name = attr.get('name', '')
        address = attr.get('address', '')
        old_lat = attr.get('latitude')
        old_lng = attr.get('longitude')

        print(f'[{i+1:3d}/{len(data)}] {name}', end=' ... ')

        lng, lat, source = geocode_one(name, address)

        if lng is not None:
            attr['latitude'] = round(lat, 6)
            attr['longitude'] = round(lng, 6)
            success_count += 1

            if old_lat and old_lng:
                lat_diff = abs(lat - old_lat)
                lng_diff = abs(lng - old_lng)
                if lat_diff > 0.01 or lng_diff > 0.01:
                    changed_count += 1
                    print(f'[OK] 修正 ({source})  ({old_lat},{old_lng}) -> ({lat:.4f},{lng:.4f})')
                else:
                    print(f'[OK] 无变化 ({source})')
            else:
                print(f'[OK] 新增 ({source})  ({lat:.4f},{lng:.4f})')
        else:
            fail_count += 1
            failed_list.append(name)
            print(f'[FAIL] 失败，保留原坐标')

    # 写回JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print('\n' + '=' * 70)
    print('修正完成！')
    print(f'  成功: {success_count}/{len(data)}')
    print(f'  坐标变化: {changed_count}')
    print(f'  失败: {fail_count}')
    if failed_list:
        print(f'  失败列表: {", ".join(failed_list)}')
    print(f'\nJSON文件已更新: {json_path}')


if __name__ == '__main__':
    main()
