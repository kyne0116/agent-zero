# Agent-Zero 提示词设置完整指南

## 概述

基于 Agent-Zero 官方现有机制，通过巧妙的目录结构和命名规范，实现通用提示词和项目级提示词的管理，同时保持与官方版本的完全兼容性。

## 官方提示词机制分析

### 核心机制

Agent-Zero 使用**双层回退机制**：

1. **主目录**：`prompts/{prompts_subdir}/` - 优先查找
2. **备份目录**：`prompts/default/` - 找不到文件时回退

### 配置方式

- **Web 界面**：Settings → Agent Config → Prompts Subdirectory
- **配置文件**：`tmp/settings.json` 中的 `agent_prompts_subdir` 字段

## 推荐目录结构设计

```
prompts/
├── default/                    # 官方默认（不要修改）
├── common-en/                  # 英文通用提示词
├── common-zh/                  # 中文通用提示词
├── project-webapp/             # Web应用项目
├── project-api/                # API项目
├── project-ecommerce/          # 电商项目
├── dev-python/                 # Python开发专用
├── dev-frontend/               # 前端开发专用
└── team-{公司名}/              # 团队/公司标准
```

## 命名规范

### 1. 通用提示词

- `common` - 基础通用配置
- `common-{语言}` - 特定语言的通用配置
- `common-{技术栈}` - 特定技术栈通用配置

### 2. 项目级提示词

- `project-{项目名}` - 具体项目配置
- `client-{客户名}` - 客户特定配置

### 3. 开发环境提示词

- `dev-{技术}` - 开发环境特定配置
- `team-{团队名}` - 团队标准配置

## 实施步骤

### 步骤 1：创建通用提示词目录

```bash
# 创建通用提示词目录
mkdir -p prompts/common

# 从默认目录复制需要修改的文件
cp prompts/default/agent.system.main.role.md prompts/common/
cp prompts/default/agent.system.behaviour_default.md prompts/common/
```

### 步骤 2：编辑通用提示词

**prompts/common/agent.system.main.role.md**

```markdown
## Your role

You are Agent Zero, an advanced autonomous AI agent designed for professional software development and business automation.

### Core Capabilities

- **Code Development**: Write, review, and optimize code across multiple languages
- **System Integration**: Connect and orchestrate various tools and services
- **Problem Solving**: Break down complex problems into manageable solutions
- **Documentation**: Create clear, comprehensive documentation

### Professional Standards

- Follow industry best practices and coding standards
- Prioritize code quality, security, and maintainability
- Provide detailed explanations and reasoning
- Maintain professional communication at all times
```

**prompts/common/agent.system.behaviour_default.md**

```markdown
- Always write clean, well-documented code
- Follow established coding conventions and best practices
- Implement proper error handling and logging
- Use meaningful variable and function names
- Write comprehensive unit tests when developing features
- Consider security implications in all implementations
- Optimize for readability first, performance second
- Provide clear commit messages and documentation
```

### 步骤 3：创建项目特定提示词

```bash
# 创建项目目录
mkdir -p prompts/project-webapp

# 只复制需要项目特定定制的文件
cp prompts/common/agent.system.behaviour_default.md prompts/project-webapp/
```

**prompts/project-webapp/agent.system.behaviour_default.md**

```markdown
- Follow React/Next.js best practices and conventions
- Use TypeScript for type safety
- Implement responsive design with Tailwind CSS
- Follow atomic design principles for components
- Use React hooks and functional components
- Implement proper state management (Redux/Zustand)
- Write comprehensive unit tests with Jest/Testing Library
- Follow accessibility (a11y) guidelines
- Optimize for Core Web Vitals and performance
- Use semantic HTML and proper SEO practices
```

### 步骤 4：配置切换

#### 方法 1：Web 界面配置

1. 打开 Agent-Zero Web 界面
2. 进入 Settings 页面
3. 在 Agent Config 部分找到"Prompts Subdirectory"
4. 选择对应的目录（如`common`、`project-webapp`等）

#### 方法 2：直接修改配置文件

编辑 `tmp/settings.json`：

```json
{
  "agent_prompts_subdir": "project-webapp"
}
```

## 高级使用技巧

### 1. 分层继承策略

**基础层** → **通用层** → **项目层**

```bash
# 基础通用配置
prompts/common/
├── agent.system.main.role.md          # 基础角色定义
└── agent.system.behaviour_default.md  # 通用行为规则

# 项目特定配置（继承通用配置）
prompts/project-webapp/
└── agent.system.behaviour_default.md  # 只覆盖行为规则
```

### 2. 模块化文件管理

只在自定义目录中放置需要修改的文件：

```bash
# 检查哪些文件需要定制
ls prompts/default/

# 只复制需要修改的文件到自定义目录
cp prompts/default/需要修改的文件.md prompts/your-custom/
```

### 3. 版本控制集成

```bash
# 将自定义提示词纳入版本控制
git add prompts/common/
git add prompts/project-*/
git commit -m "Add custom prompts configuration"

# 忽略官方默认目录（避免冲突）
echo "prompts/default/" >> .gitignore
```

## 实际应用场景

### 场景 1：多项目开发团队

```bash
# 团队通用标准
prompts/team-acme/
├── agent.system.main.role.md
└── agent.system.behaviour_default.md

# 项目A（Web应用）
prompts/project-webapp/
└── agent.system.behaviour_default.md

# 项目B（API服务）
prompts/project-api/
└── agent.system.behaviour_default.md
```

**使用方式**：

- 开发 Web 应用时：设置 `agent_prompts_subdir: "project-webapp"`
- 开发 API 服务时：设置 `agent_prompts_subdir: "project-api"`

### 场景 2：国际化支持

```bash
# 中文环境
prompts/common-zh/
├── agent.system.main.communication.md
└── agent.system.main.role.md

# 英文环境
prompts/common-en/
├── agent.system.main.communication.md
└── agent.system.main.role.md
```

### 场景 3：技术栈特化

```bash
# Python开发
prompts/dev-python/
└── agent.system.behaviour_default.md

# 前端开发
prompts/dev-frontend/
└── agent.system.behaviour_default.md

# DevOps
prompts/dev-ops/
└── agent.system.behaviour_default.md
```

## 文件内容示例

### 通用角色定义

**prompts/common/agent.system.main.role.md**

```markdown
## Your role

You are Agent Zero, a professional AI development assistant.

### Core Responsibilities

- Write high-quality, maintainable code
- Follow industry best practices
- Provide clear documentation and explanations
- Ensure security and performance considerations

### Communication Style

- Be precise and professional
- Provide code examples when helpful
- Explain complex concepts clearly
- Ask clarifying questions when needed
```

### 项目特定行为

**prompts/project-ecommerce/agent.system.behaviour_default.md**

```markdown
- Follow e-commerce security best practices
- Implement proper payment processing safeguards
- Use secure session management
- Follow PCI DSS compliance guidelines
- Implement proper inventory management logic
- Use appropriate caching strategies for product data
- Follow SEO best practices for product pages
- Implement proper error handling for payment flows
```

## 维护和更新

### 1. 定期同步官方更新

```bash
# 检查官方默认提示词的更新
git pull origin main
diff -r prompts/default/ prompts/your-custom/
```

### 2. 备份自定义配置

```bash
# 备份自定义提示词
tar -czf prompts-backup-$(date +%Y%m%d).tar.gz prompts/common/ prompts/project-*/
```

### 3. 测试配置

```bash
# 切换到测试配置
# 在settings.json中设置 "agent_prompts_subdir": "test-config"
# 验证Agent行为是否符合预期
```

## 故障排除

### 问题 1：提示词未生效

**检查清单**：

- [ ] 目录名称是否正确
- [ ] 文件名是否与 default 目录一致
- [ ] settings.json 配置是否正确
- [ ] 是否重启了 Agent-Zero

### 问题 2：文件找不到

**解决方案**：

```bash
# 检查文件是否存在
ls -la prompts/your-custom/
# 检查文件权限
chmod 644 prompts/your-custom/*.md
```

### 问题 3：配置不生效

**调试步骤**：

1. 检查 `tmp/settings.json` 文件格式
2. 验证目录是否存在
3. 查看 Agent-Zero 日志输出

## 总结

通过这种方式，您可以：

- ✅ 保持与官方版本完全兼容
- ✅ 实现通用提示词和项目级提示词管理
- ✅ 支持快速切换不同配置
- ✅ 便于版本控制和团队协作
- ✅ 随时更新官方版本而不丢失自定义配置

这种方案充分利用了 Agent-Zero 现有的回退机制，无需修改任何源码，既灵活又稳定。
