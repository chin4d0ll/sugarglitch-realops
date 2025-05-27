import requests
import json
import os

def send_discord_alert(message):
    # อ่าน webhook URL จาก config file
    config_file = "webhook/config.json"

    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
                webhook_url = config.get("discord_webhook_url")

                # ตรวจสอบว่าควรส่งการแจ้งเตือนหรือไม่
                if "error" in message.lower() and not config.get("notify_on_error", True):
                    return

                if "success" in message.lower() and not config.get("notify_on_success", True):
                    return
        else:
            # ถ้าไม่มีไฟล์ config ใช้ webhook URL ที่กำหนดไว้
            webhook_url = "https://discord.com/api/webhooks/1374978837879853151/QXLbx5hw-j17RBMFETqh49BgvctrTdHRi3FllZVFGG6FiEoV2KkWh31UASNh1YfuLuEh"

        # เพิ่ม emoji น่ารักๆ
        if "error" in message.lower() or "failed" in message.lower():
            emoji = "⚠️"
        elif "success" in message.lower():
            emoji = "✅"
        else:
            emoji = "🌸"

        # ส่ง webhook
        data = {"content": f"{emoji} {message}"}
        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            print("[✓] ส่งการแจ้งเตือนไปยัง Discord สำเร็จ")
        else:
            print(f"[!] ส่งการแจ้งเตือนไปยัง Discord ล้มเหลว: {response.status_code}")
    except Exception as e:
        print(f"[!] เกิดข้อผิดพลาดในการส่งการแจ้งเตือนไปยัง Discord: {str(e)}")