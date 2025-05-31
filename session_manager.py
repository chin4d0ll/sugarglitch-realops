import json
import os
from instagrapi import Client

SESSION_DIR = "sessions"

def save_session(username: str, client: Client):
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)
    session_data = client.get_settings()
    with open(f"{SESSION_DIR}/{username}.json", "w") as f:
        json.dump(session_data, f, indent=2)

def load_session(username: str) -> Client:
    session_path = f"{SESSION_DIR}/{username}.json"
    cl = Client()
    if os.path.exists(session_path):
        with open(session_path, "r") as f:
            settings = json.load(f)
        cl.set_settings(settings)
    return cl
