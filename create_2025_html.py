#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速生成2025年箴言HTML"""
import os
from pathlib import Path

KB_SOURCE = Path(r"C:\Users\Charlie\Desktop\段永平知识库")
KB_OUTPUT = Path(r"C:\Users\Charlie\Desktop\段永平智慧库\sayings")

# 只处理这3个新文件
files = [
    "段永平投资箴言2025（一）.md",
    "段永平投资箴言2025（二）.md",
    "段永平投资箴言2025（三）.md"
]

def simple_md_to_html(md_content, title):
    """简单的Markdown转HTML"""
    lines = md_content.strip().split('\n')
    html_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 跳过第一个标题（已经是页面标题）
        if line.startswith('# '):
            continue
        
        # 标题处理
        if line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('**网友') or line.startswith('**网友：'):
            # 加粗的网友提问
            html_lines.append(f'<p><strong>{line}</strong></p>')
        elif line.startswith('段：') or line.startswith('段:'):
            # 段永平回答
            html_lines.append(f'<p><strong>段：</strong>{line[3:]}</p>')
        elif line.startswith('网友：') or line.startswith('网友:'):
            # 普通网友提问
            html_lines.append(f'<p><strong>网友：</strong>{line[4:]}</p>')
        else:
            # 普通段落
            html_lines.append(f'<p>{line}</p>')
    
    return '\n'.join(html_lines)

def create_html(md_file):
    """生成HTML文件"""
    md_path = KB_SOURCE / md_file
    
    if not md_path.exists():
        print(f"文件不存在: {md_file}")
        return
    
    # 读取Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 提取标题
    title = md_file.replace('.md', '')
    
    # 转换HTML
    article_html = simple_md_to_html(md_content, title)
    
    # 完整HTML
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<aside class="sidebar">
<div class="sidebar-header">
<a href="../index.html" class="logo">段永平智慧库</a>
<div class="logo-sub">大道无形我有型</div>
</div>
<div class="sidebar-nav">
<a href="../index.html" class="nav-link">首页</a>
<a href="../sayings/index.html" class="nav-link">投资箴言</a>
<a href="../qa/index.html" class="nav-link">投资问答</a>
<a href="../interview/index.html" class="nav-link">访谈记录</a>
<a href="../blog/index.html" class="nav-link">博客文章</a>
<a href="../weibo/index.html" class="nav-link">微博语录</a>
<a href="../speech/index.html" class="nav-link">演讲分享</a>
</div>
</aside>
<main class="main">
<div class="meta">
<span class="type-badge">投资箴言</span>
<span class="date-tag">2025</span>
</div>
<article class="article">
{article_html}
</article>
</main>
</body>
</html>'''
    
    # 保存HTML
    output_path = KB_OUTPUT / f"{title}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"已生成: {output_path.name}")

# 处理3个文件
print("开始生成HTML...")
for md_file in files:
    create_html(md_file)

print("\n完成！")
