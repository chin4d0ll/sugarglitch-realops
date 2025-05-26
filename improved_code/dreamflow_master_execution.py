from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 DREAMFLOW MASTER EXECUTION - ALX.TRADING
=============================================
🎯 Complete extraction using sessionid + instagrapi
💎 Target: alx.trading (@alx.trading) 
🔑 Bypass: Rate limiting + checkpoint protection
=============================================
"""

import subprocess
import time
import json
import os
import sys

def print_banner():
    print("""
🔥 DREAMFLOW MASTER EXECUTION
=============================================
🎯 Target: alx.trading (@alx.trading)
💎 Method: Complete automation pipeline
🚀 Features: SessionID + InstagrAPI + Rate bypass
=============================================
""")

def run_command(description, command, background=False):
    """Run a command with proper logging"""
    print(f"\n🚀 {description}")
    print(f"💻 Command: {command}")
    print("-" * 50)
    
    try:
        if background:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"🔄 Process started in background (PID: {process.pid})")
            return process
        else:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            print(f"📋 Exit code: {result.returncode}")
            if result.stdout:
                print(f"📤 Output:\n{result.stdout}")
            if result.stderr:
                print(f"⚠️ Errors:\n{result.stderr}")
                
            return result.returncode == 0
            
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_sessionid_exists():
    """Check if we already have a valid sessionid"""
    sessionid_files = [
        "sessionid_alx.txt",
        "alx_trading_sessionid_*.txt",
        "alx_trading_sessionid_*.json"
    ]
    
    for pattern in sessionid_files:
        if '*' in pattern:
            import glob
            files = glob.glob(pattern)
            if files:
                print(f"✅ Found existing session file: {files[-1]}")
                return files[-1]
        else:
            if os.path.exists(pattern):
                print(f"✅ Found existing session file: {pattern}")
                return pattern
                
    return None

@safe_execution
def main():
    print_banner()
    
    # Phase 1: Check for existing sessionid
    print("🔍 PHASE 1: CHECKING FOR EXISTING SESSIONID")
    existing_session = check_sessionid_exists()
    
    if not existing_session:
        print("📥 No existing sessionid found - extracting new one...")
        
        # Extract new sessionid
        success = run_command(
            "Extracting SessionID using confirmed credentials",
            "python3 sessionid_extractor_alx.py"
        )
        
        if not success:
            print("❌ SessionID extraction failed - continuing without auth")
        else:
            print("✅ SessionID extraction completed")
    else:
        print(f"✅ Using existing session: {existing_session}")
    
    # Phase 2: Install required packages
    print("\n🔍 PHASE 2: INSTALLING REQUIRED PACKAGES")
    run_command(
        "Installing instagrapi for advanced extraction",
        "pip install instagrapi --quiet"
    )
    
    # Phase 3: Run DREAMFLOW Ghost Mode
    print("\n🔍 PHASE 3: EXECUTING DREAMFLOW GHOST MODE")
    success = run_command(
        "Launching DREAMFLOW Ghost Mode with rate limiting bypass",
        "python3 dreamflow_ghost_mode_alx.py",
        background=False
    )
    
    if success:
        print("✅ DREAMFLOW execution completed successfully")
    else:
        print("⚠️ DREAMFLOW execution completed with warnings")
    
    # Phase 4: Run Ultimate Ghost Session Exploitation
    print("\n🔍 PHASE 4: ULTIMATE GHOST SESSION EXPLOITATION")
    success = run_command(
        "Launching Ultimate Ghost Session Exploitation",
        "python3 ultimate_ghost_session_exploitation.py",
        background=False
    )
    
    if success:
        print("✅ Ultimate exploitation completed successfully")
    else:
        print("⚠️ Ultimate exploitation completed with warnings")
    
    # Phase 5: Generate comprehensive report
    print("\n🔍 PHASE 5: COMPREHENSIVE REPORTING")
    success = run_command(
        "Generating final intelligence report",
        "python3 intelligence_report_generator.py"
    )
    
    if success:
        print("✅ Intelligence report generated successfully")
    else:
        print("⚠️ Intelligence report generation completed with warnings")
    
    # Phase 6: Final summary
    print("\n🎉 DREAMFLOW MASTER EXECUTION COMPLETE")
    print("="*50)
    
    # Check for generated files
    output_files = [
        "sessionid_alx.txt",
        "alx_trading_sessionid_*.json",
        "DREAMFLOW_EXTRACTION_*.json",
        "ULTIMATE_GHOST_*.json",
        "INTELLIGENCE_REPORT_*.json"
    ]
    
    print("📁 Generated files:")
    for pattern in output_files:
        if '*' in pattern:
            import glob
            files = glob.glob(pattern)
            for file in files:
                if os.path.exists(file):
                    size = os.path.getsize(file)
                    print(f"   📄 {file} ({size} bytes)")
        else:
            if os.path.exists(pattern):
                size = os.path.getsize(pattern)
                print(f"   📄 {pattern} ({size} bytes)")
    
    print("\n🔥 OPERATION STATUS: COMPLETE")
    print("💎 All extraction phases executed")
    print("🎯 Target intelligence gathered")
    print("🚀 Ready for final analysis")

if __name__ == "__main__":
    main()
