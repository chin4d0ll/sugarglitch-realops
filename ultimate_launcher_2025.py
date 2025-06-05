#!/usr/bin/env python3
"""
🚀 ULTIMATE EXTRACTION LAUNCHER 2025
====================================
Central control panel for all ALX.Trading DM extraction operations
Provides easy access to all tools, status monitoring, and recovery options
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime

class UltimateLauncher:
    def __init__(self):
        self.base_path = "/workspaces/sugarglitch-realops"
        self.extractors = {
            '1': {
                'name': 'Master Stable Extractor 2025 (RECOMMENDED)',
                'file': 'master_stable_extractor_2025.py',
                'description': 'Ultimate multi-method extractor with advanced features',
                'status': '🔥 LATEST'
            },
            '2': {
                'name': 'Advanced Stable DM Extractor',
                'file': 'advanced_stable_dm_extractor.py',
                'description': 'Proven stable extractor with multi-method fallbacks',
                'status': '✅ STABLE'
            },
            '3': {
                'name': 'Ultimate ALX Extractor 2025',
                'file': 'ultimate_alx_extractor_2025.py',
                'description': 'Advanced session management and token rotation',
                'status': '⚡ ADVANCED'
            },
            '4': {
                'name': 'Real Operations Launcher',
                'file': 'real_operations_launcher.py',
                'description': 'Production-ready launcher with database integration',  
                'status': '🎯 PRODUCTION'
            },
            '5': {
                'name': 'Safe Post-Block Extractor',
                'file': 'safe_post_block_extractor.py',
                'description': 'Gentle extraction for post-IP-block recovery',
                'status': '🛡️ RECOVERY'
            }
        }
        
        self.tools = {
            'a': {
                'name': 'System Status Check',
                'function': self.show_system_status,
                'description': 'Check all components and recent extractions'
            },
            'b': {
                'name': 'Instagram Block Recovery',
                'file': 'instagram_block_recovery.py',
                'description': 'Guide for recovering from IP blocks'
            },
            'c': {
                'name': 'IP Rotation Handler',
                'file': 'ip_rotation_handler.py',
                'description': 'Manage proxy rotation and IP changes'
            },
            'd': {
                'name': 'Session Validator',
                'file': 'session_validator.py',
                'description': 'Validate Instagram session credentials'
            },
            'e': {
                'name': 'Comprehensive System Test',
                'file': 'comprehensive_system_test.py',
                'description': 'Full system validation and testing'
            }
        }
    
    def show_banner(self):
        """Display the launcher banner"""
        print("🚀" + "=" * 60 + "🚀")
        print("🎯 ULTIMATE ALX.TRADING DM EXTRACTION LAUNCHER 2025")
        print("=" * 62)
        print(f"📅 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Working Directory: {self.base_path}")
        print("🔥 Status: FULLY OPERATIONAL")
        print("=" * 62)
    
    def show_system_status(self):
        """Show current system status"""
        print("\n🔍 SYSTEM STATUS CHECK")
        print("=" * 40)
        
        # Check key extractors
        print("📊 EXTRACTOR STATUS:")
        for key, extractor in self.extractors.items():
            file_path = os.path.join(self.base_path, extractor['file'])
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"  ✅ {extractor['name']}: {size:,} bytes")
            else:
                print(f"  ❌ {extractor['name']}: MISSING")
        
        # Check databases
        print("\n💾 DATABASE STATUS:")
        data_dir = os.path.join(self.base_path, 'data')
        if os.path.exists(data_dir):
            db_files = [f for f in os.listdir(data_dir) if f.endswith('.db')]
            print(f"  📁 Database files: {len(db_files)}")
            for db in db_files[:5]:  # Show first 5
                size = os.path.getsize(os.path.join(data_dir, db))
                print(f"    • {db}: {size:,} bytes")
        else:
            print("  ❌ data/ directory missing")
        
        # Check recent extractions
        print("\n📈 RECENT EXTRACTIONS:")
        sqlite_files = [f for f in os.listdir(self.base_path) if f.endswith('.sqlite')]
        json_files = [f for f in os.listdir(self.base_path) if 'extraction' in f and f.endswith('.json')]
        
        print(f"  📊 Total SQLite DBs: {len(sqlite_files)}")
        print(f"  📄 Total JSON reports: {len(json_files)}")
        
        if json_files:
            print("  Latest extractions:")
            for f in sorted(json_files)[-3:]:
                print(f"    • {f}")
        
        # Check sessions
        sessions_dir = os.path.join(self.base_path, 'sessions')
        hijacked_dir = os.path.join(self.base_path, 'hijacked_sessions')
        
        session_count = 0
        if os.path.exists(sessions_dir):
            session_count += len([f for f in os.listdir(sessions_dir) if f.endswith('.json')])
        if os.path.exists(hijacked_dir):
            session_count += len([f for f in os.listdir(hijacked_dir) if f.endswith('.json')])
        
        print(f"\n🔐 SESSION STATUS:")
        print(f"  📊 Available sessions: {session_count}")
        
        input("\n📱 Press Enter to return to main menu...")
    
    def show_extractors_menu(self):
        """Show extractor selection menu"""
        print("\n🎯 DM EXTRACTION TOOLS")
        print("=" * 40)
        
        for key, extractor in self.extractors.items():
            status_icon = "✅" if os.path.exists(os.path.join(self.base_path, extractor['file'])) else "❌"
            print(f"{key}. {status_icon} {extractor['name']} {extractor['status']}")
            print(f"   {extractor['description']}")
            print()
        
        print("0. Return to main menu")
        print("=" * 40)
    
    def show_tools_menu(self):
        """Show tools and utilities menu"""
        print("\n🛠️ TOOLS & UTILITIES")
        print("=" * 40)
        
        for key, tool in self.tools.items():
            if 'file' in tool:
                status_icon = "✅" if os.path.exists(os.path.join(self.base_path, tool['file'])) else "❌"
                print(f"{key}. {status_icon} {tool['name']}")
            else:
                print(f"{key}. 🔍 {tool['name']}")
            print(f"   {tool['description']}")
            print()
        
        print("0. Return to main menu")
        print("=" * 40)
    
    def run_extractor(self, extractor_key):
        """Run selected extractor"""
        if extractor_key not in self.extractors:
            print("❌ Invalid selection")
            return
        
        extractor = self.extractors[extractor_key]
        file_path = os.path.join(self.base_path, extractor['file'])
        
        if not os.path.exists(file_path):
            print(f"❌ {extractor['file']} not found")
            return
        
        print(f"\n🚀 Launching {extractor['name']}...")
        print("=" * 50)
        
        # Get target
        target = input("🎯 Enter target username (default: alx.trading): ").strip()
        if not target:
            target = "alx.trading"
        
        # Confirm launch
        print(f"\n📋 LAUNCH CONFIRMATION:")
        print(f"  🎯 Target: @{target}")
        print(f"  🔧 Extractor: {extractor['name']}")
        print(f"  📁 File: {extractor['file']}")
        
        confirm = input("\n🚀 Launch extraction? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Launch cancelled")
            return
        
        # Launch extractor
        try:
            os.chdir(self.base_path)
            if target != "alx.trading":
                subprocess.run([sys.executable, extractor['file'], target])
            else:
                subprocess.run([sys.executable, extractor['file']])
        except KeyboardInterrupt:
            print("\n🛑 Extraction interrupted by user")
        except Exception as e:
            print(f"❌ Error launching extractor: {e}")
        
        input("\n📱 Press Enter to continue...")
    
    def run_tool(self, tool_key):
        """Run selected tool"""
        if tool_key not in self.tools:
            print("❌ Invalid selection")
            return
        
        tool = self.tools[tool_key]
        
        if 'function' in tool:
            # Built-in function
            tool['function']()
        elif 'file' in tool:
            # External script
            file_path = os.path.join(self.base_path, tool['file'])
            
            if not os.path.exists(file_path):
                print(f"❌ {tool['file']} not found")
                input("📱 Press Enter to continue...")
                return
            
            print(f"\n🔧 Running {tool['name']}...")
            print("=" * 40)
            
            try:
                os.chdir(self.base_path)
                subprocess.run([sys.executable, tool['file']])
            except KeyboardInterrupt:
                print("\n🛑 Tool interrupted by user")
            except Exception as e:
                print(f"❌ Error running tool: {e}")
            
            input("\n📱 Press Enter to continue...")
    
    def show_quick_actions(self):
        """Show quick actions menu"""
        print("\n⚡ QUICK ACTIONS")
        print("=" * 30)
        print("1. 🎯 Extract @alx.trading (Master Extractor)")
        print("2. 🔍 Check System Status")
        print("3. 🚨 Instagram Block Recovery")
        print("4. 🧪 Run System Test")
        print("5. 💾 View Recent Results")
        print("0. Return to main menu")
        print("=" * 30)
    
    def handle_quick_action(self, action):
        """Handle quick action selection"""
        if action == '1':
            # Quick extraction with master extractor
            self.run_extractor('1')
        elif action == '2':
            self.show_system_status()
        elif action == '3':
            self.run_tool('b')
        elif action == '4':
            self.run_tool('e')
        elif action == '5':
            self.show_recent_results()
        else:
            print("❌ Invalid selection")
    
    def show_recent_results(self):
        """Show recent extraction results"""
        print("\n📊 RECENT EXTRACTION RESULTS")
        print("=" * 40)
        
        # Find recent JSON reports
        json_files = []
        for f in os.listdir(self.base_path):
            if 'extraction' in f and f.endswith('.json'):
                file_path = os.path.join(self.base_path, f)
                mtime = os.path.getmtime(file_path)
                json_files.append((f, mtime))
        
        json_files.sort(key=lambda x: x[1], reverse=True)
        
        if not json_files:
            print("📭 No extraction results found")
            input("📱 Press Enter to continue...")
            return
        
        print(f"Found {len(json_files)} extraction reports:")
        print()
        
        for i, (filename, mtime) in enumerate(json_files[:10], 1):
            mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Try to read summary from JSON
            try:
                with open(os.path.join(self.base_path, filename), 'r') as f:
                    data = json.load(f)
                    
                messages_count = 0
                if 'summary' in data:
                    messages_count = data['summary'].get('total_messages', 0)
                elif 'statistics' in data:
                    messages_count = data['statistics'].get('total_messages', 0)
                elif 'messages' in data:
                    messages_count = len(data['messages'])
                
                print(f"{i:2d}. 📄 {filename}")
                print(f"    📅 {mod_time}")
                print(f"    💬 Messages: {messages_count}")
                print()
                
            except Exception as e:
                print(f"{i:2d}. 📄 {filename}")
                print(f"    📅 {mod_time}")
                print(f"    ❌ Error reading file: {e}")
                print()
        
        input("📱 Press Enter to continue...")
    
    def run(self):
        """Main launcher loop"""
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            self.show_banner()
            
            print("\n🎯 MAIN MENU")
            print("=" * 20)
            print("1. 🎯 DM Extractors")
            print("2. 🛠️ Tools & Utilities")
            print("3. ⚡ Quick Actions")
            print("4. 📊 System Status")
            print("5. 📈 Recent Results")
            print("q. 🚪 Quit")
            print("=" * 20)
            
            choice = input("\n🎮 Select option: ").strip().lower()
            
            if choice == 'q' or choice == 'quit':
                print("\n👋 Goodbye!")
                break
            elif choice == '1':
                while True:
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.show_banner()
                    self.show_extractors_menu()
                    
                    extractor_choice = input("🎮 Select extractor (0 to go back): ").strip()
                    
                    if extractor_choice == '0':
                        break
                    elif extractor_choice in self.extractors:
                        self.run_extractor(extractor_choice)
                    else:
                        print("❌ Invalid selection")
                        time.sleep(1)
            
            elif choice == '2':
                while True:
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.show_banner()
                    self.show_tools_menu()
                    
                    tool_choice = input("🎮 Select tool (0 to go back): ").strip().lower()
                    
                    if tool_choice == '0':
                        break
                    elif tool_choice in self.tools:
                        self.run_tool(tool_choice)
                    else:
                        print("❌ Invalid selection")
                        time.sleep(1)
            
            elif choice == '3':
                while True:
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.show_banner()
                    self.show_quick_actions()
                    
                    action_choice = input("🎮 Select action (0 to go back): ").strip()
                    
                    if action_choice == '0':
                        break
                    else:
                        self.handle_quick_action(action_choice)
            
            elif choice == '4':
                self.show_system_status()
            
            elif choice == '5':
                self.show_recent_results()
            
            else:
                print("❌ Invalid selection")
                time.sleep(1)

def main():
    """Main function"""
    try:
        launcher = UltimateLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted. Goodbye!")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")

if __name__ == "__main__":
    main()
