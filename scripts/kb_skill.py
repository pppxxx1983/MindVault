#!/usr/bin/env python3
"""
知识库技能 - 用于消息命令交互
"""

import subprocess
import sys
from pathlib import Path

KB_ROOT = Path(__file__).parent.parent
SEARCH_SCRIPT = KB_ROOT / "scripts" / "search_kb.py"
COMPILE_SCRIPT = KB_ROOT / "scripts" / "compile_wiki.py"

def run_command(cmd: list) -> str:
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"❌ 错误：{e}"

def kb_search(query: str) -> str:
    """搜索知识库"""
    return run_command([sys.executable, str(SEARCH_SCRIPT), query, "-v"])

def kb_concept(name: str) -> str:
    """查询概念"""
    return run_command([sys.executable, str(SEARCH_SCRIPT), "-c", name])

def kb_list() -> str:
    """列出所有概念"""
    return run_command([sys.executable, str(SEARCH_SCRIPT), "-l"])

def kb_compile() -> str:
    """编译知识库"""
    return run_command([sys.executable, str(COMPILE_SCRIPT)])

def main():
    if len(sys.argv) < 2:
        print("用法：kb_skill.py <command> [args]")
        print("命令：search, concept, list, compile")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "search" and len(sys.argv) > 2:
        print(kb_search(" ".join(sys.argv[2:])))
    elif cmd == "concept" and len(sys.argv) > 2:
        print(kb_concept(sys.argv[2]))
    elif cmd == "list":
        print(kb_list())
    elif cmd == "compile":
        print(kb_compile())
    else:
        print(f"❌ 未知命令：{cmd}")

if __name__ == "__main__":
    main()
