#!/usr/bin/env python3
"""
🔥💀⚡ EXTREME HARDCORE RUNNER ⚡💀🔥
================================
รันสคริปต์โหดๆ ทั้งหมดในที่เดียว!
"""

import subprocess
import sys
import time
import os

class ExtremeRunner:
    def __init__(self):
        self.scripts = [
            'ultimate_penetration_arsenal_2025.py',
            'ultimate_hacker_suite_2025.py', 
            'advanced_penetration_suite_2025.py',
            'ultimate_instagram_hacker_suite_2025.py'
        ]
        
    def display_banner(self):
        print("""
🔥💀⚡ EXTREME HARDCORE RUNNER ⚡💀🔥
===================================
   รันสคริปต์โหดๆ ทั้งหมด!
   NO MERCY - MAXIMUM POWER!
""")
    
    def run_script(self, script_name):
        """Run individual script with error handling"""
        try:
            print(f"\n🚀 Starting: {script_name}")
            
            # Check if file exists
            if not os.path.exists(script_name):
                print(f"❌ File not found: {script_name}")
                return False
                
            # Run with auto-input for testing
            process = subprocess.Popen(
                [sys.executable, script_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send test inputs
            test_inputs = "5\nwhatilove1728\n0\n"
            stdout, stderr = process.communicate(input=test_inputs, timeout=30)
            
            if process.returncode == 0:
                print(f"✅ {script_name} completed successfully!")
                if stdout:
                    print(f"📄 Output preview: {stdout[:200]}...")
                return True
            else:
                print(f"⚠️ {script_name} returned code {process.returncode}")
                if stderr:
                    print(f"🐛 Error: {stderr[:200]}...")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {script_name} timed out (30s)")
            process.kill()
            return False
        except Exception as e:
            print(f"❌ Error running {script_name}: {e}")
            return False
    
    def run_all(self):
        """Run all hardcore scripts"""
        self.display_banner()
        
        success_count = 0
        for script in self.scripts:
            if self.run_script(script):
                success_count += 1
            time.sleep(2)
            
        print(f"\n🏁 EXTREME RUNNER COMPLETE!")
        print(f"✅ Success: {success_count}/{len(self.scripts)} scripts")
        
        if success_count > 0:
            print("💀🔥 SOME HARDCORE SCRIPTS ARE WORKING! 🔥💀")
        else:
            print("⚠️ All scripts need debugging")

if __name__ == "__main__":
    runner = ExtremeRunner()
    runner.run_all()
