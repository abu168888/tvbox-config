# -*- coding: utf-8 -*-
"""
验证新增的 5 个 Guard 类是否在官方配置源中存在
来源：https://9280.kstore.vip/newwex.json
"""
import requests
import json

# 你的官方配置源
SOURCE_URL = "https://9280.kstore.vip/newwex.json"

# 新增的 5 个 Guard 类
new_guards = [
    "csp_NewBiLiYSGuard",
    "csp_WexTangDouGuard", 
    "csp_AListGuard",
    "csp_AnimeFanShuGuard",
    "csp_AnimeHuaziGuard",
]

print("=" * 60)
print("验证新增 Guard 类在官方源中的真实性")
print("=" * 60)
print(f"官方源：{SOURCE_URL}")
print()

try:
    # 1. 获取官方配置
    print("[1/2] 正在从官方源拉取数据...")
    r = requests.get(SOURCE_URL, timeout=30)
    
    if r.status_code != 200:
        print(f"[失败] HTTP {r.status_code}")
        exit(1)
    
    data = r.json()
    sites = data.get('sites', [])
    print(f"      OK 获取到 {len(sites)} 个站点")
    
    # 2. 提取所有使用的 Guard 类
    print("[2/2] 提取并验证 Guard 类...")
    used_guards = set()
    for site in sites:
        if site.get('type') == 3:
            api = site.get('api', '')
            if 'Guard' in api:
                used_guards.add(api)
    
    print(f"      OK 官方源使用 {len(used_guards)} 个唯一 Guard 类")
    print()
    
    # 3. 验证新增的 5 个类
    print("=" * 60)
    print("验证结果:")
    print("=" * 60)
    
    verified_count = 0
    for guard_class in new_guards:
        if guard_class in used_guards:
            status = "OK - 存在于官方源"
            verified_count += 1
        else:
            status = "X - 不存在于官方源"
        
        print("[{}] {} | {}".format(status[:2], guard_class, status[3:]))
    
    print()
    print("=" * 60)
    print("总结:")
    print("=" * 60)
    print("验证通过：{}/5".format(verified_count))
    
    if verified_count == 5:
        print("\n*** 全部 5 个 Guard 类都存在于官方源中!")
        print("*** 这说明它们是真实可用的高质量源。")
        print("*** 建议在 TVBox 中正常使用。")
    elif verified_count > 0:
        print("\n*** 部分可用 ({}/5)。建议替换不可用的源。")
    else:
        print("\n*** 全部不存在！需要更换其他 Guard 类。")
    
except Exception as e:
    print("[错误] {}".format(str(e)))
