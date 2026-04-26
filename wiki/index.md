# 🧠 LLM Wiki 知识库

基于 Andrej Karpathy 提出的 **LLM Wiki** 理念构建的自动知识库。

## 核心理念

> 让 LLM 自动维护知识库，而不是手动整理

## 三层结构

| 层级 | 说明 | 位置 |
|------|------|------|
| **raw/** | 原始资料库 | 丢进来就行 |
| **wiki/** | 结构化知识 | 自动生成 |
| **schema/** | 知识图谱 | 元数据 |

## 快速链接

### 📚 核心概念

- [[LLM Wiki]] - 知识库理念
- [[三层结构]] - raw/wiki/schema
- [[自动提取]] - 概念提取
- [[自动链接]] - 知识关联
- [[知识复利]] - 随时间增长

### 🔧 使用命令

```bash
# 编译知识库
python scripts/compile_wiki.py

# 搜索关键词
python scripts/search_kb.py "RAG"

# 列出所有概念
python scripts/search_kb.py -l
```

## 统计

- 概念数量：15+
- 最后编译：2026-04-26

---

📖 详细文档：[LLM Wiki 使用指南](../LLM_WIKI_USAGE.md)
