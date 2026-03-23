---
name: article-to-media-image
description: 文章转分享卡片。将文章/笔记转化为精美 HTML 卡片图片，支持多种视觉风格。触发场景：卡片图、信息图、文章转图、笔记转卡片、生成分享图、文章可视化、内容卡片化。
---

# 文章转分享卡片

文章 → AI 分析内容  → 提炼核心信息 → 选择匹配风格 → 生成 HTML 卡片 → 后处理 → 截图交付。

## 设计理念

**你是设计师，不是模板填充机。** 根据文章内容自由设计视觉风格，不要每次都用同一个模板。

- **内容决定形式** — 严肃分析用深色/衬线，轻松科普用手账/波普，技术教程用终端/蓝图
- **信息精炼** — 一张图讲清一个核心论点 + 3-4 个支撑模块，不是把文章全文塞进去
- **手机第一** — 图片在手机上缩放 3 倍，字号必须够大（详见 `rules/01-技术底线.md`）
- **每次不同** — 配色、字体、布局每次都应该有变化，避免千篇一律

**内容决定风格** — 根据文章内容自动选择最匹配的视觉风格。
**生成封面** — 总结提炼文章内容的核心论点，生成一张封面图。封面图应该突出文章的核心观点，与其他图片风格一致，展现主要内容，核心思想，关键数据，吸引读者点击。

## 工作流程

```
用户给文章和素材图片
    ↓
① 内容分析 — 提取核心论点、关键数据、对比维度。如果用户提供素材图片，则以素材图片为基础进行创作。
    ↓
② 自由设计 — 根据内容调性，自主决定视觉风格、配色、布局。然后进行风格选择，根据内容调性选择合适的模板风格
    （可参考 rules/03-风格灵感.md 和 templates/ 获取灵感）
    ↓
③ 生成 HTML — 直接生成html文件内容 - 必须遵守 rules/01-技术底线.md
    ↓
④ 后处理 — 运行 scripts/post-process.sh（可选）
    ↓
⑤ 截图交付 — 按 rules/02-截图流程.md 执行
```

## 模板学习指南

AI 应按以下步骤学习模板：

1. **阅读 SKILL.md** — 了解设计理念和工作流程
2. **分析用户内容** — 判断内容类型和调性
3. **参考 rules/03-风格灵感.md** — 选择合适的风格
4. **参考 templates/[风格].html** — 学习代码结构
5. **生成 HTML** — 遵守 rules/01-技术底线.md 直接生成
6. **截图交付** — 按 rules/02-截图流程.md 执行


## 目录结构

| 文件 | 说明 |
|------|------|
| `rules/01-技术底线.md` | **必读**：字号、宽度等硬性约束 |
| `rules/02-截图流程.md` | 截图交付流程 |
| `rules/03-风格灵感.md` | 风格说明 |
| `templates/` | 14种风格模板 + README |
| `scripts/post-process.sh` | 工具 | 一键后处理（fix CSS + 注入字号兜底） |
| `scripts/fix-html.js` | 工具 | CSS 修复脚本（被 post-process.sh 调用） |
| `scripts/validate-templates.sh` | 工具 | 验证模板结构 |

## Segment 类型

AI 应使用以下 segment 类型：

| 类型 | 说明 | 示例 |
|------|------|------|
| `title` | 文章/章节标题 | "深入理解异步编程" |
| `content` | 正文段落 | "异步编程是现代开发的核心..." |
| `quote` | 引用内容 | "并发不是并行" — Rob Pike |
| `highlight` | 强调/要点 | "关键：使用 async/await" |
| `code` | 代码片段 | "async def fetch():\n    return data" |

## 技术约束

生成 HTML 时**必须遵守** `rules/01-技术底线.md` 的规范：
- 固定宽度 1080px
- 最小字号：正文 30px，标题 72px
- 使用 min-height 而非固定 height
- 禁止 overflow: hidden

## Slide Card Layout

Templates use independent card viewport design:
- 3:4 card ratio (810×1080px)
- 80px inter-card spacing
- Group-specific theming (A-E)
- Dark canvas (#1a1a2e) for contrast

See `templates/README.md` for details.

## Output Directory
All generated files MUST be saved output/ under the AGENT'S current working directory (NOT the skill directory). Every script call MUST include an explicit --output / -o argument pointing to this location. Never omit the output argument or rely on script defaults.