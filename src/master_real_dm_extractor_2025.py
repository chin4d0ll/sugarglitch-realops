#!/usr/bin/env python3
"""
🎯 MASTER REAL DM EXTRACTOR 2025 - NO MOCKUP
=============================================
ตัวดึงข้อมูล DM หลักที่รวมเครื่องมือทั้งหมดและดึงข้อมูลจริงเท่านั้น
- รวมทุก extractor ในโปรเจกต์
- ไม่มี simulation หรือ mockup
- ใช้ session จริงและ API จริงเท่านั้น
- ลองหลายวิธีจนกว่าจะได้ข้อมูลจริง
"""

import json
import os
import time
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = "/workspaces/sugarglitch-realops"
sys.path.append(project_root)

# Import all real extractors
try:
    from src.dm_extractor import RealDMExtractor
    from src.instagram_tools.real_instagram_dm_extractor import RealInstagramDMExtractor
    from src.instagram_tools.actual_instagram_extractor import ActualInstagramExtractor
    from src.advanced_tools.advanced_real_dm_extractor import AdvancedRealDMExtractor
    from src.real_message_extractor import RealMessageExtractor
    from src.targeted.extract_dm_alx_whatilove import DMExtractor
    from scripts.ultimate_working_dm_extractor_2025 import UltimateWorkingDMExtractor
    from src.core_extractor_2025 import CoreExtractor
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Some extractors may not be available")

class MasterRealDMExtractor:
    """🎯 Master DM Extractor - REAL DATA ONLY"""
    
    def __init__(self):
        self.target = "alx.trading"
        self.project_root = project_root
        self.output_dir = f"{self.project_root}/master_extraction_results"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Results storage
        self.extraction_results = []
        self.successful_extractions = []
        self.failed_extractions = []
        
        print(f"🎯 MASTER REAL DM EXTRACTOR 2025")
        print(f"=================================")
        print(f"Target: {self.target}")
        print(f"Output: {self.output_dir}")
        print(f"⚠️  NO MOCKUP - REAL DATA ONLY")
    
    def method_1_playwright_browser(self):
        """Method 1: Browser automation with Playwright"""
        print(f"\n🔄 METHOD 1: Playwright Browser Automation")
        print("=" * 50)
        
        try:
            extractor = RealDMExtractor()
            session_data = extractor.load_session_from_file()
            
            if session_data and 'sessionid' in session_data:
                sessionid = session_data['sessionid']
                print(f"✅ Session ID found: {sessionid[:20]}...")
                
                import asyncio
                result = asyncio.run(extractor.get_dms_from_sessionid(sessionid, self.target))
                
                if result and result.get('conversations'):
                    print(f"✅ METHOD 1 SUCCESS: {len(result['conversations'])} conversations")
                    return result
                else:
                    print(f"❌ METHOD 1 FAILED: No data extracted")
                    return None
            else:
                print(f"❌ METHOD 1 FAILED: No valid session")
                return None
                
        except Exception as e:
            print(f"❌ METHOD 1 ERROR: {e}")
            return None
    
    def method_2_instagram_api_requests(self):
        """Method 2: Direct Instagram API requests"""
        print(f"\n🔄 METHOD 2: Instagram API Requests")
        print("=" * 50)
        
        try:
            extractor = RealInstagramDMExtractor()
            result = extractor.perform_real_extraction()
            
            if result and result.get('results', {}).get('conversations'):
                print(f"✅ METHOD 2 SUCCESS: {len(result['results']['conversations'])} conversations")
                return result
            else:
                print(f"❌ METHOD 2 FAILED: No conversations found")
                return None
                
        except Exception as e:
            print(f"❌ METHOD 2 ERROR: {e}")
            return None
    
    def method_3_actual_extractor(self):
        """Method 3: Actual Instagram extractor (no mockup)"""
        print(f"\n🔄 METHOD 3: Actual Instagram Extractor")
        print("=" * 50)
        
        try:
            extractor = ActualInstagramExtractor()
            result = extractor.perform_actual_extraction()
            
            if result and result.get('actual_data_found'):
                print(f"✅ METHOD 3 SUCCESS: Actual data found")
                return result
            else:
                print(f"❌ METHOD 3 FAILED: No actual data found")
                return None
                
        except Exception as e:
            print(f"❌ METHOD 3 ERROR: {e}")
            return None
    
    def method_4_advanced_techniques(self):
        """Method 4: Advanced stealth techniques"""
        print(f"\n🔄 METHOD 4: Advanced Stealth Techniques")
        print("=" * 50)
        
        try:
            extractor = AdvancedRealDMExtractor()
            result = extractor.extract_dm_data_with_real_techniques()
            
            if result and result.get('results', {}).get('extraction_success'):
                print(f"✅ METHOD 4 SUCCESS: Advanced extraction completed")
                return result
            else:
                print(f"❌ METHOD 4 FAILED: Advanced extraction failed")
                return None
                
        except Exception as e:
            print(f"❌ METHOD 4 ERROR: {e}")
            return None
    
    def method_5_ultimate_working_extractor(self):
        """Method 5: Ultimate working extractor"""
        print(f"\n🔄 METHOD 5: Ultimate Working Extractor")
        print("=" * 50)
        
        try:
            extractor = UltimateWorkingDMExtractor()
            
            # Try fresh login first
            if extractor.method_1_fresh_instagrapi_login():
                result = extractor.extract_dms_with_instagrapi()
                
                if result:
                    print(f"✅ METHOD 5 SUCCESS: {len(result)} DM threads extracted")
                    return {'dms': result, 'method': 'instagrapi'}
                else:
                    print(f"❌ METHOD 5 FAILED: No DMs extracted")
                    return None
            else:
                print(f"❌ METHOD 5 FAILED: Login failed")
                return None
                
        except Exception as e:
            print(f"❌ METHOD 5 ERROR: {e}")
            return None
    
    def method_6_real_message_extractor(self):
        """Method 6: Real message extractor"""
        print(f"\n🔄 METHOD 6: Real Message Extractor")
        print("=" * 50)
        
        try:
            extractor = RealMessageExtractor()
            result = extractor.perform_message_extraction()
            
            if result and result.get('conversation_data'):
                print(f"✅ METHOD 6 SUCCESS: Messages extracted")
                return result
            else:
                print(f"❌ METHOD 6 FAILED: No messages extracted")
                return None
                
        except Exception as e:
            print(f"❌ METHOD 6 ERROR: {e}")
            return None
    
    def method_7_targeted_extractor(self):
        """Method 7: Targeted extractor for specific accounts"""
        print(f"\n🔄 METHOD 7: Targeted Extractor")
        print("=" * 50)
        
        try:
            extractor = DMExtractor()
            result = extractor.extract_dm()
            
            if result and result.get(self.target):
                print(f"✅ METHOD 7 SUCCESS: Targeted extraction completed")
                return result
            else:
                print(f"❌ METHOD 7 FAILED: No targeted data found")
                return None
                
        except Exception as e:
            print(f"❌ METHOD 7 ERROR: {e}")
            return None
    
    def perform_comprehensive_extraction(self):
        """ลองทุกวิธีเพื่อดึงข้อมูลจริง"""
        print(f"\n🎯 STARTING COMPREHENSIVE REAL DM EXTRACTION")
        print(f"===============================================")
        print(f"Target: {self.target}")
        print(f"Time: {datetime.now().isoformat()}")
        
        # List of all extraction methods
        methods = [
            ("Playwright Browser", self.method_1_playwright_browser),
            ("Instagram API", self.method_2_instagram_api_requests),
            ("Actual Extractor", self.method_3_actual_extractor),
            ("Advanced Techniques", self.method_4_advanced_techniques),
            ("Ultimate Working", self.method_5_ultimate_working_extractor),
            ("Real Message", self.method_6_real_message_extractor),
            ("Targeted", self.method_7_targeted_extractor),
        ]
        
        for method_name, method_func in methods:
            print(f"\n{'='*60}")
            print(f"🔄 ATTEMPTING: {method_name}")
            print(f"{'='*60}")
            
            try:
                result = method_func()
                
                if result:
                    self.successful_extractions.append({
                        'method': method_name,
                        'result': result,
                        'timestamp': datetime.now().isoformat()
                    })
                    print(f"✅ SUCCESS: {method_name}")
                else:
                    self.failed_extractions.append({
                        'method': method_name,
                        'error': 'No data returned',
                        'timestamp': datetime.now().isoformat()
                    })
                    print(f"❌ FAILED: {method_name}")
                
                # Small delay between methods
                time.sleep(2)
                
            except Exception as e:
                self.failed_extractions.append({
                    'method': method_name,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                print(f"❌ ERROR in {method_name}: {e}")
        
        return self.generate_final_report()
    
    def generate_final_report(self):
        """สร้างรายงานสุดท้าย"""
        timestamp = int(time.time())
        
        final_report = {
            'extraction_info': {
                'target': self.target,
                'extraction_timestamp': datetime.now().isoformat(),
                'total_methods_attempted': len(self.successful_extractions) + len(self.failed_extractions),
                'successful_methods': len(self.successful_extractions),
                'failed_methods': len(self.failed_extractions)
            },
            'successful_extractions': self.successful_extractions,
            'failed_extractions': self.failed_extractions,
            'summary': {
                'real_data_found': len(self.successful_extractions) > 0,
                'best_methods': [result['method'] for result in self.successful_extractions],
                'total_real_conversations': sum(
                    len(result['result'].get('conversations', [])) 
                    for result in self.successful_extractions 
                    if isinstance(result['result'], dict) and 'conversations' in result['result']
                )
            }
        }
        
        # Save final report
        output_file = f"{self.output_dir}/master_extraction_report_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎯 FINAL EXTRACTION REPORT")
        print(f"===========================")
        print(f"Target: {self.target}")
        print(f"Methods attempted: {final_report['extraction_info']['total_methods_attempted']}")
        print(f"Successful methods: {final_report['extraction_info']['successful_methods']}")
        print(f"Failed methods: {final_report['extraction_info']['failed_methods']}")
        print(f"Real data found: {'✅' if final_report['summary']['real_data_found'] else '❌'}")
        print(f"Report saved: {output_file}")
        
        if final_report['summary']['best_methods']:
            print(f"\n✅ SUCCESSFUL METHODS:")
            for method in final_report['summary']['best_methods']:
                print(f"   • {method}")
        
        return final_report

def main():
    """Main execution function"""
    print("🎯 MASTER REAL DM EXTRACTOR 2025")
    print("==================================")
    print("⚠️  WARNING: NO MOCKUP - REAL DATA EXTRACTION ONLY")
    print("This tool will attempt to extract real DM data using all available methods")
    
    # Confirm before proceeding
    response = input("\nContinue with real data extraction? (yes/no): ").lower()
    if response != 'yes':
        print("❌ Extraction cancelled")
        return
    
    extractor = MasterRealDMExtractor()
    result = extractor.perform_comprehensive_extraction()
    
    print("\n🎯 MASTER EXTRACTION COMPLETED")
    print("Real data extraction attempt finished")
    
    return result

if __name__ == "__main__":
    main()
