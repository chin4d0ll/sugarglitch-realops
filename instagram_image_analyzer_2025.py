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
import urllib.parse
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import base64
from PIL import Image, ImageStat, ImageFilter
from PIL.ExifTags import TAGS
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

# Advanced analysis imports (optional)
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

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
            'ai_analysis': {},
            'face_analysis': {},
            'steganography_check': {},
            'deepfake_indicators': {},
            'related_urls': [],
            'profile_hints': [],
            'reverse_search_urls': [],
            'technical_forensics': {}
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
                    
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, str(tag_id))
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

    def advanced_ai_analysis(self, image_data: BytesIO) -> Dict[str, Any]:
        """
        🤖 Advanced AI-powered image analysis
        
        Args:
            image_data: BytesIO object ของรูปภาพ
            
        Returns:
            Dictionary ของผลการวิเคราะห์ AI
        """
        self.girly_print("🤖 กำลังทำ AI Analysis ขั้นสูง...", "INFO", "🧠")
        
        ai_analysis = {}
        
        try:
            with Image.open(image_data) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Image statistics analysis
                img_array = np.array(img)
                
                # Color analysis
                ai_analysis['color_statistics'] = {
                    'mean_brightness': float(np.mean(img_array)),
                    'std_brightness': float(np.std(img_array)),
                    'contrast_level': float(np.std(img_array) / np.mean(img_array)) if np.mean(img_array) > 0 else 0
                }
                
                # Detect image compression quality
                stats = ImageStat.Stat(img)
                ai_analysis['quality_indicators'] = {
                    'variance': stats.var,
                    'mean_values': stats.mean,
                    'extrema': stats.extrema
                }
                
                # Advanced filter detection
                ai_analysis['filter_analysis'] = self._detect_instagram_filters(img)
                
                # Scene complexity analysis
                ai_analysis['scene_complexity'] = self._analyze_scene_complexity(img)
                
                # Aesthetic scoring
                ai_analysis['aesthetic_score'] = self._calculate_aesthetic_score(img)
                
                self.girly_print(f"✅ AI Analysis สำเร็จ: {len(ai_analysis)} features", "SUCCESS", "🤖")
                
                # เพิ่มเข้า results
                self.results['ai_analysis'] = ai_analysis
                
                return ai_analysis
                
        except Exception as e:
            self.girly_print(f"⚠️ AI Analysis ล้มเหลว: {str(e)}", "WARNING", "⚠️")
            return {}

    def _detect_instagram_filters(self, img: Image.Image) -> Dict[str, Any]:
        """Detect Instagram filters applied to image"""
        filter_analysis = {}
        
        try:
            # Convert to smaller size for analysis
            small_img = img.resize((100, 100))
            img_array = np.array(small_img)
            
            # Calculate color channel statistics
            r_channel = img_array[:, :, 0]
            g_channel = img_array[:, :, 1]
            b_channel = img_array[:, :, 2]
            
            r_mean, g_mean, b_mean = np.mean(r_channel), np.mean(g_channel), np.mean(b_channel)
            r_std, g_std, b_std = np.std(r_channel), np.std(g_channel), np.std(b_channel)
            
            # Filter signatures (simplified)
            if r_mean > g_mean + 15 and r_mean > b_mean + 15:
                if r_std < 30:
                    filter_analysis['detected_filter'] = 'Valencia/Lo-Fi (Warm tone)'
                else:
                    filter_analysis['detected_filter'] = 'Ludwig/X-Pro II (High contrast warm)'
            elif b_mean > r_mean + 15 and b_mean > g_mean + 15:
                filter_analysis['detected_filter'] = 'Moon/Perpetua (Cool tone)'
            elif r_mean > 200 and g_mean > 200 and b_mean > 200:
                filter_analysis['detected_filter'] = 'Gingham/Lark (Bright/Overexposed)'
            elif r_mean < 80 and g_mean < 80 and b_mean < 80:
                filter_analysis['detected_filter'] = 'Inkwell/Willow (Dark/Moody)'
            elif abs(r_mean - g_mean) < 10 and abs(g_mean - b_mean) < 10:
                if np.std(img_array) > 50:
                    filter_analysis['detected_filter'] = 'Clarendon (High contrast)'
                else:
                    filter_analysis['detected_filter'] = 'Normal/No filter'
            else:
                filter_analysis['detected_filter'] = 'Unknown/Custom filter'
            
            # Saturation analysis
            hsv_img = img.convert('HSV')
            hsv_array = np.array(hsv_img)
            saturation = np.mean(hsv_array[:, :, 1])
            
            if saturation > 180:
                filter_analysis['saturation_level'] = 'High (Instagram filter likely)'
            elif saturation > 120:
                filter_analysis['saturation_level'] = 'Medium'
            else:
                filter_analysis['saturation_level'] = 'Low/Natural'
                
        except Exception as e:
            filter_analysis['error'] = f"Filter detection failed: {str(e)}"
            
        return filter_analysis

    def _analyze_scene_complexity(self, img: Image.Image) -> Dict[str, Any]:
        """Analyze scene complexity and composition"""
        complexity = {}
        
        try:
            # Edge detection for complexity
            gray_img = img.convert('L')
            edges = gray_img.filter(ImageFilter.FIND_EDGES)
            edge_array = np.array(edges)
            
            complexity['edge_density'] = float(np.sum(edge_array > 50) / edge_array.size)
            
            if complexity['edge_density'] > 0.3:
                complexity['scene_type'] = 'Complex (many details)'
            elif complexity['edge_density'] > 0.15:
                complexity['scene_type'] = 'Medium complexity'
            else:
                complexity['scene_type'] = 'Simple (minimal details)'
                
            # Color variety
            colors = img.getcolors(maxcolors=256*256*256)
            if colors:
                complexity['color_variety'] = len(colors)
                if len(colors) > 50000:
                    complexity['color_richness'] = 'Very rich'
                elif len(colors) > 10000:
                    complexity['color_richness'] = 'Rich'
                else:
                    complexity['color_richness'] = 'Limited palette'
                    
        except Exception as e:
            complexity['error'] = f"Complexity analysis failed: {str(e)}"
            
        return complexity

    def _calculate_aesthetic_score(self, img: Image.Image) -> Dict[str, Any]:
        """Calculate aesthetic appeal score"""
        aesthetic = {}
        
        try:
            # Rule of thirds analysis
            width, height = img.size
            img_array = np.array(img.convert('L'))
            
            # Check contrast
            contrast = np.std(img_array)
            aesthetic['contrast_score'] = min(100, contrast * 2)  # Normalize to 0-100
            
            # Check brightness distribution
            brightness_hist = np.histogram(img_array, bins=10)[0]
            brightness_variety = len([x for x in brightness_hist if x > 0])
            aesthetic['brightness_variety'] = brightness_variety * 10  # 0-100 scale
            
            # Overall aesthetic score (simplified)
            aesthetic['overall_score'] = int((aesthetic['contrast_score'] + aesthetic['brightness_variety']) / 2)
            
            if aesthetic['overall_score'] > 80:
                aesthetic['appeal_level'] = 'Very appealing'
            elif aesthetic['overall_score'] > 60:
                aesthetic['appeal_level'] = 'Good'
            elif aesthetic['overall_score'] > 40:
                aesthetic['appeal_level'] = 'Average'
            else:
                aesthetic['appeal_level'] = 'Poor'
                
        except Exception as e:
            aesthetic['error'] = f"Aesthetic analysis failed: {str(e)}"
            
        return aesthetic

    def face_detection_analysis(self, image_data: BytesIO) -> Dict[str, Any]:
        """
        👤 Face detection and analysis
        
        Args:
            image_data: BytesIO object ของรูปภาพ
            
        Returns:
            Dictionary ของผลการวิเคราะห์ใบหน้า
        """
        self.girly_print("👤 กำลังวิเคราะห์ใบหน้าในรูปภาพ...", "INFO", "🔍")
        
        face_analysis = {}
        
        try:
            if OPENCV_AVAILABLE:
                # Using OpenCV for face detection
                image_data.seek(0)
                img_bytes = np.frombuffer(image_data.read(), np.uint8)
                img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
                
                # Load cascade classifier
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                face_analysis['opencv_faces_detected'] = len(faces)
                face_analysis['face_locations'] = []
                
                for (x, y, w, h) in faces:
                    face_analysis['face_locations'].append({
                        'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)
                    })
                
                if len(faces) > 0:
                    face_analysis['has_faces'] = True
                    if len(faces) == 1:
                        face_analysis['scene_type'] = 'Portrait (single person)'
                    else:
                        face_analysis['scene_type'] = f'Group photo ({len(faces)} people)'
                else:
                    face_analysis['has_faces'] = False
                    face_analysis['scene_type'] = 'No faces detected'
                    
            elif FACE_RECOGNITION_AVAILABLE:
                # Using face_recognition library
                image_data.seek(0)
                img = face_recognition.load_image_file(image_data)
                
                face_locations = face_recognition.face_locations(img)
                face_analysis['face_recognition_faces'] = len(face_locations)
                
                if len(face_locations) > 0:
                    face_analysis['has_faces'] = True
                    face_analysis['detailed_locations'] = face_locations
                else:
                    face_analysis['has_faces'] = False
                    
            else:
                # Fallback: Basic face detection using PIL and patterns
                with Image.open(image_data) as img:
                    # Simple skin tone detection as face indicator
                    img_array = np.array(img.convert('RGB'))
                    
                    # Skin tone range (very basic)
                    skin_mask = ((img_array[:, :, 0] > 95) & 
                               (img_array[:, :, 1] > 40) & 
                               (img_array[:, :, 2] > 20) &
                               (img_array[:, :, 0] > img_array[:, :, 2]) & 
                               (img_array[:, :, 0] > img_array[:, :, 1]))
                    
                    skin_percentage = np.sum(skin_mask) / skin_mask.size * 100
                    
                    if skin_percentage > 15:
                        face_analysis['likely_has_faces'] = True
                        face_analysis['skin_tone_percentage'] = skin_percentage
                    else:
                        face_analysis['likely_has_faces'] = False
                        
                face_analysis['detection_method'] = 'Basic skin tone analysis'
                
            self.girly_print(f"✅ Face analysis สำเร็จ: {face_analysis.get('opencv_faces_detected', 'Unknown')} faces", "SUCCESS", "👤")
            
            # เพิ่มเข้า results
            self.results['face_analysis'] = face_analysis
            
            return face_analysis
            
        except Exception as e:
            self.girly_print(f"⚠️ Face detection ล้มเหลว: {str(e)}", "WARNING", "⚠️")
            return {'error': str(e)}

    def steganography_analysis(self, image_data: BytesIO) -> Dict[str, Any]:
        """
        🕵️ Check for hidden data in image (steganography)
        
        Args:
            image_data: BytesIO object ของรูปภาพ
            
        Returns:
            Dictionary ของผลการตรวจสอบ steganography
        """
        self.girly_print("🕵️ กำลังตรวจสอบข้อมูลที่ซ่อนในรูปภาพ...", "INFO", "🔍")
        
        stego_analysis = {}
        
        try:
            image_data.seek(0)
            img_bytes = image_data.read()
            
            # Check for common steganography signatures
            stego_analysis['file_size'] = len(img_bytes)
            
            # Check for unusual data at end of file
            last_1kb = img_bytes[-1024:]
            
            # Look for text patterns
            text_patterns = [b'BEGIN', b'END', b'HIDDEN', b'SECRET', b'PASSWORD', b'KEY']
            found_patterns = []
            
            for pattern in text_patterns:
                if pattern in img_bytes:
                    found_patterns.append(pattern.decode())
                    
            if found_patterns:
                stego_analysis['suspicious_text'] = found_patterns
                stego_analysis['steganography_risk'] = 'High'
            
            # Check entropy (randomness) of last part of file
            if len(last_1kb) > 100:
                unique_bytes = len(set(last_1kb))
                entropy_score = unique_bytes / 256  # Normalize
                
                if entropy_score > 0.8:
                    stego_analysis['high_entropy_detected'] = True
                    stego_analysis['steganography_risk'] = 'Medium'
                    
            # Check for unusual metadata
            try:
                with Image.open(image_data) as img:
                    info = img.info
                    unusual_keys = []
                    
                    for key in info.keys():
                        if key not in ['jfif', 'jfif_version', 'jfif_unit', 'jfif_density', 'dpi', 'exif']:
                            unusual_keys.append(key)
                            
                    if unusual_keys:
                        stego_analysis['unusual_metadata'] = unusual_keys
                        
            except:
                pass
                
            # Final risk assessment
            if 'suspicious_text' in stego_analysis:
                stego_analysis['steganography_risk'] = 'High'
            elif 'high_entropy_detected' in stego_analysis or 'unusual_metadata' in stego_analysis:
                stego_analysis['steganography_risk'] = 'Medium'
            else:
                stego_analysis['steganography_risk'] = 'Low'
                
            self.girly_print(f"✅ Steganography check สำเร็จ: {stego_analysis['steganography_risk']} risk", "SUCCESS", "🕵️")
            
            # เพิ่มเข้า results
            self.results['steganography_check'] = stego_analysis
            
            return stego_analysis
            
        except Exception as e:
            self.girly_print(f"⚠️ Steganography analysis ล้มเหลว: {str(e)}", "WARNING", "⚠️")
            return {'error': str(e)}

    def deepfake_indicators(self, image_data: BytesIO) -> Dict[str, Any]:
        """
        🎭 Check for deepfake indicators
        
        Args:
            image_data: BytesIO object ของรูปภาพ
            
        Returns:
            Dictionary ของ deepfake indicators
        """
        self.girly_print("🎭 กำลังตรวจสอบ deepfake indicators...", "INFO", "🔍")
        
        deepfake_analysis = {}
        
        try:
            with Image.open(image_data) as img:
                img_array = np.array(img.convert('RGB'))
                
                # Check for unusual compression artifacts
                # Deepfakes often have inconsistent compression
                
                # Check color inconsistencies
                if len(img_array.shape) == 3:
                    # Calculate color variance in different regions
                    height, width = img_array.shape[:2]
                    
                    # Split image into quadrants
                    quad1 = img_array[:height//2, :width//2]
                    quad2 = img_array[:height//2, width//2:]
                    quad3 = img_array[height//2:, :width//2]
                    quad4 = img_array[height//2:, width//2:]
                    
                    variances = [np.var(quad) for quad in [quad1, quad2, quad3, quad4]]
                    variance_diff = max(variances) - min(variances)
                    
                    if variance_diff > 1000:
                        deepfake_analysis['uneven_quality'] = True
                        deepfake_analysis['variance_difference'] = variance_diff
                    
                # Check for face inconsistencies (if faces detected)
                if self.results.get('face_analysis', {}).get('has_faces'):
                    # Simple check for unusual face properties
                    face_locations = self.results['face_analysis'].get('face_locations', [])
                    
                    for face in face_locations:
                        # Extract face region
                        x, y, w, h = face['x'], face['y'], face['width'], face['height']
                        face_region = img_array[y:y+h, x:x+w]
                        
                        if face_region.size > 0:
                            # Check for unusual sharpness differences
                            face_var = np.var(face_region)
                            
                            # Compare with background
                            background_regions = [
                                img_array[:y, :],  # Above face
                                img_array[y+h:, :] if y+h < height else img_array[:1, :]  # Below face
                            ]
                            
                            bg_vars = [np.var(region) for region in background_regions if region.size > 0]
                            if bg_vars:
                                avg_bg_var = np.mean(bg_vars)
                                
                                if face_var > avg_bg_var * 2:
                                    deepfake_analysis['face_sharpness_anomaly'] = True
                
                # Check metadata for AI generation signatures
                image_data.seek(0)
                img_bytes = image_data.read()
                
                ai_signatures = [b'stable-diffusion', b'midjourney', b'dall-e', b'gpt', b'ai-generated']
                found_signatures = []
                
                for sig in ai_signatures:
                    if sig in img_bytes.lower():
                        found_signatures.append(sig.decode())
                        
                if found_signatures:
                    deepfake_analysis['ai_generation_signatures'] = found_signatures
                    deepfake_analysis['likely_ai_generated'] = True
                
                # Final assessment
                risk_factors = sum([
                    'uneven_quality' in deepfake_analysis,
                    'face_sharpness_anomaly' in deepfake_analysis,
                    'likely_ai_generated' in deepfake_analysis
                ])
                
                if risk_factors >= 2:
                    deepfake_analysis['deepfake_risk'] = 'High'
                elif risk_factors == 1:
                    deepfake_analysis['deepfake_risk'] = 'Medium'
                else:
                    deepfake_analysis['deepfake_risk'] = 'Low'
                    
            self.girly_print(f"✅ Deepfake check สำเร็จ: {deepfake_analysis.get('deepfake_risk', 'Unknown')} risk", "SUCCESS", "🎭")
            
            # เพิ่มเข้า results
            self.results['deepfake_indicators'] = deepfake_analysis
            
            return deepfake_analysis
            
        except Exception as e:
            self.girly_print(f"⚠️ Deepfake analysis ล้มเหลว: {str(e)}", "WARNING", "⚠️")
            return {'error': str(e)}

    def technical_forensics(self, image_data: BytesIO) -> Dict[str, Any]:
        """
        🔬 Advanced technical forensics
        
        Args:
            image_data: BytesIO object ของรูปภาพ
            
        Returns:
            Dictionary ของ technical forensics
        """
        self.girly_print("🔬 กำลังทำ technical forensics...", "INFO", "🔬")
        
        forensics = {}
        
        try:
            image_data.seek(0)
            img_bytes = image_data.read()
            
            # File header analysis
            header = img_bytes[:20]
            forensics['file_header'] = header.hex()
            
            # Check for multiple JPEG headers (sign of editing)
            jpeg_headers = img_bytes.count(b'\xff\xd8')
            if jpeg_headers > 1:
                forensics['multiple_jpeg_headers'] = jpeg_headers
                forensics['likely_edited'] = True
                
            # Check for embedded thumbnails
            if b'\xff\xd8\xff\xe0' in img_bytes[100:]:  # Skip main header
                forensics['embedded_thumbnail'] = True
                
            # Quantization table analysis
            qt_count = img_bytes.count(b'\xff\xdb')
            forensics['quantization_tables'] = qt_count
            
            if qt_count > 2:
                forensics['editing_evidence'] = 'Multiple quantization tables suggest re-encoding'
                
            # Check for Photoshop signature
            if b'Photoshop' in img_bytes:
                forensics['photoshop_edited'] = True
                
            # Check for GIMP signature
            if b'GIMP' in img_bytes:
                forensics['gimp_edited'] = True
                
            # Error level analysis (simplified)
            with Image.open(image_data) as img:
                if img.format == 'JPEG':
                    # Save at different quality levels and compare
                    temp_high = BytesIO()
                    temp_low = BytesIO()
                    
                    img.save(temp_high, 'JPEG', quality=95)
                    img.save(temp_low, 'JPEG', quality=75)
                    
                    size_diff = len(temp_high.getvalue()) - len(temp_low.getvalue())
                    forensics['compression_analysis'] = {
                        'high_quality_size': len(temp_high.getvalue()),
                        'low_quality_size': len(temp_low.getvalue()),
                        'compression_difference': size_diff
                    }
                    
                    if size_diff < 10000:  # Very small difference suggests prior heavy compression
                        forensics['heavy_compression_detected'] = True
                        
            self.girly_print(f"✅ Technical forensics สำเร็จ: {len(forensics)} indicators", "SUCCESS", "🔬")
            
            # เพิ่มเข้า results
            self.results['technical_forensics'] = forensics
            
            return forensics
            
        except Exception as e:
            self.girly_print(f"⚠️ Technical forensics ล้มเหลว: {str(e)}", "WARNING", "⚠️")
            return {'error': str(e)}

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
        🔍 วิเคราะห์รูปจาก URL ด้วย AI ขั้นสูง
        
        Args:
            image_url: URL ของรูปภาพที่ต้องการวิเคราะห์
            
        Returns:
            Dictionary ของผลการวิเคราะห์
        """
        self.girly_print(f"🚀 เริ่มการวิเคราะห์รูปภาพขั้นสูง: {image_url[:50]}...", "INFO", "🔍")
        
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
        
        # 5. Advanced AI Analysis
        self.advanced_ai_analysis(image_data)
        
        # 6. Face detection and analysis
        self.face_detection_analysis(image_data)
        
        # 7. Steganography check
        self.steganography_analysis(image_data)
        
        # 8. Deepfake indicators
        self.deepfake_indicators(image_data)
        
        # 9. Technical forensics
        self.technical_forensics(image_data)
        
        # 10. Generate image signature
        signature = self.generate_image_signature(image_data)
        self.results['image_signature'] = signature
        
        # 11. Find similar images
        reverse_search_urls = self.find_similar_images(image_url)
        
        # 12. Save the results
        timestamp = int(time.time())
        
        # Create a sanitized filename from URL
        url_hash = hashlib.md5(image_url.encode()).hexdigest()[:10]
        result_filename = self.output_dir / f"enhanced_analysis_{url_hash}_{timestamp}.json"
        
        with open(result_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str, ensure_ascii=False)
        
        # 13. Save the image
        try:
            image_data.seek(0)
            image_filename = self.output_dir / f"analyzed_image_{url_hash}_{timestamp}.jpg"
            with open(image_filename, 'wb') as f:
                f.write(image_data.getvalue())
            self.girly_print(f"💾 บันทึกรูปภาพไปที่: {image_filename}", "SUCCESS", "📸")
        except:
            pass
        
        # 14. Add success flag and overall assessment
        self.results['success'] = True
        self.results['analysis_timestamp'] = datetime.now().isoformat()
        
        # Overall risk assessment
        risk_factors = []
        if self.results.get('steganography_check', {}).get('steganography_risk') == 'High':
            risk_factors.append('Hidden data detected')
        if self.results.get('deepfake_indicators', {}).get('deepfake_risk') == 'High':
            risk_factors.append('Possible deepfake')
        if self.results.get('technical_forensics', {}).get('likely_edited'):
            risk_factors.append('Evidence of editing')
            
        self.results['overall_assessment'] = {
            'risk_factors': risk_factors,
            'total_risk_level': 'High' if len(risk_factors) >= 2 else 'Medium' if len(risk_factors) == 1 else 'Low'
        }
        
        self.girly_print(f"✅ การวิเคราะห์ขั้นสูงเสร็จสมบูรณ์! Risk Level: {self.results['overall_assessment']['total_risk_level']}", "SUCCESS", "🎉")
        self.girly_print(f"📁 ผลลัพธ์: {result_filename}", "INFO", "📊")
        
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
