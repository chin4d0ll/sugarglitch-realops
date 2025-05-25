
import json
import os
from pathlib import Path

# 1. ตรวจสอบว่ามี session.json หรือไม่ ถ้าไม่มีจะสร้างให้
if not os.path.exists("session.json"):
    print("[!] ไม่พบ session.json ในโฟลเดอร์หลัก กำลังสร้าง...")
    
    # 2. ลองหา session.json จากที่อื่นๆก่อน
    possible_paths = [
        "extracted_files/session.json",
        "attached_assets/extracted_files/session.json",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"[~] พบไฟล์ {path} กำลังคัดลอก...")
            with open(path) as f:
                session_data = json.load(f)
                with open("session.json", "w") as out_f:
                    json.dump(session_data, out_f)
                print("[✓] คัดลอก session.json เรียบร้อย!")
                break
    else:
        # 3. ถ้าไม่เจอเลย ลองใช้ runner.py สกัด session จาก logs
        print("[~] ไม่พบไฟล์ session.json ที่มีอยู่แล้ว ลองสกัดจาก logs...")
        try:
            # ลองใช้ runner.py จาก v3
            if os.path.exists("attached_assets/extracted_files_v3/runner.py"):
                print("[~] กำลังรัน runner.py เพื่อสกัด session...")
                os.makedirs("logs", exist_ok=True)
                # คัดลอก logs ถ้ามี
                if os.path.exists("attached_assets/extracted_files_v3/logs"):
                    import shutil
                    for log_file in os.listdir("attached_assets/extracted_files_v3/logs"):
                        src = f"attached_assets/extracted_files_v3/logs/{log_file}"
                        dst = f"logs/{log_file}"
                        if not os.path.exists(dst):
                            shutil.copy(src, dst)
                
                # นำเข้าฟังก์ชันจาก runner.py
                import sys
                sys.path.append("attached_assets/extracted_files_v3")
                from runner import extract_session_from_log, save_session
                
                # ลองสกัด session จาก logs
                found = False
                for user in ["alx.trading", "whatilove1728"]:
                    log_path = os.path.join("logs", f"{user}_session_success.txt")
                    if os.path.exists(log_path):
                        session = extract_session_from_log(log_path)
                        if session:
                            print(f"[✓] พบ session สำหรับ {user}")
                            save_session(session)
                            found = True
                            break
                
                if not found:
                    # สร้าง session เริ่มต้น
                    with open("session.json", "w") as f:
                        json.dump({"sessionid": "your_session_id_here"}, f)
                    print("[!] สร้าง session เริ่มต้น กรุณาแก้ไขค่า sessionid")
        except Exception as e:
            print(f"[!] เกิดข้อผิดพลาด: {e}")
            # สร้าง session เริ่มต้น
            with open("session.json", "w") as f:
                json.dump({"sessionid": "your_session_id_here"}, f)
            print("[!] สร้าง session เริ่มต้น กรุณาแก้ไขค่า sessionid")

# 4. ตรวจสอบโฟลเดอร์ export
if not os.path.exists("export"):
    os.makedirs("export")
    print("[✓] สร้างโฟลเดอร์ export สำเร็จ")

# 5. ตอนนี้ session.json ต้องมีแล้ว รัน main logic
try:
    # ลองโหลดโมดูลที่ดึงข้อมูลจริง
    try:
        from modules.browser_api_manager import fetch_real_dms_browser_api
        print("[✓] โหลดโมดูล Browser API สำเร็จ")
        use_browser_api = True
    except ImportError:
        use_browser_api = False
        print("[!] ไม่พบโมดูล Browser API ลองใช้ proxy แทน")
        
        try:
            from modules.real_data_fetch import fetch_real_dms, analyze_suspicious_messages
            print("[✓] โหลดโมดูลดึงข้อมูลจริงสำเร็จ")
            use_real_data = True
        except ImportError:
            use_real_data = False
            print("[!] ไม่พบโมดูลดึงข้อมูลจริง ลองใช้ mock data แทน")
        
        # ตรวจสอบว่ามีโมดูล fetch_dm หรือไม่
        module_paths = [
            "modules.fetch_dm",  # โมดูลจากโฟลเดอร์หลัก
            "extracted_files.modules.fetch_dm",  # โมดูลจาก extracted_files
        ]
        
        fetch_dm = None
        for module_path in module_paths:
            try:
                fetch_dm_module = __import__(module_path, fromlist=["fetch_dms"])
                fetch_dm = fetch_dm_module.fetch_dms
                print(f"[✓] โหลดโมดูล {module_path} สำเร็จ")
                break
            except (ImportError, AttributeError):
                continue
        
        if not fetch_dm:
            # สร้างฟังก์ชัน fetch_dms เอง
            print("[!] ไม่พบโมดูล fetch_dm กำลังสร้างฟังก์ชันจำลอง...")
            def fetch_dms(session_file):
                return [{"user": "ex_boy", "last_message": "miss u"}]
    
    # ตรวจสอบว่ามีโมดูล discord_notify หรือไม่
    try:
        from webhook.discord_notify import send_discord_alert
    except ImportError:
        # สร้างฟังก์ชัน send_discord_alert เอง
        def send_discord_alert(message):
            print(f"[DISCORD] {message}")
    
    # โหลด session
    with open("session.json") as f:
        session = json.load(f)
    
    # รัน logic หลัก
    print("[✓] กำลังรัน Sugarglitch Auto Mode")
    
    if use_browser_api:
        # ใช้ Browser API (วิธีใหม่)
        print("[~] ใช้ BrightData Browser API")
        dms = fetch_real_dms_browser_api(session_file="session.json")
        if not dms:
            print("[!] ไม่สามารถดึงข้อมูลผ่าน Browser API ได้ ใช้ mock data แทน")
            dms = [{"user": "demo_user", "last_message": "ข้อความตัวอย่างจาก Browser API fallback"}]
        else:
            print(f"[✓] ดึงข้อมูลผ่าน Browser API สำเร็จ! จำนวน {len(dms)} รายการ")
            
    elif use_real_data:
        # ดึงข้อมูลผ่าน proxy (วิธีเก่า)
        print("[~] ใช้ Proxy API")
        dms = fetch_real_dms(session_file="session.json")
        if not dms:
            print("[!] ไม่สามารถดึงข้อมูลจริงได้ ใช้ mock data แทน")
            dms = fetch_dm(session_file="session.json") if 'fetch_dm' in locals() else [{"user": "mock_user", "last_message": "mock message"}]
        else:
            # วิเคราะห์ข้อความที่น่าสงสัย
            suspicious = analyze_suspicious_messages(dms)
            if suspicious:
                print(f"[!] พบข้อความที่น่าสงสัย {len(suspicious)} รายการ")
                
                # บันทึกรายงานข้อความที่น่าสงสัย
                with open("export/suspicious_report.html", "w") as report:
                    report.write("<h1>Sugarglitch Suspicious Report</h1>")
                    for sus in suspicious:
                        report.write(f"<div class='suspect'>")
                        report.write(f"<h2>{sus['username']} (คะแนนความน่าสงสัย: {sus['score']}%)</h2>")
                        report.write("<ul>")
                        for evidence in sus["evidence"]:
                            report.write(f"<li>{evidence}</li>")
                        report.write("</ul>")
                        report.write("</div>")
                
                # ส่ง Discord webhook แจ้งเตือน
                send_discord_alert(f"⚠️ พบข้อความที่น่าสงสัย {len(suspicious)} รายการ")
    else:
        # ใช้ mock data
        print("[~] ใช้ Mock Data")
        dms = fetch_dm(session_file="session.json") if 'fetch_dm' in locals() else [{"user": "demo_user", "last_message": "ข้อความตัวอย่าง"}]
    
    # บันทึกผลลัพธ์รายงานหลัก
    with open("export/report.html", "w") as report:
        report.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sugarglitch Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Sugarglitch Report</h1>
""")
        for dm in dms:
            report.write(f"<p>{dm['user']}: {dm['last_message']}</p>")
        
        report.write("""
    <footer>Generated by Sugarglitch Toolkit: Replit Edition</footer>
</body>
</html>""")
    
    print("[✓] สร้างรายงานใน export/report.html สำเร็จ!")
    
except Exception as e:
    print(f"[!] เกิดข้อผิดพลาดในการรัน: {e}")
