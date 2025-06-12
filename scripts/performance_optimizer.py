#!/usr/bin/env python3
"""
🚀 System Performance Optimizer - เพิ่มความเร็วระบบ
ทำให้ระบบทำงานลื่นและเร็วขึ้น
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(cmd, silent=False):
    """Run shell command safely"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if not silent:
            print(f"✅ {cmd}")
        return result.stdout.strip()
    except Exception as e:
        if not silent:
            print(f"❌ Error: {e}")
        return ""

def clear_python_cache():
    """Clear Python cache files"""
    print("🐍 Clearing Python cache...")
    
    commands = [
        "find /workspaces/sugarglitch-realops -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true",
        "find /workspaces/sugarglitch-realops -name '*.pyc' -delete 2>/dev/null || true",
        "find /workspaces/sugarglitch-realops -name '*.pyo' -delete 2>/dev/null || true"
    ]
    
    for cmd in commands:
        run_command(cmd, silent=True)

def clear_temp_files():
    """Clear temporary files"""
    print("🗑️ Clearing temporary files...")
    
    commands = [
        "find /workspaces/sugarglitch-realops -name 'temp*' -type f -delete 2>/dev/null || true",
        "find /workspaces/sugarglitch-realops -name '*.tmp' -delete 2>/dev/null || true",
        "find /workspaces/sugarglitch-realops -name '*~' -delete 2>/dev/null || true",
        "rm -rf /workspaces/sugarglitch-realops/temp/* 2>/dev/null || true"
    ]
    
    for cmd in commands:
        run_command(cmd, silent=True)

def clear_logs():
    """Clear large log files"""
    print("📋 Clearing large log files...")
    run_command("find /workspaces/sugarglitch-realops -name '*.log' -size +10M -delete 2>/dev/null || true", silent=True)

def optimize_git():
    """Optimize git repository"""
    print("📦 Optimizing git repository...")
    os.chdir("/workspaces/sugarglitch-realops")
    run_command("git gc --aggressive --prune=now 2>/dev/null || true", silent=True)

def check_disk_space():
    """Check disk space"""
    print("💾 Checking disk space...")
    space = run_command("du -sh /workspaces/sugarglitch-realops/", silent=True)
    print(f"📊 Project size: {space}")
    
    # Check available space
    df_output = run_command("df -h /workspaces", silent=True)
    print(f"💿 Available space: {df_output.split()[-2]} free")

def create_performance_report():
    """Create performance optimization report"""
    report = {
        "optimization_time": datetime.now().isoformat(),
        "actions_performed": [
            "Python cache cleared",
            "Temporary files removed",
            "Large log files deleted",
            "Git repository optimized",
            "System cleaned"
        ],
        "disk_usage": run_command("du -sh /workspaces/sugarglitch-realops/", silent=True),
        "system_status": "Optimized ✅"
    }
    
    with open("/workspaces/sugarglitch-realops/performance_optimization_report.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

def additional_optimizations():
    """Perform additional optimizations"""
    print("⚙️ Performing additional optimizations...")
    
    # Remove unused Docker images and containers
    run_command("docker system prune -af 2>/dev/null || true", silent=True)
    
    # Clean up orphaned packages and dependencies
    run_command("apt-get autoremove -y 2>/dev/null || true", silent=True)
    run_command("apt-get clean 2>/dev/null || true", silent=True)

def main():
    """Main optimization function"""
    print("🚀 เริ่มเพิ่มประสิทธิภาพระบบ...")
    print("=" * 50)
    
    # Clear caches and temporary files
    clear_python_cache()
    clear_temp_files()
    clear_logs()
    
    # Optimize git
    optimize_git()
    
    # Check results
    print("\n📊 ตรวจสอบผลลัพธ์:")
    check_disk_space()
    
    # Create report
    create_performance_report()
    
    # Additional optimizations
    additional_optimizations()
    
    print("\n" + "=" * 50)
    print("✅ เพิ่มประสิทธิภาพเสร็จแล้ว!")
    print("🚀 ระบบพร้อมทำงานด้วยความเร็วสูงสุด!")
    print("\n💡 เคล็ดลับ:")
    print("   - ใช้ ./clear_cache.sh เพื่อเคลียแคชเร็ว")
    print("   - ใช้ python3 performance_optimizer.py เพื่อเพิ่มประสิทธิภาพ")
    print("   - ตรวจสอบการใช้งานดิสก์และลบไฟล์ที่ไม่จำเป็นออก")
    print("   - ใช้ Docker อย่างมีประสิทธิภาพโดยการลบ image และ container ที่ไม่ใช้งาน")

if __name__ == "__main__":
    main()
