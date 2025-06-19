#!/usr/bin/env python3
import json
import os
print("🔥 VENV ACTIVATED & READY FOR ATTACK!")
print("=" * 50)

print("✅ Python imports working")

# Check workspace
workspace = "/workspaces/sugarglitch-realops"
print(f"📂 Workspace: {workspace}")

# Check key files
files = [
    "deep_personal_passwords.txt",
    "deep_osint_report_20250619_200222.json"
]

for f in files:
    path = os.path.join(workspace, f)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"✅ {f}: {size} bytes")
    else:
        print(f"❌ {f}: Missing")

# Load passwords
try:
    with open(os.path.join(workspace, "deep_personal_passwords.txt")) as f:
        passwords = [line.strip() for line in f if line.strip()
                     and not line.startswith('#')]
    print(f"✅ Loaded {len(passwords)} passwords")
    print(f"   Top 5: {passwords[:5]}")
except Exception as e:
    print(f"❌ Password loading error: {e}")

print("🚀 SYSTEM STATUS: READY FOR REAL ATTACKS!")
print("=" * 50)
