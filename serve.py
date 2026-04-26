#!/usr/bin/env python3
"""
简单的 Wiki 服务器 - 用于本地浏览知识库
"""

import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # 自动跳转到 wiki/index.md
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', '/wiki/index.html')
            self.end_headers()
            return
        super().do_GET()

print(f"""
📚 MindVault Wiki 服务器

访问地址：http://localhost:{PORT}
知识库目录：{DIRECTORY}

按 Ctrl+C 停止服务器
""")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        sys.exit(0)
