# Comprehensive source finder and tester
import json
import requests

print("="*70)
print("STEP 1: Fetch ALL type=3 sites from qist/tvbox")
print("="*70)

configs_to_fetch = [
    "https://raw.githubusercontent.com/qist/tvbox/master/0821.json",
    "https://raw.githubusercontent.com/qvqst/tvbox/master/jsm.json",
]

all_candidates = []
existing_apis = set()

# Load current config to exclude duplicates
with open('config.json', 'r', encoding='utf-8-sig') as f:
    current = json.load(f)
    existing_apis = {s.get('api') for s in current.get('sites', [])}
print(f"Existing APIs: {len(existing_apis)}\n")

# Fetch from multiple sources
for cfg_url in configs_to_fetch:
    try:
        r = requests.get(cfg_url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for site in data.get('sites', []):
                if site.get('type') != 3:
                    continue
                api = site.get('api', '')
                if not api or api in existing_apis:
                    continue
                # Must have ext field
                if 'ext' not in site:
                    continue
                all_candidates.append(site)
            print(f"[OK] Fetched from {cfg_url.split('/')[-2:][-1]}")
    except Exception as e:
        print(f"[FAIL] {cfg_url}: {str(e)[:30]}")

print(f"\nTotal candidates (excludes existing): {len(all_candidates)}\n")

# Extract URLs for testing
print("="*70)
print("STEP 2: Extract testable URLs from ext fields")
print("="*70)

testable = []
for site in all_candidates:
    name = site.get('name', '')[:20].replace(' ', '')
    api = site.get('api', '')
    ext = site.get('ext')
    
    url = None
    if isinstance(ext, str):
        if ext.startswith('http'):
            url = ext
    elif isinstance(ext, dict):
        if 'siteUrl' in ext and ext['siteUrl']:
            url = ext['siteUrl']
        elif 'host' in ext and ext['host']:
            url = ext['host']
        elif 'url' in ext and ext['url']:
            url = ext['url']
        elif 'site' in ext:
            sites_list = ext['site']
            if isinstance(sites_list, list) and len(sites_list) > 0:
                url = sites_list[0]
            elif isinstance(sites_list, str):
                url = sites_list
    
    if url:
        testable.append({
            'name': name,
            'api': api,
            'url': url,
            'ext': ext
        })

print(f"Testable with URLs: {len(testable)}\n")

# Test each URL
print("="*70)
print("STEP 3: HTTP Reachability Test (timeout=5s)")
print("="*70)

results = []
for item in testable:
    try:
        r = requests.get(item['url'], timeout=5, allow_redirects=True)
        size_kb = len(r.content) / 1024
        if 200 <= r.status_code < 400 and size_kb > 1:  # At least 1KB content
            status = "PASS"
            results.append({'name': item['name'], 'api': item['api'], 'score': int(size_kb), 'ext': item['ext']})
        else:
            status = f"SKIP({size_kb:.1f}KB)"
    except Exception as e:
        status = "FAIL"
    
    print(f"[{status}] {item['name']} | {item['url'][:40]}")

# Sort by content size (larger = more likely working)
results.sort(key=lambda x: x['score'], reverse=True)

print("\n" + "="*70)
print("TOP RESULTS (sorted by content size)")
print("="*70)

for i, r in enumerate(results[:15], 1):
    print(f"{i}. {r['name']:<20} | API:{r['api'][-25:]:<25} | Size:{r['score']}KB")

# Save best ones to file for later use
if results:
    top_10 = results[:10]
    with open('best_sources.json', 'w', encoding='utf-8') as f:
        json.dump(top_10, f, ensure_ascii=False, indent=2)
    print(f"\n[SAVED] Top {len(top_10)} sources saved to best_sources.json")

print("\nTEST COMPLETE - Ready for human review")
