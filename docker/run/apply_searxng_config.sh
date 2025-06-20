#!/bin/bash
# SearXNG配置应用脚本
# 每次容器启动时自动应用我们的配置修复

echo "🔧 应用SearXNG配置修复..."

# 检查源配置文件是否存在
if [ ! -f "/a0/docker/run/fs/etc/searxng/settings.yml" ]; then
    echo "❌ 源配置文件不存在: /a0/docker/run/fs/etc/searxng/settings.yml"
    exit 1
fi

if [ ! -f "/a0/docker/run/fs/etc/supervisor/conf.d/supervisord.conf" ]; then
    echo "❌ 源配置文件不存在: /a0/docker/run/fs/etc/supervisor/conf.d/supervisord.conf"
    exit 1
fi

# 备份原始配置文件
echo "📋 备份原始配置文件..."
cp /etc/searxng/settings.yml /etc/searxng/settings.yml.backup 2>/dev/null || true
cp /etc/supervisor/conf.d/supervisord.conf /etc/supervisor/conf.d/supervisord.conf.backup 2>/dev/null || true

# 应用我们的配置
echo "✅ 应用SearXNG配置..."
cp /a0/docker/run/fs/etc/searxng/settings.yml /etc/searxng/settings.yml

echo "✅ 应用Supervisor配置..."
cp /a0/docker/run/fs/etc/supervisor/conf.d/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 简化Supervisor配置，避免环境变量解析问题
echo "🔧 简化Supervisor配置..."
sed -i 's/environment=SEARXNG_SETTINGS_PATH.*$/environment=SEARXNG_SETTINGS_PATH="\/etc\/searxng\/settings.yml"/' /etc/supervisor/conf.d/supervisord.conf
echo "✅ 已应用简化的Supervisor配置"

# 验证配置是否正确应用
echo "🔍 验证配置..."
if grep -q "http://host.docker.internal:7897" /etc/searxng/settings.yml; then
    echo "✅ SearXNG代理配置已应用"
else
    echo "❌ SearXNG代理配置应用失败"
    exit 1
fi

if grep -q "SEARXNG_SETTINGS_PATH" /etc/supervisor/conf.d/supervisord.conf; then
    echo "✅ Supervisor配置已应用"
else
    echo "❌ Supervisor配置应用失败"
    exit 1
fi

# 重启相关服务
echo "🔄 重启SearXNG服务..."
supervisorctl restart run_searxng

# 等待服务启动
echo "⏳ 等待SearXNG启动..."
sleep 10

# 检查服务状态
if supervisorctl status run_searxng | grep -q "RUNNING"; then
    echo "✅ SearXNG服务启动成功"
else
    echo "❌ SearXNG服务启动失败"
    supervisorctl status run_searxng
    exit 1
fi

# 测试搜索功能
echo "🧪 测试搜索功能..."
sleep 5
if curl -s -m 10 "http://localhost:55510/" > /dev/null; then
    echo "✅ SearXNG Web界面可访问"
    echo "🎉 SearXNG配置修复完成！"
else
    echo "❌ SearXNG Web界面不可访问"
    exit 1
fi

echo ""
echo "📋 配置修复总结:"
echo "  • 代理配置: http://host.docker.internal:7897"
echo "  • 超时时间: 15秒"
echo "  • 端口: 55510"
echo "  • 状态: 正常运行"
echo ""
echo "💡 如果重新创建容器，请再次运行此脚本:"
echo "   docker exec agent0 bash /a0/docker/run/apply_searxng_config.sh"
