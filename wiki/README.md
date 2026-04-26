# Wiki - 结构化知识库

这里是 LLM 自动整理后的结构化知识，采用维基百科风格。

## 目录结构

```
wiki/
├── concepts/           # 概念定义
│   ├── LLM_Wiki.md
│   └── RAG.md
├── people/             # 人物/角色
│   └── Andrej_Karpathy.md
├── projects/           # 项目知识
│   └── MindVault.md
├── howto/              # 操作指南
│   └── 搭建知识库.md
└── index.md            # 知识图谱索引
```

## 条目格式

```markdown
# 概念名称

> 一句话定义

## 概述

详细说明...

## 关联概念

- [[相关概念 1]]
- [[相关概念 2]]

## 来源

- [[raw/2026-04-26_项目笔记]]
- [[raw/articles/LLM_Wiki_理念]]

## 元数据

- 创建时间：2026-04-26
- 最后更新：2026-04-26
- 置信度：high
```

## 自动维护

- 由 `scripts/compile_wiki.py` 自动更新
- 概念链接使用 `[[Wiki 链接]]` 格式
- 每个条目自动记录来源
