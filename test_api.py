# -*- coding: utf-8 -*-
"""
真实测试 Type=1 采集接口是否能返回视频数据
"""
import requests
import json

# 测试所有新增的 Type=1 接口
apis = [
    ("爱酷影视", "http://zycj.vq.tv:8080/api.php/provide/vod/"),
    ("天空影视", "https://m3u8.tiankong.baicizhan.com/api.php/provide/vod/"),
    ("金牌影视", "http://www.jinpaiwm.cn/api.php/provide/vod/"),
    ("飞速影视", "https://fszy1.tk/api.php/provide/vod/"),
    ("索尼影视", "http://suoniapi.com/api.php/provide/vod/"),
    ("暴风影视", "https://bfzyapi.com/api.php/provide/vod/")
]

print("=" * 60)
print("开始测试 Type=1 采集接口")
print("=" * 60)

results = []

for name, api_url in apis:
    print(f"\n测试：{name}")
    print(f"API: {api_url}")
    
    try:
        # 请求分类列表 (ac=detail 或 ac=list)
        url = f"{api_url}?ac=list"
        resp = requests.get(url, timeout=20)
        
        if resp.status_code != 200:
            print(f"  [失败] HTTP {resp.status_code}")
            results.append((name, False, f"HTTP {resp.status_code}"))
            continue
        
        data = resp.json()
        
        # 检查响应结构
        if isinstance(data, dict):
            list_data = data.get('list', [])
        elif isinstance(data, list):
            list_data = data
        else:
            print(f"  [失败] 非标准响应格式")
            results.append((name, False, "非标准响应"))
            continue
        
        if len(list_data) == 0:
            print(f"  [失败] 返回空列表")
            results.append((name, False, "无数据"))
            continue
        
        print(f"  [通过] 获取到 {len(list_data)} 条数据")
        
        # 尝试获取第一个视频详情
        first_item = list_data[0]
        vod_name = first_item.get('vod_name', first_item.get('name', '未知'))
        print(f"  示例影片：{vod_name}")
        
        results.append((name, True, f"可用 ({len(list_data)} 条数据)"))
        
    except requests.exceptions.Timeout:
        print(f"  [失败] 请求超时")
        results.append((name, False, "超时"))
    except Exception as e:
        print(f"  [失败] {str(e)}")
        results.append((name, False, str(e)))

# 汇总
print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)

passed = sum(1 for _, s, _ in results if s)
total = len(results)

for name, success, msg in results:
    status = "通过" if success else "失败"
    print(f"[{status}] {name}: {msg}")

print(f"\n总计：{passed}/{total} 可用 ({100*passed//total}%)")

if passed == total:
    print("\n*** 全部通过！可以提交代码了。***")
elif passed > 0:
    print(f"\n*** {passed}个可用，可以考虑提交。***")
else:
    print("\n*** 全部失败！需要更换其他源。***")
