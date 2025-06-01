#!/usr/bin/env python3
"""
🖼️💕 INSTAGRAM IMAGE ANALYZER 2025 💕🖼️
=======================================
- วิเคราะห์รูปภาพ Instagram (จาก URL)
- ดึงข้อมูลจากรูป (metadata + ai analysis)
- สำหรับเสริม Instagram Private Viewer
- เชื่อมกับ Ultimate Instagram Toolkit

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01
For: Educational & Security Research Only!
"""

import requests
import json
import os
import time
import re
import random
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import base64
from PIL import Image
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

# === GIRLY CONFIG ===
GIRLY_BANNER = """
💋💖🖼️ INSTAGRAM IMAGE ANALYZER 2025 🖼️💖💋
        โดย น้องจิน - วิเคราะห์รูปภาพสุดเทพ! ♥️
      เห็นทุกอย่างในรูป + Metadata + Hidden Info
"""

class InstagramImageAnalyzer:
    """
    🖼️ Instagram Image Analyzer - วิเคราะห์รูปภาพจาก URL หรือไฟล์
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        
        # Results storage
        self.results = {
            'image_url': '',
            'download_time': '',
            'image_data': {},
            'metadata': {},
            'analysis': {},
            'related_urls': [],
            'profile_hints': []
        }
        
        # Create output directory
        self.output_dir = Path('./analyzed_images')
        self.output_dir.mkdir(exist_ok=True)
        
        self.girly_print("🖼️ Instagram Image Analyzer ถูกเตรียมพร้อม!", "INFO", "🚀")

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

    def download_image(self, image_url: str) -> Optional[BytesIO]:
        """
        💾 ดาวน์โหลดรูปจาก URL
        
        Args:
            image_url: URL ของรูปภาพ
            
        Returns:
            BytesIO object ของรูปภาพ หรือ None ถ้าล้มเหลว
        """
        self.girly_print(f"⬇️ กำลังดาวน์โหลดรูปภาพ: {image_url[:60]}...", "INFO", "🔽")
        
        try:
            response = requests.get(image_url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                self.girly_print(f"✅ ดาวน์โหลดสำเร็จ! ขนาด: {len(response.content):,} bytes", "SUCCESS", "📥")
                
                self.results['image_url'] = image_url
                self.results['download_time'] = datetime.now().isoformat()
                
                # เก็บข้อมูลพื้นฐาน
                content_type = response.headers.get('Content-Type', '')
                self.results['image_data'] = {
                    'size_bytes': len(response.content),
                    'content_type': content_type,
                    'last_modified': response.headers.get('Last-Modified', ''),
                    'etag': response.headers.get('ETag', ''),
                    'server': response.headers.get('Server', '')
                }
                
                return BytesIO(response.content)
            else:
                self.girly_print(f"❌ ดาวน์โหลดล้มเหลว: HTTP {response.status_code}", "ERROR", "⛔")
                return None
                
        except Exception as e:
            self.girly_print(f"❌ เกิดข้อผิดพลาด: {str(e)}", "ERROR", "⛔")
            return None

    def extract_metadata(self, image_data: BytesIO) -> Dict[str, Any]:
        """
        🔍 ดึงข้อมูล metadata จากรูปภาพ
        
        Args:
            image_data: BytesIO object ของรูปภาพ
            
        Returns:
            Dictionary ของ metadata
        """
        self.girly_print("🔎 กำลังวิเคราะห์ metadata ของรูปภาพ...", "INFO", "🔍")
        
        metadata = {}
        
        try:
            with Image.open(image_data) as img:
                # ข้อมูลพื้นฐาน
                metadata['format'] = img.format
                metadata['mode'] = img.mode
                metadata['size'] = img.size
                width, height = img.size
                metadata['resolution'] = f"{width}x{height}"
                metadata['aspect_ratio'] = round(width / height, 2) if height != 0 else 0
                
                # EXIF data (ถ้ามี)
                exif_data = {}
                if hasattr(img, '_getexif') and img._getexif():
                    exif = img._getexif()
                    
                    # EXIF tags mapping
                    exif_tags = {
                        271: 'Make',
                        272: 'Model',
                        306: 'DateTime',
                        36867: 'DateTimeOriginal',
                        33432: 'Copyright',
                        37385: 'Flash',
                        37386: 'FocalLength',
                        41728: 'FileSource',
                        41729: 'SceneType'
                    }
                    
                    for tag_id, value in exif.items():
                        tag = exif_tags.get(tag_id, str(tag_id))
                        exif_data[tag] = str(value)
                
                if exif_data:
                    metadata['exif'] = exif_data
                
                # ICC Profile (ถ้ามี)
                if 'icc_profile' in img.info:
                    metadata['has_icc_profile'] = True
                
                # สี dominant
                try:
                    if img.mode == 'RGB':
                        img = img.resize((100, 100))  # Resize for faster processing
                        colors = img.getcolors(10000)  # Get colors (max 10000)
                        if colors:
                            # Sort by count (most frequent first)
                            colors.sort(key=lambda x: x[0], reverse=True)
                            dominant = colors[0][1]
                            metadata['dominant_color'] = f"#{dominant[0]:02x}{dominant[1]:02x}{dominant[2]:02x}"
                            
                            # Color temperature estimation
                            r, g, b = dominant
                            temperature = (r * 3 + g * 2 + b) / 6  # Simple estimation
                            if temperature > 170:
                                metadata['color_tone'] = 'Bright'
                            elif temperature > 85:
                                metadata['color_tone'] = 'Neutral' 
                            else:
                                metadata['color_tone'] = 'Dark'
                except:
                    pass
                
                self.girly_print(f"✅ วิเคราะห์ metadata สำเร็จ: {len(metadata)} fields", "SUCCESS", "📋")
                
                # เพิ่มเข้า results
                self.results['metadata'] = metadata
                
                return metadata
                
        except Exception as e:
            self.girly_print(f"⚠️ ไม่สามารถอ่าน metadata: {str(e)}", "WARNING", "⚠️")
            return {}

    def analyze_image_content(self, image_data: BytesIO) -> Dict[str, Any]:
        """
        🧠 วิเคราะห์เนื้อหาของรูปภาพ
        
        Args:
            image_data: BytesIO object ของรูปภาพ
            
        Returns:
            Dictionary ของผลการวิเคราะห์
        """
        self.girly_print("🧠 กำลังวิเคราะห์เนื้อหารูปภาพ...", "INFO", "🔍")
        
        analysis = {}
        
        try:
            with Image.open(image_data) as img:
                # Reposition pointer to start
                image_data.seek(0)
                
                # ขนาดรูป
                width, height = img.size
                
                # Scene analysis
                if width >= 1080 or height >= 1080:
                    analysis['quality'] = 'High Resolution'
                elif width >= 720 or height >= 720:
                    analysis['quality'] = 'Medium Resolution'
                else:
                    analysis['quality'] = 'Low Resolution'
                
                # Instagram specific analysis
                if width == height:
                    analysis['instagram_format'] = 'Square'
                elif width > height:
                    analysis['instagram_format'] = 'Landscape'
                else:
                    analysis['instagram_format'] = 'Portrait'
                
                # เช็คว่าใช่ screenshot หรือไม่
                if width in [1080, 1125, 1170, 1242, 1284, 1440, 2220, 2340, 2400, 2532, 2778, 2880] and \
                   height in [1920, 2220, 2340, 2400, 2532, 2778, 2880]:
                    analysis['likely_screenshot'] = True
                
                # Instagram filter estimation
                # This is simplified - real filter detection would need more advanced analysis
                img_array = img.resize((10, 10))  # Small sample for filter analysis
                samples = list(img_array.getdata())
                
                if len(samples) > 0:
                    # Average color
                    if img.mode == 'RGB':
                        rgb_avg = [sum(color[i] for color in samples) / len(samples) for i in range(3)]
                        
                        # Very simple filter guessing based on color balance
                        r, g, b = rgb_avg
                        
                        if r > g + 20 and r > b + 20:
                            analysis['possible_filter'] = 'Warm (possibly Valencia or Lo-Fi)'
                        elif b > r + 20 and b > g + 20:
                            analysis['possible_filter'] = 'Cool (possibly Moon or Perpetua)'
                        elif r > 200 and g > 200 and b > 200:
                            analysis['possible_filter'] = 'Bright (possibly Gingham or Lark)'
                        elif r < 100 and g < 100 and b < 100:
                            analysis['possible_filter'] = 'Dark (possibly Inkwell or Willow)'
                        else:
                            analysis['possible_filter'] = 'Neutral (possibly Normal or Clarendon)'
                    
                # เช็คการแต่งรูป
                # Full editing detection would need AI, but we can make simple estimations
                if img.format == 'JPEG':
                    # Check for re-compression artifacts
                    image_data.seek(0)
                    img_bytes = image_data.getvalue()
                    
                    # Using compression signatures to guess editing
                    # More advanced version would use proper compression forensics
                    editing_signs = 0
                    
                    # Check for Adobe Photoshop signature
                    if b'Photoshop' in img_bytes or b'Adobe' in img_bytes:
                        analysis['editing_software_hint'] = 'Adobe Photoshop'
                        editing_signs += 2
                    
                    # Check for other common editors
                    if b'GIMP' in img_bytes:
                        analysis['editing_software_hint'] = 'GIMP'
                        editing_signs += 2
                        
                    # Check quantization tables (simplified approach)
                    if img_bytes.count(b'\xff\xdb') >= 2:  # Multiple quantization tables
                        editing_signs += 1
                    
                    if editing_signs >= 2:
                        analysis['likely_edited'] = 'High probability'
                    elif editing_signs == 1:
                        analysis['likely_edited'] = 'Medium probability'
                    else:
                        analysis['likely_edited'] = 'Low probability'
                
                # Instagram profile insights
                insta_marks = 0
                
                # Check if dimensions match Instagram's preferred sizes
                if (width == 1080 and height in [1080, 1350, 608, 566]) or \
                   (height == 1080 and width in [1080, 1350, 608, 566]):
                    insta_marks += 1
                    analysis['instagram_optimized'] = True
                
                # Search for Instagram-specific compression patterns
                if b'Instagram' in image_data.getvalue():
                    insta_marks += 2
                    analysis['instagram_originated'] = True
                
                if insta_marks >= 2:
                    analysis['instagram_source'] = 'Very likely'
                elif insta_marks == 1:
                    analysis['instagram_source'] = 'Possible'
                else:
                    analysis['instagram_source'] = 'Unknown'
                
            self.girly_print(f"✅ วิเคราะห์เนื้อหารูปภาพสำเร็จ: {len(analysis)} insights", "SUCCESS", "🧠")
            
            # เพิ่มเข้า results
            self.results['analysis'] = analysis
            
            return analysis
            
        except Exception as e:
            self.girly_print(f"⚠️ ไม่สามารถวิเคราะห์รูปภาพ: {str(e)}", "WARNING", "⚠️")
            return {}

    def extract_instagram_profile_hints(self, image_url: str) -> List[str]:
        """
        👤 ดึงข้อมูลของโปรไฟล์ Instagram จาก URL รูปภาพ
        
        Args:
            image_url: URL ของรูปภาพ
            
        Returns:
            List ของ hints เกี่ยวกับโปรไฟล์
        """
        self.girly_print("👤 กำลังวิเคราะห์ความเชื่อมโยงกับโปรไฟล์...", "INFO", "🔍")
        
        hints = []
        
        try:
            # Extract username from URL
            username_patterns = [
                r'instagram\.com/([A-Za-z0-9._]+)/',
                r'instagram\.com/p/[A-Za-z0-9_-]+/\?taken-by=([A-Za-z0-9._]+)',
                r'instagram\.com/([A-Za-z0-9._]+)/p/'
            ]
            
            for pattern in username_patterns:
                matches = re.findall(pattern, image_url)
                if matches and len(matches) > 0:
                    username = matches[0]
                    if username not in ['p', 'explore', 'stories']:
                        hints.append(f"Likely Instagram username: {username}")
                        
                        # Add profile URL
                        self.results['related_urls'].append(f"https://www.instagram.com/{username}/")
            
            # Extract post ID
            post_patterns = [
                r'instagram\.com/p/([A-Za-z0-9_-]+)/',
                r'instagram\.com/reel/([A-Za-z0-9_-]+)/'
            ]
            
            for pattern in post_patterns:
                matches = re.findall(pattern, image_url)
                if matches and len(matches) > 0:
                    post_id = matches[0]
                    hints.append(f"Instagram post ID: {post_id}")
                    
                    # Add post URL
                    self.results['related_urls'].append(f"https://www.instagram.com/p/{post_id}/")
            
            # Extract CDN info from URL
            if 'cdninstagram.com' in image_url or 'fbcdn.net' in image_url:
                hints.append("Image stored on Instagram CDN - official Instagram image")
                
                # Check if it's a profile picture
                if 'profile_pic' in image_url or '/t51.2885-19/' in image_url:
                    hints.append("This appears to be a profile picture")
                elif '/t51.2885-15/' in image_url:
                    hints.append("This appears to be a post image")
            
            self.girly_print(f"✅ การวิเคราะห์โปรไฟล์เสร็จสิ้น: พบ {len(hints)} hints", "SUCCESS", "👤")
            
            # เพิ่มเข้า results
            self.results['profile_hints'] = hints
            
            return hints
            
        except Exception as e:
            self.girly_print(f"⚠️ ไม่สามารถวิเคราะห์ความเชื่อมโยงกับโปรไฟล์: {str(e)}", "WARNING", "⚠️")
            return []

    def generate_image_signature(self, image_data: BytesIO) -> str:
        """
        🔐 สร้าง unique signature สำหรับรูปภาพ
        
        Args:
            image_data: BytesIO object ของรูปภาพ
            
        Returns:
            Image signature string
        """
        try:
            # Reset pointer
            image_data.seek(0)
            data = image_data.read()
            
            # Generate both MD5 and SHA256
            md5_hash = hashlib.md5(data).hexdigest()
            sha256_hash = hashlib.sha256(data).hexdigest()
            
            return f"MD5: {md5_hash}, SHA256: {sha256_hash[:16]}"
            
        except Exception as e:
            self.girly_print(f"⚠️ ไม่สามารถสร้าง signature: {str(e)}", "WARNING", "⚠️")
            return "Unknown"

    def find_similar_images(self, image_url: str) -> List[str]:
        """
        🔍 ค้นหารูปภาพที่คล้ายกันจาก search engines
        
        Args:
            image_url: URL รูปภาพที่ต้องการหา
            
        Returns:
            List ของ URLs ที่อาจมีรูปคล้ายกัน
        """
        self.girly_print("🔍 กำลังค้นหารูปภาพที่คล้ายกัน...", "INFO", "🔎")
        
        similar_image_links = []
        
        # Encode URL for search engines
        encoded_url = urllib.parse.quote_plus(image_url) if 'urllib' in globals() else image_url
        
        # Search engine reverse image URLs
        reverse_image_urls = [
            f"https://lens.google.com/uploadbyurl?url={encoded_url}",
            f"https://yandex.com/images/search?url={encoded_url}&rpt=imageview",
            f"https://www.bing.com/images/search?view=detailv2&iss=sbi&q=imgurl:{encoded_url}",
            f"https://tineye.com/search?url={encoded_url}"
        ]
        
        self.girly_print("✅ สร้าง search URLs สำหรับ reverse image search แล้ว", "SUCCESS", "🔗")
        
        # เพิ่มเข้า results
        self.results['reverse_search_urls'] = reverse_image_urls
        
        return reverse_image_urls

    def analyze_from_url(self, image_url: str) -> Dict[str, Any]:
        """
        🔍 วิเคราะห์รูปจาก URL
        
        Args:
            image_url: URL ของรูปภาพที่ต้องการวิเคราะห์
            
        Returns:
            Dictionary ของผลการวิเคราะห์
        """
        self.girly_print(f"🚀 เริ่มการวิเคราะห์รูปภาพ: {image_url[:50]}...", "INFO", "🔍")
        
        # 1. ดาวน์โหลดรูปภาพ
        image_data = self.download_image(image_url)
        if not image_data:
            return {
                'success': False,
                'error': 'Failed to download image',
                'image_url': image_url
            }
        
        # 2. Extract Instagram profile hints
        self.extract_instagram_profile_hints(image_url)
        
        # 3. Extract metadata
        self.extract_metadata(image_data)
        
        # 4. Analyze image content
        self.analyze_image_content(image_data)
        
        # 5. Generate image signature
        signature = self.generate_image_signature(image_data)
        self.results['image_signature'] = signature
        
        # 6. Find similar images (Optional)
        reverse_search_urls = self.find_similar_images(image_url)
        
        # 7. Save the results
        timestamp = int(time.time())
        
        # Create a sanitized filename from URL
        url_hash = hashlib.md5(image_url.encode()).hexdigest()[:10]
        result_filename = self.output_dir / f"image_analysis_{url_hash}_{timestamp}.json"
        
        with open(result_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # 8. Save the image
        try:
            image_data.seek(0)
            image_filename = self.output_dir / f"image_{url_hash}_{timestamp}.jpg"
            with open(image_filename, 'wb') as f:
                f.write(image_data.getvalue())
            self.girly_print(f"💾 บันทึกรูปภาพไปที่: {image_filename}", "SUCCESS", "📸")
        except:
            pass
        
        self.girly_print(f"✅ การวิเคราะห์เสร็จสมบูรณ์! ผลลัพธ์: {result_filename}", "SUCCESS", "🎉")
        
        return self.results

    def generate_report(self) -> str:
        """
        📊 สร้างรายงานสวยๆ แบบ text
        
        Returns:
            Formatted report
        """
        report = f"""
🖼️💕 INSTAGRAM IMAGE ANALYZER 2025 - REPORT 💕🖼️
{'='*60}

📷 IMAGE SOURCE
URL: {self.results['image_url'][:60]}...
Download Time: {self.results['download_time']}
Image Signature: {self.results.get('image_signature', 'Unknown')}

📊 IMAGE DATA
Size: {self.results['image_data'].get('size_bytes', 'Unknown')} bytes
Type: {self.results['image_data'].get('content_type', 'Unknown')}
Format: {self.results['metadata'].get('format', 'Unknown')}
Resolution: {self.results['metadata'].get('resolution', 'Unknown')}
"""

        # Add profile hints
        if self.results['profile_hints']:
            report += "\n👤 PROFILE INSIGHTS\n"
            for hint in self.results['profile_hints']:
                report += f"  • {hint}\n"

        # Add metadata insights
        if self.results['metadata']:
            report += "\n🔍 METADATA INSIGHTS\n"
            
            # Add important metadata fields
            important_fields = ['dominant_color', 'color_tone', 'aspect_ratio']
            for field in important_fields:
                if field in self.results['metadata']:
                    report += f"  • {field.replace('_', ' ').title()}: {self.results['metadata'][field]}\n"
            
            # Add EXIF if available
            if 'exif' in self.results['metadata']:
                report += "  • EXIF Data:\n"
                for key, value in list(self.results['metadata']['exif'].items())[:3]:  # Show only first 3
                    report += f"     - {key}: {value}\n"
                if len(self.results['metadata']['exif']) > 3:
                    report += f"     - ...and {len(self.results['metadata']['exif']) - 3} more fields\n"

        # Add content analysis
        if self.results['analysis']:
            report += "\n🧠 CONTENT ANALYSIS\n"
            for key, value in self.results['analysis'].items():
                report += f"  • {key.replace('_', ' ').title()}: {value}\n"

        # Add related URLs
        if self.results['related_urls']:
            report += "\n🔗 RELATED URLS\n"
            for url in self.results['related_urls']:
                report += f"  • {url}\n"

        # Add reverse search
        if 'reverse_search_urls' in self.results:
            report += "\n🔎 REVERSE IMAGE SEARCH\n"
            for url in self.results['reverse_search_urls'][:2]:  # Show only first 2
                report += f"  • {url[:70]}...\n"

        report += f"""
💖 Generated with love by น้องจิน's Instagram Image Analyzer
👻 For educational and authorized research only!
"""

        return report


def main():
    """Main interactive function"""
    print(GIRLY_BANNER)
    
    analyzer = InstagramImageAnalyzer()
    
    while True:
        print("\n💖 INSTAGRAM IMAGE ANALYZER 2025 MENU 💖")
        print("1. 🚀 Analyze Image from URL")
        print("0. 💔 Exit")
        
        choice = input("\n💖 เลือกเมนู (0-1): ").strip()
        
        try:
            if choice == '1':
                image_url = input("🖼️ Instagram image URL: ").strip()
                if image_url:
                    analyzer.analyze_from_url(image_url)
                    
                    # Show report
                    print(analyzer.generate_report())
                
            elif choice == '0':
                print("👋 บาย! นะคะ ♥️")
                break
                
            else:
                print("❌ เลือกเมนูให้ถูกนะคะ")
                
        except KeyboardInterrupt:
            print("\n⚠️ หยุดการทำงาน")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
