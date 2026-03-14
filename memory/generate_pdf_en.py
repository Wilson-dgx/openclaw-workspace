#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Logic Quiz Report PDF (English)"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_pdf():
    doc = SimpleDocTemplate(
        "memory/logic_quiz_report.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#2E5090')
    )
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=13,
        spaceAfter=10,
        textColor=colors.HexColor('#4A7C59')
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=8,
        leading=14
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Logic Quiz Test Report", title_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Test Date:</b> February 25, 2026", body_style))
    story.append(Paragraph("<b>Test Subject:</b> Butler AI Agent", body_style))
    story.append(Paragraph("<b>Evaluator:</b> Zheng Weisi (AI Assistant)", body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Overall Score
    story.append(Paragraph("Overall Scoring", heading_style))
    
    score_data = [
        ['Dimension', 'Score', 'Notes'],
        ['Accuracy', '92/100', 'Mostly correct, minor deviations in some answers'],
        ['Reasoning Depth', '95/100', 'Detailed reasoning using multiple methods'],
        ['Clarity', '90/100', 'Clear structure, some answers could be more concise'],
        ['Innovation', '85/100', 'Standard solutions, lacking unique perspectives'],
        ['<b>Total</b>', '<b>90.5/100</b>', '<b>Excellent</b>']
    ]
    
    score_table = Table(score_data, colWidths=[4*cm, 2.5*cm, 7*cm])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F5F5F5')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F5E9')),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Questions
    questions = [
        ("Question 1: Prisoner's Dilemma Variant", "92/100", [
            "Three prisoners choose to confess or not. Nash equilibrium: All confess, 5 years each.",
            "Strengths: Correct payoff matrix, dominant strategy identification.",
            "Improvement: Could discuss repeated game cooperation."
        ]),
        ("Question 2: Pirate Coin Division", "98/100", [
            "5 pirates divide 100 coins. Captain's optimal: 98, 0, 1, 0, 1",
            "Strengths: Perfect backward induction, correct vote counting.",
            "Excellent demonstration of game theory principles."
        ]),
        ("Question 3: Monty Hall Problem", "95/100", [
            "Switch doors: 2/3 win probability. Stay: 1/3 probability.",
            "Strengths: Correct probability calculation, intuitive explanation.",
            "Could add Bayesian theorem proof for rigor."
        ]),
        ("Question 4: Liar Paradox", "90/100", [
            '"All my statements are false" - self-referential paradox.',
            "Solutions: Language hierarchy, context restriction, multi-valued logic.",
            "Good connection to Godel's incompleteness theorem."
        ]),
        ("Question 5: Blue-Eyed Islanders", "99/100", [
            "100 blue-eyed islanders commit suicide on day 100.",
            "Strengths: Perfect induction, common knowledge concept.",
            "Excellent distinction between 'at least 1' vs 'at least 2'."
        ]),
        ("Question 6: Einstein's Logic Puzzle", "98/100", [
            "Who keeps fish? German. Who drinks water? Norwegian.",
            "Strengths: Complete step-by-step deduction, correct answer.",
            "Well-organized elimination process."
        ]),
        ("Question 7: Hilbert's Hotel", "97/100", [
            "Infinity + 1 = infinity, infinity + infinity = infinity.",
            "Strengths: All three scenarios solved correctly.",
            "Clear explanation of countable infinity properties."
        ]),
        ("Question 8: Unexpected Hanging", "91/100", [
            "Thursday execution IS unexpected. Prisoner's backward induction fails.",
            "Core insight: Confusing post-hoc certainty with pre-hoc uncertainty.",
            "Could explore modal logic perspectives further."
        ]),
        ("Question 9: Newcomb's Paradox", "95/100", [
            "Two-box vs one-box decision. Recommended: Take only Box B (~99M expected).",
            "Strengths: Correct EDT vs CDT comparison, accurate calculations.",
            "Good coverage of decision theory分歧."
        ]),
        ("Question 10: Barber Paradox", "95/100", [
            "Barber who shaves all who don't shave themselves - contradiction.",
            "Solutions: ZFC axioms, type theory, Tarski's truth theory.",
            "Strong connection to Russell's paradox."
        ]),
    ]
    
    for title, score, details in questions:
        story.append(PageBreak())
        story.append(Paragraph(f"{title} <font size=12 color=grey>[{score}]</font>", heading_style))
        
        for detail in details:
            story.append(Paragraph(detail, body_style))
        
        story.append(Spacer(1, 0.3*cm))
    
    # Summary
    story.append(PageBreak())
    story.append(Paragraph("Summary and Conclusion", heading_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("<b>Score Summary</b>", subheading_style))
    
    summary_data = [['Question', 'Score', 'Grade']]
    for title, score, _ in questions:
        score_val = float(score.split('/')[0])
        if score_val >= 95:
            grade = 'Outstanding'
        elif score_val >= 90:
            grade = 'Excellent'
        else:
            grade = 'Good'
        summary_data.append([title.split(':')[0], score, grade])
    summary_data.append(['<b>Average</b>', '<b>90.5/100</b>', '<b>Excellent</b>'])
    
    summary_table = Table(summary_data, colWidths=[7*cm, 3*cm, 3.5*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F5F5F5')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F5E9')),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("<b>Overall Assessment</b>", subheading_style))
    story.append(Paragraph(
        "The Butler AI Agent performed excellently in this high-difficulty logic quiz test, achieving a total score of 90.5/100.",
        body_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>Strengths:</b>", body_style))
    story.append(Paragraph("- Excellent logical reasoning ability, all answers fundamentally correct", body_style))
    story.append(Paragraph("- Skilled in using induction, backward reasoning, and other methods", body_style))
    story.append(Paragraph("- Clear expression and complete structure", body_style))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>Areas for Improvement:</b>", body_style))
    story.append(Paragraph("- Some questions could introduce more diverse analytical perspectives", body_style))
    story.append(Paragraph("- Philosophical questions could explore conceptual essence more deeply", body_style))
    story.append(Paragraph("- Could attempt to propose original insights rather than standard solutions", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "<b>Final Grade: A (Excellent)</b>",
        ParagraphStyle('Final', parent=body_style, fontSize=14, textColor=colors.HexColor('#2E5090'))
    ))
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("<i>Report Generated: February 25, 2026 | Generated by: Zheng Weisi</i>", 
                          ParagraphStyle('Footer', parent=body_style, fontSize=8, textColor=colors.grey)))
    
    doc.build(story)
    print("PDF report generated: memory/logic_quiz_report.pdf")

if __name__ == "__main__":
    create_pdf()
