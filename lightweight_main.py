#!/usr/bin/env python3
"""
SugarGlitch RealOps - Lightweight Memory-Optimized Version
Minimal RAM usage with essential features only
"""

import os
import sys
import gc
from pathlib import Path

# Force memory optimization from the start
gc.set_threshold(100, 5, 5)  # More aggressive garbage collection
os.environ['PYTHONMALLOC'] = 'pymalloc'
os.environ['NODE_OPTIONS'] = '--max-old-space-size=512'

# Minimal imports to reduce memory footprint
try:
    import psutil
except ImportError:
    print("⚠️ psutil not found. Install with: pip install psutil")
    sys.exit(1)

class LightweightRealOps:
    def __init__(self):
        self.workspace = Path("/workspaces/sugarglitch-realops")
        self.clear_screen()
        self.show_header()
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_header(self):
        print("🍭 SugarGlitch RealOps - Lightweight Mode")
        print("=" * 50)
        self.show_memory_status()
        print("=" * 50)
    
    def show_memory_status(self):
        """Show current memory usage"""
        try:
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            print(f"💻 System Status:")
            print(f"   RAM: {memory.used/1024**3:.1f}GB / {memory.total/1024**3:.1f}GB ({memory.percent:.1f}%)")
            print(f"   CPU: {cpu_percent:.1f}%")
            print(f"   Available: {memory.available/1024**3:.1f}GB")
            
            if memory.percent > 80:
                print("⚠️ WARNING: High memory usage detected!")
        except Exception as e:
            print(f"⚠️ Could not get system status: {e}")
    
    def quick_memory_cleanup(self):
        """Quick memory cleanup"""
        print("\n🧹 Quick Memory Cleanup...")
        
        # Python garbage collection
        collected = gc.collect()
        print(f"   Collected {collected} objects")
        
        # Clear unnecessary variables
        for var in list(globals().keys()):
            if var.startswith('_') and var != '__name__':
                del globals()[var]
        
        print("✅ Memory cleanup completed")
        gc.collect()
    
    def show_simple_menu(self):
        """Show lightweight menu"""
        print("\n📋 Available Actions:")
        print("1. 🔍 System Status")
        print("2. 🧹 Memory Cleanup") 
        print("3. 📊 Process Monitor")
        print("4. ⚙️ Run Memory Optimizer")
        print("5. 🔧 Quick Instagram Test")
        print("6. 📝 View Logs")
        print("0. 🚪 Exit")
        
        return input("\n👉 Select option (0-6): ").strip()
    
    def run_memory_optimizer(self):
        """Run the comprehensive memory optimizer"""
        print("\n🚀 Running Memory Optimizer...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, "optimize_memory.py"], 
                                  cwd=self.workspace, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"⚠️ Warnings: {result.stderr}")
        except Exception as e:
            print(f"❌ Error running optimizer: {e}")
    
    def show_process_monitor(self):
        """Show top memory-consuming processes"""
        print("\n📊 Top Memory Consumers:")
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    if memory_mb > 50:  # Only show processes using >50MB
                        processes.append((proc.info['name'], memory_mb, proc.info['pid']))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            processes.sort(key=lambda x: x[1], reverse=True)
            
            for i, (name, memory_mb, pid) in enumerate(processes[:10]):
                print(f"   {i+1:2d}. {name:<20} {memory_mb:>6.1f}MB (PID: {pid})")
                
        except Exception as e:
            print(f"❌ Error getting processes: {e}")
    
    def quick_instagram_test(self):
        """Quick Instagram connectivity test"""
        print("\n🔍 Quick Instagram Test...")
        try:
            import requests
            response = requests.get("https://www.instagram.com", timeout=5)
            if response.status_code == 200:
                print("✅ Instagram is accessible")
            else:
                print(f"⚠️ Instagram returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ Instagram test failed: {e}")
        finally:
            # Clean up imports to save memory
            if 'requests' in locals():
                del requests
            gc.collect()
    
    def view_logs(self):
        """View recent logs"""
        print("\n📝 Recent Logs:")
        log_dir = self.workspace / "logs"
        
        if not log_dir.exists():
            print("   No logs directory found")
            return
        
        log_files = sorted(log_dir.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not log_files:
            print("   No log files found")
            return
        
        # Show last 10 lines of most recent log
        latest_log = log_files[0]
        print(f"   📄 {latest_log.name}:")
        
        try:
            with open(latest_log, 'r') as f:
                lines = f.readlines()
                for line in lines[-10:]:
                    print(f"     {line.strip()}")
        except Exception as e:
            print(f"   ❌ Error reading log: {e}")
    
    def run(self):
        """Main application loop"""
        while True:
            try:
                choice = self.show_simple_menu()
                
                if choice == '0':
                    print("\n👋 Goodbye!")
                    break
                elif choice == '1':
                    self.clear_screen()
                    self.show_header()
                elif choice == '2':
                    self.quick_memory_cleanup()
                elif choice == '3':
                    self.show_process_monitor()
                elif choice == '4':
                    self.run_memory_optimizer()
                elif choice == '5':
                    self.quick_instagram_test()
                elif choice == '6':
                    self.view_logs()
                else:
                    print("❌ Invalid option. Please try again.")
                
                # Force garbage collection after each action
                gc.collect()
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")

if __name__ == "__main__":
    app = LightweightRealOps()
    app.run()
