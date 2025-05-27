#!/usr/bin/env python3
"""
📊 ALX Trading Password Analysis
วิเคราะห์ password patterns ใน alx_trading_passwords.txt
"""

import re
from collections import Counter

def analyze_alx_passwords():
    """วิเคราะห์ patterns ใน password list"""
    
    print("📊 ALX Trading Password Analysis")
    print("=" * 50)
    
    # อ่าน passwords
    with open('alx_trading_passwords.txt', 'r') as f:
        passwords = [line.strip() for line in f if line.strip()]
    
    print(f"📋 Total passwords: {len(passwords)}")
    print()
    
    # Pattern analysis
    patterns = {
        'with_alx': [],
        'with_trading': [],
        'with_fleming': [],
        'with_alexander': [],
        'with_numbers': [],
        'with_special_chars': [],
        'years': [],
        'simple': []
    }
    
    for pwd in passwords:
        pwd_lower = pwd.lower()
        
        if 'alx' in pwd_lower:
            patterns['with_alx'].append(pwd)
        if 'trading' in pwd_lower:
            patterns['with_trading'].append(pwd)
        if 'fleming' in pwd_lower:
            patterns['with_fleming'].append(pwd)
        if 'alexander' in pwd_lower:
            patterns['with_alexander'].append(pwd)
        if re.search(r'\d', pwd):
            patterns['with_numbers'].append(pwd)
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:",.<>?]', pwd):
            patterns['with_special_chars'].append(pwd)
        if re.search(r'20\d{2}', pwd):
            patterns['years'].append(pwd)
        if len(pwd) <= 6 and pwd.isalnum():
            patterns['simple'].append(pwd)
    
    # แสดงผล analysis
    print("🔍 Password Patterns:")
    print("-" * 30)
    for pattern_name, pattern_list in patterns.items():
        if pattern_list:
            percentage = (len(pattern_list) / len(passwords)) * 100
            print(f"📌 {pattern_name.replace('_', ' ').title()}: {len(pattern_list)} ({percentage:.1f}%)")
            # แสดงตัวอย่าง 3 ตัว
            for i, example in enumerate(pattern_list[:3]):
                print(f"   {i+1}. {example}")
            if len(pattern_list) > 3:
                print(f"   ... และอีก {len(pattern_list) - 3} รายการ")
            print()
    
    # Length analysis
    lengths = [len(pwd) for pwd in passwords]
    length_counter = Counter(lengths)
    
    print("📏 Password Length Distribution:")
    print("-" * 30)
    for length in sorted(length_counter.keys()):
        count = length_counter[length]
        percentage = (count / len(passwords)) * 100
        bar = "█" * min(int(percentage), 20)
        print(f"{length:2d} chars: {count:3d} ({percentage:4.1f}%) {bar}")
    
    print(f"\nAverage length: {sum(lengths) / len(lengths):.1f} characters")
    
    # Year analysis
    years = []
    for pwd in passwords:
        year_matches = re.findall(r'20\d{2}', pwd)
        years.extend(year_matches)
    
    if years:
        year_counter = Counter(years)
        print(f"\n📅 Years found in passwords:")
        print("-" * 30)
        for year in sorted(year_counter.keys()):
            count = year_counter[year]
            print(f"{year}: {count} times")
    
    # Strength assessment
    print(f"\n🛡️ Security Assessment:")
    print("-" * 30)
    
    weak = len([p for p in passwords if len(p) < 8 and not re.search(r'[!@#$%^&*]', p)])
    medium = len([p for p in passwords if 8 <= len(p) <= 12 and re.search(r'\d', p)])
    strong = len([p for p in passwords if len(p) > 12 and re.search(r'[!@#$%^&*]', p) and re.search(r'\d', p)])
    
    print(f"🔴 Weak (short, no special chars): {weak} ({weak/len(passwords)*100:.1f}%)")
    print(f"🟡 Medium (8-12 chars + numbers): {medium} ({medium/len(passwords)*100:.1f}%)")
    print(f"🟢 Strong (>12 chars + special + numbers): {strong} ({strong/len(passwords)*100:.1f}%)")
    
    # Top patterns
    print(f"\n🔝 Most Common Substrings:")
    print("-" * 30)
    
    substrings = []
    for pwd in passwords:
        pwd_lower = pwd.lower()
        if len(pwd_lower) >= 3:
            for i in range(len(pwd_lower) - 2):
                substrings.append(pwd_lower[i:i+3])
    
    common_substrings = Counter(substrings).most_common(10)
    for substring, count in common_substrings:
        if count > 1:
            print(f"'{substring}': {count} times")

if __name__ == "__main__":
    analyze_alx_passwords()
