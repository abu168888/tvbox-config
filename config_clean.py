import json

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

sites = config['sites']

# 1. 删除不可用的源
remove_keys = {'MiSou', 'PanSearch', 'NewDouBan', 'Doubana', 'Wexconfig'}

# 2. 删除 My* 网盘源（保留 Wex* 版本，changeable:1）
remove_my = {'MyQuark', 'MyBaiDu', 'MyUcPan', 'MyPan189', 'MyPan115', 'MyPan123', 'MyGuangYa', 'Fake115Share'}

new_sites = [s for s in sites if s['key'] not in remove_keys and s['key'] not in remove_my]

# 按类型分组排序
def get_category(s):
    key = s.get('key', '')
    name = s.get('name', '')
    
    if key in ['NewDouBan', 'Doubana', 'Wexconfig']:
        return 0
    if any(k in name for k in ['4K', '玩偶', '至臻', '观影', '剧透', '虎斑', '木偶', '多多', '原盘', '123']):
        return 1
    if any(k in name for k in ['秒播', '韩剧', '瓜子', '贱片', '文才', '独播', '闪电', '师兄', '太狗', '伊影', '热播', '伯伯', '新6V', '爱看']):
        return 2
    if any(k in name for k in ['短剧', '漫短', '漫剧']):
        return 3
    if any(k in name for k in ['听书', '悦庭', '爱上', '极品']):
        return 4
    if any(k in name for k in ['体育', '球通', '咖啡', '八八', 'WWE', '飞球']):
        return 5
    if any(k in name for k in ['夸克', '百度', 'UC', '光鸭', '天翼', '115', '123', '讯雷', '蜡笔', '至臻', '分享']):
        return 6
    if any(k in name for k in ['自动', '秒播┃B', '秒播┃Em', '秒播┃直播', '秒播┃九七', '秒播┃海音', '秒播┃动漫', 'Bili', 'Emby', 'Live', 'So', 'Anime']):
        return 7
    if any(k in name for k in ['APP', '肥猫', '干饭', '光盘', '行动', '再来', '一碗', '蔬菜', '永永', '潮流']):
        return 8
    return 99

for i, s in enumerate(new_sites):
    s['_cat'] = get_category(s)

# 按 category 排序
new_sites.sort(key=lambda x: (x['_cat'], x.get('name', '')))

# 移除临时字段（先删除再验证）
for s in new_sites:
    del s['_cat']

# 验证统计
print(f'总源数: {len(new_sites)}')
cats = {}
cat_names = {0: '引导配置', 1: '4K源', 2: '秒播影视', 3: '短剧源', 4: '听书源', 5: '体育源', 6: '网盘源', 7: '采集/秒播', 8: 'APP源', 9: '其他'}
for s in new_sites:
    c = get_category(s)
    name = cat_names.get(c, '其他')
    if name not in cats:
        cats[name] = 0
    cats[name] += 1

for k, v in cats.items():
    print(f'  {k}: {v}')

# 检查重复 key
keys = [s['key'] for s in new_sites]
dups = {k: keys.count(k) for k in set(keys) if keys.count(k) > 1}
print(f'\n重复key: {dups if dups else "无"}')

# 网盘源详细检查
print(f'\n=== 网盘源 ===')
for s in new_sites:
    name = s.get('name', '')
    if any(k in name for k in ['夸克', '百度', 'UC', '光鸭', '天翼', '115', '123', '讯雷', '蜡笔', '至臻', '分享']):
        ext_str = str(s.get('ext', ''))[:50]
        changeable = s.get('changeable', 'N/A')
        print(f'  {s["key"]} | {s["name"]} | changeable: {changeable} | ext: {ext_str}')

config['sites'] = new_sites

# 保存
with open('config_clean.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print('\nconfig_clean.json 已生成')
