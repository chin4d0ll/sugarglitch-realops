#!/usr/bin/env python3
"""
🌸 ULTIMATE PYTHON VENV AUTO-ACTIVATOR 🌸
===========================================

A high-performance, secure, and beginner-friendly Python virtual environment
auto-activator with advanced features for project detection and management.

Author: SugarGlitch RealOps Team
Date: June 19, 2025
Version: 1.0.0

Features:
- Auto-detect Python projects
- Find and activate existing venv
- Create new venv if needed
- Cross-platform support
- Memory efficient caching
- Security validation
- Performance optimized
- Hacking-grade speed ⚡
"""

import asyncio
import functools
import hashlib
import os
import platform
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union


class UltimateVenvActivator:
    """
    🚀 Ultimate Python Virtual Environment Auto-Activator

    This class provides high-performance virtual environment detection,
    creation, and activation with advanced security features and
    cross-platform compatibility.
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
        "python-env",
        "py-env"
    ]

    # Security: Maximum path depth to prevent infinite loops
    MAX_SEARCH_DEPTH = 5

    def __init__(self, project_path: Optional[Union[str, Path]] = None,
                 max_workers: int = 4):
        """
            Initialize the Ultimate Venv Activator.

            Args:
                project_path: Path to search for Python projects 
                             (default: current dir)
                max_workers: Number of threads for parallel operations
            """
        self.project_path = Path(project_path or os.getcwd()).resolve()
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        # Performance caches
        self._project_cache: Dict[str, bool] = {}
        self._venv_cache: Dict[str, Optional[Path]] = {}
        self._security_cache: Set[str] = set()

        # Platform detection
        self.is_windows = platform.system() == "Windows"
        self.is_mac = platform.system() == "Darwin"
        self.is_linux = platform.system() == "Linux"

        # Timing statistics
        self.stats = {
            "project_detection_time": 0.0,
            "venv_search_time": 0.0,
            "creation_time": 0.0,
            "activation_time": 0.0
        }

        print("🚀 Ultimate Venv Activator initialized")
        print(f"📁 Project path: {self.project_path}")
        print(f"💻 Platform: {platform.system()} {platform.release()}")
        print(f"🧵 Max workers: {max_workers}")

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
            cache_key = self._get_cache_key(resolved_path)

            if cache_key in self._security_cache:
                return True

            # Check for path injection attacks
            if ".." in str(path) or str(path).startswith("/"):
                if not str(resolved_path).startswith(str(self.project_path)):
                    return False

            # Check if path exists and is accessible
            if resolved_path.exists() and os.access(resolved_path, os.R_OK):
                self._security_cache.add(cache_key)
                return True

            return False

        except (OSError, ValueError, PermissionError):
            return False

    @functools.lru_cache(maxsize=256)
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

        cache_key = self._get_cache_key(project_path)
        if cache_key in self._project_cache:
            # Return cached result with indicators
            return self._project_cache[cache_key], 10, ["cached"]

        score = 0
        found_indicators = []

        try:
            # Check for project indicators
            for indicator, points in self.PROJECT_INDICATORS.items():
                indicator_path = project_path / indicator
                if indicator_path.exists() and self._validate_path(indicator_path):
                    score += points
                    found_indicators.append(indicator)

            # Bonus points for Python files
            python_files = list(project_path.glob("*.py"))
            if python_files:
                score += min(len(python_files), 5)  # Max 5 bonus points
                found_indicators.append(f"{len(python_files)} Python files")

            # Check for common Python directories
            python_dirs = ["src", "lib", "tests", "test"]
            for dir_name in python_dirs:
                if (project_path / dir_name).exists():
                    score += 1
                    found_indicators.append(f"{dir_name}/ directory")

            is_project = score >= 3  # Minimum threshold
            self._project_cache[cache_key] = is_project

            return is_project, score, found_indicators

        except (PermissionError, OSError) as e:
            print(f"⚠️  Permission denied accessing {project_path}: {e}")
            return False, 0, []

    async def find_venv_async(self, search_path: Path) -> Optional[Path]:
        """
        Asynchronously find virtual environment in the given path.

        Args:
            search_path: Path to search for venv

        Returns:
            Optional[Path]: Path to venv if found, None otherwise
        """
        def _search_venv():
            for venv_name in self.VENV_NAMES:
                venv_path = search_path / venv_name
                if venv_path.exists() and self._validate_path(venv_path):
                    # Verify it's a valid venv
                    if self._verify_venv(venv_path):
                        return venv_path
            return None

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, _search_venv)

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

            # Check for Python executable (including symlinks)
            if self.is_windows:
                python_exe = venv_path / "Scripts" / "python.exe"
            else:
                python_exe = venv_path / "bin" / "python"

            # Accept both real files and valid symlinks
            if python_exe.exists():
                if python_exe.is_symlink():
                    # Check if symlink target exists
                    try:
                        target = python_exe.resolve()
                        return target.exists()
                    except (OSError, RuntimeError):
                        return False
                else:
                    # Check if it's a real file
                    return self._validate_path(python_exe)

            return False

        except (OSError, PermissionError):
            return False

    async def search_for_venv(self, max_depth: Optional[int] = None) -> Optional[Path]:
        """
        Search for virtual environment in project and parent directories.

        Args:
            max_depth: Maximum search depth (default: MAX_SEARCH_DEPTH)

        Returns:
            Optional[Path]: Path to found venv or None
        """
        start_time = time.time()
        max_depth = max_depth or self.MAX_SEARCH_DEPTH

        cache_key = self._get_cache_key(self.project_path)
        if cache_key in self._venv_cache:
            return self._venv_cache[cache_key]

        current_path = self.project_path
        search_tasks = []

        print(f"🔍 Searching for virtual environment...")

        # Search current directory and parents
        for depth in range(max_depth):
            print(f"   📂 Checking: {current_path} (depth: {depth})")

            # Add async search task
            task = self.find_venv_async(current_path)
            search_tasks.append(task)

            # Move to parent directory
            parent = current_path.parent
            if parent == current_path:  # Reached root
                break
            current_path = parent

        # Wait for all search tasks
        results = await asyncio.gather(*search_tasks, return_exceptions=True)

        # Find first valid result
        for result in results:
            if isinstance(result, Path):
                self._venv_cache[cache_key] = result
                self.stats["venv_search_time"] = time.time() - start_time
                print(f"✅ Found venv: {result}")
                return result

        self._venv_cache[cache_key] = None
        self.stats["venv_search_time"] = time.time() - start_time
        print("❌ No virtual environment found")
        return None

    async def create_venv(self, venv_name: str = ".venv") -> Optional[Path]:
        """
        Create a new virtual environment.

        Args:
            venv_name: Name of the venv directory

        Returns:
            Optional[Path]: Path to created venv or None if failed
        """
        start_time = time.time()
        venv_path = self.project_path / venv_name

        if venv_path.exists():
            if self._verify_venv(venv_path):
                print(f"✅ Virtual environment already exists: {venv_path}")
                return venv_path
            else:
                print(f"🗑️  Removing invalid venv: {venv_path}")
                shutil.rmtree(venv_path)

        print(f"🔨 Creating virtual environment: {venv_path}")

        try:
            # Create venv command
            cmd = [sys.executable, "-m", "venv", str(venv_path)]

            # Run subprocess asynchronously
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_path
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                if self._verify_venv(venv_path):
                    self.stats["creation_time"] = time.time() - start_time
                    print(f"✅ Virtual environment created successfully!")
                    return venv_path
                else:
                    print(f"❌ Created venv is invalid: {venv_path}")
                    return None
            else:
                print(f"❌ Failed to create venv: {stderr.decode()}")
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
            return f"source {activate_script}" def get_python_executable(self, venv_path: Path) -> Optional[Path]:
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

        # Check if executable exists (including symlinks)
        if python_exe.exists():
            if python_exe.is_symlink():
                try:
                    # Resolve symlink and check if target exists
                    target = python_exe.resolve()
                    if target.exists():
                        return python_exe  # Return the symlink path
                except (OSError, RuntimeError):
                    pass
            elif self._validate_path(python_exe):
                return python_exe

        return None

    async def install_requirements(self, venv_path: Path) -> bool:
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

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_path
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                print("✅ Requirements installed successfully!")
                return True
            else:
                print(f"❌ Failed to install requirements: {stderr.decode()}")
                return False

        except Exception as e:
            print(f"❌ Error installing requirements: {e}")
            return False

    async def run(self) -> Tuple[bool, Optional[Path]]:
        """
        Run the complete venv activation process.

        Returns:
            Tuple[bool, Optional[Path]]: (success, venv_path)
        """
        total_start = time.time()

        print(f"\n🌸 ULTIMATE VENV ACTIVATOR STARTING 🌸")
        print(f"{'='*50}")

        # Step 1: Detect Python project
        print(f"\n📋 Step 1: Project Detection")
        detect_start = time.time()

        is_project, score, indicators = self.detect_project(
            str(self.project_path))
        self.stats["project_detection_time"] = time.time() - detect_start

        if is_project:
            print(f"✅ Python project detected (score: {score})")
            print(f"   📄 Indicators: {', '.join(indicators)}")
        else:
            print(f"⚠️  No Python project detected (score: {score})")
            print(
                f"   📄 Found: {', '.join(indicators) if indicators else 'none'}")

        # Step 2: Search for existing venv
        print(f"\n🔍 Step 2: Virtual Environment Search")
        venv_path = await self.search_for_venv()

        # Step 3: Create venv if not found
        if not venv_path:
            print(f"\n🔨 Step 3: Creating Virtual Environment")
            venv_path = await self.create_venv()
        else:
            print(f"\n✅ Step 3: Using Existing Virtual Environment")

        if not venv_path:
            print(f"\n❌ Failed to create or find virtual environment!")
            return False, None

        # Step 4: Install requirements
        print(f"\n📦 Step 4: Installing Requirements")
        await self.install_requirements(venv_path)

        # Step 5: Generate activation info
        print(f"\n🚀 Step 5: Activation Information")
        activation_cmd = self.get_activation_command(venv_path)
        python_exe = self.get_python_executable(venv_path)

        total_time = time.time() - total_start
        self.stats["activation_time"] = total_time

        # Success summary
        print(f"\n🎉 ULTIMATE VENV ACTIVATOR COMPLETED! 🎉")
        print(f"{'='*50}")
        print(f"✅ Success: Virtual environment ready!")
        print(f"📁 Venv path: {venv_path}")
        print(f"🐍 Python exe: {python_exe}")
        print(f"⚡ Total time: {total_time:.3f}s")
        print(f"\n🔧 ACTIVATION COMMANDS:")
        print(f"   Shell: {activation_cmd}")
        print(f"   Direct: {python_exe} your_script.py")

        # Performance statistics
        print(f"\n📊 PERFORMANCE STATISTICS:")
        for stat_name, stat_time in self.stats.items():
            print(f"   {stat_name.replace('_', ' ').title()}: {stat_time:.3f}s")

        return True, venv_path


async def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="🌸 Ultimate Python Venv Auto-Activator 🌸"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project path to activate venv for (default: current directory)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of worker threads (default: 4)"
    )
    parser.add_argument(
        "--create-only",
        action="store_true",
        help="Only create venv, don't search for existing"
    )

    args = parser.parse_args()

    # Initialize activator
    activator = UltimateVenvActivator(
        project_path=args.path,
        max_workers=args.workers
    )

    # Run activation process
    success, venv_path = await activator.run()

    if success:
        print(f"\n🚀 Ready to hack! Use the activation commands above.")
        sys.exit(0)
    else:
        print(f"\n💥 Activation failed! Check errors above.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n⚠️  Interrupted by user. Goodbye! 👋")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
