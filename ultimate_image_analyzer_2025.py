#!/usr/bin/env python3
"""
🎨🔥 ULTIMATE INSTAGRAM IMAGE ANALYZER 2025 🔥🎨
================================================
- วิเคราะห์รูปภาพแบบ Advanced AI
- หาข้อมูลลับใน metadata
- ตรวจจับ steganography + deepfake
- Face detection + aesthetic analysis
- ใช้ร่วมกับ Enhanced Private Bypass

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 - Ultimate Edition!
For: Educational & Security Research Only!
"""

import os
import json
import time
import hashlib
import base64
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import warnings
warnings.filterwarnings("ignore")

# AI/ML Libraries (with fallback handling)
try:
    import cv2
    import numpy as np
    from PIL import Image, ExifTags
    from PIL.ExifTags import TAGS
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV not available. Face detection disabled.")

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("⚠️ face_recognition not available. Advanced face analysis disabled.")

# === GIRLY CONFIG ===
GIRLY_BANNER = """
🎨💖👻 ULTIMATE INSTAGRAM IMAGE ANALYZER 👻💖🎨
        โดย น้องจิน - Ultimate AI Edition! ♥️
    วิเคราะห์รูปแบบ AI + ค้นหาข้อมูลลับ + ตรวจจับ Deepfake
"""

class UltimateImageAnalyzer:
    """
    🎨 Ultimate Instagram Image Analyzer
    
    ✨ Features:
    - Advanced Metadata Extraction
    - Face Detection & Analysis
    - Steganography Detection
    - Deepfake Indicators
    - Aesthetic Scoring
    - Technical Forensics
    """
    
    def __init__(self):
        self.results = {
            'analyzer_id': f"ULTIMATE_{int(time.time())}",
            'analysis_timestamp': datetime.now().isoformat(),
            'images_analyzed': [],
            'total_images': 0,
            'findings': {}
        }
        
        # Detection thresholds
        self.deepfake_threshold = 0.7
        self.face_confidence_threshold = 0.6
        self.steganography_threshold = 0.8

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

    def download_image(self, image_url: str, save_path: str) -> bool:
        """
        📥 Download image from URL
        
        Args:
            image_url: URL of image to download
            save_path: Local path to save image
            
        Returns:
            Success status
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive'
            }
            
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            self.girly_print(f"📥 Downloaded: {Path(save_path).name}", "SUCCESS", "💾")
            return True
            
        except Exception as e:
            self.girly_print(f"❌ Download failed: {str(e)[:50]}...", "ERROR", "💔")
            return False

    def extract_advanced_metadata(self, image_path: str) -> Dict:
        """
        🔍 Extract comprehensive metadata from image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Metadata dictionary
        """
        self.girly_print(f"🔍 Extracting metadata: {Path(image_path).name}", "INFO", "📊")
        
        metadata = {
            'file_info': {},
            'exif_data': {},
            'technical_analysis': {},
            'security_indicators': {}
        }
        
        try:
            # File information
            file_stat = os.stat(image_path)
            metadata['file_info'] = {
                'size_bytes': file_stat.st_size,
                'size_mb': round(file_stat.st_size / 1024 / 1024, 2),
                'created': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'file_hash': hashlib.md5(open(image_path, 'rb').read()).hexdigest()
            }
            
            # Open image with PIL
            with Image.open(image_path) as img:
                # Basic image info
                metadata['file_info'].update({
                    'format': img.format,
                    'mode': img.mode,
                    'dimensions': f"{img.width}x{img.height}",
                    'aspect_ratio': round(img.width / img.height, 2) if img.height > 0 else 0
                })
                
                # EXIF data extraction
                if hasattr(img, '_getexif') and img._getexif():
                    exif_dict = img._getexif()
                    
                    for tag_id, value in exif_dict.items():
                        try:
                            tag = TAGS.get(tag_id, tag_id)
                            
                            # Convert complex values to strings
                            if isinstance(value, (tuple, list)):
                                value = str(value)
                            elif isinstance(value, bytes):
                                try:
                                    value = value.decode('utf-8', errors='ignore')
                                except:
                                    value = str(value)
                            
                            metadata['exif_data'][tag] = value
                            
                        except Exception as e:
                            continue
                
                # Technical analysis
                metadata['technical_analysis'] = self.analyze_image_technical(img)
                
                # Security indicators
                metadata['security_indicators'] = self.check_security_indicators(image_path, img)
            
            self.girly_print(f"📊 Metadata extracted: {len(metadata['exif_data'])} EXIF tags", "SUCCESS", "✅")
            return metadata
            
        except Exception as e:
            self.girly_print(f"❌ Metadata extraction failed: {str(e)[:50]}...", "ERROR", "💔")
            return metadata

    def analyze_image_technical(self, img: Image.Image) -> Dict:
        """
        🔧 Technical image analysis
        
        Args:
            img: PIL Image object
            
        Returns:
            Technical analysis results
        """
        try:
            # Convert to numpy array for analysis
            img_array = np.array(img)
            
            analysis = {
                'color_channels': len(img_array.shape),
                'bit_depth': img_array.dtype.name,
                'total_pixels': img.width * img.height,
                'file_complexity': 'unknown'
            }
            
            if len(img_array.shape) >= 3:
                # Color analysis
                analysis.update({
                    'mean_brightness': np.mean(img_array).round(2),
                    'std_brightness': np.std(img_array).round(2),
                    'color_variance': np.var(img_array).round(2)
                })
                
                # Detect compression artifacts
                if img.format == 'JPEG':
                    analysis['compression_quality'] = self.estimate_jpeg_quality(img_array)
                
                # Complexity estimation
                analysis['file_complexity'] = self.estimate_image_complexity(img_array)
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}

    def estimate_jpeg_quality(self, img_array: np.ndarray) -> str:
        """Estimate JPEG compression quality"""
        try:
            # Simple quality estimation based on noise levels
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY) if CV2_AVAILABLE else np.mean(img_array, axis=2)
            else:
                gray = img_array
                
            # Calculate noise/artifacts
            noise = np.std(np.diff(gray.flatten()))
            
            if noise < 5:
                return "High (90-100%)"
            elif noise < 15:
                return "Medium (70-90%)"
            elif noise < 30:
                return "Low (50-70%)"
            else:
                return "Very Low (<50%)"
                
        except:
            return "Unknown"

    def estimate_image_complexity(self, img_array: np.ndarray) -> str:
        """Estimate image complexity"""
        try:
            # Calculate entropy as complexity measure
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            # Histogram-based entropy
            hist, _ = np.histogram(gray.flatten(), bins=256, range=(0, 256))
            hist = hist + 1e-10  # Avoid log(0)
            entropy = -np.sum((hist / np.sum(hist)) * np.log2(hist / np.sum(hist)))
            
            if entropy > 7:
                return "Very High"
            elif entropy > 6:
                return "High"
            elif entropy > 5:
                return "Medium"
            else:
                return "Low"
                
        except:
            return "Unknown"

    def check_security_indicators(self, image_path: str, img: Image.Image) -> Dict:
        """
        🛡️ Check for security-related indicators
        
        Args:
            image_path: Path to image file
            img: PIL Image object
            
        Returns:
            Security analysis results
        """
        indicators = {
            'steganography_risk': 'Low',
            'unusual_properties': [],
            'metadata_anomalies': [],
            'file_structure_warnings': []
        }
        
        try:
            # File size vs dimension analysis
            file_size = os.path.getsize(image_path)
            expected_size = img.width * img.height * 3  # Rough estimate for RGB
            
            size_ratio = file_size / expected_size if expected_size > 0 else 0
            
            # Steganography indicators
            if size_ratio > 0.5:  # Unusually large file for dimensions
                indicators['steganography_risk'] = 'High'
                indicators['unusual_properties'].append('File size disproportionate to image dimensions')
            elif size_ratio > 0.3:
                indicators['steganography_risk'] = 'Medium'
            
            # Metadata anomalies
            if hasattr(img, '_getexif') and img._getexif():
                exif_dict = img._getexif()
                
                # Check for unusual EXIF tags
                suspicious_tags = ['MakerNote', 'UserComment', 'ImageDescription']
                for tag_id, value in exif_dict.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag in suspicious_tags and value:
                        indicators['metadata_anomalies'].append(f'Suspicious {tag} found')
            
            # Format-specific checks
            if img.format == 'PNG':
                # PNG can hide data in ancillary chunks
                with open(image_path, 'rb') as f:
                    content = f.read()
                    if b'tEXt' in content or b'zTXt' in content:
                        indicators['unusual_properties'].append('PNG text chunks detected')
            
            return indicators
            
        except Exception as e:
            indicators['error'] = str(e)
            return indicators

    def detect_faces(self, image_path: str) -> Dict:
        """
        👥 Advanced face detection and analysis
        
        Args:
            image_path: Path to image file
            
        Returns:
            Face detection results
        """
        self.girly_print(f"👥 Detecting faces: {Path(image_path).name}", "INFO", "🔍")
        
        face_data = {
            'total_faces': 0,
            'faces': [],
            'analysis_method': 'None',
            'confidence_scores': []
        }
        
        try:
            if not CV2_AVAILABLE:
                face_data['error'] = 'OpenCV not available'
                return face_data
            
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                face_data['error'] = 'Could not load image'
                return face_data
            
            # Convert to RGB for face_recognition
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Method 1: face_recognition library (more accurate)
            if FACE_RECOGNITION_AVAILABLE:
                face_locations = face_recognition.face_locations(img_rgb)
                face_encodings = face_recognition.face_encodings(img_rgb, face_locations)
                
                face_data['analysis_method'] = 'face_recognition + OpenCV'
                face_data['total_faces'] = len(face_locations)
                
                for i, (top, right, bottom, left) in enumerate(face_locations):
                    face_info = {
                        'id': i + 1,
                        'location': {'top': top, 'right': right, 'bottom': bottom, 'left': left},
                        'width': right - left,
                        'height': bottom - top,
                        'area': (right - left) * (bottom - top),
                        'encoding_available': i < len(face_encodings)
                    }
                    
                    # Face quality analysis
                    face_roi = img_rgb[top:bottom, left:right]
                    if face_roi.size > 0:
                        face_info['quality'] = self.analyze_face_quality(face_roi)
                    
                    face_data['faces'].append(face_info)
                    face_data['confidence_scores'].append(0.9)  # face_recognition is generally confident
                
            else:
                # Method 2: OpenCV Haar Cascades (fallback)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
                face_data['analysis_method'] = 'OpenCV Haar Cascades'
                face_data['total_faces'] = len(faces)
                
                for i, (x, y, w, h) in enumerate(faces):
                    face_info = {
                        'id': i + 1,
                        'location': {'x': x, 'y': y, 'width': w, 'height': h},
                        'area': w * h
                    }
                    
                    face_data['faces'].append(face_info)
                    face_data['confidence_scores'].append(0.7)  # Haar cascades are less confident
            
            if face_data['total_faces'] > 0:
                self.girly_print(f"👥 Found {face_data['total_faces']} faces!", "SUCCESS", "✅")
            else:
                self.girly_print("👥 No faces detected", "INFO", "ℹ️")
            
            return face_data
            
        except Exception as e:
            face_data['error'] = str(e)
            self.girly_print(f"❌ Face detection failed: {str(e)[:50]}...", "ERROR", "💔")
            return face_data

    def analyze_face_quality(self, face_roi: np.ndarray) -> Dict:
        """
        🎯 Analyze face quality and characteristics
        
        Args:
            face_roi: Face region of interest (numpy array)
            
        Returns:
            Face quality analysis
        """
        try:
            quality = {
                'sharpness': 'Unknown',
                'brightness': 'Unknown',
                'size_category': 'Unknown'
            }
            
            # Sharpness analysis (Laplacian variance)
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY) if len(face_roi.shape) == 3 else face_roi
            laplacian_var = cv2.Laplacian(gray_face, cv2.CV_64F).var()
            
            if laplacian_var > 500:
                quality['sharpness'] = 'High'
            elif laplacian_var > 100:
                quality['sharpness'] = 'Medium'
            else:
                quality['sharpness'] = 'Low'
            
            # Brightness analysis
            mean_brightness = np.mean(gray_face)
            if mean_brightness > 200:
                quality['brightness'] = 'Very Bright'
            elif mean_brightness > 150:
                quality['brightness'] = 'Bright'
            elif mean_brightness > 100:
                quality['brightness'] = 'Normal'
            elif mean_brightness > 50:
                quality['brightness'] = 'Dark'
            else:
                quality['brightness'] = 'Very Dark'
            
            # Size category
            face_area = face_roi.shape[0] * face_roi.shape[1]
            if face_area > 10000:
                quality['size_category'] = 'Large'
            elif face_area > 2500:
                quality['size_category'] = 'Medium'
            else:
                quality['size_category'] = 'Small'
            
            return quality
            
        except Exception as e:
            return {'error': str(e)}

    def detect_deepfake_indicators(self, image_path: str) -> Dict:
        """
        🤖 Detect potential deepfake indicators
        
        Args:
            image_path: Path to image file
            
        Returns:
            Deepfake analysis results
        """
        self.girly_print(f"🤖 Analyzing deepfake indicators: {Path(image_path).name}", "INFO", "🔍")
        
        deepfake_analysis = {
            'risk_level': 'Low',
            'confidence': 0.0,
            'indicators': [],
            'technical_anomalies': [],
            'visual_artifacts': []
        }
        
        try:
            if not CV2_AVAILABLE:
                deepfake_analysis['error'] = 'OpenCV not available'
                return deepfake_analysis
            
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                deepfake_analysis['error'] = 'Could not load image'
                return deepfake_analysis
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # 1. Face consistency analysis
            face_data = self.detect_faces(image_path)
            
            if face_data['total_faces'] > 0:
                # Check for multiple faces with inconsistent lighting
                if face_data['total_faces'] > 1:
                    deepfake_analysis['indicators'].append('Multiple faces detected - checking consistency')
                
                # Analyze face quality inconsistencies
                for face in face_data['faces']:
                    if 'quality' in face:
                        if face['quality'].get('sharpness') == 'Low':
                            deepfake_analysis['visual_artifacts'].append('Low face sharpness detected')
            
            # 2. Compression artifact analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Check for unnatural compression patterns
            # This is a simplified check - real deepfake detection requires ML models
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            if laplacian_var < 50:  # Very low variance might indicate artificial generation
                deepfake_analysis['technical_anomalies'].append('Unusually low image variance')
                deepfake_analysis['confidence'] += 0.3
            
            # 3. Edge consistency analysis
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            if edge_density < 0.05:  # Very few edges might indicate artificial generation
                deepfake_analysis['technical_anomalies'].append('Low edge density')
                deepfake_analysis['confidence'] += 0.2
            
            # 4. Color distribution analysis
            # Real photos typically have more complex color distributions
            hist_r = cv2.calcHist([img_rgb], [0], None, [256], [0, 256])
            hist_g = cv2.calcHist([img_rgb], [1], None, [256], [0, 256])
            hist_b = cv2.calcHist([img_rgb], [2], None, [256], [0, 256])
            
            # Calculate histogram uniformity
            uniformity_r = np.std(hist_r.flatten())
            uniformity_g = np.std(hist_g.flatten())
            uniformity_b = np.std(hist_b.flatten())
            
            avg_uniformity = (uniformity_r + uniformity_g + uniformity_b) / 3
            
            if avg_uniformity < 100:  # Very uniform distribution might be artificial
                deepfake_analysis['technical_anomalies'].append('Unusual color distribution uniformity')
                deepfake_analysis['confidence'] += 0.2
            
            # 5. EXIF data analysis
            with Image.open(image_path) as pil_img:
                if hasattr(pil_img, '_getexif') and pil_img._getexif():
                    exif_dict = pil_img._getexif()
                    
                    # Check for missing camera information (common in generated images)
                    camera_tags = ['Make', 'Model', 'Software']
                    missing_camera_info = 0
                    
                    for tag_id, value in exif_dict.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag in camera_tags:
                            missing_camera_info -= 1
                    
                    if missing_camera_info >= 0:  # Missing typical camera EXIF
                        deepfake_analysis['indicators'].append('Missing typical camera EXIF data')
                        deepfake_analysis['confidence'] += 0.1
                else:
                    deepfake_analysis['indicators'].append('No EXIF data found')
                    deepfake_analysis['confidence'] += 0.1
            
            # Determine risk level based on confidence
            if deepfake_analysis['confidence'] >= 0.7:
                deepfake_analysis['risk_level'] = 'High'
            elif deepfake_analysis['confidence'] >= 0.4:
                deepfake_analysis['risk_level'] = 'Medium'
            else:
                deepfake_analysis['risk_level'] = 'Low'
            
            self.girly_print(f"🤖 Deepfake risk: {deepfake_analysis['risk_level']} ({deepfake_analysis['confidence']:.2f})", "INFO", "📊")
            
            return deepfake_analysis
            
        except Exception as e:
            deepfake_analysis['error'] = str(e)
            self.girly_print(f"❌ Deepfake analysis failed: {str(e)[:50]}...", "ERROR", "💔")
            return deepfake_analysis

    def analyze_aesthetic_quality(self, image_path: str) -> Dict:
        """
        🎨 Analyze aesthetic quality and Instagram-specific features
        
        Args:
            image_path: Path to image file
            
        Returns:
            Aesthetic analysis results
        """
        self.girly_print(f"🎨 Analyzing aesthetic quality: {Path(image_path).name}", "INFO", "✨")
        
        aesthetic = {
            'overall_score': 0.0,
            'composition': {},
            'color_analysis': {},
            'technical_quality': {},
            'instagram_features': {}
        }
        
        try:
            if not CV2_AVAILABLE:
                aesthetic['error'] = 'OpenCV not available'
                return aesthetic
            
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                aesthetic['error'] = 'Could not load image'
                return aesthetic
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width = img.shape[:2]
            
            # 1. Composition analysis
            aspect_ratio = width / height
            
            # Check for common Instagram ratios
            instagram_ratios = {
                1.0: 'Square (1:1)',
                1.25: 'Portrait (4:5)',
                0.8: 'Portrait (4:5)',
                1.91: 'Landscape (16:9)',
                0.52: 'Story (9:16)'
            }
            
            closest_ratio = min(instagram_ratios.keys(), key=lambda x: abs(x - aspect_ratio))
            if abs(closest_ratio - aspect_ratio) < 0.1:
                aesthetic['composition']['aspect_ratio'] = instagram_ratios[closest_ratio]
                aesthetic['instagram_features']['optimized_ratio'] = True
            else:
                aesthetic['composition']['aspect_ratio'] = f'Custom ({aspect_ratio:.2f}:1)'
                aesthetic['instagram_features']['optimized_ratio'] = False
            
            # Rule of thirds analysis
            thirds_x = [width // 3, 2 * width // 3]
            thirds_y = [height // 3, 2 * height // 3]
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Find interesting points (corners)
            corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
            
            rule_of_thirds_score = 0
            if corners is not None:
                for corner in corners:
                    x, y = corner.ravel()
                    # Check if corner is near rule of thirds lines
                    for tx in thirds_x:
                        if abs(x - tx) < width * 0.05:  # Within 5% of line
                            rule_of_thirds_score += 1
                    for ty in thirds_y:
                        if abs(y - ty) < height * 0.05:
                            rule_of_thirds_score += 1
                
                aesthetic['composition']['rule_of_thirds_score'] = min(rule_of_thirds_score / 10, 1.0)
            
            # 2. Color analysis
            # Color harmony
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hue_hist = cv2.calcHist([img_hsv], [0], None, [180], [0, 180])
            
            # Find dominant hues
            dominant_hues = np.argsort(hue_hist.flatten())[-3:]  # Top 3 hues
            
            # Color temperature analysis
            b, g, r = cv2.split(img)
            avg_b, avg_g, avg_r = np.mean(b), np.mean(g), np.mean(r)
            
            if avg_r > avg_b:
                color_temp = 'Warm'
            else:
                color_temp = 'Cool'
            
            aesthetic['color_analysis'] = {
                'dominant_hues': dominant_hues.tolist(),
                'color_temperature': color_temp,
                'saturation_avg': np.mean(img_hsv[:, :, 1]),
                'brightness_avg': np.mean(img_hsv[:, :, 2])
            }
            
            # 3. Technical quality
            # Sharpness
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            sharpness_score = min(laplacian_var / 1000, 1.0)
            
            # Contrast
            contrast = gray.std()
            contrast_score = min(contrast / 70, 1.0)
            
            # Exposure analysis
            brightness_mean = np.mean(gray)
            if 85 <= brightness_mean <= 170:  # Well exposed
                exposure_score = 1.0
            else:
                exposure_score = max(0, 1 - abs(brightness_mean - 127.5) / 127.5)
            
            aesthetic['technical_quality'] = {
                'sharpness_score': sharpness_score,
                'contrast_score': contrast_score,
                'exposure_score': exposure_score,
                'overall_technical': (sharpness_score + contrast_score + exposure_score) / 3
            }
            
            # 4. Instagram-specific features
            # Filter detection (basic)
            # High saturation might indicate filter use
            saturation_mean = np.mean(img_hsv[:, :, 1])
            filter_likelihood = 'Low'
            if saturation_mean > 150:
                filter_likelihood = 'High'
            elif saturation_mean > 100:
                filter_likelihood = 'Medium'
            
            aesthetic['instagram_features'] = {
                'filter_likelihood': filter_likelihood,
                'saturation_level': saturation_mean,
                'professional_quality': aesthetic['technical_quality']['overall_technical'] > 0.7
            }
            
            # 5. Overall aesthetic score
            composition_score = aesthetic['composition'].get('rule_of_thirds_score', 0.5)
            technical_score = aesthetic['technical_quality']['overall_technical']
            color_score = min(aesthetic['color_analysis']['saturation_avg'] / 255, 1.0)
            
            aesthetic['overall_score'] = (composition_score + technical_score + color_score) / 3
            
            self.girly_print(f"🎨 Aesthetic score: {aesthetic['overall_score']:.2f}/1.0", "SUCCESS", "✨")
            
            return aesthetic
            
        except Exception as e:
            aesthetic['error'] = str(e)
            self.girly_print(f"❌ Aesthetic analysis failed: {str(e)[:50]}...", "ERROR", "💔")
            return aesthetic

    def analyze_single_image(self, image_path: str, image_url: str = None) -> Dict:
        """
        🔍 Complete analysis of a single image
        
        Args:
            image_path: Path to image file
            image_url: Original URL (optional)
            
        Returns:
            Complete analysis results
        """
        self.girly_print(f"🔍 Starting complete analysis: {Path(image_path).name}", "INFO", "🚀")
        
        analysis_start = time.time()
        
        image_analysis = {
            'image_path': image_path,
            'image_url': image_url,
            'analysis_id': f"IMG_{int(time.time())}_{hashlib.md5(image_path.encode()).hexdigest()[:8]}",
            'timestamp': datetime.now().isoformat(),
            'metadata': {},
            'faces': {},
            'deepfake': {},
            'aesthetic': {},
            'analysis_duration': 0
        }
        
        try:
            # 1. Metadata extraction
            self.girly_print("📊 Phase 1: Metadata Extraction", "INFO", "🔍")
            image_analysis['metadata'] = self.extract_advanced_metadata(image_path)
            
            # 2. Face detection
            self.girly_print("👥 Phase 2: Face Detection", "INFO", "🔍")
            image_analysis['faces'] = self.detect_faces(image_path)
            
            # 3. Deepfake analysis
            self.girly_print("🤖 Phase 3: Deepfake Analysis", "INFO", "🔍")
            image_analysis['deepfake'] = self.detect_deepfake_indicators(image_path)
            
            # 4. Aesthetic analysis
            self.girly_print("🎨 Phase 4: Aesthetic Analysis", "INFO", "🔍")
            image_analysis['aesthetic'] = self.analyze_aesthetic_quality(image_path)
            
            # Calculate analysis duration
            image_analysis['analysis_duration'] = round(time.time() - analysis_start, 2)
            
            # Add to results
            self.results['images_analyzed'].append(image_analysis)
            self.results['total_images'] += 1
            
            self.girly_print(f"✅ Analysis complete in {image_analysis['analysis_duration']}s", "SUCCESS", "🎉")
            
            return image_analysis
            
        except Exception as e:
            image_analysis['error'] = str(e)
            self.girly_print(f"❌ Analysis failed: {str(e)[:50]}...", "ERROR", "💔")
            return image_analysis

    def analyze_multiple_images(self, image_paths: List[str], image_urls: List[str] = None) -> Dict:
        """
        🎯 Analyze multiple images
        
        Args:
            image_paths: List of image file paths
            image_urls: List of original URLs (optional)
            
        Returns:
            Batch analysis results
        """
        self.girly_print(f"🎯 Starting batch analysis: {len(image_paths)} images", "INFO", "🚀")
        
        batch_start = time.time()
        
        if image_urls is None:
            image_urls = [None] * len(image_paths)
        
        batch_results = {
            'batch_id': f"BATCH_{int(time.time())}",
            'total_images': len(image_paths),
            'successful_analyses': 0,
            'failed_analyses': 0,
            'batch_duration': 0,
            'summary': {},
            'individual_results': []
        }
        
        # Analyze each image
        for i, (image_path, image_url) in enumerate(zip(image_paths, image_urls)):
            self.girly_print(f"📊 Analyzing image {i+1}/{len(image_paths)}", "INFO", "🔄")
            
            try:
                result = self.analyze_single_image(image_path, image_url)
                batch_results['individual_results'].append(result)
                
                if 'error' not in result:
                    batch_results['successful_analyses'] += 1
                else:
                    batch_results['failed_analyses'] += 1
                    
            except Exception as e:
                batch_results['failed_analyses'] += 1
                self.girly_print(f"❌ Failed to analyze {Path(image_path).name}: {e}", "ERROR", "💔")
        
        # Generate batch summary
        batch_results['batch_duration'] = round(time.time() - batch_start, 2)
        batch_results['summary'] = self.generate_batch_summary(batch_results['individual_results'])
        
        self.girly_print(f"🎉 Batch analysis complete: {batch_results['successful_analyses']}/{batch_results['total_images']} successful", "SUCCESS", "✅")
        
        return batch_results

    def generate_batch_summary(self, individual_results: List[Dict]) -> Dict:
        """
        📊 Generate summary from batch analysis
        
        Args:
            individual_results: List of individual analysis results
            
        Returns:
            Batch summary
        """
        successful_results = [r for r in individual_results if 'error' not in r]
        
        if not successful_results:
            return {'error': 'No successful analyses to summarize'}
        
        summary = {
            'face_detection': {
                'images_with_faces': 0,
                'total_faces_detected': 0,
                'average_faces_per_image': 0
            },
            'deepfake_analysis': {
                'high_risk_images': 0,
                'medium_risk_images': 0,
                'low_risk_images': 0
            },
            'aesthetic_quality': {
                'high_quality_images': 0,
                'medium_quality_images': 0,
                'low_quality_images': 0,
                'average_score': 0
            },
            'technical_findings': {
                'instagram_optimized': 0,
                'filter_likely': 0,
                'professional_quality': 0
            }
        }
        
        try:
            total_faces = 0
            total_aesthetic_score = 0
            
            for result in successful_results:
                # Face detection summary
                face_count = result.get('faces', {}).get('total_faces', 0)
                if face_count > 0:
                    summary['face_detection']['images_with_faces'] += 1
                    total_faces += face_count
                
                # Deepfake summary
                deepfake_risk = result.get('deepfake', {}).get('risk_level', 'Low')
                if deepfake_risk == 'High':
                    summary['deepfake_analysis']['high_risk_images'] += 1
                elif deepfake_risk == 'Medium':
                    summary['deepfake_analysis']['medium_risk_images'] += 1
                else:
                    summary['deepfake_analysis']['low_risk_images'] += 1
                
                # Aesthetic summary
                aesthetic_score = result.get('aesthetic', {}).get('overall_score', 0)
                total_aesthetic_score += aesthetic_score
                
                if aesthetic_score >= 0.7:
                    summary['aesthetic_quality']['high_quality_images'] += 1
                elif aesthetic_score >= 0.4:
                    summary['aesthetic_quality']['medium_quality_images'] += 1
                else:
                    summary['aesthetic_quality']['low_quality_images'] += 1
                
                # Technical findings
                instagram_features = result.get('aesthetic', {}).get('instagram_features', {})
                if instagram_features.get('optimized_ratio'):
                    summary['technical_findings']['instagram_optimized'] += 1
                if instagram_features.get('filter_likelihood') in ['High', 'Medium']:
                    summary['technical_findings']['filter_likely'] += 1
                if instagram_features.get('professional_quality'):
                    summary['technical_findings']['professional_quality'] += 1
            
            # Calculate averages
            summary['face_detection']['total_faces_detected'] = total_faces
            summary['face_detection']['average_faces_per_image'] = round(total_faces / len(successful_results), 2)
            summary['aesthetic_quality']['average_score'] = round(total_aesthetic_score / len(successful_results), 2)
            
            return summary
            
        except Exception as e:
            return {'error': f'Summary generation failed: {e}'}

    def generate_final_report(self, analysis_results: Dict) -> str:
        """
        📋 Generate comprehensive final report
        
        Args:
            analysis_results: Complete analysis results
            
        Returns:
            Formatted report string
        """
        
        report = f"""
🎨🔥 ULTIMATE INSTAGRAM IMAGE ANALYZER - FINAL REPORT 🔥🎨
{'='*80}

📊 ANALYSIS SUMMARY
Analyzer ID: {self.results['analyzer_id']}
Analysis Date: {self.results['analysis_timestamp']}
Total Images Analyzed: {self.results['total_images']}
"""
        
        if 'batch_id' in analysis_results:
            # Batch analysis report
            batch = analysis_results
            report += f"""
🎯 BATCH ANALYSIS RESULTS
Batch ID: {batch['batch_id']}
Total Images: {batch['total_images']}
Successful: {batch['successful_analyses']}
Failed: {batch['failed_analyses']}
Success Rate: {(batch['successful_analyses']/batch['total_images']*100):.1f}%
Duration: {batch['batch_duration']} seconds

"""
            
            if 'summary' in batch and 'error' not in batch['summary']:
                summary = batch['summary']
                
                report += f"""📊 BATCH SUMMARY
👥 Face Detection:
  • Images with faces: {summary['face_detection']['images_with_faces']}/{batch['successful_analyses']}
  • Total faces detected: {summary['face_detection']['total_faces_detected']}
  • Average faces per image: {summary['face_detection']['average_faces_per_image']}

🤖 Deepfake Analysis:
  • High risk images: {summary['deepfake_analysis']['high_risk_images']}
  • Medium risk images: {summary['deepfake_analysis']['medium_risk_images']}
  • Low risk images: {summary['deepfake_analysis']['low_risk_images']}

🎨 Aesthetic Quality:
  • High quality: {summary['aesthetic_quality']['high_quality_images']}
  • Medium quality: {summary['aesthetic_quality']['medium_quality_images']}
  • Low quality: {summary['aesthetic_quality']['low_quality_images']}
  • Average score: {summary['aesthetic_quality']['average_score']:.2f}/1.0

📱 Instagram Features:
  • Optimized ratio: {summary['technical_findings']['instagram_optimized']}
  • Filter likely: {summary['technical_findings']['filter_likely']}
  • Professional quality: {summary['technical_findings']['professional_quality']}

"""
        
        else:
            # Single image analysis report
            img = analysis_results
            report += f"""
🖼️ SINGLE IMAGE ANALYSIS
Image: {Path(img['image_path']).name}
Analysis ID: {img['analysis_id']}
Duration: {img['analysis_duration']} seconds

"""
            
            # Metadata summary
            if 'metadata' in img and img['metadata']:
                metadata = img['metadata']
                if 'file_info' in metadata:
                    file_info = metadata['file_info']
                    report += f"""📁 File Information:
  • Size: {file_info.get('size_mb', 'Unknown')} MB
  • Dimensions: {file_info.get('dimensions', 'Unknown')}
  • Format: {file_info.get('format', 'Unknown')}
  • Aspect Ratio: {file_info.get('aspect_ratio', 'Unknown')}

"""
                
                if 'exif_data' in metadata and metadata['exif_data']:
                    report += f"📊 EXIF Data: {len(metadata['exif_data'])} tags found\n"
            
            # Face detection results
            if 'faces' in img and img['faces']:
                faces = img['faces']
                report += f"""👥 Face Detection:
  • Total faces: {faces.get('total_faces', 0)}
  • Method: {faces.get('analysis_method', 'Unknown')}
"""
                
                if faces.get('total_faces', 0) > 0:
                    for i, face in enumerate(faces.get('faces', [])[:3], 1):  # Show first 3 faces
                        report += f"  • Face {i}: {face.get('width', 'Unknown')}x{face.get('height', 'Unknown')} pixels\n"
            
            # Deepfake analysis
            if 'deepfake' in img and img['deepfake']:
                deepfake = img['deepfake']
                report += f"""🤖 Deepfake Analysis:
  • Risk Level: {deepfake.get('risk_level', 'Unknown')}
  • Confidence: {deepfake.get('confidence', 0):.2f}
  • Indicators Found: {len(deepfake.get('indicators', []))}
"""
            
            # Aesthetic analysis
            if 'aesthetic' in img and img['aesthetic']:
                aesthetic = img['aesthetic']
                report += f"""🎨 Aesthetic Analysis:
  • Overall Score: {aesthetic.get('overall_score', 0):.2f}/1.0
  • Composition: {aesthetic.get('composition', {}).get('aspect_ratio', 'Unknown')}
  • Technical Quality: {aesthetic.get('technical_quality', {}).get('overall_technical', 0):.2f}
"""
                
                ig_features = aesthetic.get('instagram_features', {})
                if ig_features:
                    report += f"""📱 Instagram Features:
  • Optimized Ratio: {ig_features.get('optimized_ratio', False)}
  • Filter Likelihood: {ig_features.get('filter_likelihood', 'Unknown')}
  • Professional Quality: {ig_features.get('professional_quality', False)}
"""
        
        report += f"""
💡 RECOMMENDATIONS
"""
        
        if 'batch_id' in analysis_results:
            batch = analysis_results
            success_rate = (batch['successful_analyses']/batch['total_images']*100) if batch['total_images'] > 0 else 0
            
            if success_rate >= 80:
                report += """  ✅ Analysis highly successful
  📊 Quality data obtained from most images
  🔍 Consider deeper analysis of flagged images
  📋 Use results for comprehensive profiling
"""
            elif success_rate >= 50:
                report += """  ⚠️ Partial analysis success
  🔍 Some images may need reprocessing
  📊 Focus on successfully analyzed images
  🔄 Retry failed analyses with different methods
"""
            else:
                report += """  ❌ Low analysis success rate
  🛡️ Images may have strong protection
  🔍 Try alternative analysis methods
  ⏰ Consider manual review of failed images
"""
        
        report += f"""
💖 Generated by น้องจิน's Ultimate Image Analyzer
👻 For educational and security research only!
🔥 Report ID: {self.results['analyzer_id']}_{int(time.time())}

⚠️ DISCLAIMER: Use responsibly and ethically!
"""
        
        return report

def main():
    """Main function - interactive menu"""
    print(GIRLY_BANNER)
    
    analyzer = UltimateImageAnalyzer()
    
    while True:
        print("\n💖 ULTIMATE IMAGE ANALYZER MENU 💖")
        print("1. 🖼️ Analyze Single Image (from file)")
        print("2. 📥 Download & Analyze Image (from URL)")
        print("3. 📁 Batch Analyze Images (folder)")
        print("4. 🎯 Quick Face Detection Only")
        print("5. 🤖 Quick Deepfake Check Only")
        print("0. 💔 Exit")
        
        choice = input("\n💖 เลือกเมนู (0-5): ").strip()
        
        try:
            if choice == '1':
                # Single image analysis
                image_path = input("🖼️ Image file path: ").strip()
                if image_path and Path(image_path).exists():
                    result = analyzer.analyze_single_image(image_path)
                    report = analyzer.generate_final_report(result)
                    print(report)
                    
                    # Save report
                    timestamp = int(time.time())
                    report_file = Path(f"image_analysis_report_{timestamp}.txt")
                    with open(report_file, 'w', encoding='utf-8') as f:
                        f.write(report)
                    print(f"📋 Report saved: {report_file.name}")
                else:
                    print("❌ File not found")
            
            elif choice == '2':
                # Download and analyze
                image_url = input("📥 Image URL: ").strip()
                if image_url:
                    timestamp = int(time.time())
                    filename = f"downloaded_image_{timestamp}.jpg"
                    
                    if analyzer.download_image(image_url, filename):
                        result = analyzer.analyze_single_image(filename, image_url)
                        report = analyzer.generate_final_report(result)
                        print(report)
                        
                        # Save report
                        report_file = Path(f"image_analysis_report_{timestamp}.txt")
                        with open(report_file, 'w', encoding='utf-8') as f:
                            f.write(report)
                        print(f"📋 Report saved: {report_file.name}")
            
            elif choice == '3':
                # Batch analysis
                folder_path = input("📁 Folder path with images: ").strip()
                if folder_path and Path(folder_path).exists():
                    # Find image files
                    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
                    image_files = []
                    
                    for ext in image_extensions:
                        image_files.extend(Path(folder_path).glob(f"*{ext}"))
                        image_files.extend(Path(folder_path).glob(f"*{ext.upper()}"))
                    
                    if image_files:
                        image_paths = [str(f) for f in image_files[:10]]  # Limit to 10 images
                        print(f"📊 Found {len(image_files)} images, analyzing first {len(image_paths)}")
                        
                        result = analyzer.analyze_multiple_images(image_paths)
                        report = analyzer.generate_final_report(result)
                        print(report)
                        
                        # Save report
                        timestamp = int(time.time())
                        report_file = Path(f"batch_analysis_report_{timestamp}.txt")
                        with open(report_file, 'w', encoding='utf-8') as f:
                            f.write(report)
                        print(f"📋 Report saved: {report_file.name}")
                    else:
                        print("❌ No image files found")
                else:
                    print("❌ Folder not found")
            
            elif choice == '4':
                # Quick face detection
                image_path = input("👥 Image file path: ").strip()
                if image_path and Path(image_path).exists():
                    faces = analyzer.detect_faces(image_path)
                    print(f"👥 Found {faces.get('total_faces', 0)} faces")
                    if faces.get('total_faces', 0) > 0:
                        for i, face in enumerate(faces.get('faces', []), 1):
                            print(f"  Face {i}: {face}")
                else:
                    print("❌ File not found")
            
            elif choice == '5':
                # Quick deepfake check
                image_path = input("🤖 Image file path: ").strip()
                if image_path and Path(image_path).exists():
                    deepfake = analyzer.detect_deepfake_indicators(image_path)
                    print(f"🤖 Deepfake Risk: {deepfake.get('risk_level', 'Unknown')}")
                    print(f"🎯 Confidence: {deepfake.get('confidence', 0):.2f}")
                    if deepfake.get('indicators'):
                        print("🔍 Indicators:")
                        for indicator in deepfake['indicators']:
                            print(f"  • {indicator}")
                else:
                    print("❌ File not found")
            
            elif choice == '0':
                print("👋 บาย! ใช้งานให้เป็นประโยชน์นะคะ ♥️")
                break
                
            else:
                print("❌ เลือกเมนูให้ถูกนะคะ")
                
        except KeyboardInterrupt:
            print("\n⚠️ หยุดการทำงาน")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
