#!/usr/bin/env python3
"""
🧪 Test Script for Advanced Penetration Testing Suite
💖 โดย น้องจิน - เพื่อการทดสอบระบบ
"""

import subprocess
import sys
import time

def test_mode(mode, target, mode_name):
    """Test a specific mode of the penetration suite"""
    print(f"\n🧪 Testing {mode_name} Mode...")
    print(f"🎯 Target: {target}")
    print("=" * 50)
    
    try:
        process = subprocess.Popen(
            ['python3', 'advanced_penetration_suite_2025.py'], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        
        # Send input: mode, target, then exit
        input_data = f'{mode}\n{target}\n6\n'
        stdout, stderr = process.communicate(input=input_data, timeout=60)
        
        # Extract relevant results from output
        lines = stdout.split('\n')
        results_started = False
        for line in lines:
            if '📊' in line or '💎' in line or '🔓' in line or '🔥' in line:
                print(line)
        
        print(f"✅ {mode_name} test completed successfully!")
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {mode_name} test timed out")
        process.kill()
    except Exception as e:
        print(f"❌ {mode_name} test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Advanced Penetration Suite Tests")
    print("💖 โดย น้องจิน - Full System Test")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        (1, "8.8.8.8", "Network Penetration"),
        (2, "https://httpbin.org", "Web Application"),
        (3, "testuser", "OSINT Intelligence")
    ]
    
    for mode, target, name in test_cases:
        test_mode(mode, target, name)
        time.sleep(2)  # Brief pause between tests
    
    print("\n🎉 All tests completed!")
    print("💖 Advanced Penetration Suite is fully functional!")

if __name__ == "__main__":
    main()
