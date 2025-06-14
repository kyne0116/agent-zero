#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI模型响应速度测试脚本
测试各个AI模型提供商的响应速度和可用性
"""

import time
import requests
import concurrent.futures
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

# 测试配置
REQUEST_CONFIG = {
    'timeout': 30,  # 30秒超时
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
}

# 标准测试消息
TEST_MESSAGE = "Hello, please respond with 'OK' to confirm you are working."

def load_settings():
    """加载设置文件"""
    try:
        with open('tmp/settings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 无法加载设置文件: {e}")
        return {}

def get_api_key(provider):
    """获取API密钥"""
    key_mapping = {
        'OPENAI': 'API_KEY_OPENAI',
        'ANTHROPIC': 'API_KEY_ANTHROPIC',
        'GROQ': 'API_KEY_GROQ',
        'GOOGLE': 'API_KEY_GOOGLE',
        'MISTRALAI': 'API_KEY_MISTRALAI',
        'OPENROUTER': 'API_KEY_OPENROUTER',
        'SAMBANOVA': 'API_KEY_SAMBANOVA',
        'DEEPSEEK': 'API_KEY_DEEPSEEK',
        'HUGGINGFACE': 'API_KEY_HUGGINGFACE'
    }
    
    env_key = key_mapping.get(provider.upper())
    if env_key:
        return os.getenv(env_key)
    return None

def get_base_url(provider):
    """获取基础URL"""
    url_mapping = {
        'OPENAI': 'https://api.openai.com/v1',
        'ANTHROPIC': 'https://api.anthropic.com',
        'GROQ': 'https://api.groq.com/openai/v1',
        'GOOGLE': 'https://generativelanguage.googleapis.com/v1beta',
        'MISTRALAI': 'https://api.mistral.ai/v1',
        'OPENROUTER': os.getenv('OPEN_ROUTER_BASE_URL', 'https://openrouter.ai/api/v1'),
        'SAMBANOVA': os.getenv('SAMBANOVA_BASE_URL', 'https://fast-api.snova.ai/v1'),
        'OLLAMA': os.getenv('OLLAMA_BASE_URL', 'http://10.92.82.168:11434'),
        'LMSTUDIO': os.getenv('LM_STUDIO_BASE_URL', 'http://127.0.0.1:1234/v1'),
        'DEEPSEEK': 'https://api.deepseek.com/v1',
        'HUGGINGFACE': 'https://api-inference.huggingface.co/models'
    }
    
    return url_mapping.get(provider.upper())

def test_openai_compatible(provider, model_name, api_key, base_url):
    """测试OpenAI兼容的API"""
    if not api_key and provider.upper() not in ['OLLAMA', 'LMSTUDIO']:
        return None, "缺少API密钥"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key or "none"}'
    }
    
    data = {
        'model': model_name,
        'messages': [
            {'role': 'user', 'content': TEST_MESSAGE}
        ],
        'max_tokens': 50,
        'temperature': 0
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=REQUEST_CONFIG['timeout']
        )
        end_time = time.time()
        
        response_time = round((end_time - start_time) * 1000, 2)
        
        if response.status_code == 200:
            return response_time, "成功"
        else:
            return None, f"HTTP {response.status_code}: {response.text[:100]}"
            
    except requests.exceptions.Timeout:
        return None, f"超时 ({REQUEST_CONFIG['timeout']}秒)"
    except requests.exceptions.ConnectionError as e:
        return None, f"连接错误: {str(e)[:100]}"
    except Exception as e:
        return None, f"未知错误: {str(e)[:100]}"

def test_anthropic(model_name, api_key):
    """测试Anthropic API"""
    if not api_key:
        return None, "缺少API密钥"
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01'
    }
    
    data = {
        'model': model_name,
        'max_tokens': 50,
        'messages': [
            {'role': 'user', 'content': TEST_MESSAGE}
        ]
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data,
            timeout=REQUEST_CONFIG['timeout']
        )
        end_time = time.time()
        
        response_time = round((end_time - start_time) * 1000, 2)
        
        if response.status_code == 200:
            return response_time, "成功"
        else:
            return None, f"HTTP {response.status_code}: {response.text[:100]}"
            
    except requests.exceptions.Timeout:
        return None, f"超时 ({REQUEST_CONFIG['timeout']}秒)"
    except requests.exceptions.ConnectionError as e:
        return None, f"连接错误: {str(e)[:100]}"
    except Exception as e:
        return None, f"未知错误: {str(e)[:100]}"

def test_ollama(model_name, base_url):
    """测试Ollama API"""
    data = {
        'model': model_name,
        'prompt': TEST_MESSAGE,
        'stream': False
    }

    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/api/generate",
            json=data,
            timeout=REQUEST_CONFIG['timeout']
        )
        end_time = time.time()

        response_time = round((end_time - start_time) * 1000, 2)

        if response.status_code == 200:
            return response_time, "成功"
        else:
            return None, f"HTTP {response.status_code}: {response.text[:100]}"

    except requests.exceptions.Timeout:
        return None, f"超时 ({REQUEST_CONFIG['timeout']}秒)"
    except requests.exceptions.ConnectionError as e:
        return None, f"连接错误: {str(e)[:100]}"
    except Exception as e:
        return None, f"未知错误: {str(e)[:100]}"

def test_single_model(config):
    """测试单个模型"""
    provider = config['provider']
    model_name = config['model_name']
    model_type = config.get('type', 'test')

    result = {
        'provider': provider,
        'model_name': model_name,
        'type': model_type,
        'status': 'unknown',
        'response_time': None,
        'error': None,
        'api_key_status': None,
        'base_url': None,
        'test_message': TEST_MESSAGE
    }

    api_key = get_api_key(provider)
    base_url = get_base_url(provider)

    result['base_url'] = base_url
    result['api_key_status'] = 'configured' if api_key else 'missing'

    try:
        if provider.upper() == 'ANTHROPIC':
            response_time, error = test_anthropic(model_name, api_key)
        elif provider.upper() == 'OLLAMA':
            response_time, error = test_ollama(model_name, base_url)
        else:
            # OpenAI兼容的API
            response_time, error = test_openai_compatible(provider, model_name, api_key, base_url)

        if response_time is not None:
            result['status'] = 'success'
            result['response_time'] = response_time
        else:
            result['status'] = 'error'
            result['error'] = error

    except Exception as e:
        result['status'] = 'error'
        result['error'] = f"测试异常: {str(e)[:100]}"

    return result

def get_test_models():
    """获取要测试的模型列表"""
    settings = load_settings()

    models_to_test = []

    # 从设置中获取当前配置的模型
    if 'chat_model_provider' in settings and 'chat_model_name' in settings:
        models_to_test.append({
            'provider': settings['chat_model_provider'],
            'model_name': settings['chat_model_name'],
            'type': 'chat'
        })

    if 'util_model_provider' in settings and 'util_model_name' in settings:
        models_to_test.append({
            'provider': settings['util_model_provider'],
            'model_name': settings['util_model_name'],
            'type': 'utility'
        })

    if 'embed_model_provider' in settings and 'embed_model_name' in settings:
        models_to_test.append({
            'provider': settings['embed_model_provider'],
            'model_name': settings['embed_model_name'],
            'type': 'embedding'
        })

    # 添加一些常用的测试模型
    common_models = [
        {'provider': 'OPENAI', 'model_name': 'gpt-3.5-turbo', 'type': 'test'},
        {'provider': 'OPENAI', 'model_name': 'gpt-4', 'type': 'test'},
        {'provider': 'ANTHROPIC', 'model_name': 'claude-3-haiku-20240307', 'type': 'test'},
        {'provider': 'GROQ', 'model_name': 'llama3-8b-8192', 'type': 'test'},
        {'provider': 'OLLAMA', 'model_name': 'llama3.2', 'type': 'test'},
        {'provider': 'OPENROUTER', 'model_name': 'qwen/qwen3-32b:free', 'type': 'test'},
    ]

    # 只添加有API密钥的模型
    for model in common_models:
        if get_api_key(model['provider']) or model['provider'].upper() in ['OLLAMA', 'LMSTUDIO']:
            # 避免重复
            if not any(m['provider'] == model['provider'] and m['model_name'] == model['model_name'] for m in models_to_test):
                models_to_test.append(model)

    return models_to_test

def test_all_models():
    """并发测试所有模型"""
    models = get_test_models()

    if not models:
        print("❌ 未找到可测试的模型")
        return []

    print("🚀 开始测试AI模型响应速度...")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⚙️  超时设置: {REQUEST_CONFIG['timeout']}秒")
    print(f"📋 测试模型数量: {len(models)}")
    print(f"🔤 测试消息: {TEST_MESSAGE}")
    print("-" * 80)

    # 显示平台信息
    print("📡 平台配置信息:")
    providers_shown = set()
    for model in models:
        provider = model['provider']
        if provider not in providers_shown:
            providers_shown.add(provider)
            api_key = get_api_key(provider)
            base_url = get_base_url(provider)

            if api_key:
                # 隐藏API密钥，只显示前4位和后4位
                masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "****"
                print(f"  🔑 {provider}: API密钥 {masked_key}")
            else:
                print(f"  🌐 {provider}: {base_url}")

    print("-" * 80)

    # 显示模型类型配置
    print("🤖 模型类型配置:")
    settings = load_settings()
    model_types = {
        'chat': ('聊天模型', 'chat_model_provider', 'chat_model_name'),
        'utility': ('工具模型', 'util_model_provider', 'util_model_name'),
        'embedding': ('嵌入模型', 'embed_model_provider', 'embed_model_name')
    }

    for type_key, (type_name, provider_key, name_key) in model_types.items():
        if provider_key in settings and name_key in settings:
            print(f"  📋 {type_name}: {settings[provider_key]}/{settings[name_key]}")

    print("-" * 80)
    print("🧪 开始测试...")

    results = []

    # 使用线程池并发测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_model = {executor.submit(test_single_model, model): model for model in models}

        for future in concurrent.futures.as_completed(future_to_model):
            model = future_to_model[future]
            try:
                result = future.result()
                results.append(result)

                # 详细显示结果
                status_icon = "✅" if result['status'] == 'success' else "❌"
                model_type_icon = {
                    'chat': '💬',
                    'utility': '🔧',
                    'embedding': '🔗',
                    'test': '🧪'
                }.get(model.get('type', 'test'), '🤖')

                if result['status'] == 'success':
                    print(f"{status_icon} {model_type_icon} [{model.get('type', 'test').upper()}] {result['provider']}/{result['model_name']}: {result['response_time']}ms")
                else:
                    print(f"{status_icon} {model_type_icon} [{model.get('type', 'test').upper()}] {result['provider']}/{result['model_name']}: {result['error']}")

            except Exception as exc:
                print(f"❌ 🤖 [{model.get('type', 'test').upper()}] {model['provider']}/{model['model_name']}: 测试异常 - {exc}")
                results.append({
                    'provider': model['provider'],
                    'model_name': model['model_name'],
                    'type': model.get('type', 'test'),
                    'status': 'error',
                    'response_time': None,
                    'error': f"测试异常: {str(exc)[:100]}"
                })

    return results

def analyze_results(results):
    """分析测试结果"""
    total = len(results)
    success_count = len([r for r in results if r['status'] == 'success'])
    timeout_count = 0  # 模型测试中超时归类为错误
    error_count = len([r for r in results if r['status'] == 'error'])

    print("\n" + "=" * 80)
    print("📊 详细测试结果")
    print("=" * 80)

    # 按模型类型分组显示
    type_groups = {}
    for result in results:
        model_type = result.get('type', 'test')
        if model_type not in type_groups:
            type_groups[model_type] = []
        type_groups[model_type].append(result)

    type_icons = {
        'chat': '💬',
        'utility': '🔧',
        'embedding': '🔗',
        'test': '🧪'
    }

    type_names = {
        'chat': '聊天模型',
        'utility': '工具模型',
        'embedding': '嵌入模型',
        'test': '测试模型'
    }

    # 定义输出顺序：聊天模型、工具模型、嵌入模型、测试模型
    output_order = ['chat', 'utility', 'embedding', 'test']

    # 按指定顺序输出
    for model_type in output_order:
        if model_type not in type_groups:
            continue
        type_results = type_groups[model_type]
        icon = type_icons.get(model_type, '🤖')
        name = type_names.get(model_type, '其他模型')
        print(f"\n{icon} {name} ({len(type_results)}个):")

        for result in type_results:
            status_icon = "✅" if result['status'] == 'success' else "❌"

            # 基本信息
            print(f"  {status_icon} {result['provider']}/{result['model_name']}")

            # 平台信息
            if result.get('api_key_status') == 'configured':
                print(f"    🔑 认证: API密钥已配置")
            else:
                print(f"    🌐 地址: {result.get('base_url', 'N/A')}")

            # 测试用例
            print(f"    📝 测试消息: \"{result.get('test_message', TEST_MESSAGE)}\"")

            # 结果
            if result['status'] == 'success':
                print(f"    ⚡ 响应时间: {result['response_time']}ms")
                print(f"    ✅ 状态: 测试成功")
            else:
                print(f"    ❌ 错误: {result.get('error', '未知错误')}")

            print()  # 空行分隔

    print("=" * 80)
    print("📈 统计摘要")
    print("=" * 80)
    print(f"总测试数量: {total}")
    print(f"成功: {success_count}")
    print(f"失败: {error_count}")
    print(f"成功率: {success_count/total*100:.1f}%")

    # 成功的模型按速度排序
    successful_results = [r for r in results if r['status'] == 'success']
    if successful_results:
        successful_results.sort(key=lambda x: x['response_time'])
        print(f"\n🏆 响应最快的模型:")
        for i, result in enumerate(successful_results[:3], 1):
            type_icon = type_icons.get(result.get('type', 'test'), '🤖')
            print(f"  {i}. {type_icon} {result['provider']}/{result['model_name']}: {result['response_time']}ms")

    # 失败的模型
    failed_results = [r for r in results if r['status'] != 'success']
    if failed_results:
        print(f"\n⚠️  有问题的模型:")
        for result in failed_results:
            type_icon = type_icons.get(result.get('type', 'test'), '🤖')
            print(f"  • {type_icon} {result['provider']}/{result['model_name']}: {result.get('error', '未知错误')}")

    return {
        'total': total,
        'success': success_count,
        'timeout': timeout_count,
        'error': error_count,
        'success_rate': success_count/total*100
    }

def save_results(results, stats):
    """保存测试结果 - 已禁用文件保存"""
    # 不生成文件，只显示信息
    print(f"\n💾 测试结果统计完成 (未保存文件)")
    return None

def main():
    """主函数"""
    print("🤖 AI模型响应速度测试工具")
    print("=" * 80)

    try:
        # 执行测试
        results = test_all_models()

        # 分析结果
        stats = analyze_results(results)

        # 保存结果（不生成文件）
        save_results(results, stats)

        # 给出建议
        print("\n💡 建议:")
        if stats['success_rate'] < 50:
            print("  • 大部分模型无法访问，请检查API密钥配置")
            print("  • 检查网络连接和防火墙设置")
        elif stats['error'] > 0:
            print("  • 部分模型无法访问，请检查对应的API密钥")
        else:
            print("  • 所有模型都可以正常访问")

        print(f"\n✨ 测试完成! 成功率: {stats['success_rate']:.1f}%")

    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
