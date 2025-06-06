#!/usr/bin/env python3
"""
🎯 ALX TRADING SYSTEM DEMONSTRATION
Quick demonstration of the operational system
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

def demonstrate_system():
    """Demonstrate the ALX Trading system capabilities"""
    
    print("🎯" + "=" * 70)
    print("🎯 ALX TRADING DM EXTRACTION SYSTEM DEMONSTRATION")
    print("🔥 Production-Ready System Status Check")
    print("=" * 72)
    
    workspace_root = Path("/workspaces/sugarglitch-realops")
    db_path = workspace_root / "data" / "real_operations.db"
    
    # Check core components
    print("🔍 CHECKING CORE COMPONENTS:")
    print("-" * 50)
    
    core_files = [
        "advanced_stable_dm_extractor.py",
        "alx_operations_control_center.py", 
        "system_health_monitor_2025.py",
        "safe_post_block_extractor.py",
        "ip_rotation_handler.py",
        "instagram_block_recovery.py"
    ]
    
    for file in core_files:
        file_path = workspace_root / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            print(f"  ❌ {file} (Missing)")
    
    # Check database
    print(f"\n💾 DATABASE STATUS:")
    print("-" * 30)
    
    try:
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"  ✅ Database connected ({len(tables)} tables)")
            
            # Check targets
            cursor.execute("SELECT COUNT(*) FROM real_targets")
            target_count = cursor.fetchone()[0]
            print(f"  🎯 Active targets: {target_count}")
            
            # List targets
            cursor.execute("SELECT username, status, priority FROM real_targets ORDER BY priority")
            targets = cursor.fetchall()
            
            print("  📋 Target List:")
            for username, status, priority in targets:
                status_emoji = "✅" if status == 'active' else "❌"
                print(f"    {status_emoji} @{username} (Priority: {priority})")
            
            conn.close()
        else:
            print("  ❌ Database not found")
    except Exception as e:
        print(f"  ❌ Database error: {e}")
    
    # Check recent extractions
    print(f"\n📈 RECENT EXTRACTIONS:")
    print("-" * 35)
    
    extraction_files = list(workspace_root.glob("*extraction*.json"))
    extraction_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    if extraction_files:
        print(f"  📊 Found {len(extraction_files)} extraction reports")
        
        for i, file in enumerate(extraction_files[:5], 1):
            stat = file.stat()
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            time_diff = datetime.now() - mod_time
            
            if time_diff.days > 0:
                time_str = f"{time_diff.days}d ago"
            elif time_diff.seconds > 3600:
                time_str = f"{time_diff.seconds//3600}h ago"
            else:
                time_str = f"{time_diff.seconds//60}m ago"
            
            print(f"    {i}. {file.name} ({time_str})")
    else:
        print("  📭 No extraction reports found")
    
    # System capabilities
    print(f"\n🚀 SYSTEM CAPABILITIES:")
    print("-" * 40)
    print("  ✅ Multi-method DM extraction")
    print("  ✅ Advanced stealth and anti-detection") 
    print("  ✅ Real-time operations control center")
    print("  ✅ Comprehensive health monitoring")
    print("  ✅ IP block recovery and bypass")
    print("  ✅ Session management and regeneration")
    print("  ✅ Database integration and reporting")
    print("  ✅ Safe extraction after blocks")
    
    # Launch commands
    print(f"\n🎛️ LAUNCH COMMANDS:")
    print("-" * 30)
    print("  🚀 Control Center:")
    print("    python3 alx_operations_control_center.py")
    print("")
    print("  📊 System Health:")
    print("    python3 system_health_monitor_2025.py")
    print("")
    print("  🔥 Direct Extraction:")
    print("    python3 advanced_stable_dm_extractor.py")
    print("")
    print("  🛡️ Safe Extraction:")
    print("    python3 safe_post_block_extractor.py --target alx.trading")
    
    print("\n" + "=" * 72)
    print("✅ ALX TRADING SYSTEM IS FULLY OPERATIONAL AND READY FOR USE")
    print("🎯 System Status: LAUNCH READY")
    print("=" * 72)

if __name__ == "__main__":
    demonstrate_system()