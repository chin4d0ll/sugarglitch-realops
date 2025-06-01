#!/usr/bin/env python3
"""
🔥💾 SUGARGLITCH REALOPS SMART AUTO COMMIT 💾🔥
===============================================
ระบบ commit อัตโนมัติอัจฉริยะ
- ตรวจสอบการเปลี่ยนแปลงอัตโนมัติ
- สร้าง commit message ที่สมเหตุสมผล
- Push พร้อม status report
- รองรับ custom message

Created by: น้องจิน (chin4d0ll) ♥️
Date: 2025-06-01
"""

import subprocess
import sys
import datetime
from pathlib import Path
import argparse

class SmartAutoCommit:
    """💎 ระบบ Auto Commit อัจฉริยะ 💎"""
    
    def __init__(self):
        self.repo_path = Path("/workspaces/sugarglitch-realops")
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def run_command(self, command, capture_output=True):
        """รันคำสั่ง shell"""
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.repo_path)
                return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
            else:
                result = subprocess.run(command, shell=True, cwd=self.repo_path)
                return result.returncode == 0, "", ""
        except Exception as e:
            return False, "", str(e)
    
    def check_git_status(self):
        """ตรวจสอบสถานะ git"""
        success, output, error = self.run_command("git status --porcelain")
        if not success:
            print(f"❌ ข้อผิดพลาด git status: {error}")
            return False, []
        
        changed_files = []
        if output:
            for line in output.split('\n'):
                if line.strip():
                    status = line[:2]
                    filename = line[3:]
                    changed_files.append((status.strip(), filename))
        
        return True, changed_files
    
    def get_current_branch(self):
        """ดูชื่อ branch ปัจจุบัน"""
        success, branch, error = self.run_command("git branch --show-current")
        return branch if success else "main"
    
    def generate_smart_commit_message(self, changed_files, custom_message=None):
        """สร้าง commit message อัจฉริยะ"""
        if custom_message:
            return custom_message
        
        # วิเคราะห์ประเภทไฟล์ที่เปลี่ยน
        file_types = {
            'database': [],
            'scripts': [],
            'config': [],
            'docs': [],
            'results': [],
            'others': []
        }
        
        for status, filename in changed_files:
            filename_lower = filename.lower()
            if any(db_keyword in filename_lower for db_keyword in ['database', 'db_', 'sql']):
                file_types['database'].append(filename)
            elif filename_lower.endswith(('.py', '.sh', '.js')):
                file_types['scripts'].append(filename)
            elif any(config_keyword in filename_lower for config_keyword in ['config', 'json', '.env']):
                file_types['config'].append(filename)
            elif any(doc_keyword in filename_lower for doc_keyword in ['readme', '.md', 'doc']):
                file_types['docs'].append(filename)
            elif 'result' in filename_lower:
                file_types['results'].append(filename)
            else:
                file_types['others'].append(filename)
        
        # สร้าง commit message ตามประเภทการเปลี่ยนแปลง
        if file_types['database']:
            commit_type = "feat: Database system enhancements"
            details = f"- Updated database management files: {len(file_types['database'])} files"
        elif file_types['scripts']:
            commit_type = "feat: Script improvements and updates"  
            details = f"- Enhanced automation scripts: {len(file_types['scripts'])} files"
        elif file_types['config']:
            commit_type = "config: Configuration updates"
            details = f"- Updated configuration files: {len(file_types['config'])} files"
        elif file_types['docs']:
            commit_type = "docs: Documentation updates"
            details = f"- Updated documentation: {len(file_types['docs'])} files"
        else:
            commit_type = "feat: General system improvements"
            details = f"- Updated various system files: {len(changed_files)} files"
        
        message = f"""{commit_type}

🔥💾 SugarGlitch RealOps Updates - {self.timestamp}:
{details}
- Total files changed: {len(changed_files)}
- Auto-generated commit with smart analysis

📊 File Summary:"""
        
        for category, files in file_types.items():
            if files:
                message += f"\n- {category.title()}: {len(files)} files"
        
        message += f"\n\n🚀 Auto-committed by SugarGlitch Smart Commit System"
        
        return message
    
    def add_all_files(self):
        """เพิ่มไฟล์ทั้งหมด"""
        success, output, error = self.run_command("git add .")
        if not success:
            print(f"❌ ข้อผิดพลาด git add: {error}")
            return False
        print("✅ เพิ่มไฟล์ทั้งหมดสำเร็จ")
        return True
    
    def commit_changes(self, message):
        """Commit การเปลี่ยนแปลง"""
        # Escape quotes in message
        escaped_message = message.replace('"', '\\"')
        success, output, error = self.run_command(f'git commit -m "{escaped_message}"')
        
        if not success:
            if "nothing to commit" in error:
                print("✅ ไม่มีการเปลี่ยนแปลงที่จะ commit")
                return True
            else:
                print(f"❌ ข้อผิดพลาด git commit: {error}")
                return False
        
        print("✅ Commit สำเร็จ!")
        print(f"📝 {output}")
        return True
    
    def push_to_remote(self):
        """Push ไปยัง remote"""
        branch = self.get_current_branch()
        success, output, error = self.run_command(f"git push origin {branch}")
        
        if not success:
            print(f"❌ ข้อผิดพลาด git push: {error}")
            return False
        
        print("🚀 Push สำเร็จ!")
        return True
    
    def show_final_status(self):
        """แสดงสถานะสุดท้าย"""
        print("\n📊 Final Status:")
        success, output, error = self.run_command("git log --oneline -1")
        if success:
            print(f"📋 Latest commit: {output}")
        
        success, output, error = self.run_command("git status --short")
        if success and output:
            print(f"📁 Remaining changes: {len(output.split())}")
        else:
            print("✅ Working tree clean")
    
    def auto_commit_push(self, custom_message=None, skip_push=False):
        """ฟังก์ชันหลักสำหรับ auto commit และ push"""
        print("🔥💾 SUGARGLITCH SMART AUTO COMMIT")
        print("=" * 50)
        print(f"⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # ตรวจสอบสถานะ
        success, changed_files = self.check_git_status()
        if not success:
            return False
        
        if not changed_files:
            print("✅ ไม่มีการเปลี่ยนแปลงที่จะ commit")
            return True
        
        print(f"📝 ไฟล์ที่เปลี่ยนแปลง: {len(changed_files)} ไฟล์")
        for status, filename in changed_files[:10]:  # แสดงแค่ 10 ไฟล์แรก
            print(f"   {status} {filename}")
        
        if len(changed_files) > 10:
            print(f"   ... และอีก {len(changed_files) - 10} ไฟล์")
        
        print()
        
        # เพิ่มไฟล์ทั้งหมด
        if not self.add_all_files():
            return False
        
        # สร้าง commit message
        commit_message = self.generate_smart_commit_message(changed_files, custom_message)
        print("💬 Commit Message:")
        print(commit_message[:200] + "..." if len(commit_message) > 200 else commit_message)
        print()
        
        # Commit
        if not self.commit_changes(commit_message):
            return False
        
        # Push (ถ้าไม่ skip)
        if not skip_push:
            if not self.push_to_remote():
                return False
        else:
            print("⏭️  Skip push (local commit only)")
        
        # แสดงสถานะสุดท้าย
        self.show_final_status()
        
        print("\n🎉 Auto commit เสร็จสิ้น!")
        return True

def main():
    """ฟังก์ชันหลัก"""
    parser = argparse.ArgumentParser(description="SugarGlitch Smart Auto Commit")
    parser.add_argument("-m", "--message", help="Custom commit message")
    parser.add_argument("--local-only", action="store_true", help="Commit only (no push)")
    parser.add_argument("--quick", action="store_true", help="Quick commit with minimal output")
    
    args = parser.parse_args()
    
    auto_commit = SmartAutoCommit()
    
    try:
        success = auto_commit.auto_commit_push(
            custom_message=args.message,
            skip_push=args.local_only
        )
        
        if success:
            if not args.quick:
                print(f"\n✅ Success! Repository updated at {datetime.datetime.now().strftime('%H:%M:%S')}")
        else:
            print("\n❌ Auto commit failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
