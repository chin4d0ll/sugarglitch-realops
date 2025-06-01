#!/usr/bin/env python3
"""
💀🔥 ULTIMATE INSTAGRAM WEB DASHBOARD 2025 🔥💀
=================================================
Beautiful web dashboard for Instagram reconnaissance with real-time updates!

✨ Features:
- Modern dark UI with animations
- Real-time WebSocket updates
- Interactive data visualization
- Multi-user support
- REST API endpoints
- Advanced export options
- Mobile responsive design

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 - Ultimate Web Edition!
For: Educational & Security Research Only!
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit, join_room
import asyncio
import json
import time
import threading
from datetime import datetime
from pathlib import Path
import uuid
from concurrent.futures import ThreadPoolExecutor
import logging

# Import our enhanced bypass
try:
    from instagram_private_bypass_2025_enhanced import SuperEnhancedInstagramBypass
except ImportError:
    print("❌ Enhanced bypass module not found!")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltimateWebDashboard:
    """
    💀 Ultimate Web Dashboard - Modern and Powerful
    
    Features:
    - Real-time updates via WebSocket
    - Beautiful dark theme
    - Interactive charts
    - Multi-target scanning
    - Export capabilities
    - REST API
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'ultimate_instagram_2025'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Data storage
        self.active_scans = {}
        self.scan_results = {}
        self.scan_history = []
        
        # Thread pool for scanning
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        self.setup_routes()
        self.setup_socketio()

    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main dashboard page"""
            return render_template('dashboard.html')
        
        @self.app.route('/api/scan/start', methods=['POST'])
        def start_scan():
            """Start new scan"""
            try:
                data = request.json
                username = data.get('username', '').strip()
                scan_options = data.get('options', {})
                
                if not username:
                    return jsonify({'error': 'Username required'}), 400
                
                scan_id = str(uuid.uuid4())
                
                # Start scan in background
                self.executor.submit(self.run_scan, scan_id, username, scan_options)
                
                return jsonify({
                    'success': True,
                    'scan_id': scan_id,
                    'message': f'Scan started for @{username}'
                })
                
            except Exception as e:
                logger.error(f"Start scan error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/scan/batch', methods=['POST'])
        def start_batch_scan():
            """Start batch scan"""
            try:
                data = request.json
                usernames = data.get('usernames', [])
                scan_options = data.get('options', {})
                
                if not usernames:
                    return jsonify({'error': 'Usernames required'}), 400
                
                batch_id = str(uuid.uuid4())
                scan_ids = []
                
                for username in usernames:
                    if username.strip():
                        scan_id = str(uuid.uuid4())
                        scan_ids.append(scan_id)
                        self.executor.submit(self.run_scan, scan_id, username.strip(), scan_options)
                
                return jsonify({
                    'success': True,
                    'batch_id': batch_id,
                    'scan_ids': scan_ids,
                    'message': f'Batch scan started for {len(scan_ids)} targets'
                })
                
            except Exception as e:
                logger.error(f"Batch scan error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/scan/<scan_id>/status')
        def get_scan_status(scan_id):
            """Get scan status"""
            if scan_id in self.active_scans:
                return jsonify(self.active_scans[scan_id])
            elif scan_id in self.scan_results:
                return jsonify({
                    'status': 'completed',
                    'result': self.scan_results[scan_id]
                })
            else:
                return jsonify({'error': 'Scan not found'}), 404
        
        @self.app.route('/api/scans/history')
        def get_scan_history():
            """Get scan history"""
            return jsonify(self.scan_history[-50:])  # Last 50 scans
        
        @self.app.route('/api/export/<scan_id>')
        def export_scan(scan_id):
            """Export scan results"""
            if scan_id not in self.scan_results:
                return jsonify({'error': 'Scan not found'}), 404
            
            try:
                result = self.scan_results[scan_id]
                filename = f"instagram_scan_{scan_id[:8]}.json"
                
                # Save to file
                file_path = Path(f"/tmp/{filename}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, default=str)
                
                return send_file(file_path, as_attachment=True, download_name=filename)
                
            except Exception as e:
                logger.error(f"Export error: {e}")
                return jsonify({'error': str(e)}), 500

    def setup_socketio(self):
        """Setup SocketIO events"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            emit('connected', {'message': 'Connected to Ultimate Instagram Dashboard!'})
            logger.info('Client connected')
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            logger.info('Client disconnected')
        
        @self.socketio.on('join_scan')
        def handle_join_scan(data):
            """Join scan room for updates"""
            scan_id = data.get('scan_id')
            if scan_id:
                join_room(scan_id)
                emit('joined_scan', {'scan_id': scan_id})

    def run_scan(self, scan_id: str, username: str, options: dict):
        """Run scan in background thread"""
        try:
            # Initialize scan status
            self.active_scans[scan_id] = {
                'id': scan_id,
                'username': username,
                'status': 'starting',
                'progress': 0,
                'start_time': datetime.now().isoformat(),
                'messages': []
            }
            
            # Emit scan started
            self.socketio.emit('scan_update', self.active_scans[scan_id])
            
            # Run async scan
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.execute_scan_async(scan_id, username, options))
            
            # Complete scan
            self.active_scans[scan_id]['status'] = 'completed'
            self.active_scans[scan_id]['progress'] = 100
            self.active_scans[scan_id]['end_time'] = datetime.now().isoformat()
            
            # Store results
            self.scan_results[scan_id] = {
                'scan_info': self.active_scans[scan_id],
                'data': result
            }
            
            # Add to history
            self.scan_history.append({
                'scan_id': scan_id,
                'username': username,
                'timestamp': datetime.now().isoformat(),
                'success': result.get('success', False)
            })
            
            # Emit completion
            self.socketio.emit('scan_complete', {
                'scan_id': scan_id,
                'result': result
            })
            
            # Clean up active scan
            del self.active_scans[scan_id]
            
        except Exception as e:
            logger.error(f"Scan error for {username}: {e}")
            
            # Update scan with error
            if scan_id in self.active_scans:
                self.active_scans[scan_id]['status'] = 'error'
                self.active_scans[scan_id]['error'] = str(e)
                
                self.socketio.emit('scan_error', {
                    'scan_id': scan_id,
                    'error': str(e)
                })

    async def execute_scan_async(self, scan_id: str, username: str, options: dict):
        """Execute the actual async scan"""
        
        def update_progress(progress: int, message: str):
            """Helper to update progress"""
            if scan_id in self.active_scans:
                self.active_scans[scan_id]['progress'] = progress
                self.active_scans[scan_id]['messages'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': message
                })
                self.socketio.emit('scan_update', self.active_scans[scan_id])
        
        try:
            # Create bypass instance
            update_progress(10, f"🎯 Initializing scan for @{username}")
            bypass = SuperEnhancedInstagramBypass(username)
            
            # Execute based on options
            cache_mining = options.get('cache_mining', True)
            osint_gathering = options.get('osint_gathering', True)
            
            if cache_mining and osint_gathering:
                update_progress(30, "💎 Starting enhanced cache mining")
                cache_result = await bypass.enhanced_cache_mining()
                
                update_progress(70, "🕵️ Starting OSINT gathering")
                osint_result = await bypass.enhanced_osint_gathering()
                
                update_progress(90, "📊 Generating final report")
                report = await bypass.generate_final_report()
                
                result = {
                    'success': len(bypass.success_methods) > 0,
                    'extracted_data': bypass.extracted_data,
                    'results': bypass.results,
                    'report': report
                }
                
            elif cache_mining:
                update_progress(50, "💎 Executing cache mining only")
                result = await bypass.enhanced_cache_mining()
                
            elif osint_gathering:
                update_progress(50, "🕵️ Executing OSINT gathering only")
                result = await bypass.enhanced_osint_gathering()
                
            else:
                result = {'success': False, 'error': 'No scan methods selected'}
            
            update_progress(100, "✅ Scan completed successfully!")
            return result
            
        except Exception as e:
            update_progress(0, f"❌ Scan failed: {str(e)}")
            return {'success': False, 'error': str(e)}

    def create_html_template(self):
        """Create HTML template for dashboard"""
        
        template_dir = Path('templates')
        template_dir.mkdir(exist_ok=True)
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💀🔥 Ultimate Instagram Dashboard 2025 🔥💀</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #ffffff;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
        }
        
        .header {
            background: linear-gradient(135deg, #ff1493 0%, #00ffff 100%);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 20px;
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 0 0 20px rgba(255, 20, 147, 0.5);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .panel {
            background: rgba(26, 26, 26, 0.8);
            border: 1px solid #333;
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        
        .panel h3 {
            color: #ff1493;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .input-group {
            margin-bottom: 15px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 5px;
            color: #00ffff;
        }
        
        .input-group input, .input-group textarea {
            width: 100%;
            padding: 10px;
            background: #2a2a2a;
            border: 1px solid #555;
            border-radius: 5px;
            color: #fff;
            font-family: inherit;
        }
        
        .input-group input:focus, .input-group textarea:focus {
            outline: none;
            border-color: #ff1493;
            box-shadow: 0 0 10px rgba(255, 20, 147, 0.3);
        }
        
        .btn {
            background: linear-gradient(135deg, #ff1493 0%, #00ffff 100%);
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(255, 20, 147, 0.3);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .checkbox-group {
            display: flex;
            gap: 15px;
            margin: 10px 0;
        }
        
        .checkbox-group label {
            display: flex;
            align-items: center;
            gap: 5px;
            cursor: pointer;
        }
        
        .progress-bar {
            width: 100%;
            height: 25px;
            background: #2a2a2a;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #ff1493 0%, #00ffff 100%);
            width: 0%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .console {
            background: #000;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 15px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #00ff00;
        }
        
        .console-line {
            margin-bottom: 5px;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .scan-item {
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .scan-status {
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .status-running {
            background: #ffa500;
            color: #000;
        }
        
        .status-completed {
            background: #00ff00;
            color: #000;
        }
        
        .status-error {
            background: #ff0000;
            color: #fff;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: #2a2a2a;
            border-radius: 10px;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #ff1493;
        }
        
        .stat-label {
            color: #ccc;
            margin-top: 5px;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
            }
            
            .header {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        💀🔥 ULTIMATE INSTAGRAM DASHBOARD 2025 🔥💀
    </div>
    
    <div class="container">
        <!-- Left Panel - Scanner -->
        <div class="panel">
            <h3>🎯 Instagram Scanner</h3>
            
            <div class="input-group">
                <label>Instagram Username (without @):</label>
                <input type="text" id="username" placeholder="Enter username...">
            </div>
            
            <div class="input-group">
                <label>Batch Usernames (one per line):</label>
                <textarea id="batch-usernames" rows="4" placeholder="username1\nusername2\nusername3"></textarea>
            </div>
            
            <div class="checkbox-group">
                <label>
                    <input type="checkbox" id="cache-mining" checked>
                    💎 Cache Mining
                </label>
                <label>
                    <input type="checkbox" id="osint-gathering" checked>
                    🕵️ OSINT Gathering
                </label>
            </div>
            
            <div>
                <button class="btn" onclick="startSingleScan()">🚀 Start Single Scan</button>
                <button class="btn" onclick="startBatchScan()">📊 Start Batch Scan</button>
                <button class="btn" onclick="clearConsole()">🗑️ Clear Console</button>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" id="progress-bar">0%</div>
            </div>
        </div>
        
        <!-- Right Panel - Active Scans -->
        <div class="panel">
            <h3>📊 Active Scans</h3>
            <div id="active-scans"></div>
        </div>
        
        <!-- Full Width - Console -->
        <div class="panel full-width">
            <h3>📺 Live Console</h3>
            <div class="console" id="console"></div>
        </div>
        
        <!-- Full Width - Statistics -->
        <div class="panel full-width">
            <h3>📈 Statistics</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number" id="total-scans">0</div>
                    <div class="stat-label">Total Scans</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="successful-scans">0</div>
                    <div class="stat-label">Successful</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="active-count">0</div>
                    <div class="stat-label">Active</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Initialize Socket.IO
        const socket = io();
        
        let activeScans = {};
        let totalScans = 0;
        let successfulScans = 0;
        
        // Socket event handlers
        socket.on('connect', function() {
            addConsoleMessage('🔗 Connected to Ultimate Instagram Dashboard!');
        });
        
        socket.on('scan_update', function(data) {
            updateActiveScan(data);
            if (data.messages && data.messages.length > 0) {
                const lastMessage = data.messages[data.messages.length - 1];
                addConsoleMessage(`[${data.username}] ${lastMessage.message}`);
            }
            updateProgress(data.progress);
        });
        
        socket.on('scan_complete', function(data) {
            addConsoleMessage(`✅ Scan completed for ${data.scan_id}`);
            removeActiveScan(data.scan_id);
            if (data.result.success) {
                successfulScans++;
            }
            updateStatistics();
        });
        
        socket.on('scan_error', function(data) {
            addConsoleMessage(`❌ Scan error for ${data.scan_id}: ${data.error}`);
            removeActiveScan(data.scan_id);
            updateStatistics();
        });
        
        // Functions
        function startSingleScan() {
            const username = document.getElementById('username').value.trim();
            if (!username) {
                alert('Please enter a username!');
                return;
            }
            
            const options = {
                cache_mining: document.getElementById('cache-mining').checked,
                osint_gathering: document.getElementById('osint-gathering').checked
            };
            
            fetch('/api/scan/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    options: options
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addConsoleMessage(`🚀 Started scan for @${username}`);
                    totalScans++;
                    updateStatistics();
                    document.getElementById('username').value = '';
                } else {
                    addConsoleMessage(`❌ Failed to start scan: ${data.error}`);
                }
            })
            .catch(error => {
                addConsoleMessage(`❌ Network error: ${error}`);
            });
        }
        
        function startBatchScan() {
            const batchText = document.getElementById('batch-usernames').value.trim();
            if (!batchText) {
                alert('Please enter usernames for batch scan!');
                return;
            }
            
            const usernames = batchText.split('\\n').map(u => u.trim()).filter(u => u);
            if (usernames.length === 0) {
                alert('No valid usernames found!');
                return;
            }
            
            const options = {
                cache_mining: document.getElementById('cache-mining').checked,
                osint_gathering: document.getElementById('osint-gathering').checked
            };
            
            fetch('/api/scan/batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    usernames: usernames,
                    options: options
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addConsoleMessage(`📊 Started batch scan for ${usernames.length} targets`);
                    totalScans += usernames.length;
                    updateStatistics();
                    document.getElementById('batch-usernames').value = '';
                } else {
                    addConsoleMessage(`❌ Failed to start batch scan: ${data.error}`);
                }
            })
            .catch(error => {
                addConsoleMessage(`❌ Network error: ${error}`);
            });
        }
        
        function addConsoleMessage(message) {
            const console = document.getElementById('console');
            const timestamp = new Date().toLocaleTimeString();
            const line = document.createElement('div');
            line.className = 'console-line';
            line.textContent = `[${timestamp}] ${message}`;
            console.appendChild(line);
            console.scrollTop = console.scrollHeight;
            
            // Limit console lines
            while (console.children.length > 100) {
                console.removeChild(console.firstChild);
            }
        }
        
        function clearConsole() {
            document.getElementById('console').innerHTML = '';
        }
        
        function updateActiveScan(scanData) {
            activeScans[scanData.id] = scanData;
            renderActiveScans();
        }
        
        function removeActiveScan(scanId) {
            delete activeScans[scanId];
            renderActiveScans();
        }
        
        function renderActiveScans() {
            const container = document.getElementById('active-scans');
            container.innerHTML = '';
            
            Object.values(activeScans).forEach(scan => {
                const item = document.createElement('div');
                item.className = 'scan-item';
                
                const statusClass = `status-${scan.status}`;
                
                item.innerHTML = `
                    <div>
                        <strong>@${scan.username}</strong>
                        <div style="font-size: 12px; color: #ccc;">ID: ${scan.id.substr(0, 8)}...</div>
                    </div>
                    <div>
                        <div class="scan-status ${statusClass}">${scan.status.toUpperCase()}</div>
                        <div style="font-size: 12px; margin-top: 3px;">${scan.progress}%</div>
                    </div>
                `;
                
                container.appendChild(item);
            });
            
            updateStatistics();
        }
        
        function updateProgress(progress) {
            const progressBar = document.getElementById('progress-bar');
            progressBar.style.width = `${progress}%`;
            progressBar.textContent = `${progress}%`;
        }
        
        function updateStatistics() {
            document.getElementById('total-scans').textContent = totalScans;
            document.getElementById('successful-scans').textContent = successfulScans;
            document.getElementById('active-count').textContent = Object.keys(activeScans).length;
        }
        
        // Initial console message
        addConsoleMessage('💖 Ultimate Instagram Dashboard 2025 Ready!');
        addConsoleMessage('👻 Enter usernames and start your reconnaissance!');
    </script>
</body>
</html>'''
        
        with open(template_dir / 'dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Start the web dashboard"""
        # Create HTML template
        self.create_html_template()
        
        print(f"""
💀🔥 ULTIMATE INSTAGRAM WEB DASHBOARD 2025 🔥💀
{'='*60}

🌐 Dashboard URL: http://{host}:{port}
👻 Real-time WebSocket updates enabled
💖 Beautiful dark theme with animations
🚀 Multi-target batch scanning
📊 Advanced analytics and export

Created by: น้องจิน (chin4d0ll) ♥️
For: Educational & Security Research Only!

{'='*60}
""")
        
        # Start the web server
        self.socketio.run(self.app, host=host, port=port, debug=debug)

def main():
    """Main function"""
    try:
        dashboard = UltimateWebDashboard()
        dashboard.run(host='0.0.0.0', port=5002, debug=False)
    except Exception as e:
        print(f"❌ Dashboard Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
