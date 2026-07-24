import json, requests

configs = ['https://raw.githubusercontent.com/qist/tvbox/master/0821.json']
with open('config.json', 'r', encoding='utf-8-sig') as f:
    current = json.load(f)
existing = {s.get('api') for s in current.get('sites', [])}

candidates = []
for url in configs:
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        data = r.json()
        for site in data.get('sites', []):
            if site.get('type') != 3 or 'ext' not in site:
                continue
            api = site.get('api', '')
            if api and api not in existing:
                candidates.append(site)

print('Total candidates:', len(candidates))

testable = []
for site in candidates:
    ext = site.get('ext')
    url = None
    if isinstance(ext, dict):
        if 'siteUrl' in ext: url = ext['siteUrl']
        elif 'host' in ext: url = ext['host']
        elif 'url' in ext: url = ext['url']
        elif 'site' in ext:
            sites = ext['site']
            if isinstance(sites, list) and sites: url = sites[0]
    if isinstance(ext, str) and ext.startswith('http'): url = ext
    
    if url:
        testable.append({'name': site.get('name',''), 'api': api, 'url': url, 'ext': ext})

print('Testable with URLs:', len(testable))

results = []
for item in testable:
    try:
        r = requests.get(item['url'], timeout=5)
        size_kb = len(r.content)/1024
        if 200 <= r.status_code < 400 and size_kb > 1:
            results.append({
                'name': item['name'].replace(' ','').strip(),
                'api': item['api'], 
                'size_kb': int(size_kb), 
                'ext': item['ext']
            })
            safe_name = item['name'][:15].encode('ascii', 'ignore').decode()
            print('[OK]', safe_name, '-', size_kb, 'KB')
    except:
        pass

results.sort(key=lambda x: x['size_kb'], reverse=True)
print('\nWorking sources:', len(results))

with open('verified_sources.json', 'w', encoding='utf-8') as f:
    json.dump(results[:10], f, ensure_ascii=False, indent=2)

print('[SAVED] Top 10 to verified_sources.json')

# Print detailed info
if results:
    print('\n=== TOP WORKING SOURCES ===')
    for i, r in enumerate(results[:8], 1):
        safe = r['name'].encode('ascii', 'ignore').decode()[:18]
        print(str(i) + '. ' + safe + ' | Size:' + str(r['size_kb']) + 'KB | API:' + r['api'][-25:])
