# Slide Card Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将14个信息图模版改造为独立卡片视窗式布局，每个语义段落采用3:4比例的独立卡片，段落之间有明确的视觉间隔。

**Architecture:**
- 新增 `templates/core/` 目录存放共享CSS
- 创建卡片基础样式和主题变量系统
- 每个模版HTML结构用 `.slide-card` 包裹语义段落
- 通过CSS变量实现分组差异化

**Tech Stack:** HTML5, CSS3, CSS Variables, Flexbox布局

---

## Task 1: 创建核心CSS文件结构

**Files:**
- Create: `templates/core/slide-card-base.css`
- Create: `templates/core/slide-themes.css`

**Step 1: 创建基础卡片样式文件**

创建 `templates/core/slide-card-base.css`:

```css
/* ========== SLIDE CARD BASE STYLES ========== */
/* 独立卡片视窗基础样式 - 适用于所有14个模版 */

* { margin: 0; padding: 0; box-sizing: border-box; }

/* 外层容器 - 深色背景，垂直滚动 */
body {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 20px;
  background: #1a1a2e;
  font-family: -apple-system, 'PingFang SC', 'Noto Sans SC', 'Helvetica Neue', sans-serif;
}

.container {
  width: 1080px;
  min-height: 100vh;
  padding: 60px 135px;
  display: flex;
  flex-direction: column;
  gap: var(--card-gap, 80px);
}

/* 独立卡片 - 3:4 比例 */
.slide-card {
  width: var(--card-width, 810px);
  height: var(--card-height, 1080px);
  background: var(--card-bg, #ffffff);
  border-radius: var(--card-radius, 16px);
  box-shadow: var(--card-shadow, 0 25px 50px rgba(0,0,0,0.4));
  border: 1px solid rgba(255,255,255,0.1);
  overflow: hidden;
  position: relative;
}

/* 发光渐变边框效果 */
.slide-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--card-radius, 16px);
  padding: 2px;
  background: var(--border-gradient, linear-gradient(135deg, #667eea, #764ba2));
  -webkit-mask: linear-gradient(#fff 0 0) content-box,
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
  opacity: 0.8;
}

/* 卡片内部容器 */
.slide-card .card-inner {
  width: 100%;
  height: 100%;
  padding: var(--card-padding, 48px);
  display: flex;
  flex-direction: column;
  gap: var(--inner-gap, 32px);
  overflow: hidden;
}

/* 段落编号水印 */
.slide-card .slide-number {
  position: absolute;
  bottom: 24px;
  right: 24px;
  font-size: 72px;
  font-weight: 900;
  color: rgba(0,0,0,0.03);
  font-family: 'Inter', 'SF Mono', monospace;
  pointer-events: none;
}

/* 隐藏坐标标记（用于模块定位） */
.coord { display: none; }
```

**Step 2: 创建主题变量文件**

创建 `templates/core/slide-themes.css`:

```css
/* ========== SLIDE CARD THEME VARIABLES ========== */
/* 各分组主题变量 */

/* 默认主题 */
:root {
  --card-width: 810px;
  --card-height: 1080px;
  --card-gap: 80px;
  --card-radius: 16px;
  --card-padding: 48px;
  --inner-gap: 32px;
  --card-shadow: 0 25px 50px rgba(0,0,0,0.4);
  --border-gradient: linear-gradient(135deg, #667eea, #764ba2);
  --card-bg: #ffffff;
}

/* A组：卡片式 - 深蓝渐变 */
.theme-card-blue {
  --card-shadow: 0 30px 60px rgba(0,0,0,0.5);
  --border-gradient: linear-gradient(135deg, #1E90FF, #00C853);
  --card-bg: linear-gradient(180deg, #0A192F 0%, #142233 50%, #0F1F35 100%);
}

/* B组：扁平式 - 浅色简约 */
.theme-flat-light {
  --card-shadow: 0 20px 40px rgba(0,0,0,0.15);
  --border-gradient: linear-gradient(135deg, #e2e8f0, #cbd5e1);
  --card-radius: 12px;
}

/* C组：科技式 - 霓虹发光 */
.theme-tech-glow {
  --card-shadow: 0 25px 50px rgba(0,0,0,0.6), 0 0 30px rgba(102, 126, 234, 0.3);
  --border-gradient: linear-gradient(135deg, #00f5ff, #667eea, #764ba2);
}

/* D组：信息图式 - 网格背景 */
.theme-infographic {
  --card-shadow: 0 15px 35px rgba(0,0,0,0.2);
  --border-gradient: linear-gradient(135deg, #B8D8BE, #3A7BD5);
  --card-bg: #F2F2F2;
}

/* E组：叙事式 - 纸质纹理 */
.theme-narrative {
  --card-shadow: 0 10px 30px rgba(0,0,0,0.2);
  --border-gradient: linear-gradient(135deg, #d4c5a9, #c4b393);
  --card-radius: 4px;
}
```

**Step 3: 验证CSS文件创建成功**

运行: `ls -la templates/core/`
预期输出: 显示 `slide-card-base.css` 和 `slide-themes.css` 两个文件

**Step 4: 提交**

```bash
git add templates/core/
git commit -m "feat: add slide card base styles and theme variables

- Create core CSS directory structure
- Add slide-card-base.css with 3:4 card layout
- Add slide-themes.css for 5 template groups
- Establish CSS variable system for theming

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: 改造 infographic.html 模版

**Files:**
- Modify: `templates/infographic.html`
- Reference: `templates/core/slide-card-base.css`

**Step 1: 备份原文件**

运行: `cp templates/infographic.html templates/infographic.html.bak`

**Step 2: 添加CSS引用和主题变量**

在 `<head>` 的 `<style>` 标签开始处添加:

```html
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap');

  /* 引入主题变量 - 信息图式 */
  @import url('../core/slide-themes.css');

  :root {
    /* 信息图式主题覆盖 */
    --card-bg: #F2F2F2;
    --border-gradient: linear-gradient(135deg, #B8D8BE, #3A7BD5);
    --card-padding: 40px;
  }

  /* 原有样式保持不变... */
```

**Step 3: 修改body和container样式**

找到现有的 `body` 和 `.container` 样式，替换为:

```css
  body {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding: 40px 20px;
    background: #1a1a2e;
    font-family: -apple-system, 'PingFang SC', 'Noto Sans SC', 'Helvetica Neue', sans-serif;
  }

  .container {
    width: 1080px;
    min-height: 100vh;
    padding: 60px 135px;
    display: flex;
    flex-direction: column;
    gap: 80px;
  }
```

**Step 4: 添加slide-card样式**

在样式末尾添加:

```css
  /* 独立卡片样式 */
  .slide-card {
    width: 810px;
    height: 1080px;
    background: #F2F2F2;
    border-radius: 2px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    border: 1px solid #2D2926;
    overflow: hidden;
    position: relative;
  }

  .slide-card .card-inner {
    width: 100%;
    height: 100%;
    padding: 40px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .slide-card .slide-number {
    position: absolute;
    bottom: 20px;
    right: 20px;
    font-size: 48px;
    font-weight: 900;
    color: rgba(0,0,0,0.05);
    font-family: 'SF Mono', monospace;
  }
```

**Step 5: 修改HTML结构 - 卡片1（标题区）**

将现有的 `<div class="header">` 包裹:

```html
<!-- SLIDE 1: 标题区 -->
<div class="slide-card" data-slide="1">
  <div class="card-inner">
    <div class="header">
      <span class="coord">SEC-00</span>
      <h1>【主标题：替换为文章核心主题】</h1>
      <div class="subtitle">INFOGRAPHIC · DATA SHEET · v1.0</div>
    </div>
    <span class="slide-number">01</span>
  </div>
</div>
```

**Step 6: 修改HTML结构 - 卡片2（MOD-1品牌矩阵）**

将 MOD-1 的 `.module` 包裹:

```html
<!-- SLIDE 2: 核心选项一览 -->
<div class="slide-card" data-slide="2">
  <div class="card-inner">
    <div class="module">
      <span class="coord">A-01</span>
      <h2>核心选项一览</h2>
      <div class="grid-3col">
        <!-- ... 原有brand-card内容 ... -->
      </div>
    </div>
    <span class="slide-number">02</span>
  </div>
</div>
```

**Step 7: 修改HTML结构 - 卡片3（MOD-2规格标尺）**

将 MOD-2 包裹:

```html
<!-- SLIDE 3: 关键维度对比 -->
<div class="slide-card" data-slide="3">
  <div class="card-inner">
    <div class="module">
      <span class="coord">B-05</span>
      <h2>关键维度对比</h2>
      <div class="scale-bar">
        <!-- ... 原有scale-bar内容 ... -->
      </div>
      <div class="scale-label">
        <span>0</span><span>|</span><span>|</span><span>|</span><span>MAX</span>
      </div>
    </div>
    <span class="slide-number">03</span>
  </div>
</div>
```

**Step 8: 修改HTML结构 - 卡片4（MOD-3+MOD-4双栏）**

将 MOD-3 和 MOD-4 的 `.grid-2col` 包裹:

```html
<!-- SLIDE 4: 深度剖析与场景对比 -->
<div class="slide-card" data-slide="4">
  <div class="card-inner">
    <div class="grid-2col">
      <!-- MOD-3: 深度剖析 -->
      <div class="module">
        <span class="coord">C-12</span>
        <h2>深度剖析</h2>
        <p style="font-size:14px; color:#333; line-height:1.8;">
          核心观点描述。使用 <span class="highlight">荧光笔标记</span> 突出关键信息。
          数据支撑：<span class="data-point">87%</span> 的用户认为此方案有效。
        </p>
      </div>
      <!-- MOD-4: 场景对比 -->
      <div class="module">
        <span class="coord">D-03</span>
        <h2>场景对比</h2>
        <!-- ... 原有场景对比内容 ... -->
      </div>
    </div>
    <span class="slide-number">04</span>
  </div>
</div>
```

**Step 9: 修改HTML结构 - 卡片5（MOD-5警告）**

将 MOD-5 的 `.warning` 包裹:

```html
<!-- SLIDE 5: 避坑指南 -->
<div class="slide-card" data-slide="5">
  <div class="card-inner">
    <div class="warning">
      <span class="coord">E-08</span>
      <h2 style="color:#E91E63; font-size:18px; margin-bottom:8px; padding-left:0;">⚠ 避坑指南</h2>
      <ul>
        <li>第一个常见错误：简要说明</li>
        <li>第二个常见错误：简要说明</li>
        <li>第三个常见错误：简要说明</li>
      </ul>
    </div>
    <span class="slide-number">05</span>
  </div>
</div>
```

**Step 10: 修改HTML结构 - 卡片6（MOD-6+MOD-7+Footer）**

将 MOD-6、MOD-7 和 Footer 包裹:

```html
<!-- SLIDE 6: 速查数据与总结 -->
<div class="slide-card" data-slide="6">
  <div class="card-inner">
    <!-- MOD-6: 速查表 -->
    <div class="module">
      <span class="coord">F-15</span>
      <h2>速查数据表</h2>
      <table class="data-table">
        <!-- ... 原有表格内容 ... -->
      </table>
    </div>

    <!-- MOD-7: 状态栏 -->
    <div class="module" style="padding:0;">
      <span class="coord">G-20</span>
      <div class="status-bar">
        <!-- ... 原有状态栏内容 ... -->
      </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
      <span>Generated by openclaw · article-to-html</span>
      <span>REV 1.0 · 2026</span>
    </div>

    <span class="slide-number">06</span>
  </div>
</div>
```

**Step 11: 验证HTML结构**

运行: `grep -c 'slide-card' templates/infographic.html`
预期输出: `6` (6个卡片)

**Step 12: 在浏览器中测试视觉效果**

运行: `open templates/infographic.html`
预期: 显示6个独立的3:4卡片，段落间隔明显

**Step 13: 删除备份文件**

运行: `rm templates/infographic.html.bak`

**Step 14: 提交**

```bash
git add templates/infographic.html
git commit -m "feat: convert infographic.html to slide card layout

- Wrap semantic sections in .slide-card containers
- Apply 3:4 card dimensions (810x1080px)
- Add visual separation between 6 paragraph sections
- Preserve original infographic styling
- Add slide number watermarks

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: 改造 A组 - style-card-deep-blue.html

**Files:**
- Modify: `templates/style-card-deep-blue.html`
- Theme: A组卡片式

**Step 1: 备份原文件**

运行: `cp templates/style-card-deep-blue.html templates/style-card-deep-blue.html.bak`

**Step 2: 修改容器样式**

找到 `.container` 样式，修改为:

```css
  .container {
    width: 1080px;
    min-height: 100vh;
    padding: 60px 135px;
    display: flex;
    flex-direction: column;
    gap: 80px;
  }

  /* 独立卡片样式 - 深蓝渐变 */
  .slide-card {
    width: 810px;
    height: 1080px;
    background: linear-gradient(180deg, #0A192F 0%, #142233 50%, #0F1F35 100%);
    border-radius: 12px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.1);
    overflow: hidden;
    position: relative;
  }

  .slide-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #1E90FF, transparent);
  }

  .slide-card .card-inner {
    width: 100%;
    height: 100%;
    padding: 48px 52px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .slide-card .slide-number {
    position: absolute;
    bottom: 24px;
    right: 24px;
    font-size: 48px;
    font-weight: 900;
    color: rgba(30,144,255,0.1);
    font-family: 'Inter', sans-serif;
  }
```

**Step 3: 包裹段落 - 卡片1（Header）**

将 `.header` 包裹:

```html
<!-- SLIDE 1: 标题区 -->
<div class="slide-card" data-slide="1">
  <div class="card-inner">
    <div class="header">
      <span class="coord">SEC-00</span>
      <div class="tag">INSIGHT BRIEF</div>
      <h1>Agent<span class="highlight">认知</span>：OS与Application</h1>
      <p class="subtitle">垂类不该做Agent，该做Agent上面的应用。战场不同，壁垒不同。</p>
    </div>
    <span class="slide-number">01</span>
  </div>
</div>
```

**Step 4: 包裹段落 - 卡片2（MOD-1核心数据）**

将 `.data-strip` 包裹:

```html
<!-- SLIDE 2: 核心数据 -->
<div class="slide-card" data-slide="2">
  <div class="card-inner">
    <span class="coord">A-01</span>
    <div class="data-strip">
      <!-- ... 原有data-card内容 ... -->
    </div>
    <span class="slide-number">02</span>
  </div>
</div>
```

**Step 5: 包裹段落 - 卡片3（MOD-2三大核心卡片）**

将 `.feature-grid` 包裹:

```html
<!-- SLIDE 3: 三大核心卡片 -->
<div class="slide-card" data-slide="3">
  <div class="card-inner">
    <span class="coord">B-05</span>
    <div class="feature-grid">
      <!-- ... 原有feature-card内容 ... -->
    </div>
    <span class="slide-number">03</span>
  </div>
</div>
```

**Step 6: 包裹段落 - 卡片4（MOD-3三层光谱）**

将 `.spectrum-section` 包裹:

```html
<!-- SLIDE 4: 三层光谱 -->
<div class="slide-card" data-slide="4">
  <div class="card-inner">
    <span class="coord">C-12</span>
    <div class="spectrum-section">
      <h2>从指令到服务的三层光谱</h2>
      <div class="spectrum-grid">
        <!-- ... 原有spectrum-item内容 ... -->
      </div>
    </div>
    <span class="slide-number">04</span>
  </div>
</div>
```

**Step 7: 包裹段落 - 卡片5（MOD-4核心洞察）**

将 `.insight-box` 包裹:

```html
<!-- SLIDE 5: 核心洞察 -->
<div class="slide-card" data-slide="5">
  <div class="card-inner">
    <span class="coord">D-03</span>
    <div class="insight-box">
      <h3>核心洞察</h3>
      <p>
        好的Application让Agent OS<span class="highlight">变得更聪明</span>。领域推理搬到外部，干扰消失，其他任务更准，于是更精准调用更多Application——<span class="highlight">认知共生飞轮</span>转起来了。<br><br>
        The best context is <span class="highlight">no context</span>。Agent越轻，表现越好。
      </p>
    </div>
    <span class="slide-number">05</span>
  </div>
</div>
```

**Step 8: 包裹段落 - 卡片6（MOD-5+MOD-6+Footer）**

将 `.warning-box`、`.tag-row` 和 `.footer` 包裹:

```html
<!-- SLIDE 6: 避坑警告与标签 -->
<div class="slide-card" data-slide="6">
  <div class="card-inner">
    <!-- MOD-5: 避坑警告 -->
    <div class="warning-box">
      <span class="coord">E-08</span>
      <h3>⚠️ 垂类做OS的三个致命理由</h3>
      <div class="warning-list">
        <!-- ... 原有warning-item内容 ... -->
      </div>
    </div>

    <!-- MOD-6: 标签 -->
    <div class="tag-row">
      <span class="coord">F-15</span>
      <!-- ... 原有tag-item内容 ... -->
    </div>

    <!-- FOOTER -->
    <div class="footer">
      <span>AGENT COGNITION · DEEP BLUE TECH</span>
      <span>OS × APPLICATION · 2026</span>
    </div>

    <span class="slide-number">06</span>
  </div>
</div>
```

**Step 9: 验证并测试**

运行: `open templates/style-card-deep-blue.html`
预期: 显示6个深蓝色渐变卡片，有顶部发光线效果

**Step 10: 清理并提交**

```bash
rm templates/style-card-deep-blue.html.bak
git add templates/style-card-deep-blue.html
git commit -m "feat: convert style-card-deep-blue.html to slide card layout

- Group A: Card style template
- Apply 3:4 card dimensions with deep blue gradient
- Add top glow line effect
- Preserve original data strip and feature grid styling
- Wrap 6 semantic sections

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: 改造 A组 - style-dialog-red-blue.html

**Files:**
- Modify: `templates/style-dialog-red-blue.html`
- Theme: A组卡片式

**Step 1: 读取文件确认结构**

运行: `head -50 templates/style-dialog-red-blue.html`
预期: 确认文件存在，查看现有结构

**Step 2: 按照style-card-deep-blue.html的模式改造**

- 修改`.container`样式添加80px gap
- 添加`.slide-card`和`.card-inner`样式
- 用`.slide-card`包裹6个语义段落
- 添加`.slide-number`水印

**Step 3: 提交**

```bash
git add templates/style-dialog-red-blue.html
git commit -m "feat: convert style-dialog-red-blue.html to slide card layout

- Group A: Card style template (red-blue dialog)
- Apply 3:4 card dimensions
- Preserve dialog-style layout elements
- Wrap semantic sections in slide cards

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: 改造 B组 - style-nordic.html

**Files:**
- Modify: `templates/style-nordic.html`
- Theme: B组扁平式

**Step 1: 添加扁平式卡片样式**

```css
  .container {
    width: 1080px;
    min-height: 100vh;
    padding: 60px 135px;
    display: flex;
    flex-direction: column;
    gap: 80px;
  }

  /* 扁平式卡片 - 浅色简约 */
  .slide-card {
    width: 810px;
    height: 1080px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    border: 1px solid #e2e8f0;
    overflow: hidden;
    position: relative;
  }

  .slide-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 12px;
    padding: 1px;
    background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
                  linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
  }

  .slide-card .card-inner {
    width: 100%;
    height: 100%;
    padding: 56px;
    display: flex;
    flex-direction: column;
    gap: 40px;
  }

  .slide-card .slide-number {
    position: absolute;
    bottom: 24px;
    right: 24px;
    font-size: 56px;
    font-weight: 300;
    color: rgba(0,0,0,0.04);
    font-family: 'Inter', sans-serif;
  }
```

**Step 2: 包裹语义段落**

按语义将内容分为6个卡片包裹

**Step 3: 提交**

```bash
git add templates/style-nordic.html
git commit -m "feat: convert style-nordic.html to slide card layout

- Group B: Flat style template
- Apply minimal shadow and subtle border
- Use light color palette
- Preserve Nordic design simplicity

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: 改造 B组 - style-magazine.html

**Files:**
- Modify: `templates/style-magazine.html`
- Theme: B组扁平式

**Step 1: 按照style-nordic.html的模式改造**

- 应用扁平式卡片样式
- 保持杂志风格的排版元素
- 包裹语义段落

**Step 2: 提交**

```bash
git add templates/style-magazine.html
git commit -m "feat: convert style-magazine.html to slide card layout

- Group B: Flat style template (magazine)
- Apply minimal card styling
- Preserve magazine editorial layout
- Wrap semantic sections

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 7: 改造 C组 - style-dark-tech.html

**Files:**
- Modify: `templates/style-dark-tech.html`
- Theme: C组科技式（霓虹发光）

**Step 1: 添加科技式卡片样式**

```css
  .container {
    width: 1080px;
    min-height: 100vh;
    padding: 60px 135px;
    display: flex;
    flex-direction: column;
    gap: 80px;
  }

  /* 科技式卡片 - 霓虹发光 */
  .slide-card {
    width: 810px;
    height: 1080px;
    background: #0a0a0a;
    border-radius: 16px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.6), 0 0 30px rgba(102, 126, 234, 0.3);
    border: 1px solid rgba(102, 126, 234, 0.3);
    overflow: hidden;
    position: relative;
  }

  .slide-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    padding: 2px;
    background: linear-gradient(135deg, #00f5ff, #667eea, #764ba2);
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
                  linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    animation: glow 3s ease-in-out infinite alternate;
  }

  @keyframes glow {
    from { opacity: 0.6; }
    to { opacity: 1; }
  }

  .slide-card .card-inner {
    width: 100%;
    height: 100%;
    padding: 48px;
    display: flex;
    flex-direction: column;
    gap: 32px;
  }

  .slide-card .slide-number {
    position: absolute;
    bottom: 24px;
    right: 24px;
    font-size: 64px;
    font-weight: 900;
    color: rgba(0, 245, 255, 0.1);
    font-family: 'Orbitron', monospace;
    text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
  }
```

**Step 2: 包裹语义段落**

**Step 3: 提交**

```bash
git add templates/style-dark-tech.html
git commit -m "feat: convert style-dark-tech.html to slide card layout

- Group C: Tech style template (dark mode)
- Add neon glow animated border
- Apply cyberpunk aesthetic
- Preserve dark tech visual elements

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 8-12: 改造剩余模版

按相同模式完成：

- **Task 8**: style-retro-future.html (C组科技式)
- **Task 9**: style-lab-blueprint.html (C组科技式)
- **Task 10**: style-business.html (D组信息图式)
- **Task 11**: style-journal.html (D组信息图式)
- **Task 12**: style-newspaper.html (E组叙事式)

每个任务遵循相同步骤：
1. 备份原文件
2. 添加对应分组卡片样式
3. 包裹语义段落
4. 验证测试
5. 提交

---

## Task 13: 改造 E组 - style-memphis.html

**Files:**
- Modify: `templates/style-memphis.html`
- Theme: E组叙事式（孟菲斯风格）

**Step 1: 添加孟菲斯风格卡片样式**

```css
  /* 叙事式卡片 - 孟菲斯风格 */
  .slide-card {
    width: 810px;
    height: 1080px;
    background: #fff8e7;
    border-radius: 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    border: 3px solid #000;
    overflow: hidden;
    position: relative;
  }

  .slide-card::before {
    content: '';
    position: absolute;
    top: -10px;
    left: -10px;
    width: 40px;
    height: 40px;
    background: #ff6b6b;
    border: 3px solid #000;
    border-radius: 50%;
  }

  .slide-card::after {
    content: '';
    position: absolute;
    bottom: -15px;
    right: -15px;
    width: 0;
    height: 0;
    border-left: 25px solid transparent;
    border-right: 25px solid transparent;
    border-bottom: 40px solid #4ecdc4;
    transform: rotate(45deg);
  }

  .slide-card .card-inner {
    width: 100%;
    height: 100%;
    padding: 48px;
    display: flex;
    flex-direction: column;
    gap: 32px;
  }

  .slide-card .slide-number {
    position: absolute;
    bottom: 24px;
    right: 24px;
    font-size: 72px;
    font-weight: 900;
    color: rgba(0,0,0,0.05);
    font-family: 'Space Mono', monospace;
  }
```

**Step 2: 包裹语义段落**

**Step 3: 提交**

```bash
git add templates/style-memphis.html
git commit -m "feat: convert style-memphis.html to slide card layout

- Group E: Narrative style template (Memphis design)
- Apply bold geometric shapes and colors
- Preserve Memphis aesthetic elements
- Wrap semantic sections

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 14-15: 完成最后两个模版

- **Task 14**: style-process-blue-green.html (E组叙事式)
- **Task 15**: style-step-blue.html (E组叙事式)

---

## Task 16: 验证所有模版

**Step 1: 检查所有模版是否有slide-card**

运行: `for f in templates/*.html; do echo -n "$f: "; grep -c 'slide-card' "$f" || echo "0"; done`
预期: 每个文件显示 > 0 的卡片数量

**Step 2: 创建测试脚本**

创建 `scripts/validate-templates.sh`:

```bash
#!/bin/bash
echo "Validating slide card templates..."
for file in templates/*.html; do
  count=$(grep -c 'slide-card' "$file" 2>/dev/null || echo "0")
  if [ "$count" -gt 0 ]; then
    echo "✓ $file has $count slide cards"
  else
    echo "✗ $file has no slide cards"
  fi
done
```

**Step 3: 运行验证脚本**

运行: `chmod +x scripts/validate-templates.sh && scripts/validate-templates.sh`
预期: 所有14个模版显示✓

**Step 4: 提交验证脚本**

```bash
git add scripts/validate-templates.sh
git commit -m "test: add template validation script

- Check all templates for slide-card structure
- Report card count per template
- Flag templates missing conversion

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 17: 更新文档

**Step 1: 更新SKILL.md**

在SKILL.md中添加关于新布局的说明

**Step 2: 创建README（如果不存在）**

创建 `templates/README.md`:

```markdown
# Information Chart Templates

## Slide Card Layout

All templates now use the **Independent Card Viewport** design:
- Each semantic paragraph is wrapped in a 3:4 card (810x1080px)
- Cards have 80px visual separation
- Organized into 5 style groups for consistent theming

## Template Groups

| Group | Templates | Style |
|-------|-----------|-------|
| A | style-card-deep-blue, style-dialog-red-blue | Card |
| B | style-nordic, style-magazine | Flat |
| C | style-dark-tech, style-retro-future, style-lab-blueprint | Tech |
| D | infographic, style-business, style-journal | Infographic |
| E | style-newspaper, style-memphis, style-process-blue-green, style-step-blue | Narrative |
```

**Step 3: 提交文档**

```bash
git add SKILL.md templates/README.md
git commit -m "docs: update template documentation

- Document slide card layout design
- List all 14 templates with style groups
- Add conversion notes

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 18: 最终验证和清理

**Step 1: 运行完整验证**

运行: `scripts/validate-templates.sh`

**Step 2: 检查git状态**

运行: `git status`

**Step 3: 创建最终提交**

```bash
git add -A
git commit -m "feat: complete slide card redesign for all 14 templates

Implementation complete:
- Created core CSS infrastructure (base + themes)
- Converted all 14 templates to slide card layout
- Organized templates into 5 style groups
- Added validation scripts and documentation

All templates now display:
- 3:4 card dimensions (810x1080px)
- Clear visual separation between paragraphs
- Group-appropriate styling
- Slide number watermarks

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## 验收标准

- [ ] 14个模版全部使用 `.slide-card` 结构
- [ ] 每个卡片保持 3:4 比例 (810x1080px)
- [ ] 卡片之间有 80px 间隔
- [ ] 每个分组有独特的视觉风格
- [ ] 保留原有模版的设计元素
- [ ] 所有文件已提交到 git
- [ ] 文档已更新

---

## 备注

- 如需调整卡片尺寸，修改 CSS 变量 `--card-width` 和 `--card-height`
- 间隔距离通过 `--card-gap` 控制
- 各分组主题可在 `slide-themes.css` 中统一调整
