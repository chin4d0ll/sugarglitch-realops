# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Reports Dashboard and Viewer
แดชบอร์ดสำหรับดูและจัดการ reports ที่จัดระเบียบแล้ว
"""

import os
import json
from pathlib import Path
from datetime import datetime
import webbrowser
import tempfile

class ReportsDashboard:
    def __init__(self, reports_dir="/workspaces/sugarglitch-realops/ORGANIZED_REPORTS"):
        self.reports_dir = Path(reports_dir)
        self.summary_data = None
        self.inventory_data = None

    def load_data(self):
        """โหลดข้อมูลสรุปและ inventory"""
        # Load summary
        summary_file = self.reports_dir / "reports_summary.json"
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                self.summary_data = json.load(f)

        # Load inventory
        inventory_file = self.reports_dir / "reports_inventory.json"
        if inventory_file.exists():
            with open(inventory_file, 'r', encoding='utf-8') as f:
                self.inventory_data = json.load(f)

    def create_html_dashboard(self):
        """สร้าง HTML dashboard สำหรับดู reports"""
        self.load_data()

        html_content = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Reports Dashboard - SugarGlitch RealOps</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}

        .header h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}

        .header .subtitle {{
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
            display: block;
        }}

        .stat-label {{
            color: #7f8c8d;
            margin-top: 10px;
            font-size: 1.1em;
        }}

        .categories-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}

        .section-title {{
            color: #2c3e50;
            font-size: 2em;
            margin-bottom: 20px;
            text-align: center;
        }}

        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        .category-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 12px;
            padding: 20px;
            color: white;
            transition: all 0.3s ease;
        }}

        .category-card:nth-child(2n) {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}

        .category-card:nth-child(3n) {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }}

        .category-card:nth-child(4n) {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }}

        .category-card:hover {{
            transform: scale(1.05);
        }}

        .category-name {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .category-description {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 15px;
        }}

        .category-stats {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
        }}

        .recent-files {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}

        .file-list {{
            list-style: none;
        }}

        .file-item {{
            background: #f8f9fa;
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            transition: all 0.3s ease;
        }}

        .file-item:hover {{
            background: #e9ecef;
            transform: translateX(5px);
        }}

        .file-name {{
            font-weight: bold;
            color: #2c3e50;
        }}

        .file-meta {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .navigation {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}

        .nav-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 25px;
            border-radius: 25px;
            text-decoration: none;
            margin: 10px;
            transition: all 0.3s ease;
        }}

        .nav-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }}

        .emoji {{
            font-size: 1.2em;
            margin-right: 8px;
        }}

        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }}

            .category-grid {{
                grid-template-columns: 1fr;
            }}

            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Reports Dashboard</h1>
            <p class="subtitle">SugarGlitch RealOps - Organized Reports System</p>
            <p class="subtitle">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">{self.summary_data['total_files'] if self.summary_data else '273'}</span>
                <div class="stat-label">📄 Total Reports</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">{self.summary_data['categories_count'] if self.summary_data else '7'}</span>
                <div class="stat-label">📂 Categories</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">{self.summary_data['total_size_mb']:.1f if self.summary_data else '8.4'}</span>
                <div class="stat-label">💾 Total Size (MB)</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">{len(self.inventory_data['files']) if self.inventory_data else '273'}</span>
                <div class="stat-label">🔍 Indexed Files</div>
            </div>
        </div>
"""

        # Add categories section
        html_content += """
        <div class="categories-section">
            <h2 class="section-title">📂 Report Categories</h2>
            <div class="category-grid">
"""

        if self.inventory_data:
            categories = self.inventory_data.get('categories', {})
            for cat_key, cat_data in categories.items():
                html_content += f"""
                <div class="category-card">
                    <div class="category-name">{cat_data['name']}</div>
                    <div class="category-description">{cat_data['description']}</div>
                    <div class="category-stats">
                        <span>📄 {cat_data['file_count']} files</span>
                        <span>💾 {cat_data['total_size'] / 1024:.1f} KB</span>
                    </div>
                </div>
"""

        html_content += """
            </div>
        </div>
"""

        # Add recent files section
        html_content += """
        <div class="recent-files">
            <h2 class="section-title">🕒 Recent Report Files</h2>
            <ul class="file-list">
"""

        if self.inventory_data:
            recent_files = sorted(self.inventory_data['files'], key=lambda x: x['modified'], reverse=True)[:10]
            for file_info in recent_files:
                size_kb = file_info['size'] / 1024
                html_content += f"""
                <li class="file-item">
                    <div class="file-name">📄 {file_info['name']}</div>
                    <div class="file-meta">
                        📅 Modified: {file_info['modified'][:10]} |
                        💾 Size: {size_kb:.1f} KB |
                        📂 Category: {file_info['category'].replace('_', ' ').title()}
                    </div>
                </li>
"""

        html_content += """
            </ul>
        </div>

        <div class="navigation">
            <h2 class="section-title">🔗 Quick Navigation</h2>
            <a href="file:///workspaces/sugarglitch-realops/ORGANIZED_REPORTS" class="nav-button">
                <span class="emoji">📂</span>Open Reports Folder
            </a>
            <a href="file:///workspaces/sugarglitch-realops/ORGANIZED_REPORTS/extraction_reports" class="nav-button">
                <span class="emoji">🔍</span>Extraction Reports
            </a>
            <a href="file:///workspaces/sugarglitch-realops/ORGANIZED_REPORTS/instagram_reports" class="nav-button">
                <span class="emoji">📱</span>Instagram Reports
            </a>
            <a href="file:///workspaces/sugarglitch-realops/ORGANIZED_REPORTS/documentation" class="nav-button">
                <span class="emoji">📚</span>Documentation
            </a>
            <a href="file:///workspaces/sugarglitch-realops/ORGANIZED_REPORTS/operations_reports" class="nav-button">
                <span class="emoji">⚙️</span>Operations Reports
            </a>
        </div>
    </div>
</body>
</html>
"""

        # Save dashboard
        dashboard_file = self.reports_dir / "dashboard.html"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(dashboard_file)

    def create_quick_access_script(self):
        """สร้าง script สำหรับเข้าถึง reports อย่างรวดเร็ว"""
        script_content = f"""#!/usr/bin/env python3
'''
Quick Reports Access Script
สคริปต์เข้าถึง reports อย่างรวดเร็ว
'''

import os
import webbrowser
from pathlib import Path

class QuickReportsAccess:
    def __init__(self):
        self.reports_dir = Path("/workspaces/sugarglitch-realops/ORGANIZED_REPORTS")

    def open_dashboard(self):
        '''เปิด dashboard'''
        dashboard = self.reports_dir / "dashboard.html"
        if dashboard.exists():
            webbrowser.open(f"file://{dashboard}")
            print("🌐 Opening reports dashboard...")
        else:
            print("❌ Dashboard not found!")

    def list_categories(self):
        '''แสดงรายการหมวดหมู่'''
        print("📂 Available Report Categories:")
        print("=" * 40)

        categories = [
            ("extraction_reports", "🔍 Extraction Reports"),
            ("instagram_reports", "📱 Instagram Reports"),
            ("operations_reports", "⚙️ Operations Reports"),
            ("hacker_reports", "🔒 Hacker & Security Reports"),
            ("documentation", "📚 Documentation & Guides"),
            ("json_reports", "📄 JSON Data Reports"),
            ("other", "📦 Other Reports")
        ]

        for i, (folder, name) in enumerate(categories, 1):
            folder_path = self.reports_dir / folder
            if folder_path.exists():
                file_count = len(list(folder_path.glob("*"))) - 1  # Exclude README
                print(f"{i}. {name} ({file_count} files)")
            else:
                print(f"{i}. {name} (Not found)")

    def open_category(self, category_num):
        '''เปิดหมวดหมู่ตามหมายเลข'''
        categories = [
            "extraction_reports", "instagram_reports", "operations_reports",
            "hacker_reports", "documentation", "json_reports", "other"
        ]

        if 1 <= category_num <= len(categories):
            folder = categories[category_num - 1]
            folder_path = self.reports_dir / folder
            if folder_path.exists():
                os.system(f'code "{folder_path}"')
                print(f"📂 Opening {folder} in VS Code...")
            else:
                print(f"❌ Category {folder} not found!")
        else:
            print("❌ Invalid category number!")

    def search_reports(self, keyword):
        '''ค้นหา reports ที่มีคำค้น'''
        print(f"🔍 Searching for reports containing '{keyword}'...")
        print("=" * 50)

        found_files = []
        for file_path in self.reports_dir.rglob("*"):
            if file_path.is_file() and keyword.lower() in file_path.name.lower():
                found_files.append(file_path)

        if found_files:
            for i, file_path in enumerate(found_files, 1):
                relative_path = file_path.relative_to(self.reports_dir)
                size_kb = file_path.stat().st_size / 1024
                print(f"{i}. {file_path.name}")
                print(f"   📂 {relative_path.parent}")
                print(f"   💾 {size_kb:.1f} KB")
                print()
        else:
            print("❌ No reports found with that keyword!")

        return found_files

def main():
    access = QuickReportsAccess()

    print("🎯 Quick Reports Access")
    print("=" * 30)
    print("1. Open Dashboard")
    print("2. List Categories")
    print("3. Open Category")
    print("4. Search Reports")
    print("5. Exit")
    print()

    while True:
        choice = input("Select option (1-5): ").strip()

        if choice == '1':
            access.open_dashboard()
        elif choice == '2':
            access.list_categories()
        elif choice == '3':
            access.list_categories()
            try:
                cat_num = int(input("Enter category number: "))
                access.open_category(cat_num)
            except ValueError:
                print("❌ Please enter a valid number!")
        elif choice == '4':
            keyword = input("Enter search keyword: ").strip()
            if keyword:
                access.search_reports(keyword)
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

        print()

if __name__ == "__main__":
    main()
"""

        script_file = self.reports_dir / "quick_access.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)

        # Make it executable
        os.chmod(script_file, 0o755)

        return str(script_file)

if __name__ == "__main__":
    print("🎯 Creating Reports Dashboard...")

    dashboard = ReportsDashboard()

    # Create HTML dashboard
    dashboard_file = dashboard.create_html_dashboard()
    print(f"✅ Dashboard created: {dashboard_file}")

    # Create quick access script
    access_script = dashboard.create_quick_access_script()
    print(f"✅ Quick access script: {access_script}")

    print("🎉 Reports dashboard ready!")
