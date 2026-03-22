# Skill 重构实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标:** 移除Python相关功能和CLI功能，将项目重构为纯文档化的OpenClaw Skill

**架构:** 删除所有Python源代码和测试，将templates移到根目录，为每个模板添加README说明，更新SKILL.md移除CLI相关内容

**技术栈:** 纯Markdown/HTML/CSS文档，无代码依赖

---

### Task 1: 迁移templates到根目录

**Files:**
- Move: `src/renderer/templates/*` → `templates/`

**Step 1: 移动templates目录**

```bash
mv src/renderer/templates templates
```

**Step 2: 验证移动成功**

```bash
ls -la templates/
# 预期输出: 包含 card, dark, gradient, minimal, tech_modern 五个子目录
```

**Step 3: 提交**

```bash
git add src/renderer/templates templates
git commit -m "refactor: move templates to root directory

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2: 创建minimal模板README

**Files:**
- Create: `templates/minimal/README.md`

**Step 1: 创建minimal/README.md**

```bash
cat > templates/minimal/README.md << 'EOF'
# Minimal（北欧极简）模板

## 设计特征
- 大量留白，呼吸感强
- 衬线字体 (Playfair Display + Lora)
- 灰度配色，偶尔单色点缀
- 无装饰元素，纯粹排版

## 适用场景
- 技术文档
- 严肃分析
- 学术内容

## 关键设计点
- **配色**:
  - 背景: #FAFAFA 或 #FFFFFF
  - 文字: #2C2C2C
  - 强调: #6B7280
- **字体**:
  - 标题: Playfair Display
  - 正文: Lora
  - 衬线字体增强专业感
- **布局**:
  - 单栏布局
  - 模块间距 32px
  - 内边距 48px

## 技术要点
- 固定宽度 1080px
- 使用 min-height 而非固定 height
- 字号：标题 72px，正文 32px
EOF
```

**Step 2: 验证文件创建**

```bash
cat templates/minimal/README.md
# 预期输出: 显示README.md完整内容
```

**Step 3: 提交**

```bash
git add templates/minimal/README.md
git commit -m "docs: add minimal template README

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: 创建gradient模板README

**Files:**
- Create: `templates/gradient/README.md`

**Step 1: 创建gradient/README.md**

```bash
cat > templates/gradient/README.md << 'EOF'
# Gradient（杂志渐变）模板

## 设计特征
- 暖色渐变背景（橙/粉/紫）
- 圆角卡片 (24px border-radius)
- 柔和阴影
- 层次分明的内容区块

## 适用场景
- 生活感悟
- 情感故事
- 随笔

## 关键设计点
- **配色**:
  - 渐变: linear-gradient(135deg, #FF6B6B, #FFE66D)
  - 卡片背景: rgba(255,255,255,0.9)
  - 文字: #2D3436
- **字体**:
  - 标题: 无衬线粗体
  - 正文: 无衬线常规
  - 柔和友好
- **布局**:
  - 圆角卡片堆叠
  - 卡片间距 24px
  - 内边距 48px
- **装饰**:
  - 24px border-radius
  - 柔和 box-shadow

## 技术要点
- 固定宽度 1080px
- 使用 min-height 而非固定 height
- 字号：标题 72px，正文 32px
- 卡片背景使用半透明效果
EOF
```

**Step 2: 验证文件创建**

```bash
cat templates/gradient/README.md
# 预期输出: 显示README.md完整内容
```

**Step 3: 提交**

```bash
git add templates/gradient/README.md
git commit -m "docs: add gradient template README

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 4: 创建card模板README

**Files:**
- Create: `templates/card/README.md`

**Step 1: 创建card/README.md**

```bash
cat > templates/card/README.md << 'EOF'
# Card（信息卡片）模板

## 设计特征
- 模块化卡片布局
- 图标装饰 (emoji 或简单图形)
- 每个信息点独立卡片
- 标签化组织

## 适用场景
- 知识分享
- 教程总结
- 要点梳理

## 关键设计点
- **配色**:
  - 背景: #F0F4F8
  - 卡片: #FFFFFF
  - 边框: #E1E8EF
  - 标签: #3B82F6
- **字体**:
  - 标题: 无衬线粗体
  - 正文: 无衬线常规
  - 清晰易读
- **布局**:
  - 多卡片网格布局
  - 卡片间距 20px
  - 内边距 40px
- **装饰**:
  - 图标/emoji前缀
  - 标签化分类

## 技术要点
- 固定宽度 1080px
- 使用 min-height 而非固定 height
- 字号：标题 72px，正文 30px
- 卡片使用flex或grid布局
EOF
```

**Step 2: 验证文件创建**

```bash
cat templates/card/README.md
# 预期输出: 显示README.md完整内容
```

**Step 3: 提交**

```bash
git add templates/card/README.md
git commit -m "docs: add card template README

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 5: 创建dark模板README

**Files:**
- Create: `templates/dark/README.md`

**Step 1: 创建dark/README.md**

```bash
cat > templates/dark/README.md << 'EOF'
# Dark（暗色科技）模板

## 设计特征
- 深色背景 (#0D1117)
- 霓虹强调色 (绿/蓝/紫)
- 代码高亮样式
- 终端感排版

## 适用场景
- 开发者内容
- 技术文章
- 代码教程

## 关键设计点
- **配色**:
  - 背景: #0D1117
  - 文字: #C9D1D9
  - 强调: #58A6FF
  - 代码背景: #161B22
- **字体**:
  - 标题: 无衬线粗体
  - 正文: 无衬线常规
  - 代码: 等宽字体
- **布局**:
  - 单栏布局
  - 模块间距 32px
  - 内边距 48px
- **装饰**:
  - 终端风格的边框
  - 霓虹色强调

## 技术要点
- 固定宽度 1080px
- 使用 min-height 而非固定 height
- 字号：标题 72px，正文 32px
- 代码块使用等宽字体和深色背景
EOF
```

**Step 2: 验证文件创建**

```bash
cat templates/dark/README.md
# 预期输出: 显示README.md完整内容
```

**Step 3: 提交**

```bash
git add templates/dark/README.md
git commit -m "docs: add dark template README

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6: 创建tech_modern模板README

**Files:**
- Create: `templates/tech_modern/README.md`

**Step 1: 创建tech_modern/README.md**

```bash
cat > templates/tech_modern/README.md << 'EOF'
# Tech Modern（现代科技）模板

## 设计特征
- 几何线条装饰
- 未来感配色（青/紫/银）
- 动态元素暗示（箭头、光点）
- 科技感字体

## 适用场景
- 科技资讯
- AI 相关
- 前沿技术

## 关键设计点
- **配色**:
  - 背景: #0F172A
  - 渐变: linear-gradient(to right, #06B6D4, #8B5CF6)
  - 文字: #E2E8F0
  - 装饰: rgba(6,182,212,0.3)
- **字体**:
  - 标题: 无衬线超粗
  - 正文: 无衬线常规
  - 现代感强
- **布局**:
  - 单栏布局
  - 模块间距 32px
  - 内边距 48px
- **装饰**:
  - 几何线条
  - 渐变装饰
  - 半透明光点

## 技术要点
- 固定宽度 1080px
- 使用 min-height 而非固定 height
- 字号：标题 72px，正文 32px
- 装饰元素使用绝对定位或伪元素
EOF
```

**Step 2: 验证文件创建**

```bash
cat templates/tech_modern/README.md
# 预期输出: 显示README.md完整内容
```

**Step 3: 提交**

```bash
git add templates/tech_modern/README.md
git commit -m "docs: add tech_modern template README

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7: 更新SKILL.md - 移除CLI/Python内容

**Files:**
- Modify: `SKILL.md:31-42` (删除CLI使用方式)
- Modify: `SKILL.md:44-58` (删除Python库使用方式)
- Modify: `SKILL.md:107-119` (删除安装说明)

**Step 1: 读取当前SKILL.md内容**

```bash
cat SKILL.md
```

**Step 2: 使用Edit工具移除CLI使用方式部分**

删除第31-42行的"### 作为 CLI 工具"部分

**Step 3: 使用Edit工具移除Python库使用方式部分**

删除第44-58行的"### 作为 Python 库"部分

**Step 4: 使用Edit工具移除安装说明部分**

删除第107-119行的"## 安装"部分

**Step 5: 验证修改**

```bash
cat SKILL.md
# 预期输出: 不再包含CLI、Python库和安装相关内容
```

**Step 6: 提交**

```bash
git add SKILL.md
git commit -m "refactor: remove CLI and Python library usage from SKILL.md

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 8: 更新SKILL.md - 添加模板学习指南

**Files:**
- Modify: `SKILL.md` (在工作流程后添加新章节)

**Step 1: 添加模板学习指南章节**

在"## 工作流程"章节后，"## 目录结构"章节前添加：

```markdown
## 模板学习指南

AI 应按以下步骤学习模板：

1. **阅读 SKILL.md** — 了解设计理念和工作流程
2. **分析用户内容** — 判断内容类型和调性
3. **参考 rules/03-风格灵感.md** — 选择合适的风格
4. **阅读 templates/[风格]/README.md** — 了解该风格的设计要点
5. **参考 templates/[风格]/template.html** — 学习代码结构
6. **生成 HTML** — 遵守 rules/01-技术底线.md 直接生成
7. **截图交付** — 按 rules/02-截图流程.md 执行

**模板选择原则：**

| 内容类型 | 自动选择风格 |
|---------|-------------|
| 技术文档/严肃分析 | `minimal` |
| 生活感悟/情感故事 | `gradient` |
| 知识分享/教程总结 | `card` |
| 开发者内容/代码 | `dark` |
| 科技资讯/AI 相关 | `tech_modern` |
```

**Step 2: 验证修改**

```bash
cat SKILL.md
# 预期输出: 包含新增的模板学习指南章节
```

**Step 3: 提交**

```bash
git add SKILL.md
git commit -m "docs: add template learning guide to SKILL.md

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 9: 更新SKILL.md目录结构说明

**Files:**
- Modify: `SKILL.md` (更新目录结构表格)

**Step 1: 更新目录结构表格**

将"## 目录结构"章节的表格更新为：

```markdown
## 目录结构

| 文件 | 说明 |
|------|------|
| `rules/01-技术底线.md` | **必读**：字号、宽度等硬性约束 |
| `rules/02-截图流程.md` | 截图交付流程 |
| `rules/03-风格灵感.md` | 5 种模板的风格说明 |
| `templates/minimal/` | 北欧极简风格模板 + README |
| `templates/gradient/` | 杂志渐变风格模板 + README |
| `templates/card/` | 信息卡片风格模板 + README |
| `templates/dark/` | 暗色科技风格模板 + README |
| `templates/tech_modern/` | 现代科技风格模板 + README |
```

**Step 2: 验证修改**

```bash
grep -A 10 "## 目录结构" SKILL.md
# 预期输出: 显示更新后的目录结构表格
```

**Step 3: 提交**

```bash
git add SKILL.md
git commit -m "docs: update directory structure in SKILL.md

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 10: 删除Python源代码

**Files:**
- Delete: `src/` 整个目录

**Step 1: 删除src目录**

```bash
rm -rf src/
```

**Step 2: 验证删除**

```bash
ls -la src/ 2>&1
# 预期输出: No such file or directory
```

**Step 3: 提交**

```bash
git add -A
git commit -m "refactor: remove Python source code

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 11: 删除测试文件

**Files:**
- Delete: `tests/` 整个目录

**Step 1: 删除tests目录**

```bash
rm -rf tests/
```

**Step 2: 验证删除**

```bash
ls -la tests/ 2>&1
# 预期输出: No such file or directory
```

**Step 3: 提交**

```bash
git add -A
git commit -m "refactor: remove test files

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 12: 删除文档目录

**Files:**
- Delete: `docs/plans/` 整个目录（保留当前实现计划）

**Step 1: 删除旧的docs目录**

```bash
# 保留当前实现计划，删除其他旧文档
find docs/plans/ -name "*.md" ! -name "2026-03-22-skill-refactoring-implementation.md" -delete
# 如果目录为空则删除
rmdir docs/plans/ 2>/dev/null || true
rmdir docs/ 2>/dev/null || true
```

**Step 2: 验证**

```bash
ls -la docs/ 2>&1
# 预期输出: 目录为空或不存在
```

**Step 3: 提交**

```bash
git add -A
git commit -m "refactor: remove old documentation

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 13: 删除配置文件

**Files:**
- Delete: `pyproject.toml`
- Delete: `README.md`
- Delete: `.pytest_cache/`

**Step 1: 删除配置文件**

```bash
rm -f pyproject.toml README.md
rm -rf .pytest_cache/
```

**Step 2: 验证删除**

```bash
ls pyproject.toml README.md 2>&1
# 预期输出: No such file or directory
```

**Step 3: 提交**

```bash
git add -A
git commit -m "refactor: remove config files and README

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 14: 最终验证和清理

**Files:**
- Verify: 项目根目录结构

**Step 1: 验证最终目录结构**

```bash
ls -la
# 预期输出: 只包含 SKILL.md, rules/, templates/, docs/(可选), .git/, .claude/
```

**Step 2: 验证templates结构**

```bash
find templates/ -name "README.md" | wc -l
# 预期输出: 5 (每个模板都有README)
```

**Step 3: 验证SKILL.md内容**

```bash
grep -E "(CLI|Python|pip install|article-to-card)" SKILL.md
# 预期输出: 无匹配（已删除所有相关内容）
```

**Step 4: 检查git状态**

```bash
git status
# 预期输出: clean 或只有未追踪的文件
```

**Step 5: 最终提交**

```bash
# 如果有任何剩余更改
git add -A
git commit -m "refactor: complete skill refactoring - final cleanup

- Removed all Python/CLI functionality
- Added README.md to each template
- Updated SKILL.md with template learning guide
- Project is now documentation-only

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## 执行顺序

按以下顺序执行任务：
1. Task 1: 迁移templates
2. Task 2-6: 创建各模板README (可并行)
3. Task 7-9: 更新SKILL.md (顺序执行)
4. Task 10-13: 删除文件 (可并行)
5. Task 14: 最终验证

## 验收标准

完成后项目应满足：
- [ ] 根目录只包含: SKILL.md, rules/, templates/
- [ ] 每个templates子目录都有README.md
- [ ] SKILL.md无CLI/Python相关内容
- [ ] templates/包含5个完整模板
- [ ] 所有更改已提交到git
