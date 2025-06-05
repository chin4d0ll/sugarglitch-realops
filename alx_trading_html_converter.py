import json
import os
from datetime import datetime
import glob

def convert_alx_trading_to_html():
    """แปลงข้อมูล DM จาก alx.trading เป็น HTML"""
    
    # หาไฟล์ alx.trading ล่าสุด
    alx_files = glob.glob("alx_trading_dm_*.json")
    
    if not alx_files:
        print("❌ ไม่พบไฟล์ข้อมูล alx.trading")
        print("กรุณารัน alx_trading_dm_extractor.py ก่อน")
        return
    
    # เรียงตามเวลาและเอาไฟล์ล่าสุด
    latest_file = max(alx_files, key=os.path.getctime)
    print(f"📄 ใช้ไฟล์: {latest_file}")
    
    # อ่านข้อมูล
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # สร้าง HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DM จาก {data['target_username']} - {datetime.now().strftime('%d/%m/%Y')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .username {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #007bff;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .messages-container {{
            background: #fff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .messages-header {{
            background: #007bff;
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            display: flex;
            align-items: center;
        }}
        .message {{
            padding: 15px 20px;
            border-bottom: 1px solid #eee;
            transition: background-color 0.2s;
        }}
        .message:hover {{
            background-color: #f8f9fa;
        }}
        .message:last-child {{
            border-bottom: none;
        }}
        .message-number {{
            color: #007bff;
            font-weight: bold;
            margin-right: 10px;
        }}
        .message-text {{
            flex: 1;
            line-height: 1.5;
        }}
        .no-messages {{
            padding: 50px 20px;
            text-align: center;
            color: #666;
            font-style: italic;
        }}
        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        .status-success {{
            background: #d4edda;
            color: #155724;
        }}
        .status-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        .export-info {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .trading-icon {{
            font-size: 1.2em;
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="username">
                <span class="trading-icon">📈</span>
                {data['target_username']}
            </div>
            <p>ข้อมูล Direct Messages จาก Instagram</p>
            <span class="status-badge {'status-success' if data['chat_found'] else 'status-warning'}">
                {'✅ พบแชท' if data['chat_found'] else '⚠️ ไม่พบแชท'}
            </span>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(data.get('messages', []))}</div>
                <div class="stat-label">ข้อความทั้งหมด</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{'✅' if data['chat_found'] else '❌'}</div>
                <div class="stat-label">สถานะแชท</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{datetime.fromisoformat(data['extraction_time']).strftime('%H:%M')}</div>
                <div class="stat-label">เวลาดึงข้อมูล</div>
            </div>
        </div>
        
        <div class="messages-container">
            <div class="messages-header">
                <span class="trading-icon">💬</span>
                ข้อความจาก {data['target_username']}
            </div>
"""

    # เพิ่มข้อความ
    if data.get('messages') and len(data['messages']) > 0:
        for i, message in enumerate(data['messages'], 1):
            # ป้องกัน HTML injection
            safe_message = message.replace('<', '&lt;').replace('>', '&gt;')
            html_content += f"""
            <div class="message">
                <span class="message-number">#{i}</span>
                <div class="message-text">{safe_message}</div>
            </div>"""
    else:
        html_content += """
            <div class="no-messages">
                <span class="trading-icon">📭</span>
                ไม่พบข้อความในแชทนี้<br>
                <small>อาจเป็นเพราะ: ไม่มีสิทธิ์เข้าถึง, บัญชีไม่มีอยู่, หรือไม่เคยมีการสนทนา</small>
            </div>"""

    # ปิด HTML
    html_content += f"""
        </div>
        
        <div class="export-info">
            <p><span class="trading-icon">🔒</span> ข้อมูลนี้ถูกดึงมาเพื่อการศึกษาเท่านั้น</p>
            <p>สร้างเมื่อ: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>ไฟล์ต้นฉบับ: {latest_file}</p>
        </div>
    </div>
</body>
</html>
"""

    # บันทึกไฟล์
    output_file = f"alx_trading_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ สร้างรายงาน HTML สำเร็จ!")
    print(f"📄 ไฟล์: {output_file}")
    print(f"💬 จำนวนข้อความ: {len(data.get('messages', []))}")
    print(f"📊 สถานะ: {'พบแชท' if data['chat_found'] else 'ไม่พบแชท'}")

if __name__ == "__main__":
    convert_alx_trading_to_html()
