#!/bin/bash

echo "========================================"
echo "    Searx网络测速工具启动脚本"
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

# 检查requests库是否安装
$PYTHON_CMD -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo
    echo "⚠️  requests库未安装，正在安装..."
    
    # 尝试使用pip3，如果失败则使用pip
    if command -v pip3 &> /dev/null; then
        pip3 install requests
    elif command -v pip &> /dev/null; then
        pip install requests
    else
        echo "❌ 未找到pip，请手动安装requests库"
        echo "尝试: $PYTHON_CMD -m pip install requests"
        exit 1
    fi
    
    if [ $? -ne 0 ]; then
        echo "❌ 安装requests失败，请手动执行安装命令"
        exit 1
    fi
    echo "✅ requests库安装成功"
fi

echo
echo "🚀 启动网络测速..."
echo

# 运行测速脚本
$PYTHON_CMD network_speed_test.py

echo
echo "📋 测试完成"
