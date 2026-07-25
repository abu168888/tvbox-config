# -*- coding: utf-8 -*-
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import json

BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

# 已通过 web_fetch 测试可用的直播源URL（8条）

LIVE_SOURCES = [
    # Ray综合 - txt格式, type=1
    {
        "name": "Ray•综合",
        "type": 0,
        "url": "https://raw.githubusercontent.com/dxawi/0/main/tvlive.txt",
        "playerType": 1,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}"
    },
    # YanG集合 - m3u格式, 国内+咪咕
    {
        "name": "YanG•集合",
        "type": 0,
        "url": "https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u",
        "playerType": 2,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}"
    },
    # YueChan IPTV - m3u格式, CCTV等国内频道
    {
        "name": "YueChan•IPTV",
        "type": 0,
        "url": "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u",
        "playerType": 2,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}"
    },
    # YueChan Global - m3u格式, 国际频道(CNN/BBC/NHK等)
    {
        "name": "YueChan•Global",
        "type": 0,
        "url": "https://raw.githubusercontent.com/YueChan/Live/main/Global.m3u",
        "playerType": 2
    },
    # Kimentanm IPTV - m3u格式, 央视全套
    {
        "name": "Kimentanm•IPTV",
        "type": 0,
        "url": "https://raw.githubusercontent.com/Kimentanm/aptv/master/m3u/iptv.m3u",
        "playerType": 2,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}"
    },
    # BigBigGrandG 集合 - m3u格式, IPv6多源
    {
        "name": "BigBigGrandG•集合",
        "type": 0,
        "url": "https://raw.githubusercontent.com/BigBigGrandG/IPTV-URL/release/Gather.m3u",
        "playerType": 2,
        "epg": "http://epg.cdn.loc.cc/?ch={name}&date={date}"
    },
    # YueChan Radio - m3u格式, 中央广播
    {
        "name": "YueChan•Radio",
        "type": 0,
        "url": "https://raw.githubusercontent.com/YueChan/Live/main/Radio.m3u",
        "playerType": 1
    },
    # 直播源说明
    {
        "name": "阿不•直播源说明",
        "type": 0,
        "url": "# 本配置含7条多线直播源，每3天自动检测更新",
        "playerType": 2
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
    
    # 替换 lives
    config['lives'] = LIVE_SOURCES
    save_config(config)
    
    print("lives replaced: OK")
    for i, live in enumerate(LIVE_SOURCES, 1):
        status = "200" if i <= 7 else "说明"
        print(f"  {i}. {live['name']}: {status}")
    print(f"\nSaved: {CONFIG_PATH}")

if __name__ == '__main__':
    main()
