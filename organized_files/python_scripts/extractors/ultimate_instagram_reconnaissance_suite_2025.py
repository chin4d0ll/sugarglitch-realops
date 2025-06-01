#!/usr/bin/env python3
"""
🕵️💕 ULTIMATE INSTAGRAM RECONNAISSANCE SUITE 2025 💕🕵️
================================================================
- บูรณาการทุกเครื่องมือ Instagram ใน 1 เดียว
- Private Viewer + OSINT + Cookie Harvester + Image Analyzer
- Ultimate Toolkit สำหรับการวิเคราะห์ Instagram ขั้นสูง 
- เหมาะสำหรับ Penetration Testing & Security Research

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01
For: Educational & Authorized Security Research Only!
"""

import asyncio
import json
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import requests
import warnings
warnings.filterwarnings("ignore")

# === GIRLY CONFIG ===
GIRLY_BANNER = """
💋💖🕵️ ULTIMATE INSTAGRAM RECONNAISSANCE SUITE 2025 🕵️💖💋
        โดย น้องจิน - Ultimate Instagram Hacking Toolkit! ♥️
    Private Viewer + OSINT + Cookie Harvester + Image Analyzer
            All-in-One สำหรับ Instagram Security Research
"""

class UltimateInstagramReconSuite:
    """
    🕵️ Ultimate Instagram Reconnaissance Suite - รวมทุกเครื่องมือ
    """
    
    def __init__(self):
        self.results = {
            'target': '',
            'timestamp': datetime.now().isoformat(),
            'private_viewer_results': {},
            'osint_results': {},
            'cookie_harvest_results': {},
            'image_analysis_results': [],
            'overall_assessment': {},
            'discovered_intelligence': []
        }
        
        # Output directory
        self.output_dir = Path('./ultimate_recon_results')
        self.output_dir.mkdir(exist_ok=True)
        
        # Tool paths
        self.tool_paths = {
            'private_viewer': './ultimate_instagram_private_viewer_2025.py',
            'lightweight_viewer': './lightweight_instagram_bypass_2025.py',
            'osint_tool': './advanced_instagram_osint_2025.py',
            'cookie_harvester': './advanced_cookie_harvester_2025.py',
            'image_analyzer': './instagram_image_analyzer_2025.py'
        }
        
        self.girly_print("🕵️ Ultimate Instagram Reconnaissance Suite ถูกเตรียมพร้อม!", "INFO", "🚀")

    def girly_print(self, message: str, level: str = "INFO", emoji: str = "💖"):
        """Enhanced girly printing"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "\033[96m",     # Cyan
            "SUCCESS": "\033[92m",  # Green  
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",    # Red
            "CRITICAL": "\033[95m", # Magenta
            "RESET": "\033[0m"      # Reset
        }
        
        color = colors.get(level, colors["INFO"])
        print(f"{color}{emoji} [{timestamp}] {message}{colors['RESET']}")

    def check_tool_availability(self) -> Dict[str, bool]:
        """
        🔧 ตรวจสอบว่าเครื่องมือต่างๆ พร้อมใช้งานหรือไม่
        
        Returns:
            Dictionary ของสถานะเครื่องมือ
        """
        self.girly_print("🔧 กำลังตรวจสอบเครื่องมือที่พร้อมใช้งาน...", "INFO", "🔍")
        
        availability = {}
        
        for tool_name, tool_path in self.tool_paths.items():
            if Path(tool_path).exists():
                availability[tool_name] = True
                self.girly_print(f"✅ {tool_name}: พร้อมใช้งาน", "SUCCESS", "✅")
            else:
                availability[tool_name] = False
                self.girly_print(f"❌ {tool_name}: ไม่พบไฟล์", "WARNING", "⚠️")
        
        return availability

    async def run_private_viewer(self, target: str, use_lightweight: bool = False) -> Dict[str, Any]:
        """
        👁️ เรียกใช้ Instagram Private Viewer
        
        Args:
            target: Instagram username
            use_lightweight: ใช้เวอร์ชัน lightweight หรือไม่
            
        Returns:
            ผลลัพธ์จาก Private Viewer
        """
        tool_name = 'lightweight_viewer' if use_lightweight else 'private_viewer'
        tool_path = self.tool_paths[tool_name]
        
        self.girly_print(f"👁️ เริ่มการโจมตี Private Viewer ต่อ @{target}...", "INFO", "🎯")
        
        try:
            # Run the private viewer tool
            result = subprocess.run([
                sys.executable, tool_path, '--target', target, '--auto'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.girly_print("✅ Private Viewer เสร็จสิ้น!", "SUCCESS", "👁️")
                
                # Try to load results from output files
                result_files = list(Path('.').glob(f'instagram_*{target}*.json'))
                if result_files:
                    latest_file = max(result_files, key=lambda f: f.stat().st_mtime)
                    
                    with open(latest_file, 'r') as f:
                        viewer_results = json.load(f)
                    
                    self.results['private_viewer_results'] = viewer_results
                    return viewer_results
                else:
                    # Parse output for results
                    return {'status': 'completed', 'output': result.stdout}
            else:
                self.girly_print(f"⚠️ Private Viewer ล้มเหลว: {result.stderr}", "WARNING", "⚠️")
                return {'status': 'failed', 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            self.girly_print("⏰ Private Viewer หมดเวลา", "WARNING", "⏰")
            return {'status': 'timeout'}
        except Exception as e:
            self.girly_print(f"❌ ข้อผิดพลาด Private Viewer: {str(e)}", "ERROR", "❌")
            return {'status': 'error', 'message': str(e)}

    async def run_osint_analysis(self, target: str) -> Dict[str, Any]:
        """
        🔍 เรียกใช้ OSINT Analysis
        
        Args:
            target: Instagram username
            
        Returns:
            ผลลัพธ์จาก OSINT
        """
        self.girly_print(f"🔍 เริ่ม OSINT Analysis ต่อ @{target}...", "INFO", "🕵️")
        
        try:
            # Run OSINT tool
            result = subprocess.run([
                sys.executable, self.tool_paths['osint_tool'], '--target', target, '--auto'
            ], capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                self.girly_print("✅ OSINT Analysis เสร็จสิ้น!", "SUCCESS", "🔍")
                
                # Load OSINT results
                osint_files = list(Path('.').glob(f'osint_results_{target}*.json'))
                if osint_files:
                    latest_file = max(osint_files, key=lambda f: f.stat().st_mtime)
                    
                    with open(latest_file, 'r') as f:
                        osint_results = json.load(f)
                    
                    self.results['osint_results'] = osint_results
                    return osint_results
                else:
                    return {'status': 'completed', 'output': result.stdout}
            else:
                self.girly_print(f"⚠️ OSINT Analysis ล้มเหลว: {result.stderr}", "WARNING", "⚠️")
                return {'status': 'failed', 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            self.girly_print("⏰ OSINT Analysis หมดเวลา", "WARNING", "⏰")
            return {'status': 'timeout'}
        except Exception as e:
            self.girly_print(f"❌ ข้อผิดพลาด OSINT: {str(e)}", "ERROR", "❌")
            return {'status': 'error', 'message': str(e)}

    async def run_cookie_harvester(self, target: str) -> Dict[str, Any]:
        """
        🍪 เรียกใช้ Cookie Harvester
        
        Args:
            target: Instagram username
            
        Returns:
            ผลลัพธ์จาก Cookie Harvester
        """
        self.girly_print(f"🍪 เริ่ม Cookie Harvesting ต่อ @{target}...", "INFO", "🍯")
        
        try:
            # Run cookie harvester
            result = subprocess.run([
                sys.executable, self.tool_paths['cookie_harvester'], '--target', target
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.girly_print("✅ Cookie Harvesting เสร็จสิ้น!", "SUCCESS", "🍪")
                
                # Load cookie results
                cookie_files = list(Path('.').glob('harvested_cookies_*.json'))
                if cookie_files:
                    latest_file = max(cookie_files, key=lambda f: f.stat().st_mtime)
                    
                    with open(latest_file, 'r') as f:
                        cookie_results = json.load(f)
                    
                    self.results['cookie_harvest_results'] = cookie_results
                    return cookie_results
                else:
                    return {'status': 'completed', 'output': result.stdout}
            else:
                self.girly_print(f"⚠️ Cookie Harvesting ล้มเหลว: {result.stderr}", "WARNING", "⚠️")
                return {'status': 'failed', 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            self.girly_print("⏰ Cookie Harvesting หมดเวลา", "WARNING", "⏰")
            return {'status': 'timeout'}
        except Exception as e:
            self.girly_print(f"❌ ข้อผิดพลาด Cookie Harvester: {str(e)}", "ERROR", "❌")
            return {'status': 'error', 'message': str(e)}

    async def analyze_discovered_images(self, image_urls: List[str]) -> List[Dict[str, Any]]:
        """
        🖼️ วิเคราะห์รูปภาพที่ค้นพบด้วย AI
        
        Args:
            image_urls: รายการ URL รูปภาพ
            
        Returns:
            รายการผลการวิเคราะห์รูปภาพ
        """
        if not image_urls:
            return []
            
        self.girly_print(f"🖼️ เริ่มวิเคราะห์รูปภาพ {len(image_urls)} ภาพ...", "INFO", "🔍")
        
        image_results = []
        
        # Import the image analyzer
        try:
            sys.path.append('.')
            from instagram_image_analyzer_2025 import InstagramImageAnalyzer
            
            analyzer = InstagramImageAnalyzer()
            
            for i, url in enumerate(image_urls[:5], 1):  # Limit to 5 images
                self.girly_print(f"📊 วิเคราะห์รูปภาพ {i}/{min(len(image_urls), 5)}: {url[:50]}...", "INFO", "🖼️")
                
                try:
                    result = analyzer.analyze_from_url(url)
                    if result.get('success'):
                        image_results.append({
                            'url': url,
                            'analysis': result,
                            'risk_assessment': result.get('overall_assessment', {})
                        })
                        
                        self.girly_print(f"✅ วิเคราะห์รูปภาพสำเร็จ: Risk {result.get('overall_assessment', {}).get('total_risk_level', 'Unknown')}", "SUCCESS", "🖼️")
                    else:
                        self.girly_print(f"⚠️ วิเคราะห์รูปภาพล้มเหลว: {result.get('error', 'Unknown error')}", "WARNING", "⚠️")
                        
                except Exception as e:
                    self.girly_print(f"❌ ข้อผิดพลาดวิเคราะห์รูปภาพ: {str(e)}", "ERROR", "❌")
                
                # Rate limiting
                await asyncio.sleep(2)
                
        except ImportError:
            self.girly_print("⚠️ ไม่สามารถนำเข้า Image Analyzer ได้", "WARNING", "⚠️")
            return []
        except Exception as e:
            self.girly_print(f"❌ ข้อผิดพลาด Image Analysis: {str(e)}", "ERROR", "❌")
            return []
        
        self.results['image_analysis_results'] = image_results
        return image_results

    def extract_image_urls_from_results(self) -> List[str]:
        """
        🔗 ดึง URL รูปภาพจากผลลัพธ์ทั้งหมด
        
        Returns:
            รายการ URL รูปภาพ
        """
        image_urls = []
        
        # From private viewer results
        if self.results.get('private_viewer_results'):
            viewer_data = self.results['private_viewer_results']
            
            # Profile picture
            if 'profile_pic_url' in viewer_data:
                image_urls.append(viewer_data['profile_pic_url'])
            
            # Post images
            if 'posts' in viewer_data:
                for post in viewer_data['posts'][:3]:  # Limit to 3 posts
                    if 'image_url' in post:
                        image_urls.append(post['image_url'])
                    elif 'media_url' in post:
                        image_urls.append(post['media_url'])
        
        # From OSINT results (if they contain image URLs)
        if self.results.get('osint_results'):
            osint_data = self.results['osint_results']
            
            # Look for image URLs in OSINT data
            for platform, data in osint_data.items():
                if isinstance(data, dict) and 'profile_image' in data:
                    image_urls.append(data['profile_image'])
        
        # Remove duplicates
        image_urls = list(set(image_urls))
        
        self.girly_print(f"🔗 ค้นพบ URL รูปภาพ {len(image_urls)} รายการ", "INFO", "🖼️")
        
        return image_urls

    def generate_intelligence_summary(self) -> List[str]:
        """
        🧠 สร้างสรุปข้อมูลข่าวกรองที่ค้นพบ
        
        Returns:
            รายการข้อมูลข่าวกรอง
        """
        intelligence = []
        
        # From private viewer
        if self.results.get('private_viewer_results'):
            viewer_data = self.results['private_viewer_results']
            
            if 'success_methods' in viewer_data:
                successful_methods = [method for method, success in viewer_data['success_methods'].items() if success]
                if successful_methods:
                    intelligence.append(f"Private data accessed via: {', '.join(successful_methods)}")
            
            if 'cached_data' in viewer_data and viewer_data['cached_data']:
                intelligence.append("Cached Instagram data discovered")
            
            if 'posts_count' in viewer_data:
                intelligence.append(f"Total posts: {viewer_data['posts_count']}")
        
        # From OSINT
        if self.results.get('osint_results'):
            osint_data = self.results['osint_results']
            
            related_profiles = 0
            platforms_found = []
            
            for platform, data in osint_data.items():
                if isinstance(data, dict) and data.get('found'):
                    platforms_found.append(platform)
                    
                if isinstance(data, list):
                    related_profiles += len(data)
            
            if platforms_found:
                intelligence.append(f"Found on platforms: {', '.join(platforms_found)}")
            
            if related_profiles > 0:
                intelligence.append(f"Related profiles discovered: {related_profiles}")
        
        # From image analysis
        if self.results.get('image_analysis_results'):
            high_risk_images = 0
            faces_detected = 0
            ai_generated = 0
            
            for img_result in self.results['image_analysis_results']:
                risk_level = img_result.get('risk_assessment', {}).get('total_risk_level', 'Low')
                if risk_level == 'High':
                    high_risk_images += 1
                
                analysis = img_result.get('analysis', {})
                if analysis.get('face_analysis', {}).get('has_faces'):
                    faces_detected += 1
                
                if analysis.get('deepfake_indicators', {}).get('likely_ai_generated'):
                    ai_generated += 1
            
            if high_risk_images > 0:
                intelligence.append(f"High-risk images detected: {high_risk_images}")
            
            if faces_detected > 0:
                intelligence.append(f"Images with faces: {faces_detected}")
            
            if ai_generated > 0:
                intelligence.append(f"Possible AI-generated images: {ai_generated}")
        
        # From cookies
        if self.results.get('cookie_harvest_results'):
            cookie_data = self.results['cookie_harvest_results']
            
            if 'cookies_harvested' in cookie_data and cookie_data['cookies_harvested'] > 0:
                intelligence.append(f"Cookies harvested: {cookie_data['cookies_harvested']}")
        
        self.results['discovered_intelligence'] = intelligence
        return intelligence

    def calculate_overall_risk_assessment(self) -> Dict[str, Any]:
        """
        📊 คำนวณการประเมินความเสี่ยงโดยรวม
        
        Returns:
            การประเมินความเสี่ยงโดยรวม
        """
        risk_factors = []
        success_indicators = []
        
        # Private viewer success
        if self.results.get('private_viewer_results'):
            viewer_data = self.results['private_viewer_results']
            if 'success_methods' in viewer_data:
                successful_methods = [method for method, success in viewer_data['success_methods'].items() if success]
                if successful_methods:
                    success_indicators.append("Private data accessible")
                    risk_factors.append("Privacy breach possible")
        
        # OSINT exposure
        if self.results.get('osint_results'):
            osint_data = self.results['osint_results']
            platforms_found = sum(1 for platform, data in osint_data.items() 
                                if isinstance(data, dict) and data.get('found'))
            
            if platforms_found >= 3:
                risk_factors.append("High digital footprint")
                success_indicators.append(f"Found on {platforms_found} platforms")
            elif platforms_found >= 1:
                success_indicators.append(f"Found on {platforms_found} platform(s)")
        
        # Image analysis risks
        if self.results.get('image_analysis_results'):
            high_risk_count = sum(1 for img in self.results['image_analysis_results'] 
                                if img.get('risk_assessment', {}).get('total_risk_level') == 'High')
            
            if high_risk_count > 0:
                risk_factors.append(f"Suspicious images ({high_risk_count})")
        
        # Overall assessment
        total_risk_score = len(risk_factors)
        total_success_score = len(success_indicators)
        
        if total_risk_score >= 3:
            overall_risk = "CRITICAL"
        elif total_risk_score >= 2:
            overall_risk = "HIGH"
        elif total_risk_score >= 1:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "LOW"
        
        if total_success_score >= 3:
            recon_success = "EXCELLENT"
        elif total_success_score >= 2:
            recon_success = "GOOD"
        elif total_success_score >= 1:
            recon_success = "PARTIAL"
        else:
            recon_success = "LIMITED"
        
        assessment = {
            'overall_risk_level': overall_risk,
            'reconnaissance_success': recon_success,
            'risk_factors': risk_factors,
            'success_indicators': success_indicators,
            'total_risk_score': total_risk_score,
            'total_success_score': total_success_score
        }
        
        self.results['overall_assessment'] = assessment
        return assessment

    async def full_reconnaissance(self, target: str, options: Dict[str, bool] = None) -> Dict[str, Any]:
        """
        🎯 การทำ reconnaissance แบบเต็มรูปแบบ
        
        Args:
            target: Instagram username
            options: ตัวเลือกสำหรับเครื่องมือต่างๆ
            
        Returns:
            ผลลัพธ์การ reconnaissance ทั้งหมด
        """
        if options is None:
            options = {
                'private_viewer': True,
                'lightweight_mode': True,
                'osint_analysis': True,
                'cookie_harvesting': False,  # Disabled by default for safety
                'image_analysis': True
            }
        
        self.results['target'] = target
        
        self.girly_print(f"🎯 เริ่ม Full Reconnaissance ต่อ @{target}", "INFO", "🚀")
        self.girly_print("⚠️ การดำเนินการนี้อาจใช้เวลา 5-10 นาที", "WARNING", "⏰")
        
        # Check tool availability
        available_tools = self.check_tool_availability()
        
        # Phase 1: Private Viewer (if enabled and available)
        if options.get('private_viewer') and available_tools.get('lightweight_viewer', False):
            self.girly_print("🔍 Phase 1: Private Viewer Analysis", "INFO", "1️⃣")
            await self.run_private_viewer(target, use_lightweight=options.get('lightweight_mode', True))
            await asyncio.sleep(2)
        
        # Phase 2: OSINT Analysis (if enabled and available)
        if options.get('osint_analysis') and available_tools.get('osint_tool', False):
            self.girly_print("🕵️ Phase 2: OSINT Analysis", "INFO", "2️⃣")
            await self.run_osint_analysis(target)
            await asyncio.sleep(2)
        
        # Phase 3: Cookie Harvesting (if enabled and available)
        if options.get('cookie_harvesting') and available_tools.get('cookie_harvester', False):
            self.girly_print("🍪 Phase 3: Cookie Harvesting", "INFO", "3️⃣")
            await self.run_cookie_harvester(target)
            await asyncio.sleep(2)
        
        # Phase 4: Image Analysis (if enabled)
        if options.get('image_analysis'):
            self.girly_print("🖼️ Phase 4: Image Analysis", "INFO", "4️⃣")
            
            # Extract image URLs from previous results
            image_urls = self.extract_image_urls_from_results()
            
            if image_urls:
                await self.analyze_discovered_images(image_urls)
            else:
                self.girly_print("📷 ไม่พบ URL รูปภาพสำหรับวิเคราะห์", "INFO", "📷")
        
        # Phase 5: Intelligence Analysis
        self.girly_print("🧠 Phase 5: Intelligence Analysis", "INFO", "5️⃣")
        
        # Generate intelligence summary
        intelligence = self.generate_intelligence_summary()
        
        # Calculate overall assessment
        assessment = self.calculate_overall_risk_assessment()
        
        # Save comprehensive results
        timestamp = int(time.time())
        result_filename = self.output_dir / f"ultimate_recon_{target}_{timestamp}.json"
        
        with open(result_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str, ensure_ascii=False)
        
        self.girly_print(f"✅ Full Reconnaissance เสร็จสิ้น!", "SUCCESS", "🎉")
        self.girly_print(f"📁 ผลลัพธ์ถูกบันทึกที่: {result_filename}", "INFO", "💾")
        
        return self.results

    def generate_comprehensive_report(self) -> str:
        """
        📊 สร้างรายงานแบบครอบคลุม
        
        Returns:
            รายงานแบบ text ที่สมบูรณ์
        """
        target = self.results.get('target', 'Unknown')
        timestamp = self.results.get('timestamp', 'Unknown')
        
        report = f"""
🕵️💕 ULTIMATE INSTAGRAM RECONNAISSANCE SUITE 2025 - COMPREHENSIVE REPORT 💕🕵️
{'='*90}

🎯 TARGET INFORMATION
Target: @{target}
Analysis Time: {timestamp}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*90}
"""

        # Overall Assessment
        if self.results.get('overall_assessment'):
            assessment = self.results['overall_assessment']
            report += f"""
📊 OVERALL ASSESSMENT
Risk Level: {assessment.get('overall_risk_level', 'Unknown')}
Reconnaissance Success: {assessment.get('reconnaissance_success', 'Unknown')}
Risk Score: {assessment.get('total_risk_score', 0)}/10
Success Score: {assessment.get('total_success_score', 0)}/10

🔴 Risk Factors:
"""
            for factor in assessment.get('risk_factors', []):
                report += f"  • {factor}\n"
            
            report += f"\n✅ Success Indicators:\n"
            for indicator in assessment.get('success_indicators', []):
                report += f"  • {indicator}\n"
        
        # Intelligence Summary
        if self.results.get('discovered_intelligence'):
            report += f"\n🧠 DISCOVERED INTELLIGENCE\n"
            for intel in self.results['discovered_intelligence']:
                report += f"  • {intel}\n"
        
        # Private Viewer Results
        if self.results.get('private_viewer_results'):
            report += f"\n👁️ PRIVATE VIEWER ANALYSIS\n"
            viewer_data = self.results['private_viewer_results']
            
            if 'success_methods' in viewer_data:
                successful = [method for method, success in viewer_data['success_methods'].items() if success]
                failed = [method for method, success in viewer_data['success_methods'].items() if not success]
                
                if successful:
                    report += f"  ✅ Successful Methods: {', '.join(successful)}\n"
                if failed:
                    report += f"  ❌ Failed Methods: {', '.join(failed)}\n"
            
            if 'posts_count' in viewer_data:
                report += f"  📊 Posts Found: {viewer_data['posts_count']}\n"
        
        # OSINT Results
        if self.results.get('osint_results'):
            report += f"\n🔍 OSINT ANALYSIS RESULTS\n"
            osint_data = self.results['osint_results']
            
            platforms_found = []
            for platform, data in osint_data.items():
                if isinstance(data, dict) and data.get('found'):
                    platforms_found.append(platform)
            
            if platforms_found:
                report += f"  🌐 Platforms Found: {', '.join(platforms_found)}\n"
            else:
                report += f"  📭 No additional platforms found\n"
        
        # Image Analysis Results
        if self.results.get('image_analysis_results'):
            report += f"\n🖼️ IMAGE ANALYSIS RESULTS\n"
            
            total_images = len(self.results['image_analysis_results'])
            high_risk = sum(1 for img in self.results['image_analysis_results'] 
                          if img.get('risk_assessment', {}).get('total_risk_level') == 'High')
            faces_detected = sum(1 for img in self.results['image_analysis_results'] 
                               if img.get('analysis', {}).get('face_analysis', {}).get('has_faces'))
            
            report += f"  📊 Total Images Analyzed: {total_images}\n"
            report += f"  ⚠️ High Risk Images: {high_risk}\n"
            report += f"  👤 Images with Faces: {faces_detected}\n"
            
            # Details for high-risk images
            if high_risk > 0:
                report += f"\n  🚨 HIGH RISK IMAGE DETAILS:\n"
                for i, img_result in enumerate(self.results['image_analysis_results'], 1):
                    if img_result.get('risk_assessment', {}).get('total_risk_level') == 'High':
                        url = img_result.get('url', 'Unknown')[:60]
                        risks = img_result.get('risk_assessment', {}).get('risk_factors', [])
                        report += f"    {i}. {url}...\n"
                        for risk in risks:
                            report += f"       - {risk}\n"
        
        # Cookie Harvesting Results
        if self.results.get('cookie_harvest_results'):
            report += f"\n🍪 COOKIE HARVESTING RESULTS\n"
            cookie_data = self.results['cookie_harvest_results']
            
            cookies_count = cookie_data.get('cookies_harvested', 0)
            report += f"  🍯 Cookies Harvested: {cookies_count}\n"
            
            if cookies_count > 0:
                report += f"  ⚠️ Session data may be accessible\n"
        
        report += f"""
{'='*90}
⚠️ SECURITY RECOMMENDATIONS

1. 🔒 Enable two-factor authentication on all accounts
2. 🔐 Review privacy settings on all social media platforms  
3. 👀 Monitor for unauthorized access attempts
4. 🧹 Regular security audits of online presence
5. 📱 Use privacy-focused browsers and VPNs

{'='*90}
💖 Generated with love by น้องจิน's Ultimate Instagram Reconnaissance Suite 2025
🤖 Powered by Advanced AI Analysis & Multi-Tool Integration
👻 For educational and authorized security research only!
⚠️ Always respect privacy and follow applicable laws
🔒 Use this information responsibly for legitimate security purposes only
{'='*90}
"""

        return report


def main():
    """Enhanced main function with comprehensive reconnaissance options"""
    print(GIRLY_BANNER)
    
    suite = UltimateInstagramReconSuite()
    
    # Check tool availability
    available_tools = suite.check_tool_availability()
    
    print("\n🔧 TOOL AVAILABILITY STATUS:")
    for tool, available in available_tools.items():
        status = "✅ Available" if available else "❌ Missing"
        print(f"  • {tool.replace('_', ' ').title()}: {status}")
    
    while True:
        print("\n💖 ULTIMATE INSTAGRAM RECONNAISSANCE SUITE 2025 MENU 💖")
        print("1. 🎯 Full Reconnaissance (All Tools)")
        print("2. 🕵️ Custom Reconnaissance (Select Tools)")
        print("3. 👁️ Private Viewer Only")
        print("4. 🔍 OSINT Analysis Only")
        print("5. 🖼️ Image Analysis Only")
        print("6. 📊 View Previous Reports")
        print("7. 🛠️ Tool Management")
        print("0. 💔 Exit")
        
        choice = input("\n💖 เลือกเมนู (0-7): ").strip()
        
        try:
            if choice == '1':
                target = input("🎯 Target Instagram username: ").strip()
                
                if target:
                    print("\n🚀 Starting Full Reconnaissance...")
                    print("⚠️ This will run all available tools and may take 5-10 minutes")
                    
                    confirm = input("Continue? (y/n): ").strip().lower()
                    if confirm in ['y', 'yes']:
                        # Run full reconnaissance
                        results = asyncio.run(suite.full_reconnaissance(target))
                        
                        # Show comprehensive report
                        print(suite.generate_comprehensive_report())
                        
                        # Offer to save report
                        save_report = input("\n💾 Save comprehensive report as text file? (y/n): ").strip().lower()
                        if save_report in ['y', 'yes']:
                            timestamp = int(time.time())
                            report_file = suite.output_dir / f"comprehensive_report_{target}_{timestamp}.txt"
                            
                            with open(report_file, 'w', encoding='utf-8') as f:
                                f.write(suite.generate_comprehensive_report())
                            print(f"✅ Report saved: {report_file}")
            
            elif choice == '2':
                target = input("🎯 Target Instagram username: ").strip()
                
                if target:
                    print("\n🛠️ CUSTOM RECONNAISSANCE OPTIONS")
                    
                    options = {}
                    options['private_viewer'] = input("👁️ Enable Private Viewer? (y/n): ").strip().lower() in ['y', 'yes']
                    options['lightweight_mode'] = input("⚡ Use Lightweight mode? (y/n): ").strip().lower() in ['y', 'yes']
                    options['osint_analysis'] = input("🔍 Enable OSINT Analysis? (y/n): ").strip().lower() in ['y', 'yes']
                    options['cookie_harvesting'] = input("🍪 Enable Cookie Harvesting? (y/n): ").strip().lower() in ['y', 'yes']
                    options['image_analysis'] = input("🖼️ Enable Image Analysis? (y/n): ").strip().lower() in ['y', 'yes']
                    
                    print(f"\n🚀 Starting Custom Reconnaissance with selected options...")
                    
                    # Run custom reconnaissance
                    results = asyncio.run(suite.full_reconnaissance(target, options))
                    
                    # Show report
                    print(suite.generate_comprehensive_report())
            
            elif choice == '3':
                target = input("👁️ Target for Private Viewer: ").strip()
                
                if target:
                    use_lightweight = input("⚡ Use Lightweight mode? (y/n): ").strip().lower() in ['y', 'yes']
                    
                    suite.results['target'] = target
                    results = asyncio.run(suite.run_private_viewer(target, use_lightweight))
                    
                    print(f"\n📊 Private Viewer Results: {results.get('status', 'Unknown')}")
            
            elif choice == '4':
                target = input("🔍 Target for OSINT Analysis: ").strip()
                
                if target:
                    suite.results['target'] = target
                    results = asyncio.run(suite.run_osint_analysis(target))
                    
                    print(f"\n📊 OSINT Results: {results.get('status', 'Unknown')}")
            
            elif choice == '5':
                image_urls_input = input("🖼️ Image URLs (comma-separated): ").strip()
                
                if image_urls_input:
                    image_urls = [url.strip() for url in image_urls_input.split(',') if url.strip()]
                    
                    print(f"\n🚀 Analyzing {len(image_urls)} images...")
                    results = asyncio.run(suite.analyze_discovered_images(image_urls))
                    
                    print(f"\n📊 Analyzed {len(results)} images successfully")
                    for result in results:
                        risk = result.get('risk_assessment', {}).get('total_risk_level', 'Unknown')
                        print(f"  • {result['url'][:50]}... - Risk: {risk}")
            
            elif choice == '6':
                print("📊 PREVIOUS REPORTS")
                
                report_files = list(suite.output_dir.glob('ultimate_recon_*.json'))
                if report_files:
                    print(f"Found {len(report_files)} previous reports:")
                    for i, file in enumerate(report_files[-5:], 1):  # Show last 5
                        mtime = datetime.fromtimestamp(file.stat().st_mtime)
                        print(f"{i}. {file.name} ({mtime.strftime('%Y-%m-%d %H:%M')})")
                    
                    file_choice = input("Enter number to view (or 0 to go back): ").strip()
                    try:
                        file_idx = int(file_choice) - 1
                        if 0 <= file_idx < len(report_files[-5:]):
                            selected_file = report_files[-(5-file_idx)]
                            
                            with open(selected_file, 'r') as f:
                                old_results = json.load(f)
                            
                            suite.results = old_results
                            print(suite.generate_comprehensive_report())
                    except (ValueError, IndexError):
                        if file_choice != '0':
                            print("❌ Invalid selection")
                else:
                    print("No previous reports found")
            
            elif choice == '7':
                print("🛠️ TOOL MANAGEMENT")
                print("1. 🔍 Check Tool Status")
                print("2. 📦 Install Missing Dependencies")
                print("3. 🔄 Update Tools")
                
                tool_choice = input("Choose option (1-3): ").strip()
                
                if tool_choice == '1':
                    available_tools = suite.check_tool_availability()
                elif tool_choice == '2':
                    print("📦 Installing missing dependencies...")
                    # Here you could add package installation logic
                    print("⚠️ Manual installation may be required for some packages")
                elif tool_choice == '3':
                    print("🔄 Tool update functionality coming soon...")
            
            elif choice == '0':
                print("👋 บาย! ขอบคุณที่ใช้ Ultimate Instagram Reconnaissance Suite 2025 นะคะ ♥️")
                break
                
            else:
                print("❌ เลือกเมนูให้ถูกนะคะ")
                
        except KeyboardInterrupt:
            print("\n⚠️ หยุดการทำงาน")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
