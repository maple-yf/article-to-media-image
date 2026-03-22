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

## License

MIT License
