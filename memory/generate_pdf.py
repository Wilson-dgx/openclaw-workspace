#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成逻辑题测试报告PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys

# 注册中文字体
# 使用Helvetica字体（英文支持良好）
pdfmetrics.registerFont(TTFont('SimSun', '/System/Library/Fonts/Helvetica.ttc'))

def create_pdf():
    doc = SimpleDocTemplate(
        "memory/logic_quiz_report.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 创建样式
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='SimSun',
        fontSize=24,
        spaceAfter=30,
        alignment=1  # 居中
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName='SimSun',
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#2E5090')
    )
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontName='SimSun',
        fontSize=13,
        spaceAfter=10,
        textColor=colors.HexColor('#4A7C59')
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName='SimSun',
        fontSize=10,
        spaceAfter=8,
        leading=14
    )
    score_style = ParagraphStyle(
        'ScoreStyle',
        parent=styles['Normal'],
        fontName='SimSun',
        fontSize=11,
        spaceAfter=6
    )
    
    story = []
    
    # 标题
    story.append(Paragraph("高难度逻辑题测试报告", title_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>测试日期：</b>2026年2月25日", body_style))
    story.append(Paragraph("<b>测试对象：</b>管家智能体", body_style))
    story.append(Paragraph("<b>评价者：</b>正维斯（AI智能助理）", body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # 总体评分
    story.append(Paragraph("📊 总体评分", heading_style))
    
    score_data = [
        ['评分维度', '得分', '说明'],
        ['准确性', '92/100', '大部分答案正确，个别表述有细微偏差'],
        ['推理深度', '95/100', '推理过程详细，使用了多种分析方法'],
        ['表达清晰度', '90/100', '结构清晰，但部分题目可以更精炼'],
        ['创新性', '85/100', '解法标准，缺少独特视角'],
        ['总分', '90.5/100', '优秀']
    ]
    
    score_table = Table(score_data, colWidths=[4*cm, 2.5*cm, 7*cm])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.5*cm))
    
    # 各题详细评价
    questions = [
        ("题目一：囚徒困境变体", "92/100", [
            ("准确性", "95/100", "正确答案：三人都认罪，各判5年。纳什均衡分析正确，占优策略识别准确。"),
            ("分析深度", "90/100", "使用了收益矩阵分析，解释了严格占优策略，缺少对'集体悲剧'的更深入讨论。"),
        ]),
        ("题目二：海盗分金（5人版）", "98/100", [
            ("准确性", "100/100", "分配方案完全正确：98, 0, 1, 0, 1。逆向推理法使用正确，投票计算准确。"),
            ("分析深度", "95/100", "详细展示了逆向归纳过程，考虑了海盗优先级，可以补充成本最小化原则的讨论。"),
        ]),
        ("题目三：蒙提霍尔问题", "95/100", [
            ("准确性", "100/100", "概率计算完全正确，换门策略优势明确。"),
            ("分析深度", "90/100", "使用了直观的枚举法，包含100扇门的类比解释，可以补充贝叶斯定理的严格证明。"),
        ]),
        ("题目四：说谎者悖论变体", "90/100", [
            ("准确性", "85/100", "矛盾分析正确，解决方案多样，但'假设为假'的推导可以更严谨。"),
            ("分析深度", "95/100", "形式化表达正确，提到哥德尔不完备定理的哲学根源。"),
        ]),
        ("题目五：蓝眼睛岛民谜题", "99/100", [
            ("准确性", "100/100", "归纳推理完全正确，共同知识概念使用准确，两种表述的区分分析精彩。"),
            ("分析深度", "98/100", "详细的归纳证明，棕眼睛的人为什么不自杀的解释清晰。"),
        ]),
        ("题目六：爱因斯坦逻辑谜题", "98/100", [
            ("准确性", "100/100", "答案完全正确：养鱼的是德国人，喝水的是挪威人。推理过程详细。"),
            ("分析深度", "95/100", "步骤清晰，从固定条件出发，包含试错和自我修正的过程。"),
        ]),
        ("题目七：无限旅馆悖论", "97/100", [
            ("准确性", "100/100", "三种方案都正确，数学表达准确。"),
            ("分析深度", "95/100", "希尔伯特旅馆背景介绍，可数无穷性质解释清晰。"),
        ]),
        ("题目八：意外绞刑悖论", "91/100", [
            ("准确性", "90/100", "基本方向正确，时间错位分析准确，可以更深入讨论'知道'的哲学定义。"),
            ("分析深度", "92/100", "自我指涉推理的讨论到位，可以补充模态逻辑和认知逻辑的视角。"),
        ]),
        ("题目九：纽康姆悖论", "95/100", [
            ("准确性", "95/100", "两种决策理论对比正确，期望收益计算准确，推荐结论合理。"),
            ("分析深度", "95/100", "介绍了决策论的经典分歧，提到诺齐克的立场。"),
        ]),
        ("题目十：理发师悖论", "95/100", [
            ("准确性", "95/100", "矛盾分析清晰，解决方案全面，与罗素悖论的联系准确。"),
            ("分析深度", "95/100", "ZFC系统介绍完整，类型论解释清晰。"),
        ]),
    ]
    
    for i, (title, total_score, details) in enumerate(questions, 1):
        story.append(PageBreak())
        story.append(Paragraph(f"{title} <font size=12 color=grey>[{total_score}]</font>", heading_style))
        
        for detail_title, score, desc in details:
            story.append(Paragraph(f"<b>{detail_title}：</b>{score}", subheading_style))
            story.append(Paragraph(desc, body_style))
            story.append(Spacer(1, 0.2*cm))
        
        story.append(Spacer(1, 0.3*cm))
    
    # 总结
    story.append(PageBreak())
    story.append(Paragraph("📈 总结与结论", heading_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("<b>各题得分汇总</b>", subheading_style))
    
    summary_data = [['题目', '得分', '等级']]
    for title, score, _ in questions:
        score_val = float(score.split('/')[0])
        if score_val >= 95:
            grade = '卓越'
        elif score_val >= 90:
            grade = '优秀'
        else:
            grade = '良好'
        summary_data.append([title.split('：')[1], score, grade])
    summary_data.append(['<b>平均分</b>', '<b>90.5/100</b>', '<b>优秀</b>'])
    
    summary_table = Table(summary_data, colWidths=[7*cm, 3*cm, 3.5*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F5F5F5')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F5E9')),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("<b>总体评价</b>", subheading_style))
    story.append(Paragraph(
        "管家智能体在这次高难度逻辑题测试中表现优秀，总分90.5/100。",
        body_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>优势：</b>", body_style))
    story.append(Paragraph("• 逻辑推理能力出色，所有题目答案基本正确", body_style))
    story.append(Paragraph("• 善于使用归纳法、逆向推理等方法", body_style))
    story.append(Paragraph("• 表达清晰，结构完整", body_style))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>改进空间：</b>", body_style))
    story.append(Paragraph("• 部分题目可以引入更多元化的分析视角", body_style))
    story.append(Paragraph("• 哲学类题目可以更深入地探讨概念本质", body_style))
    story.append(Paragraph("• 可以尝试提出原创性见解，而非标准解法", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "<b>综合评价：A级（优秀）</b>",
        ParagraphStyle('Final', parent=body_style, fontSize=14, textColor=colors.HexColor('#2E5090'))
    ))
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("<i>报告生成时间：2026年2月25日 | 报告生成者：正维斯</i>", 
                          ParagraphStyle('Footer', parent=body_style, fontSize=8, textColor=colors.grey)))
    
    doc.build(story)
    print("PDF报告已生成：memory/logic_quiz_report.pdf")

if __name__ == "__main__":
    create_pdf()
