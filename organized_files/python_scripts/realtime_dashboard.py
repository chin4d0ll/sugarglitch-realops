#!/usr/bin/env python3
"""
Real-time Monitoring Dashboard for sugarglitch-realops
Web-based dashboard for monitoring extraction activities
"""

import sqlite3
import json
import datetime
from flask import Flask, render_template, jsonify, request
from typing import Dict, List
import threading
import time

app = Flask(__name__)

class RealTimeMonitor:
    def __init__(self, db_path: str = "project_realops.db"):
        self.db_path = db_path
        self.active_sessions = {}
        self.monitoring = True
        
    def get_live_stats(self) -> Dict:
        """Get current system statistics"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Recent activity (last hour)
        cursor = conn.execute("""
            SELECT COUNT(*) as count FROM extracted_data 
            WHERE extraction_date >= datetime('now', '-1 hour')
        """)
        recent_extractions = cursor.fetchone()['count']
        
        cursor = conn.execute("""
            SELECT COUNT(*) as count FROM proxy_sessions 
            WHERE start_time >= datetime('now', '-1 hour')
        """)
        recent_sessions = cursor.fetchone()['count']
        
        cursor = conn.execute("""
            SELECT COUNT(*) as count FROM cookie_harvests 
            WHERE harvest_timestamp >= datetime('now', '-1 hour')
        """)
        recent_harvests = cursor.fetchone()['count']
        
        # Success rates
        cursor = conn.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
            FROM extracted_data 
            WHERE extraction_date >= datetime('now', '-24 hours')
        """)
        extraction_stats = cursor.fetchone()
        extraction_success_rate = (extraction_stats['successful'] / max(extraction_stats['total'], 1)) * 100
        
        # Active targets
        cursor = conn.execute("""
            SELECT COUNT(*) as count FROM targets 
            WHERE status = 'active'
        """)
        active_targets = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'recent_activity': {
                'extractions': recent_extractions,
                'proxy_sessions': recent_sessions,
                'cookie_harvests': recent_harvests
            },
            'success_rates': {
                'extraction_rate': round(extraction_success_rate, 2)
            },
            'active_targets': active_targets,
            'system_status': 'operational'
        }
    
    def get_activity_timeline(self, hours: int = 24) -> List[Dict]:
        """Get timeline of activities"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=hours)
        
        # Combine different activities into timeline
        activities = []
        
        # Extractions
        cursor = conn.execute("""
            SELECT 
                'extraction' as type,
                extraction_date as timestamp,
                success,
                target_id,
                data_size
            FROM extracted_data 
            WHERE extraction_date >= ?
            ORDER BY extraction_date DESC
            LIMIT 50
        """, (cutoff.isoformat(),))
        
        for row in cursor.fetchall():
            activities.append({
                'type': 'extraction',
                'timestamp': row['timestamp'],
                'success': bool(row['success']),
                'details': f"Target {row['target_id']}, {row['data_size']} bytes"
            })
        
        # Proxy sessions
        cursor = conn.execute("""
            SELECT 
                'proxy_session' as type,
                start_time as timestamp,
                success_rate,
                requests_made
            FROM proxy_sessions 
            WHERE start_time >= ?
            ORDER BY start_time DESC
            LIMIT 50
        """, (cutoff.isoformat(),))
        
        for row in cursor.fetchall():
            activities.append({
                'type': 'proxy_session',
                'timestamp': row['timestamp'],
                'success': row['success_rate'] > 70,
                'details': f"{row['requests_made']} requests, {row['success_rate']}% success"
            })
        
        conn.close()
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return activities[:30]  # Return last 30 activities

# Flask Routes
@app.route('/')
def dashboard():
    """Main dashboard page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RealOps Monitor Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
            .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stat-number { font-size: 2em; font-weight: bold; color: #3498db; }
            .stat-label { color: #7f8c8d; font-size: 0.9em; }
            .activity-feed { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .activity-item { padding: 10px; border-left: 4px solid #3498db; margin-bottom: 10px; background: #f8f9fa; }
            .success { border-left-color: #27ae60; }
            .failure { border-left-color: #e74c3c; }
            .timestamp { font-size: 0.8em; color: #7f8c8d; }
            .refresh-btn { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
            .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
            .status-operational { background: #27ae60; }
            .status-warning { background: #f39c12; }
            .status-error { background: #e74c3c; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 RealOps Monitor Dashboard</h1>
                <p>Real-time monitoring for sugarglitch-realops project</p>
                <button class="refresh-btn" onclick="refreshData()">🔄 Refresh</button>
            </div>
            
            <div class="stats-grid" id="stats-grid">
                <!-- Stats will be populated by JavaScript -->
            </div>
            
            <div class="activity-feed">
                <h3>📊 Recent Activity</h3>
                <div id="activity-timeline">
                    <!-- Timeline will be populated by JavaScript -->
                </div>
            </div>
        </div>
        
        <script>
            function refreshData() {
                // Get live stats
                fetch('/api/stats')
                    .then(response => response.json())
                    .then(data => updateStats(data));
                
                // Get activity timeline
                fetch('/api/timeline')
                    .then(response => response.json())
                    .then(data => updateTimeline(data));
            }
            
            function updateStats(stats) {
                const grid = document.getElementById('stats-grid');
                grid.innerHTML = `
                    <div class="stat-card">
                        <div class="stat-number">${stats.recent_activity.extractions}</div>
                        <div class="stat-label">Recent Extractions (1h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.recent_activity.proxy_sessions}</div>
                        <div class="stat-label">Proxy Sessions (1h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.recent_activity.cookie_harvests}</div>
                        <div class="stat-label">Cookie Harvests (1h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.success_rates.extraction_rate}%</div>
                        <div class="stat-label">Success Rate (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.active_targets}</div>
                        <div class="stat-label">Active Targets</div>
                    </div>
                    <div class="stat-card">
                        <span class="status-indicator status-operational"></span>
                        <div class="stat-label">System Status: ${stats.system_status}</div>
                    </div>
                `;
            }
            
            function updateTimeline(activities) {
                const timeline = document.getElementById('activity-timeline');
                timeline.innerHTML = activities.map(activity => `
                    <div class="activity-item ${activity.success ? 'success' : 'failure'}">
                        <strong>${activity.type.replace('_', ' ').toUpperCase()}</strong>
                        <div>${activity.details}</div>
                        <div class="timestamp">${new Date(activity.timestamp).toLocaleString()}</div>
                    </div>
                `).join('');
            }
            
            // Auto-refresh every 30 seconds
            setInterval(refreshData, 30000);
            
            // Initial load
            refreshData();
        </script>
    </body>
    </html>
    """

@app.route('/api/stats')
def api_stats():
    """API endpoint for live statistics"""
    monitor = RealTimeMonitor()
    return jsonify(monitor.get_live_stats())

@app.route('/api/timeline')
def api_timeline():
    """API endpoint for activity timeline"""
    monitor = RealTimeMonitor()
    hours = request.args.get('hours', 24, type=int)
    return jsonify(monitor.get_activity_timeline(hours))

def start_dashboard(host='0.0.0.0', port=5000, debug=False):
    """Start the dashboard server"""
    print(f"🌐 Starting RealOps Monitor Dashboard at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    start_dashboard(debug=True)
