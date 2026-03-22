# 信息图模版卡片化设计文档

**日期**: 2026-03-22
**设计者**: Claude Code
**状态**: 已批准

---

## 1. 概述

### 1.1 设计目标

优化14个信息图模版，实现：
1. 段落之间有明确的视觉间隔
2. 每个段落采用 3:4 比例的独立卡片视窗
3. 保持各模版原有设计语言

### 1.2 核心方案

**独立卡片视窗式**：每个语义段落被包装在独立的 3:4 卡片中，卡片具有边框、阴影和圆角，段落之间有充足间距。

---

## 2. 架构设计

### 2.1 HTML结构

```html
<!-- 外层容器 -->
<div class="container">
  <div class="slide-card" data-slide="1">
    <!-- 段落1：标题区 -->
  </div>
  <div class="slide-card" data-slide="2">
    <!-- 段落2：数据展示 -->
  </div>
  <div class="slide-card" data-slide="3">
    <!-- 段落3：核心观点 -->
  </div>
</div>
```

### 2.2 CSS核心样式

```css
/* 外层容器 */
.container {
  width: 1080px;
  min-height: 100vh;
  background: #1a1a2e;
  padding: 60px 135px;
  display: flex;
  flex-direction: column;
  gap: 80px;
}

/* 独立卡片 3:4 */
.slide-card {
  width: 810px;
  height: 1080px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(0,0,0,0.4);
  border: 1px solid rgba(255,255,255,0.1);
  overflow: hidden;
  position: relative;
}

/* 发光边框 */
.slide-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 2px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-mask: linear-gradient(#fff 0 0) content-box,
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}
```

---

## 3. 段落划分规则

### 3.1 通用分段模式

| 段落 | 内容 | 典型模块 |
|------|------|----------|
| Slide 1 | 标题区 | Header（标题+副标题） |
| Slide 2 | 数据展示 | MOD-1 核心数据/KPI |
| Slide 3 | 核心观点 | MOD-2 + MOD-3 深度分析 |
| Slide 4 | 对比/场景 | MOD-4 场景对比/光谱 |
| Slide 5 | 警告/避坑 | MOD-5 避坑指南 |
| Slide 6 | 总结/行动 | MOD-6 + MOD-7 + Footer |

### 3.2 灵活调整

- 内容少的段落可合并
- 内容多的段落可拆分
- 每个卡片保持视觉平衡

---

## 4. 模版分组与适配

### 4.1 分组策略

| 分组 | 模版 | 适配重点 |
|------|------|----------|
| **A组：卡片式** | style-card-deep-blue, style-dialog-red-blue | 保持现有卡片风格，添加外层包裹 |
| **B组：扁平式** | style-nordic, style-magazine | 增强卡片边框和阴影效果 |
| **C组：科技式** | style-dark-tech, style-retro-future, style-lab-blueprint | 添加发光边框和渐变 |
| **D组：信息图式** | infographic, style-business, style-journal | 调整内部模块间距 |
| **E组：叙事式** | style-newspaper, style-memphis, style-process-blue-green, style-step-blue | 保留叙事流程和风格特征 |

### 4.2 CSS变量系统

```css
:root {
  --card-width: 810px;
  --card-height: 1080px;
  --card-gap: 80px;
  --card-radius: 16px;
  --card-shadow: 0 25px 50px rgba(0,0,0,0.4);
  --border-gradient: linear-gradient(135deg, #667eea, #764ba2);
}
```

---

## 5. 文件结构

```
templates/
├── core/
│   ├── slide-card-base.css      # 新增：卡片基础样式
│   └── slide-themes.css          # 新增：各分组主题变量
├── infographic.html               # 修改
├── style-business.html            # 修改
├── style-card-deep-blue.html      # 修改
├── style-dark-tech.html           # 修改
├── style-dialog-red-blue.html     # 修改
├── style-journal.html             # 修改
├── style-lab-blueprint.html       # 修改
├── style-magazine.html            # 修改
├── style-memphis.html             # 修改
├── style-newspaper.html           # 修改
├── style-nordic.html              # 修改
├── style-process-blue-green.html  # 修改
├── style-retro-future.html        # 修改
└── style-step-blue.html           # 修改
```

---

## 6. 实施原则

1. **最小改动**：保留现有样式，只做包裹和间距调整
2. **向后兼容**：通过CSS变量控制，不破坏原设计
3. **渐进增强**：可选择性应用新样式

---

## 7. 下一步

编写详细实施计划 → [writing-plans skill]
