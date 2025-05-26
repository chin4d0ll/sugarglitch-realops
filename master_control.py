#!/usr/bin/env python3
"""
MASTER CONTROL SYSTEM 🎯💀
Ultimate Control Panel สำหรับทุก operation
"""

import os
import json
import subprocess
import time
from datetime import datetime

class MasterController:
    def __init__(self):
        self.base_path = "/workspaces/sugarglitch-realops"
        self.target_username = "whatilove1728"
        
    def print_banner(self):
        """แสดง banner แบบโหดๆ"""
        banner = """
🔥💀 MASTER CONTROL SYSTEM 💀🔥
================================
[STATUS] OPERATIONAL
[MODE] ULTIMATE_STEALTH
[TARGET] PERSONAL_ACCOUNT
[LEVEL] MAXIMUM_CARNAGE
================================
"""
        print(banner)
    
    def show_menu(self):
        """แสดงเมนูควบคุม"""
        menu = """
🎯 SELECT OPERATION:
==================
1. 👻 Ultimate Stealth Extraction
2. 📸 Advanced Visual Extraction  
3. 🔄 Test All Proxy Systems
4. 👁️  View Extraction Results
5. 🗂️  Open Image Gallery
6. 🔥 FULL ASSAULT MODE (ทุกอย่าง)
7. 📊 System Status Check
8. 🚪 Exit

💀 Enter choice (1-8): """
        
        return input(menu).strip()
    
    def run_stealth_extraction(self):
        """รัน stealth extraction"""
        print("\n🕵️ Initiating Ultimate Stealth Extraction...")
        
        try:
            result = subprocess.run(
                ['python3', 'ultimate_stealth_extractor.py'],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            print(result.stdout)
            if result.stderr:
                print(f"⚠️ Warnings: {result.stderr}")
                
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("⏰ Extraction timeout - operation too long")
            return False
        except Exception as e:
            print(f"💀 Extraction failed: {e}")
            return False
    
    def run_visual_extraction(self):
        """รัน visual extraction"""
        print("\n📸 Initiating Advanced Visual Extraction...")
        
        try:
            result = subprocess.run(
                ['python3', 'advanced_visual_extractor.py'],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            print(result.stdout)
            if result.stderr:
                print(f"⚠️ Warnings: {result.stderr}")
                
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("⏰ Visual extraction timeout")
            return False
        except Exception as e:
            print(f"💀 Visual extraction failed: {e}")
            return False
    
    def test_proxy_systems(self):
        """ทดสอบ proxy systems ทั้งหมด"""
        print("\n🔄 Testing All Proxy Systems...")
        
        proxy_scripts = [
            'quick_attack.py',
            'test_all_proxies.py',
            'smart_proxy_manager.py'
        ]
        
        for script in proxy_scripts:
            if os.path.exists(os.path.join(self.base_path, script)):
                print(f"\n🧪 Testing: {script}")
                try:
                    result = subprocess.run(
                        ['python3', script],
                        cwd=self.base_path,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    if result.returncode == 0:
                        print(f"✅ {script}: PASSED")
                    else:
                        print(f"❌ {script}: FAILED")
                        
                except Exception as e:
                    print(f"💀 {script}: ERROR - {e}")
    
    def view_extraction_results(self):
        """ดู extraction results"""
        print("\n👁️ Viewing Extraction Results...")
        
        # หาไฟล์ extraction ทั้งหมด
        extraction_files = []
        
        for file in os.listdir(self.base_path):
            if ('STEALTH' in file or 'EXTRACTION' in file) and file.endswith('.json'):
                extraction_files.append(file)
        
        if not extraction_files:
            print("❌ No extraction results found")
            return
        
        print(f"\n📂 Found {len(extraction_files)} extraction files:")
        
        for i, file in enumerate(extraction_files, 1):
            file_path = os.path.join(self.base_path, file)
            file_size = os.path.getsize(file_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            print(f"{i}. {file}")
            print(f"   Size: {file_size} bytes")
            print(f"   Modified: {mod_time}")
            
            # แสดง preview
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                if 'profile' in data:
                    profile = data['profile']
                    print(f"   👤 Profile: {profile.get('username', 'Unknown')}")
                    print(f"   📊 Followers: {profile.get('follower_count', 0)}")
                    print(f"   📸 Posts: {len(data.get('posts', []))}")
                
            except Exception as e:
                print(f"   ⚠️ Preview error: {e}")
                
            print()
    
    def open_image_gallery(self):
        """เปิด image gallery"""
        print("\n🗂️ Opening Image Gallery...")
        
        gallery_folder = os.path.join(self.base_path, "extracted_images")
        
        if not os.path.exists(gallery_folder):
            print("❌ No images folder found")
            return
        
        # หา HTML gallery files
        html_files = [f for f in os.listdir(gallery_folder) if f.endswith('.html')]
        
        if html_files:
            latest_html = max(html_files, key=lambda x: os.path.getctime(os.path.join(gallery_folder, x)))
            gallery_path = os.path.join(gallery_folder, latest_html)
            
            print(f"🎨 Gallery found: {latest_html}")
            print(f"📁 Path: {gallery_path}")
            
            # นับไฟล์รูป
            image_files = [f for f in os.listdir(gallery_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.gif', '.mp4'))]
            print(f"📸 Total images: {len(image_files)}")
            
            # แสดงรายการไฟล์
            if len(image_files) <= 10:
                print("\n📋 Image files:")
                for img in image_files:
                    print(f"   • {img}")
            else:
                print(f"\n📋 Sample images (showing 10 of {len(image_files)}):")
                for img in image_files[:10]:
                    print(f"   • {img}")
                print(f"   ... and {len(image_files) - 10} more")
        else:
            print("❌ No gallery HTML found")
    
    def full_assault_mode(self):
        """รันทุกอย่างแบบต่อเนื่อง"""
        print("\n🔥💀 FULL ASSAULT MODE INITIATED 💀🔥")
        print("=" * 50)
        
        operations = [
            ("👻 Stealth Extraction", self.run_stealth_extraction),
            ("📸 Visual Extraction", self.run_visual_extraction),
            ("🔄 Proxy Testing", self.test_proxy_systems),
            ("👁️ Results Review", self.view_extraction_results),
            ("🗂️ Gallery Check", self.open_image_gallery)
        ]
        
        for name, operation in operations:
            print(f"\n🎯 Executing: {name}")
            print("-" * 30)
            
            try:
                operation()
                print(f"✅ {name}: COMPLETED")
            except Exception as e:
                print(f"💀 {name}: FAILED - {e}")
            
            print("\n⏱️ Waiting 2 seconds...")
            time.sleep(2)
        
        print(f"""
🏆 FULL ASSAULT COMPLETE! 🏆
==========================
All operations executed!
Check results above.
""")
    
    def system_status_check(self):
        """ตรวจสอบสถานะระบบ"""
        print("\n📊 System Status Check...")
        
        # ตรวจสอบไฟล์สำคัญ
        important_files = [
            'ultimate_stealth_extractor.py',
            'advanced_visual_extractor.py',
            'proxy_config_new.json',
            'smart_proxy_manager.py'
        ]
        
        print("\n📁 Core Files:")
        for file in important_files:
            path = os.path.join(self.base_path, file)
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"✅ {file} ({size} bytes)")
            else:
                print(f"❌ {file} (missing)")
        
        # ตรวจสอบ extraction results
        extraction_count = len([f for f in os.listdir(self.base_path) if 'STEALTH' in f and f.endswith('.json')])
        print(f"\n📊 Extraction Files: {extraction_count}")
        
        # ตรวจสอบ images
        img_folder = os.path.join(self.base_path, "extracted_images")
        if os.path.exists(img_folder):
            img_count = len([f for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.gif', '.mp4'))])
            print(f"📸 Downloaded Images: {img_count}")
        else:
            print("📸 Downloaded Images: 0 (folder not found)")
        
        # ตรวจสอบ dependencies
        try:
            import requests
            print("✅ requests library: OK")
        except ImportError:
            print("❌ requests library: MISSING")
    
    def run(self):
        """เรียกใช้ master controller"""
        self.print_banner()
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == '1':
                    self.run_stealth_extraction()
                elif choice == '2':
                    self.run_visual_extraction()
                elif choice == '3':
                    self.test_proxy_systems()
                elif choice == '4':
                    self.view_extraction_results()
                elif choice == '5':
                    self.open_image_gallery()
                elif choice == '6':
                    self.full_assault_mode()
                elif choice == '7':
                    self.system_status_check()
                elif choice == '8':
                    print("\n🚪 Exiting Master Control System...")
                    break
                else:
                    print("\n❌ Invalid choice. Please select 1-8.")
                
                input("\n⏸️ Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n🚨 Operation interrupted by user")
                break
            except Exception as e:
                print(f"\n💀 Unexpected error: {e}")

if __name__ == "__main__":
    controller = MasterController()
    controller.run()
