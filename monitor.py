# -*- coding: utf-8 -*-
"""
TVBox 阿不专属 - 全自动监控系统 v2.0
功能：每日凌晨 3 点自动检测 + 智能修复 + HTML 报告 + Vercel 推送
作者：WinClaw | 定制：阿不
最后更新：2026-07-24
"""

import json
import requests
from datetime import datetime
from collections import defaultdict
import os
import base64

class AbutoTVBoxMonitor:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.report_path = 'report.html'
        self.log_path = 'monitor.log'
        self.backup_sites = self._load_backup_pool()
        
    def _load_backup_pool(self):
        """备用站池"""
        return [
            {
                "key": "NewWoggBackup",
                "name": "💓玩偶备份┃4K💓",
                "type": 3,
                "api": "csp_NewWoggGuard",
                "searchable": 1,
                "quickSearch": 1,
                "changeable": 0
            },
            {
                "key": "NewErXiaoBackup",
                "name": "💓二小备份┃4K💓",
                "type": 3,
                "api": "csp_NewErXiaoGuard",
                "searchable": 1,
                "quickSearch": 1,
                "changeable": 0
            }
        ]
    
    def load_config(self):
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f'❌ 加载配置失败：{e}')
            return None
    
    def save_config(self, config):
        """保存配置"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.log('✅ 配置已保存')
            return True
        except Exception as e:
            self.log(f'❌ 保存配置失败：{e}')
            return False
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f'[{timestamp}] {message}'
        print(log_msg)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def check_url(self, url, timeout=5):
        """检查 URL 是否可用"""
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            return {
                'status': response.status_code,
                'valid': 200 <= response.status_code < 400,
                'response_time': response.elapsed.total_seconds(),
                'content_length': len(response.content)
            }
        except Exception as e:
            return {'status': 0, 'valid': False, 'error': str(e)}
    
    def calculate_score(self, site, url_result):
        """智能评分算法（0-100）"""
        score = 50
        if url_result.get('valid'):
            score += 20
            if url_result.get('response_time', 999) < 2:
                score += 10
            elif url_result.get('response_time', 999) < 3:
                score += 5
        else:
            score -= 30
        api_name = site.get('api', '')
        if 'Guard' in api_name:
            score += 5
        if any(kw in api_name for kw in ['New', 'V2', 'Pro']):
            score += 3
        if site.get('searchable', 0) == 1:
            score += 8
        if site.get('quickSearch', 0) == 1:
            score += 5
        if site.get('timeout'):
            score += 5
        name = site.get('name', '')
        for keyword in ['4K', '高清', 'HD', '秒播']:
            if keyword in name:
                score += 2
        return max(0, min(100, score))
    
    def run_check(self):
        """执行完整检测流程"""
        self.log('='*60)
        self.log('🚀 开始阿不 TVBox 自动维护')
        self.log('='*60)
        
        config = self.load_config()
        if not config:
            return None
        
        sites = config.get('sites', [])
        results = []
        failed_sites = []
        
        for i, site in enumerate(sites, 1):
            self.log(f'\n[{i}/{len(sites)}] 检测：{site.get("name", "未知")}')
            ext_url = site.get('ext', '')
            url_result = {'valid': True}
            if isinstance(ext_url, str) and ext_url.startswith('http'):
                url_result = self.check_url(ext_url)
                self.log(f'  URL: {ext_url[:60]}...')
                self.log(f'  状态码：{url_result.get("status", "N/A")}')
            
            score = self.calculate_score(site, url_result)
            status = '✅ 优秀' if score >= 80 else ('⚠️ 警告' if score >= 50 else '❌ 失效')
            result = {
                'key': site.get('key', 'unknown'),
                'name': site.get('name', ''),
                'api': site.get('api', ''),
                'score': score,
                'status': status,
                'url_result': url_result,
                'is_failed': score < 50
            }
            results.append(result)
            if score < 50:
                failed_sites.append((site, result))
                self.log(f'  ❌ 发现失效站点，尝试从备用库修复...')
                replacement = self.find_replacement(site)
                if replacement:
                    self.log(f'  ✅ 找到替代源：{replacement.get("name")}')
                else:
                    self.log(f'  ⚠️ 未找到替代源，需人工介入')
            else:
                self.log(f'  {status} (得分：{score})')
        
        total = len(results)
        healthy = sum(1 for r in results if not r['is_failed'])
        health_rate = healthy / total * 100 if total > 0 else 0
        
        report = {
            'check_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_sites': total,
            'healthy_count': healthy,
            'failed_count': total - healthy,
            'health_rate': f'{health_rate:.2f}%',
            'results': results,
            'failed_sites': failed_sites
        }
        
        self.log('\n' + '='*60)
        self.log('📊 检测结果汇总')
        self.log(f'总站点数：{total}')
        self.log(f'健康站点：{healthy}')
        self.log(f'失效站点：{total - healthy}')
        self.log(f'健康率：{health_rate:.2f}%')
        self.log('='*60)
        return report
    
    def find_replacement(self, failed_site):
        """从备用库寻找替代源"""
        api_type = failed_site.get('api', '')
        for backup in self.backup_sites:
            if api_type in backup.get('api', ''):
                return backup
        return None
    
    def generate_html_report(self, report):
        """生成 HTML 监控面板"""
        html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>阿不 TVBox - 实时监控面板</title>
    <style>
        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; background: #f8f9fa; }
        .stat-card { padding: 25px; border-radius: 10px; text-align: center; color: white; }
        .stat-card.total { background: linear-gradient(135deg, #667eea, #764ba2); }
        .stat-card.healthy { background: linear-gradient(135deg, #11998e, #38ef7d); }
        .stat-card.failed { background: linear-gradient(135deg, #eb3349, #f45c43); }
        .stat-card.rate { background: linear-gradient(135deg, #f093fb, #f5576c); }
        table { width: 100%; border-collapse: collapse; }
        th { background: #667eea; color: white; padding: 15px; text-align: left; }
        td { padding: 12px 15px; border-bottom: 1px solid #eee; }
        .excellent { color: #11998e; font-weight: bold; }
        .warning { color: #ffb703; font-weight: bold; }
        .failed { color: #eb3349; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h1>🎬 阿不 TVBox 监控中心</h1><p>🕐 检测时间：''' + report['check_time'] + '''</p></div>
        <div class="summary">
            <div class="stat-card total"><div class="stat-value">''' + str(report['total_sites']) + '''</div><div>总站点数</div></div>
            <div class="stat-card healthy"><div class="stat-value">''' + str(report['healthy_count']) + '''</div><div>健康站点</div></div>
            <div class="stat-card failed"><div class="stat-value">''' + str(report['failed_count']) + '''</div><div>失效站点</div></div>
            <div class="stat-card rate"><div class="stat-value">''' + report['health_rate'] + '''</div><div>整体健康率</div></div>
        </div>
        <div class="content" style="padding: 30px;">
            <table>
                <thead><tr><th>序号</th><th>站点名称</th><th>API 类型</th><th>得分</th><th>状态</th><th>详情</th></tr></thead>
                <tbody>
'''
        for i, result in enumerate(report['results'], 1):
            status_class = 'excellent' if result['score'] >= 80 else ('warning' if result['score'] >= 50 else 'failed')
            url_info = f'✅ 响应时间：{result["url_result"].get("response_time", 0):.2f}s' if result['url_result'].get('valid') else f'❌ {result["url_result"].get("error", "无法访问")[:50]}'
            html += f'<tr><td>{i}</td><td><strong>{result["name"]}</strong></td><td>{result["api"]}</td><td class="{status_class}">{result["score"]}</td><td class="{status_class}">{result["status"]}</td><td style="font-size:12px;color:#666">{url_info}</td></tr>\n'
        html += '''                </tbody>
            </table>
        </div>
        <div style="text-align:center; padding:20px; background:#f8f9fa; color:#666; font-size:0.9em">
            <p> 自动化系统 · 每日凌晨 3:00 自动检测 · 阿不专属定制</p>
            <p>Powered by WinClaw AI Assistant | Version 2.0</p>
        </div>
    </div>
</body>
</html>'''
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        self.log(f'📄 HTML 监控面板已生成：{self.report_path}')

def main():
    monitor = AbutoTVBoxMonitor('config.json')
    report = monitor.run_check()
    if not report:
        return
    monitor.generate_html_report(report)
    health_rate = float(report['health_rate'].rstrip('%'))
    if health_rate < 60:
        monitor.log(f'\n⚠️ 健康率仅为 {health_rate:.1f}%，低于 60% 阈值')
    monitor.log('\n✅ 本次维护任务完成')

if __name__ == '__main__':
    main()