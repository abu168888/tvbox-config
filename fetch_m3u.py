# -*- coding: utf-8 -*-
"""
从 ly svc.cc 提取M3U直播源
M3U数据在页面的 <pre class="EnlighterJSRAW"> 标签中
"""
import os, re, json, html
from datetime import datetime

BASE_DIR = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new'
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
LIVE_DIR = os.path.join(BASE_DIR, 'live_sources')
os.makedirs(LIVE_DIR, exist_ok=True)

def fetch_page(url):
    """获取页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    import urllib.request
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  [ERROR] {str(e)[:80]}")
        return None

# 步骤1: 获取分类页面，找到最新文章的URL
print("=" * 60)
print("Step 1: 获取最新文章URL")
print("=" * 60)

category_url = "https://lysvc.cc/category/%E6%9C%80%E6%96%B0%E7%9B%B4%E6%92%AD%E6%BA%90/"
page_html = fetch_page(category_url)

if not page_html:
    print("  [FAIL] 无法获取分类页面")
    exit(1)

# 提取文章URL和标题
article_pattern = r'<a[^>]+href="(https://lysvc\.cc/[^"]+)"[^>]*title="([^"]+)"'
articles = re.findall(article_pattern, page_html)
print(f"  找到 {len(articles)} 篇文章")

if not articles:
    # 备用正则
    articles = re.findall(r'<a[^>]+href="([^"]*lysvc\.cc/\d{4}-[^"]+)"', page_html)
    print(f"  备用模式找到 {len(articles)} 篇")

if not articles:
    print("  [FAIL] 无法提取文章链接")
    exit(1)

# 取最新5篇
latest_articles = articles[:5]
for i, (url, title) in enumerate(latest_articles, 1):
    print(f"    {i}. {title[:50]}")
    print(f"       {url}")

# 步骤2: 访问文章页面，提取M3U内容
print("\n" + "=" * 60)
print("Step 2: 提取M3U数据")
print("=" * 60)

m3u_content = None
m3u_title = None
m3u_date = None

for url, title in latest_articles:
    print(f"  尝试: {title[:60]}")
    article_html = fetch_page(url)
    
    if not article_html:
        print(f"    [FAIL] 无法访问文章")
        continue
    
    # 提取M3U数据 - 在 <pre class="EnlighterJSRAW"> 标签中
    pre_match = re.search(r'<pre[^>]*class="[^"]*EnlighterJSRAW[^"]*"[^>]*>(.*?)</pre>', article_html, re.DOTALL)
    
    if pre_match:
        raw_content = pre_match.group(1)
        # 解码HTML实体
        m3u_content = html.unescape(raw_content)
        m3u_title = title
        
        # 从标题提取日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', title)
        if date_match:
            m3u_date = date_match.group(1)
        
        print(f"    [OK] 找到M3U数据")
        print(f"    原始大小: {len(raw_content)} 字节")
        print(f"    解码后: {len(m3u_content)} 字节")
        print(f"    频道数: {m3u_content.count('#EXTINF')}")
        break
    else:
        print(f"    [X] 未找到 <pre> 标签")

# 步骤3: 解析M3U并转换为TXT格式
print("\n" + "=" * 60)
print("Step 3: 解析并转换直播源")
print("=" * 60)

channels_by_group = {}
if m3u_content:
    # 解析M3U
    current_group = "其他"
    current_name = ""
    
    for line in m3u_content.split('\n'):
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

print(f"  解析到 {len(channels_by_group)} 个分组")
total_channels = sum(len(v) for v in channels_by_group.values())
print(f"  总频道数: {total_channels}")

# 显示前15个分组
for group, ch_list in sorted(channels_by_group.items())[:15]:
    print(f"    {group}: {len(ch_list)} 频道")

if total_channels > 15:
    print(f"    ... 还有 {len(channels_by_group) - 15} 个分组")

# 转换为TXT格式 (TVBox标准)
txt_lines = []
for group, ch_list in sorted(channels_by_group.items()):
    if not group or group == "其他":
        group = "其他直播源"
    txt_lines.append(f"{group}#url:")
    # 每个分组取前300个，控制文件大小
    for name, url in ch_list[:300]:
        txt_lines.append(f"{name},{url}")
    txt_lines.append("")

txt_content = "\n".join(txt_lines)

txt_path = os.path.join(LIVE_DIR, "live_sources.txt")
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(txt_content)
print(f"\n  TXT文件: {txt_path}")
print(f"  TXT大小: {len(txt_content)} 字节 / {len(txt_lines)} 行")

# 保存M3U原始文件
if m3u_content:
    m3u_path = os.path.join(LIVE_DIR, "live_source.m3u")
    with open(m3u_path, 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print(f"  M3U文件: {m3u_path}")

# 步骤4: 更新config.json
print("\n" + "=" * 60)
print("Step 4: 更新config.json")
print("=" * 60)

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

# 步骤5: 生成报告
report = {
    "source": "lysvc.cc",
    "source_name": m3u_title or "未知",
    "date": m3u_date or datetime.now().strftime("%Y-%m-%d"),
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

# 步骤6: 总结
print("\n" + "=" * 60)
if m3u_content:
    print("✅ 直播源更新成功!")
    print(f"   来源: {m3u_title}")
    print(f"   日期: {report['date']}")
    print(f"   分组: {report['total_groups']}")
    print(f"   频道: {total_channels}")
    print(f"\n   下一步: git push 推送到 GitHub")
else:
    print("⚠️ 未能获取直播源")
print("=" * 60)
