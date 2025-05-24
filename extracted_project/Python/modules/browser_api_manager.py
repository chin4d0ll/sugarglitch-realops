import subprocess
import json
import os

class BrowserAPIManager:
    def __init__(self):
        self.browser_script = "browser_api.js"
        
    def test_browser_connection(self):
        """ทดสอบการเชื่อมต่อ Browser API"""
        try:
            print("[~] กำลังทดสอบ BrightData Browser API...")
            result = subprocess.run(
                ["node", self.browser_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("[✓] Browser API ทำงานปกติ!")
                print(result.stdout)
                return True
            else:
                print(f"[!] Browser API ล้มเหลว: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("[!] Browser API timeout")
            return False
        except Exception as e:
            print(f"[!] เกิดข้อผิดพลาด: {str(e)}")
            return False
    
    def extract_instagram_data_via_browser(self, session_id):
        """ดึงข้อมูล Instagram ผ่าน Browser API"""
        try:
            print("[~] กำลังดึงข้อมูล Instagram ผ่าน Browser API...")
            
            # สร้างไฟล์ JavaScript ชั่วคราวสำหรับรันการดึงข้อมูล
            extract_script = f"""
const {{ extractInstagramData }} = require('./browser_api.js');

async function main() {{
    const data = await extractInstagramData('{session_id}');
    if (data) {{
        console.log('BROWSER_API_RESULT:' + JSON.stringify(data));
    }} else {{
        console.log('BROWSER_API_ERROR:Failed to extract data');
    }}
}}

main().catch(console.error);
"""
            
            # เขียนไฟล์ชั่วคราว
            with open("temp_extract.js", "w") as f:
                f.write(extract_script)
            
            # รันสคริปต์
            result = subprocess.run(
                ["node", "temp_extract.js"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # ลบไฟล์ชั่วคราว
            if os.path.exists("temp_extract.js"):
                os.remove("temp_extract.js")
            
            if result.returncode == 0:
                # แยกผลลัพธ์จาก output
                for line in result.stdout.split('\n'):
                    if line.startswith('BROWSER_API_RESULT:'):
                        data_json = line.replace('BROWSER_API_RESULT:', '')
                        data = json.loads(data_json)
                        print(f"[✓] ดึงข้อมูลสำเร็จ! จำนวน {len(data)} รายการ")
                        return data
                    elif line.startswith('BROWSER_API_ERROR:'):
                        error_msg = line.replace('BROWSER_API_ERROR:', '')
                        print(f"[!] {error_msg}")
                        return None
                
                print("[!] ไม่พบผลลัพธ์จาก Browser API")
                return None
            else:
                print(f"[!] Browser API ล้มเหลว: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"[!] เกิดข้อผิดพลาด: {str(e)}")
            return None

def fetch_real_dms_browser_api(session_file):
    """ฟังก์ชันหลักสำหรับดึง DMs ผ่าน Browser API"""
    # โหลด session
    try:
        with open(session_file) as f:
            session_data = json.load(f)
        
        session_id = session_data.get("sessionid")
        if not session_id or session_id == "your_session_id_here":
            print("[!] ไม่พบ session ID ที่ถูกต้อง")
            return None
        
        # สร้าง BrowserAPIManager
        browser_manager = BrowserAPIManager()
        
        # ทดสอบการเชื่อมต่อก่อน
        if not browser_manager.test_browser_connection():
            print("[!] Browser API ไม่พร้อมใช้งาน")
            return None
        
        # ดึงข้อมูลจริง
        return browser_manager.extract_instagram_data_via_browser(session_id)
        
    except Exception as e:
        print(f"[!] เกิดข้อผิดพลาด: {str(e)}")
        return None
