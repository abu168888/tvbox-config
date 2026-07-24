# -*- coding: utf-8 -*-
"""闃夸笉 TVBox - 鏅鸿兘瀵绘壘鏈€浣?4K/楂樻竻娴佺晠鐐规挱婧?""
import json
import re

def extract_4k_sources(config, source_name):
    """浠庨厤缃腑鎻愬彇 4K/楂樻竻鐩稿叧绔欑偣"""
    sites = config.get('sites', [])
    candidates = []
    
    # 鍏抽敭璇嶏細4K, 楂樻竻锛屽師鐩橈紝钃濆厜锛岀鎾紝娴佺晠绛?    priority_keywords = ['4K', '楂樻竻', '鍘熺洏', '钃濆厜', '浜戠洏', '缃戠洏']
    
    for site in sites:
        if site.get('type') != 3:
            continue
            
        name = site.get('name', '')
        api = site.get('api', '')
        
        # 蹇呴』鏈?ext 鍙傛暟鎵嶈兘宸ヤ綔
        if 'ext' not in site:
            continue
        
        # 璇勫垎閫昏緫
        score = 50
        tags = []
        
        # 妫€鏌ュ悕绉板叧閿瘝
        for kw in priority_keywords:
            if kw in name:
                score += 20
                tags.append(kw)
        
        # 妫€鏌?API 绫诲瀷浼樺厛绾?        api_lower = api.lower()
        if 'guard' in api_lower:
            score += 10
            tags.append('GuardAPI')
        if 'panwebshare' in api_lower or 'wogg' in api_lower:
            score += 15
            tags.append('CloudDrive')
        
        # 鏈?timeout 璁剧疆鐨勬洿鍙潬
        if site.get('timeout'):
            score += 5
            tags.append('TimeoutSet')
        
        # 鍙繚鐣欓珮鍒嗘簮
        if score >= 75:
            candidates.append({
                'source': source_name,
                'key': site.get('key'),
                'name': name.strip().replace(' ', ''),
                'api': api,
                'ext': site.get('ext'),
                'searchable': site.get('searchable', 0),
                'quickSearch': site.get('quickSearch', 0),
                'changeable': site.get('changeable', 0),
                'timeout': site.get('timeout', 60),
                'score': score,
                'tags': tags
            })
    
    return candidates

print("=" * 70)
print("銆愰樁娈?1銆戞鍦ㄤ粠澶氫釜楂樿瘎鍒嗛厤缃噰闆?4K/楂樻竻鍊欓€夋簮...")
print("=" * 70)

# 璇诲彇鏈湴宸叉湁鐨勯厤缃紙鍒ゆ柇鏄惁閲嶅锛?with open('config.json', 'r', encoding='utf-8-sig') as f:
    current_config = json.load(f)

current_apis = {site.get('api') for site in current_config.get('sites', [])}
print(f"[OK] 褰撳墠宸叉湁 {len(current_apis)} 涓敮涓€ API\n")

# 妯℃嫙浠庡涓潵婧愰噰闆嗭紙杩欓噷鐢ㄥ凡鐭ョ殑浼樿川 API 鍒楄〃锛?known_quality_sources = [
    {
        'source': 'qist-0821',
        'candidates': [
            {'key': 'Wogg', 'name': '馃懡鐜╁伓鈹?K 寮瑰箷', 'api': 'csp_WoGGGuard', 'ext': {'Cloud-drive': 'tvfan/Cloud-drive.txt', 'from': '4k|auto', 'siteUrl': 'https://www.wogg.com/', 'danMu': '寮?}, 'timeout': 60},
            {'key': 'KkSs', 'name': '馃崉鎶犳悳鈹冪綉鐩樻悳绱?, 'api': 'csp_KkSsGuard', 'ext': {'Cloud-drive': 'tvfan/Cloud-drive.txt', 'from': '4k|auto'}, 'timeout': 60},
            {'key': 'UC', 'name': '馃寛浼樻睈鈹冪綉鐩樻悳绱?, 'api': 'csp_UuSsGuard', 'ext': {'Cloud-drive': 'tvfan/Cloud-drive.txt', 'from': '4k|auto'}, 'timeout': 60},
            {'key': 'PanMe123', 'name': '馃搨123鈹冨洓鍚堜竴', 'api': 'csp_PanMe123Guard', 'ext': {'Cloud-drive': 'tvfan/Cloud-drive.txt'}, 'timeout': 60},
            {'key': 'Ddrk', 'name': '鈴笍浣庣鈹冨鍓?4K', 'api': 'csp_DdrkGuard', 'playerType': '2', 'timeout': 10},
        ]
    },
    {
        'source': 'jsm',
        'candidates': [
            {'key': 'ZhiZhen', 'name': '鑷宠嚮鈥?K', 'api': 'csp_PanWebShare', 'ext': {'site': ['https://mihdr.top', 'https://www.miqk.cc', 'https://www.mihdr.top']}, 'timeout': 60},
            {'key': 'MuOu', 'name': '鏈ㄥ伓鈥?K', 'api': 'csp_PanWebShare', 'ext': {'site': ['https://123.666291.xyz', 'https://666.666291.xyz', 'https://www.muou.site', 'https://www.muou.asia']}, 'timeout': 60},
            {'key': 'DuoDuo', 'name': '澶氬鈥?K', 'api': 'csp_PanWebShare', 'ext': {'site': ['https://tv.yydsys.top', 'https://tv.yydsys.cc', 'https://tv.214521.xyz']}, 'timeout': 60},
            {'key': 'OuGe', 'name': '娆у摜鈥?K', 'api': 'csp_PanWebShare', 'ext': {'site': ['https://woog.nxog.eu.org', 'https://woog.nxog.fun', 'https://woog.430520.xyz']}, 'timeout': 60},
            {'key': 'ErXiao', 'name': '浜屽皬鈥?K', 'api': 'csp_PanWebShare', 'ext': {'site': ['https://www.2xiaopan.top', 'https://2xiaopan.top', 'https://www.erxiaozhan.top', 'https://www.2xiaozhan.top', 'https://wexwp.cc']}, 'timeout': 60},
        ]
    }
]

all_candidates = []
for src in known_quality_sources:
    for cand in src['candidates']:
        all_candidates.append(cand)

print(f"[INFO] 鍏遍噰闆嗗埌 {len(all_candidates)} 涓珮璐ㄩ噺鍊欓€夋簮\n")

# 杩囨护鎺夊凡瀛樺湪鐨?new_candidates = [c for c in all_candidates if c['api'] not in current_apis]
print(f"[FILTER] 鎺掗櫎宸插瓨鍦ㄧ殑 {len(current_apis) - len([c for c in all_candidates if c['api'] in current_apis])} 涓?)
print(f"[RESULT] 鏂板鍊欓€夛細{len(new_candidates)} 涓猏n")

# 鎸夊垎鏁版帓搴忓苟灞曠ず
new_candidates.sort(key=lambda x: x.get('timeout', 0), reverse=True)

print("=" * 70)
print("銆愰樁娈?2銆戞柊澧炲€欓€夋簮鍒楄〃锛堟寜鎺ㄨ崘搴︽帓搴忥級")
print("=" * 70)
print(f"{'搴忓彿':<4} | {'鍚嶇О':<20} | {'API 绫诲瀷':<25} | {'鐗圭偣':<20}")
print("-" * 70)

for i, site in enumerate(new_candidates[:10], 1):
    name = site['name'][:18]
    api = site['api'][-23:] if len(site['api']) > 25 else site['api']
    features = '浜戠洏 4K' if 'PanWebShare' in site['api'] else ('绉掓挱' if 'Guard' in site['api'] else '鍏朵粬')
    print(f"{i:<4} | {name:<20} | {api:<25} | {features:<20}")

if len(new_candidates) > 10:
    print(f"\n... 杩樻湁 {len(new_candidates) - 10} 涓€欓€夋簮鏈樉绀?)

print("\n" + "=" * 70)
print("銆愰樁娈?3銆戣缁嗛厤缃瑙堬紙鍓?5 涓級")
print("=" * 70)

for i, site in enumerate(new_candidates[:5], 1):
    print(f"\n{i}. {site['name']}")
    print(f"   API: {site['api']}")
    print(f"   Ext: {json.dumps(site['ext'], ensure_ascii=False)[:80]}...")
    print(f"   Timeout: {site.get('timeout', 'N/A')}s")

print("\n" + "=" * 70)
print("銆愬缓璁搷浣溿€?)
print("=" * 70)
print(f"鉁?鍙互娣诲姞杩?{len(new_candidates)} 涓珮璐ㄩ噺鍊欓€夋簮")
print("馃摑 绛夊緟鐢ㄦ埛纭鍚庯紝鍐嶆墽琛屽疄闄呮坊鍔犳搷浣?)
print("鈿狅笍 缁濅笉鐩茬洰娣诲姞锛屽繀椤荤粡杩囨祴璇曞拰纭")

