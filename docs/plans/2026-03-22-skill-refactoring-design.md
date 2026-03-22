# Article to Media Image - Skill 重构设计

**日期：** 2026-03-22
**状态：** 设计阶段

---

## 1. 目标

将现有的 MCP Server 重构为一个完整的 Skill，支持三种调用方式：
- **MCP 调用** - Agent 通过 MCP 协议调用
- **CLI 调用** - 命令行直接调用
- **API 调用** - Python 代码导入调用

---

## 2. 当前架构分析

### 2.1 现有结构
```
article-to-media-image/
├── src/
│   ├── main.py              # MCP Server 入口
│   ├── renderer/engine.py   # 核心渲染引擎
│   ├── config/settings.py   # 配置管理
│   └── templates/           # 5 个模板
└── pyproject.toml
```

### 2.2 问题
- 只支持 MCP 协议调用
- 入口点耦合在 MCP Server 中
- 核心逻辑与传输层绑定

---

## 3. 目标架构

### 3.1 Skill 目录结构
```
~/.claude/skills/article-to-media-image/  (或 ~/.agents/skills/)
├── SKILL.md                              # Skill 元数据和使用说明
├── scripts/
│   ├── __init__.py
│   ├── core.py                           # 核心渲染逻辑（从 engine.py 提取）
│   ├── mcp_server.py                     # MCP Server 入口
│   └── cli.py                            # CLI 入口
├── assets/
│   └── templates/                        # 5 个模板目录
│       ├── minimal/
│       ├── gradient/
│       ├── card/
│       ├── dark/
│       └── tech_modern/
└── references/
    ├── api-reference.md                  # API 详细文档
    └── template-guide.md                 # 模板使用指南
```

### 3.2 调用方式设计

#### MCP 调用（Agent 使用）
```json
{
  "mcpServers": {
    "article-to-media-image": {
      "command": "python",
      "args": ["-m", "scripts.mcp_server"]
    }
  }
}
```

#### CLI 调用（终端使用）
```bash
# 安装后
article-to-card --template tech_modern --output output.html segments.json

# 或 Python 模块调用
python -m scripts.cli --template minimal segments.json
```

#### API 调用（代码使用）
```python
from scripts.core import ArticleCardRenderer

renderer = ArticleCardRenderer()
html = renderer.render(segments, template="tech_modern")
renderer.to_file(html, "output.html")
```

---

## 4. 核心设计原则

1. **解耦传输层** - 渲染逻辑与调用方式无关
2. **统一接口** - 三种方式使用相同的核心逻辑
3. **渐进披露** - SKILL.md 提供快速入门，references/ 提供详细文档
4. **向后兼容** - 保持现有 MCP 配置可用

---

## 5. 重构步骤

### Phase 1: 提取核心逻辑
- 从 `src/renderer/engine.py` 提取纯渲染逻辑
- 创建 `scripts/core.py` 作为独立核心

### Phase 2: 创建适配器
- `scripts/mcp_server.py` - MCP 适配器
- `scripts/cli.py` - CLI 适配器

### Phase 3: 编写 SKILL.md
- 元数据（name, description）
- 快速入门
- 调用方式说明

### Phase 4: 测试验证
- 测试三种调用方式
- 确保功能一致

---

## 6. 文件清单

### 新建文件
- `SKILL.md` - Skill 主文件
- `scripts/__init__.py` - 包初始化
- `scripts/core.py` - 核心逻辑
- `scripts/mcp_server.py` - MCP 适配器
- `scripts/cli.py` - CLI 适配器
- `references/api-reference.md` - API 文档

### 移动文件
- `src/renderer/templates/` → `assets/templates/`

### 保留原项目
原 `article-to-media-image` 项目保持不变，Skill 引用其模板

---

## 7. 依赖关系

```
scripts/core.py
    ↓ 依赖
assets/templates/
    ↓ 被使用
scripts/mcp_server.py
scripts/cli.py
```

---

## 8. 已确认决策

1. **Skill 安装位置**: `~/.agents/skills/` （跨平台通用）
2. **模板组织方式**: 引用原项目（单一来源）
3. **环境变量**: `ARTICLE_PROJECT_PATH` 指向原项目路径

## 9. 实施状态

### 已完成 ✅

- [x] 创建 Skill 目录结构 `~/.agents/skills/article-to-media-image/`
- [x] 编写 SKILL.md 主文件
- [x] 创建 scripts/core.py 核心渲染逻辑
- [x] 创建 scripts/mcp_server.py MCP 适配器
- [x] 创建 scripts/cli.py CLI 适配器
- [x] 创建 references/ 文档
- [x] 测试 API 调用方式 - ✅ 通过
- [x] 测试 CLI 调用方式 - ✅ 通过
- [x] 验证 MCP 模块导入 - ✅ 通过

### 最终结构

```
~/.agents/skills/article-to-media-image/
├── SKILL.md                    # Skill 元数据和快速入门
├── README.md                   # 使用说明
├── scripts/
│   ├── __init__.py             # 包初始化
│   ├── core.py                 # 核心渲染逻辑
│   ├── mcp_server.py           # MCP 适配器
│   └── cli.py                  # CLI 适配器
└── references/
    ├── api-reference.md        # API 完整文档
    ├── template-guide.md       # 模板自定义指南
    └── test_segments.json      # 测试数据
```

## 10. 使用方法

### MCP 配置

在 Claude Code 设置中添加：

```json
{
  "mcpServers": {
    "article-to-media-image": {
      "command": "python",
      "args": ["-m", "scripts.mcp_server"],
      "cwd": "~/.agents/skills/article-to-media-image",
      "env": {
        "ARTICLE_PROJECT_PATH": "/Users/mapleyf/projects/myDev/article-to-media-image"
      }
    }
  }
}
```

### CLI 使用

```bash
export ARTICLE_PROJECT_PATH=~/projects/article-to-media-image
python -m scripts.cli --template tech_modern segments.json
```

### API 使用

```python
from scripts.core import ArticleCardRenderer

renderer = ArticleCardRenderer()
html = renderer.render(segments, template="tech_modern")
```
