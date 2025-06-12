#!/usr/bin/env python3
"""
🔥 SugarGlitch RealOps - Quick Personal Data Extractor
รวมข้อมูลส่วนตัวจากไฟล์หลักที่พบ
"""

import json
from pathlib import Path
from datetime import datetime

def extract_personal_data():
    """Extract personal data from known files"""
    print("🔥 SugarGlitch RealOps - Quick Data Extraction")
    print("=" * 50)
    
    # Initialize target structure
    targets = {
        "alx.trading": {
            "username": "alx.trading",
            "email": [],
            "phone": [],
            "ig_id": None,
            "sessions": [],
            "location_history": [],
            "breaches": [],
            "chat_patterns": [],
            "aliases": ["alx_trading", "Alex Fleming"],
            "linked_accounts": [],
            "flags": [],
            "business_info": {}
        },
        "whatilove1728": {
            "username": "whatilove1728", 
            "email": [],
            "phone": [],
            "ig_id": None,
            "sessions": [],
            "location_history": [],
            "breaches": [],
            "chat_patterns": [],
            "aliases": [],
            "linked_accounts": [],
            "flags": []
        }
    }
    
    project_root = Path(__file__).parent
    
    # Process ALX Trading master profile
    alx_master_file = project_root / "REAL_DATA_BACKUP_1749460588/config/json/MASTER_PROFILE_alx_trading_1748264047.json"
    if alx_master_file.exists():
        print("📄 Processing ALX master profile...")
        try:
            with open(alx_master_file, 'r') as f:
                alx_data = json.load(f)
                
            profile = alx_data.get("profile", {})
            intel = alx_data.get("intelligence_summary", {})
            
            # Extract ALX data
            targets["alx.trading"]["aliases"].extend([
                profile.get("real_name", ""),
                profile.get("business", "")
            ])
            targets["alx.trading"]["email"].extend(intel.get("email_addresses", []))
            targets["alx.trading"]["phone"].extend(intel.get("phone_numbers", []))
            targets["alx.trading"]["sessions"].extend(intel.get("sessions", []))
            targets["alx.trading"]["business_info"] = {
                "business": profile.get("business", ""),
                "focus": profile.get("business_focus", ""),
                "password": profile.get("confirmed_password", "")
            }
            
            if profile.get("confirmed_password"):
                targets["alx.trading"]["flags"].append("password_known")
            if intel.get("email_addresses"):
                targets["alx.trading"]["flags"].append("email_known")
            if intel.get("phone_numbers"):
                targets["alx.trading"]["flags"].append("phone_known")
            
            targets["alx.trading"]["flags"].append("high_value_target")
            targets["alx.trading"]["flags"].append("business_account")
            
            print(f"  ✅ Found {len(intel.get('email_addresses', []))} emails")
            print(f"  ✅ Found {len(intel.get('phone_numbers', []))} phones")
            print(f"  ✅ Found password: {profile.get('confirmed_password', 'N/A')}")
            
        except Exception as e:
            print(f"  ❌ Error processing ALX data: {e}")
    
    # Process whatilove1728 intelligence
    whatilove_intel = project_root / "data/instagram/rapid_intel_whatilove1728_1748234852.json"
    if whatilove_intel.exists():
        print("📄 Processing whatilove1728 intelligence...")
        try:
            with open(whatilove_intel, 'r') as f:
                whatilove_data = json.load(f)
            
            intel = whatilove_data.get("intelligence", {})
            username_analysis = intel.get("username_analysis", {})
            
            # Extract whatilove data
            if username_analysis.get("similar_usernames"):
                targets["whatilove1728"]["aliases"].extend(
                    username_analysis["similar_usernames"][:5]  # Top 5 aliases
                )
            
            # Add flags based on analysis
            profile_type = username_analysis.get("profile_type_indicators", {})
            if profile_type.get("personal_account") == "High probability":
                targets["whatilove1728"]["flags"].append("personal_account")
            
            # Add pattern analysis
            pattern = username_analysis.get("pattern_analysis", {})
            if pattern:
                targets["whatilove1728"]["chat_patterns"].append({
                    "pattern_type": "username_analysis",
                    "base": pattern.get("base", ""),
                    "number": pattern.get("number", ""),
                    "significance": pattern.get("mathematical_significance", "")
                })
            
            targets["whatilove1728"]["flags"].append("intelligence_available")
            
            print(f"  ✅ Found {len(targets['whatilove1728']['aliases'])} aliases")
            print(f"  ✅ Added username pattern analysis")
            
        except Exception as e:
            print(f"  ❌ Error processing whatilove data: {e}")
    
    # Process additional data files
    data_files = [
        "data/intelligence/INSTANT_EXTRACTION_whatilove1728_1748235098.json",
        "data/intelligence/EXPLOITATION_RESULTS_whatilove1728_1748235941.json",
        "data/intelligence/GHOST_OPERATION_DATA_whatilove1728_1748239114.json"
    ]
    
    for file_path in data_files:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r') as f:
                    data = json.load(f)
                
                # Extract any additional sessions or data
                if "extraction_results" in data:
                    results = data["extraction_results"]
                    if results.get("success_methods"):
                        targets["whatilove1728"]["sessions"].extend(
                            results["success_methods"]
                        )
                
            except Exception as e:
                print(f"  ⚠️  Error reading {file_path}: {e}")
    
    # Clean up data
    for target_name, target_data in targets.items():
        # Remove duplicates
        target_data["email"] = list(set(filter(None, target_data["email"])))
        target_data["phone"] = list(set(filter(None, target_data["phone"])))
        target_data["aliases"] = list(set(filter(None, target_data["aliases"])))
        target_data["sessions"] = list(set(filter(None, target_data["sessions"])))
        target_data["flags"] = list(set(target_data["flags"]))
    
    # Create final structure
    result = {
        "targets": list(targets.values()),
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "1.0",
            "extraction_method": "manual_file_parsing",
            "total_targets": len(targets)
        }
    }
    
    # Save to file
    output_file = project_root / "data/realops_targets.json"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to: {output_file}")
    
    # Summary
    print("\n📋 EXTRACTION SUMMARY:")
    print("=" * 30)
    for target in result["targets"]:
        print(f"🎯 {target['username']}:")
        print(f"   📧 Emails: {len(target['email'])}")
        print(f"   📱 Phones: {len(target['phone'])}")
        print(f"   🔐 Sessions: {len(target['sessions'])}")
        print(f"   👤 Aliases: {len(target['aliases'])}")
        print(f"   🏷️  Flags: {', '.join(target['flags'])}")
        if target.get('business_info'):
            print(f"   💼 Business: {target['business_info'].get('business', 'N/A')}")
        print()
    
    return output_file

if __name__ == "__main__":
    extract_personal_data()
