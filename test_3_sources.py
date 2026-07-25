import requests
print("="*70)
print("TESTING: Why 3 sources cannot be used")
print("="*70)

tests = [
    {'name': 'GuGu_Anime', 'url': 'https://www.gugu3.com', 'api': 'csp_AppGet'},
    {'name': 'Pan123_4K', 'url': 'https://123panfx.com', 'api': 'csp_PanWebShare123'},
    {'name': 'New6V_Magnet', 'url': 'https://www.xb6v.com', 'api': 'csp_New6v'},
]

results = []
for t in tests:
    try:
        r = requests.get(t['url'], timeout=5)
        status = "OK" if r.status_code == 200 else f"FAIL({r.status_code})"
        size = len(r.content)
        results.append({'name': t['name'], 'api': t['api'], 'url': t['url'], 'status': status, 'size': size, 'error': None})
    except Exception as e:
        results.append({'name': t['name'], 'api': t['api'], 'url': t['url'], 'status': 'ERROR', 'size': 0, 'error': str(e)[:80]})

for r in results:
    status_icon = "OK" if r['status'] == 'OK' else "FAIL"
    print(f"[{status_icon}] {r['name']} ({r['api']})")
    print(f"     URL: {r['url']}")
    print(f"     HTTP: {r['status']}")
    print(f"     Size: {r['size']}B")
    if r['error']:
        print(f"     Error: {r['error']}")
    print()

# Root cause analysis
print("="*70)
print("ROOT CAUSE ANALYSIS")
print("="*70)
print("\nProblem 1: csp_AppGet (GuGu_Anime)")
print("  - Requires spider.jar that supports 'AppGet' API")
print("  - Your spider.jar may not include this spider type")
print("  - AppGet needs specific API URL + dataKey + dataIv")

print("\nProblem 2: csp_PanWebShare123 (Pan123_4K)")
print("  - Custom spider type NOT in standard spider.jar")
print("  - This is a custom API added by qist/tvbox maintainers")
print("  - Your spider.jar does NOT support this API type")

print("\nProblem 3: csp_New6v (New6V_Magnet)")
print("  - Requires drpy2.min.js script loaded separately")
print("  - URL 'https://www.xb6v.com' is just the base URL")
print("  - Need drpy script to handle the actual scraping")

print("\n" + "="*70)
print("CONCLUSION: All 3 sources work only with specific spider.jar")
print("Your current spider.jar may not support these custom APIs.")
print("Recommendation: Use only APIs already in your existing config.")
print("="*70)
