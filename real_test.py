# -*- coding: utf-8 -*-
"""真实测试新增站点是否可用 - END TO END"""
import requests
import json

print("="*70)
print("REAL END-TO-END TEST FOR NEW SOURCES")
print("="*70)

# The 8 "fixed" sites from earlier
sites_to_test = [
    {"name": "厂长", "api": "csp_NewCzGuard", "url": "https://cz02.net"},
    {"name": "糯米", "api": "csp_NmyswvGuard", "url": "https://nmhd.tv"},
    {"name": "白白", "api": "csp_SbaibaiGuard", "url": "https://sbaibai.com"},
    {"name": "文采", "api": "csp_JpysGuard", "url": "https://www.jpys.top"},
    {"name": "神车", "api": "csp_AppSKGuard", "url": "https://appsk.app"},
    {"name": "立播", "api": "csp_LibvioGuard", "url": "https://libvio.me"},
    {"name": "在线", "api": "csp_ZxzjGuard", "url": "https://zxzj.pro"},
]

print("\nTest 1: Website Reachability (HTTP Status)")
print("-"*70)

for site in sites_to_test:
    try:
        r = requests.get(site['url'], timeout=5, allow_redirects=True)
        status = "OK" if 200 <= r.status_code < 400 else f"FAIL({r.status_code})"
        print(f"[{status}] {site['name']}: {site['url']} - {len(r.content)} bytes")
    except Exception as e:
        print(f"[FAIL] {site['name']}: {str(e)[:40]}")

# Test 2: Check if APIs actually exist in real-world configs
print("\n\nTest 2: API Presence in Active Configs")
print("-"*70)

try:
    # Fetch current qist 0821.json to verify APIs are STILL THERE
    qist_api_list = []
    response = requests.get('https://raw.githubusercontent.com/qist/tvbox/master/0821.json', timeout=10)
    if response.status_code == 200:
        config = response.json()
        current_apis = {s.get('api') for s in config.get('sites', [])}
        
        for site in sites_to_test:
            api = site['api']
            exists = api in current_apis
            status = "ACTIVE" if exists else "REMOVED"
            print(f"[{status}] {site['name']} ({api})")
except Exception as e:
    print(f"Cannot fetch qist config: {e}")

print("\n\nTest 3: Wogg/KouSou/YouXi (New Candidates)")
print("-"*70)

new_cands = [
    {"name": "Wogg 4K Danmu", "api": "csp_WoGGGuard", "url": "https://www.wogg.com"},
    {"name": "KouSou PanSearch", "api": "csp_KkSsGuard", "url": "https://kkss.kkss.one"},
    {"name": "YouXi PanSearch", "api": "csp_UuSsGuard", "url": "https://uxsearch.xyz"}
]

for cand in new_cands:
    try:
        r = requests.get(cand['url'], timeout=5)
        status = "OK" if 200 <= r.status_code < 400 else f"FAIL({r.status_code})"
        print(f"[{status}] {cand['name']}: {cand['url']} - {len(r.content)} bytes")
    except Exception as e:
        print(f"[FAIL] {cand['name']}: {str(e)[:40]}")

print("\n" + "="*70)
print("TEST COMPLETE - Waiting for human review before any action")
print("="*70)
