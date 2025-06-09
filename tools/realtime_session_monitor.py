# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Real-time Session Monitor
Monitors and automatically saves fresh Instagram sessions
"""

import os
import json
import sys
import time
import requests
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import webbrowser

class SessionMonitor:
    def __init__(self):
        self.session_file = "tools/session_alx_trading.json"
        self.backup_dir = "sessions_fresh"
        self.port = 8888
        self.server = None
        self.running = False

        os.makedirs("tools", exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def validate_session(self, session_data):
        """Quick session validation"""
        if not session_data.get('sessionid'):
            return False

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': f"sessionid={session_data['sessionid']}"
        }

        try:
            response = requests.get('https://www.instagram.com/', headers=headers, timeout=5)
            return response.status_code == 200 and 'login' not in response.url.lower()
        except Exception:
            return False

    def save_session(self, session_data):
        """Save session with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        session_info = {
            'sessionid': session_data.get('sessionid', ''),
            'csrftoken': session_data.get('csrftoken', ''),
            'ds_user_id': session_data.get('ds_user_id', ''),
            'mid': session_data.get('mid', ''),
            'target': 'alx.trading',
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'extraction_method': 'realtime_monitor'
        }

        # Save main session
        with open(self.session_file, 'w') as f:
            json.dump(session_info, f, indent=2)

        # Save backup
        backup_file = f"{self.backup_dir}/session_{timestamp}.json"
        with open(backup_file, 'w') as f:
            json.dump(session_info, f, indent=2)

        print(f"✅ Session saved: {self.session_file}")
        print(f"✅ Backup saved: {backup_file}")
        return True

class SessionHandler(BaseHTTPRequestHandler):
    def __init__(self, monitor, *args, **kwargs):
        self.monitor = monitor
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html = self.get_capture_page()
            self.wfile.write(html.encode())

        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            status = {'status': 'monitoring', 'timestamp': datetime.now().isoformat()}
            self.wfile.write(json.dumps(status).encode())

    def do_POST(self):
        """Handle POST requests with session data"""
        if self.path == '/capture':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                session_data = json.loads(post_data.decode())

                # Validate and save session
                if self.monitor.validate_session(session_data):
                    self.monitor.save_session(session_data)

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()

                    response = {'success': True, 'message': 'Session captured and saved!'}
                    self.wfile.write(json.dumps(response).encode())

                    print("🎉 Fresh session captured and saved!")
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()

                    response = {'success': False, 'message': 'Invalid session'}
                    self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                response = {'success': False, 'message': f'Error: {str(e)}'}
                self.wfile.write(json.dumps(response).encode())

    def get_capture_page(self):
        """Generate the session capture page"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Session Capture</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #fafafa; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { text-align: center; color: #333; }
        .step { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 4px; }
        .button { background: #0095f6; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .button:hover { background: #007bb3; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .log { background: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace; height: 200px; overflow-y: scroll; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🍪 Instagram Session Capture</h1>
        <p class="header">Real-time session extraction tool</p>

        <div class="step">
            <h3>📋 Instructions:</h3>
            <ol>
                <li>Open <a href="https://www.instagram.com" target="_blank">Instagram</a> in a new tab</li>
                <li>Log into your account</li>
                <li>Press F12 → Application → Cookies → https://www.instagram.com</li>
                <li>Copy the sessionid value and paste below</li>
                <li>Click "Capture Session" to save it automatically</li>
            </ol>
        </div>

        <div class="step">
            <h3>🔑 Session Data:</h3>
            <input type="text" id="sessionid" placeholder="Paste sessionid here..." style="width: 100%; padding: 8px; margin: 5px 0;">
            <input type="text" id="csrftoken" placeholder="csrftoken (optional)" style="width: 100%; padding: 8px; margin: 5px 0;">
            <input type="text" id="ds_user_id" placeholder="ds_user_id (optional)" style="width: 100%; padding: 8px; margin: 5px 0;">
            <br><br>
            <button class="button" onclick="captureSession()">🚀 Capture Session</button>
            <button class="button" onclick="autoExtract()" style="background: #28a745;">🤖 Auto Extract</button>
        </div>

        <div id="status"></div>

        <div class="step">
            <h3>📊 Log:</h3>
            <div id="log" class="log"></div>
        </div>
    </div>

    <script>
        function log(message) {
            const logDiv = document.getElementById('log');
            const timestamp = new Date().toLocaleTimeString();
            logDiv.innerHTML += "[${timestamp}] ${message}<br>";
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        function showStatus(message, type = 'success') {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = "<div class="status ${type}">${message}</div>";
        }

        function captureSession() {
            const sessionid = document.getElementById('sessionid').value.trim();
            const csrftoken = document.getElementById('csrftoken').value.trim();
            const ds_user_id = document.getElementById('ds_user_id').value.trim();

            if (!sessionid) {
                showStatus('❌ Please enter sessionid', 'error');
                return;
            }

            const sessionData = {
                sessionid: sessionid,
                csrftoken: csrftoken,
                ds_user_id: ds_user_id
            };

            log('🔄 Capturing session...');

            fetch('/capture', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(sessionData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('✅ ' + data.message, 'success');
                    log('✅ Session captured successfully!');
                } else {
                    showStatus('❌ ' + data.message, 'error');
                    log('❌ Session capture failed: ' + data.message);
                }
            })
            .catch(error => {
                showStatus('❌ Network error', 'error');
                log('❌ Network error: ' + error);
            });
        }

        function autoExtract() {
            log('🤖 Starting auto extraction...');

            // Try to extract cookies from current domain (won't work due to CORS, but shows the concept)
            if (document.cookie) {
                const cookies = document.cookie.split(';');
                log("Found ${cookies.length} cookies in current domain");
            }

            showStatus('ℹ️ Auto extraction requires manual cookie paste due to security restrictions', 'error');
            log('ℹ️ Please use manual method above');
        }

        // Auto-refresh status
        setInterval(() => {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    log("📡 Monitor active - ${data.timestamp}");
                })
                .catch(() => {});
        }, 30000);

        log('🚀 Session monitor started');
        log('📋 Follow the instructions above to capture your session');
    </script>
</body>
</html>
        '''

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def create_handler(monitor):
    """Create handler with monitor reference"""
    def handler(*args, **kwargs):
        SessionHandler(monitor, *args, **kwargs)
    return handler

class RealTimeSessionMonitor(SessionMonitor):
    def start_server(self):
        """Start the monitoring server"""
        try:
            handler = create_handler(self)
            self.server = HTTPServer(('localhost', self.port), handler)

            print(f"🌐 Session monitor started on http://localhost:{self.port}")
            print("🔗 Open this URL in your browser to capture sessions")

            # Try to open browser automatically
            try:
                webbrowser.open(f'http://localhost:{self.port}')
            except Exception:
                pass

            self.running = True
            self.server.serve_forever()

        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped")
            self.stop_server()
        except Exception as e:
            print(f"❌ Server error: {e}")

    def stop_server(self):
        """Stop the monitoring server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        self.running = False

    def run(self):
        """Main execution"""
        print("📡 REAL-TIME SESSION MONITOR")
        print("="*40)
        print(f"Port: {self.port}")
        print(f"Output: {self.session_file}")
        print()

        try:
            self.start_server()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.stop_server()

def main():
    try:
        monitor = RealTimeSessionMonitor()
        monitor.run()
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
