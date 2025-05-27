#!/usr/bin/env python3
"""
SugarGlitch RealOps - Extension Monitor
Real-time monitoring of VS Code extension processes and memory usage
"""

import psutil
import time
import json
import os
from datetime import datetime

class ExtensionMonitor:
    def __init__(self):
        self.memory_threshold = 1024 * 1024 * 1024  # 1GB in bytes
        self.log_file = "logs/extension_monitor.log"
        os.makedirs("logs", exist_ok=True)
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        print(log_entry.strip())
        with open(self.log_file, "a") as f:
            f.write(log_entry)
    
    def get_extension_processes(self):
        """Find all VS Code extension processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
            try:
                if 'extensionHost' in ' '.join(proc.info['cmdline']):
                    processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes
    
    def kill_memory_hogs(self):
        """Kill extension processes using too much memory"""
        killed = 0
        for proc in self.get_extension_processes():
            try:
                memory_usage = proc.memory_info().rss
                if memory_usage > self.memory_threshold:
                    self.log(f"Killing process {proc.pid} using {memory_usage // 1024 // 1024}MB")
                    proc.kill()
                    killed += 1
                    time.sleep(1)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return killed
    
    def get_system_memory(self):
        """Get current system memory usage"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used
        }
    
    def monitor(self, duration=60):
        """Monitor extensions for specified duration"""
        self.log("Starting extension monitoring...")
        
        start_time = time.time()
        check_interval = 5  # Check every 5 seconds
        
        while time.time() - start_time < duration:
            # Get current system memory
            memory = self.get_system_memory()
            
            # Get extension processes
            ext_processes = self.get_extension_processes()
            total_ext_memory = sum(proc.memory_info().rss for proc in ext_processes)
            
            # Log status
            status = {
                'timestamp': datetime.now().isoformat(),
                'system_memory_percent': memory['percent'],
                'system_memory_used_gb': memory['used'] / 1024 / 1024 / 1024,
                'extension_processes': len(ext_processes),
                'extension_memory_gb': total_ext_memory / 1024 / 1024 / 1024
            }
            
            self.log(f"Memory: {memory['percent']:.1f}% | Extensions: {len(ext_processes)} | Ext Memory: {total_ext_memory / 1024 / 1024:.1f}MB")
            
            # Kill memory hogs if system memory is high
            if memory['percent'] > 85:
                killed = self.kill_memory_hogs()
                if killed > 0:
                    self.log(f"Killed {killed} memory-hungry extension processes")
            
            time.sleep(check_interval)
        
        self.log("Monitoring complete")

def main():
    monitor = ExtensionMonitor()
    
    if len(os.sys.argv) > 1:
        try:
            duration = int(os.sys.argv[1])
        except ValueError:
            duration = 60
    else:
        duration = 60
    
    try:
        monitor.monitor(duration)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")

if __name__ == "__main__":
    main()
