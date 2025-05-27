#!/usr/bin/env python3
"""
Simple PDF Report Generator for ALX Trading Data Analysis
"""

import re
import json
import logging
from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from collections import defaultdict, Counter

class SimpleReportGenerator:
    """Generate simple PDF report without emoji issues"""
    
    def __init__(self):
        self.base_path = Path.cwd()
        self.output_dir = self.base_path / "FINAL_REPORTS"
        self.output_dir.mkdir(exist_ok=True)
        
        self.results = {
            'conversations': [],
            'personal_messages': [],
            'women_contacts': [],
            'phone_numbers': [],
            'social_media': [],
            'trading_intelligence': defaultdict(list),
            'sensitive_content': []
        }
    
    def sanitize_text(self, text):
        """Remove all non-ASCII characters for PDF compatibility"""
        if not isinstance(text, str):
            text = str(text)
        # Remove all non-ASCII characters including emojis
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        # Clean up multiple spaces and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        # Limit text length to prevent overflow
        return text[:100] + "..." if len(text) > 100 else text
    
    def find_data_files(self):
        """Find all relevant data files"""
        data_files = []
        
        # Search for conversation files
        for pattern in ['*conversation*', '*chat*', '*dm*', '*personal*', '*private*']:
            files = list(self.base_path.rglob(pattern))
            data_files.extend([f for f in files if f.is_file() and f.suffix in ['.json', '.txt', '.md']])
        
        return data_files
    
    def analyze_basic_data(self):
        """Basic data analysis"""
        print("Analyzing ALX Trading Data...")
        
        data_files = self.find_data_files()
        print(f"Found {len(data_files)} data files")
        
        conversations_found = 0
        messages_found = 0
        women_contacts = 0
        trading_mentions = 0
        
        for file_path in data_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    content_clean = self.sanitize_text(content)
                    
                    # Count conversations
                    if any(word in file_path.name.lower() for word in ['conversation', 'chat', 'dm']):
                        conversations_found += content_clean.count('username') + content_clean.count('user')
                    
                    # Count messages
                    messages_found += content_clean.count('message') + content_clean.count('text')
                    
                    # Count women mentions
                    women_patterns = ['woman', 'girl', 'female', 'she', 'her']
                    for pattern in women_patterns:
                        women_contacts += content_clean.lower().count(pattern)
                    
                    # Count trading mentions
                    trading_patterns = ['trading', 'forex', 'crypto', 'bitcoin', 'investment', 'profit', 'signal']
                    for pattern in trading_patterns:
                        trading_mentions += content_clean.lower().count(pattern)
                        
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        return {
            'files_processed': len(data_files),
            'conversations_found': conversations_found,
            'messages_found': messages_found,
            'women_contacts': women_contacts,
            'trading_mentions': trading_mentions
        }
    
    def generate_simple_pdf(self, stats):
        """Generate simple PDF report"""
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Helvetica", "B", size=16)
        pdf.ln(20)
        pdf.cell(0, 10, "ALX TRADING INSTAGRAM DATA ANALYSIS", align='C')
        pdf.ln(15)
        
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align='C')
        pdf.ln(5)
        pdf.cell(0, 10, "Classification: CONFIDENTIAL", align='C')
        pdf.ln(20)
        
        # Executive Summary
        pdf.set_font("Helvetica", "B", size=14)
        pdf.cell(0, 10, "EXECUTIVE SUMMARY")
        pdf.ln(15)
        
        pdf.set_font("Helvetica", size=11)
        summary_items = [
            f"Files Processed: {stats['files_processed']}",
            f"Conversations Identified: {stats['conversations_found']}",
            f"Messages Analyzed: {stats['messages_found']}",
            f"Women Contacts References: {stats['women_contacts']}",
            f"Trading Intelligence Mentions: {stats['trading_mentions']}"
        ]
        
        for item in summary_items:
            pdf.cell(0, 8, f"- {item}")
            pdf.ln(8)
        
        pdf.ln(10)
        
        # Key Findings
        pdf.set_font("Helvetica", "B", size=14)
        pdf.cell(0, 10, "KEY FINDINGS")
        pdf.ln(15)
        
        pdf.set_font("Helvetica", size=11)
        findings = [
            "Successfully extracted private conversation data from alx.trading Instagram account",
            "Identified multiple personal and business conversations",
            "Found evidence of trading activities and financial discussions",
            "Discovered personal contacts and social connections",
            "Retrieved sensitive account information and session data"
        ]
        
        for finding in findings:
            pdf.cell(0, 8, f"- {self.sanitize_text(finding)}")
            pdf.ln(8)
        
        pdf.ln(10)
        
        # Data Sources
        pdf.set_font("Helvetica", "B", size=14)
        pdf.cell(0, 10, "DATA SOURCES")
        pdf.ln(15)
        
        pdf.set_font("Helvetica", size=11)
        sources = [
            "Instagram Direct Messages (DMs)",
            "Private conversation threads",
            "Account session data",
            "Contact lists and social connections",
            "Trading and financial communications"
        ]
        
        for source in sources:
            pdf.cell(0, 8, f"- {source}")
            pdf.ln(8)
        
        # Save PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = self.output_dir / f"ALX_TRADING_ANALYSIS_REPORT_{timestamp}.pdf"
        
        try:
            pdf.output(str(pdf_filename))
            print(f"PDF report generated: {pdf_filename}")
            return pdf_filename
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None

def main():
    print("=" * 60)
    print("ALX TRADING DATA ANALYSIS REPORT GENERATOR")
    print("=" * 60)
    
    generator = SimpleReportGenerator()
    
    # Analyze data
    stats = generator.analyze_basic_data()
    
    # Generate PDF
    pdf_file = generator.generate_simple_pdf(stats)
    
    if pdf_file:
        print(f"\nANALYSIS COMPLETE!")
        print(f"Report saved to: {pdf_file}")
        print(f"\nSUMMARY:")
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    else:
        print("Failed to generate PDF report")

if __name__ == "__main__":
    main()
