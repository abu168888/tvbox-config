import json

with open('config.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

sites = d['sites']
print('=== 合并后总览 ===')
print(f'总源数: {len(sites)}')
guard_count = len([s for s in sites if 'Guard' in s.get('api', '')])
print(f'Guard类数: {guard_count}')
print()

print('=== 网盘源 ===')
pan_keywords = ['网盘', '夸克', '百度', 'UC', '光鸭', '天翼', '115', '123', '讯雷', '米搜', '盘搜', '蜡笔', '金牌', '荐片', '厂长', '农民', '360', '瓜子', '动漫巴士', '急救', '酷狗', '明星MV', '葵花', 'emby', '哔哔', '大鼻涕', '轮回', '天逸', '百度搜索', '海音', '九七', '88体育', '瓜子体育']
for s in sites:
    name = s.get('name', '')
    if any(k in name for k in pan_keywords):
        print(f'  - {s["key"]} | {s["name"]} | {s["api"]}')

print()
print('=== App源 ===')
for s in sites:
    name = s.get('name', '')
    api = s.get('api', '')
    if 'APP' in name or 'App' in api or 'AppGet' in api or 'AppQi' in api or 'AppRJ' in api:
        print(f'  - {s["key"]} | {s["name"]} | {s["api"]}')

print()
print('=== 短剧源 ===')
for s in sites:
    name = s.get('name', '')
    if '短剧' in name or '漫短' in name or '漫剧' in name:
        print(f'  - {s["key"]} | {s["name"]} | {s["api"]}')

print()
print('=== 秒播影视 ===')
for s in sites:
    name = s.get('name', '')
    if '秒播' in name or '火火' in name or '贱片' in name or '金牌' in name or '荐片' in name or '厂长' in name or '360' in name:
        print(f'  - {s["key"]} | {s["name"]} | {s["api"]}')

print()
print('=== 体育源 ===')
for s in sites:
    name = s.get('name', '')
    if '体育' in name:
        print(f'  - {s["key"]} | {s["name"]} | {s["api"]}')

print()
print('=== B站源 ===')
for s in sites:
    api = s.get('api', '')
    if 'Bili' in api:
        print(f'  - {s["key"]} | {s["name"]} | {s["api"]}')

print()
print('=== 听书源 ===')
for s in sites:
    name = s.get('name', '')
    if '听书' in name:
        print(f'  - {s["key"]} | {s["name"]} | {s["api"]}')

print()
print('=== 其他 ===')
for s in sites:
    name = s.get('name', '')
    api = s.get('api', '')
    if not any(k in name for k in pan_keywords) and 'APP' not in name and 'App' not in api and '短剧' not in name and '秒播' not in name and '体育' not in name and 'Bili' not in api and '听书' not in name and '动漫' not in name and '搜索' not in name:
        print(f'  - {s["key"]} | {s["name"]} | {s["api"]}')
