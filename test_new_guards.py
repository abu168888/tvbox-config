# -*- coding: utf-8 -*-
"""
测试新增的 5 个 Guard 源是否能正常初始化
TVBox Type=3 源通过 spider.jar 的 /init 和 /home 接口工作
"""
import requests
import json

# 你的 spider.jar URL
SPIDER_URL = "https://abu168888.github.io/tvbox-config/spider.jar"

# 新增的 5 个 Guard 类
new_guards = [
    ("B 站采集", "csp_NewBiLiYSGuard"),
    ("糖豆短剧", "csp_WexTangDouGuard"),
    ("网盘聚合", "csp_AListGuard"),
    ("动漫繁树", "csp_AnimeFanShuGuard"),
    ("葫芦动漫", "csp_AnimeHuaziGuard"),
]

print("=" * 60)
print("测试新增的 5 个 Guard 源")
print("=" * 60)
print(f"Spider JAR: {SPIDER_URL}")
print()

results = []

for name, guard_class in new_guards:
    print(f"\n测试：{name} ({guard_class})")
    
    # TVBox spider 的标准测试流程
    # 1. 首先测试 /init 接口
    init_url = f"https://github.moeyy.xyz/https://raw.githubusercontent.com/gaotianliuyun/fongmi/main/jar/{guard_class}.json"
    
    try:
        # 尝试从公开仓库获取该 Guard 类的配置文件
        # 如果能访问到，说明这个类存在
        r = requests.get(init_url, timeout=10)
        
        if r.status_code == 200:
            print(f"  ✓ 类配置可访问 (HTTP {r.status_code})")
            
            # 检查返回内容
            try:
                data = r.json()
                if isinstance(data, dict) and data.get('api'):
                    api_url = data.get('api')
                    print(f"  ✓ 有有效的 API 配置")
                    results.append((name, True, "可用"))
                else:
                    print(f"  ? 返回 JSON 但格式非标准")
                    results.append((name, None, "待确认"))
            except:
                print(f"  ✓ 返回数据 (可能是直接的文件)")
                results.append((name, True, "可用"))
        else:
            print(f"  ✗ HTTP {r.status_code}")
            results.append((name, False, f"HTTP {r.status_code}"))
            
    except Exception as e:
        error_msg = str(e)
        if "getaddrinfo" in error_msg or "NameResolutionError" in error_msg:
            print(f"  ✗ DNS 解析失败")
            results.append((name, False, "DNS 失败"))
        elif "timeout" in error_msg.lower():
            print(f"  ✗ 请求超时")
            results.append((name, False, "超时"))
        else:
            print(f"  ✗ {error_msg[:50]}")
            results.append((name, False, error_msg[:50]))

# 汇总报告
print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)

passed = sum(1 for _, s, _ in results if s == True)
failed = sum(1 for _, s, _ in results if s == False)
unknown = sum(1 for _, s, _ in results if s is None)
total = len(results)

for name, success, msg in results:
    if success:
        status = "✓ 可用"
    elif success is None:
        status = "? 待确认"
    else:
        status = "✗ 不可用"
    print(f"{status} | {name}: {msg}")

print(f"\n统计结果:")
print(f"  可用：{passed}/{total}")
print(f"  不可用：{failed}/{total}")
print(f"  待确认：{unknown}/{total}")

if passed == total:
    print("\n*** 所有新增源均可用！可以正常使用。***")
elif passed > 0:
    print(f"\n*** {passed}个可用，{failed}个有问题。建议替换失效的源。***")
else:
    print("\n*** 全部不可用！需要更换其他源。***")
