# MindVault - LLM Wiki 知识库

大哥的个人知识库，基于 Karpathy LLM Wiki 模式。

## 目录结构

### 🧠 LLM Wiki（新增）

| 目录 | 说明 |
|------|------|
| `raw/` | 原始资料库 - 丢进来就行 |
| `wiki/` | 结构化知识 - 自动生成 |
| `schema/` | 知识图谱元数据 |
| `journal/` | 编译日志 |
| `scripts/` | 工具脚本 |

### 📚 原有结构

| 目录 | 说明 |
|------|------|
| `docs/` | MkDocs 文档 |
| `notes/` | 日常笔记 |
| `projects/` | 项目记录 |
| `resources/` | 资源链接 |

## 快速使用

### 添加资料

```bash
# 手动添加
cp 笔记.md raw/2026-04-26_笔记.md
```

或者对我说：
> "小 C，把这个保存到知识库"

### 编译知识库

```bash
cd knowledge-base
python scripts/compile_wiki.py
```

### 检索知识

```bash
# 搜索关键词
python scripts/search_kb.py "LLM Wiki"

# 查询概念
python scripts/search_kb.py -c "RAG"

# 列出所有概念
python scripts/search_kb.py -l
```

### 消息命令

| 命令 | 说明 |
|------|------|
| `kb 搜索 xxx` | 搜索关键词 |
| `kb 概念 xxx` | 查询概念 |
| `kb 列表` | 列出所有概念 |
| `kb 编译` | 重新编译 |

## 文档

- 📖 [LLM Wiki 使用指南](LLM_WIKI_USAGE.md)
- 📖 [Raw 目录说明](raw/README.md)
- 📖 [Wiki 目录说明](wiki/README.md)

---
_由小 C 维护 | 基于 Karpathy LLM Wiki 模式_
