from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
RAPID FIRE TEST 💥
ทดสอบแบบเร็วและโหด
"""

import requests
import json
import time
import random
from datetime import datetime

print("""
💥⚡ RAPID FIRE INITIATED ⚡💥
============================
[MODE] MAXIMUM_SPEED
[LEVEL] ULTRA_FAST
============================
""")

def rapid_test():
    # Test 1: IP Check
    print("🔥 Phase 1: IP Check")
    try:
        response = requests.get('https://httpbin.org/ip', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Your IP: {data['origin']}")
    except Exception as e:
        print(f"❌ IP Check failed: {e}")
    
    # Test 2: Session Data
    print("\n🔥 Phase 2: Session Data")
    try:
        session_file = '/workspaces/sugarglitch-realops/extracted_project/Python/PRIVATE_BYPASS_SUCCESS_whatilove1728_20250525_234142.json'
        with open(session_file, 'r') as f:
            data = json.load(f)
        print(f"✅ Session found: {data.get('target')}")
        print(f"🆔 User ID: {data.get('ds_user_id')}")
    except Exception as e:
        print(f"❌ Session failed: {e}")
    
    # Test 3: Generate Demo Data
    print("\n🔥 Phase 3: Demo Data Generation")
    demo_data = {
        'target': 'whatilove1728',
        'timestamp': datetime.now().isoformat(),
        'mode': 'RAPID_FIRE_DEMO',
        'profile': {
            'username': 'whatilove1728',
            'full_name': 'Demo Account',
            'follower_count': random.randint(100, 1000),
            'following_count': random.randint(50, 500),
            'post_count': random.randint(10, 100),
            'biography': 'Demo account for testing'
        },
        'posts': []
    }
    
    # สร้าง demo posts
    for i in range(6):
        post = {
            'id': f'demo_post_{i}',
            'shortcode': f'DEMO{i:03d}',
            'display_url': f'https://picsum.photos/400/400?random={i}',
            'caption': f'Demo post #{i+1} - Testing purposes',
            'like_count': random.randint(10, 500),
            'comment_count': random.randint(0, 50),
            'timestamp': int(time.time()) - (i * 3600)
        }
        demo_data['posts'].append(post)
    
    # บันทึกไฟล์
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"RAPID_FIRE_DEMO_{timestamp}.json"
    filepath = f"/workspaces/sugarglitch-realops/{filename}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Demo data created: {filename}")
    
    # Test 4: Visual Test
    print("\n🔥 Phase 4: Visual Download Test")
    test_images = [
        'https://picsum.photos/300/300?random=1',
        'https://picsum.photos/300/300?random=2',
        'https://picsum.photos/300/300?random=3'
    ]
    
    import os
    os.makedirs('/workspaces/sugarglitch-realops/demo_images', exist_ok=True)
    
    for i, url in enumerate(test_images):
        try:
            print(f"📥 Downloading test image {i+1}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(f'/workspaces/sugarglitch-realops/demo_images/test_image_{i+1}.jpg', 'wb') as f:
                    f.write(response.content)
                print(f"✅ Image {i+1} downloaded")
        except Exception as e:
            print(f"❌ Image {i+1} failed: {e}")
    
    print(f"""
🎯 RAPID FIRE COMPLETE! 🎯
=========================
✅ All phases executed
📁 Demo data: {filename}
🖼️ Images: /demo_images/
⚡ Mode: MAXIMUM_SPEED
""")

if __name__ == "__main__":
    rapid_test()
