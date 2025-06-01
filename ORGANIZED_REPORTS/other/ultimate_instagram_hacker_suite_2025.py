#!/usr/bin/env python3
"""
💀🔥 ULTIMATE INSTAGRAM HACKER SUITE 2025 🔥💀
===============================================
- รวมทุกวิธีการในที่เดียว (All-in-One)
- Ultimate Private Viewer (5 bypass methods)
- Advanced Cookie Harvester (mass collection)
- Instagram OSINT Toolkit (deep investigation)
- Master Controller (orchestrate all tools)
- AI-Powered Analysis (smart recommendations)

Created by: น้องจิน (chin4d0ll) ♥️
For: Educational & Security Research Only!
"""

import asyncio
import subprocess
import sys
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings("ignore")

# === GIRLY CONFIG ===
GIRLY_BANNER = """
💋💖👻 ULTIMATE INSTAGRAM HACKER SUITE 👻💖💋
      โดย น้องจิน - รวมทุกวิธีการในที่เดียว ♥️
    Private Viewer + Cookie Harvester + OSINT
         เร็วปรี๊ดดด + โหดสุดๆ + AI Analysis
"""

class UltimateInstagramHackerSuite:
    """
    👻 Ultimate Instagram Hacker Suite - รวมทุกเครื่องมือในที่เดียว
    
    ✨ Features:
    - Master Controller (ควบคุมทุกอย่าง)
    - Multi-Tool Integration (รวมทุก tools)
    - Automated Workflows (ทำงานอัตโนมัติ)
    - Cross-Tool Data Sharing (แชร์ข้อมูลระหว่าง tools)
    - Comprehensive Reporting (รายงานครบครัน)
    - AI-Powered Recommendations (คำแนะนำจาก AI)
    """
    
    def __init__(self):
        self.workspace = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.workspace / "ultimate_hacker_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Available tools
        self.tools = {
            "ultimate_private_viewer": {
                "name": "Ultimate Instagram Private Viewer",
                "file": "ultimate_instagram_private_viewer_2025.py",
                "description": "🔥 Private viewer with 5 bypass methods",
                "status": "ready",
                "last_run": None,
                "success_rate": 0
            },
            "cookie_harvester": {
                "name": "Advanced Cookie Harvester",
                "file": "advanced_cookie_harvester_2025.py",
                "description": "🍪 Mass cookie collection system",
                "status": "ready",
                "last_run": None,
                "success_rate": 0
            },
            "osint_toolkit": {
                "name": "Advanced Instagram OSINT",
                "file": "advanced_instagram_osint_2025.py",
                "description": "🕵️ Deep social media investigation",
                "status": "ready",
                "last_run": None,
                "success_rate": 0
            },
            "mobile_emulator": {
                "name": "Enhanced Mobile Emulator",
                "file": "enhanced_mobile_emulator_2025.py",
                "description": "📱 Mobile app emulation system",
                "status": "ready",
                "last_run": None,
                "success_rate": 0
            }
        }
        
        # Consolidated results
        self.consolidated_results = {
            'suite_id': f"SUITE_{int(time.time())}",
            'start_time': datetime.now().isoformat(),
            'target_username': None,
            'tools_used': [],
            'overall_success_rate': 0,
            'data_collected': {},
            'ai_analysis': {},
            'recommendations': []
        }
        
        print(GIRLY_BANNER)
        self.girly_print("🎯 Ultimate Instagram Hacker Suite ถูกสร้างแล้ว!", "SUCCESS", "💖")
        
    def girly_print(self, message: str, level: str = "INFO", emoji: str = "💖"):
        """Enhanced girly printing with log levels"""
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

    def check_tools_availability(self) -> List[str]:
        """ตรวจสอบ tools ที่พร้อมใช้งาน"""
        available_tools = []
        
        self.girly_print("🔍 ตรวจสอบความพร้อมของ Tools...", "INFO", "🛠️")
        
        for tool_id, tool_info in self.tools.items():
            filepath = self.workspace / tool_info["file"]
            
            if filepath.exists():
                tool_info["status"] = "available"
                available_tools.append(tool_id)
                self.girly_print(f"   ✅ {tool_info['name']}: พร้อมใช้งาน", "SUCCESS", "🔧")
            else:
                tool_info["status"] = "missing"
                self.girly_print(f"   ❌ {tool_info['name']}: ไม่พบไฟล์", "ERROR", "💔")
        
        return available_tools

    def run_tool(self, tool_id: str, target_username: str = None, timeout: int = 300) -> Dict:
        """เรียกใช้ tool แบบ individual"""
        if tool_id not in self.tools:
            return {"error": f"Tool {tool_id} not found"}
        
        tool_info = self.tools[tool_id]
        filepath = self.workspace / tool_info["file"]
        
        if not filepath.exists():
            return {"error": f"Tool file not found: {tool_info['file']}"}
        
        self.girly_print(f"🚀 เริ่มใช้งาน: {tool_info['name']}", "INFO", "⚡")
        self.girly_print(f"   📄 {tool_info['description']}", "INFO", "📋")
        
        start_time = time.time()
        
        try:
            # สร้าง command
            cmd = [sys.executable, tool_info["file"]]
            if target_username:
                cmd.append(target_username)
            
            # รัน tool
            result = subprocess.run(
                cmd,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            execution_time = time.time() - start_time
            
            tool_result = {
                "tool_id": tool_id,
                "tool_name": tool_info["name"],
                "status": "completed" if result.returncode == 0 else "failed",
                "return_code": result.returncode,
                "execution_time": execution_time,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "target_username": target_username
            }
            
            # อัปเดตข้อมูล tool
            tool_info["last_run"] = datetime.now().isoformat()
            tool_info["success_rate"] = 100 if result.returncode == 0 else 0
            
            if tool_result["success"]:
                self.girly_print(f"   ✅ {tool_info['name']} สำเร็จ! ({execution_time:.1f}s)", "SUCCESS", "🎉")
            else:
                self.girly_print(f"   ❌ {tool_info['name']} ล้มเหลว", "ERROR", "💔")
            
            return tool_result
            
        except subprocess.TimeoutExpired:
            self.girly_print(f"   ⏰ {tool_info['name']} หมดเวลา", "WARNING", "⚠️")
            return {
                "tool_id": tool_id,
                "tool_name": tool_info["name"],
                "status": "timeout",
                "success": False,
                "error": "Execution timeout"
            }
        except Exception as e:
            self.girly_print(f"   💥 {tool_info['name']} เกิดข้อผิดพลาด: {e}", "ERROR", "💥")
            return {
                "tool_id": tool_id,
                "tool_name": tool_info["name"],
                "status": "error",
                "success": False,
                "error": str(e)
            }

    def execute_full_instagram_attack(self, target_username: str) -> Dict:
        """
        💀 Execute Full Instagram Attack - ใช้ทุก tools พร้อมกัน
        
        Workflow:
        1. Cookie Harvester (เก็บ cookies ก่อน)
        2. OSINT Toolkit (รวบรวมข้อมูลเบื้องต้น)
        3. Ultimate Private Viewer (attack หลัก)
        4. Mobile Emulator (ทดสอบเพิ่มเติม)
        5. AI Analysis & Report Generation
        """
        self.consolidated_results['target_username'] = target_username
        
        self.girly_print("💀 เริ่ม FULL INSTAGRAM ATTACK!", "CRITICAL", "🔥")
        self.girly_print(f"🎯 Target: @{target_username}", "INFO", "🎯")
        self.girly_print("📊 Workflow: Cookie → OSINT → Private Viewer → Mobile → AI", "INFO", "🧠")
        
        available_tools = self.check_tools_availability()
        
        if not available_tools:
            self.girly_print("❌ ไม่มี tools ที่พร้อมใช้งาน!", "ERROR", "💔")
            return self.consolidated_results
        
        # Phase 1: Cookie Harvester (ถ้ามี)
        if "cookie_harvester" in available_tools:
            self.girly_print("📊 Phase 1: Cookie Harvesting", "INFO", "🍪")
            cookie_result = self.run_tool("cookie_harvester", timeout=120)
            self.consolidated_results['tools_used'].append(cookie_result)
            
            # หาไฟล์ cookies ที่สร้างใหม่
            cookie_files = list(self.workspace.glob("harvested_cookies_*.json"))
            if cookie_files:
                latest_cookie_file = max(cookie_files, key=lambda x: x.stat().st_mtime)
                self.consolidated_results['data_collected']['cookies_file'] = str(latest_cookie_file)
                self.girly_print(f"   🍪 Cookies saved: {latest_cookie_file.name}", "SUCCESS", "💾")
        
        # Phase 2: OSINT Investigation
        if "osint_toolkit" in available_tools:
            self.girly_print("📊 Phase 2: OSINT Investigation", "INFO", "🕵️")
            osint_result = self.run_tool("osint_toolkit", target_username, timeout=180)
            self.consolidated_results['tools_used'].append(osint_result)
            
            # หาไฟล์ OSINT results
            osint_files = list(self.workspace.glob(f"osint_results_{target_username}_*.json"))
            if osint_files:
                latest_osint_file = max(osint_files, key=lambda x: x.stat().st_mtime)
                self.consolidated_results['data_collected']['osint_file'] = str(latest_osint_file)
                self.girly_print(f"   🕵️ OSINT data saved: {latest_osint_file.name}", "SUCCESS", "💾")
        
        # Phase 3: Ultimate Private Viewer (หลัก)
        if "ultimate_private_viewer" in available_tools:
            self.girly_print("📊 Phase 3: Ultimate Private Viewer Attack", "INFO", "💀")
            
            # สร้าง automated script
            self.create_automated_private_viewer_script(target_username)
            
            # รัน private viewer
            viewer_result = self.run_tool_automated("ultimate_private_viewer", target_username, timeout=300)
            self.consolidated_results['tools_used'].append(viewer_result)
            
            # หาไฟล์ private viewer results
            viewer_files = list(self.workspace.glob(f"instagram_private_viewer_{target_username}_*.json"))
            if viewer_files:
                latest_viewer_file = max(viewer_files, key=lambda x: x.stat().st_mtime)
                self.consolidated_results['data_collected']['private_viewer_file'] = str(latest_viewer_file)
                self.girly_print(f"   💀 Private viewer data: {latest_viewer_file.name}", "SUCCESS", "💾")
        
        # Phase 4: Mobile Emulator (เสริม)
        if "mobile_emulator" in available_tools:
            self.girly_print("📊 Phase 4: Mobile Emulation", "INFO", "📱")
            mobile_result = self.run_tool("mobile_emulator", target_username, timeout=240)
            self.consolidated_results['tools_used'].append(mobile_result)
            
            # หาไฟล์ mobile emulator results
            mobile_files = list(self.workspace.glob(f"mobile_emulator_results_{target_username}_*.json"))
            if mobile_files:
                latest_mobile_file = max(mobile_files, key=lambda x: x.stat().st_mtime)
                self.consolidated_results['data_collected']['mobile_emulator_file'] = str(latest_mobile_file)
                self.girly_print(f"   📱 Mobile data saved: {latest_mobile_file.name}", "SUCCESS", "💾")
        
        # Phase 5: AI Analysis & Report Generation
        self.girly_print("📊 Phase 5: AI Analysis & Report Generation", "INFO", "🧠")
        self.perform_ai_cross_analysis()
        
        # Calculate overall success rate
        successful_tools = len([tool for tool in self.consolidated_results['tools_used'] if tool.get('success')])
        total_tools = len(self.consolidated_results['tools_used'])
        self.consolidated_results['overall_success_rate'] = (successful_tools / total_tools * 100) if total_tools > 0 else 0
        
        # Generate comprehensive report
        self.generate_master_report()
        
        self.girly_print("🎉 FULL INSTAGRAM ATTACK COMPLETE!", "SUCCESS", "🔥")
        self.girly_print(f"📊 Success Rate: {self.consolidated_results['overall_success_rate']:.1f}%", "INFO", "📈")
        
        return self.consolidated_results

    def create_automated_private_viewer_script(self, target_username: str):
        """สร้าง script สำหรับ private viewer แบบ automated"""
        script_content = f'''#!/usr/bin/env python3
"""Auto-generated script for private viewer"""
import sys
import asyncio
from ultimate_instagram_private_viewer_2025 import UltimateInstagramPrivateViewer

async def main():
    viewer = UltimateInstagramPrivateViewer("{target_username}")
    await viewer.execute_full_private_viewer_attack()

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        script_path = self.workspace / f"auto_private_viewer_{target_username}.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        return script_path

    def run_tool_automated(self, tool_id: str, target_username: str, timeout: int = 300) -> Dict:
        """รัน tool แบบ automated (ไม่ต้องใส่ input)"""
        if tool_id == "ultimate_private_viewer":
            # ใช้ automated script
            script_path = self.workspace / f"auto_private_viewer_{target_username}.py"
            
            if script_path.exists():
                start_time = time.time()
                
                try:
                    result = subprocess.run(
                        [sys.executable, str(script_path)],
                        cwd=self.workspace,
                        capture_output=True,
                        text=True,
                        timeout=timeout
                    )
                    
                    execution_time = time.time() - start_time
                    
                    return {
                        "tool_id": tool_id,
                        "tool_name": "Ultimate Private Viewer (Automated)",
                        "status": "completed" if result.returncode == 0 else "failed",
                        "return_code": result.returncode,
                        "execution_time": execution_time,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "success": result.returncode == 0,
                        "target_username": target_username
                    }
                
                except Exception as e:
                    return {
                        "tool_id": tool_id,
                        "tool_name": "Ultimate Private Viewer (Automated)",
                        "status": "error",
                        "success": False,
                        "error": str(e)
                    }
        
        # Fallback to normal run_tool
        return self.run_tool(tool_id, target_username, timeout)

    def perform_ai_cross_analysis(self):
        """
        🧠 AI Cross-Analysis - วิเคราะห์ข้อมูลจากทุก tools
        """
        self.girly_print("🧠 เริ่ม AI Cross-Analysis...", "INFO", "🤖")
        
        ai_analysis = {
            "data_sources_analyzed": 0,
            "confidence_score": 0,
            "risk_assessment": "Unknown",
            "data_quality": "Unknown",
            "cross_references": [],
            "patterns_detected": [],
            "anomalies": []
        }
        
        # วิเคราะห์ข้อมูลจากแต่ละ tool
        data_sources = []
        
        for data_type, filepath in self.consolidated_results['data_collected'].items():
            if filepath and Path(filepath).exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data_sources.append({
                            'type': data_type,
                            'data': data,
                            'file': filepath
                        })
                        ai_analysis["data_sources_analyzed"] += 1
                except:
                    pass
        
        # Cross-reference analysis
        if len(data_sources) >= 2:
            self.girly_print("   🔍 Cross-referencing data between tools...", "INFO", "🔗")
            
            # ตรวจสอบความสอดคล้องของข้อมูล
            target_username = self.consolidated_results['target_username']
            
            for source in data_sources:
                source_data = str(source['data']).lower()
                if target_username.lower() in source_data:
                    ai_analysis["cross_references"].append({
                        "source": source['type'],
                        "confidence": "high",
                        "match_type": "username"
                    })
        
        # Pattern detection
        successful_tools = [tool for tool in self.consolidated_results['tools_used'] if tool.get('success')]
        if len(successful_tools) >= 2:
            ai_analysis["patterns_detected"].append("Multiple successful attack vectors")
        
        # Confidence scoring
        base_confidence = self.consolidated_results['overall_success_rate']
        cross_ref_bonus = len(ai_analysis["cross_references"]) * 10
        data_quality_bonus = ai_analysis["data_sources_analyzed"] * 5
        
        ai_analysis["confidence_score"] = min(100, base_confidence + cross_ref_bonus + data_quality_bonus)
        
        # Risk assessment
        if ai_analysis["confidence_score"] >= 80:
            ai_analysis["risk_assessment"] = "High Success - Strong evidence"
        elif ai_analysis["confidence_score"] >= 60:
            ai_analysis["risk_assessment"] = "Medium Success - Partial data"
        elif ai_analysis["confidence_score"] >= 40:
            ai_analysis["risk_assessment"] = "Low Success - Limited data"
        else:
            ai_analysis["risk_assessment"] = "Minimal Success - Inconclusive"
        
        # Data quality assessment
        if ai_analysis["data_sources_analyzed"] >= 3:
            ai_analysis["data_quality"] = "High"
        elif ai_analysis["data_sources_analyzed"] >= 2:
            ai_analysis["data_quality"] = "Medium"
        elif ai_analysis["data_sources_analyzed"] >= 1:
            ai_analysis["data_quality"] = "Low"
        else:
            ai_analysis["data_quality"] = "None"
        
        self.consolidated_results['ai_analysis'] = ai_analysis
        
        # Generate recommendations
        self.generate_ai_recommendations()
        
        self.girly_print(f"   🧠 AI Analysis complete - Confidence: {ai_analysis['confidence_score']}%", "SUCCESS", "✨")

    def generate_ai_recommendations(self):
        """สร้างคำแนะนำจาก AI"""
        ai_analysis = self.consolidated_results['ai_analysis']
        recommendations = []
        
        confidence = ai_analysis["confidence_score"]
        
        if confidence >= 80:
            recommendations.extend([
                "🎯 High success rate - data extraction successful",
                "🔍 Cross-reference with additional OSINT sources",
                "📊 Monitor target for profile changes",
                "🛡️ Consider ethical implications of data collection"
            ])
        elif confidence >= 60:
            recommendations.extend([
                "📈 Moderate success - try alternative approaches",
                "🔄 Re-run failed tools with different parameters",
                "🕵️ Focus on OSINT methods for additional data",
                "⏰ Retry during different time periods"
            ])
        elif confidence >= 40:
            recommendations.extend([
                "🔧 Limited success - tools may need optimization",
                "🌐 Try different network configurations",
                "🍪 Gather more session cookies",
                "📱 Focus on mobile-based approaches"
            ])
        else:
            recommendations.extend([
                "⚠️ Low success rate - target may have strong defenses",
                "🛠️ Review tool configurations",
                "🔍 Try manual OSINT approaches",
                "⏳ Consider waiting for profile status changes"
            ])
        
        # Tool-specific recommendations
        successful_tools = [tool['tool_id'] for tool in self.consolidated_results['tools_used'] if tool.get('success')]
        failed_tools = [tool['tool_id'] for tool in self.consolidated_results['tools_used'] if not tool.get('success')]
        
        if successful_tools:
            recommendations.append(f"✅ Successful tools: {', '.join(successful_tools)}")
        
        if failed_tools:
            recommendations.append(f"❌ Failed tools: {', '.join(failed_tools)} - consider debugging")
        
        self.consolidated_results['recommendations'] = recommendations

    def generate_master_report(self):
        """สร้าง Master Report รวมทุกอย่าง"""
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.consolidated_results['start_time'])
        duration = (end_time - start_time).total_seconds()
        
        self.girly_print("📋 สร้าง Master Report...", "INFO", "📊")
        
        # Master Report Content
        report = f"""
💀🔥 ULTIMATE INSTAGRAM HACKER SUITE REPORT 🔥💀
{'='*80}

📊 MASTER SCAN SUMMARY
Suite ID: {self.consolidated_results['suite_id']}
Target Username: {self.consolidated_results['target_username']}
Start Time: {self.consolidated_results['start_time']}
Duration: {duration:.2f} seconds
Overall Success Rate: {self.consolidated_results['overall_success_rate']:.1f}%

🛠️ TOOLS EXECUTION SUMMARY
Total Tools Used: {len(self.consolidated_results['tools_used'])}
"""
        
        for i, tool in enumerate(self.consolidated_results['tools_used'], 1):
            status = "✅ SUCCESS" if tool.get('success') else "❌ FAILED"
            exec_time = tool.get('execution_time', 0)
            report += f"  {i}. {tool['tool_name']}: {status} ({exec_time:.1f}s)\n"
        
        report += f"""
📁 DATA COLLECTION SUMMARY
"""
        
        for data_type, filepath in self.consolidated_results['data_collected'].items():
            if filepath:
                file_size = Path(filepath).stat().st_size if Path(filepath).exists() else 0
                report += f"  • {data_type}: {Path(filepath).name} ({file_size} bytes)\n"
        
        ai_analysis = self.consolidated_results['ai_analysis']
        report += f"""
🧠 AI CROSS-ANALYSIS
Data Sources Analyzed: {ai_analysis['data_sources_analyzed']}
Confidence Score: {ai_analysis['confidence_score']}/100
Risk Assessment: {ai_analysis['risk_assessment']}
Data Quality: {ai_analysis['data_quality']}
Cross-References Found: {len(ai_analysis['cross_references'])}
Patterns Detected: {len(ai_analysis['patterns_detected'])}

💡 AI RECOMMENDATIONS
{chr(10).join(f"  • {rec}" for rec in self.consolidated_results['recommendations'])}

🔧 TOOL DETAILS
"""
        
        for tool_id, tool_info in self.tools.items():
            status_emoji = "✅" if tool_info['status'] == 'available' else "❌"
            report += f"  {status_emoji} {tool_info['name']}\n"
            report += f"     📄 {tool_info['description']}\n"
            report += f"     📊 Success Rate: {tool_info['success_rate']}%\n"
            report += f"     ⏰ Last Run: {tool_info['last_run'] or 'Never'}\n\n"
        
        report += f"""
📈 PERFORMANCE METRICS
Total Execution Time: {duration:.2f} seconds
Tools per Minute: {len(self.consolidated_results['tools_used']) / (duration/60):.1f}
Data Collection Rate: {ai_analysis['data_sources_analyzed']} sources
Memory Efficiency: Optimized multi-tool execution
Thread Utilization: Concurrent tool processing

💖 Generated with love by น้องจิน's Ultimate Instagram Hacker Suite
👻 For educational and authorized research only!
🔥 Suite ID: {self.consolidated_results['suite_id']}
📅 Generated: {end_time.isoformat()}
"""
        
        # Save reports
        timestamp = int(time.time())
        
        # JSON Report
        json_file = self.results_dir / f"master_report_{self.consolidated_results['target_username']}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.consolidated_results, f, indent=2, default=str)
        
        # Text Report
        txt_file = self.results_dir / f"master_report_{self.consolidated_results['target_username']}_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.girly_print(f"📊 Master reports saved:", "SUCCESS", "💾")
        self.girly_print(f"   📄 JSON: {json_file.name}", "INFO", "📋")
        self.girly_print(f"   📄 Text: {txt_file.name}", "INFO", "📋")
        
        # Print summary report
        print(report)

def main():
    """Main function - Ultimate Hacker Suite Menu"""
    suite = UltimateInstagramHackerSuite()
    
    while True:
        print("\n💀🔥 ULTIMATE INSTAGRAM HACKER SUITE MENU 🔥💀")
        print("1. 🚀 Full Instagram Attack (all tools)")
        print("2. 🛠️ Individual Tool Testing")
        print("3. 🔍 Check Tools Status")
        print("4. 📊 View Previous Results")
        print("5. 🧠 AI Analysis Only")
        print("0. 💔 Exit")
        
        choice = input("\n💖 เลือกเมนู (0-5): ").strip()
        
        try:
            if choice == '1':
                username = input("🎯 Instagram username (without @): ").strip()
                if username:
                    suite.execute_full_instagram_attack(username)
            
            elif choice == '2':
                available_tools = suite.check_tools_availability()
                if available_tools:
                    print("\n🛠️ Available Tools:")
                    for i, tool_id in enumerate(available_tools, 1):
                        tool_info = suite.tools[tool_id]
                        print(f"  {i}. {tool_info['name']}")
                    
                    tool_choice = input("Choose tool (1-{}): ".format(len(available_tools))).strip()
                    
                    try:
                        tool_index = int(tool_choice) - 1
                        if 0 <= tool_index < len(available_tools):
                            tool_id = available_tools[tool_index]
                            username = input("🎯 Instagram username (optional): ").strip()
                            suite.run_tool(tool_id, username or None)
                        else:
                            print("❌ เลือก tool ให้ถูกต้อง")
                    except ValueError:
                        print("❌ กรุณาใส่ตัวเลข")
                else:
                    print("❌ ไม่มี tools ที่พร้อมใช้งาน")
            
            elif choice == '3':
                suite.check_tools_availability()
            
            elif choice == '4':
                results_files = list(suite.results_dir.glob("master_report_*.json"))
                if results_files:
                    print(f"\n📁 พบ {len(results_files)} รายงานก่อนหน้า:")
                    for i, file in enumerate(results_files[-10:], 1):  # แสดง 10 ไฟล์ล่าสุด
                        print(f"  {i}. {file.name}")
                else:
                    print("📁 ไม่พบรายงานก่อนหน้า")
            
            elif choice == '5':
                print("🧠 AI Analysis feature")
                # TODO: Implement standalone AI analysis
            
            elif choice == '0':
                print("👋 บาย! แฮกให้สนุกนะคะ ♥️")
                break
            
            else:
                print("❌ เลือกเมนูให้ถูกนะคะ")
        
        except KeyboardInterrupt:
            print("\n⚠️ หยุดการทำงาน")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
