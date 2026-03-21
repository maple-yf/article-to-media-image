# Article to Media Image - 设计文档

**日期：** 2026-03-21
**作者：** Claude + Maple
**状态：** 已批准

---

## 1. 项目概述

### 1.1 目标

构建一个 **MCP Skill**，将长文章转换为可截图的图卡 HTML 文件。由调用 Agent 负责内容分析和智能分段，Skill 仅负责渲染输出。

### 1.2 核心特性

- **输入**：接收 Agent 预处理的内容分段
- **输出**：竖版（3:4）HTML 文件
- **模板**：5 种精选风格
- **部署**：MCP 协议，供 Claude Code / OpenClaw / OpenCode 等 Agent 调用

---

## 2. 架构设计

### 2.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent (Claude Code)                       │
│  ├─ 智能分段：总结、观点提取、合理切分                       │
│  ├─ 模板选择：根据内容风格选择合适模板                       │
│  └─ 调用 Skill                                              │
└──────────────────────────────┬──────────────────────────────┘
                               │ MCP Protocol
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              article-to-media-image Skill                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  输入：已分段的内容数组 + 指定模板                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  模板渲染（Jinja2 + HTML/CSS）                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                   │
│                    输出 HTML 文件                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 职责划分

| 组件 | 职责 |
|------|------|
| **Agent** | 内容分析、智能分段、总结提炼、模板选择 |
| **Skill** | 接收已处理内容、渲染 HTML、输出文件 |

---

## 3. MCP 接口设计

### 3.1 工具定义

**工具名称：** `article_to_card`

### 3.2 输入参数

```json
{
  "segments": [
    {
      "type": "title|content|quote|code|highlight",
      "text": "内容文本"
    }
  ],
  "template": "模板名称（必填：minimal|gradient|card|dark|tech_modern）",
  "output_path": "输出路径（可选，默认：~/article-cards/{timestamp}-{template}.html）"
}
```

### 3.3 输出格式

**成功：**
```json
{
  "success": true,
  "output_path": "/path/to/output.html",
  "card_count": 5,
  "template": "tech_modern"
}
```

**失败：**
```json
{
  "success": false,
  "error": "错误类型",
  "message": "详细错误信息",
  "suggestion": "建议的解决方案"
}
```

---

## 4. 模板设计

### 4.1 模板总览

| 模板名 | 设计理念 | 主色调 | 适用场景 |
|--------|----------|--------|----------|
| **minimal** | Less is More | 黑白+蓝点缀 | 技术文档、严肃文章 |
| **gradient** | Warm Flow | 4种渐变轮换 | 生活随笔、情感故事 |
| **card** | Information Block | 翡翠绿+多彩标签 | 知识科普、干货分享 |
| **dark** | Night Coding | 深色+语法高亮 | 程序员内容、夜间阅读 |
| **tech_modern** | Professional Tech | 科技蓝+玻璃拟态 | 科技、AI、开发者内容 |

### 4.2 通用规范

- **比例**：竖版 3:4（CSS `aspect-ratio: 3/4`）
- **响应式**：浏览器中自动适配
- **每张卡片**：序号、内容、装饰元素

---

## 5. 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 输入为空 | 返回错误提示，不生成文件 |
| 模板不存在 | 回退到默认模板（tech_modern） |
| 输出路径无效 | 返回错误，提示用户 |
| 渲染失败 | 返回详细错误信息给 Agent |
| 内容过长 | 提示 Agent 重新分段 |

---

## 6. 配置文件

**位置：** `~/.article-to-media-image/config.yaml`

```yaml
defaults:
  template: tech_modern
  output_path: ~/article-cards/{timestamp}-{template}.html
  timestamp_format: "%Y%m%d-%H%M%S"

output:
  base_dir: ~/article-cards
  filename_template: "{timestamp}-{template}.html"

templates:
  available:
    - minimal
    - gradient
    - card
    - dark
    - tech_modern
```

---

## 7. 项目结构

```
article-to-media-image/
├── src/
│   ├── __init__.py
│   ├── main.py                  # MCP Server 入口
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # 配置管理
│   ├── renderer/
│   │   ├── __init__.py
│   │   ├── engine.py            # Jinja2 渲染引擎
│   │   └── context.py           # 模板上下文构建
│   ├── templates/
│   │   ├── minimal/
│   │   │   ├── template.html
│   │   │   └── style.css
│   │   ├── gradient/
│   │   │   ├── template.html
│   │   │   └── style.css
│   │   ├── card/
│   │   │   ├── template.html
│   │   │   └── style.css
│   │   ├── dark/
│   │   │   ├── template.html
│   │   │   └── style.css
│   │   └── tech_modern/
│   │       ├── template.html
│   │       └── style.css
│   └── utils/
│       ├── __init__.py
│       ├── file.py              # 文件操作工具
│       └── validator.py         # 输入验证
├── pyproject.toml
├── README.md
└── docs/
    └── plans/
        └── 2026-03-21-article-to-media-image-design.md
```

---

## 8. 技术栈

- **语言**：Python
- **模板引擎**：Jinja2
- **MCP SDK**：Anthropic MCP Python SDK
- **配置管理**：YAML

---

## 9. 测试策略

1. **单元测试**：配置、文件路径、输入验证
2. **模板测试**：每个模板渲染、边界情况
3. **集成测试**：MCP 工具调用、完整流程

---

## 附录：详细模板设计

详细的 5 个模板设计（配色、布局、视觉元素、卡片类型）已在设计过程中定义，详见项目文档。

### Minimal 模板要点
- 留白至上，超大 padding
- 单色点缀（蓝色）
- 极简边框，无阴影
- 居中对称

### Gradient 模板要点
- 4种渐变轮换（日出橙粉、暮光紫粉、清新薄荷、海洋蓝青）
- 玻璃拟态卡片
- 大圆角 24px
- 装饰元素（圆点、线条）

### Card 模板要点
- 模块化卡片系统
- 翡翠绿主色
- 彩色标签系统
- 交替背景（白/浅灰）

### Dark 模板要点
- 深色护眼背景
- 语法高亮色彩
- 发光效果
- 终端风格元素

### Tech Modern 模板要点
- 科技蓝主题
- 玻璃拟态 + 渐变
- 开发者语境元素（代码块、技术术语）
- 数据可视化（大数字、条形图、标签）
