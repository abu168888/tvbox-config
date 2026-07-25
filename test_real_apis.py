# -*- coding: utf-8 -*-
"""
批量测试真实的 TVBox Type=1 采集接口
从 wuxierj/TVBox 等仓库收集的已验证接口
"""
import requests
import json

# 收集的真实可用的 Type=1 接口
real_apis = [
    ("饭太硬", "http://www.饭太硬.net/tv"),
    ("肥猫", "http://肥猫.net/"),
    ("摸鱼备用", "https://6800.kstore.vip/fish.json"),
    ("俊佬", "http://home.jundie.top:81/top98.json"),
    ("王二小", "http://tvbox.xn--4kq62z5rby2qupq9ub.top/"),
]

print("=" * 60)
print("开始测试真实可用的 TVBox 采集接口")
print("=" * 60)

results = []

for name, api_url in real_apis:
    print(f"\n测试：{name}")
    print(f"URL: {api_url}")
    
    try:
        resp = requests.get(api_url, timeout=20)
        
        if resp.status_code != 200:
            print(f"  [失败] HTTP {resp.status_code}")
            results.append((name, False, f"HTTP {resp.status_code}"))
            continue
        
        data = resp.json()
        
        # TVBox 接口应该包含 sites 数组
        if isinstance(data, dict):
            sites = data.get('sites', [])
            if len(sites) == 0:
                print(f"  [警告] sites 为空数组")
                results.append((name, True, "可访问但无站点"))
                continue
            
            print(f"  [通过] 获取到 {len(sites)} 个站点")
            
            # 显示前 3 个站点名称
            print(f"  示例站点:")
            for i, site in enumerate(sites[:3], 1):
                name_str = site.get('name', site.get('key', '未知'))
                type_num = site.get('type', '?')
                print(f"    {i}. {name_str} (type={type_num})")
            
            results.append((name, True, f"可用 ({len(sites)}个站点)"))
        else:
            print(f"  [失败] 非标准 JSON 格式")
            results.append((name, False, "格式错误"))
            
    except requests.exceptions.Timeout:
        print(f"  [失败] 请求超时")
        results.append((name, False, "超时"))
    except Exception as e:
        error_msg = str(e)
        if "getaddrinfo" in error_msg or "NameResolutionError" in error_msg:
            print(f"  [失败] DNS 解析失败")
            results.append((name, False, "DNS 失败"))
        elif "Max retries" in error_msg:
            print(f"  [失败] 连接拒绝")
            results.append((name, False, "连接失败"))
        else:
            print(f"  [失败] {error_msg}")
            results.append((name, False, error_msg))

# 汇总
print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)

passed = sum(1 for _, s, _ in results if s)
total = len(results)

for name, success, msg in results:
    status = "[OK]" if success else "[X]"
    print(f"{status} {name}: {msg}")

print(f"\n总计：{passed}/{total} 可用 ({100*passed//total}%)")

if passed > 0:
    print("\n*** 有可用接口！可以提交。***")
else:
    print("\n*** 全部失败！需要找其他源。***")
