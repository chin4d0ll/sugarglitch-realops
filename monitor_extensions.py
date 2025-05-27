#!/usr/bin/env python3
"""
🔍 VS Code Extension Monitor
ตรวจสอบและแก้ไขปัญหา Remote Extensions ที่รีรันซ้ำๆ แบบอัตโนมัติ
"""

import subprocess
import time
import json
import os
from datetime import datetime

class VSCodeExtensionMonitor:
    def __init__(self):
        self.max_instances = {
            'codeium': 2,
            'sqltools': 2, 
            'mssql': 2,
            'pylance': 1
        }
        
    def get_extension_processes(self):
        """ดูจำนวน processes ของแต่ละ extension"""
        processes = {}
        
        try:
            # Get all processes
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if 'codeium' in line.lower():
                    processes.setdefault('codeium', []).append(line)
                elif 'sqltools' in line.lower():
                    processes.setdefault('sqltools', []).append(line)
                elif 'mssql' in line.lower() or 'MicrosoftSqlToolsServiceLayer' in line:
                    processes.setdefault('mssql', []).append(line)
                elif 'pylance' in line.lower():
                    processes.setdefault('pylance', []).append(line)
                    
        except Exception as e:
            print(f"❌ Error getting processes: {e}")
            
        return processes
    
    def kill_excess_processes(self, extension_name, processes):
        """ฆ่า processes ที่เกินจำนวนที่กำหนด"""
        max_allowed = self.max_instances.get(extension_name, 2)
        
        if len(processes) > max_allowed:
            print(f"⚠️ {extension_name}: {len(processes)} processes (max: {max_allowed})")
            
            # Kill excess processes (keep the oldest ones)
            excess_count = len(processes) - max_allowed
            
            for i in range(excess_count):
                try:
                    # Extract PID from process line
                    parts = processes[i].split()
                    if len(parts) > 1:
                        pid = parts[1]
                        subprocess.run(['kill', '-9', pid], check=False)
                        print(f"🔪 Killed excess {extension_name} process (PID: {pid})")
                except Exception as e:
                    print(f"❌ Error killing process: {e}")
    
    def check_and_fix(self):
        """ตรวจสอบและแก้ไขปัญหา"""
        print(f"\n🔍 Extension Monitor Check - {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 50)
        
        processes = self.get_extension_processes()
        
        if not processes:
            print("✅ No problematic extension processes found")
            return
        
        for ext_name, proc_list in processes.items():
            if len(proc_list) > self.max_instances.get(ext_name, 2):
                self.kill_excess_processes(ext_name, proc_list)
            else:
                print(f"✅ {ext_name}: {len(proc_list)} processes (OK)")
    
    def monitor_continuous(self, check_interval=30):
        """ตรวจสอบแบบต่อเนื่อง"""
        print("🚀 Starting VS Code Extension Monitor...")
        print(f"📊 Check interval: {check_interval} seconds")
        print("🛑 Press Ctrl+C to stop")
        
        try:
            while True:
                self.check_and_fix()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped by user")
        except Exception as e:
            print(f"\n❌ Monitor error: {e}")

def main():
    monitor = VSCodeExtensionMonitor()
    
    print("🔧 VS Code Extension Monitor & Fixer")
    print("=" * 50)
    
    choice = input("""
Select mode:
1. Single check and fix
2. Continuous monitoring (30s intervals)
3. Quick cleanup only

Enter choice (1-3): """).strip()
    
    if choice == '1':
        monitor.check_and_fix()
    elif choice == '2':
        monitor.monitor_continuous()
    elif choice == '3':
        # Quick cleanup
        subprocess.run(['pkill', '-f', 'codeium.*language_server'], check=False)
        subprocess.run(['pkill', '-f', 'MicrosoftSqlToolsServiceLayer'], check=False)
        subprocess.run(['pkill', '-f', 'SqlToolsResourceProviderService'], check=False)
        print("🧹 Quick cleanup completed")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
