#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Configuration Fixer
แก้ไขการตั้งค่าในไฟล์ Telegram scripts

⚡ Features:
- แก้ไข API credentials placeholders
- ตั้งค่า phone number
- ตรวจสอบ syntax errors
- ปรับปรุงการตั้งค่าทั่วไป
"""

import os
import re
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = type('MockConsole', (), {'print': print})()


class ConfigurationFixer:
    """เครื่องมือแก้ไขการตั้งค่า"""

    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.changes_made = 0

    def fix_all_configs(self):
        """แก้ไขการตั้งค่าทั้งหมด"""
        if RICH_AVAILABLE:
            console.print(
                Panel.fit("🔧 Configuration Fixer", style="bold blue"))
        else:
            print("=== Configuration Fixer ===")

        # รับข้อมูลจากผู้ใช้
        api_config = self.get_user_config()

        if not api_config:
            print("❌ ยกเลิกการตั้งค่า")
            return

        # หาไฟล์ที่ต้องแก้ไข
        python_files = list(self.project_path.glob("*.py"))
        telegram_files = []

        # กรองเฉพาะไฟล์ที่เกี่ยวข้องกับ Telegram
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if any(keyword in content.lower() for keyword in [
                        'your_api_id', 'your_api_hash', '+66xxxxxxxxx',
                        'api_id', 'api_hash', 'telegram'
                    ]):
                        telegram_files.append(file_path)
            except Exception:
                continue

        if RICH_AVAILABLE:
            console.print(
                f"[blue]📁 Found {len(telegram_files)} files to fix[/blue]")
        else:
            print(f"Found {len(telegram_files)} files to fix")

        # แก้ไขแต่ละไฟล์
        for file_path in telegram_files:
            self.fix_single_file(file_path, api_config)

        if RICH_AVAILABLE:
            console.print(
                f"\n[green]✅ Fixed {self.changes_made} configuration issues![/green]")
        else:
            print(f"Fixed {self.changes_made} configuration issues!")

    def get_user_config(self):
        """รับข้อมูลการตั้งค่าจากผู้ใช้"""
        if RICH_AVAILABLE:
            console.print(
                "\n[yellow]📋 Please provide your Telegram API configuration:[/yellow]")
            console.print(
                "[dim]Get your API credentials from: https://my.telegram.org[/dim]")

            try:
                api_id = Prompt.ask("API ID", default="skip")
                if api_id.lower() == "skip":
                    return None

                api_hash = Prompt.ask("API Hash", default="skip")
                if api_hash.lower() == "skip":
                    return None

                phone = Prompt.ask(
                    "Phone Number (with country code, e.g., +66912345678)", default="skip")
                if phone.lower() == "skip":
                    return None

                return {
                    'api_id': api_id,
                    'api_hash': api_hash,
                    'phone': phone
                }
            except KeyboardInterrupt:
                return None
        else:
            print("\n=== API Configuration ===")
            print("Get your API credentials from: https://my.telegram.org")

            api_id = input("API ID (or 'skip' to cancel): ").strip()
            if api_id.lower() == "skip":
                return None

            api_hash = input("API Hash (or 'skip' to cancel): ").strip()
            if api_hash.lower() == "skip":
                return None

            phone = input(
                "Phone Number (with country code, e.g., +66912345678): ").strip()
            if not phone:
                return None

            return {
                'api_id': api_id,
                'api_hash': api_hash,
                'phone': phone
            }

    def fix_single_file(self, file_path, config):
        """แก้ไขไฟล์เดียว"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            changes_in_file = 0

            # แก้ไข API_ID
            if 'your_api_id' in content:
                content = re.sub(
                    r"API_ID\s*=\s*['\"]your_api_id['\"]",
                    f"API_ID = '{config['api_id']}'",
                    content
                )
                content = re.sub(
                    r"api_id\s*=\s*['\"]your_api_id['\"]",
                    f"api_id = '{config['api_id']}'",
                    content
                )
                changes_in_file += 1

            # แก้ไข API_HASH
            if 'your_api_hash' in content:
                content = re.sub(
                    r"API_HASH\s*=\s*['\"]your_api_hash['\"]",
                    f"API_HASH = '{config['api_hash']}'",
                    content
                )
                content = re.sub(
                    r"api_hash\s*=\s*['\"]your_api_hash['\"]",
                    f"api_hash = '{config['api_hash']}'",
                    content
                )
                changes_in_file += 1

            # แก้ไข PHONE
            if '+66xxxxxxxxx' in content:
                content = re.sub(
                    r"PHONE\s*=\s*['\"][+]66xxxxxxxxx['\"]",
                    f"PHONE = '{config['phone']}'",
                    content
                )
                content = re.sub(
                    r"phone\s*=\s*['\"][+]66xxxxxxxxx['\"]",
                    f"phone = '{config['phone']}'",
                    content
                )
                changes_in_file += 1

            # บันทึกไฟล์ถ้ามีการเปลี่ยนแปลง
            if content != original_content:
                # สำรองไฟล์เดิม
                backup_path = file_path.with_suffix(
                    f"{file_path.suffix}.backup")
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)

                # เขียนไฟล์ใหม่
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.changes_made += changes_in_file

                if RICH_AVAILABLE:
                    console.print(
                        f"[green]✅ Fixed {file_path.name} ({changes_in_file} changes)[/green]")
                else:
                    print(
                        f"Fixed {file_path.name} ({changes_in_file} changes)")

        except Exception as e:
            if RICH_AVAILABLE:
                console.print(
                    f"[red]❌ Failed to fix {file_path.name}: {e}[/red]")
            else:
                print(f"Failed to fix {file_path.name}: {e}")


def main():
    """ฟังก์ชันหลัก"""
    try:
        fixer = ConfigurationFixer()
        fixer.fix_all_configs()

    except KeyboardInterrupt:
        print("\n⏹️ Configuration fixing interrupted")
    except Exception as e:
        print(f"❌ Configuration fixing failed: {e}")


if __name__ == "__main__":
    main()
