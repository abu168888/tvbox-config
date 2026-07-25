import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

config_path = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'

with open(config_path, 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

# 要删除的源 - 按用户要求的类别
delete_keys = [
    # 动漫类 (4个)
    'AnimeFanShu',      # 🤡番薯┃动漫🤡
    'AnimeMiaoWuGuard', # 🤡喵呜┃动漫🤡
    'AnimeHuaziGuard',  # 🤡花海┃动漫🤡
    'AnimeMoDu',        # 🤡魔都┃动漫🤡
    
    # B站教育类 (7个)
    'bilibiliys',       # 🅱️哔哩┃影视🅱️
    'bilibili',         # 🅱️哔哩┃合集🅱️
    'biliych',          # 🅱️哔哩┃歌曲🅱️
    '少儿教育',         # 📚少儿┃教育📚
    '小学课堂',         # 📚小学┃课堂📚
    '初中课堂',         # 📚初中┃课堂📚
    '高中教育',         # 📚高中┃课堂📚
    
    # 音乐儿歌类 (7个)
    'ChildrenDuoDuo',   # 👼多多┃儿歌👼
    'ChildrenBaoBao',   # 👼宝宝┃儿歌👼
    'ChildrenBeiWa',    # 👼贝贝┃儿歌👼
    'ChildrenTuTu',     # 👼兔兔┃儿歌👼
    'WexTangDou',       # 💃跳舞┃教学💃
    'MusicLiYuan',      # 🎎戏曲┃秒播🎎
    'MusicQingTing',    # 🎼蜻蜓┃电台🎼
    'MusicIKtv',        # 🎼KTV┃音乐🎼
    'Music163',         # 🎼易听┃音乐🎼
    'MusicKuWo',        # 🎼酷听┃音乐🎼
    'MusicLunHui',      # 🎼轮回┃舞曲🎼
    
    # B站戏曲
    'bilixiqu',         # 🅱️哔哩┃戏曲🅱️
    
    # 其他分类
    'SoHaiYin',         # 🎠海音┃综合🎠
    'So97So',           # 🎠九七┃综合🎠
    'emby',             # 🀄️emby┃4K🀄️
    
    # 网盘搜索
    'SoTySo',           # 🎠给力┃天逸🎠
    'SoBaiDuSo',        # 🎠给力┃百度🎠
]

deleted = []
remaining = []
for s in config['sites']:
    if s['key'] in delete_keys:
        deleted.append(s)
        print(f"  [X] 删除: {s['name']} ({s['api']})")
    else:
        remaining.append(s)

config['sites'] = remaining

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"\n已删除: {len(deleted)} 个源")
print(f"剩余: {len(config['sites'])} 个源")
print(f"config.json 已更新")
