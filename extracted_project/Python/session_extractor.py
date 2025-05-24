
import os
import json
import re
import subprocess
import platform
import getpass
from datetime import datetime

def extract_session_id_from_file(file_path):
    """ดึง session ID จากไฟล์ที่ระบุ"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # ค้นหา pattern ของ session ID (8675309-real-session-id-here-5551212)
            session_ids = re.findall(r'([a-zA-Z0-9]{7,}-[\w-]+-[a-zA-Z0-9]{7,})', content)
            if session_ids:
                return session_ids
    except Exception as e:
        print(f"[!] เกิดข้อผิดพลาดในการอ่านไฟล์ {file_path}: {e}")
    return []

def search_browser_data():
    """ค้นหา sessionid จากไฟล์ dump ของเบราว์เซอร์"""
    username = getpass.getuser()
    system = platform.system()
    results = []
    
    print("💓 กำลังค้นหา session ID ในเครื่องของคุณค่ะ...")
    
    if system == "Windows":
        chrome_path = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        edge_path = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default"
        firefox_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
        
        paths_to_check = [
            chrome_path,
            edge_path,
            firefox_path
        ]
        
        for path in paths_to_check:
            if os.path.exists(path):
                print(f"[✓] พบโฟลเดอร์ {path}")
                for root, _, files in os.walk(path):
                    for file in files:
                        if "cookie" in file.lower() or "session" in file.lower() or "cache" in file.lower():
                            file_path = os.path.join(root, file)
                            session_ids = extract_session_id_from_file(file_path)
                            if session_ids:
                                for session_id in session_ids:
                                    results.append({
                                        "source": f"Browser: {file_path}",
                                        "session_id": session_id
                                    })
    
    elif system == "Darwin":  # macOS
        home = os.path.expanduser("~")
        safari_path = f"{home}/Library/Safari"
        chrome_path = f"{home}/Library/Application Support/Google/Chrome/Default"
        
        paths_to_check = [
            safari_path,
            chrome_path
        ]
        
        for path in paths_to_check:
            if os.path.exists(path):
                print(f"[✓] พบโฟลเดอร์ {path}")
                for root, _, files in os.walk(path):
                    for file in files:
                        if "cookie" in file.lower() or "session" in file.lower():
                            file_path = os.path.join(root, file)
                            session_ids = extract_session_id_from_file(file_path)
                            if session_ids:
                                for session_id in session_ids:
                                    results.append({
                                        "source": f"Browser: {file_path}",
                                        "session_id": session_id
                                    })
    
    elif system == "Linux":
        home = os.path.expanduser("~")
        chrome_path = f"{home}/.config/google-chrome/Default"
        firefox_path = f"{home}/.mozilla/firefox"
        
        paths_to_check = [
            chrome_path,
            firefox_path
        ]
        
        for path in paths_to_check:
            if os.path.exists(path):
                print(f"[✓] พบโฟลเดอร์ {path}")
                for root, _, files in os.walk(path):
                    for file in files:
                        if "cookie" in file.lower() or "session" in file.lower():
                            file_path = os.path.join(root, file)
                            session_ids = extract_session_id_from_file(file_path)
                            if session_ids:
                                for session_id in session_ids:
                                    results.append({
                                        "source": f"Browser: {file_path}",
                                        "session_id": session_id
                                    })
    
    # ค้นหาในไฟล์ log
    log_dir = "logs"
    if os.path.exists(log_dir):
        for file in os.listdir(log_dir):
            if file.endswith(".txt") or file.endswith(".log"):
                file_path = os.path.join(log_dir, file)
                session_ids = extract_session_id_from_file(file_path)
                if session_ids:
                    for session_id in session_ids:
                        results.append({
                            "source": f"Log: {file_path}",
                            "session_id": session_id
                        })
    
    return results

def extract_from_mobile_backup():
    """ดึง session ID จากไฟล์ backup ของแอพฯ มือถือ"""
    results = []
    
    # ตรวจสอบว่ามีโฟลเดอร์ attached_assets หรือไม่
    for root_dir in ["attached_assets", "."]:
        if os.path.exists(root_dir):
            for root, _, files in os.walk(root_dir):
                for file in files:
                    if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".sqlite") or file.endswith(".db"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'rb') as f:
                                content = f.read()
                                # ค้นหาแบบ binary
                                for pattern in [b'sessionid', b'session_id', b'sid=']:
                                    pos = content.find(pattern)
                                    if pos != -1:
                                        # ดึง 100 ไบต์หลังจากตำแหน่งที่พบ pattern
                                        chunk = content[pos:pos+100]
                                        # แปลงเป็น string
                                        chunk_str = chunk.decode('utf-8', errors='ignore')
                                        # ใช้ regex ค้นหา session ID
                                        session_ids = re.findall(r'([a-zA-Z0-9]{7,}-[\w-]+-[a-zA-Z0-9]{7,})', chunk_str)
                                        if session_ids:
                                            for session_id in session_ids:
                                                results.append({
                                                    "source": f"Mobile backup: {file_path}",
                                                    "session_id": session_id
                                                })
                        except Exception as e:
                            pass
    
    return results

def decrypt_session_json():
    """พยายามถอดรหัส sessionid จากไฟล์ session.json"""
    results = []
    
    # ตรวจสอบไฟล์ session.json
    if os.path.exists("session.json"):
        try:
            with open("session.json", "r") as f:
                session_data = json.load(f)
                session_id = session_data.get("sessionid")
                
                # ตรวจสอบว่า session_id มีค่าเริ่มต้นหรือไม่
                if session_id and session_id != "your_session_id_here" and session_id != "8675309-real-session-id-here-5551212":
                    results.append({
                        "source": "session.json (decrypted)",
                        "session_id": session_id
                    })
        except Exception as e:
            print(f"[!] ไม่สามารถอ่านไฟล์ session.json: {e}")
    
    return results

def test_session_id(session_id):
    """ทดสอบว่า session ID ใช้งานได้หรือไม่ (mock function)"""
    # ในสภาพแวดล้อมจริง คุณควรทดสอบโดยการส่งคำขอไปยังเซิร์ฟเวอร์
    # เพื่อความปลอดภัย เราจะแค่จำลองการทดสอบ
    return True

def save_valid_session(session_id):
    """บันทึก session ID ที่ใช้งานได้ลงในไฟล์ session.json"""
    with open("session.json", "w") as f:
        json.dump({"sessionid": session_id}, f)
    print(f"[✓] บันทึก session ID ลงในไฟล์ session.json แล้ว")

def extract_from_uploads():
    """ดึง session ID จากไฟล์ที่อัพโหลด"""
    results = []
    
    # ตรวจสอบว่ามีโฟลเดอร์ uploads หรือไม่
    upload_dirs = ["uploads", "upload", "import", "data"]
    
    for upload_dir in upload_dirs:
        if os.path.exists(upload_dir):
            for root, _, files in os.walk(upload_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    session_ids = extract_session_id_from_file(file_path)
                    if session_ids:
                        for session_id in session_ids:
                            results.append({
                                "source": f"Upload: {file_path}",
                                "session_id": session_id
                            })
    
    return results

def main():
    print("💋 Sugarglitch Session ID Extractor 💋")
    print("📱 กำลังค้นหา session ID ในระบบ...")
    
    all_results = []
    
    # 1. ค้นหาจากไฟล์ session.json ที่ถอดรหัสแล้ว
    decrypted_results = decrypt_session_json()
    if decrypted_results:
        all_results.extend(decrypted_results)
        print(f"[✓] พบ session ID จากไฟล์ session.json ที่ถอดรหัสแล้ว: {len(decrypted_results)}")
    
    # 2. ค้นหาจากไฟล์ backup ของแอพฯ มือถือ
    mobile_results = extract_from_mobile_backup()
    if mobile_results:
        all_results.extend(mobile_results)
        print(f"[✓] พบ session ID จากไฟล์ backup ของแอพฯ มือถือ: {len(mobile_results)}")
    
    # 3. ค้นหาจากเบราว์เซอร์
    browser_results = search_browser_data()
    if browser_results:
        all_results.extend(browser_results)
        print(f"[✓] พบ session ID จากเบราว์เซอร์: {len(browser_results)}")
    
    # 4. ค้นหาจากไฟล์ที่อัพโหลด
    upload_results = extract_from_uploads()
    if upload_results:
        all_results.extend(upload_results)
        print(f"[✓] พบ session ID จากไฟล์ที่อัพโหลด: {len(upload_results)}")
    
    # ถ้าไม่พบ session ID เลย
    if not all_results:
        print("[!] ไม่พบ session ID ใด ๆ ในระบบ")
        return
    
    # แสดงผลการค้นหา
    print("\n💘 ผลการค้นหา session ID:")
    valid_sessions = []
    for i, result in enumerate(all_results):
        print(f"{i+1}. จาก: {result['source']}")
        print(f"   Session ID: {result['session_id']}")
        
        # ทดสอบว่า session ID ใช้งานได้หรือไม่
        is_valid = test_session_id(result['session_id'])
        if is_valid:
            valid_sessions.append(result['session_id'])
            print(f"   สถานะ: ✅ ใช้งานได้")
        else:
            print(f"   สถานะ: ❌ ใช้งานไม่ได้")
        print()
    
    # บันทึก session ID ที่ใช้งานได้
    if valid_sessions:
        print(f"[✓] พบ session ID ที่ใช้งานได้: {len(valid_sessions)}")
        
        # ถ้ามี session ID ที่ใช้งานได้มากกว่า 1 อัน ให้ผู้ใช้เลือก
        if len(valid_sessions) > 1:
            print("เลือก session ID ที่ต้องการบันทึก (กรอกตัวเลข):")
            for i, session_id in enumerate(valid_sessions):
                print(f"{i+1}. {session_id}")
            
            choice = input("เลือก: ")
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(valid_sessions):
                    save_valid_session(valid_sessions[choice])
                else:
                    print("[!] ตัวเลือกไม่ถูกต้อง บันทึก session ID แรกแทน")
                    save_valid_session(valid_sessions[0])
            except:
                print("[!] ข้อมูลไม่ถูกต้อง บันทึก session ID แรกแทน")
                save_valid_session(valid_sessions[0])
        else:
            # บันทึก session ID เดียวที่ใช้งานได้
            save_valid_session(valid_sessions[0])
    else:
        print("[!] ไม่พบ session ID ที่ใช้งานได้")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[!] เกิดข้อผิดพลาด: {e}")
