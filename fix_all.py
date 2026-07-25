# -*- coding: utf-8 -*-
import json
import os

BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

# 修复影视站 - 使用经过qist验证的API名称
# 格式：标准爬虫名称 + 正确ext参数

MOVIE_SITES_FIX = [
    # 在线影视（经过验证）
    {
        "key": "zxzj",
        "name": "🍊在线┃影视",
        "type": 3,
        "api": "csp_ZxzjGuard",
        "timeout": 10,
        "playerType": 1,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://www.zxzjhd.com/"
    },
    {
        "key": "厂长",
        "name": "📔厂长┃不卡",
        "type": 3,
        "api": "csp_NewCzGuard",
        "timeout": 10,
        "playerType": 2,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1
    },
    {
        "key": "低端",
        "name": "⏮️低端┃外剧",
        "type": 3,
        "api": "csp_DdrkGuard",
        "timeout": 10,
        "playerType": "2",
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1
    },
    {
        "key": "糯米",
        "name": "🍓糯米┃秒播",
        "type": 3,
        "api": "csp_NmyswvGuard",
        "timeout": 10,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1
    },
    {
        "key": "白白",
        "name": "🐟白白┃秒播",
        "type": 3,
        "api": "csp_SbaibaiGuard",
        "timeout": 10,
        "playerType": 2,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1
    },
    {
        "key": "文采",
        "name": "💮文采┃秒播",
        "type": 3,
        "api": "csp_JpysGuard",
        "timeout": 10,
        "playerType": 2,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1
    },
    {
        "key": "快看",
        "name": "👀快看┃影视",
        "type": 3,
        "api": "csp_Kuaikan",
        "timeout": 10,
        "searchable": 1,
        "quickSearch": 1,
        "filterable": 1,
        "changeable": 1
    },
    {
        "key": "热播",
        "name": "📺热播┃多线",
        "type": 3,
        "api": "csp_AppTTGuard",
        "timeout": 10,
        "playerType": 2,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "uqGL1bNENExT7/hGxpSE5qU="
    },
    {
        "key": "欢视",
        "name": "👓欢视┃多线",
        "type": 3,
        "api": "csp_AppTTGuard",
        "timeout": 10,
        "playerType": 2,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "uqGL1bNENExT9fFAy5mE5qU="
    },
    {
        "key": "OT",
        "name": "🏝奥特┃多线",
        "type": 3,
        "api": "csp_AueteGuard",
        "timeout": 10,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": "https://auete.com/"
    },
    {
        "key": "比特",
        "name": "🍄比特┃手机",
        "type": 3,
        "api": "csp_BttwooGuard",
        "timeout": 10,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1
    },
    {
        "key": "lib",
        "name": "🌟立播┃秒播",
        "type": 3,
        "api": "csp_LibvioGuard",
        "timeout": 10,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 1,
        "ext": {"Cloud-drive": "tvfan/Cloud-drive.txt", "from": "4k|auto"}
    },
]

# 修复直播源 - 使用经过验证的URL格式
LIVE_SOURCES_FIX = [
    {
        "name": "初秋语•ipv4",
        "type": 0,
        "url": "https://github.moeyy.xyz/https://raw.githubusercontent.com/fmz2000/quantv/main/g1.m3u",
        "playerType": 2,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}",
        "logo": "https://live.fanmingming.com/tv/{name}.png"
    },
    {
        "name": "YanG•综合",
        "type": 0,
        "url": "https://tv.iill.top/m3u/Gather",
        "ua": "okhttp/3.15",
        "playerType": 2,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}"
    },
    {
        "name": "YanG•直播",
        "type": 0,
        "url": "https://tv.iill.top/m3u/Live",
        "ua": "okhttp/3.15",
        "playerType": 2
    },
    {
        "name": "范明明•ipv6",
        "type": 0,
        "url": "https://live.fanmingming.com/tv/m3u/ipv6.m3u",
        "playerType": 2,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}",
        "logo": "https://logo.wyfc.qzz.io/{name}.png"
    },
    {
        "name": "YueChan•综合",
        "type": 0,
        "url": "https://github.moeyy.xyz/https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u",
        "playerType": 1,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}",
        "logo": "https://logo.wyfc.qzz.io/{name}.png"
    },
    {
        "name": "肥猫•综合",
        "type": 0,
        "url": "http://我不是.肥猫.live/TV/tvzb.txt",
        "playerType": 1,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}",
        "logo": "https://logo.wyfc.qzz.io/{name}.png"
    },
    {
        "name": "Ray•综合",
        "type": 0,
        "url": "https://github.moeyy.xyz/https://raw.githubusercontent.com/dxawi/0/main/tvlive.txt",
        "playerType": 1,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}",
        "logo": "https://logo.wyfc.qzz.io/{name}.png"
    },
    {
        "name": "俊于•综合",
        "type": 0,
        "url": "http://home.jundie.top:81/Cat/tv/live.txt",
        "playerType": 1,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}",
        "logo": "https://logo.wyfc.qzz.io/{name}.png"
    },
]

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def main():
    config = load_config()
    
    # 1. 删除有问题的影视站（Bdys, NanGua, Kuaikan, NiNi, Star等）
    remove_keys = ['Bdys', 'NanGua', 'Kuaikan', 'NiNi', 'Star', 'ZhuiJu', 'TianTian', 'ChangZhang', 'TV3V', 'ReBoZJ', 'ShiPinSou', 'DaDaG', 'LiveNew']
    config['sites'] = [s for s in config['sites'] if s.get('key') not in remove_keys]
    print(f"Removed {len(remove_keys)} invalid movie sources")
    
    # 2. 添加修复后的影视站
    for site in MOVIE_SITES_FIX:
        config['sites'].append(site)
    print(f"Added {len(MOVIE_SITES_FIX)} verified movie sources")
    
    # 3. 替换直播源
    config['lives'] = LIVE_SOURCES_FIX
    print(f"Replaced lives: {len(LIVE_SOURCES_FIX)} sources")
    
    save_config(config)
    print(f"Total sites: {len(config['sites'])}")
    print(f"Total lives: {len(config['lives'])}")

if __name__ == '__main__':
    main()
