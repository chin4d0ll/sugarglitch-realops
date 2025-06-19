#!/usr/bin/env python3
"""
🚀 REAL-TIME INTELLIGENCE DASHBOARD 🚀
Advanced monitoring for social media attacks and OSINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Features:
- Live attack monitoring
- Social media data visualization
- Success rate analytics
- Target intelligence mapping
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import time
import os
from datetime import datetime
import glob


class IntelligenceDashboard:
    def __init__(self):
        self.workspace = "/workspaces/sugarglitch-realops"
        self.running = True

    def clear_screen(self):
        os.system('clear')

    def load_osint_reports(self):
        """Load all OSINT intelligence reports"""
        reports = []
        pattern = f"{self.workspace}/deep_osint_report_*.json"

        for report_file in glob.glob(pattern):
            try:
                with open(report_file, 'r') as f:
                    report = json.load(f)
                    report['file'] = os.path.basename(report_file)
                    reports.append(report)
            except Exception:
                pass

        return sorted(reports, key=lambda x: x.get('generated_at', ''),
                      reverse=True)

    def load_attack_results(self):
        """Load attack result files"""
        results = []
        patterns = [
            f"{self.workspace}/attack_report_*.json",
            f"{self.workspace}/hardcore_results_*.txt",
            f"{self.workspace}/stealth_osint_report_*.json"
        ]

        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    stat = os.stat(file_path)
                    results.append({
                        'file': os.path.basename(file_path),
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'type': self.get_file_type(file_path)
                    })
                except Exception:
                    pass

        return sorted(results, key=lambda x: x['modified'], reverse=True)

    def get_file_type(self, file_path):
        """Determine file type from filename"""
        filename = os.path.basename(file_path)
        if 'attack_report' in filename:
            return 'Attack Report'
        elif 'hardcore_results' in filename:
            return 'Hardcore Attack'
        elif 'osint_report' in filename:
            return 'OSINT Intelligence'
        else:
            return 'Unknown'

    def analyze_password_effectiveness(self):
        """Analyze password lists and their effectiveness"""
        password_files = [
            'passwords.txt',
            'priority_passwords.txt',
            'emergency_passwords.txt',
            'deep_personal_passwords.txt',
            'stealth_passwords.txt'
        ]

        analysis = {}

        for pwd_file in password_files:
            file_path = f"{self.workspace}/{pwd_file}"
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()

                    passwords = [
                        line.strip() for line in lines if line.strip() and not line.startswith('#')]

                    analysis[pwd_file] = {
                        'count': len(passwords),
                        'size': os.path.getsize(file_path),
                        'modified': datetime.fromtimestamp(os.path.getmtime(file_path)),
                        'patterns': self.analyze_password_patterns(passwords[:50])
                    }
                except:
                    pass

        return analysis

    def analyze_password_patterns(self, passwords):
        """Analyze patterns in password list"""
        patterns = {
            'names': 0,
            'years': 0,
            'numbers': 0,
            'common': 0
        }

        for pwd in passwords:
            pwd_lower = pwd.lower()
            if any(name in pwd_lower for name in ['alex', 'alejandro', 'alx']):
                patterns['names'] += 1
            if any(year in pwd for year in ['1990', '1991', '1992', '1993', '1994', '1995', '2000', '2024', '2025']):
                patterns['years'] += 1
            if any(char.isdigit() for char in pwd):
                patterns['numbers'] += 1
            if pwd_lower in ['password', '123456', 'admin', 'trading']:
                patterns['common'] += 1

        return patterns

    def get_target_intelligence(self):
        """Get comprehensive target intelligence"""
        target_data = {
            'primary_target': 'alx.trading',
            'aliases': ['whatilove1728'],
            'platforms_found': [],
            'total_passwords': 0,
            'social_data_points': 0,
            'attack_vectors': []
        }

        # Load latest OSINT report
        reports = self.load_osint_reports()
        if reports:
            latest = reports[0]
            target_data['platforms_found'] = latest.get(
                'intelligence_summary', {}).get('platforms_discovered', [])
            target_data['total_passwords'] = latest.get(
                'intelligence_summary', {}).get('total_passwords', 0)
            target_data['social_data_points'] = latest.get(
                'intelligence_summary', {}).get('real_social_data_found', 0)

        # Analyze attack vectors
        if os.path.exists(f"{self.workspace}/scripts"):
            attack_scripts = glob.glob(f"{self.workspace}/scripts/*attack*.py")
            target_data['attack_vectors'] = [
                os.path.basename(script) for script in attack_scripts]

        return target_data

    def display_header(self):
        """Display dashboard header"""
        print("╔" + "═"*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "🚀 REAL-TIME INTELLIGENCE DASHBOARD 2025 🚀".center(78) + "║")
        print("║" + " "*78 + "║")
        print(
            "║" + f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        print()

    def display_target_intelligence(self, target_data):
        """Display target intelligence section"""
        print("🎯 TARGET INTELLIGENCE")
        print(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🔍 Primary Target: {target_data['primary_target']}")
        print(f"👥 Known Aliases: {', '.join(target_data['aliases'])}")
        print(
            f"🌐 Platforms Found: {', '.join(target_data['platforms_found']) if target_data['platforms_found'] else 'None detected'}")
        print(f"🔐 Password Database: {target_data['total_passwords']} entries")
        print(f"📊 Social Data Points: {target_data['social_data_points']}")
        print(f"⚡ Active Attack Vectors: {len(target_data['attack_vectors'])}")
        print()

    def display_password_analysis(self, pwd_analysis):
        """Display password analysis section"""
        print("🔐 PASSWORD ARSENAL ANALYSIS")
        print(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        total_passwords = sum(data['count'] for data in pwd_analysis.values())
        print(f"📋 Total Password Arsenal: {total_passwords} entries")
        print()

        for file_name, data in pwd_analysis.items():
            file_display = file_name.replace(
                '.txt', '').replace('_', ' ').title()
            age = datetime.now() - data['modified']
            age_str = f"{age.days}d {age.seconds//3600}h ago" if age.days > 0 else f"{age.seconds//3600}h {(age.seconds%3600)//60}m ago"

            print(f"   📁 {file_display}")
            print(
                f"      └─ {data['count']} passwords | {data['size']} bytes | Modified {age_str}")

            patterns = data['patterns']
            if patterns['names'] > 0:
                print(f"         🏷️  Name-based: {patterns['names']}")
            if patterns['years'] > 0:
                print(f"         📅 Year-based: {patterns['years']}")
            if patterns['numbers'] > 0:
                print(f"         🔢 Number patterns: {patterns['numbers']}")
            print()

    def display_recent_activity(self, attack_results):
        """Display recent attack activity"""
        print("⚡ RECENT ATTACK ACTIVITY")
        print(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        if not attack_results:
            print("   📭 No recent attack activity detected")
            print()
            return

        for result in attack_results[:5]:  # Show last 5 results
            age = datetime.now() - result['modified']
            age_str = f"{age.days}d {age.seconds//3600}h ago" if age.days > 0 else f"{age.seconds//3600}h {(age.seconds%3600)//60}m ago"

            print(f"   📊 {result['type']}: {result['file']}")
            print(f"      └─ {result['size']} bytes | {age_str}")

        print()

    def display_live_stats(self):
        """Display live system statistics"""
        print("📈 LIVE SYSTEM STATISTICS")
        print(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # Count script files
        scripts_path = f"{self.workspace}/scripts"
        script_count = len(
            glob.glob(f"{scripts_path}/*.py")) if os.path.exists(scripts_path) else 0

        # Count password files
        pwd_files = len(glob.glob(f"{self.workspace}/*password*.txt"))

        # Count reports
        report_files = len(glob.glob(f"{self.workspace}/*report*.json"))

        print(f"   🐍 Active Python Scripts: {script_count}")
        print(f"   🔐 Password Databases: {pwd_files}")
        print(f"   📊 Intelligence Reports: {report_files}")
        print(f"   💾 Workspace Size: {self.get_workspace_size()} MB")
        print()

    def get_workspace_size(self):
        """Calculate workspace size in MB"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(self.workspace):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        pass
        except:
            pass
        return round(total_size / (1024 * 1024), 2)

    def display_footer(self):
        """Display dashboard footer"""
        print(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(
            "🔥 Dashboard Status: ACTIVE | 📡 Real-time Monitoring: ON | 💀 Attack Ready: YES")
        print("⌨️  Press Ctrl+C to exit | 🔄 Auto-refresh: 30 seconds")
        print()

    def run_dashboard(self):
        """Run the main dashboard loop"""
        print("🚀 Starting Real-time Intelligence Dashboard...")
        time.sleep(2)

        while self.running:
            try:
                self.clear_screen()

                # Load all data
                target_data = self.get_target_intelligence()
                osint_reports = self.load_osint_reports()
                attack_results = self.load_attack_results()
                pwd_analysis = self.analyze_password_effectiveness()

                # Display dashboard
                self.display_header()
                self.display_target_intelligence(target_data)
                self.display_password_analysis(pwd_analysis)
                self.display_recent_activity(attack_results)
                self.display_live_stats()
                self.display_footer()

                # Wait for refresh
                time.sleep(30)

            except KeyboardInterrupt:
                print("\n⏹️  Dashboard shutdown requested...")
                self.running = False
                break
            except Exception as e:
                print(f"\n❌ Dashboard error: {e}")
                time.sleep(5)


def main():
    """Main execution function"""
    dashboard = IntelligenceDashboard()
    dashboard.run_dashboard()


if __name__ == "__main__":
    main()
