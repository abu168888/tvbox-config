import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

config_path = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'

with open(config_path, 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

# 要删除的源
delete_keys = [
    # DIY工具 (3个)
    'AList',          # 👁️Alist┃DIY👁️
    'webdav',         # 👁️WebDav┃DIY👁️
    'DiyVod',         # 👁Vod┃DIY👁️
    
    # 新增的5个4K源
    'NewPanSou',      # 新盘搜4K
    'YiSo',           # 新易搜4K
    'NewKunYu',       # 新酷云4K
    'NewLiangCai',    # 新猎手4K
    'NewDm84',        # 新动漫4K
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
