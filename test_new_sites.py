# -*- coding: utf-8 -*-
"""测试新增的 8 个秒播源是否真实可用"""
import json
import requests
from datetime import datetime

def test_site_api(api_name):
    """测试 API 的实际可用性 - 这里只能测试 spider.jar 能否加载该 API"""
    # 由于 type=3 需要 spider.jar 才能运行，我们无法直接测试 API
    # 但可以检查这些 API 在 qist 仓库中是否真的被使用
    
    test_urls = {
        '厂长': 'https://www.cz02.net',
        '糯米': 'https://nmhd.tv',
        '白白': 'https://sbaibai.com',
        '文采': 'https://www.jpys.top',
        '神车': 'https://appsk.app',
        '立播': 'https://libvio.me',
        '在线': 'https://zxzj.pro'
    }
    
    name = api_name.split('┃')[0].replace('💡', '')
    if name not in test_urls:
        return None
    
    try:
        response = requests.get(test_urls[name], timeout=5)
        return {
            'name': name,
            'url': test_urls[name],
            'status_code': response.status_code,
            'is_reachable': 200 <= response.status_code < 400,
            'response_size': len(response.content)
        }
    except Exception as e:
        return {
            'name': name,
            'error': str(e)[:50],
            'is_reachable': False
        }

print("测试新增站点对应的源网站是否可访问:")
print("=" * 60)

sites_to_test = ['厂长', '糯米', '白白', '文采', '神车', '立播', '在线']
results = []

for site in sites_to_test:
    result = test_site_api(site)
    if result:
        status = "OK" if result.get('is_reachable') else "FAIL"
        print(f"[{status}] {result['name']}: {result.get('status_code', 'N/A')} - {result.get('response_size', 'N/A')} bytes")
        results.append(result)

print("=" * 60)

# 同时检查这些 API 是否在 qist 的主配置中真实存在
print("\n检查这些 API 是否在 qist/tvbox 主配置中:")
try:
    config_0821 = requests.get('https://raw.githubusercontent.com/qist/tvbox/master/0821.json', timeout=10).json()
    apis_in_qist = {site.get('api') for site in config_0821.get('sites', [])}
    
    our_apis = [
        'csp_NewCzGuard',      # 厂长
        'csp_NmyswvGuard',     # 糯米
        'csp_SbaibaiGuard',    # 白白
        'csp_JpysGuard',       # 文采
        'csp_AppSKGuard',      # 神车
        'csp_LibvioGuard',     # 立播
        'csp_ZxzjGuard'        # 在线
    ]
    
    for api in our_apis:
        exists = api in apis_in_qist
        status = "存在" if exists else "不存在"
        print(f"[{status}] {api}")
except Exception as e:
    print(f"无法获取 qist 配置：{e}")
