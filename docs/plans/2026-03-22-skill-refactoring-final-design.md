# Article to Media Image Skill 重构设计

**日期**: 2026-03-22
**目标**: 移除Python相关功能和CLI功能，将项目重构为纯文档化的OpenClaw Skill

## 背景

当前项目包含Python渲染引擎、CLI工具和模板系统。为了简化维护并让AI直接生成HTML，需要重构为纯文档化结构。

## 设计原则

1. **最小化结构** - 只保留必要的文档和示例
2. **AI直接生成** - AI阅读规则和示例后直接生成HTML
3. **示例增强** - 每个模板附带README说明设计意图
4. **单一入口** - SKILL.md作为唯一入口文件

## 目标结构

```
article-to-media-image/
├── SKILL.md              # 技能入口文件
├── rules/                # 技术规范
│   ├── 01-技术底线.md
│   ├── 02-截图流程.md
│   └── 03-风格灵感.md
└── templates/            # 模板示例（带README说明）
    ├── minimal/
    │   ├── README.md     # 模板设计说明
    │   ├── template.html
    │   └── style.css
    ├── gradient/
    │   ├── README.md
    │   ├── template.html
    │   └── style.css
    ├── card/
    │   ├── README.md
    │   ├── template.html
    │   └── style.css
    ├── dark/
    │   ├── README.md
    │   ├── template.html
    │   └── style.css
    └── tech_modern/
        ├── README.md
        ├── template.html
        └── style.css
```

## 删除内容

### Python源代码
- `src/__init__.py`
- `src/cli.py`
- `src/config/` 整个目录
- `src/renderer/` 整个目录（保留templates移到根目录）
- `src/utils/` 整个目录

### 测试文件
- `tests/` 整个目录

### 文档
- `docs/plans/` 整个目录
- `README.md`（功能合并到SKILL.md）

### 配置文件
- `pyproject.toml`
- `.pytest_cache/`

## SKILL.md 更新

### 移除内容
- CLI使用方式（第31-42行）
- Python库使用方式（第44-58行）
- 安装说明（第107-119行）

### 保留内容
- 设计理念
- 工作流程（简化为AI直接生成HTML）
- Segment类型说明
- 技术约束引用

### 新增内容
- **模板学习指南**：如何使用templates作为参考
- **设计流程说明**：AI如何分析内容并选择风格
- **目录结构更新**：反映新的文件组织

## Template README.md 结构

每个模板的README.md包含以下内容：

```markdown
# [风格名称] 模板

## 设计特征
- [核心视觉特征列表]

## 适用场景
[推荐使用的内容类型]

## 关键设计点
- **配色**: [主色、辅色说明]
- **字体**: [字体选择及理由]
- **布局**: [布局特点]
- **装饰**: [装饰元素使用]

## 技术要点
- [需要特别注意的技术实现细节]

## 参考代码
- [模板中的关键代码片段说明]
```

### 示例：minimal/README.md

```markdown
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
```

## 迁移步骤

### 步骤1：备份templates
```bash
# 将templates从src/renderer/移到根目录
mv src/renderer/templates templates
```

### 步骤2：删除不需要的文件
```bash
# 删除Python源代码
rm -rf src/
# 删除测试
rm -rf tests/
# 删除文档
rm -rf docs/
# 删除配置
rm -f pyproject.toml README.md
# 清理缓存
rm -rf .pytest_cache/
```

### 步骤3：创建模板README
为每个templates/*/创建README.md，包含：
- minimal/README.md
- gradient/README.md
- card/README.md
- dark/README.md
- tech_modern/README.md

### 步骤4：更新SKILL.md
- 移除Python/CLI相关内容
- 更新工作流程描述
- 添加模板学习指南
- 更新目录结构说明

### 步骤5：验证
- 确保SKILL.md能正确引用rules和templates
- 确认所有引用路径正确
- 检查无残留Python依赖描述

## 使用流程

重构后，AI使用此skill的流程：

1. **阅读SKILL.md** - 了解设计理念和工作流程
2. **分析用户内容** - 判断内容类型和调性
3. **参考rules/03-风格灵感.md** - 选择合适的风格
4. **阅读templates/[风格]/README.md** - 了解该风格的设计要点
5. **参考templates/[风格]/template.html** - 学习代码结构
6. **生成HTML** - 遵守rules/01-技术底线.md直接生成HTML
7. **截图交付** - 按rules/02-截图流程.md执行

## 风险与考虑

1. **AI理解偏差** - AI可能误解规则，导致生成的HTML不符合要求
   - 缓解：rules/01-技术底线.md已包含明确约束

2. **模板维护** - 5个模板需要同步更新
   - 缓解：README文档化降低维护成本

3. **缺少验证** - 无自动化测试验证生成的HTML
   - 缓解：AI在截图前可以预览检查

## 后续优化

1. 考虑添加HTML验证checklist到SKILL.md
2. 考虑为每个模板添加视觉示例图片
3. 考虑添加更多segment类型示例
