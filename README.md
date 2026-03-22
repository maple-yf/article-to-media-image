# Article to Media Image

将文章/笔记转化为精美 HTML 卡片图片，支持 5 种视觉风格。

## 特性

- **5 种精美模板**: Minimal、Gradient、Card、Dark、Tech Modern
- **CLI 工具**: 简单命令行接口
- **Python 库**: 可作为 Python 包使用
- **灵活配置**: 自定义输出路径和默认模板

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

## 使用

### CLI 工具

```bash
# 基本使用
article-to-card --template minimal --output card.html << 'EOF'
{"segments": [
  {"type": "title", "text": "文章标题"},
  {"type": "content", "text": "内容段落..."}
]}
EOF

# 指定风格
article-to-card -t dark -s '[{"type":"title","text":"标题"}]'

# 管道输入
echo '{"segments":[...]}' | article-to-card -t gradient
```

### Python 库

```python
from src.renderer.engine import RenderEngine

engine = RenderEngine()

segments = [
    {"type": "title", "text": "文章标题"},
    {"type": "content", "text": "内容段落..."},
    {"type": "highlight", "text": "关键洞察"},
]

# 渲染到文件
output_path = engine.render_to_file(segments, template="tech_modern")
print(f"Generated: {output_path}")
```

## 模板

| 模板 | 风格 | 适用场景 |
|------|------|---------|
| `minimal` | 北欧极简 | 技术文档、严肃分析 |
| `gradient` | 杂志渐变 | 生活感悟、情感故事 |
| `card` | 信息卡片 | 知识分享、教程总结 |
| `dark` | 暗色科技 | 开发者内容、技术文章 |
| `tech_modern` | 现代科技 | 科技资讯、AI 相关 |

更多风格说明请参考 `rules/03-风格灵感.md`。

## Segment 类型

| 类型 | 说明 |
|------|------|
| `title` | 文章/章节标题 |
| `content` | 正文段落 |
| `quote` | 引用内容 |
| `highlight` | 强调/要点 |
| `code` | 代码片段 |

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 列出可用模板
article-to-card --list-templates
```

## 技术约束

生成 HTML 时请遵守 `rules/01-技术底线.md` 的规范。

## OpenClaw Skill 使用

### 安装到 OpenClaw

```bash
# 创建软链接到 OpenClaw skills 目录
ln -sfn /path/to/article-to-media-image ~/.openclaw/skills/article-to-media-image
```

### 使用示例

**场景 1：技术文章转卡**
```
你: 把这篇技术文章转成卡片
[粘贴 Go 并发编程文章]

AI: [分析后] 这是一篇技术文档，我选择 minimal 风格。
    [调用 article-to-card 生成 HTML]
    ✅ 卡片已生成：~/article-cards/xxx-minimal.html
```

**场景 2：生活感悟**
```
你: 帮我把这段感悟做成好看的图片
[粘贴内容]

AI: 这是情感类内容，我选择 gradient 暖色渐变风格。
    ✅ 卡片已生成：~/article-cards/xxx-gradient.html
```

**场景 3：开发者内容**
```
你: 用暗色主题生成这张代码教程的卡片

AI: 使用 dark 模板，深色背景 + 霓虹强调。
    ✅ 卡片已生成：~/article-cards/xxx-dark.html
```

**场景 4：科技资讯**
```
你: 用科技现代风格生成这张 AI 新闻的卡片

AI: 使用 tech_modern 模板，几何线条 + 青紫渐变。
    ✅ 卡片已生成：~/article-cards/xxx-tech_modern.html
```

**场景 5：知识总结**
```
你: 把这篇教程总结成信息卡片

AI: 使用 card 模板，模块化卡片 + 图标装饰。
    ✅ 卡片已生成：~/article-cards/xxx-card.html
```

### 触发词

以下关键词会自动触发此 skill：
- 文章转图
- 笔记转卡片
- 生成分享图
- 文章可视化
- 内容卡片化

### 风格自动选择

| 内容类型 | 自动选择风格 |
|---------|-------------|
| 技术文档/严肃分析 | `minimal` |
| 生活感悟/情感故事 | `gradient` |
| 知识分享/教程总结 | `card` |
| 开发者内容/代码 | `dark` |
| 科技资讯/AI 相关 | `tech_modern``

也可以手动指定风格：
```
你: 用科技现代风格生成这张卡片
你: 用北欧极简风格
你: 用暗色科技主题
```

## License

MIT License
