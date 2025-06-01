#!/usr/bin/env python3
"""
🔍 Advanced Image Discovery and Recovery Tool
ค้นหาและกู้คืนรูปภาพขั้นสูง

This script scans the entire workspace for images and attempts to recover
Instagram images that may have been extracted but moved or deleted.
"""

import os
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import mimetypes
import base64

class ImageDiscoveryTool:
    def __init__(self, workspace_path="/workspaces/sugarglitch-realops"):
        self.workspace_path = Path(workspace_path)
        self.found_images = []
        self.recovered_images = []
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.tiff'}
        
    def scan_workspace(self):
        """Scan entire workspace for images"""
        print("🔍 กำลังสแกนหารูปภาพ... Scanning for images...")
        
        for root, dirs, files in os.walk(self.workspace_path):
            # Skip hidden directories and cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for file in files:
                file_path = Path(root) / file
                
                if file_path.suffix.lower() in self.image_extensions:
                    try:
                        size = file_path.stat().st_size
                        self.found_images.append({
                            'path': str(file_path),
                            'name': file,
                            'size': size,
                            'size_mb': round(size / (1024 * 1024), 2),
                            'extension': file_path.suffix.lower(),
                            'directory': str(file_path.parent.relative_to(self.workspace_path))
                        })
                    except Exception as e:
                        print(f"⚠️ Error reading {file_path}: {e}")
        
        print(f"✅ พบรูปภาพทั้งหมด {len(self.found_images)} ไฟล์")
        return self.found_images
    
    def analyze_json_files(self):
        """Analyze JSON files for image data or references"""
        print("📊 กำลังวิเคราะห์ไฟล์ JSON... Analyzing JSON files...")
        
        image_references = []
        json_files = list(self.workspace_path.rglob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Look for image-related data
                self._extract_image_refs(data, json_file, image_references)
                    
            except Exception as e:
                print(f"⚠️ Error reading {json_file}: {e}")
        
        return image_references
    
    def _extract_image_refs(self, data, source_file, refs):
        """Recursively extract image references from JSON data"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    # Check for URLs, file paths, or base64 encoded images
                    if any(ext in value.lower() for ext in self.image_extensions):
                        refs.append({
                            'source': str(source_file),
                            'key': key,
                            'value': value,
                            'type': 'file_reference'
                        })
                    elif value.startswith(('http', 'https')) and any(ext in value for ext in ['.jpg', '.png', '.gif']):
                        refs.append({
                            'source': str(source_file),
                            'key': key,
                            'value': value,
                            'type': 'url'
                        })
                    elif value.startswith('data:image/'):
                        refs.append({
                            'source': str(source_file),
                            'key': key,
                            'value': value[:100] + "...",  # Truncate for display
                            'type': 'base64_image'
                        })
                elif isinstance(value, (dict, list)):
                    self._extract_image_refs(value, source_file, refs)
        elif isinstance(data, list):
            for item in data:
                self._extract_image_refs(item, source_file, refs)
    
    def create_recovery_directory(self):
        """Create directory for recovered images"""
        recovery_dir = self.workspace_path / "recovered_images"
        recovery_dir.mkdir(exist_ok=True)
        return recovery_dir
    
    def attempt_image_recovery(self):
        """Attempt to recover images from various sources"""
        print("🔧 กำลังพยายามกู้คืนรูปภาพ... Attempting image recovery...")
        
        recovery_dir = self.create_recovery_directory()
        recovered_count = 0
        
        # Check for temporary files, browser cache, etc.
        potential_locations = [
            self.workspace_path / "temp",
            self.workspace_path / ".cache",
            self.workspace_path / "downloads",
            Path.home() / "Downloads",
            Path("/tmp") if os.path.exists("/tmp") else None
        ]
        
        for location in potential_locations:
            if location and location.exists():
                for file_path in location.rglob("*"):
                    if file_path.is_file() and file_path.suffix.lower() in self.image_extensions:
                        if "whatilove1728" in str(file_path).lower():
                            try:
                                dest = recovery_dir / f"recovered_{file_path.name}"
                                shutil.copy2(file_path, dest)
                                recovered_count += 1
                                print(f"✅ Recovered: {file_path.name}")
                            except Exception as e:
                                print(f"⚠️ Failed to recover {file_path}: {e}")
        
        return recovered_count
    
    def generate_report(self):
        """Generate comprehensive image discovery report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {
            "scan_date": datetime.now().isoformat(),
            "workspace_path": str(self.workspace_path),
            "total_images_found": len(self.found_images),
            "images_by_extension": {},
            "images_by_directory": {},
            "largest_images": [],
            "found_images": self.found_images
        }
        
        # Group by extension
        for img in self.found_images:
            ext = img['extension']
            if ext not in report['images_by_extension']:
                report['images_by_extension'][ext] = 0
            report['images_by_extension'][ext] += 1
        
        # Group by directory
        for img in self.found_images:
            dir_name = img['directory']
            if dir_name not in report['images_by_directory']:
                report['images_by_directory'][dir_name] = 0
            report['images_by_directory'][dir_name] += 1
        
        # Find largest images
        report['largest_images'] = sorted(
            self.found_images, 
            key=lambda x: x['size'], 
            reverse=True
        )[:10]
        
        # Save report
        report_file = self.workspace_path / f"image_discovery_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report, report_file
    
    def create_image_gallery_html(self, report):
        """Create an enhanced HTML gallery with all found images"""
        html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖼️ Complete Image Gallery - แกลเลอรี่รูปภาพ</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }}
        .image-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .image-card:hover {{
            transform: translateY(-5px);
        }}
        .image-card img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            cursor: pointer;
        }}
        .image-info {{
            margin-top: 10px;
            font-size: 0.9em;
        }}
        .filter-section {{
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        select, input {{
            padding: 8px 12px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Complete Image Gallery - แกลเลอรี่รูปภาพครบถ้วน</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{report['total_images_found']}</div>
                <div>Total Images</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(report['images_by_extension'])}</div>
                <div>File Types</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(report['images_by_directory'])}</div>
                <div>Directories</div>
            </div>
        </div>
        
        <div class="filter-section">
            <h3>🔍 Filter Images - กรองรูปภาพ</h3>
            <select id="extensionFilter" onchange="filterImages()">
                <option value="">All Extensions</option>"""
        
        for ext in report['images_by_extension'].keys():
            html_content += f'<option value="{ext}">{ext.upper()} ({report["images_by_extension"][ext]})</option>'
        
        html_content += """
            </select>
            <select id="directoryFilter" onchange="filterImages()">
                <option value="">All Directories</option>"""
        
        for dir_name in report['images_by_directory'].keys():
            html_content += f'<option value="{dir_name}">{dir_name} ({report["images_by_directory"][dir_name]})</option>'
        
        html_content += """
            </select>
            <input type="text" id="searchFilter" placeholder="Search by filename..." onkeyup="filterImages()">
        </div>
        
        <div class="image-grid" id="imageGrid">"""
        
        for img in report['found_images']:
            rel_path = Path(img['path']).relative_to(self.workspace_path)
            html_content += f"""
            <div class="image-card" data-extension="{img['extension']}" data-directory="{img['directory']}" data-name="{img['name'].lower()}">
                <img src="{rel_path}" alt="{img['name']}" onclick="openModal(this.src)" onerror="this.style.display='none'">
                <div class="image-info">
                    <strong>{img['name']}</strong><br>
                    📁 {img['directory']}<br>
                    📊 {img['size_mb']} MB
                </div>
            </div>"""
        
        html_content += """
        </div>
    </div>
    
    <script>
        function filterImages() {
            const extensionFilter = document.getElementById('extensionFilter').value;
            const directoryFilter = document.getElementById('directoryFilter').value;
            const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
            const cards = document.querySelectorAll('.image-card');
            
            cards.forEach(card => {
                const extension = card.getAttribute('data-extension');
                const directory = card.getAttribute('data-directory');
                const name = card.getAttribute('data-name');
                
                const matchesExtension = !extensionFilter || extension === extensionFilter;
                const matchesDirectory = !directoryFilter || directory === directoryFilter;
                const matchesSearch = !searchFilter || name.includes(searchFilter);
                
                if (matchesExtension && matchesDirectory && matchesSearch) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        function openModal(src) {
            window.open(src, '_blank');
        }
    </script>
</body>
</html>"""
        
        gallery_file = self.workspace_path / "complete_image_gallery.html"
        with open(gallery_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return gallery_file

def main():
    print("🚀 Starting Advanced Image Discovery...")
    
    tool = ImageDiscoveryTool()
    
    # Scan for images
    found_images = tool.scan_workspace()
    
    # Analyze JSON files for image references
    image_refs = tool.analyze_json_files()
    
    # Attempt recovery
    recovered_count = tool.attempt_image_recovery()
    
    # Generate report
    report, report_file = tool.generate_report()
    
    # Create enhanced gallery
    gallery_file = tool.create_image_gallery_html(report)
    
    print(f"""
    ✅ Image Discovery Complete!
    
    📊 Summary:
    - Found {len(found_images)} images
    - Found {len(image_refs)} image references in JSON files
    - Recovered {recovered_count} Instagram images
    - Report saved: {report_file}
    - Gallery created: {gallery_file}
    
    🌐 Open the gallery in your browser to view all images!
    """)

if __name__ == "__main__":
    main()
