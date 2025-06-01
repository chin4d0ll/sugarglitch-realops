#!/usr/bin/env python3
"""
🔥 Instagram Image Extraction Runner 2025 🔥
ระบบรันเครื่องมือดึงข้อมูล Instagram แบบครบถ้วน
Multiple strategies for maximum success rate
"""

import asyncio
import subprocess
import sys
import json
import time
import os
from pathlib import Path
from datetime import datetime
import threading

class InstagramExtractionRunner:
    def __init__(self):
        self.workspace = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.workspace / "extracted_images"
        self.results_dir.mkdir(exist_ok=True)
        
        # Available extraction strategies
        self.extractors = {
            "working": {
                "file": "working_instagram_extractor_2025.py",
                "description": "🔥 Working extractor with real credentials",
                "pros": ["Real login data", "Proven working code", "Good success rate"],
                "cons": ["Rate limiting", "Account safety concerns"]
            },
            "master": {
                "file": "instagram_master_extractor.py", 
                "description": "🎯 Master extractor with Playwright",
                "pros": ["Browser automation", "Multiple strategies", "Screenshot capture"],
                "cons": ["Slower execution", "More resource intensive"]
            },
            "comprehensive": {
                "file": "instagram_comprehensive_extractor.py",
                "description": "📊 Comprehensive extraction with multiple APIs",
                "pros": ["Multiple API endpoints", "Fallback strategies", "Data diversity"],
                "cons": ["Complex setup", "Multiple dependencies"]
            },
            "instagrapi": {
                "file": "instagram_instagrapi_extractor.py",
                "description": "📱 InstagrAPI-based extractor",
                "pros": ["Official-like API", "High success rate", "Rich data"],
                "cons": ["Library dependency", "Account verification"]
            },
            "puppeteer": {
                "file": "instagram_puppeteer_extractor.py",
                "description": "🎭 Puppeteer-based browser automation",
                "pros": ["Real browser behavior", "JavaScript execution", "Human-like"],
                "cons": ["Node.js dependency", "Resource intensive"]
            }
        }
        
        # Target accounts to extract from
        self.target_accounts = [
            "alx.trading",
            "whatilove1728", 
            "instagram",  # Official Instagram account for testing
            "natgeo",     # National Geographic - lots of images
            "nasa"        # NASA - public content
        ]
        
        print("🚀 Instagram Image Extraction Runner 2025")
        print(f"📁 Results directory: {self.results_dir}")
        print(f"🎯 Target accounts: {', '.join(self.target_accounts)}")
        
    def show_menu(self):
        """Display extraction strategy menu"""
        print("\n" + "="*60)
        print("🎯 INSTAGRAM IMAGE EXTRACTION MENU")
        print("="*60)
        
        for i, (key, extractor) in enumerate(self.extractors.items(), 1):
            print(f"\n{i}. {extractor['description']}")
            print(f"   📄 File: {extractor['file']}")
            print(f"   ✅ Pros: {', '.join(extractor['pros'])}")
            print(f"   ⚠️  Cons: {', '.join(extractor['cons'])}")
        
        print(f"\n{len(self.extractors)+1}. 🔄 Run ALL extractors (parallel)")
        print(f"{len(self.extractors)+2}. 📊 Show extraction statistics")
        print(f"{len(self.extractors)+3}. 🧹 Clean old results")
        print(f"{len(self.extractors)+4}. 🌐 Launch image viewer")
        print(f"{len(self.extractors)+5}. ❌ Exit")
        
        return self.get_user_choice()
    
    def get_user_choice(self):
        """Get user choice with validation"""
        max_choice = len(self.extractors) + 5
        
        while True:
            try:
                choice = input(f"\n🤔 เลือกตัวเลือก (1-{max_choice}): ").strip()
                
                if choice.isdigit():
                    choice = int(choice)
                    if 1 <= choice <= max_choice:
                        return choice
                
                print(f"❌ กรุณาเลือกตัวเลข 1-{max_choice}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_extractor(self, extractor_key, background=False):
        """Run a specific extractor"""
        extractor = self.extractors[extractor_key]
        extractor_file = self.workspace / extractor["file"]
        
        if not extractor_file.exists():
            print(f"❌ Extractor file not found: {extractor_file}")
            return False
        
        print(f"\n🚀 Running {extractor['description']}")
        print(f"📄 File: {extractor_file}")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            if background:
                # Run in background and return process
                process = subprocess.Popen([
                    sys.executable, str(extractor_file)
                ], cwd=str(self.workspace))
                return process
            else:
                # Run and wait for completion
                result = subprocess.run([
                    sys.executable, str(extractor_file)
                ], cwd=str(self.workspace), capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ {extractor['description']} completed successfully!")
                    if result.stdout:
                        print("📊 Output:")
                        print(result.stdout[-1000:])  # Last 1000 chars
                else:
                    print(f"❌ {extractor['description']} failed!")
                    if result.stderr:
                        print("❌ Error:")
                        print(result.stderr[-1000:])  # Last 1000 chars
                
                return result.returncode == 0
                
        except Exception as e:
            print(f"❌ Error running extractor: {e}")
            return False
    
    def run_all_extractors(self):
        """Run all extractors in parallel"""
        print("\n🔄 Running ALL extractors in parallel...")
        print("⚠️  This will use significant system resources!")
        
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            return
        
        processes = []
        
        for key in self.extractors.keys():
            print(f"🚀 Starting {self.extractors[key]['description']}...")
            process = self.run_extractor(key, background=True)
            if process:
                processes.append((key, process))
            time.sleep(2)  # Stagger starts to avoid conflicts
        
        print(f"\n⏳ Waiting for {len(processes)} extractors to complete...")
        
        # Wait for all processes and collect results
        results = {}
        for key, process in processes:
            try:
                process.wait(timeout=300)  # 5 minute timeout per extractor
                results[key] = process.returncode == 0
                status = "✅ Success" if results[key] else "❌ Failed"
                print(f"{status}: {self.extractors[key]['description']}")
            except subprocess.TimeoutExpired:
                process.kill()
                results[key] = False
                print(f"⏰ Timeout: {self.extractors[key]['description']}")
        
        # Summary
        successful = sum(results.values())
        print(f"\n📊 Results: {successful}/{len(processes)} extractors succeeded")
        
        return results
    
    def show_statistics(self):
        """Show extraction statistics"""
        print("\n📊 EXTRACTION STATISTICS")
        print("="*50)
        
        # Count images by directory
        image_dirs = [
            self.results_dir,
            self.workspace / "screenshots",
            self.workspace / "media" / "extracted",
            self.workspace / "data" / "instagram"
        ]
        
        total_images = 0
        for img_dir in image_dirs:
            if img_dir.exists():
                images = list(img_dir.rglob("*.{png,jpg,jpeg,gif,webp}"))
                if images:
                    print(f"📁 {img_dir.name}: {len(images)} images")
                    total_images += len(images)
        
        print(f"\n🖼️ Total images found: {total_images}")
        
        # Show recent extraction results
        results_files = list((self.workspace / "results").glob("*extraction*.json"))
        if results_files:
            print(f"\n📄 Recent extraction reports: {len(results_files)}")
            for result_file in sorted(results_files)[-5:]:  # Last 5 reports
                mtime = datetime.fromtimestamp(result_file.stat().st_mtime)
                print(f"   📊 {result_file.name} - {mtime.strftime('%Y-%m-%d %H:%M')}")
    
    def clean_old_results(self):
        """Clean old extraction results"""
        print("\n🧹 CLEANING OLD RESULTS")
        print("="*40)
        
        confirm = input("⚠️  This will delete old extraction results. Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            return
        
        # Clean directories
        clean_dirs = [
            self.results_dir,
            self.workspace / "screenshots",
            self.workspace / "temp"
        ]
        
        cleaned_files = 0
        for clean_dir in clean_dirs:
            if clean_dir.exists():
                for file_path in clean_dir.rglob("*"):
                    if file_path.is_file():
                        try:
                            file_path.unlink()
                            cleaned_files += 1
                        except Exception as e:
                            print(f"❌ Error deleting {file_path}: {e}")
        
        print(f"✅ Cleaned {cleaned_files} files")
    
    def launch_image_viewer(self):
        """Launch the image viewer in browser"""
        print("\n🌐 Launching image viewer...")
        
        # Update the gallery first by running the discovery tool
        try:
            subprocess.run([
                sys.executable, str(self.workspace / "image_discovery_tool.py")
            ], cwd=str(self.workspace))
        except Exception as e:
            print(f"⚠️  Warning: Could not update image gallery: {e}")
        
        # Try to open in browser
        gallery_file = self.workspace / "complete_image_gallery.html"
        if gallery_file.exists():
            try:
                import webbrowser
                webbrowser.open(f"file://{gallery_file}")
                print(f"✅ Opened {gallery_file} in browser")
            except Exception as e:
                print(f"❌ Could not open browser: {e}")
                print(f"📁 Manually open: {gallery_file}")
        else:
            print(f"❌ Gallery file not found: {gallery_file}")
    
    def setup_dependencies(self):
        """Setup required dependencies"""
        print("📦 Setting up dependencies...")
        
        required_packages = [
            "requests",
            "playwright", 
            "instagrapi",
            "selenium",
            "beautifulsoup4",
            "pillow"
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package} - installed")
            except ImportError:
                print(f"📦 Installing {package}...")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                    print(f"✅ {package} - installed successfully")
                except Exception as e:
                    print(f"❌ Failed to install {package}: {e}")
    
    def run(self):
        """Main runner loop"""
        # Setup dependencies first
        self.setup_dependencies()
        
        while True:
            choice = self.show_menu()
            
            if choice <= len(self.extractors):
                # Run specific extractor
                extractor_keys = list(self.extractors.keys())
                extractor_key = extractor_keys[choice - 1]
                self.run_extractor(extractor_key)
                
            elif choice == len(self.extractors) + 1:
                # Run all extractors
                self.run_all_extractors()
                
            elif choice == len(self.extractors) + 2:
                # Show statistics
                self.show_statistics()
                
            elif choice == len(self.extractors) + 3:
                # Clean old results
                self.clean_old_results()
                
            elif choice == len(self.extractors) + 4:
                # Launch image viewer
                self.launch_image_viewer()
                
            elif choice == len(self.extractors) + 5:
                # Exit
                print("\n👋 Thank you for using Instagram Extraction Runner!")
                break
            
            input("\n⏸️  Press Enter to continue...")

def main():
    """Main entry point"""
    try:
        runner = InstagramExtractionRunner()
        runner.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
