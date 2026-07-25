# -*- coding: utf-8 -*-
"""
最终修复 - 完美版本
1. 删除所有错误源
2. 在 Wogg4K 后插入影视源
3. 移除直播源
"""
import json, os

CONFIG_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'

def load():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(c):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(c, f, indent=2, ensure_ascii=False)

c = load()

# 删除错误和重复的源
remove_keys = [
    'zxzj', '厂长', '低端', '快看', '热播', '星星', '南瓜', 'Auete', 
    '泥巴', '6V', '比特', '文采', 'lib', 'XunLeim', 'LiveNew',
    'Bdys', 'Bdys01', 'NanGua', 'Kuaikan', 'NiNi', 'Star', 'ZhuiJu',
    'TianTian', 'ChangZhang', 'TV3V', 'ReBoZJ', 'ShiPinSou', 'DaDaG'
]
c['sites'] = [s for s in c['sites'] if s.get('key') not in remove_keys]

# 高质量影视源列表
movie_sites = [
    {"key": "哔滴", "name": "哔滴│高清", "type": 3, "api": "csp_Bdys", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "南瓜", "name": "南瓜│高清", "type": 3, "api": "csp_NanGua", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "http://pan.nanag.com"},
    {"key": "泥巴", "name": "泥巴│高清", "type": 3, "api": "csp_NiNi", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "http://nila.cc"},
    {"key": "快看", "name": "快看│高清", "type": 3, "api": "csp_Kkys", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "星星", "name": "星星│高清", "type": 3, "api": "csp_Star", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "http://www.xingxg.cn"},
    {"key": "厂长", "name": "厂长│高清", "type": 3, "api": "csp_NewCz", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "在线", "name": "在线│高清", "type": 3, "api": "csp_Zxzj", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://www.zxzjhd.com/"},
    {"key": "低端", "name": "低端│高清", "type": 3, "api": "csp_Ddrk", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://ddrk.co"},
    {"key": "热播", "name": "热播│高清", "type": 3, "api": "csp_AppTT", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "AO7TcBkd8I/B5wQc4Qma+pU="},
    {"key": "Auete", "name": "Auete│高清", "type": 3, "api": "csp_Auete", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://auete.pro/"},
    {"key": "6V", "name": "新 6V│磁力", "type": 3, "api": "csp_SixV", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://www.xb6v.com/"},
    {"key": "比特", "name": "比特│高清", "type": 3, "api": "csp_Bttwoo", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
]

# 找到 Wogg4K 的位置（第 19 个左右的元素）
insert_index = None
for i, site in enumerate(c['sites']):
    if site.get('key') == 'Wogg4K':
        insert_index = i + 1
        break

if insert_index is None:
    print("[ERROR] 找不到 Wogg4K!")
    exit(1)

# 插入影视源
for idx, site in enumerate(movie_sites, start=insert_index):
    c['sites'].insert(idx, site)

# 移除直播源
if 'lives' in c:
    del c['lives']

print(f"[OK] 删除 {len(remove_keys)} 个错误源")
print(f"[OK] 添加 {len(movie_sites)} 个影视源 (位置：{insert_index})")
print(f"[OK] 移除直播源")
print(f"[OK] 总数：{len(c['sites'])}")

save(c)
print("\n[SUCCESS] config.json 修复完成!")
