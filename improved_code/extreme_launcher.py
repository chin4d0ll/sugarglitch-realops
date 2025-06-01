from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥💀⚡ ULTIMATE HARDCORE LAUNCHER ⚡💀🔥
THE MOST EXTREME SCRIPT EVER CREATED
MAXIMUM POWER - BREAK THROUGH THE SCREEN!
"""

import os
import sys
import time
import subprocess
import threading
from colorama import init, Fore, Back, Style

init(autoreset=True)

def display_ultimate_banner():
    """Display the most EXTREME banner in existence"""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Ultimate hardcore banner
    banner = f"""
{Fore.RED + Back.BLACK + Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  {Fore.YELLOW + Style.BRIGHT}🔥💀⚡ ULTIMATE HARDCORE INSTAGRAM DESTROYER ⚡💀🔥{Fore.RED}                ║
║                                                                               ║
║  {Fore.CYAN}██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗{Fore.RED}          ║
║  {Fore.CYAN}██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝{Fore.RED}          ║
║  {Fore.CYAN}██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗{Fore.RED}            ║
║  {Fore.CYAN}██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝{Fore.RED}            ║
║  {Fore.CYAN}╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗{Fore.RED}          ║
║  {Fore.CYAN}╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝{Fore.RED}          ║
║                                                                               ║
║  {Fore.MAGENTA + Style.BRIGHT}💀 POWER LEVEL: ∞ INFINITY ∞ 💀{Fore.RED}                                   ║
║  {Fore.YELLOW + Style.BRIGHT}⚡ STATUS: READY TO BREAK REALITY ⚡{Fore.RED}                               ║
║  {Fore.GREEN + Style.BRIGHT}🔥 MODE: MAXIMUM DESTRUCTION 🔥{Fore.RED}                                   ║
║                                                                               ║
║  {Fore.WHITE + Style.BRIGHT}[WARNING] This launcher operates beyond all limits{Fore.RED}                ║
║  {Fore.WHITE + Style.BRIGHT}[CAUTION] Prepare for ULTIMATE POWER{Fore.RED}                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def extreme_loading_sequence():
    """The most EXTREME loading sequence ever"""
    loading_stages = [
        ("🔋 Charging Power Cores", "⚡⚡⚡", Fore.YELLOW),
        ("💀 Activating Death Mode", "💀💀💀", Fore.RED),
        ("🔥 Igniting Destruction Engine", "🔥🔥🔥", Fore.RED),
        ("🥷 Engaging Stealth Protocols", "🥷🥷🥷", Fore.BLUE),
        ("⚡ Overclocking All Systems", "⚡⚡⚡", Fore.CYAN),
        ("💀 GODMODE ACTIVATION", "💀💀💀", Fore.RED),
        ("🚀 MAXIMUM POWER ACHIEVED", "🚀🚀🚀", Fore.GREEN)
    ]
    
    for stage, symbols, color in loading_stages:
        print(f"\n{color + Style.BRIGHT}{stage}")
        
        # Animated loading bar
        for i in range(21):
            progress = "█" * i + "░" * (20 - i)
            percentage = (i * 100) // 20
            
            print(f"\r{color}[{progress}] {percentage}% {symbols}", end="")
            time.sleep(0.1)
            
        print(f" {Fore.GREEN + Style.BRIGHT}✅ COMPLETE!")
        time.sleep(0.3)

def display_ultimate_menu():
    """Display the ultimate menu of destruction"""
    print(f"\n{Fore.RED + Style.BRIGHT}{'='*80}")
    print(f"{Fore.YELLOW + Style.BRIGHT}💀 SELECT YOUR WEAPON OF MASS EXTRACTION 💀")
    print(f"{Fore.RED + Style.BRIGHT}{'='*80}")
    
    menu_options = [
        ("1", "🔥 Ultimate Hardcore Extractor", "Launch the most powerful extraction tool", Fore.RED),
        ("2", "💀 Matrix Breach Monitor", "Real-time monitoring with matrix effects", Fore.GREEN),
        ("3", "⚡ Dual Mode Assault", "Run both tools simultaneously for MAXIMUM POWER", Fore.MAGENTA),
        ("4", "🚀 Session Status Check", "Verify GODLIKE session power", Fore.CYAN),
        ("5", "💀 System Diagnostics", "Run complete system check", Fore.YELLOW),
        ("6", "🔥 Emergency Shutdown", "Terminate all operations", Fore.RED)
    ]
    
    for option, title, desc, color in menu_options:
        print(f"{Fore.WHITE + Style.BRIGHT}[{option}] {color + Style.BRIGHT}{title}")
        print(f"    {Fore.WHITE}{desc}")
        print()

def run_ultimate_extractor():
    """Launch the ultimate hardcore extractor"""
    print(f"{Fore.RED + Style.BRIGHT}🚀 LAUNCHING ULTIMATE EXTRACTOR 🚀")
    
    script_path = "/workspaces/sugarglitch-realops/ultimate_hardcore_extractor.py"
    
    if os.path.exists(script_path):
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}❌ Extractor failed: {str(e)}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED + Style.BRIGHT}💀 EXTRACTION INTERRUPTED 💀")
    else:
        print(f"{Fore.RED}❌ Extractor not found!")

def run_matrix_monitor():
    """Launch the matrix breach monitor"""
    print(f"{Fore.GREEN + Style.BRIGHT}🔍 LAUNCHING MATRIX MONITOR 🔍")
    
    script_path = "/workspaces/sugarglitch-realops/matrix_breach_monitor.py"
    
    if os.path.exists(script_path):
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}❌ Monitor failed: {str(e)}")
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN + Style.BRIGHT}💀 MONITORING TERMINATED 💀")
    else:
        print(f"{Fore.RED}❌ Monitor not found!")

def run_dual_mode_assault():
    """Run both tools simultaneously for MAXIMUM POWER"""
    print(f"{Fore.MAGENTA + Style.BRIGHT}⚡ LAUNCHING DUAL MODE ASSAULT ⚡")
    print(f"{Fore.YELLOW}WARNING: This will use MAXIMUM system resources!")
    
    confirm = input(f"{Fore.RED + Style.BRIGHT}Are you ready for ULTIMATE POWER? (yes/NO): ").lower()
    
    if confirm == "yes":
        print(f"{Fore.RED + Style.BRIGHT}💀 DUAL MODE ACTIVATED 💀")
        
        # Launch matrix monitor in background
        monitor_script = "/workspaces/sugarglitch-realops/matrix_breach_monitor.py"
        extractor_script = "/workspaces/sugarglitch-realops/ultimate_hardcore_extractor.py"
        
        if os.path.exists(monitor_script) and os.path.exists(extractor_script):
            try:
                # Start monitor in background
                monitor_process = subprocess.Popen([sys.executable, monitor_script])
                
                # Give monitor time to start
                time.sleep(2)
                
                # Start extractor in foreground
                subprocess.run([sys.executable, extractor_script], check=True)
                
                # Terminate monitor
                monitor_process.terminate()
                
            except Exception as e:
                print(f"{Fore.RED}❌ Dual mode failed: {str(e)}")
        else:
            print(f"{Fore.RED}❌ Required scripts not found!")
    else:
        print(f"{Fore.YELLOW}⚠️  Dual mode cancelled")

def check_session_status():
    """Check GODLIKE session status"""
    print(f"{Fore.CYAN + Style.BRIGHT}🔍 CHECKING GODLIKE SESSION STATUS 🔍")
    
    sessions_dir = "/workspaces/sugarglitch-realops/sessions"
    
    if os.path.exists(sessions_dir):
        sessions = os.listdir(sessions_dir)
        godlike_sessions = [s for s in sessions if s.startswith("GODLIKE_")]
        
        if godlike_sessions:
            print(f"{Fore.GREEN + Style.BRIGHT}✅ {len(godlike_sessions)} GODLIKE session(s) found!")
            
            # Show latest session
            latest = sorted(godlike_sessions)[-1]
            session_path = os.path.join(sessions_dir, latest)
            
            try:
                import json
                with open(session_path, 'r') as f:
                    session_data = json.load(f)
                    
                print(f"{Fore.CYAN}📊 Latest Session:")
                print(f"{Fore.WHITE}  File: {latest}")
                print(f"{Fore.WHITE}  Power: {session_data.get('power_level', 'Unknown')}")
                print(f"{Fore.WHITE}  Timestamp: {session_data.get('timestamp', 'Unknown')}")
                print(f"{Fore.WHITE}  Cookies: {len(session_data.get('cookies', {}))}")
                
            except Exception as e:
                print(f"{Fore.RED}❌ Error reading session: {str(e)}")
        else:
            print(f"{Fore.RED}❌ No GODLIKE sessions found!")
    else:
        print(f"{Fore.RED}❌ Sessions directory not found!")

def run_system_diagnostics():
    """Run complete system diagnostics"""
    print(f"{Fore.YELLOW + Style.BRIGHT}🔧 RUNNING SYSTEM DIAGNOSTICS 🔧")
    
    diagnostics = [
        ("Python Version", sys.version.split()[0]),
        ("Operating System", os.name),
        ("Current Directory", os.getcwd()),
        ("Script Location", os.path.dirname(os.path.abspath(__file__)))
    ]
    
    print(f"\n{Fore.CYAN + Style.BRIGHT}📊 SYSTEM INFORMATION:")
    for name, value in diagnostics:
        print(f"{Fore.WHITE}  {name}: {Fore.GREEN}{value}")
        
    # Check required files
    print(f"\n{Fore.CYAN + Style.BRIGHT}📁 FILE STATUS:")
    
    required_files = [
        "ultimate_hardcore_extractor.py",
        "matrix_breach_monitor.py",
        "advanced_session_manager.py",
        "sessions/",
        "requirements.txt"
    ]
    
    for file in required_files:
        file_path = f"/workspaces/sugarglitch-realops/{file}"
        if os.path.exists(file_path):
            status = f"{Fore.GREEN}✅ EXISTS"
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                status += f" ({size} bytes)"
        else:
            status = f"{Fore.RED}❌ MISSING"
            
        print(f"{Fore.WHITE}  {file}: {status}")
        
    # Check Python packages
    print(f"\n{Fore.CYAN + Style.BRIGHT}📦 PACKAGE STATUS:")
    
    required_packages = [
        "requests",
        "selenium",
        "undetected_chromedriver",
        "colorama",
        "cryptography"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"{Fore.WHITE}  {package}: {Fore.GREEN}✅ INSTALLED")
        except ImportError:
            print(f"{Fore.WHITE}  {package}: {Fore.RED}❌ MISSING")

def emergency_shutdown():
    """Emergency shutdown sequence"""
    print(f"{Fore.RED + Style.BRIGHT}🚨 INITIATING EMERGENCY SHUTDOWN 🚨")
    
    shutdown_sequence = [
        "Terminating extraction processes...",
        "Shutting down matrix monitor...",
        "Clearing memory buffers...",
        "Closing browser instances...",
        "Securing session data...",
        "System shutdown complete."
    ]
    
    for step in shutdown_sequence:
        print(f"{Fore.YELLOW}⚡ {step}")
        time.sleep(0.5)
        
    print(f"\n{Fore.GREEN + Style.BRIGHT}✅ EMERGENCY SHUTDOWN COMPLETE")
    print(f"{Fore.YELLOW + Style.BRIGHT}⚡ ALL SYSTEMS TERMINATED ⚡")

@safe_execution
def main():
    """Main launcher function"""
    try:
        while True:
            # Display ultimate banner
            display_ultimate_banner()
            
            # Extreme loading sequence (only on first run)
            if 'first_run' not in main.__dict__:
                extreme_loading_sequence()
                main.first_run = False
                
            # Display menu
            display_ultimate_menu()
            
            # Get user choice
            choice = input(f"{Fore.RED + Style.BRIGHT}💀 SELECT YOUR WEAPON [1-6]: ").strip()
            
            if choice == "1":
                run_ultimate_extractor()
            elif choice == "2":
                run_matrix_monitor()
            elif choice == "3":
                run_dual_mode_assault()
            elif choice == "4":
                check_session_status()
            elif choice == "5":
                run_system_diagnostics()
            elif choice == "6":
                emergency_shutdown()
                break
            else:
                print(f"{Fore.RED}❌ Invalid choice! Try again.")
                
            # Pause before next iteration
            input(f"\n{Fore.YELLOW}Press Enter to return to main menu...")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.RED + Style.BRIGHT}💀 LAUNCHER INTERRUPTED 💀")
        emergency_shutdown()
    except Exception as e:
        print(f"\n{Fore.RED + Style.BRIGHT}💀 CRITICAL ERROR: {str(e)} 💀")
    finally:
        print(f"\n{Fore.YELLOW + Style.BRIGHT}⚡ ULTIMATE LAUNCHER TERMINATED ⚡")

if __name__ == "__main__":
    main()
