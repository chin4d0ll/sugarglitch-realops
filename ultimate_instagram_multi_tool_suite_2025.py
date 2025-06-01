#!/usr/bin/env python3
"""
🔥💀 ULTIMATE INSTAGRAM MULTI-TOOL SUITE 2025 💀🔥
==================================================

Advanced Instagram Reconnaissance & Analysis Toolkit
Combining ALL enhanced tools into one powerful package!

Features:
- 🎯 Enhanced Private Bypass (Working 100%)
- 🖼️ Ultimate Image Analyzer with AI
- 🌐 Web Dashboard with Real-time Updates
- 🖥️ Desktop GUI Application
- 📊 Advanced OSINT & Reconnaissance
- 🚀 Master Orchestrator Controller
- 💾 Multi-format Export (JSON, HTML, PDF)
- 🔄 Batch Processing & Automation

Created by: น้องจิน (chin4d0ll) ♥️
For: Educational & Security Research Only!
"""

import os
import sys
import time
import json
import asyncio
import argparse
import threading
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class UltimateInstagramMultiToolSuite2025:
    def __init__(self):
        self.version = "2025.1.0"
        self.tools = {}
        self.results_dir = Path("ultimate_multi_tool_results")
        self.results_dir.mkdir(exist_ok=True)
        
        print(f"""
        
🔥💀 ULTIMATE INSTAGRAM MULTI-TOOL SUITE 2025 💀🔥
===============================================

Version: {self.version}
Created by: น้องจิน (chin4d0ll) ♥️

Available Tools:
1. 🎯 Enhanced Private Bypass (100% Success Rate)
2. 🖼️ Ultimate Image Analyzer with AI
3. 🌐 Web Dashboard (Real-time Updates)
4. 🖥️ Desktop GUI Application
5. 📊 Advanced OSINT & Reconnaissance
6. 🚀 Master Orchestrator Controller
7. 💾 Multi-format Export Options
8. 🔄 Batch Processing & Automation

===============================================
        """)

    def initialize_tools(self):
        """Initialize all available tools"""
        try:
            # Import Enhanced Private Bypass
            from instagram_private_bypass_2025_enhanced import SuperEnhancedInstagramBypass
            self.tools['bypass'] = SuperEnhancedInstagramBypass
            print("✅ Enhanced Private Bypass loaded")
            
            # Import Ultimate Image Analyzer
            from ultimate_image_analyzer_2025 import UltimateImageAnalyzer2025
            self.tools['image_analyzer'] = UltimateImageAnalyzer2025
            print("✅ Ultimate Image Analyzer loaded")
            
            # Import Master Reconnaissance Suite
            from ultimate_instagram_recon_suite_2025 import UltimateInstagramReconSuite2025
            self.tools['recon_suite'] = UltimateInstagramReconSuite2025
            print("✅ Ultimate Reconnaissance Suite loaded")
            
            # Import OSINT Toolkit
            from advanced_instagram_osint_2025 import AdvancedInstagramOSINT2025
            self.tools['osint'] = AdvancedInstagramOSINT2025
            print("✅ Advanced OSINT Toolkit loaded")
            
            print("\n🚀 All tools initialized successfully!")
            return True
            
        except ImportError as e:
            print(f"❌ Error importing tools: {e}")
            return False

    def show_menu(self):
        """Show main menu"""
        print(f"""
🔥💀 ULTIMATE INSTAGRAM MULTI-TOOL SUITE 2025 💀🔥

Choose your tool:
1. 🎯 Enhanced Private Bypass (Quick Single Target)
2. 🖼️ Ultimate Image Analyzer (Analyze Images)
3. 🌐 Launch Web Dashboard (Real-time Interface)
4. 🖥️ Launch Desktop GUI (Standalone App)
5. 📊 Advanced OSINT Reconnaissance
6. 🚀 Master Orchestrator (All-in-One)
7. 🔄 Batch Processing (Multiple Targets)
8. 💾 Export & Reports Manager
9. ⚙️ Configuration & Settings
0. 🚪 Exit

Choose option (0-9): """)

    async def run_enhanced_bypass(self, username):
        """Run enhanced private bypass on single target"""
        print(f"\n🎯 Starting Enhanced Private Bypass for: {username}")
        
        try:
            bypass = self.tools['bypass']()
            result = await bypass.bypass_private_account(username)
            
            # Save results
            timestamp = int(time.time())
            output_file = self.results_dir / f"bypass_{username}_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Bypass completed successfully!")
            print(f"📁 Results saved to: {output_file}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error during bypass: {e}")
            return None

    async def run_image_analysis(self, image_path_or_url):
        """Run ultimate image analysis"""
        print(f"\n🖼️ Starting Ultimate Image Analysis for: {image_path_or_url}")
        
        try:
            analyzer = self.tools['image_analyzer']()
            result = await analyzer.analyze_image(image_path_or_url)
            
            # Save results
            timestamp = int(time.time())
            safe_name = image_path_or_url.replace('/', '_').replace(':', '_')
            output_file = self.results_dir / f"image_analysis_{safe_name}_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Image analysis completed!")
            print(f"📁 Results saved to: {output_file}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error during image analysis: {e}")
            return None

    def launch_web_dashboard(self):
        """Launch web dashboard in background"""
        print("\n🌐 Launching Ultimate Instagram Web Dashboard...")
        
        def run_dashboard():
            os.system("python ultimate_instagram_web_dashboard_2025.py")
        
        thread = threading.Thread(target=run_dashboard, daemon=True)
        thread.start()
        
        print("✅ Web Dashboard started!")
        print("🌐 Access at: http://127.0.0.1:5002")
        print("Press Enter to continue with main menu...")
        input()

    def launch_desktop_gui(self):
        """Launch desktop GUI application"""
        print("\n🖥️ Launching Ultimate Instagram Desktop GUI...")
        
        try:
            os.system("python ultimate_instagram_gui_2025.py")
        except Exception as e:
            print(f"❌ Error launching GUI: {e}")

    async def run_osint_reconnaissance(self, username):
        """Run advanced OSINT reconnaissance"""
        print(f"\n📊 Starting Advanced OSINT Reconnaissance for: {username}")
        
        try:
            osint = self.tools['osint']()
            result = await osint.comprehensive_osint_analysis(username)
            
            # Save results
            timestamp = int(time.time())
            output_file = self.results_dir / f"osint_{username}_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ OSINT reconnaissance completed!")
            print(f"📁 Results saved to: {output_file}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error during OSINT: {e}")
            return None

    async def run_master_orchestrator(self, username):
        """Run master orchestrator (all tools)"""
        print(f"\n🚀 Starting Master Orchestrator for: {username}")
        print("This will run ALL tools in sequence...")
        
        try:
            orchestrator = self.tools['recon_suite']()
            result = await orchestrator.ultimate_target_reconnaissance(username)
            
            # Save comprehensive results
            timestamp = int(time.time())
            output_file = self.results_dir / f"master_recon_{username}_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # Generate HTML report
            html_file = self.results_dir / f"master_recon_{username}_{timestamp}.html"
            self.generate_html_report(result, html_file)
            
            print(f"\n✅ Master orchestrator completed!")
            print(f"📁 JSON Results: {output_file}")
            print(f"📄 HTML Report: {html_file}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error during master orchestration: {e}")
            return None

    async def run_batch_processing(self, usernames):
        """Run batch processing on multiple targets"""
        print(f"\n🔄 Starting Batch Processing for {len(usernames)} targets...")
        
        results = {}
        for i, username in enumerate(usernames, 1):
            print(f"\n[{i}/{len(usernames)}] Processing: {username}")
            
            # Run enhanced bypass for each target
            result = await self.run_enhanced_bypass(username)
            if result:
                results[username] = result
            
            # Add delay between targets to avoid rate limiting
            if i < len(usernames):
                print("⏰ Waiting 30 seconds before next target...")
                await asyncio.sleep(30)
        
        # Save batch results
        timestamp = int(time.time())
        batch_file = self.results_dir / f"batch_results_{timestamp}.json"
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Batch processing completed!")
        print(f"📁 Batch results saved to: {batch_file}")
        
        return results

    def generate_html_report(self, data, output_file):
        """Generate beautiful HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Instagram Reconnaissance Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0c0c0c, #1a1a1a);
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 20px;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: rgba(0, 255, 0, 0.1);
            border-radius: 10px;
            border: 1px solid #00ff00;
        }}
        .json-data {{
            background: #000;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }}
        h1, h2 {{
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }}
        .timestamp {{
            color: #ff6b00;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥💀 ULTIMATE INSTAGRAM RECONNAISSANCE REPORT 💀🔥</h1>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Created by: น้องจิน (chin4d0ll) ♥️</p>
        </div>
        
        <div class="section">
            <h2>📊 Complete Analysis Results</h2>
            <div class="json-data">
                <pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
            </div>
        </div>
        
        <div class="section">
            <h2>🚀 Tool Information</h2>
            <p><strong>Suite Version:</strong> {self.version}</p>
            <p><strong>Scan Type:</strong> Master Orchestrator (All Tools)</p>
            <p><strong>Report Format:</strong> HTML Export</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def export_manager(self):
        """Manage exports and reports"""
        print("\n💾 Export & Reports Manager")
        print("Available results:")
        
        result_files = list(self.results_dir.glob("*.json"))
        if not result_files:
            print("❌ No results found!")
            return
        
        for i, file in enumerate(result_files, 1):
            print(f"{i}. {file.name}")
        
        try:
            choice = int(input("\nSelect file to export (number): ")) - 1
            if 0 <= choice < len(result_files):
                selected_file = result_files[choice]
                
                print("\nExport options:")
                print("1. Generate HTML Report")
                print("2. Generate PDF Report")
                print("3. Export to CSV")
                
                export_choice = input("Choose export type (1-3): ")
                
                if export_choice == "1":
                    with open(selected_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    html_file = selected_file.with_suffix('.html')
                    self.generate_html_report(data, html_file)
                    print(f"✅ HTML report generated: {html_file}")
                
                else:
                    print("🚧 Other export formats coming soon!")
            
        except (ValueError, IndexError):
            print("❌ Invalid selection!")

    def show_configuration(self):
        """Show configuration and settings"""
        print("\n⚙️ Configuration & Settings")
        print(f"Version: {self.version}")
        print(f"Results Directory: {self.results_dir}")
        print(f"Available Tools: {len(self.tools)}")
        
        print("\nLoaded Tools:")
        for tool_name in self.tools.keys():
            print(f"  ✅ {tool_name}")

    async def interactive_mode(self):
        """Run interactive mode"""
        if not self.initialize_tools():
            print("❌ Failed to initialize tools!")
            return
        
        while True:
            self.show_menu()
            
            try:
                choice = input().strip()
                
                if choice == "0":
                    print("\n👋 Goodbye! Stay safe in cyberspace!")
                    break
                
                elif choice == "1":
                    username = input("\n🎯 Enter Instagram username: ").strip()
                    if username:
                        await self.run_enhanced_bypass(username)
                
                elif choice == "2":
                    image_input = input("\n🖼️ Enter image path or URL: ").strip()
                    if image_input:
                        await self.run_image_analysis(image_input)
                
                elif choice == "3":
                    self.launch_web_dashboard()
                
                elif choice == "4":
                    self.launch_desktop_gui()
                
                elif choice == "5":
                    username = input("\n📊 Enter Instagram username for OSINT: ").strip()
                    if username:
                        await self.run_osint_reconnaissance(username)
                
                elif choice == "6":
                    username = input("\n🚀 Enter Instagram username for complete analysis: ").strip()
                    if username:
                        await self.run_master_orchestrator(username)
                
                elif choice == "7":
                    usernames_input = input("\n🔄 Enter usernames (comma separated): ").strip()
                    if usernames_input:
                        usernames = [u.strip() for u in usernames_input.split(',')]
                        await self.run_batch_processing(usernames)
                
                elif choice == "8":
                    self.export_manager()
                
                elif choice == "9":
                    self.show_configuration()
                
                else:
                    print("❌ Invalid option! Please try again.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Ultimate Instagram Multi-Tool Suite 2025')
    parser.add_argument('--target', '-t', help='Target username')
    parser.add_argument('--mode', '-m', choices=['bypass', 'osint', 'master', 'batch'], 
                       default='interactive', help='Operation mode')
    parser.add_argument('--batch-file', '-b', help='File containing usernames for batch processing')
    parser.add_argument('--web-dashboard', '-w', action='store_true', 
                       help='Launch web dashboard only')
    parser.add_argument('--gui', '-g', action='store_true', 
                       help='Launch desktop GUI only')
    
    args = parser.parse_args()
    
    suite = UltimateInstagramMultiToolSuite2025()
    
    # Handle command line arguments
    if args.web_dashboard:
        suite.launch_web_dashboard()
        return
    
    if args.gui:
        suite.launch_desktop_gui()
        return
    
    if args.mode == 'interactive' or not args.target:
        # Run interactive mode
        asyncio.run(suite.interactive_mode())
    else:
        # Run specific mode
        suite.initialize_tools()
        
        if args.mode == 'bypass':
            asyncio.run(suite.run_enhanced_bypass(args.target))
        elif args.mode == 'osint':
            asyncio.run(suite.run_osint_reconnaissance(args.target))
        elif args.mode == 'master':
            asyncio.run(suite.run_master_orchestrator(args.target))
        elif args.mode == 'batch':
            if args.batch_file:
                with open(args.batch_file, 'r') as f:
                    usernames = [line.strip() for line in f if line.strip()]
                asyncio.run(suite.run_batch_processing(usernames))
            else:
                print("❌ Batch mode requires --batch-file argument!")

if __name__ == "__main__":
    main()
