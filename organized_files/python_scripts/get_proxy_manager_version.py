#!/usr/bin/env python3

print('If you get error "ImportError: No module named requests", please install it:\n$ pip install requests')

import requests

try:
    r = requests.get('http://127.0.0.1:22999/api/last_version')
    print(r.content)
except Exception as e:
    print(f"[ERROR] {e}")
