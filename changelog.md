# 代码变更历史记录 (Changelog)

本文档记录 Agent Zero 项目的 lsy3 分支代码变更历史，用于跟踪和管理代码库的演进过程。

## 维护规则

- **记录范围**: 记录所有需要提交到 git 管理的文件变更
- **排除文件**: 不记录以下文件和文件夹的变更
  - `/memory/` - Agent 的内存文件
  - `/knowledge/` - 自定义知识库文件
  - `/instruments/` - 自定义工具和函数
  - `/prompts/` - 提示词文件
  - `/work_dir/` - 工作目录
  - `.env` - API 密钥配置文件
  - `/tmp/settings.json` - Agent Zero 临时设置
  - `/tmp/chats/` - 聊天历史记录
  - `settings.json` - Agent Zero 设置文件
- **更新频率**: 每次代码变更后及时更新
- **格式要求**: 使用标准 Markdown 格式，日期格式为 YYYY-MM-DD HH:MM:SS

---

## 变更汇总表格

| 文件名称                        | 文件路径                                              | 变更类型 | 变更日期            | 备注说明                       |
| ------------------------------- | ----------------------------------------------------- | -------- | ------------------- | ------------------------------ |
| browser_agent.py                | /python/tools/browser_agent.py                        | Modified | 2025-06-20 18:30:00 | 修复 BrowserSession 方法兼容性 |
| setup_venv.sh                   | /docker/run/fs/ins/setup_venv.sh                      | Modified | 2025-06-20 15:45:00 | 虚拟环境持久化配置             |
| deploy_agent0.sh                | /deploy_agent0.sh                                     | Modified | 2025-06-20 15:45:00 | 增加自定义软件包安装功能       |
| install_custom_packages.sh      | /install_custom_packages.sh                           | Added    | 2025-06-20 15:45:00 | 自定义软件包安装脚本           |
| settings.yml                    | /docker/run/fs/etc/searxng/settings.yml               | Modified | 2025-06-19 16:30:00 | SearXNG 代理配置和超时设置     |
| supervisord.conf                | /docker/run/fs/etc/supervisor/conf.d/supervisord.conf | Modified | 2025-06-19 16:30:00 | SearXNG 进程环境变量配置       |
| searxng.py                      | /python/helpers/searxng.py                            | Modified | 2025-06-19 16:30:00 | SearXNG 服务 URL 配置修正      |
| search_engine.py                | /python/tools/search_engine.py                        | Modified | 2025-06-19 16:30:00 | 搜索引擎逻辑改进和容错机制     |
| apply_searxng_config.sh         | /docker/run/apply_searxng_config.sh                   | Added    | 2025-06-19 16:30:00 | SearXNG 配置自动应用脚本       |
| SearXNG 网络检索问题分析总结.md | /docs/SearXNG 网络检索问题分析总结.md                 | Added    | 2025-06-19 16:30:00 | SearXNG 问题分析和解决方案文档 |
| preload.py                      | /preload.py                                           | Modified | 2025-06-17 09:30:00 | 修复设置加载方法调用           |
| model_speed_test.py             | /model_speed_test.py                                  | Added    | 2025-06-16 14:30:00 | AI 模型响应速度测试脚本        |
| model_speed_test.sh             | /model_speed_test.sh                                  | Added    | 2025-06-16 14:30:00 | AI 模型测试脚本启动器          |
| network_speed_test.py           | /network_speed_test.py                                | Added    | 2025-06-16 14:30:00 | 网络连接测速脚本               |
| network_speed_test.sh           | /network_speed_test.sh                                | Added    | 2025-06-16 14:30:00 | 网络测试脚本启动器             |

---

## 详细变更日志

### 2025-06-20 18:30:00 - 修复浏览器代理 BrowserSession 方法兼容性问题

**变更文件**: `/python/tools/browser_agent.py`

- **变更类型**: Modified (修改)
- **变更内容**:
  - 修复 `override_hooks()` 方法中的 `AttributeError: 'BrowserSession' object has no attribute 'get_state'` 错误
  - 添加 `hasattr()` 检查，确保方法存在后再尝试访问
  - 当 `get_state` 方法不存在时，自动使用 `get_state_summary` 方法作为替代
  - 为 `get_session` 和 `remove_highlights` 方法也添加了相同的安全检查
  - 增强代码的健壮性，适应不同版本的 browser-use 库
- **变更原因**: 解决 browser-use 库版本更新后方法名变更导致的兼容性问题，修复浏览器代理工具无法正常工作的错误
- **影响范围**: 影响浏览器代理工具的正常运行，修复后可以正常使用浏览器自动化功能
- **相关问题**: 修复了日志中出现的 `AttributeError: 'BrowserSession' object has no attribute 'get_state'` 错误
- **技术细节**:

  ```python
  # 修改前（会导致 AttributeError）
  self.context.get_state = override_hook(self.context.get_state)

  # 修改后（增加安全检查）
  if hasattr(self.context, 'get_state'):
      self.context.get_state = override_hook(self.context.get_state)
  elif hasattr(self.context, 'get_state_summary'):
      self.context.get_state = override_hook(self.context.get_state_summary)
  ```

---

### 2025-06-20 15:45:00 - 实现 Docker 容器软件包持久化

**变更文件**: `/docker/run/fs/ins/setup_venv.sh`

- **变更类型**: Modified (修改)
- **变更内容**:
  - 将 Python 虚拟环境路径从 `/opt/venv` 修改为 `/root/.venv`
  - 使用变量 `VENV_DIR="/root/.venv"` 统一管理虚拟环境路径
  - 更新虚拟环境创建和激活逻辑，确保使用持久化目录
- **变更原因**: 解决 Docker 容器删除重建后软件包丢失问题，将 Python 虚拟环境迁移到持久化挂载目录
- **影响范围**: 影响容器内 Python 环境的持久化，确保 pip 安装的包在容器重建后保持
- **相关问题**: 修复了容器重新创建后需要重新安装 matplotlib 等 Python 包的问题

**变更文件**: `/deploy_agent0.sh`

- **变更类型**: Modified (修改)
- **变更内容**:
  - 重构 SearXNG 配置修复的错误处理逻辑
  - 新增自定义软件包安装功能模块
  - 添加 `install_custom_packages.sh` 脚本的自动检测和执行
  - 增强部署完成后的信息提示，包含自定义包安装命令
- **变更原因**: 提供容器软件包的自动化安装和管理功能，改善用户体验
- **影响范围**: 增强部署脚本的功能完整性，提供更好的软件包管理体验

**变更文件**: `/install_custom_packages.sh`

- **变更类型**: Added (新增)
- **变更内容**:
  - 创建自定义软件包安装脚本
  - 自动激活持久化 Python 虚拟环境 (`/root/.venv`)
  - 安装常用 Python 科学计算包：matplotlib、seaborn、pandas、numpy、scipy、scikit-learn、jupyter、notebook
  - 安装常用系统工具：vim、curl、wget、htop、tree
  - 提供详细的安装进度反馈和状态提示
- **变更原因**: 为用户提供一键安装常用软件包的便利工具，解决容器重建后的软件环境恢复问题
- **影响范围**: 简化容器软件环境的配置和维护，提升开发效率

---

### 2025-06-19 16:30:00 - 修复 SearXNG 网络检索超时问题

**变更文件**: `/docker/run/fs/etc/searxng/settings.yml`

- **变更类型**: Modified (修改)
- **变更内容**:
  - 添加代理配置：`http://: "http://host.docker.internal:7897"` 和 `https://: "http://host.docker.internal:7897"`
  - 增加请求超时时间：从 3 秒增加到 15 秒 (`request_timeout: 15.0`)
  - 修正服务端口：从 8888 修改为 55510 (`port: 55510`)
  - 禁用 HTTP2：避免代理兼容性问题 (`enable_http2: false`)
- **变更原因**: 解决 SearXNG 搜索引擎无法访问外部网络的超时问题
- **影响范围**: 影响 SearXNG 搜索服务的网络连接和响应性能
- **相关问题**: 修复了搜索引擎 ConnectTimeout 错误，提高搜索成功率

**变更文件**: `/docker/run/fs/etc/supervisor/conf.d/supervisord.conf`

- **变更类型**: Modified (修改)
- **变更内容**:
  - 为 SearXNG 进程添加代理环境变量
  - 配置 HTTP_PROXY 和 HTTPS_PROXY 环境变量
- **变更原因**: 确保 SearXNG 进程能够通过代理访问外部网络
- **影响范围**: 影响 SearXNG 服务的进程环境配置

**变更文件**: `/python/helpers/searxng.py`

- **变更类型**: Modified (修改)
- **变更内容**:
  - 修正 SearXNG 服务 URL 配置
  - 确保正确访问 SearXNG 服务端点
- **变更原因**: 修复 URL 配置错误，确保搜索请求能够正确路由
- **影响范围**: 影响 Python 代码中对 SearXNG 服务的调用

**变更文件**: `/python/tools/search_engine.py`

- **变更类型**: Modified (修改)
- **变更内容**:
  - 改进空结果检测逻辑：增加内容长度验证 (`len(content.strip()) > 10`)
  - 添加 DuckDuckGo 备用搜索机制：SearXNG 失败时自动切换
  - 增强错误处理和日志输出：提供详细的调试信息
  - 修正 PrintStyle 调用方式：使用正确的参数格式
- **变更原因**: 提高搜索引擎的稳定性和容错能力，解决间歇性空结果问题
- **影响范围**: 影响搜索工具的可靠性和用户体验

**变更文件**: `/docker/run/apply_searxng_config.sh`

- **变更类型**: Added (新增)
- **变更内容**:
  - 创建 SearXNG 配置自动应用脚本
  - 自动复制配置文件到容器内正确位置
  - 重启 SearXNG 服务并验证配置
  - 提供详细的执行状态反馈
- **变更原因**: 解决容器重新创建后配置丢失问题，提供自动化配置管理
- **影响范围**: 简化 SearXNG 配置部署和维护流程

**变更文件**: `/deploy_agent0.sh`

- **变更类型**: Added (新增)
- **变更内容**:
  - 创建 Agent-Zero 一键部署脚本
  - 自动处理容器创建、配置应用和服务启动
  - 提供交互式部署流程和状态检查
  - 集成 SearXNG 配置修复流程
- **变更原因**: 简化完整的部署流程，提供用户友好的部署体验
- **影响范围**: 改善项目的部署和维护体验

**变更文件**: `/docs/SearXNG网络检索问题分析总结.md`

- **变更类型**: Added (新增)
- **变更内容**:
  - 详细记录 SearXNG 网络问题的分析过程
  - 提供完整的解决方案和配置说明
  - 包含测试验证结果和部署指南
  - 记录注意事项和最佳实践
- **变更原因**: 为后续维护和问题排查提供完整的技术文档
- **影响范围**: 提升项目的可维护性和知识传承

---

### 2025-06-17 09:30:00 - 修复预加载设置方法调用

**变更文件**: `/preload.py`

- **变更类型**: Modified (修改)
- **变更内容**:
  - 将 `settings.get_default_settings()` 修改为 `settings.get_settings()`
  - 修复了设置加载方法的调用，确保使用正确的设置获取函数
- **变更原因**: 解决 SearXNG 网络连接超时问题，确保正确加载配置设置
- **影响范围**: 影响预加载模块的设置获取逻辑
- **相关问题**: 修复了因设置方法调用错误导致的网络配置问题

---

### 2025-06-16 14:30:00 - 新增测试工具脚本

**变更文件**: `/model_speed_test.py`

- **变更类型**: Added (新增)
- **变更内容**:
  - 创建 AI 模型响应速度测试脚本
  - 支持测试多种 AI 模型提供商（OpenAI、Anthropic、Groq、Google、Mistral、DeepSeek、HuggingFace、OpenRouter、SambaNova、Ollama、LMStudio）
  - 从 settings.json 自动读取配置的模型进行测试
  - 支持并发测试提高效率
  - 提供详细的测试结果分析和统计
  - 支持不同类型模型测试（聊天、工具、嵌入、浏览器模型）
- **变更原因**: 为 Agent Zero 提供模型性能监控和诊断工具

**变更文件**: `/model_speed_test.sh`

- **变更类型**: Added (新增)
- **变更内容**:
  - 创建模型测试脚本的 Shell 启动器
  - 自动检查 Python 环境和依赖
  - 验证必要的配置文件（.env、tmp/settings.json）
  - 提供用户友好的启动界面
- **变更原因**: 简化模型测试工具的使用，提供一键启动功能

**变更文件**: `/network_speed_test.py`

- **变更类型**: Added (新增)
- **变更内容**:
  - 创建网络连接测速脚本
  - 测试搜索引擎站点连接速度（Google、DuckDuckGo、Wikipedia、Wikidata、Startpage、Brave、Bing、Yandex、Searx）
  - 测试 AI 模型 API 站点连接速度和可用性
  - 支持本地和内网服务测试（Ollama、LMStudio）
  - 提供并发测试和详细的结果分析
  - 自动处理代理设置（内网地址禁用代理）
- **变更原因**: 为 Agent Zero 提供网络连接诊断工具，帮助排查网络相关问题

**变更文件**: `/network_speed_test.sh`

- **变更类型**: Added (新增)
- **变更内容**:
  - 创建网络测试脚本的 Shell 启动器
  - 自动检查 Python 环境
  - 自动安装 requests 依赖库
  - 提供用户友好的启动界面
- **变更原因**: 简化网络测试工具的使用，自动处理依赖安装

---

## 注意事项

1. 本 changelog 仅记录代码库中需要版本控制的文件变更
2. 临时文件、配置文件、日志文件等不在记录范围内
3. 每次提交代码前请更新此文档
4. 变更描述应详细说明变更内容、原因和影响
5. 相同文件的多次变更只保留最新记录在汇总表格中，但详细日志保留所有记录
