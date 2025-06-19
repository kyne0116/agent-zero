#!/bin/bash
# Agent-Zero 一键部署脚本
# 自动创建容器并应用SearXNG配置修复

echo "🚀 Agent-Zero 一键部署脚本"
echo "================================"

# 检查是否存在同名容器
if docker ps -a --format "table {{.Names}}" | grep -q "^agent0$"; then
    echo "⚠️  发现已存在的agent0容器"
    read -p "是否删除现有容器并重新创建？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  删除现有容器..."
        docker stop agent0 2>/dev/null || true
        docker rm agent0 2>/dev/null || true
    else
        echo "❌ 部署取消"
        exit 1
    fi
fi

# 创建新容器
echo "📦 创建agent0容器..."
docker run -d --name agent0 -p 50080:80 \
  -e HTTP_PROXY=http://host.docker.internal:7897 \
  -e HTTPS_PROXY=http://host.docker.internal:7897 \
  -e "NO_PROXY=localhost,127.0.0.1,10.*,192.168.*,172.*,10.*" \
  -v ~/Work/Github/agent-zero:/a0 \
  -v ~/Work/Github/agent-zero-data:/root \
  frdel/agent-zero-run

if [ $? -ne 0 ]; then
    echo "❌ 容器创建失败"
    exit 1
fi

echo "✅ 容器创建成功"

# 等待容器启动
echo "⏳ 等待容器启动完成..."
sleep 30

# 检查容器状态
if ! docker ps --format "table {{.Names}}" | grep -q "^agent0$"; then
    echo "❌ 容器启动失败"
    docker logs agent0
    exit 1
fi

echo "✅ 容器启动成功"

# 应用SearXNG配置修复
echo "🔧 应用SearXNG配置修复..."
docker exec agent0 bash /a0/docker/run/apply_searxng_config.sh

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Agent-Zero部署完成！"
    echo "================================"
    echo "📱 Web界面: http://localhost:50080"
    echo "🔍 SearXNG: 已配置代理，搜索功能正常"
    echo "📊 状态检查: docker exec agent0 supervisorctl status"
    echo ""
    echo "💡 提示: 如果需要重新部署，直接运行此脚本即可"
else
    echo "❌ SearXNG配置修复失败"
    echo "请手动运行: docker exec agent0 bash /a0/docker/run/apply_searxng_config.sh"
    exit 1
fi
