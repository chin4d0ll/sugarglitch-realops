import json
from modules import fetch_dm
from webhook.discord_notify import send_discord_alert

with open("session.json") as f:
    session = json.load(f)

# Placeholder runner logic
print("[✓] Running Sugarglitch Auto Mode")
dms = fetch_dm.fetch_dms(session_file="session.json")

# Save output
with open("export/report.html", "w") as report:
    report.write("<h1>Sugarglitch Report</h1>")
    for dm in dms:
        report.write(f"<p>{dm['user']}: {dm['last_message']}</p>")
