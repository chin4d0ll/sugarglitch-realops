#!/usr/bin/env python3
"""
🎯💎 Personal Data Summary Generator 
สร้างรายงานสรุปข้อมูลส่วนตัว Alexander Fleming
"""

import json
from pathlib import Path
from datetime import datetime


def analyze_extraction_results():
    """วิเคราะห์ผลการดึงข้อมูล"""

    print("🎯💎 Personal Data Analysis - Alexander Fleming")
    print("=" * 60)

    # อ่านรายงานล่าสุด
    reports_dir = Path(
        "/workspaces/sugarglitch-realops/extracted_personal_data/reports")
    latest_report = None

    if reports_dir.exists():
        report_files = list(reports_dir.glob("extraction_summary_*.json"))
        if report_files:
            latest_report = sorted(report_files)[-1]

    if not latest_report:
        print("❌ ไม่พบรายงานการดึงข้อมูล")
        return

    print(f"📋 กำลังวิเคราะห์: {latest_report.name}")

    with open(latest_report, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # วิเคราะห์ข้อมูลรูปภาพ
    images = data.get("image_details", [])
    print(f"\n📸 รูปภาพที่ดาวน์โหลด: {len(images)} รูป")

    if images:
        total_size = sum(img.get("file_size", 0) for img in images)
        print(
            f"   💾 ขนาดรวม: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")

        for i, img in enumerate(images, 1):
            print(f"   {i}. {img.get('filename', 'Unknown')}")
            print(f"      📊 ขนาด: {img.get('file_size', 0):,} bytes")
            print(f"      🔗 URL: {img.get('url', 'N/A')[:60]}...")

    # วิเคราะห์ข้อมูลส่วนตัว
    personal_data = data.get("personal_data_summary", {})

    all_emails = []
    all_phones = []
    all_names = []

    for filename, file_data in personal_data.items():
        emails = file_data.get("emails", [])
        phones = file_data.get("phone_numbers", [])
        names = file_data.get("names", [])

        print(f"\n📁 {filename}:")
        print(f"   📧 อีเมล: {len(emails)} รายการ")
        print(f"   📱 เบอร์โทร: {len(phones)} รายการ")
        print(f"   👤 ชื่อ: {len(names)} รายการ")

        all_emails.extend(emails)
        all_phones.extend(phones)
        all_names.extend(names)

    # รวมข้อมูลทั้งหมด
    print(f"\n🎯 สรุปข้อมูลส่วนตัวที่พบ:")
    print("=" * 40)

    # อีเมลที่ไม่ซ้ำ
    unique_emails = []
    seen_emails = set()

    for email_data in all_emails:
        email = email_data.get("email", "").lower()
        if email and "@" in email and email not in seen_emails:
            unique_emails.append(email_data)
            seen_emails.add(email)

    print(f"📧 อีเมลที่พบ: {len(unique_emails)} รายการ")
    for email_data in unique_emails:
        email = email_data.get("email", "")
        source = email_data.get("source", "")
        print(f"   ✅ {email}")
        print(f"      📂 แหล่งที่มา: {source}")

    # เบอร์โทรที่ดูน่าเชื่อถือ
    valid_phones = []
    for phone_data in all_phones:
        phone = phone_data.get("phone", "")
        # กรองเฉพาะเบอร์ที่ดูสมจริง
        if phone and len(phone.replace("-", "").replace(".", "").replace(" ", "")) >= 8:
            # ไม่เอาวันที่
            if not any(char in phone for char in ["2025", "2024", "2023"]):
                valid_phones.append(phone_data)

    # เอาเฉพาะที่ไม่ซ้ำ
    unique_phones = []
    seen_phones = set()

    for phone_data in valid_phones[:20]:  # เอาแค่ 20 อันแรก
        phone = phone_data.get("phone", "")
        if phone not in seen_phones:
            unique_phones.append(phone_data)
            seen_phones.add(phone)

    print(f"\n📱 เบอร์โทรที่น่าเชื่อถือ: {len(unique_phones)} รายการ")
    for phone_data in unique_phones[:10]:  # แสดงแค่ 10 อันแรก
        phone = phone_data.get("phone", "")
        source = phone_data.get("source", "")
        print(f"   📞 {phone}")

    # ชื่อที่น่าสนใจ
    interesting_names = []
    for name_data in all_names:
        name = name_data.get("value", "").strip()
        if name and len(name) > 2 and len(name) < 50:
            # กรองชื่อที่ดูสมจริง
            if not any(char in name.lower() for char in ["http", "www", ".com", "json", "null"]):
                interesting_names.append(name_data)

    # เอาเฉพาะที่ไม่ซ้ำ
    unique_names = []
    seen_names = set()

    for name_data in interesting_names:
        name = name_data.get("value", "").lower()
        if name not in seen_names:
            unique_names.append(name_data)
            seen_names.add(name)

    print(f"\n👤 ชื่อที่พบ: {len(unique_names)} รายการ")
    for name_data in unique_names[:15]:  # แสดงแค่ 15 อันแรก
        name = name_data.get("value", "")
        key = name_data.get("key", "")
        print(f"   👤 {name} (จาก: {key})")

    # สร้างรายงานสรุป
    summary = {
        "analysis_time": datetime.now().isoformat(),
        "source_report": str(latest_report),
        "summary": {
            "total_files_processed": len(data.get("files_processed", [])),
            "images_downloaded": len(images),
            "total_image_size_mb": sum(img.get("file_size", 0) for img in images) / 1024 / 1024,
            "unique_emails_found": len(unique_emails),
            "valid_phones_found": len(unique_phones),
            "interesting_names_found": len(unique_names)
        },
        "emails": [email["email"] for email in unique_emails],
        "phones": [phone["phone"] for phone in unique_phones[:10]],
        "names": [name["value"] for name in unique_names[:15]],
        "images": [{"filename": img["filename"], "size_kb": img["file_size"]//1024} for img in images]
    }

    # บันทึกรายงานสรุป
    summary_file = reports_dir / \
        f"personal_data_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n💾 รายงานสรุปบันทึกที่: {summary_file}")

    # สรุปข้อมูลสำคัญ
    print(f"\n🎯 ข้อมูลสำคัญที่พบ:")
    print("=" * 40)

    # เช็ค target emails
    target_emails = [
        "alexander_fleming@gmail.com",
        "alexanderfleming@gmail.com",
        "alexander.fleming@gmail.com",
        "alx.trading@gmail.com",
        "alx.trading@protonmail.com"
    ]

    found_targets = []
    for target in target_emails:
        if any(target.lower() in email.lower() for email in summary["emails"]):
            found_targets.append(target)

    print(f"✅ พบอีเมลเป้าหมาย: {len(found_targets)}/{len(target_emails)}")
    for target in found_targets:
        print(f"   📧 {target}")

    if summary["images"]:
        print(f"\n📸 รูปภาพที่ได้:")
        for img in summary["images"]:
            print(f"   📷 {img['filename']} ({img['size_kb']} KB)")

    print(f"\n📊 สถิติรวม:")
    print(
        f"   📁 ไฟล์ที่ประมวลผล: {summary['summary']['total_files_processed']}")
    print(f"   📧 อีเมลที่พบ: {summary['summary']['unique_emails_found']}")
    print(f"   📱 เบอร์โทรที่พบ: {summary['summary']['valid_phones_found']}")
    print(f"   👤 ชื่อที่พบ: {summary['summary']['interesting_names_found']}")
    print(
        f"   📸 รูปภาพ: {summary['summary']['images_downloaded']} รูป ({summary['summary']['total_image_size_mb']:.2f} MB)")

    print("\n" + "=" * 60)
    print("🎉 การวิเคราะห์เสร็จสมบูรณ์!")
    print("💡 ข้อมูลทั้งหมดถูกบันทึกไว้แล้ว")

    return summary_file


if __name__ == "__main__":
    analyze_extraction_results()
