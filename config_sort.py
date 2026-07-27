import json
import sys
import os

# 设置 UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

sites = config['sites']

def get_category(s):
    key = s.get('key', '')
    name = s.get('name', '')
    
    if key in ['NewDouBan', 'Doubana', 'Wexconfig']:
        return 0
    if any(k in name for k in ['4K', '玩偶', '至臻', '观影', '剧透', '虎斑', '木偶', '多多', '原盘']):
        return 1
    if any(k in name for k in ['秒播', '韩剧', '贱片', '文才', '独播', '闪电', '师兄', '太狗', '伊影', '热播', '伯伯', '新6V', '爱看', '瓜子']):
        return 2
    if any(k in name for k in ['短剧', '漫短', '漫剧']):
        return 3
    if any(k in name for k in ['听书', '悦庭', '爱上', '极品']):
        return 4
    if any(k in name for k in ['体育', '球通', '咖啡', '八八', 'WWE', '飞球']):
        return 5
    if any(k in name for k in ['夸克', '百度', 'UC', '光鸭', '天翼', '115', '123', '讯雷', '蜡笔', '至臻', '分享']):
        return 6
    if any(k in name for k in ['自动', '秒播', 'Bili', 'Emby', 'Live', 'So', 'Anime']):
        return 7
    if any(k in name for k in ['APP', '肥猫', '干饭', '光盘', '行动', '再来', '一碗', '蔬菜', '永永', '潮流']):
        return 8
    return 99

# 添加 category
for s in sites:
    s['_cat'] = get_category(s)

# 统计
print(f'Total: {len(sites)}')
cats = {}
cat_names = {0: 'Guide', 1: '4K', 2: 'FastPlay', 3: 'ShortDrama', 4: 'Audio', 5: 'Sports', 6: 'Cloud', 7: 'Agg', 8: 'App', 9: 'Other'}
for s in sites:
    c = s['_cat']
    name = cat_names.get(c, 'Other')
    if name not in cats:
        cats[name] = 0
    cats[name] += 1

for k, v in cats.items():
    print(f'  {k}: {v}')

# 检查重复 key
keys = [s['key'] for s in sites]
dups = {k: keys.count(k) for k in set(keys) if keys.count(k) > 1}
print(f'Dupes: {dups if dups else "None"}')

# 网盘源
print('\n=== Cloud Sources ===')
for s in sites:
    name = s.get('name', '')
    if any(k in name for k in ['夸克', '百度', 'UC', '光鸭', '天翼', '115', '123', '讯雷', '蜡笔', '至臻', '分享']):
        ext_str = str(s.get('ext', ''))[:30]
        changeable = s.get('changeable', 'N/A')
        print(f'  {s["key"]} | {s["name"]} | changeable: {changeable}')

# 排序
sites.sort(key=lambda x: (x['_cat'], x.get('name', '')))

# 移除临时字段
for s in sites:
    if '_cat' in s:
        del s['_cat']

# 保存
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print('Done')
