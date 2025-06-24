#!/usr/bin/env python3
"""
🔥📸 Advanced Personal Data & Image Extractor
ดึงข้อมูลส่วนตัวและรูปภาพจากไฟล์ JSON ที่พบ
"""

import json
import requests
import os
import hashlib
from pathlib import Path
from datetime import datetime
import re
import urllib.parse


def download_image(url, output_dir, filename_prefix=""):
    """ดาวน์โหลดรูปภาพจาก URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()

        # สร้างชื่อไฟล์
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

        # หา extension
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path.lower()

        if path.endswith(('.jpg', '.jpeg')):
            ext = '.jpg'
        elif path.endswith('.png'):
            ext = '.png'
        elif path.endswith('.gif'):
            ext = '.gif'
        elif path.endswith('.webp'):
            ext = '.webp'
        else:
            content_type = response.headers.get('content-type', '').lower()
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            else:
                ext = '.jpg'  # default

        filename = f"{filename_prefix}{url_hash}{ext}"
        file_path = output_dir / filename

        # บันทึกไฟล์
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        file_size = file_path.stat().st_size
        print(f"   ✅ Downloaded: {filename} ({file_size} bytes)")

        return {
            "filename": filename,
            "local_path": str(file_path),
            "file_size": file_size,
            "url": url,
            "downloaded_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"   ❌ Failed to download {url}: {e}")
        return None


def extract_images_from_json(json_file, output_dir):
    """ดึงรูปภาพจากไฟล์ JSON"""
    print(f"🔍 Extracting images from: {json_file.name}")

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        image_urls = []

        def find_image_urls(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key

                    # ค้นหา URL รูปภาพ
                    if isinstance(value, str):
                        if any(keyword in key.lower() for keyword in ['pic', 'image', 'photo', 'avatar']):
                            if value.startswith(('http://', 'https://')):
                                image_urls.append({
                                    "url": value,
                                    "source_key": key,
                                    "path": current_path
                                })

                        # ค้นหา URL ที่มี image extension
                        if value.startswith(('http://', 'https://')) and any(ext in value.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                            image_urls.append({
                                "url": value,
                                "source_key": key,
                                "path": current_path
                            })

                    # เรียกซ้ำ
                    if isinstance(value, (dict, list)):
                        find_image_urls(value, current_path)

            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_image_urls(item, f"{path}[{i}]")

        find_image_urls(data)

        print(f"   📸 Found {len(image_urls)} image URLs")

        # ดาวน์โหลดรูปภาพ
        downloaded_images = []
        for i, img_info in enumerate(image_urls):
            url = img_info["url"]
            filename_prefix = f"{json_file.stem}_{i+1}_"

            result = download_image(url, output_dir, filename_prefix)
            if result:
                result.update(img_info)
                downloaded_images.append(result)

        return downloaded_images

    except Exception as e:
        print(f"   ❌ Error processing {json_file.name}: {e}")
        return []


def extract_personal_data_from_json(json_file):
    """ดึงข้อมูลส่วนตัวจากไฟล์ JSON"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        personal_data = {
            "emails": [],
            "phone_numbers": [],
            "names": [],
            "usernames": [],
            "locations": [],
            "social_profiles": [],
            "other_data": {}
        }

        def extract_data(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key

                    if isinstance(value, str):
                        # ค้นหาอีเมล
                        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                        emails = re.findall(email_pattern, value)
                        personal_data["emails"].extend(
                            [{"email": email, "source": current_path} for email in emails])

                        # ค้นหาเบอร์โทร
                        phone_patterns = [
                            r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
                            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
                        ]
                        for pattern in phone_patterns:
                            phones = re.findall(pattern, value)
                            personal_data["phone_numbers"].extend(
                                [{"phone": phone, "source": current_path} for phone in phones])

                        # ค้นหาข้อมูลอื่น ๆ
                        personal_keywords = {
                            'names': ['name', 'full_name', 'display_name'],
                            'usernames': ['username', 'user', 'handle'],
                            'locations': ['location', 'address', 'city', 'country'],
                            'social_profiles': ['instagram', 'facebook', 'twitter', 'tiktok', 'linkedin']
                        }

                        for data_type, keywords in personal_keywords.items():
                            if any(keyword in key.lower() for keyword in keywords):
                                personal_data[data_type].append({
                                    "value": value,
                                    "source": current_path,
                                    "key": key
                                })

                    # เรียกซ้ำ
                    if isinstance(value, (dict, list)):
                        extract_data(value, current_path)

            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    extract_data(item, f"{path}[{i}]")

        extract_data(data)

        return personal_data

    except Exception as e:
        print(
            f"   ❌ Error extracting personal data from {json_file.name}: {e}")
        return {}


def main():
    print("🔥📸 Advanced Personal Data & Image Extractor")
    print("=" * 50)

    # สร้าง directories
    base_dir = Path("/workspaces/sugarglitch-realops/extracted_personal_data")
    images_dir = base_dir / "images"
    reports_dir = base_dir / "reports"

    base_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    print(f"📁 Output directory: {base_dir}")

    # ไฟล์ที่พบจากการสแกนก่อนหน้า
    target_files = [
        "legendary_instagram_data_1750367143.json",
        "spiderfoot_adult_analysis_alx.trading_20250624_173758.json",
        "telegram_intelligence_Alx_TYW_1750786438.json",
        "deep_domain_analysis_20250624_180014.json",
        "stealth_osint_report_20250619_200615.json"
    ]

    workspace = Path("/workspaces/sugarglitch-realops")

    all_results = {
        "extraction_time": datetime.now().isoformat(),
        "files_processed": [],
        "total_images_downloaded": 0,
        "total_personal_data_found": {},
        "image_details": [],
        "personal_data_summary": {}
    }

    # ประมวลผลแต่ละไฟล์
    for filename in target_files:
        file_path = workspace / filename

        if not file_path.exists():
            print(f"⚠️ File not found: {filename}")
            continue

        print(f"\n🔍 Processing: {filename}")

        # ดึงรูปภาพ
        downloaded_images = extract_images_from_json(file_path, images_dir)
        all_results["image_details"].extend(downloaded_images)
        all_results["total_images_downloaded"] += len(downloaded_images)

        # ดึงข้อมูลส่วนตัว
        personal_data = extract_personal_data_from_json(file_path)
        all_results["personal_data_summary"][filename] = personal_data

        all_results["files_processed"].append(filename)

        print(f"   📸 Images downloaded: {len(downloaded_images)}")
        if personal_data:
            print(f"   📧 Emails found: {len(personal_data.get('emails', []))}")
            print(
                f"   📱 Phone numbers found: {len(personal_data.get('phone_numbers', []))}")
            print(f"   👤 Names found: {len(personal_data.get('names', []))}")

    # สร้างรายงานสรุป
    summary_report = reports_dir / \
        f"extraction_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(summary_report, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Summary report saved: {summary_report}")

    # แสดงสรุป
    print("\n" + "=" * 50)
    print("📊 EXTRACTION SUMMARY")
    print("=" * 50)
    print(f"Files processed: {len(all_results['files_processed'])}")
    print(f"Total images downloaded: {all_results['total_images_downloaded']}")

    # รวมข้อมูลส่วนตัวทั้งหมด
    all_emails = []
    all_phones = []
    all_names = []

    for file_data in all_results["personal_data_summary"].values():
        all_emails.extend(file_data.get("emails", []))
        all_phones.extend(file_data.get("phone_numbers", []))
        all_names.extend(file_data.get("names", []))

    # Remove duplicates
    unique_emails = list(set([item["email"] for item in all_emails]))
    unique_phones = list(set([item["phone"] for item in all_phones]))
    unique_names = list(set([item["value"] for item in all_names]))

    print(f"Unique emails found: {len(unique_emails)}")
    print(f"Unique phone numbers found: {len(unique_phones)}")
    print(f"Unique names found: {len(unique_names)}")

    if unique_emails:
        print("\n📧 Emails found:")
        for email in unique_emails[:10]:  # Show first 10
            print(f"   {email}")

    if unique_names:
        print("\n👤 Names found:")
        for name in unique_names[:10]:  # Show first 10
            if name and len(name) > 2:
                print(f"   {name}")

    print(f"\n📁 Images saved in: {images_dir}")
    print(f"📋 Reports saved in: {reports_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()
