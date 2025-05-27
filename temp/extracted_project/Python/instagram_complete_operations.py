#!/usr/bin/env python3
"""
Instagram Complete Operations Suite - ชุดเครื่องมือปฏิบัติการ Instagram ครบวงจร
รวมทุกเครื่องมือสำหรับการสกัดข้อมูล วิเคราะห์ และสร้างกลยุทธ์การจู่โจม

🎯 Target: alx.trading
🔐 Credentials: Fleming654 + Multi-factor auth
🛡️ Safety: Maximum stealth, checkpoint avoidance
📊 Analysis: Behavioral profiling, targeting vectors
🎪 Seduction: Advanced psychological manipulation
"""

import os
import sys
import json
import time
from datetime import datetime
import subprocess

class InstagramOperationsSuite:
    def __init__(self):
        """Initialize complete operations suite"""
        self.target = "alx.trading"
        self.operation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"instagram_ops_{self.operation_id}"
        
        # Create results directory
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        
        print("🎯 Instagram Complete Operations Suite")
        print("=" * 60)
        print(f"Target: {self.target}")
        print(f"Operation ID: {self.operation_id}")
        print(f"Results Directory: {self.results_dir}")
        print("=" * 60)
    
    def session_management(self):
        """Handle session creation and refresh"""
        print("\n🔄 PHASE 1: SESSION MANAGEMENT")
        print("-" * 40)
        
        try:
            result = subprocess.run([
                sys.executable, "instagram_session_refresher.py"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Session management completed")
                print("Session is ready for extraction")
                return True
            else:
                print("❌ Session management failed")
                print(f"Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Session management timed out")
            return False
        except Exception as e:
            print(f"❌ Session management error: {str(e)}")
            return False
    
    def data_extraction(self):
        """Execute advanced data extraction"""
        print("\n📊 PHASE 2: ADVANCED DATA EXTRACTION")
        print("-" * 40)
        
        try:
            result = subprocess.run([
                sys.executable, "instagram_advanced_extractor.py"
            ], capture_output=True, text=True, timeout=900)  # 15 minutes timeout
            
            if result.returncode == 0:
                print("✅ Data extraction completed")
                
                # Find extraction result file
                extraction_files = [f for f in os.listdir('.') if f.startswith('instagram_advanced_extraction_')]
                if extraction_files:
                    latest_file = max(extraction_files, key=os.path.getctime)
                    
                    # Move to results directory
                    os.rename(latest_file, os.path.join(self.results_dir, latest_file))
                    print(f"📁 Results moved to {self.results_dir}/{latest_file}")
                    return latest_file
                else:
                    print("⚠️ No extraction file found")
                    return None
            else:
                print("❌ Data extraction failed")
                print(f"Error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ Data extraction timed out")
            return None
        except Exception as e:
            print(f"❌ Data extraction error: {str(e)}")
            return None
    
    def intelligence_analysis(self, extraction_file):
        """Execute intelligence analysis"""
        print("\n🧠 PHASE 3: INTELLIGENCE ANALYSIS")
        print("-" * 40)
        
        if not extraction_file:
            print("❌ No extraction file for analysis")
            return None
        
        try:
            # Copy extraction file back temporarily for analysis
            temp_file = extraction_file
            if not os.path.exists(temp_file):
                temp_file = os.path.join(self.results_dir, extraction_file)
                if os.path.exists(temp_file):
                    # Copy back to current directory temporarily
                    os.system(f"cp '{temp_file}' .")
                    temp_file = extraction_file
            
            result = subprocess.run([
                sys.executable, "instagram_intelligence_analyzer.py"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Intelligence analysis completed")
                
                # Find intelligence report
                intel_files = [f for f in os.listdir('.') if f.startswith('instagram_intelligence_report_')]
                if intel_files:
                    latest_intel = max(intel_files, key=os.path.getctime)
                    
                    # Move to results directory
                    os.rename(latest_intel, os.path.join(self.results_dir, latest_intel))
                    print(f"📁 Intelligence report moved to {self.results_dir}/{latest_intel}")
                    return latest_intel
                else:
                    print("⚠️ No intelligence report found")
                    return None
            else:
                print("❌ Intelligence analysis failed")
                print(f"Error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ Intelligence analysis timed out")
            return None
        except Exception as e:
            print(f"❌ Intelligence analysis error: {str(e)}")
            return None
    
    def seduction_targeting(self):
        """Execute seduction targeting analysis"""
        print("\n💕 PHASE 4: SEDUCTION TARGETING")
        print("-" * 40)
        
        seduction_tools = [
            "master_seduction_targeting.py",
            "advanced_seduction_engine.py", 
            "thai_seduction_engine.py"
        ]
        
        results = []
        
        for tool in seduction_tools:
            if os.path.exists(tool):
                try:
                    print(f"🎪 Running {tool}...")
                    result = subprocess.run([
                        sys.executable, tool
                    ], capture_output=True, text=True, timeout=180)
                    
                    if result.returncode == 0:
                        print(f"✅ {tool} completed")
                        results.append(tool)
                    else:
                        print(f"❌ {tool} failed: {result.stderr}")
                        
                except subprocess.TimeoutExpired:
                    print(f"⏰ {tool} timed out")
                except Exception as e:
                    print(f"❌ {tool} error: {str(e)}")
            else:
                print(f"⚠️ {tool} not found")
        
        # Move seduction results to results directory
        seduction_files = [f for f in os.listdir('.') if any(x in f for x in ['SEDUCTION', 'seduction', 'TARGETING'])]
        for file in seduction_files:
            if file.endswith('.json'):
                try:
                    os.rename(file, os.path.join(self.results_dir, file))
                    print(f"📁 {file} moved to results directory")
                except:
                    pass
        
        return results
    
    def generate_operation_report(self, extraction_file, intelligence_file, seduction_results):
        """Generate comprehensive operation report"""
        print("\n📋 PHASE 5: OPERATION REPORT GENERATION")
        print("-" * 40)
        
        report = {
            "operation_id": self.operation_id,
            "timestamp": datetime.now().isoformat(),
            "target": self.target,
            "phases_completed": {
                "session_management": True,
                "data_extraction": extraction_file is not None,
                "intelligence_analysis": intelligence_file is not None,
                "seduction_targeting": len(seduction_results) > 0
            },
            "results_files": {
                "extraction_data": extraction_file,
                "intelligence_report": intelligence_file,
                "seduction_tools": seduction_results
            },
            "operation_summary": {},
            "next_steps": [],
            "operational_security": {
                "session_status": "active",
                "detection_risk": "low",
                "recommended_actions": []
            }
        }
        
        # Load intelligence summary if available
        if intelligence_file:
            intel_path = os.path.join(self.results_dir, intelligence_file)
            if os.path.exists(intel_path):
                try:
                    with open(intel_path, 'r', encoding='utf-8') as f:
                        intel_data = json.load(f)
                    
                    summary = intel_data.get("intelligence_summary", {})
                    report["operation_summary"] = {
                        "target_assessment": summary.get("target_profile", {}),
                        "key_vulnerabilities": summary.get("key_vulnerabilities", []),
                        "success_probability": summary.get("success_probability", {}),
                        "recommended_approach": summary.get("recommended_approach", {}),
                        "operational_timeline": summary.get("operational_timeline", {})
                    }
                    
                except Exception as e:
                    print(f"⚠️ Could not load intelligence data: {str(e)}")
        
        # Next steps recommendations
        if extraction_file and intelligence_file:
            report["next_steps"] = [
                "Deploy seduction targeting vectors",
                "Initiate contact using recommended approach",
                "Monitor target response and adapt strategy",
                "Execute data mining operations",
                "Maintain operational security protocols"
            ]
        elif extraction_file:
            report["next_steps"] = [
                "Complete intelligence analysis",
                "Develop targeting strategy",
                "Plan seduction approach"
            ]
        else:
            report["next_steps"] = [
                "Resolve session issues",
                "Retry data extraction",
                "Check operational security"
            ]
        
        # Security recommendations
        report["operational_security"]["recommended_actions"] = [
            "Maintain session security",
            "Monitor target activity for changes",
            "Use varied attack vectors",
            "Implement communication OPSEC",
            "Regular security assessment updates"
        ]
        
        # Save operation report
        report_file = os.path.join(self.results_dir, f"OPERATION_REPORT_{self.operation_id}.json")
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Operation report generated: {report_file}")
            
        except Exception as e:
            print(f"❌ Failed to save operation report: {str(e)}")
        
        return report
    
    def print_operation_summary(self, report):
        """Print formatted operation summary"""
        print("\n" + "="*80)
        print("🎯 INSTAGRAM OPERATIONS COMPLETE - MISSION SUMMARY")
        print("="*80)
        
        print(f"\n📊 OPERATION DETAILS:")
        print(f"   • Operation ID: {report['operation_id']}")
        print(f"   • Target: @{report['target']}")
        print(f"   • Timestamp: {report['timestamp']}")
        print(f"   • Results Directory: {self.results_dir}")
        
        phases = report['phases_completed']
        print(f"\n✅ PHASES COMPLETED:")
        print(f"   • Session Management: {'✅' if phases['session_management'] else '❌'}")
        print(f"   • Data Extraction: {'✅' if phases['data_extraction'] else '❌'}")
        print(f"   • Intelligence Analysis: {'✅' if phases['intelligence_analysis'] else '❌'}")
        print(f"   • Seduction Targeting: {'✅' if phases['seduction_targeting'] else '❌'}")
        
        if 'operation_summary' in report and report['operation_summary']:
            summary = report['operation_summary']
            
            if 'success_probability' in summary:
                success = summary['success_probability']
                print(f"\n📈 SUCCESS ASSESSMENT:")
                print(f"   • Overall Probability: {success.get('overall', 'unknown')}")
                print(f"   • Confidence Level: {success.get('confidence', 'unknown')}")
            
            if 'recommended_approach' in summary:
                approach = summary['recommended_approach']
                print(f"\n🎯 RECOMMENDED APPROACH:")
                print(f"   • Primary Vector: {approach.get('primary_vector', 'unknown')}")
                print(f"   • Success Rate: {approach.get('probability', 'unknown')}")
        
        print(f"\n🚀 NEXT STEPS:")
        for i, step in enumerate(report.get('next_steps', []), 1):
            print(f"   {i}. {step}")
        
        print(f"\n🛡️ OPERATIONAL SECURITY:")
        security = report.get('operational_security', {})
        print(f"   • Session Status: {security.get('session_status', 'unknown')}")
        print(f"   • Detection Risk: {security.get('detection_risk', 'unknown')}")
        
        print("\n" + "="*80)
        print("🎉 MISSION READY FOR DEPLOYMENT!")
        print("="*80)
    
    def run_complete_operation(self):
        """Execute complete Instagram operations suite"""
        print("🚀 STARTING COMPLETE INSTAGRAM OPERATIONS")
        print("⚠️  WARNING: Advanced psychological warfare engaged")
        print("\n" + "="*60)
        
        start_time = time.time()
        
        # Phase 1: Session Management
        session_success = self.session_management()
        if not session_success:
            print("\n❌ OPERATION ABORTED: Session management failed")
            return False
        
        time.sleep(2)
        
        # Phase 2: Data Extraction
        extraction_file = self.data_extraction()
        
        time.sleep(2)
        
        # Phase 3: Intelligence Analysis
        intelligence_file = self.intelligence_analysis(extraction_file)
        
        time.sleep(2)
        
        # Phase 4: Seduction Targeting
        seduction_results = self.seduction_targeting()
        
        time.sleep(2)
        
        # Phase 5: Generate Operation Report
        report = self.generate_operation_report(extraction_file, intelligence_file, seduction_results)
        
        # Calculate total time
        total_time = time.time() - start_time
        
        # Print summary
        self.print_operation_summary(report)
        
        print(f"\n⏰ Total Operation Time: {total_time/60:.1f} minutes")
        print(f"📁 All results saved to: {self.results_dir}")
        
        return True

def main():
    """Main execution function"""
    print("🎯 Instagram Complete Operations Suite")
    print("🇹🇭 ระบบปฏิบัติการ Instagram ครบวงจร")
    print("\n⚠️  ETHICAL TESTING PURPOSES ONLY")
    print("This tool is for security research and authorized testing only")
    
    # Confirmation prompt
    response = input("\nProceed with Instagram operations? (YES/no): ").strip()
    if response.lower() not in ['yes', 'y', '']:
        print("Operation cancelled by user")
        return
    
    # Initialize and run operations
    ops_suite = InstagramOperationsSuite()
    success = ops_suite.run_complete_operation()
    
    if success:
        print("\n🎉 Instagram operations completed successfully!")
        print("🎯 Ready for deployment and data exploitation")
    else:
        print("\n❌ Instagram operations failed")
        print("Check logs and retry if necessary")

if __name__ == "__main__":
    main()
