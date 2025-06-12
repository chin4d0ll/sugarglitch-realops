#!/usr/bin/env python3
"""
SugarGlitch RealOps - Instagram OSINT Tool
Basic Instagram reconnaissance (Legal/Educational use only)
"""

import re
import sys
from datetime import datetime

def banner():
    print("📱 SugarGlitch RealOps - Instagram OSINT")
    print("="*45)
    print("⚠️  LEGAL USE ONLY - Educational Purpose")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def validate_username(username):
    """Validate Instagram username format"""
    pattern = r'^[a-zA-Z0-9._]{1,30}$'
    return re.match(pattern, username) is not None

def analyze_username(username):
    """Analyze username for patterns"""
    print(f"🔍 Analyzing username: @{username}")
    print("-" * 30)
    
    # Basic analysis
    print(f"📏 Length: {len(username)} characters")
    
    if username.isdigit():
        print("🔢 Type: Numeric only")
    elif username.isalpha():
        print("🔤 Type: Alphabetic only")
    else:
        print("🔣 Type: Mixed (letters, numbers, symbols)")
    
    # Pattern analysis
    if '.' in username:
        print("📍 Contains: Dots (.)")
    if '_' in username:
        print("📍 Contains: Underscores (_)")
    if any(c.isdigit() for c in username):
        print("📍 Contains: Numbers")
    
    # Common patterns
    if username.endswith(('2023', '2024', '2025')):
        print("📅 Pattern: Year suffix detected")
    
    print(f"\n✅ Username format is {'valid' if validate_username(username) else 'invalid'}")

def osint_suggestions(username):
    """Suggest OSINT techniques"""
    print(f"\n🎯 OSINT Suggestions for @{username}:")
    print("-" * 30)
    print("1. 🔍 Search variations:")
    print(f"   - {username}official")
    print(f"   - {username}_")
    print(f"   - {username}2025")
    
    print("2. 🌐 Cross-platform search:")
    print("   - Twitter, TikTok, Facebook")
    print("   - LinkedIn, YouTube")
    
    print("3. 🔎 Reverse search techniques:")
    print("   - Profile photo reverse search")
    print("   - Bio keywords analysis")

if __name__ == "__main__":
    banner()
    
    # Demo with example username
    test_username = "example_user123"
    analyze_username(test_username)
    osint_suggestions(test_username)
    
    print(f"\n⚠️  Remember: Use only for legal/educational purposes!")
