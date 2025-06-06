#!/usr/bin/env python3
"""
Simple ALX.Trading Extractor - Basic extraction with session validation
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

def validate_session():
    """Validate session by testing Instagram connectivity"""
    print("🔍 Validating session...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
    })
    
    # Load session if exists
    session_file = Path("../sessions/session-alx.trading")  # Parent directory
    if not session_file.exists():
        session_file = Path("sessions/session-alx.trading")  # Current directory
    
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            if 'cookies' in session_data:
                for name, value in session_data['cookies'].items():
                    session.cookies.set(name, value, domain='.instagram.com')
                print("✅ Session cookies loaded")
        except Exception as e:
            print(f"⚠️ Session load error: {e}")
    
    # Test connectivity
    try:
        response = session.get('https://www.instagram.com/', timeout=10)
        if response.status_code == 200 and 'instagram' in response.text.lower():
            print("✅ Session validation successful")
            return session
        else:
            print("⚠️ Session validation failed")
            return session
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return session

def extract_alx_simple():
    """Simple extraction of ALX.Trading profile"""
    print("🎯 Simple ALX.Trading Extractor")
    print("=" * 40)
    
    # Validate session first
    session = validate_session()
    
    target_url = "https://www.instagram.com/alx.trading"
    
    try:
        print(f"🔍 Accessing: {target_url}")
        
        response = session.get(target_url, timeout=15, allow_redirects=True)
        
        print(f"📡 Status: HTTP {response.status_code}")
        print(f"📏 Content Size: {len(response.text):,} chars")
        
        if response.status_code == 200:
            print("✅ Access successful!")
            
            # Create data directory
            Path("../data").mkdir(exist_ok=True)
            
            # Save HTML content
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_file = f"../data/simple_alx_extraction_{timestamp}.html"
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"💾 HTML saved: {html_file}")
            
            # Try to extract JSON data
            import re
            
            result = {
                "timestamp": timestamp,
                "status_code": response.status_code,
                "url": response.url,
                "content_length": len(response.text),
                "extraction_type": "simple"
            }
            
            # Look for shared data
            json_match = re.search(r'window\._sharedData = ({.+?});', response.text)
            if json_match:
                try:
                    shared_data = json.loads(json_match.group(1))
                    result["shared_data"] = shared_data
                    print("✅ Extracted shared data")
                    
                    # Extract profile info if available
                    if 'entry_data' in shared_data:
                        entry_data = shared_data['entry_data']
                        if 'ProfilePage' in entry_data and entry_data['ProfilePage']:
                            profile_data = entry_data['ProfilePage'][0]
                            if 'graphql' in profile_data and 'user' in profile_data['graphql']:
                                user = profile_data['graphql']['user']
                                
                                print(f"\n👤 Profile Info:")
                                print(f"   Username: {user.get('username', 'N/A')}")
                                print(f"   Full Name: {user.get('full_name', 'N/A')}")
                                print(f"   Followers: {user.get('edge_followed_by', {}).get('count', 'N/A')}")
                                print(f"   Following: {user.get('edge_follow', {}).get('count', 'N/A')}")
                                print(f"   Posts: {user.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')}")
                                print(f"   Private: {user.get('is_private', 'N/A')}")
                                
                                result["profile_info"] = {
                                    "username": user.get('username'),
                                    "full_name": user.get('full_name'),
                                    "followers": user.get('edge_followed_by', {}).get('count'),
                                    "following": user.get('edge_follow', {}).get('count'),
                                    "posts": user.get('edge_owner_to_timeline_media', {}).get('count'),
                                    "is_private": user.get('is_private')
                                }
                        
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing error: {e}")
                except Exception as e:
                    print(f"⚠️ Data extraction error: {e}")
            
            # Save JSON result
            json_file = f"../data/simple_alx_extraction_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 JSON saved: {json_file}")
            
            # Content analysis
            content_lower = response.text.lower()
            analysis = {
                "contains_alx": "alx" in content_lower,
                "contains_trading": "trading" in content_lower,
                "contains_profile": "profile" in content_lower,
                "contains_user": "user" in content_lower,
                "contains_instagram": "instagram" in content_lower
            }
            
            print(f"\n📊 Content Analysis:")
            for key, value in analysis.items():
                status = "✅" if value else "❌"
                print(f"   {status} {key.replace('_', ' ').title()}")
            
            return result
            
        else:
            print(f"❌ Access failed with status: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    """Main function"""
    result = extract_alx_simple()
    
    if result:
        print("\n🎉 Simple extraction completed!")
        print(f"📊 Status: Success")
        print(f"📏 Data extracted: {result.get('content_length', 0):,} chars")
    else:
        print("\n❌ Extraction failed")

if __name__ == "__main__":
    main()
