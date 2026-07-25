# -*- coding: utf-8 -*-
"""
真实测试影视源是否能加载列表
通过请求 spider.jar 的 init 和 home 方法来验证
"""
import requests
import json

SPIDER_URL = "https://abu168888.github.io/tvbox-config/spider.jar"

def test_source(api_class, ext=None):
    """测试单个源是否能初始化并返回列表"""
    print(f"\n{'='*50}")
    print(f"测试：{api_class}")
    if ext:
        print(f"Ext: {ext}")
    
    try:
        # 1. 调用 init 方法初始化
        init_url = f"{SPIDER_URL}/init"
        data = {"key": api_class, "ext": ext or ""}
        resp = requests.post(init_url, json=data, timeout=30)
        
        if resp.status_code != 200:
            return False, f"Init 失败：HTTP {resp.status_code}"
        
        init_result = resp.json()
        if not init_result.get("code") == 200:
            return False, f"Init 返回错误：{init_result}"
        
        print(f"✓ Init 成功")
        
        # 2. 调用 home 方法获取分类/列表
        home_url = f"{SPIDER_URL}/home"
        resp = requests.post(home_url, json={"key": api_class}, timeout=30)
        
        if resp.status_code != 200:
            return False, f"Home 失败：HTTP {resp.status_code}"
        
        home_result = resp.json()
        
        if not home_result.get("code") == 200:
            return False, f"Home 返回错误：{home_result}"
        
        classes = home_result.get("data", {}).get("class", [])
        print(f"✓ Home 成功 - 获取到 {len(classes)} 个分类")
        
        if len(classes) > 0:
            print(f"  示例分类：{classes[0]}")
            
            # 3. 尝试获取第一个分类的内容
            cate_name = classes[0].get("type_id", "")
            if cate_name:
                type_url = f"{SPIDER_URL}/type"
                resp = requests.post(type_url, json={
                    "key": api_class,
                    "tid": cate_name,
                    "pg": 1
                }, timeout=30)
                
                if resp.status_code == 200:
                    type_result = resp.json()
                    videos = type_result.get("data", {}).get("list", [])
                    print(f"✓ Type 成功 - 该分类有 {len(videos)} 个视频")
                    
                    if len(videos) > 0:
                        print(f"  示例视频：{videos[0].get('vod_name', 'N/A')}")
                        return True, "完整可用"
                    else:
                        return True, "结构正常但无内容"
        
        return True, "基本可用"
        
    except requests.exceptions.Timeout:
        return False, "请求超时"
    except Exception as e:
        return False, str(e)

# 测试所有新增的源
test_cases = [
    ("csp_Douban", None),
    ("csp_Uku", None),
    ("csp_Iqiyi", None),
    ("csp_Tencent", None),
    ("csp_Mangguo", None),
    ("csp_Bili", None),
]

print("=" * 50)
print("开始测试影视源可用性")
print("=" * 50)

results = []
for api, ext in test_cases:
    success, msg = test_source(api, ext)
    status = "通过" if success else "失败"
    results.append((api, success, msg))
    print(f"\n[{status}] {api}: {msg}")

# 总结
print("\n" + "=" * 50)
print("测试结果汇总")
print("=" * 50)

passed = sum(1 for _, s, _ in results if s)
total = len(results)

for api, success, msg in results:
    status = "✓" if success else "X"
    print(f"[{status}] {api}: {msg}")

print(f"\n总计：{passed}/{total} 可用 ({100*passed//total}%)")

if passed == total:
    print("\n*** 所有源测试通过！可以直接使用。***")
else:
    print("\n*** 部分源测试失败，需要进一步处理。***")
