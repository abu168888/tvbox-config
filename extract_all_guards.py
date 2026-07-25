# -*- coding: utf-8 -*-
"""从新配置源提取所有唯一的 Guard 类名"""
import requests
import json

url = 'https://9280.kstore.vip/newwex.json'
r = requests.get(url, timeout=30)
data = r.json()

# 提取所有 type=3 且包含 Guard 的 api
guards = set()
for site in data.get('sites', []):
    if site.get('type') == 3:
        api = site.get('api', '')
        if 'Guard' in api:
            guards.add(api)

guards_list = sorted(list(guards))
print("总共找到 {} 个唯一 Guard 类".format(len(guards_list)))

# 分类统计
categories = {
    "4K 源": [],
    "影视源": [],
    "短剧源": [],
    "听书源": [],
    "体育源": [],
    "网盘源": [],
    "配置中心": [],
    "其他": []
}

for g in guards_list:
    if 'Wogg' in g or 'WoGG' in g or '4K' in g:
        categories["4K 源"].append(g)
    elif 'DuanJu' in g or 'ManJu' in g:
        categories["短剧源"].append(g)
    elif 'Book' in g or 'TingShu' in g:
        categories["听书源"].append(g)
    elif 'Sport' in g:
        categories["体育源"].append(g)
    elif 'My' in g or 'Pan' in g or 'Quark' in g or 'BaiDu' in g:
        categories["网盘源"].append(g)
    elif 'Config' in g or 'DouBan' in g:
        categories["配置中心"].append(g)
    else:
        categories["影视源"].append(g)

# 输出详细分类
for cat, items in categories.items():
    print("\n【{}】(共 {} 个)".format(cat, len(items)))
    for item in items[:10]:
        print(" - {}".format(item))
    if len(items) > 10:
        print(" ... 还有 {} 个".format(len(items)-10))

# 保存完整清单
with open('all_guard_classes.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total': len(guards_list),
        'categories': categories,
        'all_guards': guards_list
    }, f, indent=2, ensure_ascii=False)

print("\n[完成] 已保存到 all_guard_classes.json")
