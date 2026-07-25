# -*- coding: utf-8 -*-
import requests

apis = [
    ("优酷", "https://api.ikfans.top/api.php/provide/vod/?ac=list"),
    ("爱奇艺", "https://aixi.lvdou.pro/api.php/provide/vod/?ac=list"),
    ("腾讯", "https://tx.lvdou.pro/api.php/provide/vod/?ac=list"),
    ("芒果", "https://mg.lvdou.pro/api.php/provide/vod/?ac=list"),
    ("搜狐", "https://sohu.lvdou.pro/api.php/provide/vod/?ac=list"),
    ("PTTV", "https://api.pttvy.com/api.php/provide/vod/?ac=list")
]

for name, url in apis:
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            count = len(data.get('list', data) if isinstance(data, dict) else data)
            print("[OK] {}: {}条数据".format(name, count))
        else:
            print("[X] {}: HTTP{}".format(name, r.status_code))
    except Exception as e:
        print("[X] {}: {}".format(name, str(e)[:40]))
