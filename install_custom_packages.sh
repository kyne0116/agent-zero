#!/bin/bash
# 自定义软件包安装脚本
# 在容器重新创建后运行此脚本来安装常用软件

echo "🔧 安装自定义软件包..."

# 激活Python虚拟环境
source /root/.venv/bin/activate

# 安装常用Python包
echo "📦 安装Python包..."
pip install matplotlib seaborn pandas numpy scipy scikit-learn jupyter notebook

# 安装系统工具（如果需要）
echo "🛠️ 安装系统工具..."
apt-get update
apt-get install -y vim curl wget htop tree

echo "✅ 自定义软件包安装完成！"
