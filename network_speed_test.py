#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络测速脚本
测试搜索引擎站点和AI模型API的连接速度和可用性
"""

import time
import requests
import concurrent.futures
from urllib.parse import urlparse
import json
import sys
import os
from datetime import datetime
try:
    from dotenv import load_dotenv
except ImportError:
    print("⚠️  python-dotenv 未安装，将跳过 .env 文件加载")
    def load_dotenv():
        pass

# 加载环境变量
load_dotenv()

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

# AI模型API站点配置
def get_ai_model_urls():
    """获取AI模型API的URL地址"""
    ai_urls = {
        'openai': 'https://api.openai.com/v1',
        'anthropic': 'https://api.anthropic.com',
        'groq': 'https://api.groq.com/openai/v1',
        'google_ai': 'https://generativelanguage.googleapis.com/v1beta',
        'mistralai': 'https://api.mistral.ai/v1',
        'deepseek': 'https://api.deepseek.com/v1',
        'huggingface': 'https://api-inference.huggingface.co',
        'openrouter': os.getenv('OPEN_ROUTER_BASE_URL', 'https://openrouter.ai/api/v1'),
        'sambanova': os.getenv('SAMBANOVA_BASE_URL', 'https://fast-api.snova.ai/v1'),
    }

    # 添加本地/内网服务
    ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
    lmstudio_url = os.getenv('LM_STUDIO_BASE_URL', 'http://127.0.0.1:1234')

    if ollama_url:
        ai_urls['ollama'] = ollama_url
    if lmstudio_url:
        ai_urls['lmstudio'] = lmstudio_url.replace('/v1', '')

    return ai_urls

# 请求配置
REQUEST_CONFIG = {
    'timeout': 10,  # 超时时间（秒）
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
}

def test_single_site(name, url, site_type='search'):
    """测试单个站点的连接速度"""
    result = {
        'name': name,
        'url': url,
        'type': site_type,
        'status': 'unknown',
        'response_time': None,
        'status_code': None,
        'error': None
    }

    try:
        start_time = time.time()

        # 为内网地址禁用代理
        proxies = None
        if any(addr in url for addr in ['127.0.0.1', 'localhost', '10.', '192.168.', '172.']):
            proxies = {'http': '', 'https': ''}

        response = requests.get(
            url,
            timeout=REQUEST_CONFIG['timeout'],
            headers=REQUEST_CONFIG['headers'],
            allow_redirects=True,
            proxies=proxies
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

def test_ai_api_site(name, base_url):
    """测试AI API站点的连接速度和可用性"""
    result = {
        'name': name,
        'url': base_url,
        'type': 'ai_api',
        'status': 'unknown',
        'response_time': None,
        'status_code': None,
        'error': None
    }

    try:
        start_time = time.time()

        # 为内网地址禁用代理
        proxies = None
        if any(addr in base_url for addr in ['127.0.0.1', 'localhost', '10.', '192.168.', '172.']):
            proxies = {'http': '', 'https': ''}

        # 根据不同的API提供商选择合适的测试端点
        if name == 'ollama':
            # Ollama使用/api/tags端点获取模型列表
            test_url = f"{base_url}/api/tags"
            response = requests.get(test_url, timeout=REQUEST_CONFIG['timeout'], proxies=proxies)
        elif name == 'lmstudio':
            # LM Studio使用/v1/models端点
            test_url = f"{base_url}/v1/models"
            response = requests.get(test_url, timeout=REQUEST_CONFIG['timeout'], proxies=proxies)
        elif name == 'anthropic':
            # Anthropic使用/v1/messages端点，发送HEAD请求测试连接
            test_url = f"{base_url}/v1/messages"
            response = requests.head(test_url, timeout=REQUEST_CONFIG['timeout'], proxies=proxies)
        elif name == 'huggingface':
            # Hugging Face直接测试基础URL
            response = requests.get(base_url, timeout=REQUEST_CONFIG['timeout'],
                                  headers=REQUEST_CONFIG['headers'], proxies=proxies)
        else:
            # 其他API使用/models端点（OpenAI兼容）
            test_url = f"{base_url}/models"
            response = requests.get(test_url, timeout=REQUEST_CONFIG['timeout'], proxies=proxies)

        end_time = time.time()

        result['response_time'] = round((end_time - start_time) * 1000, 2)  # 毫秒
        result['status_code'] = response.status_code

        # 对于AI API，我们接受更多的状态码作为"可用"
        if response.status_code in [200, 401, 403, 405]:  # 200=成功, 401/403=需要认证, 405=方法不允许但服务可用
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
    print("🚀 开始测试网络连接速度...")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⚙️  超时设置: {REQUEST_CONFIG['timeout']}秒")
    print("-" * 80)

    results = []

    # 获取所有要测试的站点
    all_sites = []

    # 添加搜索引擎站点
    for name, url in SEARCH_ENGINES.items():
        all_sites.append((name, url, 'search'))

    # 添加AI模型API站点
    ai_urls = get_ai_model_urls()
    for name, url in ai_urls.items():
        all_sites.append((name, url, 'ai_api'))

    print(f"📋 测试站点总数: {len(all_sites)} (搜索引擎: {len(SEARCH_ENGINES)}, AI模型API: {len(ai_urls)})")
    print("-" * 80)

    # 使用线程池并发测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(all_sites), 10)) as executor:
        future_to_site = {}

        # 为不同类型的站点使用不同的测试函数
        for name, url, site_type in all_sites:
            if site_type == 'ai_api':
                future = executor.submit(test_ai_api_site, name, url)
            else:
                future = executor.submit(test_single_site, name, url, site_type)
            future_to_site[future] = (name, url, site_type)

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

            type_emoji = {
                'search': '🔍',
                'ai_api': '🤖'
            }

            emoji = status_emoji.get(result['status'], '❓')
            type_icon = type_emoji.get(result['type'], '🌐')

            if result['response_time']:
                print(f"{emoji} {type_icon} {result['name']:<15} | {result['response_time']:>6}ms | {result['status']}")
            else:
                print(f"{emoji} {type_icon} {result['name']:<15} | {'N/A':>6}   | {result['status']} - {result['error']}")

    return results

def analyze_results(results):
    """分析测试结果"""
    print("\n" + "=" * 80)
    print("📊 详细测试结果分析")
    print("=" * 80)

    # 按类型分组
    search_results = [r for r in results if r.get('type') == 'search']
    ai_results = [r for r in results if r.get('type') == 'ai_api']

    # 总体统计
    total = len(results)
    success_count = len([r for r in results if r['status'] == 'success'])
    timeout_count = len([r for r in results if r['status'] == 'timeout'])
    error_count = total - success_count - timeout_count

    print(f"总测试站点: {total}")
    print(f"成功连接: {success_count} ({success_count/total*100:.1f}%)")
    print(f"超时: {timeout_count} ({timeout_count/total*100:.1f}%)")
    print(f"错误: {error_count} ({error_count/total*100:.1f}%)")

    # 分类显示结果
    if search_results:
        print(f"\n🔍 搜索引擎站点 ({len(search_results)}个):")
        search_success = [r for r in search_results if r['status'] == 'success']
        search_failed = [r for r in search_results if r['status'] != 'success']

        if search_success:
            search_success.sort(key=lambda x: x['response_time'])
            print("  ✅ 可用站点:")
            for result in search_success:
                print(f"    • {result['name']}: {result['response_time']}ms")

        if search_failed:
            print("  ❌ 不可用站点:")
            for result in search_failed:
                print(f"    • {result['name']}: {result['status']} - {result.get('error', 'N/A')}")

    if ai_results:
        print(f"\n🤖 AI模型API站点 ({len(ai_results)}个):")
        ai_success = [r for r in ai_results if r['status'] == 'success']
        ai_failed = [r for r in ai_results if r['status'] != 'success']

        if ai_success:
            ai_success.sort(key=lambda x: x['response_time'])
            print("  ✅ 可用API:")
            for result in ai_success:
                print(f"    • {result['name']}: {result['response_time']}ms ({result['url']})")

        if ai_failed:
            print("  ❌ 不可用API:")
            for result in ai_failed:
                print(f"    • {result['name']}: {result['status']} - {result.get('error', 'N/A')} ({result['url']})")

    # 最快的站点（所有类型）
    successful_results = [r for r in results if r['status'] == 'success']
    if successful_results:
        successful_results.sort(key=lambda x: x['response_time'])
        print(f"\n🏆 响应最快的站点 (所有类型):")
        for i, result in enumerate(successful_results[:5], 1):
            type_icon = '🔍' if result.get('type') == 'search' else '🤖'
            print(f"  {i}. {type_icon} {result['name']}: {result['response_time']}ms")

    return {
        'total': total,
        'success': success_count,
        'timeout': timeout_count,
        'error': error_count,
        'success_rate': success_count/total*100,
        'search_results': search_results,
        'ai_results': ai_results
    }

def save_results(results, stats):
    """保存测试结果到JSON文件 - 已禁用文件保存"""
    # 不生成文件，只显示信息
    print(f"\n💾 测试结果统计完成 (未保存文件)")
    return None

def main():
    """主函数"""
    print("🌐 网络连接测速工具 (搜索引擎 + AI模型API)")
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
        search_success_rate = len([r for r in stats.get('search_results', []) if r['status'] == 'success']) / max(len(stats.get('search_results', [])), 1) * 100
        ai_success_rate = len([r for r in stats.get('ai_results', []) if r['status'] == 'success']) / max(len(stats.get('ai_results', [])), 1) * 100

        if stats['success_rate'] < 50:
            print("  • 网络连接质量较差，建议检查网络设置或使用代理")
            print("  • 考虑增加超时时间设置")
        elif stats['timeout'] > 0:
            print("  • 部分站点响应较慢，建议增加超时时间")

        if search_success_rate < 50:
            print("  • 搜索引擎连接较差，Searx可能无法正常工作")
        elif search_success_rate >= 80:
            print("  • 搜索引擎连接良好，Searx应该能正常工作")

        if ai_success_rate < 50:
            print("  • AI模型API连接较差，建议检查API配置和网络")
        elif ai_success_rate >= 80:
            print("  • AI模型API连接良好，模型应该能正常工作")

        print(f"\n✨ 测试完成! 总体成功率: {stats['success_rate']:.1f}%")
        print(f"   🔍 搜索引擎成功率: {search_success_rate:.1f}%")
        print(f"   🤖 AI模型API成功率: {ai_success_rate:.1f}%")

    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
