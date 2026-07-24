# -*- coding: utf-8 -*-
"""
阿不 TVBox - 多渠道自动采集系统
功能：从 qist/tvbox 等仓库自动采集高质量配置源，扩展备用源池
作者：WinClaw AI | 定制：阿不
创建时间：2026-07-24
"""

import json
import requests
from datetime import datetime

class SourceCollector:
    def __init__(self):
        self.collected_sites = []
        self.backup_pool = []
        
    def fetch_config(self, url):
        """获取配置 JSON"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'FAIL {url} - HTTP {response.status_code}')
                return None
        except Exception as e:
            print(f'FAIL {url} - {str(e)[:50]}')
            return None
    
    def extract_high_quality_sources(self, config, source_name):
        """从配置中提取高质量源"""
        sites = config.get('sites', [])
        high_quality = []
        
        # 筛选规则：优先选择 type=3 爬虫源
        priority_keywords = ['玩偶', '至臻', '虎斑', '原盘', '4K', '秒播']
        
        for site in sites:
            if site.get('type') != 3:
                continue
                
            name = site.get('name', '')
            api = site.get('api', '')
            
            # 评分逻辑
            score = 0
            if any(kw in name for kw in priority_keywords):
                score += 30
            if 'Guard' in api:
                score += 20
            if site.get('searchable', 0) == 1:
                score += 15
            
            # 只收集中高分源
            if score >= 30:
                # 添加来源标记
                site['_source'] = source_name
                site['_score'] = score
                high_quality.append(site)
        
        return high_quality
    
    def collect_from_known_repos(self):
        """从已知的高质量仓库采集"""
        known_configs = [
            {
                'name': 'qist-tvbox-0821',
                'url': 'https://raw.githubusercontent.com/qist/tvbox/master/0821.json'
            },
            {
                'name': 'qist-tvbox-jsm',
                'url': 'https://raw.githubusercontent.com/qist/tvbox/master/jsm.json'
            },
            {
                'name': 'qist-tvbox-fty',
                'url': 'https://raw.githubusercontent.com/qist/tvbox/master/fty.json'
            }
        ]
        
        all_sources = []
        
        for cfg in known_configs:
            print(f'\nDOWNLOAD 正在采集：{cfg["name"]}')
            config = self.fetch_config(cfg['url'])
            if config:
                sources = self.extract_high_quality_sources(config, cfg['name'])
                print(f'  OK 提取 {len(sources)} 个高质量源')
                all_sources.extend(sources)
            else:
                print(f'  WARN 跳过（获取失败）')
        
        return all_sources
    
    def deduplicate_sources(self, sources):
        """去重：同一 API 只保留最高分的"""
        unique = {}
        
        for site in sources:
            api_key = site.get('api', '')
            score = site.get('_score', 0)
            
            if api_key not in unique or unique[api_key]['_score'] < score:
                unique[api_key] = site
        
        return list(unique.values())
    
    def generate_backup_pool(self, sources):
        """生成备用源池 JSON"""
        backup_pool = []
        
        for site in sources:
            # 移除临时字段
            backup_site = {
                'key': site.get('key'),
                'name': f"💡[{site.get('_source', 'unknown')}] {site.get('name')}",
                'type': 3,
                'api': site.get('api'),
                'searchable': site.get('searchable', 1),
                'quickSearch': site.get('quickSearch', 1),
                'changeable': 0,
                '_meta_score': site.get('_score', 0),
                '_meta_source': site.get('_source', '')
            }
            backup_pool.append(backup_site)
        
        return backup_pool
    
    def save_to_file(self, backup_pool, output_path='backup_sources.json'):
        """保存备用源池到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(backup_pool, f, indent=2, ensure_ascii=False)
        print(f'\nOK 备用源池已保存：{output_path}')
        print(f'BOX 总计 {len(backup_pool)} 个备用源')
    
    def run_full_collection(self):
        """执行完整采集流程"""
        print('='*60)
        print('[START] 开始阿不 TVBox 多渠道采集')
        print('='*60)
        
        # Step 1: 从已知仓库采集
        all_sources = self.collect_from_known_repos()
        
        if not all_sources:
            print('\nWARN 未采集到任何源，请检查网络连接')
            return
        
        print(f'\nSTATS 初始采集：{len(all_sources)} 个源')
        
        # Step 2: 去重
        unique_sources = self.deduplicate_sources(all_sources)
        print(f'UNIQUE 去重后：{len(unique_sources)} 个唯一 API')
        
        # Step 3: 生成备用池
        backup_pool = self.generate_backup_pool(unique_sources)
        
        # Step 4: 保存
        self.save_to_file(backup_pool)
        
        print('\n' + '='*60)
        print('DONE 采集完成！')
        print('='*60)
        
        # 统计信息
        api_types = {}
        for site in backup_pool:
            api = site.get('api', '')
            prefix = api.split('_')[1] if len(api.split('_')) > 1 else 'unknown'
            api_types[prefix] = api_types.get(prefix, 0) + 1
        
        print('\nCHART 按类型统计:')
        for api_type, count in sorted(api_types.items(), key=lambda x: x[1], reverse=True):
            print(f'  {api_type}: {count}个')

if __name__ == '__main__':
    collector = SourceCollector()
    collector.run_full_collection()

