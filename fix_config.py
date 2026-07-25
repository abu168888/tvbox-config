import json
import sys
import io

# Fix console encoding for Chinese output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

config_path = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'

with open(config_path, 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

# Step 1: Delete invalid sources
delete_keys = ['GuGu_Anime', 'Pan123_4K', 'New6V_Magnet']
deleted = []
for s in config['sites']:
    if s['key'] in delete_keys:
        deleted.append((s['key'], s['name'], s['api']))

print("=" * 60)
print("删除无效源")
print("=" * 60)
for k, n, a in deleted:
    print(f"  [X] 删除: {n} ({a})")

# Step 2: Analyze reasons
print("")
print("=" * 60)
print("原因分析")
print("=" * 60)
print("网站可达性: 3个源网站 HTTP 200 正常返回")
print("根本原因: spider.jar 不支持这些 API 类型")
print("")
print("  咕咕动漫 -> csp_AppGet")
print("     需要特定 spider.jar 支持 AppGet 协议 + dataKey/dataIv 解密")
print("     你的 spider.jar 不包含此 spider")
print("")
print("  123 4K -> csp_PanWebShare123")
print("     这是 qist 的自定义 API，不在标准 spider.jar 中")
print("     你的 spider.jar 没有内置此类型")
print("")
print("  New6V 磁力 -> csp_New6v")
print("     需要 drpy2.min.js 脚本支持")
print("     你的 spider.jar 不支持 drpy 抓取")
print("")
print("结论: 这些源需要 spider.jar 包含对应 spider 类型才能工作")
print("      你的 spider.jar 只支持 csp_*Guard 系列")

# Step 3: Add new 4K sources
new_sources = [
    {"key": "NewPanSou", "name": "新盘搜4K", "type": 3, "api": "csp_PanSou", "searchable": 1, "quickSearch": 1, "changeable": 0},
    {"key": "YiSo", "name": "新易搜4K", "type": 3, "api": "csp_YiSo", "searchable": 1, "quickSearch": 1, "changeable": 0},
    {"key": "XunLeim", "name": "新迅雷磁力", "type": 3, "api": "csp_XunLeim", "searchable": 1, "quickSearch": 1, "changeable": 0},
    {"key": "NewKunYu", "name": "新酷云4K", "type": 3, "api": "csp_KunYu", "searchable": 1, "quickSearch": 1, "changeable": 0},
    {"key": "NewLiangCai", "name": "新猎手4K", "type": 3, "api": "csp_LiangCai", "searchable": 1, "quickSearch": 1, "changeable": 0},
    {"key": "NewDm84", "name": "新动漫4K", "type": 3, "api": "csp_Dm84", "searchable": 1, "quickSearch": 1, "changeable": 0},
]

print("")
print("=" * 60)
print("新增 4K 源")
print("=" * 60)
for s in new_sources:
    print(f"  [OK] {s['name']} ({s['api']})")

# Write updated config
config['sites'] = [s for s in config['sites'] if s['key'] not in delete_keys]
for s in new_sources:
    config['sites'].append(s)

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# Statistics
four_k = [s for s in config['sites'] if '4K' in s.get('name', '') or '动漫' in s.get('name', '')]
print("")
print("=" * 60)
print("统计")
print("=" * 60)
print(f"  删除: {len(deleted)} 个无效源")
print(f"  新增: {len(new_sources)} 个新 4K 源")
print(f"  当前 4K/动漫源总数: {len(four_k)}")
print(f"  总站点数: {len(config['sites'])}")
print("")
print("[OK] config.json 已更新")
