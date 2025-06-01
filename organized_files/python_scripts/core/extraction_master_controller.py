#!/usr/bin/env python3
"""
🎯 Instagram Extraction Master Controller 2025 🎯
ตัวควบคุมหลักสำหรับการดึงข้อมูล Instagram

Features:
- Multiple extraction methods
- Automatic fallback strategies
- Error recovery
- Progress tracking
- Results consolidation
"""

import subprocess
import sys
import json
import time
from datetime import datetime
from pathlib import Path
import os

class ExtractionController:
    def __init__(self):
        self.workspace = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.workspace / "consolidated_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Available extractors (in order of safety/reliability)
        self.extractors = [
            {
                "name": "Safe Extractor",
                "file": "safe_instagram_extractor.py",
                "description": "🛡️ Safest method - no login required",
                "safety_level": "HIGH",
                "expected_success": "MEDIUM"
            },
            {
                "name": "Improved Extractor", 
                "file": "improved_instagram_extractor_fixed.py",
                "description": "🔧 Improved method with better error handling",
                "safety_level": "MEDIUM",
                "expected_success": "HIGH"
            },
            {
                "name": "Working Extractor",
                "file": "working_instagram_extractor_2025.py", 
                "description": "🔥 Working method with real credentials",
                "safety_level": "LOW",
                "expected_success": "HIGH"
            }
        ]
        
        print("🎯 Instagram Extraction Master Controller")
        print(f"📁 Results will be consolidated in: {self.results_dir}")
        
    def check_extractor_availability(self):
        """Check which extractors are available"""
        available = []
        
        for extractor in self.extractors:
            filepath = self.workspace / extractor["file"]
            if filepath.exists():
                available.append(extractor)
                print(f"✅ {extractor['name']}: Available")
            else:
                print(f"❌ {extractor['name']}: Not found ({extractor['file']})")
        
        return available
    
    def run_extractor(self, extractor: dict, timeout: int = 300) -> dict:
        """Run a specific extractor"""
        print(f"\n🚀 Running: {extractor['name']}")
        print(f"📄 Description: {extractor['description']}")
        print(f"🛡️ Safety Level: {extractor['safety_level']}")
        print(f"📈 Expected Success: {extractor['expected_success']}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            # Run the extractor
            result = subprocess.run(
                [sys.executable, extractor["file"]],
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            execution_time = time.time() - start_time
            
            return {
                "extractor": extractor["name"],
                "status": "completed" if result.returncode == 0 else "failed",
                "return_code": result.returncode,
                "execution_time": execution_time,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                "extractor": extractor["name"],
                "status": "timeout",
                "execution_time": timeout,
                "error": f"Timed out after {timeout} seconds",
                "success": False
            }
        except Exception as e:
            return {
                "extractor": extractor["name"],
                "status": "error",
                "execution_time": time.time() - start_time,
                "error": str(e),
                "success": False
            }
    
    def analyze_results(self) -> dict:
        """Analyze results from all extraction attempts"""
        print("\n📊 Analyzing extraction results...")
        
        analysis = {
            "analysis_time": datetime.now().isoformat(),
            "directories_scanned": [],
            "total_images_found": 0,
            "results_by_method": {},
            "best_results": None,
            "recommendations": []
        }
        
        # Scan for result directories
        result_dirs = [
            "safe_extraction_results",
            "improved_extraction_results", 
            "results",
            "extracted_images",
            "media/extracted"
        ]
        
        for dir_name in result_dirs:
            dir_path = self.workspace / dir_name
            if dir_path.exists():
                analysis["directories_scanned"].append(str(dir_path))
                
                # Count images in each directory
                image_count = 0
                if (dir_path / "images").exists():
                    image_count += len(list((dir_path / "images").glob("*.*")))
                if (dir_path / "downloaded_images").exists():
                    image_count += len(list((dir_path / "downloaded_images").glob("*.*")))
                
                analysis["results_by_method"][dir_name] = {
                    "image_count": image_count,
                    "directory": str(dir_path)
                }
                analysis["total_images_found"] += image_count
        
        # Find best method
        if analysis["results_by_method"]:
            best_method = max(
                analysis["results_by_method"].items(),
                key=lambda x: x[1]["image_count"]
            )
            analysis["best_results"] = {
                "method": best_method[0],
                "image_count": best_method[1]["image_count"],
                "directory": best_method[1]["directory"]
            }
        
        # Generate recommendations
        if analysis["total_images_found"] == 0:
            analysis["recommendations"] = [
                "❌ No images were extracted successfully",
                "🔄 Try running the Safe Extractor manually",
                "🌐 Check internet connection",
                "👤 Verify target usernames are public profiles",
                "⏱️ Consider trying again later (rate limits)"
            ]
        elif analysis["total_images_found"] < 5:
            analysis["recommendations"] = [
                "⚠️ Low image count - might be rate limited",
                "🔄 Try the next extractor method",
                "👤 Check if profiles are public",
                "⏱️ Wait longer between attempts"
            ]
        else:
            analysis["recommendations"] = [
                "✅ Good results obtained!",
                f"📁 Best results in: {analysis['best_results']['directory']}",
                "🖼️ Update image gallery to include new images",
                "💾 Backup results before running again"
            ]
        
        return analysis
    
    def create_consolidated_gallery(self, analysis: dict):
        """Create a consolidated gallery of all extracted images"""
        print("🖼️ Creating consolidated image gallery...")
        
        all_images = []
        
        # Scan all result directories for images
        for method, data in analysis["results_by_method"].items():
            method_dir = Path(data["directory"])
            
            # Look for images in common subdirectories
            image_dirs = [
                method_dir / "images",
                method_dir / "downloaded_images",
                method_dir
            ]
            
            for img_dir in image_dirs:
                if img_dir.exists():
                    for img_file in img_dir.glob("*.*"):
                        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                            rel_path = img_file.relative_to(self.workspace)
                            all_images.append({
                                "filename": img_file.name,
                                "path": str(rel_path),
                                "method": method,
                                "size": img_file.stat().st_size if img_file.exists() else 0
                            })
        
        # Create HTML gallery
        html_content = self.generate_gallery_html(all_images, analysis)
        gallery_file = self.results_dir / "consolidated_gallery.html"
        
        with open(gallery_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Consolidated gallery created: {gallery_file}")
        return gallery_file
    
    def generate_gallery_html(self, images: list, analysis: dict) -> str:
        """Generate HTML for consolidated gallery"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Consolidated Instagram Gallery - รวมรูป Instagram</title>
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
        .header {{
            text-align: center;
            margin-bottom: 30px;
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
        .method-section {{
            margin-bottom: 40px;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }}
        .image-card {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .image-card:hover {{
            transform: translateY(-5px);
        }}
        .image-card img {{
            width: 100%;
            height: 150px;
            object-fit: cover;
            cursor: pointer;
        }}
        .image-info {{
            padding: 10px;
            font-size: 0.8em;
            color: #666;
        }}
        .recommendations {{
            background: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 8px;
            padding: 20px;
            margin-top: 30px;
        }}
        .recommendations h3 {{
            color: #0066cc;
            margin-top: 0;
        }}
        .recommendations ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .recommendations li {{
            margin-bottom: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Consolidated Instagram Gallery</h1>
            <h2>รวมรูปภาพ Instagram ที่ดึงมาได้</h2>
            <p>Generated: {timestamp}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{analysis['total_images_found']}</h3>
                <p>Total Images</p>
            </div>
            <div class="stat-card">
                <h3>{len(analysis['results_by_method'])}</h3>
                <p>Extraction Methods</p>
            </div>
            <div class="stat-card">
                <h3>{len(analysis['directories_scanned'])}</h3>
                <p>Directories Scanned</p>
            </div>
        </div>
"""
        
        # Group images by method
        images_by_method = {}
        for img in images:
            method = img['method']
            if method not in images_by_method:
                images_by_method[method] = []
            images_by_method[method].append(img)
        
        # Generate sections for each method
        for method, method_images in images_by_method.items():
            html += f"""
        <div class="method-section">
            <h3>📁 {method} ({len(method_images)} images)</h3>
            <div class="image-grid">"""
            
            for img in method_images:
                size_mb = img['size'] / (1024 * 1024)
                html += f"""
                <div class="image-card">
                    <img src="{img['path']}" alt="{img['filename']}" onclick="window.open(this.src, '_blank')">
                    <div class="image-info">
                        <strong>{img['filename']}</strong><br>
                        📊 {size_mb:.2f} MB
                    </div>
                </div>"""
            
            html += """
            </div>
        </div>"""
        
        # Add recommendations
        html += f"""
        <div class="recommendations">
            <h3>💡 Recommendations</h3>
            <ul>"""
        
        for rec in analysis['recommendations']:
            html += f"<li>{rec}</li>"
        
        html += """
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def run_all_extractors(self):
        """Run all available extractors and consolidate results"""
        print("🎯 Starting comprehensive Instagram extraction...")
        print("=" * 60)
        
        # Check available extractors
        available_extractors = self.check_extractor_availability()
        
        if not available_extractors:
            print("❌ No extractors available!")
            return
        
        extraction_results = []
        
        # Run each extractor
        for extractor in available_extractors:
            print(f"\n{'='*20} {extractor['name']} {'='*20}")
            
            result = self.run_extractor(extractor)
            extraction_results.append(result)
            
            # Print result summary
            if result['success']:
                print(f"✅ {extractor['name']}: Completed successfully")
                if result['stdout']:
                    print("📄 Output preview:")
                    print(result['stdout'][-500:])  # Last 500 chars
            else:
                print(f"❌ {extractor['name']}: Failed")
                if result.get('error'):
                    print(f"Error: {result['error']}")
                if result.get('stderr'):
                    print(f"Error details: {result['stderr'][-300:]}")
            
            # Wait between extractors
            if extractor != available_extractors[-1]:
                print("⏱️ Waiting before next extractor...")
                time.sleep(10)
        
        # Analyze all results
        print("\n" + "="*60)
        analysis = self.analyze_results()
        
        # Create consolidated gallery
        gallery_file = self.create_consolidated_gallery(analysis)
        
        # Save execution report
        report = {
            "execution_time": datetime.now().isoformat(),
            "extractors_run": extraction_results,
            "analysis": analysis,
            "gallery_file": str(gallery_file)
        }
        
        report_file = self.results_dir / f"extraction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Print final summary
        print("\n🎉 Extraction process completed!")
        print(f"📊 Total images found: {analysis['total_images_found']}")
        print(f"🖼️ Gallery created: {gallery_file}")
        print(f"📋 Report saved: {report_file}")
        
        if analysis['best_results']:
            best = analysis['best_results']
            print(f"🏆 Best method: {best['method']} ({best['image_count']} images)")
        
        print("\n💡 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"   {rec}")
        
        return report

def main():
    print("🎯 Instagram Extraction Master Controller 2025")
    print("=" * 60)
    
    try:
        controller = ExtractionController()
        report = controller.run_all_extractors()
        
        # Open gallery if images were found
        if report['analysis']['total_images_found'] > 0:
            gallery_file = Path(report['gallery_file'])
            print(f"\n🌐 Opening gallery: {gallery_file}")
            
    except KeyboardInterrupt:
        print("\n⏹️ Extraction stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
