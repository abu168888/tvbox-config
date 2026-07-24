# -*- coding: utf-8 -*-
"""
阿不 TVBox - 失效源追踪与自动清理
功能：
1. 记录每个站点的失效次数和日期
2. 连续 7 次失效后自动从配置中删除
3. 生成清理报告
"""

import json
import os
from datetime import datetime, timedelta

FAILURE_TRACK_FILE = 'failure_tracking.json'

def load_failure_tracking():
    """加载失效追踪记录"""
    if os.path.exists(FAILURE_TRACK_FILE):
        with open(FAILURE_TRACK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'failures': {}}

def save_failure_tracking(data):
    """保存失效追踪记录"""
    with open(FAILURE_TRACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_failure_record(site_key, failed_today):
    """更新站点失效记录"""
    tracking = load_failure_tracking()
    
    if site_key not in tracking['failures']:
        tracking['failures'][site_key] = []
    
    # 如果今天失败，记录日期
    today = datetime.now().strftime('%Y-%m-%d')
    if failed_today and today not in tracking['failures'][site_key]:
        tracking['failures'][site_key].append(today)
        # 只保留最近 30 天的记录
        tracking['failures'][site_key] = tracking['failures'][site_key][-30:]
    
    # 如果今天成功，清空记录
    elif not failed_today:
        tracking['failures'][site_key] = []
    
    save_failure_tracking(tracking)
    return tracking

def get_sites_to_remove(threshold_days=7):
    """获取应该删除的站点列表（连续失效>=阈值天数）"""
    tracking = load_failure_tracking()
    to_remove = []
    
    for site_key, fail_dates in tracking['failures'].items():
        # 检查是否连续失效
        if len(fail_dates) >= threshold_days:
            # 验证连续性
            dates_sorted = sorted(fail_dates)
            is_continuous = True
            
            for i in range(len(dates_sorted) - 1):
                d1 = datetime.strptime(dates_sorted[i], '%Y-%m-%d')
                d2 = datetime.strptime(dates_sorted[i+1], '%Y-%m-%d')
                if (d2 - d1).days > 1:
                    is_continuous = False
                    break
            
            # 检查最后一次失效是否在 1 天内
            last_fail = datetime.strptime(dates_sorted[-1], '%Y-%m-%d')
            days_since_last = (datetime.now() - last_fail).days
            
            if is_continuous and days_since_last <= 1:
                to_remove.append({
                    'key': site_key,
                    'fail_count': len(fail_dates),
                    'last_fail': dates_sorted[-1]
                })
    
    return to_remove

def remove_sites_from_config(config_path, sites_to_remove):
    """从配置中删除指定站点"""
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    
    original_count = len(config.get('sites', []))
    
    # 过滤掉要删除的站点
    filtered_sites = [
        site for site in config.get('sites', [])
        if site.get('key') not in [s['key'] for s in sites_to_remove]
    ]
    
    removed_count = original_count - len(filtered_sites)
    
    if removed_count > 0:
        config['sites'] = filtered_sites
        
        # 保存
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f'[OK] 已删除 {removed_count} 个长期失效站点')
        return True
    else:
        print('[INFO] 无站点需要删除')
        return False

def main():
    print('='*70)
    print('阿不 TVBox - 失效源追踪与清理')
    print('执行时间:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('='*70)
    
    # Step 1: 检查需要删除的站点
    to_remove = get_sites_to_remove(threshold_days=7)
    
    if to_remove:
        print(f'\n[WARN] 发现 {len(to_remove)} 个长期失效站点（连续 7 天）:')
        for site in to_remove:
            print(f"  - {site['key']}: 失效{site['fail_count']}次，最后失效于{site['last_fail']}")
        
        # Step 2: 执行删除
        confirm = input('\n确认删除这些站点？(y/N): ')
        if confirm.lower() == 'y':
            remove_sites_from_config('config.json', to_remove)
            
            # 清除已删除站点的追踪记录
            tracking = load_failure_tracking()
            for site in to_remove:
                if site['key'] in tracking['failures']:
                    del tracking['failures'][site['key']]
            save_failure_tracking(tracking)
            
            print('\n[SUCCESS] 清理完成！')
        else:
            print('\n[SKIP] 已取消删除操作')
    else:
        print('\n[OK] 没有连续失效 7 天的站点，无需清理')
    
    # Step 3: 显示当前追踪状态
    tracking = load_failure_tracking()
    print(f'\n[STATS] 当前追踪着 {len(tracking["failures"])} 个站点的失效记录')
    
    if tracking['failures']:
        print('\n最近有失效记录的站点:')
        for key, dates in list(tracking['failures'].items())[:5]:
            print(f"  - {key}: {len(dates)}次 (最近:{dates[-1]})")

if __name__ == '__main__':
    main()
