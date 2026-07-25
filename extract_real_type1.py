# -*- coding: utf-8 -*-
"""从俊佬的真实配置中提取 Type=1 接口并验证"""
import requests
import json

print("正在从俊佬配置提取 Type=1 接口...")

try:
    resp = requests.get('http://home.jundie.top:81/top98.json', timeout=20)
    data = resp.json()
    
    # 提取所有 type=1 且有 api 字段的站点
    type1_sites = []
    for site in data.get('sites', []):
        if site.get('type') == 1 and site.get('api'):
            api = site.get('api')
            # 只保留标准 vod api
            if 'provide/vod' in api or 'api.php' in api:
                type1_sites.append(site)
    
    print("找到 {} 个 Type=1 接口".format(len(type1_sites)))
    
    # 取前 10 个进行测试
    test_sites = type1_sites[:10]
    print("\n开始验证可用性...")
    
    valid_sites = []
    for site in test_sites:
        name = site.get('name', site.get('key', '未知'))
        api = site.get('api', '')
        
        # 添加 ac=list 参数
        test_url = api + ('&ac=list' if '?' in api else '?ac=list')
        
        try:
            r = requests.get(test_url, timeout=10)
            if r.status_code == 200:
                try:
                    d = r.json()
                    count = 0
                    if isinstance(d, dict):
                        count = len(d.get('list', []))
                    elif isinstance(d, list):
                        count = len(d)
                    
                    if count > 0:
                        print("[OK] {}: {}条数据".format(name, count))
                        # 改名避免冲突
                        new_site = site.copy()
                        new_site['key'] = '阿不_' + site.get('key', name).replace('/', '_').replace(' ', '_')
                        new_site['name'] = '阿不┃' + name
                        valid_sites.append(new_site)
                    else:
                        print("[X] {}: 无数据".format(name))
                except:
                    print("[X] {}: JSON 解析失败".format(name))
            else:
                print("[X] {}: HTTP{}".format(name, r.status_code))
        except Exception as e:
            print("[X] {}: {}".format(name, str(e)[:30]))
    
    print("\n=== 验证结果 ===")
    print("有效接口：{}/{}".format(len(valid_sites), len(test_sites)))
    
    if len(valid_sites) > 0:
        # 保存到文件供后续使用
        with open('valid_type1_sites.json', 'w', encoding='utf-8') as f:
            json.dump(valid_sites, f, indent=2, ensure_ascii=False)
        print("已保存 {} 个有效接口到 valid_type1_sites.json".format(len(valid_sites)))
    
except Exception as e:
    print("错误：{}".format(e))
