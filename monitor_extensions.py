#!/usr/bin/env python3
"""
VS Code Extension Monitor
Prevents multiple extensionHost processes and monitors memory usage
"""
import os
import time
import subprocess
import psutil
import signal
import sys
from datetime import datetime

class ExtensionMonitor:
    def __init__(self):
        self.max_extension_hosts = 2  # Allow max 2 extension hosts
        self.memory_threshold = 85    # Kill if memory usage > 85%
        self.check_interval = 30      # Check every 30 seconds
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def get_extension_hosts(self):
        """Get all extensionHost processes"""
        procs = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_percent', 'create_time']):
            try:
                if 'extensionHost' in ' '.join(proc.info['cmdline'] or []):
                    procs.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return procs
        
    def kill_old_extension_hosts(self, procs):
        """Kill older extensionHost processes, keep the newest ones"""
        if len(procs) <= self.max_extension_hosts:
            return
            
        # Sort by creation time, newest first
        procs.sort(key=lambda p: p.info['create_time'], reverse=True)
        
        # Kill older processes
        for proc in procs[self.max_extension_hosts:]:
            try:
                self.log(f"Killing old extensionHost PID {proc.pid}")
                proc.kill()
                proc.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                pass
                
    def check_memory_usage(self):
        """Check system memory usage"""
        memory = psutil.virtual_memory()
        if memory.percent > self.memory_threshold:
            self.log(f"⚠️  High memory usage: {memory.percent:.1f}%")
            return True
        return False
        
    def cleanup_temp_files(self):
        """Clean up temporary VS Code files"""
        try:
            cmd = ["find", "/tmp", "-name", "*vscode*", "-type", "f", "-mmin", "+60", "-delete"]
            subprocess.run(cmd, capture_output=True, timeout=10)
        except subprocess.TimeoutExpired:
            pass
            
    def monitor(self):
        """Main monitoring loop"""
        self.log("🔍 Starting Extension Monitor...")
        
        while True:
            try:
                # Get extension hosts
                ext_hosts = self.get_extension_hosts()
                
                if len(ext_hosts) > self.max_extension_hosts:
                    self.log(f"Found {len(ext_hosts)} extensionHost processes (max: {self.max_extension_hosts})")
                    self.kill_old_extension_hosts(ext_hosts)
                    
                # Check memory
                if self.check_memory_usage():
                    # Force cleanup if memory is high
                    self.cleanup_temp_files()
                    
                # Log status
                memory = psutil.virtual_memory()
                self.log(f"Status: {len(ext_hosts)} ext hosts, {memory.percent:.1f}% RAM used")
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.log("Monitor stopped by user")
                break
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(5)

def signal_handler(sig, frame):
    print("\n🛑 Extension monitor stopped")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    monitor = ExtensionMonitor()
    monitor.monitor()
