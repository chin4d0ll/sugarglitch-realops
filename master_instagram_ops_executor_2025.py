#!/usr/bin/env python3
"""
🎯🔥 MASTER INSTAGRAM OPERATIONS EXECUTOR 2025 🔥🎯
==================================================
- Systematic execution of all Instagram bypass methods
- Real-time session validation and recovery
- Comprehensive DM extraction orchestration
- Multi-target intelligence operations
- Personal conversation analysis automation

ระบบควบคุมการดำเนินงานรวม Instagram แบบอัตโนมัติ!

Created by: น้องจิน (chin4d0ll) ♥️
For: Advanced Instagram Intelligence Operations
"""

import asyncio
import json
import time
import random
import sqlite3
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import warnings
warnings.filterwarnings("ignore")

# Import our advanced systems
try:
    from fresh_cookie_harvesting_2025 import FreshCookieHarvester2025
    from ultra_dm_conversation_extractor_2025 import UltraDMConversationExtractor
    from comprehensive_dm_analyzer_2025 import ComprehensiveDMAnalyzer
    from personal_conversation_insight_extractor_2025 import PersonalConversationInsightExtractor
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    # Define dummy classes if imports fail
    class FreshCookieHarvester2025:
        async def browser_automation_harvest(self, target): return False
        async def mobile_simulation_harvest(self, target): return False
        async def api_discovery_harvest(self, target): return False
        async def validate_session_freshness(self, target): return False
    
    class UltraDMConversationExtractor:
        async def load_fresh_session(self, target): return False
        async def inject_fresh_cookies(self, target): return False
        async def extract_conversations(self, target): return []
    
    class ComprehensiveDMAnalyzer:
        async def analyze_dm_file(self, file_path): return {}
        async def generate_comprehensive_report(self, data, file_path): return True
    
    class PersonalConversationInsightExtractor:
        async def extract_comprehensive_intelligence(self, target): return {}
        async def generate_intelligence_markdown_report(self, data, file_path): return True

class MasterInstagramOpsExecutor:
    """🎯 ระบบควบคุมการดำเนินงาน Instagram แบบรวม"""
    
    def __init__(self):
        self.targets = ["whatilove1728", "alx.trading"]
        self.operation_id = f"MASTER_OP_{int(time.time())}"
        self.results_dir = Path(f"master_operations_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.results_dir.mkdir(exist_ok=True)
        
        # Initialize logging
        self.setup_logging()
        
        # Operation status
        self.operation_status = {
            'fresh_cookies_harvested': False,
            'sessions_validated': False,
            'dm_extraction_completed': False,
            'analysis_completed': False,
            'intelligence_generated': False
        }
        
        self.extracted_data = {}
        self.intelligence_reports = {}
        
        self.log("🎯 Master Instagram Operations Executor initialized")
        self.log(f"📂 Results directory: {self.results_dir}")
    
    def setup_logging(self):
        """🔧 Setup comprehensive logging"""
        log_file = self.results_dir / f"master_operations_{self.operation_id}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log(self, message: str, level: str = "INFO"):
        """📝 Enhanced logging with colors"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_codes = {
            "INFO": "\033[94m",  # Blue
            "SUCCESS": "\033[92m",  # Green
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",  # Red
            "RESET": "\033[0m"
        }
        
        colored_message = f"{color_codes.get(level, '')}{timestamp} - {message}{color_codes['RESET']}"
        print(colored_message)
        
        if hasattr(self, 'logger'):
            getattr(self.logger, level.lower(), self.logger.info)(message)
    
    async def execute_operation_phase_1_cookie_harvesting(self) -> bool:
        """🍪 Phase 1: Fresh Cookie Harvesting"""
        self.log("🍪 Starting Phase 1: Fresh Cookie Harvesting", "INFO")
        
        try:
            harvester = FreshCookieHarvester2025()
            
            for target in self.targets:
                self.log(f"🎯 Harvesting cookies for target: {target}")
                
                # Try multiple harvesting methods
                methods = [
                    harvester.browser_automation_harvest,
                    harvester.mobile_simulation_harvest,
                    harvester.api_discovery_harvest
                ]
                
                for method_idx, method in enumerate(methods, 1):
                    try:
                        self.log(f"📱 Trying harvesting method {method_idx}/3...")
                        success = await method(target)
                        
                        if success:
                            self.log(f"✅ Cookie harvesting successful for {target} using method {method_idx}", "SUCCESS")
                            break
                    except Exception as e:
                        self.log(f"❌ Method {method_idx} failed for {target}: {e}", "WARNING")
                        continue
                
                # Validate harvested sessions
                valid_session = await harvester.validate_session_freshness(target)
                if valid_session:
                    self.log(f"✅ Session validation successful for {target}", "SUCCESS")
                else:
                    self.log(f"⚠️ Session validation failed for {target}", "WARNING")
            
            self.operation_status['fresh_cookies_harvested'] = True
            return True
            
        except Exception as e:
            self.log(f"❌ Phase 1 failed: {e}", "ERROR")
            return False
    
    async def execute_operation_phase_2_dm_extraction(self) -> bool:
        """💬 Phase 2: Ultra DM Conversation Extraction"""
        self.log("💬 Starting Phase 2: Ultra DM Conversation Extraction", "INFO")
        
        try:
            extractor = UltraDMConversationExtractor()
            
            for target in self.targets:
                self.log(f"🎯 Extracting DMs for target: {target}")
                
                # Load or inject fresh cookies
                session_loaded = extractor.load_fresh_session(target)
                if not session_loaded:
                    self.log(f"🍪 Injecting fresh cookies for {target}")
                    await extractor.inject_fresh_cookies(target)
                
                # Extract conversations using the correct method
                conversations = await extractor.extract_all_conversations_for_target(target)
                
                if conversations:
                    self.log(f"✅ Extracted conversations for {target}", "SUCCESS")
                    self.extracted_data[target] = conversations
                    
                    # Save to file
                    output_file = self.results_dir / f"dm_conversations_{target}_{int(time.time())}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(conversations, f, ensure_ascii=False, indent=2)
                    
                    self.log(f"💾 Conversations saved: {output_file}")
                else:
                    self.log(f"⚠️ No conversations extracted for {target}", "WARNING")
            
            self.operation_status['dm_extraction_completed'] = True
            return True
            
        except Exception as e:
            self.log(f"❌ Phase 2 failed: {e}", "ERROR")
            return False
    
    async def execute_operation_phase_3_data_analysis(self) -> bool:
        """📊 Phase 3: Comprehensive Data Analysis"""
        self.log("📊 Starting Phase 3: Comprehensive Data Analysis", "INFO")
        
        try:
            analyzer = ComprehensiveDMAnalyzer()
            
            for target in self.targets:
                self.log(f"🔍 Analyzing data for target: {target}")
                
                # Find existing data files
                data_files = list(Path().glob(f"*{target}*.json"))
                
                if data_files:
                    self.log(f"📁 Found {len(data_files)} data files for {target}")
                    
                    analysis_results = {}
                    for data_file in data_files:
                        try:
                            # Load and analyze the file data
                            with open(data_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            result = analyzer.analyze_dm_conversations(data)
                            if result:
                                analysis_results[str(data_file)] = result
                                self.log(f"✅ Analysis completed for {data_file}", "SUCCESS")
                        except Exception as e:
                            self.log(f"⚠️ Analysis failed for {data_file}: {e}", "WARNING")
                    
                    if analysis_results:
                        # Save analysis results
                        report_file = self.results_dir / f"comprehensive_analysis_{target}_{int(time.time())}.json"
                        with open(report_file, 'w', encoding='utf-8') as f:
                            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
                        self.log(f"📋 Analysis report saved: {report_file}")
                else:
                    self.log(f"⚠️ No data files found for {target}", "WARNING")
            
            self.operation_status['analysis_completed'] = True
            return True
            
        except Exception as e:
            self.log(f"❌ Phase 3 failed: {e}", "ERROR")
            return False
    
    async def execute_operation_phase_4_intelligence_extraction(self) -> bool:
        """🧠 Phase 4: Personal Intelligence Extraction"""
        self.log("🧠 Starting Phase 4: Personal Intelligence Extraction", "INFO")
        
        try:
            intelligence_extractor = PersonalConversationInsightExtractor()
            
            for target in self.targets:
                self.log(f"🎯 Extracting intelligence for target: {target}")
                
                # Process all available data using the correct method
                intelligence_report = intelligence_extractor.analyze_existing_instagram_data()
                
                if intelligence_report:
                    self.log(f"✅ Intelligence extracted for {target}", "SUCCESS")
                    self.intelligence_reports[target] = intelligence_report
                    
                    # Save intelligence report
                    report_file = self.results_dir / f"intelligence_report_{target}_{int(time.time())}.json"
                    with open(report_file, 'w', encoding='utf-8') as f:
                        json.dump(intelligence_report, f, ensure_ascii=False, indent=2)
                    
                    # Generate markdown report with target-specific filename
                    md_report_file = self.results_dir / f"intelligence_report_{target}_{int(time.time())}.md"
                    with open(md_report_file, 'w', encoding='utf-8') as f:
                        f.write(f"# Personal Intelligence Report - {target}\n\n")
                        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write("## Intelligence Summary\n\n")
                        f.write(json.dumps(intelligence_report, ensure_ascii=False, indent=2))
                    
                    self.log(f"🧠 Intelligence reports saved: {report_file} & {md_report_file}")
                else:
                    self.log(f"⚠️ No intelligence extracted for {target}", "WARNING")
            
            self.operation_status['intelligence_generated'] = True
            return True
            
        except Exception as e:
            self.log(f"❌ Phase 4 failed: {e}", "ERROR")
            return False
    
    async def execute_operation_phase_5_final_report(self) -> bool:
        """📊 Phase 5: Final Master Report Generation"""
        self.log("📊 Starting Phase 5: Final Master Report Generation", "INFO")
        
        try:
            # Create master operation summary
            master_report = {
                'operation_id': self.operation_id,
                'timestamp': datetime.now().isoformat(),
                'targets_processed': self.targets,
                'operation_status': self.operation_status,
                'extracted_data_summary': {},
                'intelligence_summary': {},
                'statistics': {
                    'total_targets': len(self.targets),
                    'successful_extractions': len([t for t in self.targets if t in self.extracted_data]),
                    'intelligence_reports_generated': len(self.intelligence_reports),
                    'total_files_created': len(list(self.results_dir.glob("*")))
                }
            }
            
            # Add summaries
            for target in self.targets:
                if target in self.extracted_data:
                    master_report['extracted_data_summary'][target] = {
                        'conversations_count': len(self.extracted_data[target]),
                        'data_size': len(str(self.extracted_data[target]))
                    }
                
                if target in self.intelligence_reports:
                    intel = self.intelligence_reports[target]
                    master_report['intelligence_summary'][target] = {
                        'personal_details_found': len(intel.get('personal_details', {})),
                        'relationships_mapped': len(intel.get('relationships', [])),
                        'sensitive_content_detected': len(intel.get('sensitive_content', []))
                    }
            
            # Save master report
            master_report_file = self.results_dir / f"MASTER_OPERATION_REPORT_{self.operation_id}.json"
            with open(master_report_file, 'w', encoding='utf-8') as f:
                json.dump(master_report, f, ensure_ascii=False, indent=2)
            
            # Generate markdown summary
            await self.generate_master_markdown_report(master_report)
            
            self.log(f"📊 Master operation report generated: {master_report_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"❌ Phase 5 failed: {e}", "ERROR")
            return False
    
    async def generate_master_markdown_report(self, master_report: Dict):
        """📋 Generate comprehensive markdown report"""
        md_content = f"""# 🎯 MASTER INSTAGRAM OPERATIONS REPORT 2025
## Operation ID: {master_report['operation_id']}
## Timestamp: {master_report['timestamp']}

---

## 📊 OPERATION SUMMARY

### Targets Processed
{chr(10).join([f"- **{target}**" for target in master_report['targets_processed']])}

### Operation Status
{chr(10).join([f"- **{status.replace('_', ' ').title()}**: {'✅ Complete' if completed else '❌ Failed'}" for status, completed in master_report['operation_status'].items()])}

### Statistics
- **Total Targets**: {master_report['statistics']['total_targets']}
- **Successful Extractions**: {master_report['statistics']['successful_extractions']}
- **Intelligence Reports Generated**: {master_report['statistics']['intelligence_reports_generated']}
- **Total Files Created**: {master_report['statistics']['total_files_created']}

---

## 💬 EXTRACTED DATA SUMMARY

"""
        
        for target, data in master_report['extracted_data_summary'].items():
            md_content += f"""### {target}
- **Conversations Found**: {data['conversations_count']}
- **Data Size**: {data['data_size']} characters

"""
        
        md_content += """---

## 🧠 INTELLIGENCE SUMMARY

"""
        
        for target, intel in master_report['intelligence_summary'].items():
            md_content += f"""### {target}
- **Personal Details Found**: {intel['personal_details_found']}
- **Relationships Mapped**: {intel['relationships_mapped']}
- **Sensitive Content Detected**: {intel['sensitive_content_detected']}

"""
        
        md_content += f"""---

## 📁 FILES GENERATED

All operation files are stored in: `{self.results_dir}`

### File Types Generated:
- DM Conversation Extractions (JSON)
- Comprehensive Analysis Reports (MD)
- Intelligence Reports (JSON & MD)
- Master Operation Report (JSON & MD)
- Operation Logs

---

*Generated by Master Instagram Operations Executor 2025*  
*Created by: น้องจิน (chin4d0ll) ♥️*
"""
        
        md_file = self.results_dir / f"MASTER_OPERATION_REPORT_{self.operation_id}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        self.log(f"📋 Master markdown report generated: {md_file}")
    
    async def execute_master_operation(self):
        """🚀 Execute complete master operation"""
        self.log("🚀 STARTING MASTER INSTAGRAM OPERATIONS EXECUTION", "SUCCESS")
        self.log("=" * 60)
        
        start_time = time.time()
        
        # Execute all phases
        phases = [
            ("🍪 Fresh Cookie Harvesting", self.execute_operation_phase_1_cookie_harvesting),
            ("💬 DM Conversation Extraction", self.execute_operation_phase_2_dm_extraction),
            ("📊 Comprehensive Data Analysis", self.execute_operation_phase_3_data_analysis),
            ("🧠 Personal Intelligence Extraction", self.execute_operation_phase_4_intelligence_extraction),
            ("📊 Final Master Report", self.execute_operation_phase_5_final_report)
        ]
        
        successful_phases = 0
        for phase_name, phase_func in phases:
            self.log(f"\n🎯 EXECUTING: {phase_name}")
            self.log("-" * 50)
            
            try:
                success = await phase_func()
                if success:
                    successful_phases += 1
                    self.log(f"✅ {phase_name} COMPLETED SUCCESSFULLY", "SUCCESS")
                else:
                    self.log(f"❌ {phase_name} FAILED", "ERROR")
            except Exception as e:
                self.log(f"💥 {phase_name} CRASHED: {e}", "ERROR")
        
        # Final summary
        execution_time = time.time() - start_time
        self.log("\n" + "=" * 60)
        self.log("🏁 MASTER OPERATION EXECUTION COMPLETED", "SUCCESS")
        self.log(f"⏱️ Total Execution Time: {execution_time:.2f} seconds")
        self.log(f"✅ Successful Phases: {successful_phases}/{len(phases)}")
        self.log(f"📂 Results Directory: {self.results_dir}")
        self.log("=" * 60)
        
        return successful_phases == len(phases)

async def main():
    """🚀 Main execution function"""
    print("""
🎯🔥 MASTER INSTAGRAM OPERATIONS EXECUTOR 2025 🔥🎯
==================================================
Starting comprehensive Instagram intelligence operations...

Targets: whatilove1728, alx.trading
Operations: Cookie Harvesting → DM Extraction → Analysis → Intelligence
    """)
    
    executor = MasterInstagramOpsExecutor()
    success = await executor.execute_master_operation()
    
    if success:
        print("\n🎉 ALL OPERATIONS COMPLETED SUCCESSFULLY! 🎉")
    else:
        print("\n⚠️ Some operations encountered issues. Check logs for details.")

if __name__ == "__main__":
    asyncio.run(main())
