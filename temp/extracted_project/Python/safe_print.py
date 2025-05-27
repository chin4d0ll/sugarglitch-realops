#!/usr/bin/env python3
"""
Safe Print Function for Instagram Bypass
ฟังก์ชัน print ที่ปลอดภัยจาก BrokenPipeError
"""

import sys

def safe_print(*args, **kwargs):
    """Print function ที่ปลอดภัยจาก BrokenPipeError"""
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except BrokenPipeError:
        # Ignore broken pipe errors silently
        sys.stderr = open('/dev/null', 'w')
        sys.stdout = open('/dev/null', 'w')
    except Exception:
        # Ignore any other print-related errors
        pass

# Replace built-in print with safe_print globally
print = safe_print
