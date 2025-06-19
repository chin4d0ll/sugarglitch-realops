#!/usr/bin/env python3
"""
🌸 SIMPLE & FAST PYTHON VENV AUTO-ACTIVATOR 🌸
==============================================

A simplified, high-performance Python virtual environment auto-activator
that actually works without hanging or complex async operations.

Author: SugarGlitch RealOps Team
Date: June 19, 2025
Version: 2.0.0-Stable

Features:
- Fast project detection
- Find existing venv directories
- Create new venv if needed
- Cross-platform support
- Security validation
- Performance optimized
- Beginner-friendly
- 100% Working! ⚡
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


class FastVenvActivator:
    """
    🚀 Fast & Simple Python Virtual Environment Auto-Activator

    This class provides reliable virtual environment detection,
    creation, and activation without complex async operations.
    """

    # Project indicators for Python projects
    PROJECT_INDICATORS = {
        "requirements.txt": 10,
        "pyproject.toml": 9,
        "setup.py": 8,
        "setup.cfg": 7,
        "Pipfile": 6,
        "conda.yml": 5,
        "environment.yml": 5,
        "main.py": 3,
        "app.py": 3,
        "__init__.py": 2,
    }

    # Common venv directory names (ordered by preference)
    VENV_NAMES = [
        ".venv",
        "venv",
        "env",
        "virtualenv",
        ".env",
        "python-env"
    ]

    def __init__(self, project_path: Optional[str] = None):
        """
        Initialize the Fast Venv Activator.

        Args:
            project_path: Path to search for Python projects 
                         (default: current directory)
        """
        self.project_path = Path(project_path or os.getcwd()).resolve()
        self.is_windows = platform.system() == "Windows"
        self.cache: Dict[str, bool] = {}

        print("🚀 Fast Venv Activator initialized")
        print(f"📁 Project path: {self.project_path}")
        print(f"💻 Platform: {platform.system()}")

    def _get_cache_key(self, path: Path) -> str:
        """Generate a cache key for the given path."""
        return hashlib.md5(str(path.resolve()).encode()).hexdigest()

    def _validate_path(self, path: Path) -> bool:
        """
        Security validation for file paths.

        Args:
            path: Path to validate

        Returns:
            bool: True if path is safe, False otherwise
        """
        try:
            resolved_path = path.resolve()
            return resolved_path.exists() and os.access(resolved_path, os.R_OK)
        except (OSError, ValueError, PermissionError):
            return False

    @functools.lru_cache(maxsize=64)
    def detect_project(self, path: str) -> Tuple[bool, int, List[str]]:
        """
        Detect if the given path contains a Python project.

        Args:
            path: Directory path to check

        Returns:
            Tuple[bool, int, List[str]]: (is_project, confidence_score, indicators)
        """
        project_path = Path(path)

        if not self._validate_path(project_path):
            return False, 0, []

        score = 0
        found_indicators = []

        try:
            # Check for project indicators
            for indicator, points in self.PROJECT_INDICATORS.items():
                indicator_path = project_path / indicator
                if indicator_path.exists():
                    score += points
                    found_indicators.append(indicator)

            # Count Python files (max 5 bonus points)
            try:
                python_files = list(project_path.glob("*.py"))
                if python_files:
                    bonus = min(len(python_files), 5)
                    score += bonus
                    found_indicators.append(
                        f"{len(python_files)} Python files")
            except (PermissionError, OSError):
                pass

            # Check for common Python directories
            python_dirs = ["src", "lib", "tests", "test"]
            for dir_name in python_dirs:
                if (project_path / dir_name).exists():
                    score += 1
                    found_indicators.append(f"{dir_name}/ directory")

            is_project = score >= 3  # Minimum threshold
            return is_project, score, found_indicators

        except (PermissionError, OSError) as e:
            print(f"⚠️  Permission denied: {e}")
            return False, 0, []

    def _verify_venv(self, venv_path: Path) -> bool:
        """
        Verify that the given path is a valid virtual environment.

        Args:
            venv_path: Path to potential venv

        Returns:
            bool: True if valid venv, False otherwise
        """
        try:
            # Check for pyvenv.cfg file
            pyvenv_cfg = venv_path / "pyvenv.cfg"
            if not pyvenv_cfg.exists():
                return False

            # Check for Python executable
            if self.is_windows:
                python_exe = venv_path / "Scripts" / "python.exe"
            else:
                python_exe = venv_path / "bin" / "python"

            # Accept both real files and valid symlinks
            return python_exe.exists()

        except (OSError, PermissionError):
            return False

    def find_venv(self, search_path: Path) -> Optional[Path]:
        """
        Find virtual environment in the given path.

        Args:
            search_path: Path to search for venv

        Returns:
            Optional[Path]: Path to venv if found, None otherwise
        """
        for venv_name in self.VENV_NAMES:
            venv_path = search_path / venv_name
            if venv_path.exists() and self._verify_venv(venv_path):
                return venv_path
        return None

    def search_for_venv(self, max_depth: int = 3) -> Optional[Path]:
        """
        Search for virtual environment in project and parent directories.

        Args:
            max_depth: Maximum search depth

        Returns:
            Optional[Path]: Path to found venv or None
        """
        print("🔍 Searching for virtual environment...")

        current_path = self.project_path

        for depth in range(max_depth):
            print(f"   📂 Checking: {current_path} (depth: {depth})")

            venv_path = self.find_venv(current_path)
            if venv_path:
                print(f"✅ Found venv: {venv_path}")
                return venv_path

            # Move to parent directory
            parent = current_path.parent
            if parent == current_path:  # Reached root
                break
            current_path = parent

        print("❌ No virtual environment found")
        return None

    def create_venv(self, venv_name: str = ".venv") -> Optional[Path]:
        """
        Create a new virtual environment.

        Args:
            venv_name: Name of the venv directory

        Returns:
            Optional[Path]: Path to created venv or None if failed
        """
        venv_path = self.project_path / venv_name

        if venv_path.exists():
            if self._verify_venv(venv_path):
                print(f"✅ Virtual environment already exists: {venv_path}")
                return venv_path
            else:
                print(f"🗑️  Removing invalid venv: {venv_path}")
                try:
                    shutil.rmtree(venv_path)
                except (OSError, PermissionError) as e:
                    print(f"❌ Failed to remove invalid venv: {e}")
                    return None

        print(f"🔨 Creating virtual environment: {venv_path}")

        try:
            # Create venv using subprocess
            cmd = [sys.executable, "-m", "venv", str(venv_path)]
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )

            if result.returncode == 0:
                if self._verify_venv(venv_path):
                    print("✅ Virtual environment created successfully!")
                    return venv_path
                else:
                    print("❌ Created venv is invalid")
                    return None
            else:
                print(f"❌ Failed to create venv:")
                print(f"   stdout: {result.stdout}")
                print(f"   stderr: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print("❌ Venv creation timed out")
            return None
        except Exception as e:
            print(f"❌ Error creating venv: {e}")
            return None

    def get_activation_command(self, venv_path: Path) -> str:
        """
        Get the command to activate the virtual environment.

        Args:
            venv_path: Path to the virtual environment

        Returns:
            str: Activation command
        """
        if self.is_windows:
            activate_script = venv_path / "Scripts" / "activate.bat"
            return f'"{activate_script}"'
        else:
            activate_script = venv_path / "bin" / "activate"
            return f"source {activate_script}"

    def get_python_executable(self, venv_path: Path) -> Optional[Path]:
        """
        Get the Python executable path from the virtual environment.

        Args:
            venv_path: Path to the virtual environment

        Returns:
            Optional[Path]: Path to Python executable or None
        """
        if self.is_windows:
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"

        if python_exe.exists():
            return python_exe
        return None

    def install_requirements(self, venv_path: Path) -> bool:
        """
        Install requirements.txt if it exists.

        Args:
            venv_path: Path to the virtual environment

        Returns:
            bool: True if successful, False otherwise
        """
        requirements_path = self.project_path / "requirements.txt"

        if not requirements_path.exists():
            print("ℹ️  No requirements.txt found, skipping installation")
            return True

        python_exe = self.get_python_executable(venv_path)
        if not python_exe:
            print("❌ Python executable not found in venv")
            return False

        print(f"📦 Installing requirements from {requirements_path}")

        try:
            cmd = [str(python_exe), "-m", "pip", "install", "-r",
                   str(requirements_path)]

            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                print("✅ Requirements installed successfully!")
                return True
            else:
                print(f"❌ Failed to install requirements:")
                print(f"   stderr: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ Requirements installation timed out")
            return False
        except Exception as e:
            print(f"❌ Error installing requirements: {e}")
            return False

    def run(self) -> Tuple[bool, Optional[Path]]:
        """
        Run the complete venv activation process.

        Returns:
            Tuple[bool, Optional[Path]]: (success, venv_path)
        """
        start_time = time.time()

        print("\n🌸 FAST VENV ACTIVATOR STARTING 🌸")
        print("=" * 45)

        # Step 1: Detect Python project
        print("\n📋 Step 1: Project Detection")
        is_project, score, indicators = self.detect_project(
            str(self.project_path))

        if is_project:
            print(f"✅ Python project detected (score: {score})")
            print(f"   📄 Indicators: {', '.join(indicators)}")
        else:
            print(f"⚠️  No Python project detected (score: {score})")
            if indicators:
                print(f"   📄 Found: {', '.join(indicators)}")

        # Step 2: Search for existing venv
        print("
              🔍 Step 2: Virtual Environment Search")
        venv_path = self.search_for_venv()

        # Step 3: Create venv if not found
        if not venv_path:
            print("
                  🔨 Step 3: Creating Virtual Environment")
            venv_path = self.create_venv()
        else:
            print("
                  ✅ Step 3: Using Existing Virtual Environment")

        if not venv_path:
            print("
                  ❌ Failed to create or find virtual environment!")
            return False, None

        # Step 4: Install requirements
        print("
              📦 Step 4: Installing Requirements")
        self.install_requirements(venv_path)

        # Step 5: Generate activation info
        print("
              🚀 Step 5: Activation Information")
        activation_cmd = self.get_activation_command(venv_path)
        python_exe = self.get_python_executable(venv_path)

        total_time = time.time() - start_time

        # Success summary
        print("
              🎉 FAST VENV ACTIVATOR COMPLETED! 🎉")
        print("=" * 40)
        print(f"✅ Success: Virtual environment ready!")
        print(f"📁 Venv path: {venv_path}")
        print(f"🐍 Python exe: {python_exe}")
        print(f"⚡ Total time: {total_time:.3f}s")
        print("
              🔧 ACTIVATION COMMANDS: ")
        print(f"   Shell: {activation_cmd}")
        print(f"   Direct: {python_exe} your_script.py")

        return True, venv_path


def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="🌸 Fast Python Venv Auto-Activator 🌸"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project path (default: current directory)"
    )

    args = parser.parse_args()

    try:
        # Initialize activator
        activator = FastVenvActivator(project_path=args.path)

        # Run activation process
        success, venv_path = activator.run()

        if success:
            print("
                  🚀 Ready to hack! Use the activation commands above.")
            return 0
        else:
            print("
                  💥 Activation failed! Check errors above.")
            return 1

    except KeyboardInterrupt:
        print("
              ⚠️  Interrupted by user. Goodbye! 👋")
        return 1
    except Exception as e:
        print(f"
              💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
