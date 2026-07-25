# -*- coding: utf-8 -*-
"""删除玩偶|4K 弹幕源并验证配置"""
import json

CONFIG_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    c = json.load(f)

original_count = len(c['sites'])

# 删除 key=Wogg4K 的源（玩偶 |4K 弹幕）
deleted_name = None
c['sites'] = [s for s in c['sites'] if not (s.get('key') == 'Wogg4K')]

for site in c['sites']:
    if site.get('key') == 'Wogg4K':
        deleted_name = site.get('name')
        break

if original_count != len(c['sites']):
    deleted_name = "💡玩偶┃4K 弹幕💡"
    
print("删除前：{} 个站点".format(original_count))
print("删除后：{} 个站点".format(len(c['sites'])))
print("已删除：{}".format(deleted_name or "未找到"))

with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)

print("\n[完成] config.json 已更新")
