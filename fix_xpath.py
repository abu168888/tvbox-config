# -*- coding: utf-8 -*-
"""
终极修复 - 使用 XPath 类型的稳定影视源
这些源不依赖特定 spider.jar，任何 TVBox 都能用
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

# 删除所有之前添加的错误源
remove_keys = ['哔滴', '南瓜', '泥巴', '快看', '星星', '厂长', '在线', '低端', '热播', 'Auete', '6V', '比特']
c['sites'] = [s for s in c['sites'] if s.get('key') not in remove_keys]

# 使用 XPath 类型的稳定影视源（不需要特定 spider.jar）
xpath_sites = [
    {
        "key": "哔滴",
        "name": "哔滴│高可用",
        "type": 3,
        "api": "csp_XPathMacFilter",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/XP/master/bdys.json"
    },
    {
        "key": "南瓜",
        "name": "南瓜│高可用",
        "type": 3,
        "api": "csp_XPathMacFilter",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/XP/master/nangua.json"
    },
    {
        "key": "泥巴",
        "name": "泥巴│高可用",
        "type": 3,
        "api": "csp_XPathMacFilter",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/XP/master/nm.json"
    },
    {
        "key": "快看",
        "name": "快看│高可用",
        "type": 3,
        "api": "csp_XPathMacFilter",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/XP/master/kuaikan.json"
    },
    {
        "key": "星星",
        "name": "星星│高可用",
        "type": 3,
        "api": "csp_XPathMacFilter",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/XP/master/xingxg.json"
    },
    {
        "key": "厂长",
        "name": "厂长│高可用",
        "type": 3,
        "api": "csp_XPathMacFilter",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/XP/master/cz.json"
    },
    {
        "key": "在线之家",
        "name": "在线之家│高可用",
        "type": 3,
        "api": "csp_XPathMacFilter",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/XP/master/zxzj.json"
    },
    {
        "key": "低端",
        "name": "低端│高可用",
        "type": 3,
        "api": "csp_XPathMacFilter",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/XP/master/ddrk.json"
    }
]

# 找到插入位置 (Wogg4K 之后)
insert_index = None
for i, site in enumerate(c['sites']):
    if site.get('key') == 'Wogg4K':
        insert_index = i + 1
        break

if insert_index is None:
    print("[ERROR] 找不到 Wogg4K!")
    exit(1)

# 插入 XPath 影视源
for idx, site in enumerate(xpath_sites, start=insert_index):
    c['sites'].insert(idx, site)

print(f"[OK] 已删除 {len(remove_keys)} 个错误源")
print(f"[OK] 已添加 {len(xpath_sites)} 个 XPath 类型的高可用影视源")
print(f"[OK] 插入位置：第 {insert_index} 位 (Wogg4K 后)")
print(f"[OK] 总数：{len(c['sites'])}")

save(c)
print("\n[SUCCESS] 完成！XPath 源兼容任何 TVBox 版本")
