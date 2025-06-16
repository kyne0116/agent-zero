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

| 文件名称              | 文件路径               | 变更类型 | 变更日期            | 备注说明                |
| --------------------- | ---------------------- | -------- | ------------------- | ----------------------- |
| model_speed_test.py   | /model_speed_test.py   | Added    | 2025-06-16 14:30:00 | AI 模型响应速度测试脚本 |
| model_speed_test.sh   | /model_speed_test.sh   | Added    | 2025-06-16 14:30:00 | AI 模型测试脚本启动器   |
| network_speed_test.py | /network_speed_test.py | Added    | 2025-06-16 14:30:00 | 网络连接测速脚本        |
| network_speed_test.sh | /network_speed_test.sh | Added    | 2025-06-16 14:30:00 | 网络测试脚本启动器      |

---

## 详细变更日志

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
