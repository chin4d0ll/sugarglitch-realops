#!/usr/bin/env python3
"""
Instagram DM Extractor - Quick Start
Get up and running in under 2 minutes
"""

import os
import json

def main():
    print("🚀 INSTAGRAM DM EXTRACTOR - QUICK START")
    print("=" * 45)
    print()
    
    print("Step 1: Get your Instagram session")
    print("- Open Instagram in browser and login")
    print("- Press F12 → Application → Cookies → instagram.com")
    print("- Copy the 'sessionid' value")
    print()
    
    sessionid = input("Paste your sessionid here: ").strip()
    
    if not sessionid:
        print("❌ No sessionid provided!")
        return
    
    # Save session
    session_data = {
        "sessionid": sessionid,
        "target": "alx.trading",
        "created": "quick_start"
    }
    
    with open("session.json", "w") as f:
        json.dump(session_data, f, indent=2)
    
    print("✅ Session saved!")
    print()
    print("Step 2: Run extraction")
    print("Choose your extraction method:")
    print("A) python3 ultimate_dm_extractor_2025.py")
    print("B) python3 hardcore_dm_extractor.py")
    print("C) python3 thai_solution.py")
    print()
    print("🎉 You're ready to extract DMs!")

if __name__ == "__main__":
    main()
