#!/bin/bash

echo "========================================"
echo "    AI模型响应速度测试工具"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ 错误: 未找到Python，请先安装Python 3.6+"
        echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "macOS: brew install python3"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python已安装"
$PYTHON_CMD --version

# Python依赖库会在运行时自动检查

# 检查配置文件
echo
echo "🔍 检查配置文件..."

if [ ! -f ".env" ]; then
    echo "❌ 未找到 .env 文件"
    exit 1
fi

if [ ! -f "tmp/settings.json" ]; then
    echo "❌ 未找到 tmp/settings.json 文件"
    exit 1
fi

echo "✅ 配置文件检查完成"

echo
echo "🚀 启动模型响应速度测试..."
echo

# 运行测试脚本
$PYTHON_CMD model_speed_test.py

echo
echo "📋 测试完成"
