#!/usr/bin/env python3
"""
ALX TRADING - SENSITIVE DATA PDF REPORT GENERATOR
สร้าง PDF รายงานข้อมูลละเอียดจากไฟล์ COMPLETE_SENSITIVE_REPORTS/ALX_TRADING_COMPLETE_SENSITIVE_DATA_20250527_164633.txt
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

def sanitize(text):
    if not isinstance(text, str):
        text = str(text)
    return text.replace('\x00', '').replace('\x1a', '').replace('\r', '').replace('\n', ' ').strip()

def extract_sensitive_blocks(txt_path, max_lines=2000):
    blocks = []
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    block = []
    count = 0
    for line in lines:
        if line.strip().startswith('FILE:') or line.strip().startswith('NUMBER:') or line.strip().startswith('CONVERSATION') or line.strip().startswith('KEY:'):
            if block:
                blocks.append(''.join(block))
                block = []
                count += 1
                if count >= max_lines:
                    break
        block.append(line)
    if block:
        blocks.append(''.join(block))
    return blocks

def generate_sensitive_pdf(txt_path, pdf_path):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, alignment=TA_CENTER, textColor=colors.darkred)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=16, alignment=TA_LEFT, textColor=colors.darkblue)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, alignment=TA_LEFT)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = []
    story.append(Paragraph('ALX TRADING - SENSITIVE DATA BREACH REPORT', title_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph('ข้อมูลละเอียดที่เจาะระบบมาจาก IG alx.trading (uncensored)', section_style))
    story.append(Spacer(1, 12))
    
    # Extract and add blocks
    blocks = extract_sensitive_blocks(txt_path, max_lines=40)  # ปรับจำนวน block ตามต้องการ
    for i, block in enumerate(blocks):
        story.append(Paragraph(f'--- Section {i+1} ---', section_style))
        story.append(Paragraph(sanitize(block), normal_style))
        story.append(Spacer(1, 10))
        if (i+1) % 5 == 0:
            story.append(PageBreak())
    
    doc.build(story)
    print(f'✅ PDF รายงานข้อมูลละเอียดสร้างแล้ว: {pdf_path}')

if __name__ == "__main__":
    txt_path = "COMPLETE_SENSITIVE_REPORTS/ALX_TRADING_COMPLETE_SENSITIVE_DATA_20250527_164633.txt"
    pdf_path = "FINAL_REAL_DATA_REPORTS/ALX_TRADING_SENSITIVE_DATA_REPORT_20250527.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    generate_sensitive_pdf(txt_path, pdf_path)
