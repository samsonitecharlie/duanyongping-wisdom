#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段永平知识库一键同步工具
自动将Markdown源文件转换为HTML并同步到网站目录
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# ===== 路径配置 =====
KB_SOURCE = Path(r"C:\Users\Charlie\Desktop\段永平知识库")  # Markdown源文件
KB_OUTPUT = Path(r"C:\Users\Charlie\Desktop\段永平智慧库")  # HTML网站

# 内容类型映射
FOLDER_MAP = {
    'sayings': '投资箴言',
    'weibo': '微博语录', 
    'qa': '投资问答',
    'interview': '访谈记录',
    'speech': '演讲分享',
    'blog': '博客文章',
    'concepts': '概念',
    'people': '人物',
    'companies': '公司',
    'misc': '其他'
}

# 侧边栏导航模板
SIDEBAR_TEMPLATE = '''
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
'''

def detect_type_from_filename(filename):
    """根据文件名判断类型"""
    name = filename.lower()
    if '箴言' in name or '投资语录' in name:
        return 'sayings'
    elif '微博' in name:
        return 'weibo'
    elif '问答' in name or '雪球' in name or '回答' in name:
        return 'qa'
    elif '访谈' in name or '采访' in name:
        return 'interview'
    elif '演讲' in name or '分享' in name:
        return 'speech'
    elif '博客' in name:
        return 'blog'
    elif any(k in name for k in ['苹果', '茅台', '网易', '腾讯', '阿里', '拼多多']):
        return 'companies'
    elif any(k in name for k in ['本分', '护城河', '能力圈', '平常心', '长期主义', '安全边际', 'stop']):
        return 'concepts'
    else:
        return 'misc'

def extract_year(filename):
    """提取年份"""
    match = re.search(r'(20\d{2})', filename)
    return match.group(1) if match else None

def md_to_html(md_content, title, content_type, year=None):
    """Markdown转HTML"""
    
    # 简单的Markdown转换
    html = md_content
    
    # 标题
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 段落处理
    lines = html.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<'):
            if not stripped.startswith('-') and not stripped.startswith('*'):
                new_lines.append(f'<p>{stripped}</p>')
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    html = '\n'.join(new_lines)
    
    # 列表
    html = re.sub(r'^[-*] (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>', html)
    
    # 引用
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # 类型名称
    type_name = FOLDER_MAP.get(content_type, '其他')
    
    # 生成完整HTML
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<button class="hamburger" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>
{SIDEBAR_TEMPLATE}
<main class="main">
<div class="meta">
<span class="type-badge type-{type_name}">{type_name}</span>
{f'<span class="date-tag">{year}</span>' if year else ''}
</div>
<article class="article">
{html}
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
    
    return full_html

def process_md_file(md_path, force=False):
    """处理单个Markdown文件"""
    md_path = Path(md_path)
    
    # 检测类型
    content_type = detect_type_from_filename(md_path.name)
    year = extract_year(md_path.name)
    
    # 目标路径
    output_dir = KB_OUTPUT / content_type
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{md_path.stem}.html"
    
    # 检查是否需要更新
    if output_path.exists() and not force:
        md_mtime = md_path.stat().st_mtime
        html_mtime = output_path.stat().st_mtime
        if html_mtime > md_mtime:
            return None  # 已是最新
    
    # 读取并转换
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html = md_to_html(md_content, md_path.stem, content_type, year)
    
    # 写入HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path

def sync_all():
    """同步所有Markdown文件"""
    print("="*50)
    print("   段永平知识库同步工具")
    print("="*50)
    
    # 扫描源目录
    md_files = list(KB_SOURCE.glob("*.md"))
    
    if not md_files:
        print("\n未找到Markdown文件")
        return
    
    print(f"\n找到 {len(md_files)} 个源文件")
    
    updated = 0
    skipped = 0
    
    for md_path in md_files:
        result = process_md_file(md_path)
        if result:
            print(f"  [OK] {md_path.name} -> {result.parent.name}/")
            updated += 1
        else:
            skipped += 1
    
    print(f"\n{'='*50}")
    print(f"同步完成: 更新 {updated} 个, 跳过 {skipped} 个")
    print(f"{'='*50}")
    
    # 更新时间戳
    with open(KB_OUTPUT / ".last_sync", 'w') as f:
        f.write(datetime.now().isoformat())

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # 处理指定文件
        for path in sys.argv[1:]:
            if Path(path).exists():
                process_md_file(path, force=True)
                print(f"已处理: {path}")
    else:
        # 同步所有
        sync_all()
    
    input("\n按回车键退出...")
