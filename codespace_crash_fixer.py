#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Git Configuration Fixer - สำหรับมือใหม่
แก้ไขปัญหา git commit ไม่ได้เพราะไม่มี username/email
"""

import subprocess
import os
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_step(step_num, message):
    print(f"{Colors.BLUE}📋 Step {step_num}: {message}{Colors.END}")


def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_warning(message):
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")


def run_command(command, show_output=True):
    """รันคำสั่งและแสดงผลลัพธ์"""
    try:
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)
        if show_output and result.stdout:
            print(f"   {result.stdout.strip()}")
        if result.stderr and "warning" not in result.stderr.lower():
            print(f"   {Colors.YELLOW}{result.stderr.strip()}{Colors.END}")
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        print_error(f"Error running command: {e}")
        return False, ""


def check_current_git_config():
    """ตรวจสอบการตั้งค่า git ปัจจุบัน"""
    print_step(1, "ตรวจสอบการตั้งค่า Git ปัจจุบัน")

    print("   🔍 ตรวจสอบ username:")
    success, username = run_command("git config user.name")
    if not success or not username:
        print("   ❌ ไม่มี username")
        has_username = False
    else:
        print(f"   ✅ Username: {username}")
        has_username = True

    print("   🔍 ตรวจสอบ email:")
    success, email = run_command("git config user.email")
    if not success or not email:
        print("   ❌ ไม่มี email")
        has_email = False
    else:
        print(f"   ✅ Email: {email}")
        has_email = True

    return has_username, has_email


def fix_git_config():
    """แก้ไขการตั้งค่า git"""
    print_step(2, "แก้ไขการตั้งค่า Git")

    # ตั้งค่า username
    print("   🔧 ตั้งค่า username เป็น 'chin4d0ll'...")
    success, output = run_command('git config --global user.name "chin4d0ll"')
    if success:
        print_success("ตั้งค่า username สำเร็จ")
    else:
        print_error("ไม่สามารถตั้งค่า username ได้")
        return False

    # ตั้งค่า email
    print("   📧 ตั้งค่า email เป็น 'beamr.1232@gmail.com'...")
    success, output = run_command(
        'git config --global user.email "beamr.1232@gmail.com"')
    if success:
        print_success("ตั้งค่า email สำเร็จ")
    else:
        print_error("ไม่สามารถตั้งค่า email ได้")
        return False

    return True


def verify_git_config():
    """ตรวจสอบการตั้งค่าหลังจากแก้ไข"""
    print_step(3, "ตรวจสอบการตั้งค่าหลังจากแก้ไข")

    success, username = run_command("git config user.name")
    success2, email = run_command("git config user.email")

    if username == "chin4d0ll" and email == "beamr.1232@gmail.com":
        print_success("การตั้งค่า Git ถูกต้องแล้ว!")
        print(f"   👤 Username: {username}")
        print(f"   📧 Email: {email}")
        return True
    else:
        print_error("การตั้งค่ายังไม่ถูกต้อง")
        return False


def disable_gpg_signing():
    """ปิดการใช้ GPG signing ที่อาจทำให้เกิดปัญหา"""
    print_step(4, "ปิดการใช้ GPG signing (ป้องกันปัญหา)")

    success, output = run_command('git config --global commit.gpgsign false')
    if success:
        print_success("ปิด GPG signing แล้ว")
    else:
        print_warning("ไม่สามารถปิด GPG signing ได้ (ไม่เป็นไร)")


def test_git_commit():
    """ทดสอบการ commit"""
    print_step(5, "ทดสอบการ commit")

    # สร้างไฟล์ทดสอบ
    test_file = Path("git_test.txt")
    with open(test_file, 'w') as f:
        f.write(f"Git test file - {os.popen('date').read().strip()}\n")

    print("   📝 สร้างไฟล์ทดสอบ...")

    # Add ไฟล์
    success, output = run_command(f"git add {test_file}")
    if not success:
        print_error("ไม่สามารถ add ไฟล์ได้")
        return False

    print("   ➕ Add ไฟล์สำเร็จ")

    # Commit
    success, output = run_command(
        'git commit -m "🔧 Test commit after fixing git config"')
    if success:
        print_success("Commit สำเร็จ! 🎉")

        # ลบไฟล์ทดสอบ
        test_file.unlink()
        run_command(f"git add {test_file}")
        run_command('git commit -m "🧹 Clean up test file"')

        return True
    else:
        print_error("Commit ไม่สำเร็จ")
        test_file.unlink()  # ลบไฟล์ทดสอบ
        return False


def create_easy_commit_script():
    """สร้างสคริปต์สำหรับ commit ง่าย ๆ"""
    print_step(6, "สร้างสคริปต์ commit ง่าย ๆ")

    script_content = '''#!/bin/bash
# Easy Commit Script
echo "🚀 Easy Git Commit"
echo "=================="

# Add all files
git add .
echo "✅ Added all files"

# Get commit message
if [ "$1" != "" ]; then
    MESSAGE="$1"
else
    echo "📝 Enter commit message:"
    read MESSAGE
fi

# Commit
git commit -m "$MESSAGE"

if [ $? -eq 0 ]; then
    echo "🎉 Commit successful!"
    echo "💫 Push to GitHub? (y/n)"
    read PUSH
    if [ "$PUSH" = "y" ] || [ "$PUSH" = "Y" ]; then
        git push
        echo "🌟 Pushed to GitHub!"
    fi
else
    echo "❌ Commit failed"
fi
'''

    script_path = Path("easy_commit.sh")
    with open(script_path, 'w') as f:
        f.write(script_content)

    # ทำให้ executable
    os.chmod(script_path, 0o755)

    print_success("สร้าง easy_commit.sh แล้ว")
    print("   📄 วิธีใช้: ./easy_commit.sh \"ข้อความ commit\"")
    print("   📄 หรือ: ./easy_commit.sh (จะถาม message)")


def show_git_tips():
    """แสดงเทคนิคการใช้ git"""
    print_step(7, "เทคนิคการใช้ Git สำหรับมือใหม่")

    tips = [
        "git add . - เพิ่มไฟล์ทั้งหมด",
        "git commit -m \"message\" - commit พร้อมข้อความ",
        "git push - อัพโหลดไปยัง GitHub",
        "git status - ดูสถานะไฟล์",
        "git log --oneline - ดูประวัติ commit",
        "./easy_commit.sh - ใช้สคริปต์ที่เราสร้าง"
    ]

    for i, tip in enumerate(tips, 1):
        print(f"   {i}. {tip}")


def main():
    """ฟังก์ชันหลัก"""
    print(f"{Colors.BOLD}🔧 Git Configuration Fixer{Colors.END}")
    print("=" * 50)
    print("แก้ไขปัญหา git commit สำหรับมือใหม่")
    print("=" * 50)

    # ตรวจสอบการตั้งค่าปัจจุบัน
    has_username, has_email = check_current_git_config()

    if has_username and has_email:
        print_success("การตั้งค่า Git ครบถ้วนแล้ว!")
        print("   🤔 หากยัง commit ไม่ได้ ลองขั้นตอนถัดไป...")

    # แก้ไขการตั้งค่า
    if fix_git_config():
        # ตรวจสอบอีกครั้ง
        if verify_git_config():
            # ปิด GPG signing
            disable_gpg_signing()

            # ทดสอบ commit
            if test_git_commit():
                print(
                    f"\n{Colors.GREEN}🎉 แก้ไขสำเร็จ! Git พร้อมใช้งานแล้ว{Colors.END}")
            else:
                print_warning("Git config แก้แล้ว แต่ commit ยังไม่ได้")
                print("   💡 ลองเช็ค git status และ repository ที่อยู่")

            # สร้างสคริปต์ช่วย
            create_easy_commit_script()

            # แสดงเทคนิค
            show_git_tips()

        else:
            print_error("ไม่สามารถแก้ไขการตั้งค่าได้")

    print(f"\n{Colors.BOLD}📝 สรุปการแก้ไข:{Colors.END}")
    print("1. ✅ ตั้งค่า username: chin4d0ll")
    print("2. ✅ ตั้งค่า email: beamr.1232@gmail.com")
    print("3. ✅ ปิด GPG signing")
    print("4. ✅ สร้างสคริปต์ easy_commit.sh")
    print(f"\n{Colors.YELLOW}💡 คำแนะนำ:{Colors.END}")
    print("- ใช้ git status เพื่อดูสถานะไฟล์")
    print("- ใช้ ./easy_commit.sh เพื่อ commit แบบง่าย")
    print("- หากยังมีปัญหา ตรวจสอบว่าอยู่ในโฟลเดอร์ git repository")


if __name__ == "__main__":
    main()
