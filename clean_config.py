import json
import sys
import os

# 设置 UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

sites = config['sites']

remove_non_guard = {'Netfixtv', 'Duopan', 'Wwys', 'Gz360', 'SP360', 'Jianpian', 'MTV', 'Kugou', 'FirstAid', 'Dm84'}
remove_app = {'FeiMao', 'GanFan', 'GuangPan', 'XingDong', 'ZaiLai', 'YiWan', 'ShuCai', 'YongYong', 'ChaoLiu'}
remove_my_pan = {'MyQuark', 'MyBaiDu', 'MyUcPan', 'MyGuangYa', 'MyPan189', 'MyPan115', 'Fake115Share', 'MyPan123'}

all_remove = remove_non_guard.union(remove_app).union(remove_my_pan)

print("Total removed:", len(all_remove))
print("\nKeys to remove:")
for key in sorted(all_remove):
    print("  " + key)

new_sites = [s for s in sites if s['key'] not in all_remove]

print("\nAfter cleanup:")
cats = {}
for s in new_sites:
    name = s.get('name', '')
    if any(k in name for k in ['夸克', '百度', 'UC', '光鸭', '天翼', '115', '123', '讯雷']):
        category = 'Cloud'
    elif any(k in name for k in ['4K', '玩偶', '至臻', '观影', '剧透', '虎斑', '木偶']):
        category = '4K'
    elif any(k in name for k in ['秒播', '韩剧', '贱片', '文才', '独播', '闪电', '师兄', '太狗', '伊影', '热播', '伯伯']):
        category = 'FastPlay'
    elif any(k in name for k in ['短剧', '漫短', '漫剧']):
        category = 'ShortDrama'
    elif any(k in name for k in ['听书']):
        category = 'Audio'
    elif any(k in name for k in ['体育']):
        category = 'Sports'
    elif any(k in name for k in ['自动', '采集']):
        category = 'Agg'
    else:
        category = 'Other'
    
    cats[category] = cats.get(category, 0) + 1

for k, v in sorted(cats.items()):
    print("  %s: %d" % (k, v))

keys = [s['key'] for s in new_sites]
dups = {k: keys.count(k) for k in set(keys) if keys.count(k) > 1}
print("\nDuplicate keys:", dups if dups else "None")

print("\nCloud sources:")
for s in new_sites:
    name = s.get('name', '')
    if any(k in name for k in ['夸克', '百度', 'UC', '光鸭', '天翼', '115', '123', '讯雷']):
        changeable = s.get('changeable', 'N/A')
        ext = str(s.get('ext', ''))[:30]
        print("  %s | %s | changeable: %s | ext: %s" % (s['key'], name, changeable, ext))

config['sites'] = new_sites
with open('config_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("\nTotal: %d -> %d (removed %d)" % (len(sites), len(new_sites), len(all_remove)))
print("Saved to config_cleaned.json")
