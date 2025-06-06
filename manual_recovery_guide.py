#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ Manual Recovery Guide
คู่มือการกู้คืนไฟล์แบบ manual สำหรับ chin4d0ll
"""

import subprocess
import sys
from pathlib import Path

def run_command(command: str, description: str):
    """🔧 รัน command และแสดงผล"""
    print(f"\n💖 {description}")
    print(f"🔧 Command: {command}")
    print("-" * 40)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("📋 Output:")
            print(result.stdout)
        
        if result.stderr and result.returncode != 0:
            print("❌ Error:")
            print(result.stderr)
            
    except Exception as e:
        print(f"💥 Error running command: {e}")

def main():
    """🚀 Main manual recovery guide"""
    print("🛠️ Manual Git Recovery Guide")
    print("🌸 Girly Hacker Edition for chin4d0ll")
    print("=" * 50)
    
    # Step 1: ตรวจสอบสถานะ
    run_command("git status", "ตรวจสอบสถานะ Git repository")
    
    # Step 2: ดู commits ล่าสุด
    run_command("git log --oneline -10", "ดู 10 commits ล่าสุด")
    
    # Step 3: ดูไฟล์ที่มีใน commit ล่าสุด
    run_command("git ls-tree -r HEAD --name-only", "ดูไฟล์ทั้งหมดใน commit ล่าสุด")
    
    # Step 4: ดูไฟล์ที่เปลี่ยนแปลงใน commit ล่าสุด
    run_command("git show --name-status HEAD", "ดูการเปลี่ยนแปลงใน commit ล่าสุด")
    
    # Step 5: หาไฟล์ที่ถูกลบ
    run_command("git log --diff-filter=D --summary --oneline", "หาไฟล์ที่ถูกลบ")
    
    print("\n🌸 Manual Recovery Instructions:")
    print("=" * 40)
    print("1. 💾 กู้คืนไฟล์เฉพาะ:")
    print("   git checkout <commit-hash> -- <filename>")
    print("   ตัวอย่าง: git checkout HEAD~1 -- session-alx.trading")
    print("")
    print("2. 🔄 ย้อนกลับทั้ง repository:")
    print("   git reset --hard <commit-hash>")
    print("   ตัวอย่าง: git reset --hard HEAD~1")
    print("")
    print("3. 🌿 ดูเนื้อหาไฟล์ในอดีต:")
    print("   git show <commit-hash>:<filename>")
    print("   ตัวอย่าง: git show HEAD~1:session-alx.trading")
    print("")
    print("4. 📂 สร้างไฟล์ใหม่จากอดีต:")
    print("   git show <commit-hash>:<filename> > <new-filename>")
    print("   ตัวอย่าง: git show HEAD~1:session-alx.trading > recovered-session.json")

if __name__ == "__main__":
    main()
    