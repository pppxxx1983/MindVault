#!/usr/bin/env python3
"""
LLM Wiki 检索工具
支持关键词搜索、语义搜索、概念图谱查询
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

def load_schema():
    """加载知识图谱 schema"""
    schema_file = SCHEMA_DIR / "index.json"
    if schema_file.exists():
        with open(schema_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def search_keyword(query: str, limit: int = 10):
    """关键词搜索"""
    results = []
    query_lower = query.lower()
    
    # 搜索 wiki 目录
    for wiki_file in WIKI_DIR.rglob("*.md"):
        if wiki_file.name == "README.md":
            continue
        
        with open(wiki_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 计算匹配度
        matches = 0
        if query_lower in content.lower():
            matches += 1
        
        # 检查标题匹配
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match and query_lower in title_match.group(1).lower():
            matches += 2
        
        if matches > 0:
            results.append({
                "type": "wiki",
                "path": str(wiki_file.relative_to(KB_ROOT)),
                "title": title_match.group(1) if title_match else wiki_file.stem,
                "score": matches,
                "snippet": content[:200] + "..." if len(content) > 200 else content
            })
    
    # 搜索 raw 目录
    for raw_file in RAW_DIR.rglob("*.md"):
        if raw_file.name == "README.md":
            continue
        
        with open(raw_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if query_lower in content.lower():
            results.append({
                "type": "raw",
                "path": str(raw_file.relative_to(KB_ROOT)),
                "title": raw_file.stem,
                "score": 1,
                "snippet": content[:200] + "..." if len(content) > 200 else content
            })
    
    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]

def search_concept(concept_name: str):
    """概念精确查询"""
    schema = load_schema()
    if not schema:
        return {"error": "Schema 不存在，请先运行 compile_wiki.py"}
    
    # 查找匹配的概念
    matches = []
    for concept in schema.get("concepts", []):
        if concept_name.lower() in concept["name"].lower():
            matches.append(concept)
    
    if not matches:
        return {"found": False, "message": f"未找到概念：{concept_name}"}
    
    return {"found": True, "concepts": matches}

def get_related_concepts(concept_id: str):
    """获取关联概念"""
    schema = load_schema()
    if not schema:
        return []
    
    for concept in schema.get("concepts", []):
        if concept["id"] == concept_id:
            return concept.get("relations", [])
    
    return []

def list_all_concepts():
    """列出所有概念"""
    schema = load_schema()
    if not schema:
        return {"error": "Schema 不存在"}
    
    return {
        "total": len(schema.get("concepts", [])),
        "last_compiled": schema.get("last_compiled"),
        "concepts": [
            {"id": c["id"], "name": c["name"], "category": c["category"]}
            for c in schema.get("concepts", [])
        ]
    }

def format_results(results: list, verbose: bool = False) -> str:
    """格式化搜索结果"""
    if not results:
        return "❌ 未找到匹配结果"
    
    output = f"📚 找到 {len(results)} 个结果:\n\n"
    
    for i, r in enumerate(results, 1):
        output += f"{i}. **{r['title']}** [{r['type']}]\n"
        output += f"   路径：`{r['path']}`\n"
        if verbose and r.get("snippet"):
            output += f"   摘要：{r['snippet'][:100]}...\n"
        output += "\n"
    
    return output

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Wiki 检索工具")
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("-c", "--concept", help="查询特定概念")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有概念")
    parser.add_argument("-r", "--related", help="查询关联概念")
    parser.add_argument("-n", "--limit", type=int, default=10, help="结果数量限制")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示摘要")
    
    args = parser.parse_args()
    
    if args.list:
        result = list_all_concepts()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.concept:
        result = search_concept(args.concept)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.related:
        result = get_related_concepts(args.related)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.query:
        results = search_keyword(args.query, args.limit)
        print(format_results(results, args.verbose))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
