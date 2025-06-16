# Agent-Zero 中文优化分支变更记录

## 分支信息
- **分支名称**: chinese-optimization
- **基于分支**: main
- **总提交数**: 116 个提交
- **变更文件数**: 169 个文件
- **创建日期**: 2025-06-14

## 主要功能变更

### 1. 中文本地化支持
- 新增完整的中文提示词系统 (`prompts/chinese/`)
- 包含所有核心功能的中文提示词文件
- 支持中文环境下的智能体交互

### 2. 性能测试工具
- **网络速度测试**: `network_speed_test.py`, `network_speed_test.sh`
- **模型速度测试**: `model_speed_test.py`, `model_speed_test.sh`
- 支持动态配置读取和多模型测试

### 3. MCP (Model Context Protocol) 集成
- 完整的 MCP 客户端和服务器支持
- MCP 工具集成和管理界面
- 支持 stdio 和 SSE 服务器类型

### 4. Docker 优化
- 新增 CUDA 支持的 Docker 配置
- 优化容器构建和依赖管理
- 改进初始化脚本和环境配置

### 5. Web UI 增强
- 新增 MCP 管理界面组件
- 改进设置页面和模态框
- 优化前端组件架构

## 详细文件变更列表

### 核心系统文件
- `agent.py` - 主智能体逻辑
- `initialize.py` - 初始化脚本
- `run_ui.py` - Web UI 启动脚本
- `run_cli.py` - CLI 启动脚本
- `preload.py` - 预加载配置

### 中文提示词系统 (prompts/chinese/)
- `agent.system.main.md` - 主系统提示词
- `agent.system.behaviour.md` - 行为规范
- `agent.system.tools.md` - 工具使用指南
- `fw.*.md` - 框架消息模板 (30+ 文件)
- `agent.system.tool.*.md` - 各工具专用提示词 (10+ 文件)

### MCP 集成文件
- `python/helpers/mcp_handler.py` - MCP 处理器
- `python/helpers/mcp_server.py` - MCP 服务器
- `python/api/mcp_*.py` - MCP API 接口 (4 个文件)
- `webui/components/settings/mcp/` - MCP 管理界面

### Docker 配置
- `docker/base/Dockerfile` - 基础镜像
- `docker/run/Dockerfile.cuda` - CUDA 支持镜像
- `docker/run/docker-compose.cuda.yml` - CUDA 编排配置
- `docker/*/fs/ins/*.sh` - 安装脚本 (15+ 文件)

### 测试工具
- `model_speed_test.py` - 模型性能测试
- `network_speed_test.py` - 网络连接测试
- `*.sh` - 对应的 Shell 脚本

### Python 核心模块
- `python/helpers/settings.py` - 设置管理
- `python/helpers/memory.py` - 内存管理
- `python/helpers/errors.py` - 错误处理
- `python/tools/*.py` - 工具模块优化

### Web UI 组件
- `webui/index.html` - 主页面
- `webui/js/*.js` - JavaScript 模块 (8 个文件)
- `webui/css/*.css` - 样式文件
- `webui/components/` - UI 组件

### 配置文件
- `.gitignore` - Git 忽略规则
- `requirements.txt` - Python 依赖
- `jsconfig.json` - JavaScript 配置
- `docker/*/fs/etc/` - 系统配置文件

### 文档
- `docs/mcp_setup.md` - MCP 设置指南
- `docs/cuda_docker_setup.md` - CUDA Docker 设置
- `README.md` - 项目说明更新

## 主要技术改进

1. **多语言支持**: 完整的中文本地化
2. **性能监控**: 网络和模型性能测试工具
3. **扩展性**: MCP 协议支持第三方工具集成
4. **容器化**: 改进的 Docker 支持和 CUDA 加速
5. **用户体验**: 优化的 Web 界面和交互流程

## 兼容性说明

- 保持与主分支的向后兼容性
- 新增功能通过配置开关控制
- 支持原有的英文提示词系统
- Docker 镜像支持多种部署方式

---
*文档生成时间: 2025-06-15*
*分支状态: 活跃开发中*
