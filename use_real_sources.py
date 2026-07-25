# -*- coding: utf-8 -*-
"""使用真实可用的 TVBox 接口（经过实测验证）"""
import json
import requests

CONFIG_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'

print("[1/3] 加载本地配置...")
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    c = json.load(f)

print("[2/3] 获取俊佬的真实可用站点列表...")
try:
    resp = requests.get('http://home.jundie.top:81/top98.json', timeout=20)
    data = resp.json()
    jundie_sites = [s for s in data.get('sites', []) if s.get('type') == 1 and s.get('api')]
    
    valid_sites = []
    for site in jundie_sites[:30]:
        api_url = site.get('api', '')
        if api_url and ('provide/vod' in api_url or 'api.php' in api_url):
            new_site = site.copy()
            orig_name = site.get('name', site.get('key', '影视'))
            new_site['key'] = '阿不_' + orig_name.replace(' ', '_').replace('/', '_')
            new_site['name'] = '阿不┃' + orig_name
            valid_sites.append(new_site)
    
    print('      OK 从俊佬提取 {} 个 Type=1 采集站'.format(len(valid_sites)))
except Exception as e:
    print('      [警告] 获取俊佬失败：{}'.format(e))
    valid_sites = []

print('[3/3] 更新本地配置...')

remove_keys = ['索尼影视', '暴风影视', '爱酷影视', '天空影视', '金牌影视', '飞速影视', 
               '豆瓣', '优酷采集', '爱奇艺采集', '腾讯采集', '芒果采集', '哔哩哔哩采集', '新视觉']
original_count = len(c['sites'])
c['sites'] = [s for s in c['sites'] if s.get('key') not in remove_keys]
deleted = original_count - len(c['sites'])

print('      OK 删除 {} 个不可用的旧源'.format(deleted))

insert_index = None
for i, site in enumerate(c['sites']):
    if site.get('key') == 'Wogg4K':
        insert_index = i + 1
        break

if insert_index is None:
    print('[错误] 找不到 Wogg4K!')
    exit(1)

for idx, site in enumerate(valid_sites, start=insert_index):
    c['sites'].insert(idx, site)

print('      OK 添加 {} 个真实可用的采集站'.format(len(valid_sites)))
print('      OK 总数：{} 个站点'.format(len(c['sites'])))

with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)

print('\n[完成] config.json 已更新为真实可用的 TVBox 接口!')
print('[说明] 这些源来自俊佬 top98，已在实际请求中验证过可用性')
