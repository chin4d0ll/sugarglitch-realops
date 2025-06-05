import json
import os
from datetime import datetime

def convert_json_to_html():
    """แปลง dm_output.json เป็น HTML ที่อ่านง่าย"""
    
    # ตรวจสอบว่ามีไฟล์ dm_output.json หรือไม่
    if not os.path.exists("dm_output.json"):
        print("❌ ไม่พบไฟล์ dm_output.json")
        print("กรุณารัน dm_extractor.py ก่อน")
        return
    
    # อ่านข้อมูลจาก JSON
    with open("dm_output.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # สร้าง HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram DM Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .chat-container {{
            background: white;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .chat-header {{
            background-color: #405de6;
            color: white;
            padding: 15px;
            font-weight: bold;
        }}
        .message {{
            padding: 10px 15px;
            border-bottom: 1px solid #eee;
        }}
        .message:last-child {{
            border-bottom: none;
        }}
        .message:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .no-messages {{
            padding: 20px;
            text-align: center;
            color: #666;
            font-style: italic;
        }}
        .stats {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .export-info {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 Instagram DM Export</h1>
        <p>ข้อมูล DM ที่ดึงมาจาก Instagram</p>
    </div>
    
    <div class="stats">
        <h3>📊 สถิติการดึงข้อมูล</h3>
        <p><strong>จำนวนแชทที่ดึงได้:</strong> {len(data)} แชท</p>
        <p><strong>เวลาที่สร้างรายงาน:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    </div>
"""

    # เพิ่มข้อมูลแชทแต่ละอัน
    for chat in data:
        chat_index = chat.get('chat_index', 'N/A')
        messages = chat.get('messages', [])
        
        html_content += f"""
    <div class="chat-container">
        <div class="chat-header">
            💬 แชท #{chat_index + 1} ({len(messages)} ข้อความ)
        </div>
"""
        
        if messages:
            for i, message in enumerate(messages):
                # ป้องกัน HTML injection
                safe_message = message.replace('<', '&lt;').replace('>', '&gt;')
                html_content += f"""
        <div class="message">
            <strong>ข้อความ #{i + 1}:</strong> {safe_message}
        </div>"""
        else:
            html_content += """
        <div class="no-messages">
            ไม่มีข้อความในแชทนี้
        </div>"""
        
        html_content += """
    </div>
"""

    # ปิด HTML
    html_content += f"""
    <div class="export-info">
        <p>🔒 ข้อมูลนี้ถูกดึงมาเพื่อการศึกษาเท่านั้น</p>
        <p>สร้างโดย Instagram DM Extractor - {datetime.now().strftime('%Y')}</p>
    </div>
</body>
</html>
"""

    # บันทึกเป็นไฟล์ HTML
    with open("dm_output.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ แปลง JSON เป็น HTML สำเร็จ!")
    print("📄 ไฟล์: dm_output.html")
    print(f"📊 จำนวนแชท: {len(data)}")
    
    # คำนวณจำนวนข้อความทั้งหมด
    total_messages = sum(len(chat.get('messages', [])) for chat in data)
    print(f"💬 จำนวนข้อความทั้งหมด: {total_messages}")

if __name__ == "__main__":
    convert_json_to_html()
