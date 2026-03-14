#!/usr/bin/env python3
"""
将 Markdown 报告转换为简单的文本 PDF
"""
from fpdf import FPDF
import re

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_left_margin(15)
        self.set_right_margin(15)
        # 添加中文字体支持
        self.add_font('SimHei', '', '/System/Library/Fonts/STHeiti Medium.ttc')
        
    def header(self):
        pass
    
    def footer(self):
        self.set_y(-15)
        self.set_font('SimHei', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('SimHei', '', 12)
    
    # 读取 Markdown 文件
    with open('/Users/ciss-ai/.openclaw/agents/zongzhu/已安装技能详细报告.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理每一行
    lines = content.split('\n')
    for line in lines:
        # 处理标题
        if line.startswith('# '):
            pdf.set_font('SimHei', '', 18)
            pdf.multi_cell(0, 10, line[2:])
            pdf.ln(3)
        elif line.startswith('## '):
            pdf.set_font('SimHei', '', 16)
            pdf.multi_cell(0, 8, line[3:])
            pdf.ln(2)
        elif line.startswith('### '):
            pdf.set_font('SimHei', '', 14)
            pdf.multi_cell(0, 7, line[4:])
            pdf.ln(2)
        elif line.startswith('```'):
            pdf.set_font('SimHei', '', 10)
            # 不处理代码块的标记行
            pass
        elif line.strip():
            pdf.set_font('SimHei', '', 11)
            # 清理 Markdown 标记
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            clean_line = re.sub(r'\*(.*?)\*', r'\1', clean_line)
            clean_line = re.sub(r'`(.*?)`', r'\1', clean_line)
            clean_line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line)
            pdf.multi_cell(0, 6, clean_line)
        else:
            pdf.ln(3)
    
    # 保存 PDF
    pdf.output('/Users/ciss-ai/Desktop/已安装技能详细报告.pdf')
    print("PDF 创建成功！")

if __name__ == '__main__':
    create_pdf()
