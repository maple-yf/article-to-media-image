---
name: article-to-media-image
description: 文章转分享卡片。将文章/笔记转化为精美 HTML 卡片图片，支持 5 种视觉风格。触发场景：文章转图、笔记转卡片、生成分享图、文章可视化、内容卡片化。
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

| 风格 | 适用场景 | 特征 |
|------|---------|------|
| `minimal` | 技术文档、严肃分析 | 北欧极简，大量留白 |
| `gradient` | 生活感悟、情感故事 | 暖色渐变，圆角卡片 |
| `card` | 知识分享、教程总结 | 模块化卡片，图标装饰 |
| `dark` | 开发者内容、技术文章 | 深色背景，霓虹强调 |
| `tech_modern` | 科技资讯、AI 相关 | 几何线条，未来感 |

## 使用方式

### 作为 CLI 工具

```bash
# 基本使用
article-to-card --template minimal --output card.html

# JSON 输入
article-to-card -t dark -s '[{"type":"title","text":"标题"}]'

# 管道输入
echo '{"segments":[...]}' | article-to-card -t gradient
```

### 作为 Python 库

```python
from src.renderer.engine import RenderEngine

engine = RenderEngine()
segments = [
    {"type": "title", "text": "文章标题"},
    {"type": "content", "text": "内容段落..."},
    {"type": "highlight", "text": "关键洞察"}
]

output_path = engine.render_to_file(segments, template="tech_modern")
print(f"Generated: {output_path}")
```

## 工作流程

```
用户给文章
    ↓
① 内容分析 — 提取核心论点、关键数据、对比维度
    ↓
② 自由设计 — 根据内容调性，自主决定视觉风格、配色、布局。然后进行风格选择，根据内容调性选择合适的模板风格
    （可参考 rules/03-风格灵感.md 和 templates/ 获取灵感）
    ↓
③ 生成 HTML — CLI 工具生成自包含 HTML，必须遵守 rules/01-技术底线.md
    ↓
④ 后处理 — 运行 scripts/post-process.sh（可选）
    ↓
⑤ 截图交付 — 按 rules/02-截图流程.md 执行
```

## 目录结构

| 文件 | 说明 |
|------|------|
| `rules/01-技术底线.md` | **必读**：字号、宽度等硬性约束 |
| `rules/02-截图流程.md` | 截图交付流程 |
| `rules/03-风格灵感.md` | 5 种模板的风格说明 |
| `templates/` | HTML 模板文件 |
| `scripts/post-process.sh` | 后处理脚本（可选） |

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

## 安装

```bash
# 克隆仓库
git clone <repo-url>
cd article-to-media-image

# 安装依赖
pip install -e .

# 验证安装
article-to-card --help
```
