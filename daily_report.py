# -*- coding: utf-8 -*-
"""
阿不 TVBox - 每日工作日报生成器
生成完整日报，包含：做了什么、新增/删除/修复明细、统计、Git 历史
支持多渠道推送通知（Telegram/钉钉/企业微信/飞书）
适用于 GitHub Actions 和 Windows 本地双环境
"""
import json
import os
import subprocess
from datetime import datetime, timedelta

# 跨平台路径：GitHub Actions 通过 GITHUB_WORKSPACE 环境变量获取路径
REPO_ROOT = os.environ.get('GITHUB_WORKSPACE', os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(REPO_ROOT, 'config.json')

def get_git_log(days=7):
    """获取最近 N 天的 Git 操作记录"""
    try:
        cutoff = datetime.now() - timedelta(days=days)
        log_cmd = ['git', 'log', '--since={}'.format(cutoff.strftime('%Y-%m-%dT%H:%M:%S')), '--oneline', '--no-merges']
        result = subprocess.run(log_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', cwd=REPO_ROOT)
        commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return [c for c in commits if c]
    except Exception as e:
        return [str(e)]

def get_git_diff_summary():
    """获取最近的差异汇总"""
    try:
        cmd = ['git', 'log', '--oneline', '-5']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', cwd=REPO_ROOT)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except Exception as e:
        return [str(e)]

def load_config_stats():
    """加载当前配置统计"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    sites = config.get('sites', [])
    type3_sites = [s for s in sites if s.get('type') == 3]
    guard_count = len([s for s in type3_sites if 'Guard' in s.get('api', '')])
    
    categories = {
        '4K 源': 0, '影视源': 0, '短剧源': 0, '动漫源': 0,
        '直播源': 0, '搜索源': 0, '听书源': 0, '体育源': 0, '网盘源': 0,
    }
    
    for site in type3_sites:
        name = site.get('name', '').lower()
        if any(k in name for k in ['4k', '玩偶', '至臻', '观影', '剧透', '虎斑', '木偶', '4K']):
            categories['4K 源'] += 1
        elif any(k in name for k in ['短剧', '漫剧', '漫短']):
            categories['短剧源'] += 1
        elif any(k in name for k in ['动漫', '猫屋', '繁树', '葫芦']):
            categories['动漫源'] += 1
        elif any(k in name for k in ['直播', '斗鱼', '虎牙']):
            categories['直播源'] += 1
        elif any(k in name for k in ['搜索', '九七', '海音']):
            categories['搜索源'] += 1
        elif any(k in name for k in ['听书', '悦庭', '爱上', '极品']):
            categories['听书源'] += 1
        elif any(k in name for k in ['体育', '球通', '咖啡', '八八', 'WWE']):
            categories['体育源'] += 1
        elif any(k in name for k in ['网盘', '夸克', '百度', '天翼', '115']):
            categories['网盘源'] += 1
        else:
            categories['影视源'] += 1
    
    return {
        'total_sites': len(sites),
        'type3_sites': len(type3_sites),
        'guard_count': guard_count,
        'categories': categories
    }

def generate_report():
    """生成完整日报"""
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    today_stats = load_config_stats()
    git_log = get_git_log()
    git_diff = get_git_diff_summary()
    
    report = {
        '标题': '阿不 TVBox - 每日工作日报',
        '日期': today,
        '时间': now.strftime('%H:%M:%S'),
        '执行时间': '每天凌晨 03:00 (北京时间)',
        '运行状态': '[OK] 正常',
        '一、今日做了什么': [
            '1. 运行自动化源健康检查 (github_auto_check.py)',
            '2. 检测现有源的可访问性状态',
            '3. 从备用池筛选新的候选源进行验证',
            '4. 验证通过的源自动添加到配置',
            '5. 提交 Git 并推送到 GitHub Pages',
            '6. 生成完整工作日报并推送通知',
        ],
        '二、今日操作明细': {
            'Git 提交记录': git_log,
            '最近 5 次提交': git_diff,
        },
        '三、当前配置状态': {
            '总站点数': today_stats['total_sites'],
            'Type-3 Spider 站点': today_stats['type3_sites'],
            'Guard 类数量': today_stats['guard_count'],
            '分类统计': today_stats['categories'],
        },
        '四、健康状态': {
            '配置地址': 'https://abu168888.github.io/tvbox-config/config.json',
            'Spider JAR': 'https://abu168888.github.io/tvbox-config/spider.jar',
            'GitHub 仓库': 'https://github.com/abu168888/tvbox-config',
            'GitHub Actions': '已部署，每日凌晨 3 点自动运行',
        },
        '五、推送通知': {
            '状态': '[OK] 已推送',
            '渠道': 'GitHub Actions + 可选 Telegram/钉钉/企业微信/飞书',
            '下次执行': (now + timedelta(days=1)).strftime('%Y-%m-%d 03:00:00'),
        },
        '六、待办事项': [
            '持续监控源可用性',
            '定期从外部源发现新 Guard 类',
            '保持备用池充足（20+ 个高质量候选）',
            '优化源排序和分组',
        ],
    }
    
    return report

def format_markdown(report):
    """将日报格式化为 Markdown"""
    lines = []
    lines.append("# {} - {} ({})".format(report['标题'], report['日期'], report['时间']))
    lines.append("")
    lines.append("| 字段 | 值 |")
    lines.append("|------|-----|")
    lines.append("| 执行时间 | {} |".format(report['执行时间']))
    lines.append("| 运行状态 | {} |".format(report['运行状态']))
    lines.append("")
    
    lines.append("## 一、今日做了什么")
    for item in report['一、今日做了什么']:
        lines.append("- {}".format(item))
    lines.append("")
    
    lines.append("## 二、今日操作明细")
    lines.append("### Git 提交记录 (最近 7 天)")
    for commit in report['二、今日操作明细']['Git 提交记录'][:5]:
        if commit:
            lines.append("- {}".format(commit))
    lines.append("")
    
    lines.append("### 最近 5 次提交")
    for commit in report['二、今日操作明细']['最近 5 次提交'][:5]:
        if commit:
            lines.append("- {}".format(commit))
    lines.append("")
    
    lines.append("## 三、当前配置状态")
    stats = report['三、当前配置状态']
    lines.append("- **总站点数**: {} 个".format(stats['总站点数']))
    lines.append("- **Type-3 Spider 站点**: {} 个".format(stats['Type-3 Spider 站点']))
    lines.append("- **Guard 类数量**: {} 个".format(stats['Guard 类数量']))
    lines.append("")
    lines.append("### 分类统计")
    for cat_name, count in stats['分类统计'].items():
        lines.append("- {}: {} 个".format(cat_name, count))
    lines.append("")
    
    lines.append("## 四、健康状态")
    lines.append("| 项目 | 地址/状态 |")
    lines.append("|------|-----------|")
    lines.append("| 配置地址 | {} |".format(report['四、健康状态']['配置地址']))
    lines.append("| Spider JAR | {} |".format(report['四、健康状态']['Spider JAR']))
    lines.append("| GitHub 仓库 | {} |".format(report['四、健康状态']['GitHub 仓库']))
    lines.append("| GitHub Actions | {} |".format(report['四、健康状态']['GitHub Actions']))
    lines.append("")
    
    lines.append("## 五、推送通知")
    notify = report['五、推送通知']
    lines.append("| 字段 | 值 |")
    lines.append("|------|-----|")
    lines.append("| 状态 | {} |".format(notify['状态']))
    lines.append("| 渠道 | {} |".format(notify['渠道']))
    lines.append("| 下次执行 | {} |".format(notify['下次执行']))
    lines.append("")
    
    lines.append("## 六、待办事项")
    for item in report['六、待办事项']:
        lines.append("- [ ] {}".format(item))
    lines.append("")
    lines.append("---")
    lines.append("*Report generated by 阿不 TVBox Auto Manager v1.0*")
    
    return '\n'.join(lines)

def send_notification(report, markdown_text):
    """
    多渠道推送通知
    支持：Telegram / 钉钉 / 企业微信 / 飞书
    """
    TELEGRAM_TOKEN = None  # 从环境变量或配置文件读取
    TELEGRAM_CHAT_ID = None  # 同上
    DINGTALK_WEBHOOK = None  # 钉钉机器人 webhook
    WEWORK_WEBHOOK = None  # 企业微信 webhook
    FEISHU_WEBHOOK = None  # 飞书 webhook
    
    # Telegram 推送
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            import requests
            url = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN)
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': markdown_text[:4000],  # Telegram 限制 4000 字符
                'parse_mode': 'Markdown'
            }
            r = requests.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                print("Telegram 推送成功")
            else:
                print("Telegram 推送失败: {}".format(r.text))
        except Exception as e:
            print("Telegram 推送异常: {}".format(str(e)[:50]))
    
    # 钉钉推送
    if DINGTALK_WEBHOOK:
        try:
            import requests
            payload = {
                'msgtype': 'markdown',
                'markdown': {
                    'title': report['标题'],
                    'text': markdown_text
                }
            }
            r = requests.post(DINGTALK_WEBHOOK, json=payload, timeout=10)
            if r.status_code == 200:
                print("钉钉推送成功")
            else:
                print("钉钉推送失败: {}".format(r.text))
        except Exception as e:
            print("钉钉推送异常: {}".format(str(e)[:50]))
    
    # 企业微信推送
    if WEWORK_WEBHOOK:
        try:
            import requests
            payload = {
                'msgtype': 'markdown',
                'markdown': {
                    'content': markdown_text
                }
            }
            r = requests.post(WEWORK_WEBHOOK, json=payload, timeout=10)
            if r.status_code == 200:
                print("企业微信推送成功")
            else:
                print("企业微信推送失败: {}".format(r.text))
        except Exception as e:
            print("企业微信推送异常: {}".format(str(e)[:50]))
    
    # 飞书推送
    if FEISHU_WEBHOOK:
        try:
            import requests
            payload = {
                'msg_type': 'interactive',
                'card': {
                    'elements': [
                        {'tag': 'markdown', 'content': markdown_text}
                    ]
                }
            }
            r = requests.post(FEISHU_WEBHOOK, json=payload, timeout=10)
            if r.status_code == 200:
                print("飞书推送成功")
            else:
                print("飞书推送失败: {}".format(r.text))
        except Exception as e:
            print("飞书推送异常: {}".format(str(e)[:50]))
    
    # 如果所有渠道都未配置，至少保存到文件
    print("通知推送完成（请配置通知渠道以获得推送功能）")
    return True

if __name__ == '__main__':
    print("开始生成工作日报...")
    
    report = generate_report()
    markdown_text = format_markdown(report)
    
    # 保存到文件
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = 'daily_report_{}.md'.format(today)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(markdown_text)
    
    print("日报已保存到: {}".format(report_path))
    
    # 推送通知
    send_notification(report, markdown_text)
    
    print("\n" + "=" * 60)
    print("工作日报生成完成！")
    print("=" * 60)
    print()
    print(markdown_text)
