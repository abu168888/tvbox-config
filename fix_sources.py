# -*- coding: utf-8 -*-
import json, os
BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

def load():
    with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save(c):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(c, f, indent=2, ensure_ascii=False)

c = load()

# 影视源修复 - 使用正确的API名称（匹配spider.jar中的类）
fixed_sites = [
    {"key": "zxzj", "name": "在线影视", "type": 3, "api": "csp_Zxzj", "timeout": 10, "playerType": 1, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://www.zxzjhd.com/"},
    {"key": "厂长", "name": "厂长影视", "type": 3, "api": "csp_NewCz", "timeout": 10, "playerType": 2, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "低端", "name": "低端影视", "type": 3, "api": "csp_Ddrk", "timeout": 10, "playerType": "2", "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "快看", "name": "快看影视", "type": 3, "api": "csp_Kkys", "timeout": 10, "playerType": 1, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "热播", "name": "热播影视", "type": 3, "api": "csp_AppTT", "timeout": 10, "playerType": 2, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "AO7TcBkd8I/B5wQc4Qma+pU="},
    {"key": "星星", "name": "星星影视", "type": 3, "api": "csp_Star", "timeout": 10, "playerType": 2, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "南瓜", "name": "南瓜影视", "type": 3, "api": "csp_NanGua", "timeout": 10, "playerType": 2, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "Auete", "name": "Auete影视", "type": 3, "api": "csp_Auete", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": "https://auete.pro/"},
    {"key": "泥巴", "name": "泥巴影视", "type": 3, "api": "csp_NiNi", "timeout": 10, "playerType": 2, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "6V", "name": "新6V磁力", "type": 3, "api": "csp_SixV", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 0, "ext": "https://www.xb6v.com/"},
    {"key": "比特", "name": "比特影视", "type": 3, "api": "csp_Bttwoo", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "文采", "name": "文采影视", "type": 3, "api": "csp_Jpys", "timeout": 10, "playerType": 2, "searchable": 1, "quickSearch": 1, "changeable": 1},
    {"key": "lib", "name": "立播影视", "type": 3, "api": "csp_Libvio", "timeout": 10, "searchable": 1, "quickSearch": 1, "changeable": 1, "ext": {"Cloud-drive": "tvfan/Cloud-drive.txt", "from": "4k|auto"}},
]

# 删除有问题的影视源
remove_keys = ['Bdys', 'NanGua', 'Kuaikan', 'NiNi', 'Star', 'ZhuiJu', 'TianTian', 'ChangZhang', 'TV3V', 'ReBoZJ', 'ShiPinSou', 'DaDaG', 'LiveNew']
c['sites'] = [s for s in c['sites'] if s.get('key') not in remove_keys]

# 添加修复后的影视源
for site in fixed_sites:
    if not any(s.get('key') == site['key'] for s in c['sites']):
        c['sites'].append(site)

# 直播源修复 - 统一playerType和URL格式
c['lives'] = [
    {"name": "初秋语•综合", "type": 0, "url": "https://raw.githubusercontent.com/fmz2000/quantv/main/g1.m3u", "playerType": 2, "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}", "logo": "https://live.fanmingming.com/tv/{name}.png"},
    {"name": "YanG•直播", "type": 0, "url": "https://tv.iill.top/m3u/Live", "playerType": 2, "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}"},
    {"name": "范明明•IPv6", "type": 0, "url": "https://live.fanmingming.com/tv/m3u/ipv6.m3u", "playerType": 2, "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}", "logo": "https://logo.wyfc.qzz.io/{name}.png"},
    {"name": "肥猫•综合", "type": 0, "url": "http://我不是.肥猫.live/TV/tvzb.txt", "playerType": 1, "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}", "logo": "https://logo.wyfc.qzz.io/{name}.png"},
    {"name": "Ray•综合", "type": 0, "url": "https://raw.githubusercontent.com/dxawi/0/main/tvlive.txt", "playerType": 1, "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}", "logo": "https://logo.wyfc.qzz.io/{name}.png"},
    {"name": "YueChan•综合", "type": 0, "url": "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u", "playerType": 1, "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}", "logo": "https://logo.wyfc.qzz.io/{name}.png"},
    {"name": "俊于•综合", "type": 0, "url": "http://home.jundie.top:81/Cat/tv/live.txt", "playerType": 1, "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}", "logo": "https://logo.wyfc.qzz.io/{name}.png"},
]

save(c)
print(f"Fixed {len(fixed_sites)} movie sources")
print(f"Fixed {len(c['lives'])} live sources")
print(f"Total sites: {len(c['sites'])}")
print(f"Total lives: {len(c['lives'])}")
