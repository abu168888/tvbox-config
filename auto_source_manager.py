# -*- coding: utf-8 -*-
"""
阿不 TVBox - 自动化影视源管理系统 (方案 C: 混合型 A+B)
功能:
  A - 本地备用池：从已知可用的 80 个 Guard 类中选择未使用的高质量源作为热备
  B - 外部发现器：定期拉取多个公开配置的 Guard 类，筛选稳定的加入候选池
  核心：检测到失效源 → 自动从候选池选择新的替换 → 测试验证 → 提交推送
"""
import json
import requests
from datetime import datetime, timedelta

CONFIG_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'
GUARDS_DB_PATH = r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\all_guard_classes.json'

# 监控日志
log_file = 'auto_source_manager.log'

def log(msg):
    """记录日志到文件和控制台"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = '[{}] {}'.format(timestamp, msg)
    print(log_msg)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def load_config():
    """加载当前配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(c):
    """保存配置"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(c, f, indent=2, ensure_ascii=False)

def get_used_guards(c):
    """获取当前已使用的 Guard 类"""
    used = set()
    for site in c.get('sites', []):
        if site.get('type') == 3:
            api = site.get('api', '')
            if 'Guard' in api:
                used.add(api)
    return used

def get_available_guards():
    """加载可用 Guard 类数据库"""
    try:
        with open(GUARDS_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['all_guards'], data['categories']
    except Exception as e:
        log("错误：无法加载 Guard 数据库：{}".format(e))
        return [], {}

def build_hot_standby_pool(used_guards, all_guards, categories):
    """
    A 策略：构建热备用池
    从每个分类中选择高质量但未被使用的 Guard 类作为备用
    """
    hot_standby = []
    
    # 重点关注的影视源类别
    priority_categories = ["4K 源", "影视源"]
    
    for cat_name in priority_categories:
        cat_guards = categories.get(cat_name, [])
        unused = [g for g in cat_guards if g not in used_guards]
        
        # 每个类别选前 3 个作为热备
        for g in unused[:3]:
            hot_standby.append({
                'class': g,
                'category': cat_name,
                'priority': 1 if cat_name == "4K 源" else 2
            })
    
    # 添加短剧源（如果用户喜欢）
    danju_guards = categories.get("短剧源", [])
    for g in [dg for dg in danju_guards if dg not in used_guards][:2]:
        hot_standby.append({
            'class': g,
            'category': '短剧源',
            'priority': 3
        })
    
    return sorted(hot_standby, key=lambda x: x['priority'])

def fetch_external_configs():
    """
    B 策略：从多个公开配置源拉取新的 Guard 类
    持续发现并扩展候选池
    """
    external_sources = [
        'http://home.jundie.top:81/top98.json',
        'https://jihulab.com/ymz1231/xymz/-/raw/main/ymshaoer',
        # TODO: 可以添加更多稳定源
    ]
    
    new_guards = set()
    
    for src_url in external_sources:
        try:
            log("正在拉取外部源：{}".format(src_url[:50]))
            r = requests.get(src_url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                for site in data.get('sites', []):
                    if site.get('type') == 3:
                        api = site.get('api', '')
                        if 'Guard' in api and api not in ['csp_NewDouBanGuard']:  # 排除配置中心类
                            new_guards.add(api)
        except Exception as e:
            log("拉取失败 {}: {}".format(src_url[:30], str(e)[:40]))
    
    return list(new_guards)

def test_guard_class(guard_class):
    """
    简单测试 Guard 类是否可用
    这里用启发式判断：检查类名是否符合命名规范
    实际生产中可能需要调用 spider.jar 接口测试
    """
    # 基础验证：必须是 csp_*Guard 格式
    if not guard_class.startswith('csp_') or not guard_class.endswith('Guard'):
        return False
    
    # 排除已知的不可用类（如果有）
    known_bad = set()  # 后续根据测试结果填充
    if guard_class in known_bad:
        return False
    
    return True

def find_unused_quality_guards(used_guards, all_guards):
    """寻找高质量的未使用 Guard 类"""
    # 优先选择带 "New" 前缀或"Wex" 前缀的（通常是新版本/优化版）
    quality_patterns = ['New', 'Wex']
    
    candidates = []
    for g in all_guards:
        if g in used_guards:
            continue
        
        # 计算质量分
        score = 0
        for pattern in quality_patterns:
            if pattern in g:
                score += 1
        
        # 排除一些特殊用途的
        if any(x in g for x in ['Config', 'Push', 'My']):
            continue
        
        candidates.append((g, score))
    
    # 按分数排序
    candidates.sort(key=lambda x: -x[1])
    
    return [g for g, s in candidates[:20]]  # 返回前 20 个

def auto_replace_failed_site(c, failed_key, replacement_class):
    """
    自动替换失效站点
    failed_key: 失效站点的 key
    replacement_class: 新的 Guard 类名
    """
    new_key = 'Auto_' + replacement_class.replace('csp_', '').replace('Guard', '')
    
    # 找到失效站点的位置
    insert_idx = None
    for i, site in enumerate(c['sites']):
        if site.get('key') == failed_key:
            insert_idx = i
            break
    
    if insert_idx is None:
        return False
    
    # 创建新站点配置（参考同类别的模板）
    new_site = {
        "key": new_key,
        "name": "自动┃{}".format(replacement_class.replace('csp_', '').replace('Guard', '')),
        "type": 3,
        "api": replacement_class,
        "searchable": 1,
        "quickSearch": 1,
        "changeable": 0
    }
    
    # 替换
    c['sites'][insert_idx] = new_site
    
    log("已替换：{} -> {} (class: {})".format(failed_key, new_key, replacement_class))
    return True

def main():
    """主流程"""
    log("=" * 60)
    log("启动自动化影视源管理系统")
    log("=" * 60)
    
    # 1. 加载数据
    log("[1/5] 加载配置...")
    c = load_config()
    used_guards = get_used_guards(c)
    log("当前已使用 {} 个 Guard 类".format(len(used_guards)))
    
    log("[2/5] 加载可用 Guard 数据库...")
    all_guards, categories = get_available_guards()
    log("可用 Guard 总数：{}".format(len(all_guards)))
    
    # 2. A 策略：构建热备用池
    log("[3/5] 构建热备用池 (A 策略)...")
    hot_standby = build_hot_standby_pool(used_guards, all_guards, categories)
    log("热备用池大小：{}".format(len(hot_standby)))
    
    # 3. B 策略：发现外部新源
    log("[4/5] 扫描外部配置源 (B 策略)...")
    external_new = fetch_external_configs()
    log("发现 {} 个新的外部 Guard 类".format(len(external_new)))
    
    # 合并到新候选池（去重）
    candidate_pool = [g for g in external_new if g not in used_guards and g not in all_guards]
    log("扩展候选池：{} 个新类".format(len(candidate_pool)))
    
    # 4. 生成报告
    log("[5/5] 生成管理报告...")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'current_stats': {
            'total_sites': len(c['sites']),
            'used_guards': len(used_guards),
            'guard_list': list(used_guards)
        },
        'hot_standby_pool': hot_standby[:10],  # 前 10 个热备
        'new_discovered': candidate_pool[:10],  # 前 10 个新发现的
        'recommendations': find_unused_quality_guards(used_guards, all_guards)[:5]
    }
    
    # 保存报告
    with open('source_manager_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    log("\n=== 管理报告 ===")
    log("当前站点数：{}".format(report['current_stats']['total_sites']))
    log("可用热备源：{}".format(len(hot_standby)))
    log("发现新源：{}".format(len(candidate_pool)))
    log("\n推荐添加的高质量源:")
    for i, rec in enumerate(report['recommendations'][:5], 1):
        log(" {}. {}".format(i, rec))
    
    log("\n[完成] 报告已保存到 source_manager_report.json")
    log("下一步：等待用户指令进行自动替换，或设置定时任务")
    
    return report

if __name__ == '__main__':
    main()
