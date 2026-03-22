# Article to Media Image - Skill 重构设计

**日期：** 2026-03-22
**状态：** 已完成

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
~/.agents/skills/article-to-media-image/
├── SKILL.md                              # Skill 元数据和使用说明
├── README.md                             # 使用说明
├── scripts/
│   ├── __init__.py                       # 包初始化
│   ├── core.py                           # 核心渲染逻辑
│   ├── mcp_server.py                     # MCP Server 入口
│   └── cli.py                            # CLI 入口
├── assets/
│   └── templates/                        # 5 个模板目录（从原项目复制）
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
      "args": ["-m", "scripts.mcp_server"],
      "cwd": "~/.agents/skills/article-to-media-image"
    }
  }
}
```

#### CLI 调用（终端使用）
```bash
python -m scripts.cli --template tech_modern segments.json
```

#### API 调用（代码使用）
```python
from scripts.core import ArticleCardRenderer

renderer = ArticleCardRenderer()
html = renderer.render(segments, template="tech_modern")
renderer.to_file(segments, template="minimal")
```

---

## 4. 核心设计原则

1. **解耦传输层** - 渲染逻辑与调用方式无关
2. **统一接口** - 三种方式使用相同的核心逻辑
3. **渐进披露** - SKILL.md 提供快速入门，references/ 提供详细文档
4. **自包含** - 模板文件随 Skill 打包，无需外部依赖
5. **零配置** - 无需环境变量，开箱即用

---

## 5. 重构步骤

### Phase 1: 提取核心逻辑 ✅
- 从 `src/renderer/engine.py` 提取纯渲染逻辑
- 创建 `scripts/core.py` 作为独立核心

### Phase 2: 创建适配器 ✅
- `scripts/mcp_server.py` - MCP 适配器
- `scripts/cli.py` - CLI 适配器

### Phase 3: 打包模板 ✅
- 复制原项目模板到 `assets/templates/`
- 移除环境变量依赖
- Skill 完全独立运行

### Phase 4: 编写文档 ✅
- SKILL.md 主文件
- references/api-reference.md
- references/template-guide.md
- README.md

### Phase 5: 测试验证 ✅
- 测试 API 调用方式 ✅
- 测试 CLI 调用方式 ✅
- 验证 MCP 模块导入 ✅

---

## 6. 文件清单

### 新建文件
- `SKILL.md` - Skill 主文件
- `README.md` - 使用说明
- `scripts/__init__.py` - 包初始化
- `scripts/core.py` - 核心逻辑（无环境变量依赖）
- `scripts/mcp_server.py` - MCP 适配器（无环境变量依赖）
- `scripts/cli.py` - CLI 适配器（移除 --project-path 参数）
- `references/api-reference.md` - API 文档
- `references/template-guide.md` - 模板指南

### 复制文件
- `src/renderer/templates/*` → `assets/templates/*`

### 移除内容
- 删除 `references/test_segments.json`
- 移除所有 `ARTICLE_PROJECT_PATH` 环境变量相关代码

---

## 7. 依赖关系

```
scripts/core.py
    ↓ 依赖
assets/templates/    # 模板文件随 Skill 打包
    ↓ 被使用
scripts/mcp_server.py
scripts/cli.py
```

---

## 8. 已确认决策

1. **Skill 安装位置**: `~/.agents/skills/` （跨平台通用）
2. **模板组织方式**: 复制到 Skill 内部（自包含）
3. **环境变量**: 移除所有环境变量依赖

---

## 9. 实施状态

### 已完成 ✅

- [x] 创建 Skill 目录结构
- [x] 复制模板文件到 `assets/templates/`
- [x] 编写 SKILL.md 主文件
- [x] 创建 scripts/core.py 核心渲染逻辑
- [x] 创建 scripts/mcp_server.py MCP 适配器
- [x] 创建 scripts/cli.py CLI 适配器
- [x] 创建 references/ 文档
- [x] 移除所有环境变量依赖
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
├── assets/
│   └── templates/              # 打包的模板文件
│       ├── minimal/
│       ├── gradient/
│       ├── card/
│       ├── dark/
│       └── tech_modern/
└── references/
    ├── api-reference.md        # API 完整文档
    └── template-guide.md       # 模板自定义指南
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
      "cwd": "~/.agents/skills/article-to-media-image"
    }
  }
}
```

### CLI 使用

```bash
cd ~/.agents/skills/article-to-media-image
python -m scripts.cli --template tech_modern segments.json
```

### API 使用

```python
from scripts.core import ArticleCardRenderer

renderer = ArticleCardRenderer()
html = renderer.render(segments, template="tech_modern")
```

### 测试

```bash
cd ~/.agents/skills/article-to-media-image
python3 -c "
from scripts.core import ArticleCardRenderer

segments = [
    {'type': 'title', 'text': 'Test'},
    {'type': 'content', 'text': 'Content here'}
]

renderer = ArticleCardRenderer()
output = renderer.render_to_file(segments, 'minimal')
print(f'Generated: {output}')
"
```

---

## 11. 关键变更

### 变更前（依赖原项目）
- 需要设置 `ARTICLE_PROJECT_PATH` 环境变量
- 模板文件从原项目引用
- Skill 无法独立使用

### 变更后（自包含）
- 无需任何环境变量
- 模板文件打包在 Skill 内部
- Skill 完全独立，可单独分发
- 开箱即用，零配置

---

**重构完成日期:** 2026-03-22
**测试状态:** ✅ 全部通过
