import json

with open('config.json', 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

sites = config.get('sites', [])
print(f"Total sites: {len(sites)}\n")

type3 = [s for s in sites if s.get('type') == 3]
print(f"Type=3 sites: {len(type3)}\n")

# List all 4K/cloud related
print("=== 4K/CLOUD SITES ===")
for s in type3:
    name = s.get('name', '')
    api = s.get('api', '')
    if '4K' in name or 'Wogg' in api or 'PanWebShare' in api or 'Zhinan' in api or '4K' in api:
        print(f"{name} | {api}")

# List all "秒播" sites  
print("\n=== 秒播 SITES ===")
for s in type3:
    name = s.get('name', '')
    api = s.get('api', '')
    if '秒播' in name:
        has_ext = 'ext' in s
        print(f"{name} | {api} | ext:{has_ext}")
