# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Git File Recovery System
🌸 Girly Hacker Edition - กู้คืนไฟล์จาก Git แบบสาวๆ
💖 Made for chin4d0ll who lost files but has commits
"""

import os
import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import re

class GirlyGitRecovery:
    """
    🌸 Girly Git Recovery System
    ระบบกู้คืนไฟล์จาก Git แบบสาวๆ hacker
    """

    def __init__(self):
        self.logger = self._setup_girly_logger()
        self.repo_path = Path.cwd()
        self.recovery_results = {}

        print("🌸 Git File Recovery System")
        print("💖 Girly Hacker Edition for chin4d0ll")
        print("🔍 ช่วยหาไฟล์ที่หายไปแบบสาวๆ")
        print("=" * 60)

    def _setup_girly_logger(self) -> logging.Logger:
        """💖 Setup cute girly logger"""
        logger = logging.getLogger("GirlyGitRecovery")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '🌸 %(asctime)s - %(message)s 💖'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _run_git_command(self, command: List[str]) -> Tuple[bool, str, str]:
        """🔧 รัน Git command แบบปลอดภัย"""
        try:
            self.logger.info(f"🔧 Running: git {' '.join(command[1:])}")

            result = subprocess.run(
                command,
                cwd = self.repo_path,
                capture_output = True,
                text = True,
                timeout = 30
            )

            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if success:
                self.logger.info(f"✅ Command successful")
            else:
                self.logger.warning(f"⚠️ Command failed: {stderr}")

            return success, stdout, stderr

        except subprocess.TimeoutExpired:
            self.logger.error("⏰ Git command timeout")
            return False, "", "Command timeout"
        except Exception as e:
            self.logger.error(f"💥 Git command error: {e}")
            return False, "", str(e)

    def check_git_status(self) -> Dict[str, Any]:
        """📊 ตรวจสอบสถานะ Git repository"""
        self.logger.info("📊 ตรวจสอบสถานะ Git repository...")

        status_info = {
            'is_git_repo': False,
            'current_branch': '',
            'has_commits': False,
            'working_tree_clean': False,
            'untracked_files': [],
            'modified_files': [],
            'deleted_files': [],
            'staged_files': []
        }

        # ตรวจสอบว่าเป็น Git repo หรือไม่
        success, stdout, stderr = self._run_git_command(['git', 'rev-parse', '--git-dir'])
        if not success:
            self.logger.error("❌ ไม่ใช่ Git repository")
            return status_info

        status_info['is_git_repo'] = True
        self.logger.info("✅ เป็น Git repository")

        # ตรวจสอบ branch ปัจจุบัน
        success, stdout, stderr = self._run_git_command(['git', 'branch', '--show-current'])
        if success and stdout:
            status_info['current_branch'] = stdout
            self.logger.info(f"🌿 Current branch: {stdout}")

        # ตรวจสอบว่ามี commits หรือไม่
        success, stdout, stderr = self._run_git_command(['git', 'log', '--oneline', '-n', '1'])
        if success and stdout:
            status_info['has_commits'] = True
            self.logger.info(f"✅ Has commits: {stdout}")

        # ตรวจสอบ working tree status
        success, stdout, stderr = self._run_git_command(['git', 'status', '--porcelain'])
        if success:
            if not stdout:
                status_info['working_tree_clean'] = True
                self.logger.info("✅ Working tree is clean")
            else:
                # Parse status output
                for line in stdout.split('\n'):
                    if line.strip():
                        status_code = line[:2]
                        filename = line[3:]

                        if status_code == '??':
                            status_info['untracked_files'].append(filename)
                        elif status_code[0] in ['M', 'A', 'D', 'R', 'C']:
                            status_info['staged_files'].append(filename)
                        elif status_code[1] in ['M', 'D']:
                            if status_code[1] == 'M':
                                status_info['modified_files'].append(filename)
                            elif status_code[1] == 'D':
                                status_info['deleted_files'].append(filename)

                self.logger.info(f"📝 Working tree has changes")
                if status_info['deleted_files']:
                    self.logger.warning(f"🗑️ Deleted files: {status_info['deleted_files']}")

        return status_info

    def get_recent_commits(self, count: int = 10) -> List[Dict[str, str]]:
        """📚 ดึงรายการ commits ล่าสุด"""
        self.logger.info(f"📚 ดึงรายการ {count} commits ล่าสุด...")

        success, stdout, stderr = self._run_git_command([
            'git', 'log', '--oneline', '--graph', '--decorate', f'-n', str(count)
        ])

        commits = []
        if success and stdout:
            for line in stdout.split('\n'):
                if line.strip():
                    # Parse commit line
                    match = re.match(r'[*|\\\s]*([a-f0-9]+)\s+(.+)', line.strip())
                    if match:
                        commit_hash = match.group(1)
                        commit_message = match.group(2)

                        commits.append({
                            'hash': commit_hash,
                            'message': commit_message,
                            'full_line': line
                        })

            self.logger.info(f"✅ พบ {len(commits)} commits")
            for i, commit in enumerate(commits[:5], 1):
                self.logger.info(f"  {i}. {commit['hash']}: {commit['message']}")

        return commits

    def find_lost_files(self, pattern: str = "") -> List[Dict[str, str]]:
        """🔍 หาไฟล์ที่หายไปใน Git history"""
        self.logger.info(f"🔍 ค้นหาไฟล์ที่หายไป (pattern: '{pattern}')...")

        # ใช้ git log เพื่อหาไฟล์ที่เคยมีอยู่
        success, stdout, stderr = self._run_git_command([
            'git', 'log', '--all', '--full-history', '--name-status', '--pretty = format:%H|%s|%ai'
        ])

        lost_files = []
        current_commit = None

        if success and stdout:
            for line in stdout.split('\n'):
                if '|' in line and not line.startswith(('A\t', 'M\t', 'D\t')):
                    # This is a commit line
                    parts = line.split('|', 2)
                    if len(parts) >= 3:
                        current_commit = {
                            'hash': parts[0],
                            'message': parts[1],
                            'date': parts[2]
                        }
                elif line.startswith(('A\t', 'M\t', 'D\t')) and current_commit:
                    # This is a file change line
                    status = line[0]
                    filename = line[2:]

                    # ถ้ามี pattern ให้ filter
                    if pattern and pattern.lower() not in filename.lower():
                        continue

                    # ตรวจสอบว่าไฟล์ยังอยู่หรือไม่
                    file_path = Path(filename)
                    if not file_path.exists():
                        lost_files.append({
                            'filename': filename,
                            'status': status,
                            'commit_hash': current_commit['hash'],
                            'commit_message': current_commit['message'],
                            'commit_date': current_commit['date'],
                            'exists_now': False
                        })

        # Remove duplicates
        unique_files = {}
        for file_info in lost_files:
            filename = file_info['filename']
            if filename not in unique_files:
                unique_files[filename] = file_info

        result = list(unique_files.values())

        self.logger.info(f"🔍 พบไฟล์ที่หายไป {len(result)} ไฟล์")
        for file_info in result[:10]:  # แสดงแค่ 10 ไฟล์แรก
            self.logger.info(f"  📄 {file_info['filename']} (last seen in {file_info['commit_hash'][:8]})")

        return result

    def recover_file_from_commit(self, filename: str, commit_hash: str,
                                new_filename: Optional[str] = None) -> bool:
        """💾 กู้คืนไฟล์จาก commit เฉพาะ"""

        if new_filename is None:
            new_filename = filename

        self.logger.info(f"💾 กู้คืนไฟล์: {filename} จาก commit {commit_hash[:8]}...")

        # ใช้ git show เพื่อดึงเนื้อหาไฟล์
        success, stdout, stderr = self._run_git_command([
            'git', 'show', f'{commit_hash}:{filename}'
        ])

        if success and stdout:
            try:
                # สร้าง directory ถ้าจำเป็น
                new_file_path = Path(new_filename)
                new_file_path.parent.mkdir(parents = True, exist_ok = True)

                # เขียนไฟล์
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(stdout)

                self.logger.info(f"✅ กู้คืนสำเร็จ: {new_filename}")
                return True

            except Exception as e:
                self.logger.error(f"💥 ไม่สามารถเขียนไฟล์: {e}")
                return False
        else:
            self.logger.error(f"❌ ไม่พบไฟล์ {filename} ใน commit {commit_hash[:8]}")
            return False

    def interactive_file_recovery(self) -> None:
        """🎮 Interactive file recovery สำหรับมือใหม่"""
        self.logger.info("🎮 เริ่ม Interactive File Recovery...")

        print("\n🌸 Interactive File Recovery Menu")
        print("=" * 40)

        while True:
            print("\n💖 เลือกสิ่งที่ต้องการทำ:")
            print("1. 📊 ดูสถานะ Git repository")
            print("2. 📚 ดู commits ล่าสุด")
            print("3. 🔍 หาไฟล์ที่หายไป")
            print("4. 💾 กู้คืนไฟล์เฉพาะ")
            print("5. 🚀 กู้คืนไฟล์ทั้งหมดที่หายไป")
            print("6. 🌸 ออกจากโปรแกรม")

            try:
                choice = input("\n💖 เลือกเมนู (1-6): ").strip()

                if choice == "1":
                    self._show_git_status()
                elif choice == "2":
                    self._show_recent_commits()
                elif choice == "3":
                    self._find_and_show_lost_files()
                elif choice == "4":
                    self._recover_specific_file()
                elif choice == "5":
                    self._recover_all_lost_files()
                elif choice == "6":
                    print("🌸 ขอบคุณที่ใช้ Girly Git Recovery! 💖")
                    break
                else:
                    print("❌ เลือกเมนู 1-6 เท่านั้นค่ะ")

            except KeyboardInterrupt:
                print("\n🛑 ออกจากโปรแกรม")
                break
            except Exception as e:
                print(f"💥 Error: {e}")

    def _show_git_status(self):
        """📊 แสดงสถานะ Git"""
        status = self.check_git_status()

        print("\n📊 Git Repository Status:")
        print("-" * 30)
        print(f"📁 Is Git Repo: {'✅' if status['is_git_repo'] else '❌'}")
        print(f"🌿 Current Branch: {status['current_branch'] or 'N/A'}")
        print(f"📚 Has Commits: {'✅' if status['has_commits'] else '❌'}")
        print(f"🧹 Working Tree Clean: {'✅' if status['working_tree_clean'] else '❌'}")

        if status['deleted_files']:
            print(f"🗑️ Deleted Files ({len(status['deleted_files'])}):")
            for f in status['deleted_files'][:5]:
                print(f"   - {f}")

        if status['untracked_files']:
            print(f"❓ Untracked Files ({len(status['untracked_files'])}):")
            for f in status['untracked_files'][:5]:
                print(f"   - {f}")

    def _show_recent_commits(self):
        """📚 แสดง commits ล่าสุด"""
        commits = self.get_recent_commits(15)

        print("\n📚 Recent Commits:")
        print("-" * 30)
        for i, commit in enumerate(commits, 1):
            print(f"{i:2}. {commit['hash'][:8]} - {commit['message']}")

    def _find_and_show_lost_files(self):
        """🔍 หาและแสดงไฟล์ที่หายไป"""
        pattern = input("🔍 ใส่ชื่อไฟล์ที่ต้องการหา (หรือ Enter สำหรับทั้งหมด): ").strip()

        lost_files = self.find_lost_files(pattern)

        if not lost_files:
            print("✅ ไม่พบไฟล์ที่หายไป")
            return

        print(f"\n🔍 พบไฟล์ที่หายไป {len(lost_files)} ไฟล์:")
        print("-" * 50)
        for i, file_info in enumerate(lost_files[:20], 1):  # แสดงแค่ 20 ไฟล์แรก
            print(f"{i:2}. 📄 {file_info['filename']}")
            print(f"     Last seen: {file_info['commit_hash'][:8]} - {file_info['commit_message'][:50]}...")

    def _recover_specific_file(self):
        """💾 กู้คืนไฟล์เฉพาะ"""
        filename = input("💾 ใส่ชื่อไฟล์ที่ต้องการกู้คืน: ").strip()
        if not filename:
            print("❌ กรุณาใส่ชื่อไฟล์")
            return

        commits = self.get_recent_commits(20)

        print(f"\n📚 เลือก commit ที่ต้องการกู้คืน:")
        for i, commit in enumerate(commits, 1):
            print(f"{i:2}. {commit['hash'][:8]} - {commit['message']}")

        try:
            choice = int(input(f"\n💖 เลือก commit (1-{len(commits)}): ")) - 1
            if 0 <= choice < len(commits):
                selected_commit = commits[choice]
                success = self.recover_file_from_commit(filename, selected_commit['hash'])

                if success:
                    print(f"✅ กู้คืนไฟล์ {filename} สำเร็จ!")
                else:
                    print(f"❌ ไม่สามารถกู้คืนไฟล์ {filename} ได้")
            else:
                print("❌ เลือก commit ไม่ถูกต้อง")
        except ValueError:
            print("❌ กรุณาใส่ตัวเลข")

    def _recover_all_lost_files(self):
        """🚀 กู้คืนไฟล์ทั้งหมดที่หายไป"""
        print("🚀 กำลังหาไฟล์ที่หายไป...")
        lost_files = self.find_lost_files()

        if not lost_files:
            print("✅ ไม่พบไฟล์ที่หายไป")
            return

        print(f"🔍 พบไฟล์ที่หายไป {len(lost_files)} ไฟล์")

        # ขอยืนยัน
        confirm = input(f"💖 ต้องการกู้คืนทั้งหมด? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ ยกเลิกการกู้คืน")
            return

        # สร้าง recovery directory
        recovery_dir = Path(f"recovered_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        recovery_dir.mkdir(exist_ok = True)

        print(f"📁 สร้างโฟลเดอร์กู้คืน: {recovery_dir}")

        success_count = 0
        total_count = len(lost_files)

        for i, file_info in enumerate(lost_files, 1):
            filename = file_info['filename']
            commit_hash = file_info['commit_hash']

            print(f"💾 กู้คืน ({i}/{total_count}): {filename}...")

            # กู้คืนไปยัง recovery directory
            new_filename = recovery_dir / filename
            success = self.recover_file_from_commit(filename, commit_hash, str(new_filename))

            if success:
                success_count += 1

        print(f"\n🎉 กู้คืนเสร็จสิ้น!")
        print(f"✅ สำเร็จ: {success_count}/{total_count} ไฟล์")
        print(f"📁 ไฟล์อยู่ใน: {recovery_dir}")

def main():
    """🚀 Main function"""
    print("🌸 Git File Recovery System")
    print("💖 Girly Hacker Edition for chin4d0ll")
    print("🔍 ช่วยหาไฟล์ที่หายไปจาก Git")
    print("=" * 60)

    try:
        recovery = GirlyGitRecovery()

        # ตรวจสอบสถานะ Git ก่อน
        status = recovery.check_git_status()

        if not status['is_git_repo']:
            print("❌ Directory นี้ไม่ใช่ Git repository")
            print("💡 ลอง cd ไปยัง directory ที่มี .git folder")
            return

        if not status['has_commits']:
            print("❌ Repository นี้ยังไม่มี commits")
            print("💡 ไม่สามารถกู้คืนไฟล์ได้ถ้าไม่มี commits")
            return

        print("✅ พร้อมใช้งาน Git Recovery System!")

        # เริ่ม interactive recovery
        recovery.interactive_file_recovery()

    except KeyboardInterrupt:
        print("\n🛑 ออกจากโปรแกรม")
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
