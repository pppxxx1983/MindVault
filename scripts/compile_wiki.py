#!/usr/bin/env python3
"""
LLM Wiki Compiler
将 raw/ 目录的原始资料编译成 wiki/ 的结构化知识
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

KB_ROOT = Path(__file__).parent.parent
RAW_DIR = KB_ROOT / "raw"
WIKI_DIR = KB_ROOT / "wiki"
SCHEMA_DIR = KB_ROOT / "schema"
JOURNAL_DIR = KB_ROOT / "journal"

def extract_concepts(content: str) -> list:
    """从内容中提取关键概念"""
    # 简单实现：提取标题、加粗文本、代码块
    concepts = []
    
    # 提取标题
    titles = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
    concepts.extend([t.strip() for t in titles])
    
    # 提取加粗文本
    bolds = re.findall(r'\*\*(.+?)\*\*', content)
    concepts.extend([b.strip() for b in bolds])
    
    return list(set(concepts))

def extract_links(content: str) -> list:
    """提取 Wiki 链接 [[xxx]]"""
    return re.findall(r'\[\[(.+?)\]\]', content)

def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        fm = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip()
        return fm
    return {}

def compile_raw_to_wiki():
    """编译 raw 目录到 wiki"""
    print(f"📚 开始编译知识库...")
    print(f"   源目录：{RAW_DIR}")
    print(f"   目标目录：{WIKI_DIR}")
    
    # 确保目录存在
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    (WIKI_DIR / "concepts").mkdir(exist_ok=True)
    (WIKI_DIR / "journal").mkdir(exist_ok=True)
    
    concepts_index = {}
    all_sources = []
    
    # 遍历 raw 目录
    for raw_file in RAW_DIR.rglob("*.md"):
        if raw_file.name == "README.md":
            continue
            
        print(f"   处理：{raw_file.relative_to(KB_ROOT)}")
        
        with open(raw_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fm = parse_frontmatter(content)
        concepts = extract_concepts(content)
        links = extract_links(content)
        
        # 记录来源
        rel_path = str(raw_file.relative_to(KB_ROOT))
        all_sources.append({
            "file": rel_path,
            "concepts": concepts,
            "tags": fm.get('tags', '').split(','),
            "created": fm.get('created', datetime.now().strftime('%Y-%m-%d'))
        })
        
        # 为每个概念创建/更新 wiki 条目
        for concept in concepts:
            if len(concept) < 2 or len(concept) > 50:
                continue
                
            concept_id = concept.replace(' ', '_').replace('/', '_')
            
            if concept_id not in concepts_index:
                concepts_index[concept_id] = {
                    "name": concept,
                    "sources": [],
                    "aliases": [],
                    "related": set()
                }
            
            concepts_index[concept_id]["sources"].append(rel_path)
            concepts_index[concept_id]["related"].update(links)
    
    # 生成 wiki 条目
    print(f"\n📝 生成 {len(concepts_index)} 个概念条目...")
    
    for concept_id, data in concepts_index.items():
        wiki_file = WIKI_DIR / "concepts" / f"{concept_id}.md"
        
        wiki_content = f"""# {data['name']}

## 概述

从原始资料中自动提取的概念。

## 来源

"""
        for source in data["sources"]:
            wiki_content += f"- [[{source}]]\n"
        
        if data["related"]:
            wiki_content += "\n## 关联\n\n"
            for related in data["related"]:
                wiki_content += f"- [[{related}]]\n"
        
        wiki_content += f"\n## 元数据\n\n- 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        
        with open(wiki_file, 'w', encoding='utf-8') as f:
            f.write(wiki_content)
    
    # 更新 schema
    schema = {
        "version": "1.0.0",
        "last_compiled": datetime.now().isoformat(),
        "concepts": [
            {
                "id": cid,
                "name": data["name"],
                "category": "concept",
                "sources": data["sources"],
                "relations": [{"type": "related", "target": r} for r in data["related"]],
                "updated_at": datetime.now().strftime('%Y-%m-%d')
            }
            for cid, data in concepts_index.items()
        ],
        "sources": all_sources
    }
    
    schema_file = SCHEMA_DIR / "index.json"
    with open(schema_file, 'w', encoding='utf-8') as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
    
    # 记录 journal
    journal_entry = JOURNAL_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(journal_entry, 'a', encoding='utf-8') as f:
        f.write(f"\n## {datetime.now().strftime('%H:%M')} - 知识库编译\n\n")
        f.write(f"- 处理文件：{len(all_sources)}\n")
        f.write(f"- 生成概念：{len(concepts_index)}\n\n")
    
    print(f"\n✅ 编译完成!")
    print(f"   概念条目：{len(concepts_index)}")
    print(f"   Schema: {schema_file}")
    
    return schema

if __name__ == "__main__":
    compile_raw_to_wiki()
