# -*- coding: utf-8 -*-
"""
阿不 TVBox - 多渠道智能采集系统
功能：从多个活跃维护者处自动采集、验证高质量 4K/高清源
作者：WinClaw AI | 定制：阿不
更新：2026-07-24
"""

import json
import requests
from datetime import datetime

class SourceCollector:
    def __init__(self):
        self.config_path = 'config.json'
        self.results_log = 'collection_results.json'
        self.existing_apis = set()
        
    def load_current_config(self):
        """加载当前配置，获取已有 API 列表"""
        with open(self.config_path, 'r', encoding='utf-8-sig') as f:
            config = json.load(f)
        self.existing_apis = {s.get('api') for s in config.get('sites', [])}
        print(f'[OK] 当前已有 {len(self.existing_apis)} 个唯一 API\n')
        
    def fetch_from_source(self, source_name, url):
        """从指定源获取配置"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                sites = data.get('sites', [])
                print(f'[OK] {source_name}: {len(sites)} 个站点')
                return sites
            else:
                print(f'[FAIL] {source_name}: HTTP {response.status_code}')
                return []
        except Exception as e:
            print(f'[ERROR] {source_name}: {str(e)[:50]}')
            return []
    
    def extract_testable_urls(self, site):
        """从站点配置中提取可测试的 URL"""
        ext = site.get('ext')
        url = None
        
        if isinstance(ext, str) and ext.startswith('http'):
            url = ext
        elif isinstance(ext, dict):
            # 优先查找 siteUrl/host/url/site 字段
            for key in ['siteUrl', 'host', 'url', 'site']:
                if key in ext:
                    value = ext[key]
                    if isinstance(value, list) and len(value) > 0:
                        url = value[0]
                        break
                    elif isinstance(value, str):
                        url = value
                        break
        
        return url
    
    def test_url_reachability(self, url):
        """测试 URL 是否真正可达且返回有效内容"""
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            size_kb = len(response.content) / 1024
            
            # 有效标准：HTTP 200 且内容大于 1KB
            if 200 <= response.status_code < 400 and size_kb > 1:
                return {'valid': True, 'size_kb': int(size_kb), 'status': response.status_code}
            else:
                return {'valid': False, 'size_kb': int(size_kb), 'reason': '太小或状态码异常'}
        except Exception as e:
            return {'valid': False, 'reason': str(e)[:50]}
    
    def collect_high_quality_sources(self):
        """执行完整采集流程"""
        print('='*70)
        print('阿不 TVBox - 多渠道采集系统')
        print('执行时间:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('='*70)
        
        # Step 1: 加载当前配置
        self.load_current_config()
        
        # Step 2: 定义采集源（按活跃度排序）
        sources = [
            {'name': 'qist-0821', 'url': 'https://raw.githubusercontent.com/qist/tvbox/master/0821.json'},
            {'name': 'qist-jsm', 'url': 'https://raw.githubusercontent.com/qist/tvbox/master/jsm.json'},
            {'name': 'fantaiying-m3u', 'url': 'https://raw.githubusercontent.com/fantaiying/Tv/main/0821.json'},
            {'name': 'yoursmile-xc', 'url': 'https://agit.ai/Yoursmile7/TVBox/raw/branch/master/XC.json'},
        ]
        
        all_candidates = []
        
        # Step 3: 批量采集
        print('\n【阶段 1】正在从各渠道采集...')
        print('-'*70)
        for src in sources:
            sites = self.fetch_from_source(src['name'], src['url'])
            for site in sites:
                # 只保留 type=3 且有 ext 参数的
                if site.get('type') == 3 and 'ext' in site:
                    api = site.get('api', '')
                    # 排除已存在的和新添加的 drpy 格式
                    if api and api not in self.existing_apis and './lib/drpy' not in api:
                        site['_source'] = src['name']
                        all_candidates.append(site)
        
        print(f'\n[STATS] 共采集到 {len(all_candidates)} 个候选源（排除重复和 drpy 格式）\n')
        
        # Step 4: 测试验证
        print('【阶段 2】正在 HTTP 验证可用性...')
        print('-'*70)
        verified = []
        failed = []
        
        for site in all_candidates:
            name = site.get('name', '').strip()[:20]
            api = site.get('api', '')
            url = self.extract_testable_urls(site)
            
            if not url:
                failed.append({'name': name, 'api': api, 'reason': '无可测试 URL'})
                continue
            
            result = self.test_url_reachability(url)
            
            if result['valid']:
                site['_test_result'] = result
                site['_test_url'] = url
                verified.append(site)
                safe_name = name.encode('ascii', 'ignore').decode()[:18]
                print(f'[PASS] {safe_name:<18} | Size:{result["size_kb"]>3}KB | API:{api[-25:]}')
            else:
                failed.append({'name': name, 'api': api, 'reason': result.get('reason', '测试失败')})
                safe_name = name.encode('ascii', 'ignore').decode()[:18]
                print(f'[FAIL] {safe_name:<18} | {result.get("reason", "")}')
        
        # Step 5: 去重并按质量排序
        unique_verified = {}
        for site in verified:
            api = site['api']
            size = site['_test_result']['size_kb']
            if api not in unique_verified or unique_verified[api]['_test_result']['size_kb'] < size:
                unique_verified[api] = site
        
        final_sources = sorted(unique_verified.values(), 
                             key=lambda x: x['_test_result']['size_kb'], 
                             reverse=True)
        
        # Step 6: 保存结果
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_candidates': len(all_candidates),
            'verified_count': len(verified),
            'failed_count': len(failed),
            'unique_sources': len(final_sources),
            'top_sources': [{
                'name': s.get('name'),
                'api': s.get('api'),
                'size_kb': s['_test_result']['size_kb'],
                'source': s.get('_source'),
                'ext': s.get('ext')
            } for s in final_sources[:10]],
            'failed_list': failed[:20]
        }
        
        with open(self.results_log, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Step 7: 输出统计
        print('\n' + '='*70)
        print('采集完成统计')
        print('='*70)
        print(f'总计采集：{len(all_candidates)} 个候选')
        print(f'验证通过：{len(verified)} 个')
        print(f'测试失败：{len(failed)} 个')
        print(f'最终可用：{len(final_sources)} 个（去重后）')
        print(f'\n[SAVED] 详细结果保存到 {self.results_log}')
        
        if final_sources:
            print('\n前 5 个推荐源:')
            for i, s in enumerate(final_sources[:5], 1):
                safe_name = s.get('name', '').encode('ascii', 'ignore').decode()[:18]
                print(f"{i}. {safe_name} | {s['_test_result']['size_kb']}KB | {s.get('_source')}")
        
        return results

if __name__ == '__main__':
    collector = SourceCollector()
    results = collector.collect_high_quality_sources()
