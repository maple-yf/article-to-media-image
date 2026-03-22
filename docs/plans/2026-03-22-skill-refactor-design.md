# 文章转卡片 - Skill 项目重构设计

**日期**: 2026-03-22
**方案**: 方案 A - 极简重构
**目标**: 将 MCP Server 项目改造为标准 skill 项目

## 概述

移除 MCP 协议依赖，保留 Python 渲染引擎核心能力，改造为 CLI 工具 + SKILL.md 架构的纯 skill 项目。

## 项目结构

```
article-to-media-image/
├── SKILL.md                    # 新增：skill 入口文件
├── README.md                   # 更新：skill 使用说明
├── pyproject.toml              # 修改：CLI 入口
├── rules/                      # 新增：技术规范
│   ├── 01-技术底线.md
│   ├── 02-截图流程.md
│   └── 03-风格灵感.md
├── templates/                  # 新增：HTML 模板
│   ├── minimal/template.html
│   ├── gradient/template.html
│   ├── card/template.html
│   ├── dark/template.html
│   └── tech_modern/template.html
├── scripts/                    # 新增：后处理
│   └── post-process.sh
├── src/
│   ├── cli.py                  # 新增：CLI 入口
│   ├── renderer/               # 保留核心引擎
│   ├── config/
│   └── utils/
└── tests/                      # 更新测试
```

## 核心变更

### 1. SKILL.md 入口
- frontmatter: name, description, 触发词
- 设计理念：内容决定风格
- 5 种模板风格说明
- 目录结构导航

### 2. CLI 接口
```bash
article-to-card --template minimal --output card.html
article-to-card -t dark -s '[{"type":"title","text":"..."}]'
echo '{"segments":[...]}' | article-to-card -t gradient
```

### 3. 模板适配

| 当前模板 | 参考风格 | 特征 |
|---------|---------|------|
| minimal | nordic | 北欧极简，大量留白 |
| gradient | magazine | 暖色渐变，圆角卡片 |
| card | infographic | 模块化卡片，图标装饰 |
| dark | dark-tech | 深色背景，霓虹强调 |
| tech_modern | retro-future | 几何线条，未来感 |

### 4. 依赖清理
- 移除：`mcp>=0.1.0`
- 保留：`jinja2>=3.1.0`, `pyyaml>=6.0`

## 迁移步骤

### 阶段 1：结构调整
- [ ] 创建 rules/、templates/、scripts/ 目录
- [ ] 复制并适配参考项目的规则文件
- [ ] 创建 5 个模板 HTML 文件

### 阶段 2：代码调整
- [ ] 新增 src/cli.py
- [ ] 移除 src/main.py 的 MCP 依赖
- [ ] 更新 pyproject.toml

### 阶段 3：测试验证
- [ ] 测试 CLI 渲染
- [ ] 测试后处理脚本
- [ ] 更新 README.md

## 设计原则

1. **保留核心价值**：Python 渲染引擎的模板能力
2. **平滑迁移**：最小化代码变更
3. **skill 优先**：AI 可直接读取并执行
4. **向后兼容**：segments 数据结构保持一致
