# Skill 项目重构实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标:** 将 MCP Server 项目改造为标准 skill 项目，移除 MCP 协议，保留 Python 渲染引擎，新增 CLI 入口

**架构:**
- 移除 `mcp` 依赖，保留 `jinja2` 和 `pyyaml`
- 新增 CLI 入口 `src/cli.py` 替代 `src/main.py`
- 创建 `rules/`、`templates/`、`scripts/` 目录
- 保持 segments 数据结构向后兼容

**技术栈:**
- Python 3.10+
- Jinja2 (模板渲染)
- CLI (argparse)

---

## Task 1: 创建目录结构

**Files:**
- Create: `rules/01-技术底线.md`
- Create: `rules/02-截图流程.md`
- Create: `rules/03-风格灵感.md`
- Create: `templates/minimal/`
- Create: `templates/gradient/`
- Create: `templates/card/`
- Create: `templates/dark/`
- Create: `templates/tech_modern/`
- Create: `scripts/`

**Step 1: 创建规则目录**

Run: `mkdir -p rules templates/{minimal,gradient,card,dark,tech_modern} scripts`

**Step 2: 验证目录创建**

Run: `ls -la | grep -E 'rules|templates|scripts'`
Expected: 输出包含 rules, templates, scripts 三个目录

**Step 3: 创建 .gitkeep 文件**

Run: `touch rules/.gitkeep templates/minimal/.gitkeep templates/gradient/.gitkeep templates/card/.gitkeep templates/dark/.gitkeep templates/tech_modern/.gitkeep scripts/.gitkeep`

**Step 4: 提交**

```bash
git add rules templates scripts
git commit -m "feat: create skill project directories

- Add rules/ for technical specifications
- Add templates/ for 5 HTML template styles
- Add scripts/ for post-processing tools"
```

---

## Task 2: 复制并适配技术规则文件

**Files:**
- Create: `rules/01-技术底线.md`
- Create: `rules/02-截图流程.md`

**Step 1: 从参考项目复制技术底线**

Run: `cp /Users/mapleyf/projects/github/openclaw-article-to-image/rules/01-技术底线.md rules/01-技术底线.md`

**Step 2: 验证复制**

Run: `head -20 rules/01-技术底线.md`
Expected: 包含 "技术底线" 标题和 CSS 约束

**Step 3: 从参考项目复制截图流程**

Run: `cp /Users/mapleyf/projects/github/openclaw-article-to-image/rules/02-截图流程.md rules/02-截图流程.md`

**Step 4: 提交**

```bash
git add rules/01-技术底线.md rules/02-截图流程.md
git commit -m "feat: add technical rules from reference project

- Copy technical baseline rules
- Copy screenshot workflow guide"
```

---

## Task 3: 创建风格灵感文件

**Files:**
- Create: `rules/03-风格灵感.md`

**Step 1: 创建风格灵感文档**

Write content to `rules/03-风格灵感.md`:

```markdown
<!--
input: 无
output: 5种模板的风格说明，供 AI 选择时参考
pos: 风格选择参考
-->

# 风格灵感

## minimal（北欧极简）

**参考**: `templates/minimal/template.html`

**特征**:
- 大量留白，呼吸感强
- 衬线字体 (Playfair Display + Lora)
- 灰度配色，偶尔单色点缀
- 无装饰元素，纯粹排版

**适用场景**: 技术文档、严肃分析、学术内容

**配色灵感**:
- 背景: #FAFAFA 或 #FFFFFF
- 文字: #2C2C2C
- 强调: #6B7280

---

## gradient（杂志渐变）

**参考**: `templates/gradient/template.html`

**特征**:
- 暖色渐变背景（橙/粉/紫）
- 圆角卡片 (24px border-radius)
- 柔和阴影
- 层次分明的内容区块

**适用场景**: 生活感悟、情感故事、随笔

**配色灵感**:
- 渐变: linear-gradient(135deg, #FF6B6B, #FFE66D)
- 卡片背景: rgba(255,255,255,0.9)
- 文字: #2D3436

---

## card（信息卡片）

**参考**: `templates/card/template.html`

**特征**:
- 模块化卡片布局
- 图标装饰 (emoji 或简单图形)
- 每个信息点独立卡片
- 标签化组织

**适用场景**: 知识分享、教程总结、要点梳理

**配色灵感**:
- 背景: #F0F4F8
- 卡片: #FFFFFF
- 边框: #E1E8EF
- 标签: #3B82F6

---

## dark（暗色科技）

**参考**: `templates/dark/template.html`

**特征**:
- 深色背景 (#0D1117)
- 霓虹强调色 (绿/蓝/紫)
- 代码高亮样式
- 终端感排版

**适用场景**: 开发者内容、技术文章、代码教程

**配色灵感**:
- 背景: #0D1117
- 文字: #C9D1D9
- 强调: #58A6FF
- 代码背景: #161B22

---

## tech_modern（现代科技）

**参考**: `templates/tech_modern/template.html`

**特征**:
- 几何线条装饰
- 未来感配色（青/紫/银）
- 动态元素暗示（箭头、光点）
- 科技感字体

**适用场景**: 科技资讯、AI 相关、前沿技术

**配色灵感**:
- 背景: #0F172A
- 渐变: linear-gradient(to right, #06B6D4, #8B5CF6)
- 文字: #E2E8F0
- 装饰: rgba(6,182,212,0.3)
```

**Step 2: 验证文件创建**

Run: `wc -l rules/03-风格灵感.md`
Expected: 行数 > 80

**Step 3: 提交**

```bash
git add rules/03-风格灵感.md
git commit -m "feat: add style inspiration guide

- Document 5 template styles with characteristics
- Include color schemes and use cases for each style"
```

---

## Task 4: 创建 minimal 模板

**Files:**
- Create: `templates/minimal/template.html`

**Step 1: 创建北欧极简模板**

Write content to `templates/minimal/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080">
  <title>Minimal Card</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lora:wght@400;500&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      margin: 0;
      padding: 0;
      background: #FAFAFA;
      font-family: 'Lora', Georgia, serif;
    }

    .container {
      width: 1080px;
      min-height: 1440px;
      padding: 80px 72px;
      margin: 0;
      background: #FFFFFF;
      color: #2C2C2C;
    }

    .title {
      font-family: 'Playfair Display', serif;
      font-size: 80px;
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 64px;
      color: #1A1A1A;
    }

    .content {
      font-size: 34px;
      line-height: 1.7;
      color: #3A3A3A;
      margin-bottom: 40px;
    }

    .quote {
      font-size: 36px;
      font-style: italic;
      color: #6B7280;
      border-left: 4px solid #E5E7EB;
      padding-left: 32px;
      margin: 48px 0;
    }

    .highlight {
      font-size: 38px;
      font-weight: 500;
      color: #1F2937;
      background: #F3F4F6;
      padding: 24px 32px;
      margin: 32px 0;
      border-radius: 8px;
    }

    .code {
      font-family: 'SF Mono', 'Consolas', monospace;
      font-size: 26px;
      background: #F9FAFB;
      padding: 24px;
      margin: 24px 0;
      border-radius: 6px;
      color: #374151;
      white-space: pre-wrap;
    }

    .footer {
      margin-top: 80px;
      padding-top: 32px;
      border-top: 1px solid #E5E7EB;
      font-size: 24px;
      color: #9CA3AF;
    }
  </style>
</head>
<body>
  <div class="container">
    {% for segment in segments %}
    {% if segment.type == 'title' %}
    <h1 class="title">{{ segment.text }}</h1>
    {% elif segment.type == 'content' %}
    <p class="content">{{ segment.text }}</p>
    {% elif segment.type == 'quote' %}
    <p class="quote">{{ segment.text }}</p>
    {% elif segment.type == 'highlight' %}
    <p class="highlight">{{ segment.text }}</p>
    {% elif segment.type == 'code' %}
    <pre class="code">{{ segment.text }}</pre>
    {% endif %}
    {% endfor %}

    <div class="footer">
      Generated with article-to-media-image
    </div>
  </div>
</body>
</html>
```

**Step 2: 验证模板创建**

Run: `python3 -c "from pathlib import Path; print(Path('templates/minimal/template.html').exists())"`
Expected: True

**Step 3: 提交**

```bash
git add templates/minimal/template.html
git commit -m "feat: add minimal (nordic) template

- Clean, lots of whitespace
- Serif fonts (Playfair Display + Lora)
- Suitable for technical content"
```

---

## Task 5: 创建 gradient 模板

**Files:**
- Create: `templates/gradient/template.html`

**Step 1: 创建杂志渐变模板**

Write content to `templates/gradient/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080">
  <title>Gradient Card</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@600;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      margin: 0;
      padding: 0;
      background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
      font-family: 'Noto Sans SC', sans-serif;
      min-height: 1440px;
    }

    .container {
      width: 1080px;
      min-height: 1440px;
      padding: 60px 48px;
      margin: 0;
      background: linear-gradient(135deg, rgba(255,107,107,0.15) 0%, rgba(255,230,109,0.15) 100%);
    }

    .card {
      background: rgba(255, 255, 255, 0.95);
      border-radius: 24px;
      padding: 48px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.15);
      margin-bottom: 32px;
      backdrop-filter: blur(10px);
    }

    .title {
      font-family: 'Noto Serif SC', serif;
      font-size: 72px;
      font-weight: 700;
      line-height: 1.3;
      color: #2D3436;
      margin-bottom: 40px;
    }

    .content {
      font-size: 32px;
      line-height: 1.8;
      color: #2D3436;
    }

    .highlight {
      background: linear-gradient(135deg, #FF6B6B, #FFE66D);
      color: #FFFFFF;
      padding: 28px 36px;
      border-radius: 16px;
      font-size: 34px;
      font-weight: 500;
      margin: 28px 0;
      box-shadow: 0 8px 24px rgba(255,107,107,0.3);
    }

    .quote {
      font-size: 32px;
      color: #636E72;
      font-style: italic;
      padding-left: 24px;
      border-left: 4px solid #FF6B6B;
      margin: 36px 0;
    }

    .code {
      font-family: 'SF Mono', monospace;
      background: #F8F9FA;
      padding: 24px;
      border-radius: 12px;
      font-size: 24px;
      color: #2D3436;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <div class="container">
    {% for segment in segments %}
    {% if segment.type == 'title' %}
    <div class="card"><h1 class="title">{{ segment.text }}</h1></div>
    {% elif segment.type == 'content' %}
    <div class="card"><p class="content">{{ segment.text }}</p></div>
    {% elif segment.type == 'quote' %}
    <div class="card"><p class="quote">{{ segment.text }}</p></div>
    {% elif segment.type == 'highlight' %}
    <div class="card"><p class="highlight">{{ segment.text }}</p></div>
    {% elif segment.type == 'code' %}
    <div class="card"><pre class="code">{{ segment.text }}</pre></div>
    {% endif %}
    {% endfor %}
  </div>
</body>
</html>
```

**Step 2: 提交**

```bash
git add templates/gradient/template.html
git commit -m "feat: add gradient (magazine) template

- Warm gradient background (orange/pink/yellow)
- Rounded cards with glassmorphism
- Suitable for lifestyle content"
```

---

## Task 6: 创建 card 模板

**Files:**
- Create: `templates/card/template.html`

**Step 1: 创建信息卡片模板**

Write content to `templates/card/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080">
  <title>Card Template</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      margin: 0;
      padding: 0;
      background: #F0F4F8;
      font-family: 'Noto Sans SC', sans-serif;
    }

    .container {
      width: 1080px;
      min-height: 1440px;
      padding: 48px;
      margin: 0;
      background: #F0F4F8;
    }

    .title-card {
      background: linear-gradient(135deg, #3B82F6, #1D4ED8);
      color: white;
      padding: 48px;
      border-radius: 20px;
      margin-bottom: 32px;
      box-shadow: 0 10px 30px rgba(59,130,246,0.3);
    }

    .title {
      font-size: 64px;
      font-weight: 700;
      line-height: 1.3;
    }

    .card {
      background: #FFFFFF;
      border-radius: 16px;
      padding: 36px;
      margin-bottom: 24px;
      border: 1px solid #E1E8EF;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .card-icon {
      font-size: 48px;
      margin-bottom: 16px;
    }

    .content {
      font-size: 30px;
      line-height: 1.7;
      color: #334155;
    }

    .highlight {
      background: #EFF6FF;
      border-left: 6px solid #3B82F6;
      padding: 28px;
      border-radius: 12px;
      font-size: 32px;
      font-weight: 600;
      color: #1E40AF;
    }

    .quote {
      background: #FEF3C7;
      border-left: 6px solid #F59E0B;
      padding: 28px;
      border-radius: 12px;
      font-size: 30px;
      color: #92400E;
      font-style: italic;
    }

    .code {
      font-family: 'SF Mono', monospace;
      background: #1E293B;
      color: #E2E8F0;
      padding: 24px;
      border-radius: 12px;
      font-size: 22px;
      white-space: pre-wrap;
    }

    .tag {
      display: inline-block;
      background: #3B82F6;
      color: white;
      padding: 8px 20px;
      border-radius: 20px;
      font-size: 22px;
      margin-bottom: 16px;
    }
  </style>
</head>
<body>
  <div class="container">
    {% for segment in segments %}
    {% if segment.type == 'title' %}
    <div class="title-card">
      <span class="tag">文章</span>
      <h1 class="title">{{ segment.text }}</h1>
    </div>
    {% elif segment.type == 'content' %}
    <div class="card">
      <span class="card-icon">📝</span>
      <p class="content">{{ segment.text }}</p>
    </div>
    {% elif segment.type == 'highlight' %}
    <div class="card"><p class="highlight">💡 {{ segment.text }}</p></div>
    {% elif segment.type == 'quote' %}
    <div class="card"><p class="quote">💬 {{ segment.text }}</p></div>
    {% elif segment.type == 'code' %}
    <div class="card"><pre class="code">{{ segment.text }}</pre></div>
    {% endif %}
    {% endfor %}
  </div>
</body>
</html>
```

**Step 2: 提交**

```bash
git add templates/card/template.html
git commit -m "feat: add card (infographic) template

- Modular card layout with icons
- Tag-based organization
- Suitable for knowledge sharing"
```

---

## Task 7: 创建 dark 模板

**Files:**
- Create: `templates/dark/template.html`

**Step 1: 创建暗色科技模板**

Write content to `templates/dark/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080">
  <title>Dark Tech</title>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      margin: 0;
      padding: 0;
      background: #0D1117;
      font-family: 'Inter', sans-serif;
    }

    .container {
      width: 1080px;
      min-height: 1440px;
      padding: 60px 56px;
      margin: 0;
      background: #0D1117;
      color: #C9D1D9;
    }

    .title {
      font-size: 68px;
      font-weight: 700;
      color: #58A6FF;
      margin-bottom: 48px;
      border-bottom: 2px solid #30363D;
      padding-bottom: 24px;
    }

    .content {
      font-size: 32px;
      line-height: 1.7;
      color: #C9D1D9;
      margin-bottom: 32px;
    }

    .highlight {
      background: rgba(88,166,255,0.1);
      border: 1px solid #58A6FF;
      border-left: 4px solid #58A6FF;
      padding: 24px 28px;
      border-radius: 8px;
      font-size: 32px;
      color: #58A6FF;
      margin: 24px 0;
    }

    .quote {
      color: #8B949E;
      font-size: 30px;
      font-style: italic;
      border-left: 3px solid #8B949E;
      padding-left: 24px;
      margin: 32px 0;
    }

    .code {
      font-family: 'JetBrains Mono', monospace;
      background: #161B22;
      border: 1px solid #30363D;
      padding: 24px;
      border-radius: 8px;
      font-size: 24px;
      color: #C9D1D9;
      white-space: pre-wrap;
      overflow-x: auto;
    }

    .code .keyword { color: #FF7B72; }
    .code .string { color: #A5D6FF; }
    .code .comment { color: #8B949E; }

    .footer {
      margin-top: 60px;
      padding-top: 24px;
      border-top: 1px solid #30363D;
      font-size: 22px;
      color: #484F58;
    }

    .glow {
      text-shadow: 0 0 20px rgba(88,166,255,0.5);
    }
  </style>
</head>
<body>
  <div class="container">
    {% for segment in segments %}
    {% if segment.type == 'title' %}
    <h1 class="title glow">{{ segment.text }}</h1>
    {% elif segment.type == 'content' %}
    <p class="content">{{ segment.text }}</p>
    {% elif segment.type == 'highlight' %}
    <p class="highlight">▶ {{ segment.text }}</p>
    {% elif segment.type == 'quote' %}
    <p class="quote">{{ segment.text }}</p>
    {% elif segment.type == 'code' %}
    <pre class="code">{{ segment.text }}</pre>
    {% endif %}
    {% endfor %}

    <div class="footer">
      // Generated with article-to-media-image
    </div>
  </div>
</body>
</html>
```

**Step 2: 提交**

```bash
git add templates/dark/template.html
git commit -m "feat: add dark (tech) template

- Dark theme with neon accents
- Code-friendly styling
- Suitable for developer content"
```

---

## Task 8: 创建 tech_modern 模板

**Files:**
- Create: `templates/tech_modern/template.html`

**Step 1: 创建现代科技模板**

Write content to `templates/tech_modern/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080">
  <title>Tech Modern</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;900&family=Rajdhani:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      margin: 0;
      padding: 0;
      background: #0F172A;
      font-family: 'Rajdhani', sans-serif;
      overflow-x: hidden;
    }

    .container {
      width: 1080px;
      min-height: 1440px;
      padding: 56px;
      margin: 0;
      background: #0F172A;
      color: #E2E8F0;
      position: relative;
    }

    .container::before {
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      width: 400px;
      height: 400px;
      background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%);
      pointer-events: none;
    }

    .container::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(139,92,246,0.15) 0%, transparent 70%);
      pointer-events: none;
    }

    .title {
      font-family: 'Orbitron', sans-serif;
      font-size: 72px;
      font-weight: 900;
      background: linear-gradient(to right, #06B6D4, #8B5CF6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 48px;
      text-transform: uppercase;
      letter-spacing: 2px;
      position: relative;
    }

    .title::after {
      content: '';
      position: absolute;
      bottom: -16px;
      left: 0;
      width: 120px;
      height: 4px;
      background: linear-gradient(to right, #06B6D4, #8B5CF6);
    }

    .content {
      font-size: 34px;
      line-height: 1.7;
      color: #CBD5E1;
      margin-bottom: 36px;
      position: relative;
      z-index: 1;
    }

    .highlight {
      background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(139,92,246,0.2));
      border: 1px solid rgba(6,182,212,0.4);
      padding: 28px 32px;
      border-radius: 12px;
      font-size: 36px;
      font-weight: 600;
      color: #06B6D4;
      margin: 28px 0;
      position: relative;
      z-index: 1;
    }

    .highlight::before {
      content: '◆';
      margin-right: 12px;
      color: #8B5CF6;
    }

    .quote {
      font-size: 32px;
      color: #94A3B8;
      font-style: italic;
      padding-left: 28px;
      border-left: 3px solid #8B5CF6;
      margin: 36px 0;
      position: relative;
      z-index: 1;
    }

    .code {
      font-family: 'JetBrains Mono', monospace;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(6,182,212,0.3);
      padding: 24px;
      border-radius: 10px;
      font-size: 23px;
      color: #E2E8F0;
      white-space: pre-wrap;
      position: relative;
      z-index: 1;
      box-shadow: 0 0 30px rgba(6,182,212,0.1);
    }

    .decorative-line {
      position: absolute;
      background: linear-gradient(to bottom, transparent, rgba(6,182,212,0.3), transparent);
      width: 1px;
      height: 200px;
      top: 200px;
      right: 80px;
    }

    .decorative-dot {
      position: absolute;
      width: 8px;
      height: 8px;
      background: #06B6D4;
      border-radius: 50%;
      opacity: 0.6;
    }

    .footer {
      margin-top: 80px;
      padding-top: 32px;
      border-top: 1px solid rgba(6,182,212,0.2);
      font-size: 22px;
      color: #64748B;
      font-family: 'Orbitron', sans-serif;
      letter-spacing: 3px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="decorative-line"></div>
    <div class="decorative-dot" style="top: 180px; right: 76px;"></div>
    <div class="decorative-dot" style="top: 400px; right: 76px;"></div>

    {% for segment in segments %}
    {% if segment.type == 'title' %}
    <h1 class="title">{{ segment.text }}</h1>
    {% elif segment.type == 'content' %}
    <p class="content">{{ segment.text }}</p>
    {% elif segment.type == 'highlight' %}
    <p class="highlight">{{ segment.text }}</p>
    {% elif segment.type == 'quote' %}
    <p class="quote">{{ segment.text }}</p>
    {% elif segment.type == 'code' %}
    <pre class="code">{{ segment.text }}</pre>
    {% endif %}
    {% endfor %}

    <div class="footer">
      &lt; ARTICLE-TO-MEDIA-IMAGE /&gt;
    </div>
  </div>
</body>
</html>
```

**Step 2: 提交**

```bash
git add templates/tech_modern/template.html
git commit -m "feat: add tech_modern (futuristic) template

- Geometric decorative elements
- Cyan and purple gradient
- Suitable for tech/AI content"
```

---

## Task 9: 创建 SKILL.md 入口文件

**Files:**
- Create: `SKILL.md`

**Step 1: 创建 SKILL.md**

Write content to `SKILL.md`:

```markdown
---
name: article-to-media-image
description: 文章转分享卡片。将文章/笔记转化为精美 HTML 卡片图片，支持 5 种视觉风格。触发场景：文章转图、笔记转卡片、生成分享图、文章可视化、内容卡片化。
---

# 文章转分享卡片

文章 → AI 分析内容 → 选择匹配风格 → 生成 HTML 卡片 → 后处理 → 截图交付。

## 设计理念

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
② 风格选择 — 根据内容调性选择合适的模板风格
    ↓
③ 生成 HTML — CLI 工具生成自包含 HTML
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
```

**Step 2: 验证 SKILL.md**

Run: `head -30 SKILL.md`
Expected: 包含 frontmatter (name, description) 和标题

**Step 3: 提交**

```bash
git add SKILL.md
git commit -m "feat: add SKILL.md entry point

- Define skill metadata and triggers
- Document 5 template styles
- Include usage examples for CLI and Python
- Add workflow and segment type reference"
```

---

## Task 10: 创建 CLI 入口文件

**Files:**
- Create: `src/cli.py`

**Step 1: 创建 CLI 入口**

Write content to `src/cli.py`:

```python
"""CLI entry point for article-to-media-image."""

import argparse
import json
import sys
from pathlib import Path
from .renderer.engine import RenderEngine
from .config import Settings


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="将文章转换为精美的 HTML 卡片"
    )
    parser.add_argument(
        "--template", "-t",
        choices=["minimal", "gradient", "card", "dark", "tech_modern"],
        default="tech_modern",
        help="模板风格 (默认: tech_modern)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="输出文件路径 (默认: ~/article-cards/{timestamp}-{template}.html)"
    )
    parser.add_argument(
        "--segments", "-s",
        help="JSON 格式的 segments 数据"
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="列出所有可用模板"
    )

    args = parser.parse_args()

    # List templates mode
    if args.list_templates:
        print("可用模板:")
        for template in ["minimal", "gradient", "card", "dark", "tech_modern"]:
            print(f"  - {template}")
        return 0

    # Parse segments
    if args.segments:
        try:
            segments = json.loads(args.segments)
        except json.JSONDecodeError as e:
            print(f"错误: JSON 解析失败 - {e}", file=sys.stderr)
            return 1
    else:
        # Read from stdin
        try:
            data = json.load(sys.stdin)
            segments = data.get("segments", [])
        except json.JSONDecodeError:
            print("错误: 请提供 --segments 参数或通过 stdin 传入 JSON", file=sys.stderr)
            return 1
        except Exception:
            print("错误: 无法读取 stdin", file=sys.stderr)
            return 1

    # Validate segments
    if not segments:
        print("错误: segments 不能为空", file=sys.stderr)
        return 1

    # Render
    try:
        engine = RenderEngine()
        output_path = engine.render_to_file(
            segments=segments,
            template=args.template,
            output_path=args.output
        )
        print(f"✅ Generated: {output_path}")
        print(f"🎨 Template: {args.template}")
        print(f"📦 Segments: {len(segments)}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Step 2: 更新模板路径**

修改 `src/renderer/engine.py` 第 25 行：

```python
# 旧代码
template_dir = Path(__file__).parent / "templates"

# 新代码
template_dir = Path(__file__).parent.parent.parent / "templates"
```

**Step 3: 验证 CLI 创建**

Run: `python3 -c "from src.cli import main; print('CLI module OK')"`
Expected: CLI module OK

**Step 4: 提交**

```bash
git add src/cli.py src/renderer/engine.py
git commit -m "feat: add CLI entry point

- Add src/cli.py with argparse interface
- Support --template, --output, --segments options
- Add --list-templates for template discovery
- Update template path in engine.py"
```

---

## Task 11: 更新 pyproject.toml

**Files:**
- Modify: `pyproject.toml`

**Step 1: 更新项目元数据和依赖**

替换 `pyproject.toml` 内容：

```toml
[project]
name = "article-to-media-image"
version = "0.2.0"
description = "Convert articles to shareable HTML card images"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "jinja2>=3.1.0",
    "pyyaml>=6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
article-to-card = "src.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
]
```

**Step 2: 验证配置**

Run: `cat pyproject.toml | grep -A2 "\[project.scripts\]"`
Expected: 包含 article-to-card 入口

**Step 3: 提交**

```bash
git add pyproject.toml
git commit -m "chore: update pyproject.toml for skill project

- Remove mcp dependency
- Add CLI entry point: article-to-card
- Bump version to 0.2.0"
```

---

## Task 12: 删除 MCP 相关文件

**Files:**
- Delete: `src/main.py`

**Step 1: 删除 main.py**

Run: `rm src/main.py`

**Step 2: 验证删除**

Run: `ls src/main.py 2>&1`
Expected: No such file or directory

**Step 3: 提交**

```bash
git add src/main.py
git commit -m "refactor: remove MCP server main.py

- Remove MCP protocol dependency
- Replaced by CLI interface in src/cli.py"
```

---

## Task 13: 创建后处理脚本

**Files:**
- Create: `scripts/post-process.sh`

**Step 1: 创建后处理脚本**

Write content to `scripts/post-process.sh`:

```bash
#!/bin/bash
# HTML 后处理脚本
# 用法: scripts/post-process.sh <html_file>

set -e

HTML_FILE="$1"

if [ -z "$HTML_FILE" ]; then
  echo "用法: $0 <html_file>"
  exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
  echo "错误: 文件不存在: $HTML_FILE"
  exit 1
fi

echo "后处理: $HTML_FILE"

# 备份原文件
cp "$HTML_FILE" "${HTML_FILE}.bak"

# 确保 container 使用 min-height
sed -i.tmp 's/height: 1440px/min-height: 1440px/g' "$HTML_FILE"
rm -f "${HTML_FILE}.tmp"

# 确保没有 margin: 0 auto
sed -i.tmp 's/margin: 0 auto;/margin: 0;/g' "$HTML_FILE"
rm -f "${HTML_FILE}.tmp"

# 确保宽度固定
sed -i.tmp 's/max-width: 1080px/width: 1080px/g' "$HTML_FILE"
rm -f "${HTML_FILE}.tmp"

echo "✅ 后处理完成"
```

**Step 2: 添加执行权限**

Run: `chmod +x scripts/post-process.sh`

**Step 3: 验证脚本**

Run: `ls -l scripts/post-process.sh`
Expected: 包含执行权限 (rwxr-xr-x)

**Step 4: 提交**

```bash
git add scripts/post-process.sh
git commit -m "feat: add HTML post-processing script

- Fix min-height vs height issues
- Fix max-width vs width issues
- Fix margin auto issues"
```

---

## Task 14: 更新 README.md

**Files:**
- Modify: `README.md`

**Step 1: 更新 README 内容**

替换 `README.md` 内容：

```markdown
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
```

**Step 2: 提交**

```bash
git add README.md
git commit -m "docs: update README for skill project

- Remove MCP configuration
- Add CLI usage examples
- Update template descriptions
- Add Python library usage"
```

---

## Task 15: 测试 CLI 功能

**Files:**
- Test: 验证 CLI 工具正常运行

**Step 1: 测试 CLI 帮助**

Run: `python3 -m src.cli --help`
Expected: 显示帮助信息

**Step 2: 测试列出模板**

Run: `python3 -m src.cli --list-templates`
Expected: 列出 5 个模板

**Step 3: 测试渲染功能**

Run:
```bash
echo '{"segments":[{"type":"title","text":"测试标题"},{"type":"content","text":"测试内容"}]}' | python3 -m src.cli -t minimal
```
Expected: 生成 HTML 文件并显示路径

**Step 4: 验证生成的 HTML**

Run: `ls -la ~/article-cards/*.html | tail -1`
Expected: 存在最新的 HTML 文件

**Step 5: 提交测试结果**

```bash
echo "# CLI 测试通过" | git commit -F -
git commit --allow-empty -m "test: verify CLI functionality

- Help command works
- List templates works
- Render to file works
- Generated HTML valid"
```

---

## Task 16: 清理和最终检查

**Files:**
- Various: 最终项目检查

**Step 1: 检查项目结构**

Run: `tree -L 2 -I '.git|__pycache__|*.pyc|.pytest_cache'`
Expected: 显示包含 SKILL.md, rules/, templates/, scripts/, src/

**Step 2: 检查模板文件**

Run: `find templates/ -name "template.html" | wc -l`
Expected: 5

**Step 3: 检查规则文件**

Run: `ls -1 rules/*.md`
Expected: 01-技术底线.md, 02-截图流程.md, 03-风格灵感.md

**Step 4: 最终 Git 状态**

Run: `git status`
Expected: working tree clean

**Step 5: 提交最终版本**

```bash
git add -A
git commit --allow-empty -m "feat: skill project refactor complete

- Removed MCP protocol dependency
- Added CLI interface (article-to-card)
- Created 5 HTML templates (minimal, gradient, card, dark, tech_modern)
- Added technical rules in rules/
- Added SKILL.md entry point
- Updated README.md

Project is now a standard skill project."
```

---

## 完成清单

- [ ] 目录结构创建
- [ ] 技术规则文件复制
- [ ] 风格灵感文档创建
- [ ] 5 个 HTML 模板创建
- [ ] SKILL.md 入口文件
- [ ] CLI 工具实现
- [ ] pyproject.toml 更新
- [ ] MCP 代码清理
- [ ] 后处理脚本
- [ ] README 更新
- [ ] CLI 功能测试
- [ ] 最终检查
