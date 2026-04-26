# Raw - 原始资料库

这里存放所有原始输入资料，LLM 会自动从这里提取知识并编译到 `wiki/`。

## 支持的格式

- Markdown (`.md`)
- 纯文本 (`.txt`)
- PDF (需转换)
- 网页剪藏 (`.html`)

## 命名规范

```
raw/
├── 2026-04-26_项目笔记.md      # 日期_主题.md
├── 2026-04-25_会议记录.md
├── articles/                    # 文章剪藏
│   └── LLM_Wiki_理念.md
└── chats/                       # 对话记录
    └── 2026-04-26_大哥对话.md
```

## 使用方式

1. 把任何原始资料丢进这里
2. 运行 `python scripts/compile_wiki.py` 自动整理
3. 知识会自动出现在 `wiki/` 目录

## 元数据头

建议在文件顶部添加：

```markdown
---
source: manual
tags: [标签 1, 标签 2]
created: 2026-04-26
---
```
