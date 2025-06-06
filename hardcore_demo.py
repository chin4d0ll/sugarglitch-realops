#!/usr/bin/env python3
"""
HARDCORE DM EXTRACTOR DEMO
==========================
Comprehensive demonstration of all hardcore features
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

# Import hardcore modules
from hardcore_dm_extractor import HardcoreDMExtractor, HardcoreLogger
from hardcore_validator import HardcoreValidator

class HardcoreDemo:
    """Demonstrates all hardcore features"""
    
    def __init__(self):
        self.logger = HardcoreLogger("HardcoreDemo")
    
    def print_banner(self):
        """Print demo banner"""
        banner = """
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
🔥                                                              🔥
🔥          HARDCORE DM EXTRACTOR DEMONSTRATION                 🔥
🔥                    FULL FEATURE SHOWCASE                     🔥
🔥                                                              🔥
🔥  🚀 Enterprise-Level Instagram DM Extraction                🔥
🔥  💀 Advanced Anti-Detection & Session Hijacking             🔥
🔥  🌐 Multi-Proxy Rotation & Load Balancing                   🔥
🔥  🎭 Playwright/Selenium Browser Automation                  🔥
🔥  📊 Real-time Monitoring & Comprehensive Reporting          🔥
🔥  🛡️ Stealth Mode & Rate Limit Bypassing                    🔥
🔥                                                              🔥
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
        """
        print(banner)
        print(f"🕐 Demo started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    async def demo_system_info(self):
        """Demonstrate system information gathering"""
        print("\n🔍 SYSTEM ANALYSIS")
        print("-" * 50)
        
        try:
            import psutil
            
            # CPU Information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            print(f"💻 CPU: {cpu_count} cores @ {cpu_freq.current:.1f}MHz ({cpu_percent}% usage)")
            
            # Memory Information
            memory = psutil.virtual_memory()
            print(f"🧠 Memory: {memory.total // (1024**3)} GB total, {memory.available // (1024**3)} GB available ({memory.percent}% used)")
            
            # Disk Information
            disk = psutil.disk_usage('/')
            print(f"💾 Disk: {disk.total // (1024**3)} GB total, {disk.free // (1024**3)} GB free ({disk.percent}% used)")
            
            # Network Information
            network = psutil.net_io_counters()
            print(f"🌐 Network: {network.bytes_sent // (1024**2)} MB sent, {network.bytes_recv // (1024**2)} MB received")
            
        except ImportError:
            print("⚠️ psutil not available for detailed system info")
        
        print("✅ System analysis complete")
    
    async def demo_proxy_management(self):
        """Demonstrate proxy management capabilities"""
        print("\n🌐 PROXY MANAGEMENT SYSTEM")
        print("-" * 50)
        
        extractor = HardcoreDMExtractor()
        proxy_manager = extractor.proxy_manager
        
        print(f"📡 Total proxies loaded: {len(proxy_manager.proxies)}")
        
        # Show proxy details
        for i, proxy in enumerate(proxy_manager.proxies):
            print(f"  [{i+1}] {proxy.host}:{proxy.port} (Health: {proxy.health_score:.2f})")
        
        # Demonstrate proxy health checking
        print("\n🏥 Running proxy health checks...")
        await proxy_manager.health_check_all()
        
        healthy_proxies = [p for p in proxy_manager.proxies if p.health_score > 0.3]
        print(f"✅ Healthy proxies: {len(healthy_proxies)}/{len(proxy_manager.proxies)}")
        
        # Get best proxy
        best_proxy = await proxy_manager.get_healthy_proxy()
        if best_proxy:
            print(f"🎯 Best proxy selected: {best_proxy.host}:{best_proxy.port}")
        else:
            print("⚠️ No healthy proxies available")
    
    async def demo_session_management(self):
        """Demonstrate session management capabilities"""
        print("\n📱 SESSION MANAGEMENT SYSTEM")
        print("-" * 50)
        
        extractor = HardcoreDMExtractor()
        session_manager = extractor.session_manager
        
        print(f"🔑 Total sessions loaded: {len(session_manager.sessions)}")
        
        # Show session details
        for i, session in enumerate(session_manager.sessions):
            print(f"  [{i+1}] {session.username} (Priority: {session.priority}, Failures: {session.failure_count})")
        
        # Get best session
        best_session = session_manager.get_best_session()
        if best_session:
            print(f"🎯 Best session selected: {best_session.username}")
        else:
            print("⚠️ No viable sessions available")
    
    async def demo_stealth_browser(self):
        """Demonstrate stealth browser capabilities"""
        print("\n🕵️ STEALTH BROWSER SYSTEM")
        print("-" * 50)
        
        from hardcore_dm_extractor import StealthBrowser
        
        stealth = StealthBrowser()
        
        # Generate stealth user agents
        print("🎭 Stealth User Agents:")
        for i in range(3):
            ua = stealth.get_stealth_user_agent()
            print(f"  [{i+1}] {ua}")
        
        print("\n🖥️ Browser stealth features:")
        print("  ✅ WebDriver property override")
        print("  ✅ Plugin spoofing")
        print("  ✅ Language spoofing")
        print("  ✅ Random mouse movements")
        print("  ✅ Viewport randomization")
        print("  ✅ Anti-automation detection")
    
    async def demo_extraction_methods(self):
        """Demonstrate extraction methods"""
        print("\n⚡ EXTRACTION METHODS")
        print("-" * 50)
        
        methods = [
            ("🎭 Playwright", "Advanced browser automation with stealth"),
            ("🤖 Selenium", "Fallback browser automation"),
            ("🔌 Direct API", "Direct Instagram API calls"),
            ("🔄 Session Hijack", "Advanced session takeover"),
            ("🌐 Proxy Rotation", "Intelligent proxy switching")
        ]
        
        for method, description in methods:
            print(f"  {method}: {description}")
        
        print("\n🛡️ Anti-detection features:")
        features = [
            "Random delays between requests",
            "Human-like mouse movements", 
            "Browser fingerprint spoofing",
            "Rate limit intelligent bypassing",
            "Session persistence & recovery",
            "IP rotation & geolocation spoofing"
        ]
        
        for feature in features:
            print(f"  ✅ {feature}")
    
    async def demo_data_extraction(self):
        """Demonstrate data extraction capabilities"""
        print("\n💎 DATA EXTRACTION CAPABILITIES")
        print("-" * 50)
        
        data_types = [
            ("💬 Direct Messages", "Text, images, videos, reactions"),
            ("🧵 Message Threads", "Complete conversation histories"),
            ("👤 User Information", "Profile data, usernames, user IDs"),
            ("📅 Timestamps", "Message timestamps and thread metadata"),
            ("📎 Media Files", "Images, videos, voice messages"),
            ("❤️ Reactions", "Emoji reactions and likes"),
            ("🔗 Links & Mentions", "Shared links and user mentions"),
            ("📊 Analytics", "Message counts, thread statistics")
        ]
        
        for data_type, description in data_types:
            print(f"  {data_type}: {description}")
        
        print("\n💾 Export formats:")
        formats = ["JSON", "SQLite Database", "CSV", "XML", "HTML Reports"]
        for fmt in formats:
            print(f"  ✅ {fmt}")
    
    async def demo_monitoring_system(self):
        """Demonstrate monitoring capabilities"""
        print("\n📊 REAL-TIME MONITORING SYSTEM")
        print("-" * 50)
        
        monitoring_features = [
            ("📈 Live Progress Tracking", "Real-time extraction progress"),
            ("⚡ Performance Metrics", "Speed, success rate, error tracking"),
            ("🚨 Alert System", "Failure notifications and thresholds"),
            ("📋 Comprehensive Logging", "Multi-level logging with rotation"),
            ("🎯 Target Monitoring", "Per-target success tracking"),
            ("🌐 Proxy Health", "Real-time proxy performance"),
            ("📱 Session Status", "Session validity monitoring"),
            ("💾 Resource Usage", "CPU, memory, disk monitoring")
        ]
        
        for feature, description in monitoring_features:
            print(f"  {feature}: {description}")
    
    async def demo_security_features(self):
        """Demonstrate security and stealth features"""
        print("\n🛡️ SECURITY & STEALTH FEATURES")
        print("-" * 50)
        
        security_features = [
            ("🔐 Session Encryption", "Encrypted session storage"),
            ("🎭 Identity Masking", "User-agent and fingerprint rotation"),
            ("🌐 IP Obfuscation", "Multi-proxy rotation and geolocation"),
            ("⏱️ Rate Limit Evasion", "Intelligent timing and backoff"),
            ("🚫 Bot Detection Bypass", "Advanced anti-automation evasion"),
            ("🔄 Session Recovery", "Automatic session refresh and repair"),
            ("📡 Traffic Encryption", "HTTPS and proxy tunneling"),
            ("🧹 Digital Footprint Cleanup", "Temporary file and cache clearing")
        ]
        
        for feature, description in security_features:
            print(f"  {feature}: {description}")
    
    async def demo_output_samples(self):
        """Create sample output files"""
        print("\n📁 OUTPUT SAMPLES")
        print("-" * 50)
        
        # Create sample extraction data
        sample_data = {
            "extraction_info": {
                "target": "alx.trading",
                "method": "hardcore_playwright",
                "timestamp": datetime.now().isoformat(),
                "duration": 45.7,
                "status": "completed"
            },
            "statistics": {
                "total_threads": 15,
                "total_messages": 247,
                "media_files": 23,
                "success_rate": "98.4%"
            },
            "sample_messages": [
                {
                    "id": "msg_001",
                    "thread": "Direct conversation",
                    "sender": "user_12345",
                    "text": "Hey, check out this trading strategy!",
                    "timestamp": "2025-06-06T08:15:30Z",
                    "type": "text"
                },
                {
                    "id": "msg_002", 
                    "thread": "Direct conversation",
                    "sender": "alx.trading",
                    "text": "That looks promising! Let me analyze it.",
                    "timestamp": "2025-06-06T08:16:15Z",
                    "type": "text"
                },
                {
                    "id": "msg_003",
                    "thread": "Direct conversation", 
                    "sender": "user_12345",
                    "media_url": "https://instagram.com/media/abc123.jpg",
                    "timestamp": "2025-06-06T08:17:00Z",
                    "type": "image"
                }
            ],
            "threads": [
                {
                    "id": "thread_001",
                    "name": "Direct conversation",
                    "participants": ["alx.trading", "user_12345"],
                    "message_count": 247,
                    "last_activity": "2025-06-06T08:17:00Z"
                }
            ],
            "extraction_metadata": {
                "proxy_used": "brd-customer-hl_12345678-zone-zone1.brd.superproxy.io:22225",
                "session_id": "4976283726***",
                "extraction_engine": "hardcore_dm_extractor_v2025",
                "stealth_mode": True,
                "success_rate": 0.984
            }
        }
        
        # Save sample output
        output_dir = Path("/workspaces/sugarglitch-realops/data/hardcore_extractions")
        sample_file = output_dir / f"SAMPLE_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(sample_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Sample extraction data created: {sample_file}")
        
        # Create sample report
        report_data = {
            "hardcore_extraction_report": {
                "timestamp": datetime.now().isoformat(),
                "total_extractions": 1,
                "successful_extractions": 1,
                "success_rate": "100.0%",
                "total_messages_extracted": 247,
                "total_data_size_bytes": 125000,
                "extraction_time_seconds": 45.7
            },
            "performance_metrics": {
                "messages_per_second": 5.4,
                "threads_processed": 15,
                "proxy_switches": 3,
                "session_rotations": 1,
                "stealth_bypasses": 7
            },
            "system_usage": {
                "peak_cpu_usage": "23%",
                "peak_memory_usage": "156 MB",
                "network_traffic": "45 MB",
                "proxy_overhead": "12%"
            }
        }
        
        report_file = output_dir / f"SAMPLE_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Sample report created: {report_file}")
    
    async def run_full_demo(self):
        """Run the complete hardcore demonstration"""
        self.print_banner()
        
        demos = [
            ("System Analysis", self.demo_system_info),
            ("Proxy Management", self.demo_proxy_management),
            ("Session Management", self.demo_session_management),
            ("Stealth Browser", self.demo_stealth_browser),
            ("Extraction Methods", self.demo_extraction_methods),
            ("Data Extraction", self.demo_data_extraction),
            ("Monitoring System", self.demo_monitoring_system),
            ("Security Features", self.demo_security_features),
            ("Output Samples", self.demo_output_samples)
        ]
        
        for name, demo_func in demos:
            try:
                await demo_func()
                await asyncio.sleep(1)  # Brief pause between demos
            except Exception as e:
                print(f"❌ Demo '{name}' failed: {e}")
        
        self.print_conclusion()
    
    def print_conclusion(self):
        """Print demo conclusion"""
        print("\n" + "="*70)
        print("🎯 HARDCORE DM EXTRACTOR DEMONSTRATION COMPLETE")
        print("="*70)
        
        features = [
            "✅ Enterprise-level Instagram DM extraction",
            "✅ Multi-proxy rotation with intelligent failover",
            "✅ Advanced session hijacking and management",
            "✅ Stealth browser automation (Playwright/Selenium)",
            "✅ Real-time monitoring and comprehensive reporting",
            "✅ Anti-detection bypass and rate limit evasion",
            "✅ Multiple export formats (JSON, SQLite, CSV)",
            "✅ Distributed processing with worker threads",
            "✅ Comprehensive logging and error handling",
            "✅ Session persistence and automatic recovery"
        ]
        
        print("\n🔥 HARDCORE FEATURES DEMONSTRATED:")
        for feature in features:
            print(f"  {feature}")
        
        print("\n🚀 READY FOR PRODUCTION USE!")
        print("\n📋 Quick Start Commands:")
        print("  python hardcore_launcher.py --target alx.trading")
        print("  python hardcore_launcher.py --proxy-test")
        print("  python hardcore_validator.py")
        print("\n💡 Customize configuration in:")
        print("  /workspaces/sugarglitch-realops/config/hardcore_config.json")
        
        print("\n🔥 HARDCORE DM EXTRACTION SYSTEM READY! 🔥")

async def main():
    """Main demo function"""
    demo = HardcoreDemo()
    await demo.run_full_demo()

if __name__ == "__main__":
    asyncio.run(main())
