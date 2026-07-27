import json

with open('config_cleaned.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

sites = config['sites']

# 需要修复的网盘源：添加 ext 参数
pan_fixes = {
    'WexWoquark': {  # 夸克
        'changeable': 1,
        'timeout': 50,
        'ext': 'https://阿布自有域名/quark_token.txt'
    },
    'WexWoBaidu': {  # 百度
        'changeable': 1,
        'timeout': 50,
        'ext': 'https://阿布自有域名/baidu_token.txt'
    },
    'Wex115share': {  # 115
        'changeable': 1,
        'timeout': 50,
        'ext': ''
    },
    'WexWo189': {  # 天翼
        'changeable': 1,
        'timeout': 50,
        'ext': ''
    },
    'WexWo123': {  # 123
        'changeable': 1,
        'timeout': 50,
        'ext': ''
    },
    'WexXunLei': {  # 讯雷
        'changeable': 1,
        'timeout': 50,
        'ext': ''
    },
}

print("Fixing cloud sources:")
for s in sites:
    key = s['key']
    if key in pan_fixes:
        print("  %s | %s" % (key, s.get('name', '')))
        for k, v in pan_fixes[key].items():
            s[k] = v

# 保存
config['sites'] = sites
with open('config_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("\nFixed %d sources" % len(pan_fixes))
print("Saved to config_fixed.json")
