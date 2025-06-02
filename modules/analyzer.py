import json

def analyze_interactions(username, session):
    print(f"[~] Analyzing DMs and followers for {username}...")
    # MOCKED analysis
    suspect = {
        "username": "queen.mochi",
        "score": 92,
        "evidence": ["'คิดถึงนะ'", "emoji heart", "ส่งรูป 3 ครั้ง"]
    }
    html_path = f"export/suspect_report_{username}.html"
    with open(html_path, "w") as f:
        f.write(f"<h1>Suspicious Contact for {username}</h1>")
        f.write(f"<p><b>{suspect['username']}</b> - Score: {suspect['score']}</p>")
        f.write("<ul>")
        for item in suspect["evidence"]:
            f.write(f"<li>{item}</li>")
        f.write("</ul>")
    print(f"[✓] Exported report to {html_path}")
