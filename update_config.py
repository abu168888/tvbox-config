# -*- coding: utf-8 -*-
import io, os, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

# 影视站配置（12个）
MOVIE_SITES = [
    # 哔滴影视
    {"key": "Bdys", "name": "哔滴影视", "type": 3, "api": "csp_Bdys01", "searchable": 1, "quickSearch": 1, "filterable": 1, "changeable": 1, "timeout": 30},
    # 南瓜影视
    {"key": "NanGua", "name": "南瓜影视", "type": 3, "api": "csp_NanGua", "searchable": 1, "changeable": 1, "timeout": 30},
    # 快看影视
    {"key": "Kuaikan", "name": "快看影视", "type": 3, "api": "csp_Kuaikan", "searchable": 1, "quickSearch": 1, "filterable": 1, "changeable": 1, "timeout": 30},
    # 泥巴影视
    {"key": "NiNi", "name": "泥巴影视", "type": 3, "api": "csp_NiNi", "searchable": 1, "changeable": 1, "timeout": 60},
    # 星星影视
    {"key": "Star", "name": "星星影视", "type": 3, "api": "csp_Star", "searchable": 1, "changeable": 1, "timeout": 30},
    # 追剧影视
    {"key": "ZhuiJu", "name": "追剧影视", "type": 3, "api": "csp_TTian", "ext": "http://app.kzjtv.com$$$null$$$1", "searchable": 1, "changeable": 1, "timeout": 30},
    # 天天影视
    {"key": "TianTian", "name": "天天影视", "type": 3, "api": "csp_TTian", "ext": "http://op.ysdqjs.cn$$$null$$$1", "searchable": 1, "changeable": 1, "timeout": 30},
    # 厂长影视
    {"key": "ChangZhang", "name": "厂长影视", "type": 3, "api": "csp_DiDuan", "searchable": 1, "quickSearch": 1, "filterable": 1, "changeable": 0, "timeout": 60},
    # 电视猫
    {"key": "TV3V", "name": "电视猫", "type": 3, "api": "csp_TianShi", "searchable": 1, "changeable": 0, "timeout": 30},
    # 热播之家
    {"key": "ReBoZJ", "name": "热播之家", "type": 3, "api": "csp_TTian", "ext": "http://app.kzjtv.com$$$null$$$1", "searchable": 1, "changeable": 1, "timeout": 30},
    # 视频搜
    {"key": "ShiPinSou", "name": "视频搜", "type": 3, "api": "csp_Shapi", "searchable": 1, "quickSearch": 1, "filterable": 1, "changeable": 0, "timeout": 60},
    # 达达龟
    {"key": "DaDaG", "name": "达达龟", "type": 3, "api": "csp_DadaG", "searchable": 1, "quickSearch": 1, "filterable": 1, "changeable": 0, "timeout": 60},
]

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def main():
    config = load_config()
    
    # 1. 修复 wallpaper URL (改为 qist 标准的 https)
    config['wallpaper'] = 'https://jianbian.chuqiuyu.workers.dev'
    print('wallpaper: fixed')
    
    # 2. 添加影视站
    added = []
    for site in MOVIE_SITES:
        key = site.get('key', '')
        name = site.get('name', '')
        
        # 检查是否已存在
        existing = [s for s in config['sites'] if s.get('key') == key]
        if existing:
            print(f'  SKIP: {name} (duplicate)')
            continue
        
        config['sites'].append(site)
        added.append(name)
    
    print(f'Added {len(added)} movie sources:')
    for name in added:
        print(f'  OK: {name}')
    
    save_config(config)
    print(f'Total sites: {len(config["sites"])}')
    print(f'Total lives: {len(config["lives"])}')

if __name__ == '__main__':
    main()
