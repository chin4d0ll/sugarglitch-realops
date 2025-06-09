# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
ตัวช่วยสร้าง Session File
Session File Helper
"""

import json

def create_session_file():
    print("🔑 สร้างไฟล์ Session")
    print("=" * 30)

    sessionid = input("📋 ใส่ sessionid ที่คัดลอกมา: ")

    if sessionid:
        session_data = {
            "sessionid": sessionid.strip(),
            "created": "manual_input",
            "target": "alx.trading"
        }

        with open("session.json", "w") as f:
            json.dump(session_data, f, indent=2)

        print("✅ สร้างไฟล์ session.json เรียบร้อย!")
        print("▶️ ตอนนี้รัน: python3 extract_alx_trading.py")
    else:
        print("❌ ไม่ได้ใส่ sessionid")

if __name__ == "__main__":
    create_session_file()
