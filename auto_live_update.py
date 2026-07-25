# -*- coding: utf-8 -*-
"""
狸云直播源自动更新系统 - ly svc.cc
1. 爬取最新文章获取M3U下载链接
2. 下载M3U文件
3. 转换为TVBox兼容的TXT格式
4. 更新config.json中的直播源
5. 推送到GitHub Pages
"""
import os
import re
import json
import time
import urllib.request
from datetime import datetime

BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
LIVE_DIR = os.path.join(BASE_DIR, 'live_sources')
os.makedirs(LIVE_DIR, exist_ok=True)

def fetch_url(url, timeout=15):
    """HTTP GET with headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return None

def save_html(html, filename):
    """保存HTML用于调试"""
    path = os.path.join(LIVE_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path

def parse_m3u(content):
    """解析M3U文件，返回分组字典"""
    channels_by_group = {}
    current_group = "其他"
    current_name = ""
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('#EXTINF:'):
            # 提取频道名称
            name_match = re.search(r',\s*(.+)$', line)
            if name_match:
                current_name = name_match.group(1).strip()
            # 提取分组
            group_match = re.search(r'group-title="([^"]*)"', line)
            if group_match:
                current_group = group_match.group(1)
        elif not line.startswith('#') and line:
            url = line
            if current_group not in channels_by_group:
                channels_by_group[current_group] = []
            channels_by_group[current_group].append((current_name, url))
            current_name = ""
    
    return channels_by_group

def convert_to_txt(channels_by_group, max_per_group=500):
    """转换为TVBox兼容的TXT格式"""
    txt_lines = []
    for group, ch_list in sorted(channels_by_group.items()):
        if not group or group == "其他":
            group = "其他直播源"
        txt_lines.append(f"{group}#url:")
        # 每个分组取前N个，控制文件大小
        for name, url in ch_list[:max_per_group]:
            txt_lines.append(f"{name},{url}")
        txt_lines.append("")  # 空行分隔
    return "\n".join(txt_lines)

# ============================================
# Step 1: 爬取分类页面，获取文章链接
# ============================================
print("=" * 60)
print("狸云直播源 - 自动更新系统")
print("=" * 60)

print("\n[Step 1] 获取最新直播源文章...")
print("-" * 60)

category_url = "https://lysvc.cc/category/%E6%9C%80%E6%96%B0%E7%9B%B4%E6%92%AD%E6%BA%90/"
page_html = fetch_url(category_url)

if not page_html:
    print("  [FAIL] 无法获取分类页面")
    exit(1)

# 提取文章链接
post_links = re.findall(r'<a[^>]+href="([^"]*lysvc\.cc/[^"]+)"[^>]*title="([^"]+)"', page_html)
if not post_links:
    post_links = re.findall(r'<a[^>]+href="([^"]*lysvc\.cc/\d{4}-[^"]+)"', page_html)

print(f"  找到 {len(post_links)} 个文章链接")
latest_posts = post_links[:5]

for i, (url, title) in enumerate(latest_posts, 1):
    print(f"    {i}. {title}")
    print(f"       {url}")

# ============================================
# Step 2: 访问文章页面，获取M3U下载链接
# ============================================
print("\n[Step 2] 获取M3U下载链接...")
print("-" * 60)

m3u_url = None
m3u_title = None

for url, title in latest_posts:
    print(f"  尝试: {title}")
    article_html = fetch_url(url)
    
    if not article_html:
        print(f"    [FAIL] 无法访问")
        continue
    
    # 保存HTML用于调试
    debug_path = save_html(article_html, 'debug_article.html')
    print(f"    调试HTML: {debug_path}")
    
    # 查找M3U下载链接 - 多种模式
    m3u_candidates = []
    
    # 模式1: 直接href包含.m3u
    m3u_candidates.extend(re.findall(r'href="([^"]+\.m3u[^"]*)"', article_html))
    
    # 模式2: download按钮
    m3u_candidates.extend(re.findall(r'download[^>]*href="([^"]+)"', article_html))
    
    # 模式3: 包含m3u关键词
    m3u_candidates.extend(re.findall(r'[^" ]+\.m3u[^"]*', article_html))
    
    # 去重并过滤
    seen = set()
    unique_urls = []
    for url in m3u_candidates:
        if url not in seen and url.startswith('http') and '.m3u' in url:
            seen.add(url)
            unique_urls.append(url)
    
    print(f"    找到 {len(unique_urls)} 个M3U链接:")
    for link in unique_urls[:3]:
        print(f"      - {link[:120]}")
    
    # 尝试下载第一个链接
    if unique_urls:
        test_url = unique_urls[0]
        print(f"    尝试下载: {test_url[:80]}...")
        m3u_content = fetch_url(test_url)
        
        if m3u_content and m3u_content.startswith('#EXTM3U'):
            m3u_url = test_url
            m3u_title = title
            print(f"    [OK] 下载成功!")
            break
        else:
            print(f"    [X] 下载失败或格式不对")

# ============================================
# Step 3: 下载并解析M3U
# ============================================
print("\n[Step 3] 下载并解析M3U直播源...")
print("-" * 60)

m3u_content = None
if m3u_url:
    m3u_content = fetch_url(m3u_url)
    if m3u_content and m3u_content.startswith('#EXTM3U'):
        print(f"  [OK] 下载成功")
        print(f"  文件大小: {len(m3u_content)} 字节")
        print(f"  频道数: {m3u_content.count('#EXTINF')}")
    else:
        print(f"  [FAIL] 不是有效的M3U文件")
        m3u_content = None
else:
    print("  [SKIP] 未找到M3U下载链接")

# ============================================
# Step 4: 解析M3U并转换格式
# ============================================
print("\n[Step 4] 解析并转换直播源...")
print("-" * 60)

channels_by_group = {}
if m3u_content:
    channels_by_group = parse_m3u(m3u_content)

print(f"  解析到 {len(channels_by_group)} 个分组")
total_channels = sum(len(v) for v in channels_by_group.values())
print(f"  总频道数: {total_channels}")

# 显示前10个分组
for group, ch_list in sorted(channels_by_group.items())[:10]:
    print(f"    {group}: {len(ch_list)} 频道")

if total_channels > 10:
    print(f"    ... 还有 {len(channels_by_group) - 10} 个分组")

# 转换为TXT
txt_content = convert_to_txt(channels_by_group, max_per_group=500)

txt_path = os.path.join(LIVE_DIR, "live_sources.txt")
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(txt_content)
print(f"\n  TXT文件: {txt_path}")
print(f"  TXT大小: {len(txt_content)} 字节 / {len(txt_content.splitlines())} 行")

# 保存M3U
if m3u_content:
    m3u_path = os.path.join(LIVE_DIR, "live_source.m3u")
    with open(m3u_path, 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print(f"  M3U文件: {m3u_path}")

# ============================================
# Step 5: 更新config.json
# ============================================
print("\n[Step 5] 更新config.json...")
print("-" * 60)

with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

# 删除旧的直播源
old_live_keys = ['LiveHuYa', 'LiveDouYu', 'LiveBiLi', 'LiveNew']
for key in old_live_keys:
    config['sites'] = [s for s in config['sites'] if s.get('key') != key]
    print(f"  删除旧源: {key}")

# 添加新的直播源条目
new_live_entry = {
    "key": "LiveNew",
    "name": "📡全球直播📡",
    "type": 3,
    "api": "csp_Yj1211",
    "searchable": 1,
    "changeable": 1,
    "timeout": 60
}
config['sites'].append(new_live_entry)

# 保存
with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"  已更新: {CONFIG_PATH}")
print(f"  总站点数: {len(config['sites'])}")

# ============================================
# Step 6: 生成报告
# ============================================
report = {
    "source": "lysvc.cc",
    "source_name": m3u_title or "未知",
    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "total_channels": total_channels,
    "total_groups": len(channels_by_group),
    "groups": list(channels_by_group.keys()),
    "txt_file": txt_path,
    "m3u_file": os.path.join(LIVE_DIR, "live_source.m3u") if m3u_content else None,
    "success": m3u_content is not None
}

report_path = os.path.join(LIVE_DIR, "live_report.json")
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n  状态报告: {report_path}")

# ============================================
# Summary
# ============================================
print("\n" + "=" * 60)
if m3u_content:
    print("✅ 直播源更新成功!")
    print(f"   来源: {m3u_title}")
    print(f"   日期: {report['date']}")
    print(f"   分组: {report['total_groups']}")
    print(f"   频道: {total_channels}")
    print(f"\n  下一步: git push 推送到 GitHub")
else:
    print("⚠️ 未能从网站获取直播源")
    print("  可能原因:")
    print("  1. 网站链接结构变更")
    print("  2. 需要登录或反爬验证")
    print("  3. 网络问题")
    print("  建议: 手动下载M3U文件放到 live_sources/ 目录")
print("=" * 60)
