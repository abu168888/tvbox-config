# -*- coding: utf-8 -*-
"""
自动筛选并添加更多高质量秒播源（去重）
策略：优先选择带 New/Wex 前缀的影视源，排除已使用的
"""
import json
import requests

CONFIG_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'
GUARDS_DB_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\all_guard_classes.json'
SOURCE_URL = "https://9280.kstore.vip/newwex.json"

print("=" * 60)
print("步骤 1: 提取当前已使用的 Guard 类")
print("=" * 60)

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    c = json.load(f)

used_guards = set()
for site in c.get('sites', []):
    if site.get('type') == 3:
        api = site.get('api', '')
        if 'Guard' in api:
            used_guards.add(api)

print("当前已使用：{} 个 Guard 类".format(len(used_guards)))

print("\n步骤 2: 加载 Guard 数据库")
print("=" * 60)

with open(GUARDS_DB_PATH, 'r', encoding='utf-8') as f:
    guards_db = json.load(f)

categories = guards_db['categories']
all_guards = guards_db['all_guards']

print("数据库中总共有：{} 个 Guard 类".format(len(all_guards)))

print("\n步骤 3: 筛选未使用的高质量秒播源")
print("=" * 60)

# 从"影视源"类别中筛选
video_sources = categories.get("影视源", [])

candidates = []
for guard_class in video_sources:
    # 排除已使用的
    if guard_class in used_guards:
        continue
    
    # 排除特殊用途
    if any(x in guard_class for x in ['Config', 'Push', 'My', 'Book', 'Sport', 'DuanJu', 'ManJu']):
        continue
    
    # 计算质量分数
    score = 0
    name_desc = ""
    
    if 'New' in guard_class:
        score += 2
        name_desc += "新版本 "
    if 'Wex' in guard_class:
        score += 1
        name_desc += "优化版 "
    
    # 知名源加分
    known_good = ['Bili', 'AList', 'Emby', 'Live', 'So97So', 'SoHaiYin']
    for keyword in known_good:
        if keyword in guard_class:
            score += 1
            name_desc += "{} ".format(keyword)
    
    candidates.append((guard_class, score, name_desc))

# 按分数排序
candidates.sort(key=lambda x: -x[1])

print("找到 {} 个候选源".format(len(candidates)))
print("\n推荐的前 8 个（按质量分排序）:")
for i, (gc, score, desc) in enumerate(candidates[:8], 1):
    clean_name = gc.replace('csp_', '').replace('Guard', '')
    print("{}. {} | 分数:{} | {}".format(i, clean_name, score, desc.strip() if desc else "标准版"))

print("\n步骤 4: 准备验证列表")
print("=" * 60)

# 选取 Top 8 进行验证
verify_list = [gc for gc, _, _ in candidates[:8]]
print("待验证列表:")
for gc in verify_list:
    print(" - {}".format(gc))

print("\n步骤 5: 开始在线验证...")
print("=" * 60)

# 获取官方配置
r = requests.get(SOURCE_URL, timeout=30)
if r.status_code != 200:
    print("[失败] 无法连接官方源")
    exit(1)

data = r.json()
official_sites = data.get('sites', [])

# 提取官方源中使用的所有 Guard 类
official_guards = set()
for site in official_sites:
    if site.get('type') == 3:
        api = site.get('api', '')
        if 'Guard' in api:
            official_guards.add(api)

# 验证候选列表
verified = []
for gc in verify_list:
    if gc in official_guards:
        status = "OK"
        verified.append(gc)
    else:
        status = "X"
    print("[{}] {}".format(status, gc))

print("\n验证结果：{}/{} 通过".format(len(verified), len(verify_list)))

if len(verified) < 4:
    print("通过数量不足，建议重新筛选或扩大验证范围")
    exit(0)

print("\n步骤 6: 创建添加配置")
print("=" * 60)

sources_to_add = []
name_mapping = {
    "csp_AnimeMiaoWuGuard": "动漫喵屋",
    "csp_AnimeMoDuGuard": "动漫墨读",
    "csp_DiyVodGuard": "DIY 点播",
    "csp_EmbyGuard": "Emby 影音",
    "csp_LiveBiLiGuard": "直播 B 站",
    "csp_So97SoGuard": "九七搜索",
    "csp_SoHaiYinGuard": "海音影视",
    "csp_WebDAVGuard": "WebDAV 云盘",
}

for gc in verified:
    clean_name = gc.replace('csp_', '').replace('Guard', '')
    display_name = name_mapping.get(gc, clean_name)
    
    source = {
        "key": "Auto_" + clean_name,
        "name": "秒播┃{}".format(display_name),
        "type": 3,
        "api": gc,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 0
    }
    sources_to_add.append(source)

print("将添加 {} 个新源:".format(len(sources_to_add)))
for s in sources_to_add:
    print(" - {} ({})".format(s['name'], s['api']))

print("\n步骤 7: 执行添加操作")
print("=" * 60)

original_count = len(c['sites'])

# 检查重复并添加
existing_keys = {s.get('key') for s in c['sites']}
actually_added = []
for source in sources_to_add:
    if source['key'] not in existing_keys:
        c['sites'].append(source)
        actually_added.append(source)

new_count = len(c['sites'])
print("原本站点数：{}".format(original_count))
print("新增站点数：{}".format(len(actually_added)))
print("现在总站点数：{}".format(new_count))

# 保存配置
with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)

print("\n[完成] 配置已更新")
print("下一步：git add . && git commit -m \"...\" && git push")
