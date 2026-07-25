# -*- coding: utf-8 -*-
"""删除玩偶|4K 弹幕源（GBK 安全版）"""
import json

CONFIG_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    c = json.load(f)

original_count = len(c['sites'])

# 删除 key=Wogg4K 的源
c['sites'] = [s for s in c['sites'] if s.get('key') != 'Wogg4K']

print("删除前站点数：{}".format(original_count))
print("删除后站点数：{}".format(len(c['sites'])))
print("已删除：key=Wogg4K (玩偶|4K 弹幕)")

with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)

print("\n[完成] config.json 已更新")
