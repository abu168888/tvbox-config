import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

with open(r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json', 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

sites = config['sites']
total = len(sites)

print(f"{'='*60}")
print(f"阿不 TVBox 配置 - 所有源列表 (共 {total} 个)")
print(f"{'='*60}")

# 分类统计
categories = {}
for i, s in enumerate(sites, 1):
    name = s.get('name', '')
    api = s.get('api', '')
    key = s.get('key', '')
    
    # 分类
    if '秒播' in name or 'GuZi' in api or 'JianPian' in api or 'WenCai' in api or 'DuBoKu' in api or 'YueYue' in api or 'DaShiXiong' in api or 'TeGou' in api or 'YiYs' in api or 'ReBo' in api or 'BoBo' in api or 'IkanBot' in api:
        cat = '秒播影视'
    elif '4K' in name or '新盘搜' in name or '新易搜' in name or '新酷云' in name or '新猎手' in name or '盘搜' in name or '易搜' in name or '玩偶' in name or '至臻' in name or '观影' in name or '剧透' in name or '虎斑' in name or '木偶' in name or '多多' in name or '原盘' in name or '123' in name:
        cat = '4K网盘'
    elif '动漫' in name or 'Anime' in name or '番薯' in name or '喵呜' in name or '花海' in name or '魔都' in name:
        cat = '动漫'
    elif '短剧' in name or '漫剧' in name or '漫短' in name or 'DuanJu' in name or 'ManJu' in name:
        cat = '短剧'
    elif '直播' in name or 'Live' in name:
        cat = '直播'
    elif '儿歌' in name or 'Children' in name or '跳舞' in name or 'Music' in name or '戏曲' in name or 'KTV' in name or '舞曲' in name:
        cat = '音乐儿歌'
    elif '哔哩' in name or 'Bili' in name or '少儿' in name or '小学' in name or '初中' in name or '高中' in name:
        cat = 'B站教育'
    elif '听书' in name or 'Book' in name:
        cat = '听书'
    elif '体育' in name or 'Sport' in name:
        cat = '体育'
    elif 'DIY' in name or 'Diy' in name or 'AList' in name or 'WebDav' in name:
        cat = 'DIY工具'
    elif '我的' in name or 'My' in name or 'Fake' in name or '115' in name:
        cat = '个人网盘'
    elif '给力' in name or 'So' in name:
        cat = '网盘搜索'
    elif '磁力' in name or '6V' in name or '新6V' in name:
        cat = '磁力搜索'
    elif '指南' in name or '配置' in name or '日期' in name or '扫码' in name:
        cat = '指引配置'
    else:
        cat = '其他'
    
    categories.setdefault(cat, []).append((i, name, api))

for cat, items in sorted(categories.items(), key=lambda x: -len(x[1])):
    print(f"\n【{cat}】({len(items)}个)")
    for num, name, api in items:
        print(f"  {num:2d}. {name:25s} ({api})")

print(f"\n{'='*60}")
print(f"总计: {total} 个源")
print(f"{'='*60}")
print(f"\n各分类统计:")
for cat, items in sorted(categories.items(), key=lambda x: -len(x[1])):
    print(f"  {cat}: {len(items)}")
