# -*- coding: utf-8 -*-
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import json

BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

MOVIE_SITES = [
    {'key': 'Bdys', 'name': '哔滴影视', 'type': 3, 'api': 'csp_Bdys01', 'searchable': 1, 'quickSearch': 1, 'filterable': 1, 'changeable': 1, 'timeout': 30},
    {'key': 'NanGua', 'name': '南瓜影视', 'type': 3, 'api': 'csp_NanGua', 'searchable': 1, 'changeable': 1, 'timeout': 30},
    {'key': 'Kuaikan', 'name': '快看影视', 'type': 3, 'api': 'csp_Kuaikan', 'searchable': 1, 'quickSearch': 1, 'filterable': 1, 'changeable': 1, 'timeout': 30},
    {'key': 'NiNi', 'name': '泥巴影视', 'type': 3, 'api': 'csp_NiNi', 'searchable': 1, 'changeable': 1, 'timeout': 60},
    {'key': 'Star', 'name': '星星影视', 'type': 3, 'api': 'csp_Star', 'searchable': 1, 'changeable': 1, 'timeout': 30},
    {'key': 'ZhuiJu', 'name': '追剧影视', 'type': 3, 'api': 'csp_TTian', 'ext': 'http://app.kzjtv.com$$$null$$$1', 'searchable': 1, 'changeable': 1, 'timeout': 30},
    {'key': 'TianTian', 'name': '天天影视', 'type': 3, 'api': 'csp_TTian', 'ext': 'http://op.ysdqjs.cn$$$null$$$1', 'searchable': 1, 'changeable': 1, 'timeout': 30},
    {'key': 'ChangZhang', 'name': '厂长影视', 'type': 3, 'api': 'csp_DiDuan', 'searchable': 1, 'quickSearch': 1, 'filterable': 1, 'changeable': 0, 'timeout': 60},
    {'key': 'TV3V', 'name': '电视猫', 'type': 3, 'api': 'csp_TianShi', 'searchable': 1, 'changeable': 0, 'timeout': 30},
    {'key': 'ReBoZJ', 'name': '热播之家', 'type': 3, 'api': 'csp_TTian', 'ext': 'http://app.kzjtv.com$$$null$$$1', 'searchable': 1, 'changeable': 1, 'timeout': 30},
    {'key': 'ShiPinSou', 'name': '视频搜', 'type': 3, 'api': 'csp_Shapi', 'searchable': 1, 'quickSearch': 1, 'filterable': 1, 'changeable': 0, 'timeout': 60},
    {'key': 'DaDaG', 'name': '达达龟', 'type': 3, 'api': 'csp_DadaG', 'searchable': 1, 'quickSearch': 1, 'filterable': 1, 'changeable': 0, 'timeout': 60},
]

LIVE_SOURCES = [
    {'name': '初秋语综合', 'type': 0, 'url': 'https://raw.githubusercontent.com/fmz2000/quantv/main/g1.m3u', 'playerType': 2, 'epg': 'http://epg.cdn.loc.cc/?ch={name}&date={date}', 'logo': 'https://raw.githubusercontent.com/fmz2000/quantv/main/logo/{name}.png'},
    {'name': '范明明IPv4', 'type': 0, 'url': 'https://raw.githubusercontent.com/fanmingming/main/master/tv/m3u/ipv4.m3u', 'playerType': 2, 'epg': 'http://epg.cdn.loc.cc/?ch={name}&date={date}', 'logo': 'https://raw.githubusercontent.com/fanmingming/main/master/tv/logo/{name}.png'},
    {'name': '肥猫综合', 'type': 0, 'url': 'http://我不是.肥猫.live/TV/tvzb.txt', 'playerType': 1, 'epg': 'http://epg.cdn.loc.cc/?ch={name}&date={date}', 'logo': 'https://live.fanmingming.com/tv/{name}.png'},
    {'name': 'YanG直播', 'type': 0, 'url': 'https://tv.iill.top/m3u/Live', 'playerType': 2, 'logo': 'https://tv.iill.top/logo/{name}.png'},
    {'name': 'Ray综合', 'type': 0, 'url': 'https://raw.githubusercontent.com/dxawi/0/main/tvlive.txt', 'playerType': 1, 'epg': 'http://epg.cdn.loc.cc/?ch={name}&date={date}', 'logo': 'https://raw.githubusercontent.com/dxawi/0/main/logo/{name}.png'},
    {'name': '多多直播', 'type': 0, 'url': 'https://raw.githubusercontent.com/ddxxxx520/tv/main/tv.m3u', 'playerType': 2, 'logo': 'https://raw.githubusercontent.com/ddxxxx520/tv/main/logo/{name}.png'},
    {'name': '南风综合', 'type': 0, 'url': 'https://raw.githubusercontent.com/Fanlingou/FLG/main/TVBox/南风电视直播.txt', 'playerType': 1, 'epg': 'http://epg.cdn.loc.cc/?ch={name}&date={date}'},
]

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def add_movie_sites(config):
    added = []
    for site in MOVIE_SITES:
        key = site.get('key', '')
        name = site.get('name', '')
        existing = [s for s in config['sites'] if s.get('key') == key]
        if existing:
            print(f"  [SKIP] {name} (duplicate key)")
            continue
        config['sites'].append(site)
        added.append(name)
        print(f"  [OK]   {name}")
    print(f"\n  Added {len(added)} movie sources")
    return config

def replace_lives(config):
    if 'lives' in config:
        old_lives = [l.get('name', '') for l in config['lives']]
        config['lives'] = []
        print(f"\n  Removed old lives: {old_lives}")
    for live in LIVE_SOURCES:
        config['lives'].append(live)
        print(f"  [OK]   {live.get('name', '')}")
    print(f"\n  Added {len(LIVE_SOURCES)} live sources")
    return config

def main():
    config = load_config()
    print(f"Current sites: {len(config['sites'])}")
    print(f"Current lives: {len(config.get('lives', []))}")
    
    config = add_movie_sites(config)
    config = replace_lives(config)
    
    save_config(config)
    print(f"\nTotal sites: {len(config['sites'])}")
    print(f"Total lives: {len(config['lives'])}")
    print(f"Saved: {CONFIG_PATH}")

if __name__ == '__main__':
    main()
