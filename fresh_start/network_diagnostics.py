# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Network Diagnostics - ตรวจสอบและแก้ปัญหา network
"""

import subprocess
import time
import socket
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def quick_network_test():
    """ทест network connection แบบเร็ว"""
    tests = [
        ("DNS Resolution", test_dns),
        ("Local Network", test_local_network),
        ("Internet Connectivity", test_internet),
        ("Firewall Check", test_firewall)
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(test_func)
                result = future.result(timeout=5)  # 5 second timeout
                results[test_name] = result
        except TimeoutError:
            results[test_name] = "❌ TIMEOUT - Hanging detected"
        except Exception as e:
            results[test_name] = f"❌ ERROR: {e}"

    return results

def test_dns():
    """ทดสอบ DNS resolution"""
    try:
        socket.gethostbyname("google.com")
        return "✅ DNS working"
    except socket.gaierror:
        return "❌ DNS failed"

def test_local_network():
    """ทดสอบ local network"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 22))
        sock.close()
        return "✅ Local network OK" if result == 0 else "⚠️ Limited local access"
    except Exception:
        return "❌ Local network failed"

def test_internet():
    """ทดสอบ internet connectivity"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('8.8.8.8', 53))
        sock.close()
        return "✅ Internet OK" if result == 0 else "❌ No internet"
    except Exception:
        return "❌ Internet failed"

def test_firewall():
    """ตรวจสอบ firewall"""
    return "⚠️ May need manual check"

if __name__ == "__main__":
    print("🔍 Network Diagnostics Running...")
    results = quick_network_test()

    for test, result in results.items():
        print(f"{test}: {result}")