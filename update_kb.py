#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段永平知识库更新工具
用法：将新的Markdown文件拖到这个脚本上，或运行后按提示操作
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# ===== 配置 =====
KB_ROOT = Path(r"C:\Users\Charlie\Desktop\段永平智慧库")
SOURCE_ROOT = Path(r"C:\Users\Charlie\Desktop\段永平知识库")

# 内容类型关键词
TYPE_KEYWORDS = {
    'sayings': ['箴言', '投资箴言', '投资语录'],
    'weibo': ['微博', 'weibo'],
    'qa': ['问答', '雪球', '回答'],
    'interview': ['访谈', '采访'],
    'speech': ['演讲', '分享'],
    'blog': ['博客', '博客文章']
}

def detect_content_type(filename):
    """根据文件名判断内容类型"""
    filename_lower = filename.lower()
    for content_type, keywords in TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in filename_lower:
                return content_type
    return 'other'

def extract_year(filename):
    """从文件名提取年份"""
    match = re.search(r'(20\d{2})', filename)
    return match.group(1) if match else None

def clean_markdown(content):
    """清理Markdown内容"""
    # 移除YAML front matter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # 标准化标题
    content = re.sub(r'^#{1,6}\s+', lambda m: '# ' if m.group().count('#') == 1 else m.group(), content, flags=re.MULTILINE)
    return content.strip()

def generate_html(content, title, content_type, year=None):
    """生成HTML页面"""
    
    # 将Markdown转换为简单HTML
    html_content = content
    
    # 标题转换
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    
    # 段落
    html_content = re.sub(r'\n\n', '</p>\n\n<p>', html_content)
    html_content = '<p>' + html_content + '</p>'
    
    # 清理空段落
    html_content = re.sub(r'<p>\s*</p>', '', html_content)
    
    # 引用块
    html_content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html_content, flags=re.MULTILINE)
    
    # 粗体
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # 链接
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_content)
    
    # 类型显示名称
    type_names = {
        'sayings': '投资箴言',
        'weibo': '微博语录',
        'qa': '投资问答',
        'interview': '访谈记录',
        'speech': '演讲分享',
        'blog': '博客文章',
        'other': '其他'
    }
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<button class="hamburger" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>
<aside class="sidebar" id="sidebar">
<div class="sidebar-header"><a href="../index.html" class="logo">段永平智慧库</a><div class="logo-sub">大道无形我有型</div></div>
<div class="sidebar-nav">
<a href="../index.html" class="nav-link nav-home">🏠 首页</a>
<div class="nav-group">
<div class="nav-group-title" onclick="toggle('grp_sayings')"><span class="caret"></span>投资箴言</div>
<div class="nav-group-items" id="grp_sayings"><a href="../sayings/index.html" class="nav-link">投资箴言总览</a></div>
</div>
<div class="nav-group">
<div class="nav-group-title" onclick="toggle('grp_blog')"><span class="caret"></span>博客文章</div>
<div class="nav-group-items" id="grp_blog"><a href="../blog/index.html" class="nav-link">博客文章合集</a></div>
</div>
<div class="nav-group">
<div class="nav-group-title" onclick="toggle('grp_weibo')"><span class="caret"></span>微博语录</div>
<div class="nav-group-items" id="grp_weibo"><a href="../weibo/index.html" class="nav-link">微博语录</a></div>
</div>
<div class="nav-group">
<div class="nav-group-title" onclick="toggle('grp_qa')"><span class="caret"></span>投资问答</div>
<div class="nav-group-items" id="grp_qa"><a href="../qa/index.html" class="nav-link">投资问答总览</a></div>
</div>
<div class="nav-group">
<div class="nav-group-title" onclick="toggle('grp_interview')"><span class="caret"></span>访谈记录</div>
<div class="nav-group-items" id="grp_interview"><a href="../interview/index.html" class="nav-link">访谈记录</a></div>
</div>
<div class="nav-group">
<div class="nav-group-title" onclick="toggle('grp_speech')"><span class="caret"></span>演讲分享</div>
<div class="nav-group-items" id="grp_speech"><a href="../speech/index.html" class="nav-link">演讲分享</a></div>
</div>
</div>
</aside>
<main class="main">
<div class="meta">
<span class="type-badge type-{type_names[content_type]}">{type_names[content_type]}</span>
{f'<span class="date-tag">{year}</span>' if year else ''}
</div>
<article class="article">
{html_content}
</article>
</main>
<script>
function toggle(id) {{
    const el = document.getElementById(id);
    const title = el.previousElementSibling;
    el.classList.toggle('open');
    title.classList.toggle('open');
}}
</script>
</body>
</html>'''
    
    return html_template

def process_new_file(md_path):
    """处理单个新文件"""
    md_path = Path(md_path)
    
    print(f"\n{'='*50}")
    print(f"处理文件: {md_path.name}")
    
    # 读取内容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检测类型和年份
    content_type = detect_content_type(md_path.name)
    year = extract_year(md_path.name)
    
    print(f"  类型: {content_type}" + (f" | 年份: {year}" if year else ""))
    
    # 清理内容
    content = clean_markdown(content)
    
    # 生成标题
    title = md_path.stem
    
    # 生成HTML
    html = generate_html(content, title, content_type, year)
    
    # 确定目标文件夹
    target_dir = KB_ROOT / content_type
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存HTML
    html_path = target_dir / f"{title}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  ✓ 已生成: {html_path}")
    
    # 同时复制源文件到知识库
    source_target = SOURCE_ROOT / content_type
    source_target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(md_path, source_target / md_path.name)
    print(f"  ✓ 已复制源文件到: {source_target / md_path.name}")
    
    return html_path

def process_folder(folder_path):
    """处理文件夹中的所有Markdown文件"""
    folder_path = Path(folder_path)
    md_files = list(folder_path.glob("*.md"))
    
    if not md_files:
        print(f"文件夹中没有找到Markdown文件: {folder_path}")
        return
    
    print(f"\n找到 {len(md_files)} 个Markdown文件")
    
    for md_path in md_files:
        try:
            process_new_file(md_path)
        except Exception as e:
            print(f"  ✗ 处理失败: {e}")
    
    print(f"\n{'='*50}")
    print(f"处理完成！共处理 {len(md_files)} 个文件")

def main():
    print("="*50)
    print("   段永平知识库更新工具 v1.0")
    print("="*50)
    
    print("\n请选择操作：")
    print("1. 处理单个Markdown文件")
    print("2. 处理整个文件夹")
    print("3. 处理下载文件夹中的新内容")
    print("4. 退出")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    if choice == '1':
        path = input("请输入Markdown文件路径: ").strip().strip('"')
        if os.path.exists(path):
            process_new_file(path)
        else:
            print(f"文件不存在: {path}")
    
    elif choice == '2':
        path = input("请输入文件夹路径: ").strip().strip('"')
        if os.path.exists(path):
            process_folder(path)
        else:
            print(f"文件夹不存在: {path}")
    
    elif choice == '3':
        # 默认下载文件夹
        downloads = Path.home() / "Downloads"
        print(f"\n扫描下载文件夹: {downloads}")
        process_folder(downloads)
    
    elif choice == '4':
        print("再见！")
        return
    
    else:
        print("无效选项")
    
    print("\n" + "="*50)
    print("下一步: 将更新后的内容上传到服务器")
    print("服务器路径通常是: /var/www/html/ 或 Docker容器内")
    print("="*50)

if __name__ == '__main__':
    main()
