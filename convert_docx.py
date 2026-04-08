# 转换docx文件为Markdown并生成HTML
import os
from docx import Document

# 文件路径
desktop = r"C:\Users\Charlie\Desktop"
kb_folder = r"C:\Users\Charlie\Desktop\段永平知识库"
html_folder = r"C:\Users\Charlie\Desktop\段永平智慧库"

# 要处理的文件
files = [
    "2025（一）.docx",
    "2025（二）.docx", 
    "2025（三）.docx"
]

def extract_text_from_docx(docx_path):
    """从docx提取文本"""
    doc = Document(docx_path)
    text = []
    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text)
    return "\n\n".join(text)

def create_markdown(content, title, output_path):
    """创建Markdown文件"""
    md_content = f"""# {title}

{content}
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Created: {output_path}")

# 处理每个文件
for filename in files:
    docx_path = os.path.join(desktop, filename)
    
    if not os.path.exists(docx_path):
        print(f"File not found: {docx_path}")
        continue
    
    # 提取文件名（去掉.docx后缀）
    name = filename.replace(".docx", "")
    
    # 提取文本
    print(f"Processing: {filename}")
    content = extract_text_from_docx(docx_path)
    
    # 保存为Markdown
    md_path = os.path.join(kb_folder, f"段永平投资箴言{name}.md")
    create_markdown(content, f"段永平投资箴言{name}", md_path)

print("\nAll files converted successfully!")
