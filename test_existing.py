# Test current config sites that ARE WORKING
import json
import requests

print("="*70)
print("TEST CURRENT CONFIG - FIND ACTUALLY WORKING SITES")
print("="*70)

with open('config.json', 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

sites = config.get('sites', [])

# Filter for type=3 with ext (云盘/爬虫类)
cloud_sites = []
for s in sites:
    if s.get('type') == 3 and 'ext' in s:
        ext = s.get('ext')
        if isinstance(ext, dict):
            site_url = ext.get('site', [])
            if isinstance(site_url, list) and len(site_url) > 0:
                cloud_sites.append({
                    'name': s['name'],
                    'api': s['api'],
                    'url': site_url[0]
                })

print(f"\nFound {len(cloud_sites)} cloud-drive sites to test\n")

print("Testing URLs...")
print("-"*70)

for item in cloud_sites[:15]:
    try:
        r = requests.get(item['url'], timeout=3)
        status = "OK" if 200 <= r.status_code < 400 else f"FAIL"
        print(f"[{status}] {item['name'][:15]:<15} - {len(r.content)}B")
    except:
        print(f"[FAIL] {item['name'][:15]}")

print("\n" + "="*70)
