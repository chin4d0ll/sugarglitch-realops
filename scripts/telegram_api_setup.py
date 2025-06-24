#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 TELEGRAM API INSTALLER & RUNNER 🔥
ติดตั้ง dependencies และรันการดึงข้อมูลจริง
"""

import subprocess
import sys
import os


def install_requirements():
    """ติดตั้ง packages ที่จำเป็น"""
    print("📦 ติดตั้ง Telegram API libraries...")

    packages = [
        'telethon',
        'cryptg',  # สำหรับเร่งความเร็ว
        'pillow',  # สำหรับรูปภาพ
        'aiofiles'  # สำหรับไฟล์ async
    ]

    for package in packages:
        try:
            print(f"📥 Installing {package}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False

    return True


def create_config_template():
    """สร้างไฟล์ config template"""
    config_content = """{
  "api_id": "YOUR_API_ID_FROM_MY_TELEGRAM_ORG",
  "api_hash": "YOUR_API_HASH_FROM_MY_TELEGRAM_ORG",
  "phone": "YOUR_PHONE_NUMBER_WITH_COUNTRY_CODE"
}"""

    with open('telegram_config.json', 'w') as f:
        f.write(config_content)

    print("📄 สร้างไฟล์ telegram_config.json แล้ว")
    print("✏️ กรุณาแก้ไขไฟล์นี้ด้วยข้อมูลจริง")


def main():
    print("🚀 TELEGRAM API SETUP & RUNNER")
    print("=" * 40)

    # ติดตั้ง requirements
    if not install_requirements():
        print("❌ การติดตั้งล้มเหลว")
        return

    # สร้าง config
    if not os.path.exists('telegram_config.json'):
        create_config_template()
        print("\n📋 SETUP INSTRUCTIONS:")
        print("1. ไปที่ https://my.telegram.org/")
        print("2. เข้าสู่ระบบด้วยเบอร์โทร")
        print("3. ไป 'API development tools'")
        print("4. สร้าง app ใหม่ (ใส่ชื่ออะไรก็ได้)")
        print("5. คัดลอก API ID และ API Hash")
        print("6. แก้ไขไฟล์ telegram_config.json")
        print("7. รันสคริปต์อีกครั้ง")
        return

    print("✅ Setup เสร็จสิ้น!")
    print("🔥 พร้อมใช้งาน Telegram API แล้ว")


if __name__ == "__main__":
    main()
