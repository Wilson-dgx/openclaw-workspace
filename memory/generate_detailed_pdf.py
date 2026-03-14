#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate detailed logic quiz report PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register fonts
try:
    pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Helvetica.ttc'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', '/System/Library/Fonts/Helvetica.ttc'))
    main_font = 'Arial'
except:
    main_font = 'Helvetica'

def create_pdf():
    doc = SimpleDocTemplate(
        "memory/逻辑题测试报告_详细版.pdf",
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=1,
        textColor=colors.HexColor('#1a5490')
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#2E5090')
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.HexColor('#4A7C59')
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=9,
        spaceAfter=6,
        leading=13
    )
    
    score_style = ParagraphStyle(
        'Score',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4
    )
    
    story = []
    
    # Title
    story.append(Paragraph("High Difficulty Logic Quiz Test Report", title_style))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>Test Date:</b> February 25, 2026", body_style))
    story.append(Paragraph("<b>Test Subject:</b> Butler AI Agent", body_style))
    story.append(Paragraph("<b>Evaluator:</b> Zheng Weisi (AI Assistant)", body_style))
    story.append(Paragraph("<b>Language:</b> Chinese", body_style))
    story.append(Spacer(1, 0.4*cm))
    
    # Overall Score
    story.append(Paragraph("Overall Scoring", heading_style))
    
    score_data = [
        ['Dimension', 'Score', 'Weight', 'Weighted'],
        ['Accuracy', '93/100', '40%', '37.2'],
        ['Reasoning Depth', '92/100', '30%', '27.6'],
        ['Clarity', '94/100', '20%', '18.8'],
        ['Innovation', '85/100', '10%', '8.5'],
        ['<b>Total</b>', '', '', '<b>92.1/100</b>']
    ]
    
    score_table = Table(score_data, colWidths=[4*cm, 2.5*cm, 2*cm, 2.5*cm])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F5F5F5')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F5E9')),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Grade: A (Excellent)</b>", score_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Summary table
    story.append(Paragraph("Score Summary by Question", heading_style))
    
    summary_data = [
        ['Question', 'Score', 'Grade'],
        ['1. Prisoner\'s Dilemma', '92', 'Excellent'],
        ['2. Pirate Coin Division', '95', 'Outstanding'],
        ['3. Monty Hall Problem', '95', 'Outstanding'],
        ['4. Liar Paradox', '90', 'Excellent'],
        ['5. Blue-Eyed Islanders', '96', 'Outstanding'],
        ['6. Einstein Logic Puzzle', '95', 'Outstanding'],
        ['7. Hilbert Hotel', '95', 'Outstanding'],
        ['8. Unexpected Hanging', '92', 'Excellent'],
        ['9. Newcomb Paradox', '94', 'Outstanding'],
        ['10. Barber Paradox', '94', 'Outstanding'],
        ['<b>Average</b>', '<b>92.1</b>', '<b>Excellent</b>']
    ]
    
    summary_table = Table(summary_data, colWidths=[7*cm, 3*cm, 3*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F5F5F5')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F5E9')),
    ]))
    story.append(summary_table)
    story.append(PageBreak())
    
    # Question details (abbreviated for PDF)
    questions_summary = [
        ("Q1: Prisoner's Dilemma", "95", "95", "95", "80", "92",
         "All three prisoners confess, 5 years each. Correct dominant strategy and Nash equilibrium analysis."),
        ("Q2: Pirate Coin Division", "98", "95", "95", "85", "95",
         "Captain keeps 98, gives 1 to 3rd and 5th pirates. Perfect backward induction."),
        ("Q3: Monty Hall Problem", "100", "95", "95", "85", "95",
         "Switch doors: 2/3 win probability. Verified with three methods."),
        ("Q4: Liar Paradox", "90", "95", "90", "85", "90",
         "Paradoxical in classical logic. Four solutions provided."),
        ("Q5: Blue-Eyed Islanders", "98", "98", "95", "90", "96",
         "100 blue-eyed islanders commit suicide on day 100. Excellent induction proof."),
        ("Q6: Einstein Logic", "100", "95", "95", "85", "95",
         "German keeps fish, Norwegian drinks water. Complete step-by-step deduction."),
        ("Q7: Hilbert Hotel", "100", "95", "95", "85", "95",
         "All three scenarios solved correctly. Clear mathematical principles."),
        ("Q8: Unexpected Hanging", "92", "92", "95", "88", "92",
         "Thursday execution IS unexpected. Correct time-displacement analysis."),
        ("Q9: Newcomb Paradox", "95", "95", "95", "90", "94",
         "EDT vs CDT comparison accurate. Recommendation: Take only Box B."),
        ("Q10: Barber Paradox", "96", "96", "95", "88", "94",
         "Such barber cannot exist. ZFC, type theory, NBG solutions explained."),
    ]
    
    story.append(Paragraph("Detailed Evaluation by Question", heading_style))
    story.append(Spacer(1, 0.2*cm))
    
    for q_num, (title, acc, depth, clarity, innov, total, summary) in enumerate(questions_summary, 1):
        story.append(Paragraph(f"{title}", subheading_style))
        
        eval_data = [
            ['Accuracy', 'Depth', 'Clarity', 'Innovation', 'Total'],
            [acc, depth, clarity, innov, f'<b>{total}</b>']
        ]
        
        eval_table = Table(eval_data, colWidths=[2.5*cm]*5)
        eval_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A7C59')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ]))
        story.append(eval_table)
        story.append(Paragraph(f"Summary: {summary}", body_style))
        story.append(Spacer(1, 0.3*cm))
        
        if q_num % 3 == 0 and q_num < 10:
            story.append(PageBreak())
    
    # Final conclusion
    story.append(PageBreak())
    story.append(Paragraph("Conclusion", heading_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("<b>Overall Assessment</b>", subheading_style))
    story.append(Paragraph(
        "The Butler AI Agent performed excellently in this high-difficulty logic quiz test, achieving a total score of 92.1/100.",
        body_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>Strengths:</b>", body_style))
    story.append(Paragraph("- Excellent logical reasoning ability, all answers fundamentally correct", body_style))
    story.append(Paragraph("- Skilled in using induction, backward reasoning, and other methods", body_style))
    story.append(Paragraph("- Clear expression with effective use of tables and hierarchical structure", body_style))
    story.append(Paragraph("- Deep understanding of philosophical and mathematical backgrounds", body_style))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>Areas for Improvement:</b>", body_style))
    story.append(Paragraph("- Some questions could introduce more diverse analytical perspectives", body_style))
    story.append(Paragraph("- Certain derivations could be more rigorous", body_style))
    story.append(Paragraph("- Could attempt to propose more original insights", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "<b>Final Grade: A (Excellent)</b>",
        ParagraphStyle('Final', parent=body_style, fontSize=12, textColor=colors.HexColor('#2E5090'))
    ))
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("<i>Report Generated: February 25, 2026 | Generated by: Zheng Weisi</i>", 
                          ParagraphStyle('Footer', parent=body_style, fontSize=7, textColor=colors.grey)))
    
    doc.build(story)
    print("Detailed PDF report generated: memory/逻辑题测试报告_详细版.pdf")

if __name__ == "__main__":
    create_pdf()
