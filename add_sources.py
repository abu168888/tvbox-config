# -*- coding: utf-8 -*-
import json

# Read current config and backup pool
with open('config.json', 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

with open('backup_sources.json', 'r', encoding='utf-8-sig') as f:
    backup_pool = json.load(f)

# Get current APIs
current_apis = {site.get('api') for site in config.get('sites', [])}

# Define high-quality sources to add (farmers, factory, etc.)
priority_keywords = ['鍐滄皯', '鍘傞暱', '绯背', '鐧界櫧', '鏂囬噰', '绁炶溅', '绔嬫挱', '鍦ㄧ嚎']

print("褰撳墠宸插寘鍚殑绉掓挱婧?")
for site in config.get('sites', []):
    name = site.get('name', '')
    if any(kw in name for kw in priority_keywords + ['绉掓挱']):
        print(f"  鉁?{name}")

print("\n浠庡鐢ㄦ睜鎵惧埌鐨勪紭璐ㄦ湭娣诲姞婧?")
to_add = []
for site in backup_pool:
    api = site.get('api')
    if api in current_apis:
        continue
    
    name = site.get('name', '').replace('馃挕[qist-tvbox-0821] ', '').replace('馃挕[qist-tvbox-jsm] ', '')
    score = site.get('_meta_score', 0)
    
    # Prioritize high-score sources with good keywords
    if score >= 65 or any(kw in name for kw in priority_keywords):
        print(f"  鉃?{name} (寰楀垎:{score})")
        to_add.append({
            'key': site.get('key'),
            'name': name,
            'type': 3,
            'api': api,
            'searchable': site.get('searchable', 1),
            'quickSearch': site.get('quickSearch', 1),
            'changeable': 0
        })

# Insert new sources after the first few existing ones
if to_add:
    sites = config.get('sites', [])
    insert_pos = 4  # After header sections
    sites[insert_pos:insert_pos] = to_add
    
    print(f"\n鉁?宸叉坊鍔?{len(to_add)} 涓紭璐ㄦ簮鍒伴厤缃腑")
    
    # Save updated config
    with open('config.json', 'w', encoding='utf-8') as f:  # Write without BOM
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("馃摑 閰嶇疆宸叉洿鏂帮紒")
else:
    print("\n鈿狅笍 鎵€鏈変紭璐ㄦ簮宸插瓨鍦紝鏃犻渶娣诲姞")

print("OK Done")

