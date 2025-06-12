#!/usr/bin/env python3

"""
SugarGlitch RealOps - Main Entry Point
Production-ready organized structure
"""

import sys
from pathlib import Path

# Add core directory to Python path
core_dir = Path(__file__).parent / "core"
sys.path.insert(0, str(core_dir))

if __name__ == "__main__":
    try:
        # Import the main application from core
        from main import main
        main()
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("🔧 Please run: cd core && python main.py")
        print("📁 Or check the organized project structure")
        sys.exit(1)
