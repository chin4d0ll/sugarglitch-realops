#!/usr/bin/env python3
"""
🌸 INSTANT VENV ACTIVATOR 🌸
============================

A super-fast virtual environment activator that just checks 
and activates without installing requirements to avoid hanging.

Features:
- Instant detection
- No requirements installation 
- Pure speed ⚡
"""

import functools
import os
import platform
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple


class InstantVenvActivator:
    """Instant Virtual Environment Activator - Speed focused"""

    PROJECT_INDICATORS = {
        "requirements.txt": 10,
        "pyproject.toml": 9,
        "setup.py": 8,
        "main.py": 3,
        "app.py": 3,
    }

    VENV_NAMES = [".venv", "venv", "env", "virtualenv"]

    def __init__(self, project_path: Optional[str] = None):
        self.project_path = Path(project_path or os.getcwd()).resolve()
        self.is_windows = platform.system() == "Windows"

        print("⚡ Instant Venv Activator - SPEED MODE")
        print(f"📁 Project: {self.project_path}")

    @functools.lru_cache(maxsize=32)
    def detect_project(self, path: str) -> Tuple[bool, int, List[str]]:
        """Fast project detection."""
        project_path = Path(path)
        score = 0
        found = []

        for indicator, points in self.PROJECT_INDICATORS.items():
            if (project_path / indicator).exists():
                score += points
                found.append(indicator)

        # Quick Python file count
        py_files = list(project_path.glob("*.py"))
        if py_files:
            score += min(len(py_files), 5)
            found.append(f"{len(py_files)} Python files")

        return score >= 3, score, found

    def verify_venv(self, venv_path: Path) -> bool:
        """Quick venv verification."""
        pyvenv_cfg = venv_path / "pyvenv.cfg"
        if not pyvenv_cfg.exists():
            return False

        if self.is_windows:
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"

        return python_exe.exists()

    def find_venv(self) -> Optional[Path]:
        """Find virtual environment quickly."""
        # Check current directory first
        for venv_name in self.VENV_NAMES:
            venv_path = self.project_path / venv_name
            if venv_path.exists() and self.verify_venv(venv_path):
                return venv_path
        return None

    def get_activation_info(self, venv_path: Path) -> Tuple[str, Optional[Path]]:
        """Get activation command and python executable."""
        if self.is_windows:
            activate_cmd = f'"{venv_path / "Scripts" / "activate.bat"}"'
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            activate_cmd = f"source {venv_path / 'bin' / 'activate'}"
            python_exe = venv_path / "bin" / "python"

        python_exe = python_exe if python_exe.exists() else None
        return activate_cmd, python_exe

    def run(self) -> bool:
        """Run instant activation check."""
        start_time = time.time()

        print()
        print("⚡ INSTANT VENV ACTIVATOR ⚡")
        print("=" * 30)

        # Fast project detection
        is_project, score, indicators = self.detect_project(
            str(self.project_path))
        print(
            f"📋 Project: {'✅ Detected' if is_project else '❌ Not detected'} (score: {score})")

        # Find venv
        venv_path = self.find_venv()

        if venv_path:
            print(f"🔍 Venv: ✅ Found at {venv_path}")

            # Get activation info
            activate_cmd, python_exe = self.get_activation_info(venv_path)

            elapsed = time.time() - start_time

            print()
            print("🎉 INSTANT ACTIVATION READY! 🎉")
            print("=" * 35)
            print(f"⚡ Time: {elapsed:.3f}s (INSTANT!)")
            print(f"📁 Venv: {venv_path}")
            print(f"🐍 Python: {python_exe}")
            print()
            print("🔧 ACTIVATION COMMANDS:")
            print(f"   {activate_cmd}")
            print(f"   {python_exe} your_script.py")
            print()
            print("🚀 Ready to hack immediately!")

            return True
        else:
            print("🔍 Venv: ❌ Not found")
            print()
            print("💡 To create venv:")
            print(f"   python -m venv {self.project_path}/.venv")
            print(f"   source {self.project_path}/.venv/bin/activate")

            return False


def main():
    """Main function."""
    try:
        activator = InstantVenvActivator()
        success = activator.run()
        return 0 if success else 1
    except Exception as e:
        print(f"💥 Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
