# -*- coding: utf-8 -*-
"""
最终修复脚本 - 重点修复哔滴/南瓜/泥巴/快看/星星等影视源
1. 删除所有可能错误的影视源
2. 在 4K 源后面立即插入正确的影视源列表
3. 移除直播源（按用户要求）
"""
import json, os

BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

def load():
    with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save(c):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(c, f, indent=2, ensure_ascii=False)

c = load()

# 要完全移除的 key 列表（清理所有有问题的影视源）
remove_keys = [
    # 旧的可能错误的源
    'Bdys', 'Bdys01', 'NanGua', 'Kuaikan', 'NiNi', 'Star', 'ZhuiJu', 
    'TianTian', 'ChangZhang', 'TV3V', 'ReBoZJ', 'ShiPinSou', 'DaDaG',
    # 修复脚本添加但在错误位置的源
    'zxzj', '厂长', '低端', '快看', '热播', '星星', '南瓜', 'Auete', 
    '泥巴', '6V', '比特', '文采', 'lib', 'XunLeim', 'LiveNew'
]

# 先过滤掉所有要移除的源
c['sites'] = [s for s in c['sites'] if s.get('key') not in remove_keys]

# 高质量的影视源列表（按用户要求的关键源 + 其他稳定源）
fixed_sites = [
    # === 核心需求源（必选）===
    {"key": "哔滴", "name": "⚡哔滴┃高清⚡", "type": 3, "api": "csp_Bdys", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "南瓜", "name": "⚡南瓜┃高清⚡", "type": 3, "api": "csp_NanGua", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "http://pan.nanag.com"},
    {"key": "泥巴", "name": "⚡泥巴┃高清⚡", "type": 3, "api": "csp_NiNi", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "http://nila.cc"},
    {"key": "快看", "name": "⚡快看┃高清⚡", "type": 3, "api": "csp_Kkys", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "星星", "name": "⚡星星┃高清⚡", "type": 3, "api": "csp_Star", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "http://www.xingxg.cn"},
    
    # === 补充高质量源 ===
    {"key": "厂长", "name": "⚡厂长┃高清⚡", "type": 3, "api": "csp_NewCz", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "在线", "name": "⚡在线┃高清⚡", "type": 3, "api": "csp_Zxzj", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://www.zxzjhd.com/"},
    {"key": "低端", "name": "⚡低端┃高清⚡", "type": 3, "api": "csp_Ddrk", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://ddrk.co"},
    {"key": "热播", "name": "⚡热播┃高清⚡", "type": 3, "api": "csp_AppTT", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "AO7TcBkd8I/B5wQc4Qma+pU="},
    {"key": "Auete", "name": "⚡Auete┃高清⚡", "type": 3, "api": "csp_Auete", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://auete.pro/"},
    {"key": "6V", "name": "⚡新 6V┃磁力⚡", "type": 3, "api": "csp_SixV", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://www.xb6v.com/"},
    {"key": "比特", "name": "⚡比特┃高清⚡", "type": 3, "api": "csp_Bttwoo", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
]

# 找到 4K 源的最后一个位置（寻找"💓123┃4K💓"这个源）
insert_index = None
for i, site in enumerate(c['sites']):
    if '123┃4K' in site.get('name', '') or site.get('key') == 'NewPanMe123':
        insert_index = i + 1
        break

# 如果没有找到，默认插入到第 5 个元素后面（Wexconfig 之后）
if insert_index is None:
    insert_index = 5

# 在指定位置插入修复后的影视源
for idx, site in enumerate(fixed_sites, start=insert_index):
    c['sites'].insert(idx, site)

# 移除直播源（按用户要求）
c.pop('lives', None)

print(f"[OK] 已删除 {len(remove_keys)} 个可能错误的影视源")
print(f"[OK] 已添加 {len(fixed_sites)} 个修复后的影视源")
print(f"[OK] 插入位置：在第 {insert_index} 个元素后 (紧跟 4K 源)")
print(f"[OK] 总影视源数量：{len(c['sites'])}")
print(f"[OK] 已移除直播源列表")
print("\n[INFO] 核心影视源清单:")
for site in fixed_sites[:5]:
    print(f"   - {site['name']}: {site['api']}")

save(c)
print("\n[SUCCESS] config.json 已保存成功!")
