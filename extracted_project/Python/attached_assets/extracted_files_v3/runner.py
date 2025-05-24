import os
import json
from modules.analyzer import analyze_interactions
from webhook.discord_notify import send_discord_alert

LOG_DIR = "logs"
SESSION_FILE = "session.json"

def extract_session_from_log(log_path):
    with open(log_path) as f:
        for line in f:
            if "password" in line:
                parts = line.strip().split("password:")
                if len(parts) == 2:
                    return {"sessionid": "MOCKED_SESSIONID_FOR_" + parts[0].split(":")[1].strip()}
    return None

def save_session(session_data):
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f)
    print("[✓] Session saved to session.json")

def main():
    for user in ["alx.trading", "whatilove1728"]:
        log_path = os.path.join(LOG_DIR, f"{user}_session_success.txt")
        if os.path.exists(log_path):
            session = extract_session_from_log(log_path)
            if session:
                print(f"[✓] Found session for {user}")
                save_session(session)
                send_discord_alert(f"[✓] Session extracted for {user}")
                analyze_interactions(user, session)
            else:
                print(f"[!] No session found in {log_path}")

if __name__ == "__main__":
    main()
