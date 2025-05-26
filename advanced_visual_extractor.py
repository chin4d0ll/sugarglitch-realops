#!/usr/bin/env python3
"""
ADVANCED VISUAL EXTRACTION SYSTEM 📸💀
สำหรับดึงรูปจากบัญชีตัวเองแบบโหดๆ
"""

import json
import requests
import os
from datetime import datetime
import time
import random
from urllib.parse import urlparse
from pathlib import Path
from typing import Dict, List, Optional

class AdvancedVisualExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.download_folder = "/workspaces/sugarglitch-realops/extracted_images"
        self.setup_download_folder()
        self.setup_stealth_session()
        
    def setup_download_folder(self):
        """สร้าง folder สำหรับดาวน์โหลดรูป"""
        Path(self.download_folder).mkdir(exist_ok=True)
        print(f"📁 Download folder: {self.download_folder}")
    
    def setup_stealth_session(self):
        """ตั้งค่า stealth headers สำหรับดาวน์โหลด"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        self.session.headers.update(headers)
    
    def ghost_delay(self, min_delay: float = 0.5, max_delay: float = 2.0):
        """Human-like delay"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def download_image(self, url: str, filename: str) -> bool:
        """ดาวน์โหลดรูปแบบ stealth mode"""
        
        if not url:
            return False
            
        try:
            self.ghost_delay(0.3, 1.5)
            
            print(f"📥 Downloading: {filename}")
            response = self.session.get(url, timeout=30, stream=True)
            
            if response.status_code == 200:
                filepath = os.path.join(self.download_folder, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                file_size = os.path.getsize(filepath)
                print(f"✅ Downloaded: {filename} ({file_size} bytes)")
                return True
            else:
                print(f"❌ Download failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"💀 Download error: {e}")
            return False
    
    def extract_from_json(self, json_file: str) -> Dict:
        """ดึงรูปจาก extraction results"""
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📊 Processing: {json_file}")
            
            results = {
                'profile_pic': None,
                'posts': [],
                'total_downloaded': 0,
                'download_folder': self.download_folder
            }
            
            # ดึง Profile Picture
            profile = data.get('profile', {})
            if profile and profile.get('profile_pic_url'):
                username = profile.get('username', 'unknown')
                profile_filename = f"{username}_profile.jpg"
                
                if self.download_image(profile['profile_pic_url'], profile_filename):
                    results['profile_pic'] = profile_filename
                    results['total_downloaded'] += 1
            
            # ดึงรูปจากโพสต์
            posts = data.get('posts', [])
            
            for i, post in enumerate(posts):
                if post.get('display_url'):
                    shortcode = post.get('shortcode', f'post_{i}')
                    post_filename = f"post_{shortcode}.jpg"
                    
                    if self.download_image(post['display_url'], post_filename):
                        post_info = {
                            'filename': post_filename,
                            'shortcode': shortcode,
                            'caption': post.get('caption', '')[:100] + '...' if len(post.get('caption', '')) > 100 else post.get('caption', ''),
                            'like_count': post.get('like_count'),
                            'comment_count': post.get('comment_count')
                        }
                        results['posts'].append(post_info)
                        results['total_downloaded'] += 1
                
                # ดาวน์โหลดวิดีโอถ้ามี
                if post.get('is_video') and post.get('video_url'):
                    shortcode = post.get('shortcode', f'video_{i}')
                    video_filename = f"video_{shortcode}.mp4"
                    
                    if self.download_image(post['video_url'], video_filename):
                        results['total_downloaded'] += 1
            
            return results
            
        except Exception as e:
            print(f"💀 JSON processing error: {e}")
            return {}
    
    def create_download_summary(self, results: Dict, username: str):
        """สร้าง summary ของการดาวน์โหลด"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"DOWNLOAD_SUMMARY_{username}_{timestamp}.json"
        summary_path = os.path.join(self.download_folder, summary_file)
        
        summary = {
            'username': username,
            'download_timestamp': datetime.now().isoformat(),
            'total_files': results['total_downloaded'],
            'profile_pic': results['profile_pic'],
            'posts_downloaded': len(results['posts']),
            'download_folder': self.download_folder,
            'files': results['posts']
        }
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary saved: {summary_file}")
        
        # สร้าง HTML gallery
        self.create_html_gallery(summary, username)
        
        return summary_path
    
    def create_html_gallery(self, summary: Dict, username: str):
        """สร้าง HTML gallery สำหรับดูรูป"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Gallery - {username}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #000;
            color: #fff;
            margin: 0;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .profile {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .profile img {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 3px solid #ff0040;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .post {{
            background: #1a1a1a;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #333;
        }}
        .post img {{
            width: 100%;
            height: 300px;
            object-fit: cover;
        }}
        .post-info {{
            padding: 15px;
        }}
        .stats {{
            color: #ff0040;
            font-weight: bold;
        }}
        .caption {{
            margin-top: 10px;
            color: #ccc;
            font-size: 14px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 INSTAGRAM GALLERY 🔥</h1>
        <h2>@{username}</h2>
        <p>Downloaded: {summary['download_timestamp']}</p>
        <p>Total Files: {summary['total_files']}</p>
    </div>
    
    <div class="profile">
        {f'<img src="{summary["profile_pic"]}" alt="Profile Picture">' if summary.get('profile_pic') else '<div>No profile picture</div>'}
    </div>
    
    <div class="gallery">
"""
        
        for post in summary.get('files', []):
            html_content += f"""
        <div class="post">
            <img src="{post['filename']}" alt="Post">
            <div class="post-info">
                <div class="stats">
                    ❤️ {post.get('like_count', 0)} | 💬 {post.get('comment_count', 0)}
                </div>
                <div class="caption">{post.get('caption', 'No caption')}</div>
            </div>
        </div>
"""
        
        html_content += """
    </div>
    
    <div class="footer">
        <p>🔥 Generated by Ultimate Stealth Extractor 🔥</p>
    </div>
</body>
</html>
"""
        
        html_file = os.path.join(self.download_folder, f"gallery_{username}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🎨 HTML Gallery created: gallery_{username}.html")
    
    def full_visual_extraction(self, extraction_file: str, username: str = None):
        """ดึงรูปครบถ้วนจาก extraction file"""
        
        if not username:
            username = "unknown"
        
        print(f"""
📸💀 ADVANCED VISUAL EXTRACTION STARTED 💀📸
Source: {extraction_file}
Target: {username}
Mode: MAXIMUM_DOWNLOAD
""")
        
        results = self.extract_from_json(extraction_file)
        
        if results['total_downloaded'] > 0:
            summary_path = self.create_download_summary(results, username)
            
            print(f"""
🎯 VISUAL EXTRACTION COMPLETE! 🎯
================================
✅ Profile Pic: {'✓' if results['profile_pic'] else '✗'}
✅ Posts: {len(results['posts'])}
✅ Total Files: {results['total_downloaded']}
📁 Folder: {self.download_folder}
📋 Summary: {summary_path}
🎨 Gallery: gallery_{username}.html
""")
        else:
            print("❌ No images downloaded")
        
        return results

def main():
    """Main execution"""
    
    print("""
📸💀 ADVANCED VISUAL EXTRACTION SYSTEM 💀📸
==========================================
[MODE] STEALTH_DOWNLOAD
[TARGET] PERSONAL_ACCOUNT_IMAGES
""")
    
    extractor = AdvancedVisualExtractor()
    
    # หาไฟล์ extraction ล่าสุด
    extraction_files = [
        f for f in os.listdir('/workspaces/sugarglitch-realops/')
        if f.startswith('ULTIMATE_STEALTH_') and f.endswith('.json')
    ]
    
    if extraction_files:
        latest_file = max(extraction_files, key=lambda x: os.path.getctime(f'/workspaces/sugarglitch-realops/{x}'))
        full_path = f'/workspaces/sugarglitch-realops/{latest_file}'
        
        print(f"📂 Using extraction file: {latest_file}")
        
        results = extractor.full_visual_extraction(full_path, "whatilove1728")
        
    else:
        print("❌ No extraction files found. Run ultimate_stealth_extractor.py first!")

if __name__ == "__main__":
    main()
