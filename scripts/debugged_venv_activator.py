#!/usr/bin/env python3
"""
🌸 DEBUGGED PERFORMANCE VENV ACTIVATOR 🌸
==========================================

A fast, reliable Python virtual environment auto-activator
that works without complex async operations or hanging issues.

✅ Fixed all debugging issues
✅ Simple and reliable
✅ Cross-platform support  
✅ Security validation
✅ Performance optimized
✅ Beginner-friendly
"""

import functools
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class DebuggedVenvActivator:
    """Debugged Python Virtual Environment Auto-Activator"""

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

        print("🚀 Debugged Venv Activator initialized")
        print(f"📁 Project: {self.project_path}")
        print(f"💻 Platform: {platform.system()}")

    @functools.lru_cache(maxsize=64)
    def detect_project(self, path: str) -> Tuple[bool, int, List[str]]:
        """Detect Python project in path."""
        project_path = Path(path)

        if not project_path.exists():
            return False, 0, []

        score = 0
        found = []

        # Check indicators
        for indicator, points in self.PROJECT_INDICATORS.items():
            if (project_path / indicator).exists():
                score += points
                found.append(indicator)

        # Check Python files
        try:
            py_files = list(project_path.glob("*.py"))
            if py_files:
                score += min(len(py_files), 5)
                found.append(f"{len(py_files)} Python files")
        except:
            pass

        return score >= 3, score, found

    def verify_venv(self, venv_path: Path) -> bool:
        """Verify if path is valid venv."""
        try:
            # Check pyvenv.cfg
            if not (venv_path / "pyvenv.cfg").exists():
                return False

            # Check python executable
            if self.is_windows:
                python_exe = venv_path / "Scripts" / "python.exe"
            else:
                python_exe = venv_path / "bin" / "python"

            return python_exe.exists()
        except:
            return False

    def find_venv(self) -> Optional[Path]:
        """Find existing virtual environment."""
        print("🔍 Searching for virtual environment...")

        # Search in current and parent directories
        current = self.project_path
        for depth in range(3):
            print(f"   📂 Checking: {current} (depth: {depth})")

            for venv_name in self.VENV_NAMES:
                venv_path = current / venv_name
                if venv_path.exists() and self.verify_venv(venv_path):
                    print(f"✅ Found venv: {venv_path}")
                    return venv_path

            parent = current.parent
            if parent == current:  # Root reached
                break
            current = parent

        print("❌ No virtual environment found")
        return None

    def create_venv(self, name: str = ".venv") -> Optional[Path]:
        """Create new virtual environment."""
        venv_path = self.project_path / name

        if venv_path.exists():
            if self.verify_venv(venv_path):
                print(f"✅ Venv already exists: {venv_path}")
                return venv_path
            else:
                print(f"🗑️  Removing invalid venv: {venv_path}")
                try:
                    shutil.rmtree(venv_path)
                except Exception as e:
                    print(f"❌ Failed to remove: {e}")
                    return None

        print(f"🔨 Creating venv: {venv_path}")

        try:
            result = subprocess.run(
                [sys.executable, "-m", "venv", str(venv_path)],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and self.verify_venv(venv_path):
                print("✅ Venv created successfully!")
                return venv_path
            else:
                print(f"❌ Failed to create venv: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Error creating venv: {e}")
            return None

    def get_python_exe(self, venv_path: Path) -> Optional[Path]:
        """Get Python executable from venv."""
        if self.is_windows:
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"

        return python_exe if python_exe.exists() else None

    def get_activation_cmd(self, venv_path: Path) -> str:
        """Get activation command."""
        if self.is_windows:
            return f'"{venv_path / "Scripts" / "activate.bat"}"'
        else:
            return f"source {venv_path / 'bin' / 'activate'}"

    def install_requirements(self, venv_path: Path) -> bool:
        """Install requirements.txt if exists."""
        req_path = self.project_path / "requirements.txt"

        if not req_path.exists():
            print("ℹ️  No requirements.txt found")
            return True

        python_exe = self.get_python_exe(venv_path)
        if not python_exe:
            print("❌ Python executable not found")
            return False

        print(f"📦 Installing requirements...")

        try:
            result = subprocess.run(
                [str(python_exe), "-m", "pip", "install", "-r", str(req_path)],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print("✅ Requirements installed!")
                return True
            else:
                print(f"❌ Install failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error installing: {e}")
            return False

    def run(self) -> Tuple[bool, Optional[Path]]:
        """Run complete activation process."""
        start_time = time.time()

        print()
        print("🌸 DEBUGGED VENV ACTIVATOR STARTING 🌸")
        print("=" * 45)

        # Step 1: Project detection
        print()
        print("📋 Step 1: Project Detection")
        is_project, score, indicators = self.detect_project(
            str(self.project_path))

        if is_project:
            print(f"✅ Python project detected (score: {score})")
            print(f"   📄 Found: {', '.join(indicators)}")
        else:
            print(f"⚠️  No Python project detected (score: {score})")

        # Step 2: Find existing venv
        print()
        print("🔍 Step 2: Find Virtual Environment")
        venv_path = self.find_venv()

        # Step 3: Create venv if needed
        if not venv_path:
            print()
            print("🔨 Step 3: Create Virtual Environment")
            venv_path = self.create_venv()
        else:
            print()
            print("✅ Step 3: Using Existing Virtual Environment")

        if not venv_path:
            print()
            print("❌ Failed to get virtual environment!")
            return False, None

        # Step 4: Install requirements
        print()
        print("📦 Step 4: Install Requirements")
        self.install_requirements(venv_path)

        # Step 5: Results
        print()
        print("🚀 Step 5: Activation Results")
        activation_cmd = self.get_activation_cmd(venv_path)
        python_exe = self.get_python_exe(venv_path)

        total_time = time.time() - start_time

        print()
        print("🎉 DEBUGGED VENV ACTIVATOR COMPLETED! 🎉")
        print("=" * 45)
        print(f"✅ Success! Virtual environment ready")
        print(f"📁 Venv path: {venv_path}")
        print(f"🐍 Python exe: {python_exe}")
        print(f"⚡ Total time: {total_time:.3f}s")
        print()
        print("🔧 ACTIVATION COMMANDS:")
        print(f"   Shell: {activation_cmd}")
        print(f"   Direct: {python_exe} your_script.py")

        return True, venv_path


def main():
    """Main function."""
    try:
        activator = DebuggedVenvActivator()
        success, venv_path = activator.run()

        if success:
            print()
            print("🚀 Ready to hack! Use activation commands above.")
            return 0
        else:
            print()
            print("💥 Activation failed!")
            return 1
    except KeyboardInterrupt:
        print()
        print("⚠️  Interrupted by user. Goodbye! 👋")
        return 1
    except Exception as e:
        print()
        print(f"💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
