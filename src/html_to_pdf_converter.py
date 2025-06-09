# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import os
import subprocess
import sys

def install_wkhtmltopdf():
    """ติดตั้ง wkhtmltopdf บน Linux"""
    try:
        print("🔧 ติดตั้ง wkhtmltopdf...")
        result = subprocess.run([
            "sudo", "apt-get", "update", "&&",
            "sudo", "apt-get", "install", "wkhtmltopdf", "-y"
        ], shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ ติดตั้ง wkhtmltopdf สำเร็จ!")
            return True
        else:
            print("❌ ติดตั้ง wkhtmltopdf ไม่สำเร็จ")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการติดตั้ง: {e}")
        return False

def check_wkhtmltopdf():
    """ตรวจสอบว่ามี wkhtmltopdf หรือไม่"""
    try:
        result = subprocess.run(["wkhtmltopdf", "--version"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ พบ wkhtmltopdf แล้ว")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def convert_html_to_pdf():
    """แปลง HTML เป็น PDF"""

    # ตรวจสอบว่ามีไฟล์ HTML หรือไม่
    if not os.path.exists("dm_output.html"):
        print("❌ ไม่พบไฟล์ dm_output.html")
        print("กรุณารัน json_to_html_converter.py ก่อน")
        return False

    # ตรวจสอบ wkhtmltopdf
    if not check_wkhtmltopdf():
        print("❌ ไม่พบ wkhtmltopdf")
        response = input("ต้องการติดตั้งหรือไม่? (y/n): ").strip().lower()
        if response == 'y':
            if not install_wkhtmltopdf():
                return False
        else:
            print("💡 วิธีติดตั้งด้วยตนเอง:")
            print("sudo apt-get update")
            print("sudo apt-get install wkhtmltopdf -y")
            return False

    # แปลง HTML เป็น PDF
    try:
        print("📄 กำลังแปลง HTML เป็น PDF...")

        # คำสั่งแปลง PDF พร้อมตัวเลือกต่างๆ
        cmd = [
            "wkhtmltopdf",
            "--page-size", "A4",
            "--margin-top", "0.75in",
            "--margin-right", "0.75in",
            "--margin-bottom", "0.75in",
            "--margin-left", "0.75in",
            "--encoding", "UTF-8",
            "--no-outline",
            "dm_output.html",
            "dm_output.pdf"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ แปลง HTML เป็น PDF สำเร็จ!")
            print("📄 ไฟล์: dm_output.pdf")

            # แสดงขขนาดไฟล์
            if os.path.exists("dm_output.pdf"):
                size = os.path.getsize("dm_output.pdf")
                print(f"📏 ขนาดไฟล์: {size:,} bytes ({size/1024:.1f} KB)")

            return True
        else:
            print("❌ แปลง PDF ไม่สำเร็จ")
            print(f"Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    print("🔄 HTML to PDF Converter")
    print("=" * 30)

    success = convert_html_to_pdf()

    if success:
        print("\n🎉 เสร็จสิ้น! ไฟล์ที่ได้:")
        print("📄 dm_output.html - รายงานแบบ HTML")
        print("📄 dm_output.pdf - รายงานแบบ PDF")
    else:
        print("\n❌ การแปลง PDF ไม่สำเร็จ")
        print("💡 แต่ยังมีไฟล์ HTML ให้ใช้งาน: dm_output.html")

if __name__ == "__main__":
    main()
