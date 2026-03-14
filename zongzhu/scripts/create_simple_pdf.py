#!/usr/bin/env python3
"""
创建一个简单的纯文本 PDF 报告
"""
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_left_margin(10)
        self.set_right_margin(10)

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # 尝试添加中文字体（如果失败，使用默认字体）
    try:
        pdf.add_font('Chinese', '', '/System/Library/Fonts/STHeiti Medium.ttc')
        font_name = 'Chinese'
    except:
        font_name = 'Arial'
        print("Warning: Chinese font not available, using Arial")
    
    # 标题
    pdf.set_font(font_name, '', 20)
    pdf.cell(0, 15, 'Agent Skills Report', ln=True, align='C')
    pdf.ln(5)
    
    # 元数据
    pdf.set_font(font_name, '', 12)
    pdf.cell(0, 8, 'Generated: 2026-03-06', ln=True)
    pdf.cell(0, 8, 'Total Skills: 27', ln=True)
    pdf.ln(10)
    
    # Top 5 Skills
    pdf.set_font(font_name, '', 16)
    pdf.cell(0, 10, 'Top 5 Recommended Skills', ln=True)
    pdf.ln(3)
    
    pdf.set_font(font_name, '', 11)
    skills = [
        ("1. ai-meeting-notes", "Extract action items from meeting notes"),
        ("2. task / things-mac", "Task management with Things 3 sync"),
        ("3. calendar", "Calendar and meeting management"),
        ("4. summarize", "Summarize web, PDF, YouTube"),
        ("5. self-improvement", "Continuous improvement tracking")
    ]
    
    for skill, desc in skills:
        pdf.set_font(font_name, '', 12)
        pdf.cell(0, 8, skill, ln=True)
        pdf.set_font(font_name, '', 10)
        pdf.cell(0, 6, f"   {desc}", ln=True)
        pdf.ln(2)
    
    pdf.ln(5)
    
    # Categories
    pdf.set_font(font_name, '', 16)
    pdf.cell(0, 10, 'Skill Categories', ln=True)
    pdf.ln(3)
    
    pdf.set_font(font_name, '', 10)
    categories = [
        ("Notes/Docs", "6 skills", "ai-meeting-notes, apple-notes, flomo, obsidian, document-pro, summarize"),
        ("Tasks", "3 skills", "apple-reminders, task, things-mac"),
        ("Calendar/Email", "5 skills", "calendar, email-to-calendar, gog, himalaya, meeting-prep"),
        ("Security", "1 skill", "1password"),
        ("Automation", "1 skill", "automation-workflows"),
        ("Productivity", "1 skill", "productivity"),
        ("Search", "2 skills", "tavily-search, find-skills"),
        ("Improvement", "1 skill", "self-improvement"),
        ("Development", "1 skill", "skill-creator")
    ]
    
    for cat, count, examples in categories:
        pdf.set_font(font_name, '', 11)
        pdf.cell(0, 7, f"{cat} ({count})", ln=True)
        pdf.set_font(font_name, '', 9)
        pdf.multi_cell(0, 5, f"   {examples}")
        pdf.ln(1)
    
    pdf.add_page()
    
    # Quick Start Commands
    pdf.set_font(font_name, '', 16)
    pdf.cell(0, 10, 'Quick Start Commands', ln=True)
    pdf.ln(3)
    
    pdf.set_font(font_name, '', 10)
    commands = [
        "# 1. Summarize web/PDF",
        'summarize "https://example.com"',
        "",
        "# 2. Add task",
        'things add "Buy milk"',
        "",
        "# 3. Search Gmail",
        "gog gmail search 'newer_than:7d'",
        "",
        "# 4. Process meeting notes",
        "[Paste notes] -> Extract action items",
        "",
        "# 5. View today's tasks",
        "things today",
        "",
        "# 6. View calendar",
        "calendar show this week",
        "",
        "# 7. Save to Flomo",
        '"记录到 flomo：..."',
        "",
        "# 8. Search Obsidian",
        'obsidian-cli search "query"'
    ]
    
    for cmd in commands:
        if cmd.startswith("#"):
            pdf.set_font(font_name, '', 11)
            pdf.ln(2)
        else:
            pdf.set_font(font_name, '', 9)
        pdf.cell(0, 6, cmd, ln=True)
    
    pdf.ln(5)
    
    # macOS Skills
    pdf.set_font(font_name, '', 16)
    pdf.cell(0, 10, 'macOS-Only Skills', ln=True)
    pdf.ln(3)
    
    pdf.set_font(font_name, '', 10)
    macos_skills = [
        ("1password", "op CLI", "Password management"),
        ("apple-notes", "memo CLI", "Notes management"),
        ("apple-reminders", "remindctl CLI", "Reminders"),
        ("obsidian", "obsidian-cli", "Knowledge base"),
        ("things-mac", "things CLI", "Things 3 tasks")
    ]
    
    for skill, tool, desc in macos_skills:
        pdf.set_font(font_name, '', 11)
        pdf.cell(0, 7, f"{skill} ({tool})", ln=True)
        pdf.set_font(font_name, '', 9)
        pdf.cell(0, 5, f"   {desc}", ln=True)
        pdf.ln(1)
    
    # Footer
    pdf.ln(10)
    pdf.set_font(font_name, '', 10)
    pdf.cell(0, 8, "Full report available at: ~/Desktop/已安装技能详细报告.md", ln=True, align='C')
    pdf.cell(0, 8, "HTML version available at: ~/Desktop/已安装技能详细报告.html", ln=True, align='C')
    
    # Save
    output_path = os.path.expanduser('~/Desktop/Skills_Report.pdf')
    pdf.output(output_path)
    print(f"PDF created successfully: {output_path}")

if __name__ == '__main__':
    create_pdf()
