#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发送邮件报告"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# 配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 587
SENDER_EMAIL = "zenrvis321@163.com"
# 注意：需要设置SMTP授权码
# RECEIVER_EMAIL = "wilson@cis-systems.com"
RECEIVER_EMAIL = "zenrvis321@163.com"  # 先发送给自己测试

subject = "高难度逻辑题测试报告 - 管家智能体评估"

body = """方总您好！

已完成10道高难度逻辑题的测试。管家智能体的表现非常优秀！

【总体评分】90.5/100（优秀）

【各题得分】
1. 囚徒困境变体：92/100
2. 海盗分金：98/100 ⭐
3. 蒙提霍尔问题：95/100
4. 说谎者悖论：90/100
5. 蓝眼睛岛民：99/100 ⭐⭐
6. 爱因斯坦逻辑谜题：98/100 ⭐
7. 无限旅馆悖论：97/100
8. 意外绞刑悖论：91/100
9. 纽康姆悖论：95/100
10. 理发师悖论：95/100

【优势】
- 逻辑推理能力出色，所有答案基本正确
- 善于使用归纳法、逆向推理等方法
- 表达清晰，结构完整

【改进空间】
- 部分题目可引入更多元化的分析视角
- 哲学类题目可更深入探讨概念本质

详细报告和PDF请查看附件。

— 正维斯
2026年2月25日
"""

# 创建邮件
msg = MIMEMultipart()
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL
msg['Subject'] = subject

# 添加正文
msg.attach(MIMEText(body, 'plain', 'utf-8'))

# 添加PDF附件
pdf_path = "memory/logic_quiz_report.pdf"
if os.path.exists(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename='logic_quiz_report.pdf')
        msg.attach(pdf_attachment)
    print(f"PDF附件已添加: {pdf_path}")
else:
    print(f"PDF文件未找到: {pdf_path}")

# 添加Markdown附件
md_path = "memory/逻辑题测试报告_完整版.md"
if os.path.exists(md_path):
    with open(md_path, 'rb') as f:
        md_attachment = MIMEApplication(f.read(), _subtype="octet-stream")
        md_attachment.add_header('Content-Disposition', 'attachment', filename='逻辑题测试报告_完整版.md')
        msg.attach(md_attachment)
    print(f"Markdown附件已添加: {md_path}")

print("\n邮件内容已准备完成。")
print(f"发件人: {SENDER_EMAIL}")
print(f"收件人: {RECEIVER_EMAIL}")
print(f"主题: {subject}")
print("\n注意：要发送邮件，需要设置SMTP授权码。")
print("请手动配置或使用邮件客户端发送。")

# 邮件内容预览
print("\n" + "="*50)
print("邮件预览")
print("="*50)
print(body)
print("="*50)
