#!/usr/bin/env python3
"""
🧪 Beautiful Soup และ Dependencies Test
"""

def test_beautifulsoup():
    print("🧪 Testing BeautifulSoup...")
    try:
        from bs4 import BeautifulSoup
        
        # ทดสอบการใช้งานพื้นฐาน
        html = "<html><body><h1>Test</h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1').text
        
        print(f"✅ BeautifulSoup works: {title}")
        return True
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ BeautifulSoup test failed: {e}")
        return False

def test_all_dependencies():
    print("📦 Testing All Dependencies...")
    
    dependencies = {
        'paramiko': 'SSH connections',
        'requests': 'HTTP requests', 
        'bs4': 'Web scraping (BeautifulSoup)',
        'cryptography': 'Encryption/decryption',
        'numpy': 'Numerical computing',
        'pandas': 'Data analysis',
        'base64': 'Base64 encoding/decoding',
        'hashlib': 'Hash functions',
        'json': 'JSON handling',
        'time': 'Time operations',
        'sys': 'System operations',
        'os': 'Operating system interface'
    }
    
    passed = 0
    total = len(dependencies)
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
            passed += 1
        except ImportError:
            print(f"❌ {package:15} - MISSING - {description}")
    
    print(f"\n📊 Dependencies Status: {passed}/{total} ({passed/total*100:.1f}%)")
    return passed == total

if __name__ == "__main__":
    print("🔥🔥🔥 DEPENDENCY VERIFICATION 🔥🔥🔥")
    
    bs4_ok = test_beautifulsoup()
    deps_ok = test_all_dependencies()
    
    if bs4_ok and deps_ok:
        print("\n🎉 ALL DEPENDENCIES OK!")
    else:
        print(f"\n⚠️ Some dependencies missing")
