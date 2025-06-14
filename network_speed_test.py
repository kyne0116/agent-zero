#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Searx搜索引擎网络测速脚本
测试各个搜索引擎站点的连接速度和可用性
"""

import time
import requests
import concurrent.futures
from urllib.parse import urlparse
import json
import sys
from datetime import datetime

# 搜索引擎站点配置
SEARCH_ENGINES = {
    'google': 'https://www.google.com',
    'duckduckgo': 'https://html.duckduckgo.com',
    'wikipedia': 'https://en.wikipedia.org',
    'wikidata': 'https://www.wikidata.org',
    'startpage': 'https://www.startpage.com',
    'brave': 'https://search.brave.com',
    'bing': 'https://www.bing.com',
    'yandex': 'https://yandex.com',
    'searx_instance': 'https://searx.be'  # 公共searx实例
}

# 请求配置
REQUEST_CONFIG = {
    'timeout': 10,  # 超时时间（秒）
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
}

def test_single_site(name, url):
    """测试单个站点的连接速度"""
    result = {
        'name': name,
        'url': url,
        'status': 'unknown',
        'response_time': None,
        'status_code': None,
        'error': None
    }
    
    try:
        start_time = time.time()
        response = requests.get(
            url, 
            timeout=REQUEST_CONFIG['timeout'],
            headers=REQUEST_CONFIG['headers'],
            allow_redirects=True
        )
        end_time = time.time()
        
        result['response_time'] = round((end_time - start_time) * 1000, 2)  # 毫秒
        result['status_code'] = response.status_code
        
        if response.status_code == 200:
            result['status'] = 'success'
        else:
            result['status'] = 'error'
            result['error'] = f'HTTP {response.status_code}'
            
    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
        result['error'] = f'Timeout after {REQUEST_CONFIG["timeout"]}s'
    except requests.exceptions.ConnectionError as e:
        result['status'] = 'connection_error'
        result['error'] = f'Connection error: {str(e)[:100]}'
    except Exception as e:
        result['status'] = 'error'
        result['error'] = f'Unknown error: {str(e)[:100]}'
    
    return result

def test_all_sites():
    """并发测试所有站点"""
    print("🚀 开始测试搜索引擎站点连接速度...")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⚙️  超时设置: {REQUEST_CONFIG['timeout']}秒")
    print("-" * 80)
    
    results = []
    
    # 使用线程池并发测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SEARCH_ENGINES)) as executor:
        future_to_site = {
            executor.submit(test_single_site, name, url): (name, url)
            for name, url in SEARCH_ENGINES.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_site):
            result = future.result()
            results.append(result)
            
            # 实时显示结果
            status_emoji = {
                'success': '✅',
                'timeout': '⏰',
                'connection_error': '❌',
                'error': '⚠️',
                'unknown': '❓'
            }
            
            emoji = status_emoji.get(result['status'], '❓')
            if result['response_time']:
                print(f"{emoji} {result['name']:<15} | {result['response_time']:>6}ms | {result['status']}")
            else:
                print(f"{emoji} {result['name']:<15} | {'N/A':>6}   | {result['status']} - {result['error']}")
    
    return results

def analyze_results(results):
    """分析测试结果"""
    print("\n" + "=" * 80)
    print("📊 测试结果分析")
    print("=" * 80)
    
    # 统计
    total = len(results)
    success_count = len([r for r in results if r['status'] == 'success'])
    timeout_count = len([r for r in results if r['status'] == 'timeout'])
    error_count = total - success_count - timeout_count
    
    print(f"总测试站点: {total}")
    print(f"成功连接: {success_count} ({success_count/total*100:.1f}%)")
    print(f"超时: {timeout_count} ({timeout_count/total*100:.1f}%)")
    print(f"错误: {error_count} ({error_count/total*100:.1f}%)")
    
    # 成功连接的站点按速度排序
    successful_results = [r for r in results if r['status'] == 'success']
    if successful_results:
        successful_results.sort(key=lambda x: x['response_time'])
        print(f"\n🏆 最快的站点:")
        for i, result in enumerate(successful_results[:3], 1):
            print(f"  {i}. {result['name']}: {result['response_time']}ms")
    
    # 问题站点
    problem_results = [r for r in results if r['status'] != 'success']
    if problem_results:
        print(f"\n⚠️  有问题的站点:")
        for result in problem_results:
            print(f"  • {result['name']}: {result['status']} - {result['error']}")
    
    return {
        'total': total,
        'success': success_count,
        'timeout': timeout_count,
        'error': error_count,
        'success_rate': success_count/total*100
    }

def save_results(results, stats):
    """保存测试结果到JSON文件 - 已禁用文件保存"""
    # 不生成文件，只显示信息
    print(f"\n💾 测试结果统计完成 (未保存文件)")
    return None

def main():
    """主函数"""
    print("🌐 Searx搜索引擎网络测速工具")
    print("=" * 80)
    
    try:
        # 执行测试
        results = test_all_sites()
        
        # 分析结果
        stats = analyze_results(results)
        
        # 保存结果（不生成文件）
        save_results(results, stats)
        
        # 给出建议
        print("\n💡 建议:")
        if stats['success_rate'] < 50:
            print("  • 网络连接质量较差，建议检查网络设置或使用代理")
            print("  • 考虑增加searx的超时时间设置")
        elif stats['timeout'] > 0:
            print("  • 部分站点响应较慢，建议增加超时时间")
        else:
            print("  • 网络连接良好，searx应该能正常工作")
        
        print(f"\n✨ 测试完成! 成功率: {stats['success_rate']:.1f}%")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
