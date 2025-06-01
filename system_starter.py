#!/usr/bin/env python3
"""
RealOps System Starter
Quick setup and demonstration script
"""

import os
import sys
import time
import subprocess
from typing import List

class RealOpsStarter:
    def __init__(self):
        self.base_dir = "/workspaces/sugarglitch-realops"
        
    def show_banner(self):
        """Display system banner"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 RealOps Enhanced System                 ║
║              Advanced Database & Monitoring Platform           ║
╚══════════════════════════════════════════════════════════════╝

Enhanced sugarglitch-realops with:
✅ Advanced Database Operations    ✅ Real-time Monitoring
✅ Automated Maintenance           ✅ Cookie Analysis  
✅ Performance Analytics           ✅ Risk Assessment
""")
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        required_packages = ['flask', 'schedule', 'sqlite3']
        missing = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"❌ Missing packages: {', '.join(missing)}")
            print("📦 Install with: pip install flask schedule")
            return False
        
        return True
    
    def check_database(self) -> bool:
        """Check if database exists and has data"""
        db_path = os.path.join(self.base_dir, "project_realops.db")
        
        if not os.path.exists(db_path):
            print("❌ Database not found: project_realops.db")
            return False
        
        import sqlite3
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM targets")
            count = cursor.fetchone()[0]
            conn.close()
            
            if count == 0:
                print("⚠️  Database exists but has no data")
                return False
            
            print(f"✅ Database ready with {count} targets")
            return True
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
    
    def run_quick_analysis(self):
        """Run the quick analysis"""
        print("\n🔍 Running Quick System Analysis...")
        print("-" * 50)
        
        try:
            result = subprocess.run([
                sys.executable, "quick_demo.py"
            ], cwd=self.base_dir, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"❌ Analysis failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⚠️  Analysis timed out")
        except Exception as e:
            print(f"❌ Analysis error: {e}")
    
    def start_dashboard(self, port: int = 5001):
        """Start the dashboard on specified port"""
        print(f"\n🌐 Starting Dashboard on port {port}...")
        print(f"   Access at: http://localhost:{port}")
        print("   Press Ctrl+C to stop")
        
        try:
            # Modify the dashboard to use different port
            dashboard_code = f"""
import sys
sys.path.append('{self.base_dir}')
from realtime_dashboard import app, start_dashboard
start_dashboard(host='0.0.0.0', port={port}, debug=False)
"""
            
            with open(f"{self.base_dir}/temp_dashboard.py", "w") as f:
                f.write(dashboard_code)
            
            subprocess.run([
                sys.executable, "temp_dashboard.py"
            ], cwd=self.base_dir)
            
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped")
        except Exception as e:
            print(f"❌ Dashboard error: {e}")
        finally:
            # Cleanup temp file
            temp_file = f"{self.base_dir}/temp_dashboard.py"
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def generate_sample_data(self):
        """Generate sample data if needed"""
        print("\n🎲 Generating Sample Data...")
        
        try:
            result = subprocess.run([
                sys.executable, "compatible_data_generator.py"
            ], cwd=self.base_dir, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(result.stdout)
                return True
            else:
                print(f"❌ Data generation failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️  Data generation timed out")
            return False
        except Exception as e:
            print(f"❌ Data generation error: {e}")
            return False
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\n" + "="*60)
            print("🎯 RealOps System Menu")
            print("="*60)
            print("1. 🔍 Run Quick Analysis")
            print("2. 🌐 Start Dashboard (port 5001)")
            print("3. 🎲 Generate Sample Data") 
            print("4. 📊 Show System Status")
            print("5. 🚪 Exit")
            print("="*60)
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == "1":
                self.run_quick_analysis()
            elif choice == "2":
                self.start_dashboard()
            elif choice == "3":
                self.generate_sample_data()
            elif choice == "4":
                self.show_system_status()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
    
    def show_system_status(self):
        """Show current system status"""
        print("\n📊 System Status Check")
        print("-" * 30)
        
        # Check database
        db_status = self.check_database()
        
        # Check files
        important_files = [
            "database_enhancements.py",
            "realtime_dashboard.py", 
            "automated_operations.py",
            "compatible_data_generator.py",
            "quick_demo.py"
        ]
        
        print(f"\n📄 Enhancement Files:")
        for file in important_files:
            path = os.path.join(self.base_dir, file)
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"   ✅ {file} ({size:,} bytes)")
            else:
                print(f"   ❌ {file} (missing)")
        
        # Check dependencies
        print(f"\n📦 Dependencies:")
        deps_ok = self.check_dependencies()
        
        print(f"\n🎯 Overall Status: {'✅ Ready' if db_status and deps_ok else '⚠️  Needs attention'}")
    
    def auto_setup(self):
        """Automatic setup if needed"""
        print("\n🔧 Auto-Setup Check...")
        
        if not self.check_database():
            print("📊 Database needs data. Generating...")
            if self.generate_sample_data():
                print("✅ Sample data generated successfully")
            else:
                print("❌ Failed to generate sample data")
                return False
        
        if not self.check_dependencies():
            print("❌ Please install missing dependencies first")
            return False
        
        print("✅ System ready!")
        return True

def main():
    """Main function"""
    starter = RealOpsStarter()
    starter.show_banner()
    
    print("🔧 Performing system checks...")
    
    if starter.auto_setup():
        print("\n🚀 System is ready!")
        starter.show_menu()
    else:
        print("\n❌ Setup failed. Please check requirements.")

if __name__ == "__main__":
    main()
