import requests

WEBHOOK_URL = "https://discord.com/api/v10/webhooks/1374978837879853151/QXLbx5hw-j17RBMFETqh49BgvctrTdHRi3FllZVFGG6FiEoV2KkWh31UASNh1YfuLuEh"

def send_discord_alert(message):
    data = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"[!] Failed to send Discord alert: {str(e)}")
