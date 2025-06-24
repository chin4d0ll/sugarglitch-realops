#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥💎 Personal Data Extractor - Alexander Fleming Edition 💎🔥
==============================================================
ดึงข้อมูลส่วนตัวจากอีเมลที่พบทั้งหมด รวมถึงรูปภาพและไฟล์ต่างๆ
สำหรับ alexander_fleming@gmail.com และ alx.trading

Created by: น้องจิน (chin4d0ll) ♥️
Date: 24 มิถุนายน 2025
"""

import os
import json
import time
import requests
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import re
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import base64


class Colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_cute(text, color=Colors.PINK):
    print(f"{color}{text}{Colors.END}")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ️ {text}{Colors.END}")


class PersonalDataExtractor:
    def __init__(self):
        self.target_emails = [
            "alexander_fleming@gmail.com",
            "alexanderfleming@gmail.com",
            "alexander.fleming@gmail.com",
            "alexanderf@gmail.com",
            "alexander@gmail.com",
            "fleming@gmail.com",
            "afleming@gmail.com",
            "alx.trading@gmail.com",
            "alx.trading@protonmail.com",
            "whatilove1728@protonmail.com"
        ]

        self.output_dir = Path(
            "/workspaces/sugarglitch-realops/extracted_personal_data")
        self.output_dir.mkdir(exist_ok=True)

        self.images_dir = self.output_dir / "images"
        self.images_dir.mkdir(exist_ok=True)

        self.documents_dir = self.output_dir / "documents"
        self.documents_dir.mkdir(exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        self.extracted_data = {
            "emails": {},
            "personal_info": {},
            "images": [],
            "documents": [],
            "social_profiles": [],
            "relationships": [],
            "timestamps": {
                "extraction_start": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat()
            }
        }

        self.init_database()

    def init_database(self):
        """สร้างฐานข้อมูลสำหรับเก็บข้อมูลส่วนตัว"""
        try:
            self.db_path = self.output_dir / "personal_data.db"

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # ตาราง profiles
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS profiles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE,
                        full_name TEXT,
                        username TEXT,
                        phone TEXT,
                        location TEXT,
                        bio TEXT,
                        profile_pic_url TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # ตาราง images
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS images (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        profile_id INTEGER,
                        image_url TEXT,
                        local_path TEXT,
                        image_type TEXT,
                        description TEXT,
                        metadata TEXT,
                        downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (profile_id) REFERENCES profiles (id)
                    )
                ''')

                # ตาราง social_accounts
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS social_accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        profile_id INTEGER,
                        platform TEXT,
                        username TEXT,
                        profile_url TEXT,
                        follower_count INTEGER,
                        following_count INTEGER,
                        verified BOOLEAN,
                        private BOOLEAN,
                        last_active TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (profile_id) REFERENCES profiles (id)
                    )
                ''')

                # ตาราง relationships
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS relationships (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        profile_id INTEGER,
                        contact_name TEXT,
                        contact_email TEXT,
                        contact_phone TEXT,
                        relationship_type TEXT,
                        platform TEXT,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (profile_id) REFERENCES profiles (id)
                    )
                ''')

                conn.commit()
                print_success("ฐานข้อมูลถูกสร้างเรียบร้อย")

        except Exception as e:
            print_error(f"ไม่สามารถสร้างฐานข้อมูลได้: {e}")

    def extract_from_existing_files(self):
        """ดึงข้อมูลจากไฟล์ที่มีอยู่แล้ว"""
        print_cute("🔍 กำลังสแกนไฟล์ที่มีอยู่...")

        workspace_path = Path("/workspaces/sugarglitch-realops")

        # ไฟล์ที่น่าสนใจ
        target_files = [
            "deep_domain_analysis_*.json",
            "spiderfoot_*.json",
            "attack_report_*.json",
            "deep_osint_report_*.json",
            "*personal*.txt",
            "*password*.txt",
            "*email*.txt",
            "*.db"
        ]

        found_data = {}

        for pattern in target_files:
            for file_path in workspace_path.glob(pattern):
                try:
                    print_info(f"กำลังวิเคราะห์: {file_path.name}")

                    if file_path.suffix == '.json':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            self.extract_personal_from_json(
                                data, file_path.name)

                    elif file_path.suffix == '.txt':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            self.extract_personal_from_text(
                                content, file_path.name)

                    elif file_path.suffix == '.db':
                        self.extract_from_database(file_path)

                except Exception as e:
                    print_warning(f"ไม่สามารถอ่านไฟล์ {file_path.name}: {e}")

        return found_data

    def extract_personal_from_json(self, data: Any, filename: str):
        """ดึงข้อมูลส่วนตัวจาก JSON"""
        try:
            def search_in_object(obj, path=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key

                        # ค้นหาอีเมล
                        if any(email in str(value).lower() for email in [e.lower() for e in self.target_emails]):
                            self.extracted_data["emails"][current_path] = {
                                "value": value,
                                "source": filename,
                                "context": key
                            }

                        # ค้นหาข้อมูลส่วนตัว
                        personal_keys = ['name', 'phone', 'address',
                                         'bio', 'location', 'age', 'profile']
                        if any(pk in key.lower() for pk in personal_keys):
                            if current_path not in self.extracted_data["personal_info"]:
                                self.extracted_data["personal_info"][current_path] = [
                                ]

                            self.extracted_data["personal_info"][current_path].append({
                                "value": value,
                                "source": filename,
                                "key": key
                            })

                        # ค้นหา URL รูปภาพ
                        if 'pic' in key.lower() or 'image' in key.lower() or 'photo' in key.lower():
                            if isinstance(value, str) and ('http' in value or 'cdn' in value):
                                self.extracted_data["images"].append({
                                    "url": value,
                                    "source": filename,
                                    "context": key,
                                    "path": current_path
                                })

                        # ค้นหาข้อมูล Social Media
                        social_platforms = [
                            'instagram', 'facebook', 'twitter', 'tiktok', 'linkedin']
                        if any(platform in key.lower() for platform in social_platforms):
                            self.extracted_data["social_profiles"].append({
                                "platform": key,
                                "data": value,
                                "source": filename,
                                "path": current_path
                            })

                        # เรียกซ้ำสำหรับ nested objects
                        if isinstance(value, (dict, list)):
                            search_in_object(value, current_path)

                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        search_in_object(item, f"{path}[{i}]")

            search_in_object(data)
            print_success(f"วิเคราะห์ {filename} เสร็จสิ้น")

        except Exception as e:
            print_error(f"ข้อผิดพลาดในการวิเคราะห์ JSON: {e}")

    def extract_personal_from_text(self, content: str, filename: str):
        """ดึงข้อมูลส่วนตัวจากไฟล์ข้อความ"""
        try:
            lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue

                # ค้นหาอีเมล
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, line)

                for email in emails:
                    if any(target in email.lower() for target in [e.lower() for e in self.target_emails]):
                        self.extracted_data["emails"][f"{filename}:line_{line_num}"] = {
                            "value": email,
                            "source": filename,
                            "context": line,
                            "line_number": line_num
                        }

                # ค้นหาเบอร์โทร
                phone_patterns = [
                    r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
                    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                    r'\b\d{10,15}\b'
                ]

                for pattern in phone_patterns:
                    phones = re.findall(pattern, line)
                    for phone in phones:
                        if len(re.sub(r'[^\d]', '', phone)) >= 8:
                            if "phone_numbers" not in self.extracted_data["personal_info"]:
                                self.extracted_data["personal_info"]["phone_numbers"] = [
                                ]

                            self.extracted_data["personal_info"]["phone_numbers"].append({
                                "value": phone,
                                "source": filename,
                                "context": line,
                                "line_number": line_num
                            })

                # ค้นหา URLs
                url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                urls = re.findall(url_pattern, line)

                for url in urls:
                    if any(platform in url.lower() for platform in ['instagram', 'facebook', 'twitter', 'tiktok']):
                        self.extracted_data["social_profiles"].append({
                            "url": url,
                            "source": filename,
                            "context": line,
                            "line_number": line_num
                        })

            print_success(f"วิเคราะห์ {filename} เสร็จสิ้น")

        except Exception as e:
            print_error(f"ข้อผิดพลาดในการวิเคราะห์ text: {e}")

    def extract_from_database(self, db_path: Path):
        """ดึงข้อมูลจากฐานข้อมูล SQLite"""
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                # ดูตารางที่มี
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                for table in tables:
                    table_name = table[0]
                    print_info(f"กำลังสแกนตาราง: {table_name}")

                    try:
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
                        rows = cursor.fetchall()

                        # ดู column names
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        columns = [col[1] for col in cursor.fetchall()]

                        for row in rows:
                            row_dict = dict(zip(columns, row))

                            # ค้นหาข้อมูลที่เกี่ยวข้อง
                            for col, value in row_dict.items():
                                if value and isinstance(value, str):
                                    # ค้นหาอีเมล
                                    if '@' in value and any(target in value.lower() for target in [e.lower() for e in self.target_emails]):
                                        self.extracted_data["emails"][f"{db_path.name}:{table_name}:{col}"] = {
                                            "value": value,
                                            "source": str(db_path),
                                            "table": table_name,
                                            "column": col,
                                            "row_data": row_dict
                                        }

                                    # ค้นหา URLs รูปภาพ
                                    if any(keyword in col.lower() for keyword in ['pic', 'image', 'photo', 'avatar']):
                                        if 'http' in value:
                                            self.extracted_data["images"].append({
                                                "url": value,
                                                "source": str(db_path),
                                                "table": table_name,
                                                "column": col,
                                                "context": row_dict
                                            })

                    except Exception as e:
                        print_warning(f"ไม่สามารถอ่านตาราง {table_name}: {e}")

        except Exception as e:
            print_error(f"ข้อผิดพลาดในการอ่านฐานข้อมูล: {e}")

    def download_images(self):
        """ดาวน์โหลดรูปภาพทั้งหมดที่พบ"""
        print_cute("📸 กำลังดาวน์โหลดรูปภาพ...")

        downloaded_count = 0

        for i, image_info in enumerate(self.extracted_data["images"]):
            try:
                url = image_info.get("url", "")
                if not url or not url.startswith(('http://', 'https://')):
                    continue

                print_info(f"กำลังดาวน์โหลด: {url}")

                response = self.session.get(url, timeout=15, stream=True)
                response.raise_for_status()

                # สร้างชื่อไฟล์
                url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                file_extension = self.get_file_extension(
                    url, response.headers.get('content-type', ''))
                filename = f"image_{i+1}_{url_hash}{file_extension}"

                file_path = self.images_dir / filename

                # บันทึกไฟล์
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # อัพเดทข้อมูล
                image_info["local_path"] = str(file_path)
                image_info["filename"] = filename
                image_info["file_size"] = file_path.stat().st_size
                image_info["downloaded_at"] = datetime.now().isoformat()

                downloaded_count += 1
                print_success(f"ดาวน์โหลดสำเร็จ: {filename}")

                time.sleep(1)  # หน่วงเวลาป้องกันการ block

            except Exception as e:
                print_warning(f"ไม่สามารถดาวน์โหลดรูปภาพได้: {e}")

        print_success(f"ดาวน์โหลดรูปภาพเสร็จสิ้น: {downloaded_count} ไฟล์")

    def get_file_extension(self, url: str, content_type: str) -> str:
        """หาไฟล์ extension จาก URL หรือ content-type"""
        # จาก URL
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.lower()

        if path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')):
            return os.path.splitext(path)[1]

        # จาก content-type
        content_type_mapping = {
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/bmp': '.bmp'
        }

        return content_type_mapping.get(content_type.lower(), '.jpg')

    def save_to_database(self):
        """บันทึกข้อมูลลงฐานข้อมูล"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # บันทึกข้อมูล profiles
                for email in self.target_emails:
                    email_data = [v for k, v in self.extracted_data["emails"].items(
                    ) if email.lower() in v.get("value", "").lower()]

                    if email_data:
                        cursor.execute('''
                            INSERT OR REPLACE INTO profiles (email, full_name, created_at, updated_at)
                            VALUES (?, ?, ?, ?)
                        ''', (email, "Alexander Fleming", datetime.now(), datetime.now()))

                        profile_id = cursor.lastrowid

                        # บันทึกรูปภาพ
                        for image_info in self.extracted_data["images"]:
                            cursor.execute('''
                                INSERT INTO images (profile_id, image_url, local_path, image_type, metadata, downloaded_at)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (
                                profile_id,
                                image_info.get("url", ""),
                                image_info.get("local_path", ""),
                                "profile_image",
                                json.dumps(image_info),
                                image_info.get("downloaded_at",
                                               datetime.now().isoformat())
                            ))

                        # บันทึก social accounts
                        for social_info in self.extracted_data["social_profiles"]:
                            cursor.execute('''
                                INSERT INTO social_accounts (profile_id, platform, profile_url, created_at)
                                VALUES (?, ?, ?, ?)
                            ''', (
                                profile_id,
                                social_info.get("platform", "unknown"),
                                social_info.get(
                                    "url", social_info.get("data", "")),
                                datetime.now()
                            ))

                conn.commit()
                print_success("บันทึกข้อมูลลงฐานข้อมูลเรียบร้อย")

        except Exception as e:
            print_error(f"ข้อผิดพลาดในการบันทึกฐานข้อมูล: {e}")

    def generate_report(self):
        """สร้างรายงานสรุป"""
        report_path = self.output_dir / \
            f"personal_data_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # อัพเดท timestamp
        self.extracted_data["timestamps"]["extraction_end"] = datetime.now(
        ).isoformat()

        # สรุปสถิติ
        stats = {
            "total_emails_found": len(self.extracted_data["emails"]),
            "total_images_found": len(self.extracted_data["images"]),
            "total_images_downloaded": len([img for img in self.extracted_data["images"] if img.get("local_path")]),
            "total_social_profiles": len(self.extracted_data["social_profiles"]),
            "total_personal_info_fields": len(self.extracted_data["personal_info"]),
            "target_emails": self.target_emails
        }

        self.extracted_data["statistics"] = stats

        # บันทึกรายงาน
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)

        print_success(f"รายงานถูกบันทึกที่: {report_path}")

        # แสดงสรุป
        self.print_summary()

        return report_path

    def print_summary(self):
        """แสดงสรุปผลการดึงข้อมูล"""
        print_cute("\n" + "="*60)
        print_cute("🎯 สรุปผลการดึงข้อมูลส่วนตัว Alexander Fleming")
        print_cute("="*60)

        stats = self.extracted_data.get("statistics", {})

        print(f"📧 อีเมลที่พบ: {stats.get('total_emails_found', 0)} รายการ")
        print(f"📸 รูปภาพที่พบ: {stats.get('total_images_found', 0)} รูป")
        print(
            f"💾 รูปภาพที่ดาวน์โหลด: {stats.get('total_images_downloaded', 0)} รูป")
        print(
            f"🌐 โปรไฟล์โซเชียล: {stats.get('total_social_profiles', 0)} แพลตฟอร์ม")
        print(
            f"👤 ข้อมูลส่วนตัว: {stats.get('total_personal_info_fields', 0)} ฟิลด์")

        print_cute("\n📧 อีเมลเป้าหมาย:")
        for email in self.target_emails:
            found = any(email.lower() in v.get("value", "").lower()
                        for v in self.extracted_data["emails"].values())
            status = "✅ พบ" if found else "❌ ไม่พบ"
            print(f"   {email} - {status}")

        if self.extracted_data["images"]:
            print_cute("\n📸 รูปภาพที่พบ:")
            for i, img in enumerate(self.extracted_data["images"][:5], 1):
                print(f"   {i}. {img.get('url', 'N/A')[:60]}...")
                if img.get("local_path"):
                    print(
                        f"      💾 ดาวน์โหลดแล้ว: {Path(img['local_path']).name}")

        print_cute(f"\n📁 ไฟล์ทั้งหมดถูกบันทึกใน: {self.output_dir}")
        print_cute("="*60)

    def run_full_extraction(self):
        """รันการดึงข้อมูลแบบครบวงจร"""
        print_cute("🚀 เริ่มการดึงข้อมูลส่วนตัว Alexander Fleming")
        print_cute("="*60)

        # 1. ดึงข้อมูลจากไฟล์ที่มี
        self.extract_from_existing_files()

        # 2. ดาวน์โหลดรูปภาพ
        self.download_images()

        # 3. บันทึกลงฐานข้อมูล
        self.save_to_database()

        # 4. สร้างรายงาน
        report_path = self.generate_report()

        print_cute("\n🎉 การดึงข้อมูลเสร็จสมบูรณ์!")

        return report_path


def main():
    """ฟังก์ชันหลัก"""
    try:
        extractor = PersonalDataExtractor()
        report_path = extractor.run_full_extraction()

        print_cute(f"\n📋 รายงานฉบับสมบูรณ์: {report_path}")
        print_cute("💡 ใช้ข้อมูลเพื่อการป้องกันและการศึกษาเท่านั้น")

    except KeyboardInterrupt:
        print_warning("\n⏹️ การดึงข้อมูลถูกยกเลิกโดยผู้ใช้")
    except Exception as e:
        print_error(f"ข้อผิดพลาด: {e}")


if __name__ == "__main__":
    main()
