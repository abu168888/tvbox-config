# -*- coding: utf-8 -*-
"""
分析文章页面结构，找到M3U下载链接
"""
import os, re, json, urllib.request

BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'

def fetch_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return None

# 获取最新文章页面
url = "https://lysvc.cc/2026-07-25%e6%9b%b4%e6%96%b0595%e4%b8%aa%e5%85%a8%e7%90%83%e7%9b%b4%e6%92%ad%e6%ba%90m3u-%e6%b6%b5%e7%9b%96%e6%b8%af%e6%be%b0%e5%8f%b0-%e6%ac%a7%e7%be%8e-%e6%97%a5%e9%9f%a9%ef%bc%8c%e6%94%af/"
html = fetch_url(url)

if not html:
    print("[FAIL] 无法获取页面")
    exit(1)

print("=" * 60)
print("文章页面结构分析")
print("=" * 60)

# 保存原始HTML到文件
html_path = os.path.join(BASE_DIR, 'live_sources', 'debug_page.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"完整HTML已保存: {html_path}")

# 分析下载链接
print("\n[分析] 所有链接提取:")
all_links = re.findall(r'href="([^"]+)"', html)
download_links = []
for link in all_links:
    if any(keyword in link.lower() for keyword in ['download', 'm3u', 'txt', 'source', '直播', '下载']):
        download_links.append(link)

print(f"  找到 {len(download_links)} 个潜在下载链接:")
for link in download_links[:20]:
    print(f"    - {link[:100]}")

# 查找特定模式
print("\n[模式匹配] 寻找M3U相关元素:")

# 模式1: download按钮/链接
download_patterns = [
    r'download.*?href="([^"]+)"',
    r'href="([^"]+)"[^>]*download',
    r'直播源.*?href="([^"]+)"',
    r'm3u.*?href="([^"]+)"',
]

for pattern in download_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"  模式 '{pattern[:30]}...' 匹配: {len(matches)} 个")
        for m in matches[:5]:
            print(f"    - {m}")

# 查找iframe/embed/src等可能的M3U来源
print("\n[媒体链接] 查找可能的M3U URL:")
media_links = re.findall(r'(https?://[^"' + r']+\.m3u[^" ]*)', html)
if media_links:
    print(f"  找到 {len(media_links)} 个M3U链接:")
    for link in media_links[:10]:
        print(f"    - {link}")
else:
    print("  未直接找到.m3u链接")

# 查找JavaScript中的变量
print("\n[JS变量] 查找可能的数据源:")
js_patterns = [
    r'(https?://[^"' + r'\\s]*\.(?:m3u|txt|m3u8))',
    r'var\s+\w*live\w*\s*=\s*["\']([^"\']+)["\']',
    r'source.*?url.*?["\']([^"\']+(?:m3u|txt|live))',
]

for pattern in js_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"  模式匹配到: {len(matches)} 个")
        for m in matches[:5]:
            print(f"    - {m[:150]}")

# 检查页面是否有动态加载内容
print("\n[动态加载检测] 检查可能的API调用:")
api_patterns = [
    r'(?:api|ajax|fetch|request)[^;]*?url[^;]*?:\s*["\']([^"\']+)["\']',
    r'https?://[^"' + r'\\s]+(?:api|live|source)[^"' + r'\\s]*',
]

for pattern in api_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"  找到API相关URL: {len(matches)} 个")
        for m in matches[:5]:
            print(f"    - {m[:150]}")

print("\n[HTML结构] 关键区域预览:")
# 查找主要内容区域
content_areas = re.findall(r'<div[^>]*class="[^"]*(?:content|post|article|entry)[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
if content_areas:
    print(f"  找到 {len(content_areas)} 个内容区域")
    for i, area in enumerate(content_areas[:3]):
        # 只取前500字符
        preview = area[:500].replace('\n', ' ').replace('\r', '')
        print(f"  区域{i+1}: {preview[:200]}...")
else:
    # 查找任何包含"直播"或"m3u"的区域
    relevant_sections = re.findall(r'<[^>]*>(?:.*?(?:直播|m3u|下载|source).*?)</[^>]*>', html, re.IGNORECASE | re.DOTALL)
    print(f"  找到 {len(relevant_sections)} 个相关区域:")
    for i, section in enumerate(relevant_sections[:10]):
        preview = section.replace('\n', ' ').replace('\r', '')[:200]
        print(f"    {i+1}. {preview}...")

print("\n[页面统计]")
print(f"  总链接数: {len(all_links)}")
print(f"  页面大小: {len(html)} 字节")
print(f"  包含'm3u': {'是' if 'm3u' in html.lower() else '否'}")
print(f"  包含'download': {'是' if 'download' in html.lower() else '否'}")
print(f"  包含'直播源': {'是' if '直播源' in html else '否'}")

print("\n" + "=" * 60)
print("分析完成")
print("=" * 60)
