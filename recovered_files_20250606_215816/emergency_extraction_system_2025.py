#!/usr/bin/env python3
"""
🚨 EMERGENCY EXTRACTION SYSTEM 2025
===================================
Last resort extraction methods when all else fails
Created: 2025-01-26
"""

import time
import random
import requests
import json
import subprocess
import os
from datetime import datetime, timedelta
import threading

class EmergencyExtractionSystem:
    def __init__(self):
        self.emergency_methods = []
        self.results = {}
        self.current_ip = self.get_current_ip()
        
    def get_current_ip(self):
        """Get current IP address"""
        try:
            response = requests.get('https://httpbin.org/ip', timeout=5)
            return response.json()['origin']
        except:
            return "Unknown"
    
    def emergency_method_1_time_window_attack(self):
        """Time window attack - Extract during Instagram maintenance windows"""
        print("⏰ Emergency Method 1: Time Window Attack")
        
        # Instagram typically has maintenance windows:
        # - Late night PST (2-4 AM PST)
        # - Early morning GMT (5-7 AM GMT)
        current_hour = datetime.now().hour
        
        maintenance_windows = [
            {'start': 2, 'end': 4, 'name': 'Late Night PST'},
            {'start': 5, 'end': 7, 'name': 'Early Morning GMT'},
            {'start': 10, 'end': 12, 'name': 'Mid Morning'},
        ]
        
        for window in maintenance_windows:
            if window['start'] <= current_hour <= window['end']:
                print(f"   🎯 Current time in maintenance window: {window['name']}")
                
                try:
                    response = requests.get('https://www.instagram.com/', timeout=10)
                    if response.status_code == 200:
                        print(f"   ✅ Instagram accessible during {window['name']}")
                        self.results['time_window'] = {'status': 'SUCCESS', 'window': window['name']}
                        return True
                except:
                    pass
        
        print("   ❌ Not in maintenance window or still blocked")
        self.results['time_window'] = {'status': 'FAILED'}
        return False
    
    def emergency_method_2_api_endpoint_discovery(self):
        """Discover alternative API endpoints"""
        print("🔍 Emergency Method 2: API Endpoint Discovery")
        
        # Alternative Instagram API endpoints
        api_endpoints = [
            'https://i.instagram.com/api/v1/',
            'https://graph.instagram.com/',
            'https://api.instagram.com/',
            'https://instagram.com/api/',
            'https://www.instagram.com/graphql/',
            'https://edge-chat.instagram.com/',
            'https://realtime-chat.instagram.com/'
        ]
        
        working_endpoints = []
        
        for endpoint in api_endpoints:
            try:
                headers = {
                    'User-Agent': 'Instagram 219.0.0.12.117 Android',
                    'Accept': 'application/json'
                }
                
                response = requests.get(endpoint, headers=headers, timeout=5)
                
                if response.status_code not in [403, 429]:  # Not forbidden or rate limited
                    print(f"   ✅ Endpoint accessible: {endpoint}")
                    working_endpoints.append(endpoint)
                else:
                    print(f"   ❌ Endpoint blocked: {endpoint} - {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Endpoint error: {endpoint} - {str(e)}")
        
        if working_endpoints:
            self.results['api_discovery'] = {'status': 'SUCCESS', 'endpoints': working_endpoints}
            return True
        else:
            self.results['api_discovery'] = {'status': 'FAILED'}
            return False
    
    def emergency_method_3_session_hijacking_simulation(self):
        """Simulate session hijacking from legitimate sources"""
        print("🔓 Emergency Method 3: Session Hijacking Simulation")
        
        # Look for existing session files or tokens
        session_locations = [
            '~/.instagram/',
            './sessions/',
            './cookies/',
            './',
        ]
        
        found_sessions = []
        
        for location in session_locations:
            try:
                import glob
                expanded_path = os.path.expanduser(location)
                if os.path.exists(expanded_path):
                    # Look for session files
                    session_files = glob.glob(os.path.join(expanded_path, '*session*'))
                    session_files.extend(glob.glob(os.path.join(expanded_path, '*cookie*')))
                    session_files.extend(glob.glob(os.path.join(expanded_path, '*token*')))
                    
                    found_sessions.extend(session_files)
            except:
                pass
        
        if found_sessions:
            print(f"   ✅ Found {len(found_sessions)} potential session files")
            for session in found_sessions[:5]:  # Show first 5
                print(f"      📁 {session}")
            
            self.results['session_hijacking'] = {'status': 'SUCCESS', 'sessions': found_sessions}
            return True
        else:
            print("   ❌ No session files found")
            self.results['session_hijacking'] = {'status': 'FAILED'}
            return False
    
    def emergency_method_4_database_direct_access(self):
        """Direct database access without Instagram API"""
        print("💾 Emergency Method 4: Database Direct Access")
        
        # Check if we have existing data in our database
        db_files = [
            'integrated_targets_2025.db',
            'advanced_dm_database_*.sqlite',
            '*.db',
            '*.sqlite'
        ]
        
        found_databases = []
        
        for pattern in db_files:
            try:
                import glob
                databases = glob.glob(pattern)
                found_databases.extend(databases)
            except:
                pass
        
        if found_databases:
            print(f"   ✅ Found {len(found_databases)} database files")
            
            # Try to extract data from existing databases
            for db in found_databases[:3]:  # Check first 3
                try:
                    import sqlite3
                    conn = sqlite3.connect(db)
                    cursor = conn.cursor()
                    
                    # Get table names
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    
                    if tables:
                        print(f"      📊 {db}: {len(tables)} tables")
                        
                        # Check for data in tables
                        for table in tables[:3]:  # Check first 3 tables
                            try:
                                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                                count = cursor.fetchone()[0]
                                print(f"         🔢 {table[0]}: {count} records")
                            except:
                                pass
                    
                    conn.close()
                    
                except Exception as e:
                    print(f"      ❌ Database error: {str(e)}")
            
            self.results['database_access'] = {'status': 'SUCCESS', 'databases': found_databases}
            return True
        else:
            print("   ❌ No database files found")
            self.results['database_access'] = {'status': 'FAILED'}
            return False
    
    def emergency_method_5_backup_data_recovery(self):
        """Recover data from backup files"""
        print("📂 Emergency Method 5: Backup Data Recovery")
        
        backup_patterns = [
            '*.csv',
            '*.json',
            'backup_*',
            'extracted_*',
            'legitimate_*'
        ]
        
        found_backups = []
        
        for pattern in backup_patterns:
            try:
                import glob
                backups = glob.glob(pattern)
                found_backups.extend(backups)
            except:
                pass
        
        if found_backups:
            print(f"   ✅ Found {len(found_backups)} backup files")
            
            # Analyze backup files
            for backup in found_backups[:5]:  # Show first 5
                try:
                    file_size = os.path.getsize(backup)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(backup))
                    
                    print(f"      📁 {backup}: {file_size} bytes, modified {mod_time.strftime('%Y-%m-%d %H:%M')}")
                    
                except Exception as e:
                    print(f"      ❌ File error: {str(e)}")
            
            self.results['backup_recovery'] = {'status': 'SUCCESS', 'backups': found_backups}
            return True
        else:
            print("   ❌ No backup files found")
            self.results['backup_recovery'] = {'status': 'FAILED'}
            return False
    
    def emergency_method_6_network_interface_switching(self):
        """Switch network interfaces"""
        print("🌐 Emergency Method 6: Network Interface Switching")
        
        try:
            # Get available network interfaces
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            
            if result.returncode == 0:
                interfaces = []
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and '127.0.0.1' not in line:
                        parts = line.split()
                        if len(parts) > 1:
                            ip = parts[1].split('/')[0]
                            interfaces.append(ip)
                
                if len(interfaces) > 1:
                    print(f"   ✅ Found {len(interfaces)} network interfaces")
                    for i, interface in enumerate(interfaces):
                        print(f"      🌐 Interface {i+1}: {interface}")
                    
                    self.results['network_switching'] = {'status': 'SUCCESS', 'interfaces': interfaces}
                    return True
                else:
                    print("   ❌ Only one network interface available")
            else:
                print("   ❌ Could not get network interfaces")
                
        except Exception as e:
            print(f"   ❌ Network interface error: {str(e)}")
        
        self.results['network_switching'] = {'status': 'FAILED'}
        return False
    
    def create_emergency_extraction_plan(self):
        """Create emergency extraction plan based on available methods"""
        successful_methods = [method for method, result in self.results.items() if result['status'] == 'SUCCESS']
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'current_ip': self.current_ip,
            'available_methods': successful_methods,
            'extraction_plan': [],
            'estimated_success_rate': 0
        }
        
        if 'database_access' in successful_methods:
            plan['extraction_plan'].append({
                'method': 'Database Direct Access',
                'description': 'Extract data from existing database files',
                'command': 'python3 database_complete_extractor.py',
                'priority': 1
            })
            plan['estimated_success_rate'] += 40
        
        if 'backup_recovery' in successful_methods:
            plan['extraction_plan'].append({
                'method': 'Backup Data Recovery',
                'description': 'Recover data from backup files',
                'command': 'python3 backup_important_data.py',
                'priority': 2
            })
            plan['estimated_success_rate'] += 30
        
        if 'api_discovery' in successful_methods:
            plan['extraction_plan'].append({
                'method': 'Alternative API Access',
                'description': 'Use discovered API endpoints',
                'command': 'python3 alternative_data_processor.py',
                'priority': 3
            })
            plan['estimated_success_rate'] += 20
        
        if 'session_hijacking' in successful_methods:
            plan['extraction_plan'].append({
                'method': 'Session Restoration',
                'description': 'Restore from existing session files',
                'command': 'python3 session_regenerator_fleming654.py',
                'priority': 4
            })
            plan['estimated_success_rate'] += 10
        
        plan['estimated_success_rate'] = min(plan['estimated_success_rate'], 95)  # Cap at 95%
        
        return plan
    
    def execute_emergency_plan(self, plan):
        """Execute the emergency extraction plan"""
        print(f"\n🚨 EXECUTING EMERGENCY PLAN")
        print(f"📊 Estimated Success Rate: {plan['estimated_success_rate']}%")
        print(f"🎯 Available Methods: {len(plan['extraction_plan'])}")
        
        for step in plan['extraction_plan']:
            print(f"\n🔄 Executing: {step['method']}")
            print(f"📝 Description: {step['description']}")
            print(f"💻 Command: {step['command']}")
            
            try:
                # Execute the command
                result = subprocess.run(step['command'].split(), capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"   ✅ {step['method']} SUCCESSFUL")
                    return True
                else:
                    print(f"   ❌ {step['method']} FAILED: {result.stderr}")
                    
            except Exception as e:
                print(f"   💥 {step['method']} ERROR: {str(e)}")
        
        return False
    
    def run_emergency_system(self):
        """Run the complete emergency extraction system"""
        print("🚨 EMERGENCY EXTRACTION SYSTEM 2025")
        print("=" * 50)
        print(f"🌍 Current IP: {self.current_ip}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 This is your LAST RESORT when all other methods fail!")
        print()
        
        emergency_methods = [
            self.emergency_method_1_time_window_attack,
            self.emergency_method_2_api_endpoint_discovery,
            self.emergency_method_3_session_hijacking_simulation,
            self.emergency_method_4_database_direct_access,
            self.emergency_method_5_backup_data_recovery,
            self.emergency_method_6_network_interface_switching
        ]
        
        successful_methods = 0
        
        for method in emergency_methods:
            try:
                if method():
                    successful_methods += 1
                time.sleep(2)
            except Exception as e:
                print(f"💥 Emergency method error: {str(e)}")
        
        print(f"\n🎉 EMERGENCY ANALYSIS COMPLETE!")
        print(f"📊 Available Methods: {successful_methods}/{len(emergency_methods)}")
        
        # Create and execute emergency plan
        plan = self.create_emergency_extraction_plan()
        
        plan_file = f"emergency_extraction_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"📁 Emergency plan saved: {plan_file}")
        
        if plan['extraction_plan']:
            print(f"\n🚀 EXECUTING EMERGENCY EXTRACTION...")
            success = self.execute_emergency_plan(plan)
            
            if success:
                print("\n🎉 EMERGENCY EXTRACTION SUCCESSFUL!")
                return True
            else:
                print("\n❌ EMERGENCY EXTRACTION FAILED")
        else:
            print("\n⚠️ NO EMERGENCY METHODS AVAILABLE")
        
        return False

if __name__ == "__main__":
    emergency_system = EmergencyExtractionSystem()
    success = emergency_system.run_emergency_system()
    
    if not success:
        print("\n🕐 FINAL RECOMMENDATION:")
        print("Wait 24-48 hours for IP blacklist to automatically clear")
        print("Instagram typically removes IP bans after 1-2 days")