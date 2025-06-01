#!/usr/bin/env python3
"""
🖼️ Simple Image Viewer - Local Files Only
ดูรูปภาพที่มีอยู่ในเครื่องและแสดงรายละเอียด
"""

import os
from pathlib import Path
import json
from datetime import datetime

def find_all_images():
    """ค้นหารูปภาพทั้งหมดในพื้นที่ทำงาน"""
    base_dir = Path("/workspaces/sugarglitch-realops")
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
    
    images = []
    
    print("🔍 กำลังค้นหารูปภาพ...")
    
    for file_path in base_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            try:
                stat = file_path.stat()
                images.append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024*1024), 2),
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'extension': file_path.suffix.lower(),
                    'relative_path': str(file_path.relative_to(base_dir))
                })
            except Exception as e:
                print(f"⚠️ Error reading {file_path}: {e}")
    
    return images

def create_enhanced_viewer(images):
    """สร้าง HTML viewer ที่ปรับปรุงแล้ว"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖼️ Enhanced Image Viewer - {len(images)} Images</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .controls {{
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 250px;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-select {{
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            background: white;
        }}
        
        .clear-btn {{
            padding: 12px 20px;
            background: #ff6b6b;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }}
        
        .clear-btn:hover {{
            background: #ff5252;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }}
        
        .image-card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
        }}
        
        .image-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        }}
        
        .image-container {{
            position: relative;
            width: 100%;
            height: 200px;
            overflow: hidden;
            background: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .image-container img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: cover;
            cursor: pointer;
            transition: transform 0.3s;
        }}
        
        .image-container:hover img {{
            transform: scale(1.05);
        }}
        
        .image-info {{
            padding: 15px;
        }}
        
        .image-name {{
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            word-break: break-all;
        }}
        
        .image-details {{
            color: #666;
            font-size: 0.9em;
            line-height: 1.4;
        }}
        
        .image-path {{
            color: #888;
            font-size: 0.8em;
            font-family: monospace;
            margin-top: 10px;
            padding: 8px;
            background: #f5f5f5;
            border-radius: 4px;
        }}
        
        .no-images {{
            text-align: center;
            color: #666;
            font-size: 1.2em;
            padding: 50px;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
        }}
        
        .modal-content {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            max-width: 90%;
            max-height: 90%;
        }}
        
        .modal-content img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
        
        .close {{
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }}
        
        .close:hover {{
            color: #fff;
        }}
        
        @media (max-width: 768px) {{
            .controls {{
                flex-direction: column;
            }}
            
            .search-box {{
                min-width: 100%;
            }}
            
            .gallery {{
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Enhanced Image Viewer</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(images)}</div>
                <div>Total Images</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(img['size'] for img in images) / (1024*1024):.1f}</div>
                <div>Total Size (MB)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(set(img['extension'] for img in images))}</div>
                <div>File Types</div>
            </div>
        </div>
        
        <div class="controls">
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 ค้นหาชื่อไฟล์หรือพาธ...">
            <select class="filter-select" id="filterSelect">
                <option value="">All Types</option>"""
    
    # Add file type options
    extensions = sorted(set(img['extension'] for img in images))
    for ext in extensions:
        count = len([img for img in images if img['extension'] == ext])
        html_content += f'<option value="{ext}">{ext.upper()} ({count})</option>'
    
    html_content += """</select>
            <button class="clear-btn" onclick="clearFilters()">Clear</button>
        </div>
        
        <div class="gallery" id="gallery">"""
    
    if not images:
        html_content += """
            <div class="no-images">
                ไม่พบรูปภาพในพื้นที่ทำงาน
            </div>"""
    else:
        for img in images:
            html_content += f"""
            <div class="image-card" data-name="{img['name'].lower()}" data-path="{img['relative_path'].lower()}" data-ext="{img['extension']}">
                <div class="image-container">
                    <img src="file://{img['path']}" alt="{img['name']}" onclick="openModal(this)">
                </div>
                <div class="image-info">
                    <div class="image-name">{img['name']}</div>
                    <div class="image-details">
                        Size: {img['size_mb']} MB<br>
                        Modified: {img['modified']}<br>
                        Type: {img['extension'].upper()}
                    </div>
                    <div class="image-path">{img['relative_path']}</div>
                </div>
            </div>"""
    
    html_content += """
        </div>
    </div>
    
    <!-- Modal for full-size image viewing -->
    <div id="imageModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <div class="modal-content">
            <img id="modalImage" src="" alt="">
        </div>
    </div>
    
    <script>
        function openModal(img) {
            document.getElementById('imageModal').style.display = 'block';
            document.getElementById('modalImage').src = img.src;
        }
        
        function closeModal() {
            document.getElementById('imageModal').style.display = 'none';
        }
        
        function clearFilters() {
            document.getElementById('searchBox').value = '';
            document.getElementById('filterSelect').value = '';
            filterImages();
        }
        
        function filterImages() {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            const filterType = document.getElementById('filterSelect').value;
            const cards = document.querySelectorAll('.image-card');
            
            cards.forEach(card => {
                const name = card.dataset.name;
                const path = card.dataset.path;
                const ext = card.dataset.ext;
                
                const matchesSearch = name.includes(searchTerm) || path.includes(searchTerm);
                const matchesFilter = !filterType || ext === filterType;
                
                card.style.display = (matchesSearch && matchesFilter) ? 'block' : 'none';
            });
        }
        
        // Event listeners
        document.getElementById('searchBox').addEventListener('input', filterImages);
        document.getElementById('filterSelect').addEventListener('change', filterImages);
        
        // Close modal when clicking outside
        document.getElementById('imageModal').onclick = function(event) {
            if (event.target === this) {
                closeModal();
            }
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModal();
            }
        });
        
        console.log('🖼️ Enhanced Image Viewer loaded with {len(images)} images');
    </script>
</body>
</html>"""
    
    return html_content

def main():
    print("🖼️ Simple Image Viewer - กำลังเริ่มต้น...")
    
    # Find all images
    images = find_all_images()
    
    print(f"✅ พบรูปภาพทั้งหมด: {len(images)} ไฟล์")
    
    if images:
        # Show summary
        print("\n📊 สรุปข้อมูล:")
        total_size = sum(img['size'] for img in images) / (1024*1024)
        extensions = {}
        for img in images:
            ext = img['extension']
            extensions[ext] = extensions.get(ext, 0) + 1
        
        print(f"   📁 ขนาดรวม: {total_size:.2f} MB")
        print(f"   🎯 ประเภทไฟล์: {len(extensions)} ชนิด")
        for ext, count in sorted(extensions.items()):
            print(f"      {ext.upper()}: {count} ไฟล์")
        
        # Create viewer
        html_content = create_enhanced_viewer(images)
        
        # Save HTML file
        output_file = "/workspaces/sugarglitch-realops/enhanced_image_viewer.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ Enhanced Image Viewer สร้างเสร็จแล้ว: {output_file}")
        print("🌐 เปิดไฟล์ HTML ในเบราว์เซอร์เพื่อดูรูปภาพ")
        
        # Save JSON report
        report_file = f"/workspaces/sugarglitch-realops/images_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_images': len(images),
                'total_size_mb': round(total_size, 2),
                'file_types': extensions,
                'images': images
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📄 รายงาน JSON: {report_file}")
        
    else:
        print("❌ ไม่พบรูปภาพในพื้นที่ทำงาน")

if __name__ == "__main__":
    main()
