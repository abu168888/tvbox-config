# -*- coding: utf-8 -*-
"""添加推荐的 5 个高质量 Guard 类到配置中"""
import json

CONFIG_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'

# 推荐的高品质源列表
recommended_sources = [
    {
        "key": "Auto_NewBiLiYS",
        "name": "自动┃B 站采集",
        "type": 3,
        "api": "csp_NewBiLiYSGuard",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 0
    },
    {
        "key": "Auto_WexTangDou",
        "name": "自动┃糖豆短剧",
        "type": 3,
        "api": "csp_WexTangDouGuard",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 0
    },
    {
        "key": "Auto_AList",
        "name": "自动┃网盘聚合",
        "type": 3,
        "api": "csp_AListGuard",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 0
    },
    {
        "key": "Auto_AnimeFanShu",
        "name": "自动┃动漫繁树",
        "type": 3,
        "api": "csp_AnimeFanShuGuard",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 0
    },
    {
        "key": "Auto_AnimeHuazi",
        "name": "自动┃葫芦动漫",
        "type": 3,
        "api": "csp_AnimeHuaziGuard",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 0
    }
]

print("[1/3] 加载当前配置...")
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    c = json.load(f)

original_count = len(c['sites'])
print("   当前站点数：{}".format(original_count))

print("\n[2/3] 检查重复...")
existing_keys = {s.get('key') for s in c['sites']}
to_add = []
for source in recommended_sources:
    if source['key'] not in existing_keys:
        to_add.append(source)
        print("   OK 待添加：{}".format(source['name']))
    else:
        print("   SKIP (已存在): {}".format(source['name']))

print("\n[3/3] 添加到配置末尾...")
for source in to_add:
    c['sites'].append(source)

new_count = len(c['sites'])
print("   新增站点数：{}".format(len(to_add)))
print("   现在总站点数：{}".format(new_count))

# 保存配置
with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)

print("\n[完成] 配置已更新")
print("下一步：git add . && git commit -m \"...\" && git push")
