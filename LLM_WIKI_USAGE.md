# LLM Wiki 使用指南

## 目录结构

```
knowledge-base/
├── raw/           # 原始资料（丢进来就行）
├── wiki/          # 结构化知识（自动生成）
├── schema/        # 知识图谱元数据
├── journal/       # 编译日志
├── scripts/       # 工具脚本
└── docs/          # 原有 MkDocs 文档
```

## 快速开始

### 1. 添加原始资料

把任何资料丢进 `raw/` 目录：

```bash
# 手动添加
cp 笔记.md knowledge-base/raw/2026-04-26_笔记.md

# 或者让我帮你添加
"小 C，把刚才的对话记录保存到知识库"
```

### 2. 编译知识库

```bash
cd knowledge-base
python scripts/compile_wiki.py
```

### 3. 检索知识

```bash
# 关键词搜索
python scripts/search_kb.py "LLM Wiki"

# 查询概念
python scripts/search_kb.py -c "RAG"

# 列出所有概念
python scripts/search_kb.py -l

# 查看关联概念
python scripts/search_kb.py -r "LLM_Wiki"
```

## 消息命令

在聊天中可以直接对我说：

| 命令 | 说明 |
|------|------|
| `kb 搜索 xxx` | 搜索关键词 |
| `kb 概念 xxx` | 查询特定概念 |
| `kb 列表` | 列出所有概念 |
| `kb 编译` | 重新编译知识库 |
| `kb 添加 [内容]` | 添加新资料 |

## 资料格式

### 推荐格式

```markdown
---
source: manual
tags: [LLM, 知识库]
created: 2026-04-26
---

# 标题

内容正文...

## 关联
- [[相关概念]]
```

### 自动提取

系统会自动从内容中提取：
- 标题（`# 标题`）
- 加粗重点（`**重点**`）
- Wiki 链接（`[[概念]]`）

## 知识图谱

Schema 文件 `schema/index.json` 包含：
- 所有概念及关系
- 来源追溯
- 更新时间

## 最佳实践

1. **勤添加**：有任何想法/笔记就丢进 `raw/`
2. **定期编译**：每天或每周运行一次编译
3. **用链接**：在笔记中使用 `[[概念]]` 建立关联
4. **查来源**：每个 wiki 条目都记录原始来源

---

_由小 C 维护 | 基于 Karpathy LLM Wiki 模式_
