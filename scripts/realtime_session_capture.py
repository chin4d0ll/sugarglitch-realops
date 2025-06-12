# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Real-time Session Interceptor
จับ sessionid แบบ real-time ขณะ login สำเร็จ
"""

import json
import os
import time
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import urllib.parse

class SessionInterceptor:
    def __init__(self):
        self.session_file = "tools/session_alx_trading.json"
        self.captured_session = None
        self.server = None
        self.server_thread = None

    def create_login_helper_page(self):
        """สร้างหน้าเว็บช่วย login และจับ session"""
        html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Session Capture</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .step { margin: 20px 0; padding: 15px; background: #e3f2fd; border-radius: 5px; }
        .success { background: #e8f5e8; color: #2e7d32; }
        .error { background: #ffebee; color: #c62828; }
        button { padding: 10px 20px; background: #1976d2; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #1565c0; }
        #status { margin-top: 20px; padding: 15px; border-radius: 5px; }
        .session-info { background: #f3e5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Instagram Session Capture Tool</h1>
        <p>เครื่องมือจับ sessionid แบบ real-time ขณะ login สำเร็จ</p>

        <div class="step">
            <h3>ขั้นตอนที่ 1: เปิด Instagram</h3>
            <button onclick="openInstagram()">เปิด Instagram</button>
            <p>จะเปิด Instagram ในแท็บใหม่</p>
        </div>

        <div class="step">
            <h3>ขั้นตอนที่ 2: Login</h3>
            <p>Login ด้วย username/password ของคุณใน Instagram</p>
        </div>

        <div class="step">
            <h3>ขั้นตอนที่ 3: จับ Session</h3>
            <button onclick="captureSession()">จับ Session ทันที</button>
            <p>กดหลังจาก login สำเร็จแล้ว</p>
        </div>

        <div id="status"></div>
    </div>

    <script>
        function showStatus(message, type = 'info') {
            const status = document.getElementById('status');
            status.innerHTML = message;
            status.className = type;
        }

        function openInstagram() {
            window.open('https://www.instagram.com/accounts/login/', '_blank');
            showStatus('✅ เปิด Instagram แล้ว - กรุณา login ในแท็บที่เปิดขึ้น', 'success');
        }

        async function captureSession() {
            showStatus('🔍 กำลังจับ session...', 'info');

            try {
                // ดึง cookies จาก browser
                const cookies = document.cookie.split(';');
                let sessionData = {};

                // หา sessionid จาก cookies ของ Instagram
                // เนื่องจาก same-origin policy เราต้องใช้วิธีอื่น

                // แจ้งให้ user คัดลอก sessionid เอง
                const sessionid = prompt('กรุณาเปิด Developer Tools (F12)\\nไป Application > Cookies > instagram.com\\nคัดลอก sessionid มาใส่ที่นี่:');

                if (sessionid && sessionid.trim()) {
                    // ส่ง session ไปบันทึก
                    const response = await fetch('/save-session', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            sessionid: sessionid.trim(),
                            timestamp: new Date().toISOString()
                        })
                    });

                    const result = await response.json();

                    if (result.success) {
                        showStatus('🎉 จับ session สำเร็จ! พร้อมใช้งาน', 'success');

                        // แสดงข้อมูล session
                        const sessionInfo = document.createElement('div');
                        sessionInfo.className = 'session-info';
                        sessionInfo.innerHTML = "
                            <h4>📋 Session Information</h4>
                            <p><strong>Session ID:</strong> ${sessionid.substring(0, 20)}...</p>
                            <p><strong>เวลา:</strong> ${new Date().toLocaleString('th-TH')}</p>
                            <p><strong>ไฟล์:</strong> tools/session_alx_trading.json</p>
                        ";
                        document.querySelector('.container').appendChild(sessionInfo);
                    } else {
                        showStatus('❌ ไม่สามารถบันทึก session ได้: ' + result.error, 'error');
                    }
                } else {
                    showStatus('❌ ไม่ได้ใส่ sessionid', 'error');
                }

            } catch (error) {
                showStatus('❌ เกิดข้อผิดพลาด: ' + error.message, 'error');
            }
        }

        // Auto refresh status
        setInterval(async () => {
            try {
                const response = await fetch('/status');
                const status = await response.json();
                if (status.captured) {
                    showStatus('✅ Session ถูกจับเรียบร้อยแล้ว!', 'success');
                }
            } catch (e) {
                // Ignore connection errors
            }
        }, 2000);
    </script>
</body>
</html>
'''
        return html_content

    class RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, interceptor, *args, **kwargs):
            self.interceptor = interceptor
            super().__init__(*args, **kwargs)

        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()
                self.wfile.write(self.interceptor.create_login_helper_page().encode('utf-8'))
            elif self.path == '/status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                status = {'captured': self.interceptor.captured_session is not None}
                self.wfile.write(json.dumps(status).encode('utf-8'))
            else:
                self.send_error(404)

        def do_POST(self):
            if self.path == '/save-session':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)

                try:
                    data = json.loads(post_data.decode('utf-8'))
                    sessionid = data.get('sessionid', '').strip()

                    if sessionid:
                        # บันทึก session
                        session_info = {
                            'sessionid': sessionid,
                            'target': 'alx.trading',
                            'created_at': datetime.now().isoformat(),
                            'status': 'active',
                            'capture_method': 'realtime_intercept'
                        }

                        os.makedirs('tools', exist_ok = True)
                        with open(self.interceptor.session_file, 'w') as f:
                            json.dump(session_info, f, indent = 2)

                        self.interceptor.captured_session = session_info

                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {'success': True, 'message': 'Session saved successfully'}
                        self.wfile.write(json.dumps(response).encode('utf-8'))

                        print(f"✅ Session จับได้แล้ว: {sessionid[:20]}...")
                        print(f"📁 บันทึกไว้ที่: {self.interceptor.session_file}")
                    else:
                        raise ValueError("ไม่มี sessionid")

                except Exception as e:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'error': str(e)}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_error(404)

        def log_message(self, format, *args):
            # ปิด log ของ HTTP server
            pass

    def start_server(self, port = 8080):
        """เริ่ม HTTP server สำหรับจับ session"""
        handler = lambda *args, **kwargs: self.RequestHandler(self, *args, **kwargs)

        try:
            self.server = HTTPServer(('localhost', port), handler)
            print(f"🌐 เริ่ม HTTP server ที่ http://localhost:{port}")

            def run_server():
                self.server.serve_forever()

            self.server_thread = threading.Thread(target = run_server, daemon = True)
            self.server_thread.start()

            return True
        except Exception as e:
            print(f"❌ ไม่สามารถเริ่ม server ได้: {e}")
            return False

    def stop_server(self):
        """หยุด HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    def run(self):
        """เรียกใช้งานหลัก"""
        print("🚀 REAL-TIME SESSION INTERCEPTOR")
        print("="*60)
        print("จับ sessionid แบบ real-time ขณะ login สำเร็จ")
        print()

        # เริ่ม server
        if not self.start_server():
            return False

        # เปิด browser
        try:
            webbrowser.open('http://localhost:8080')
            print("✅ เปิด browser แล้ว")
        except Exception:
            print("⚠️ ไม่สามารถเปิด browser อัตโนมัติได้")
            print("กรุณาเปิด http://localhost:8080 ด้วยตนเอง")

        print("\n📋 วิธีการใช้งาน:")
        print("1. เปิด Instagram ในแท็บใหม่")
        print("2. Login ด้วย username/password")
        print("3. กดปุ่ม 'จับ Session ทันที'")
        print("4. คัดลอก sessionid จาก Developer Tools")
        print("5. Session จะถูกบันทึกอัตโนมัติ")
        print("\n⏳ รอการจับ session... (กด Ctrl+C เพื่อออก)")

        try:
            # รอจนกว่าจะจับ session ได้
            while not self.captured_session:
                time.sleep(1)

            print("\n🎉 SUCCESS! Session จับได้แล้ว!")
            print(f"📁 บันทึกไว้ที่: {self.session_file}")
            print("\n📋 ขั้นตอนถัดไป:")
            print("1. เพิ่ม working proxies ใน config/proxies.json")
            print("2. รัน DM extraction: python tools/dm_extraction_with_interceptor.py")
            print("3. ตรวจสอบ logs: tail -f logs/requests.log")

            return True

        except KeyboardInterrupt:
            print("\n\n⚠️ ผู้ใช้ยกเลิกการทำงาน")
            return False
        finally:
            self.stop_server()

if __name__ == "__main__":
    try:
        interceptor = SessionInterceptor()
        interceptor.run()
    except KeyboardInterrupt:
        print("\n\n👋 ลาก่อน!")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
