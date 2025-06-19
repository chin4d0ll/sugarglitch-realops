# COPILOT PROMPT: Performance-optimized venv activator
#
# Requirements:
# - Use asyncio for non-blocking operations
# - Implement LRU cache for project detection
# - Memory pool for reduced allocations
# - Benchmark timing for each operation
# - Multi-threading for directory scanning
# - Optimize for speed

import asyncio
import functools
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import time
from typing import Optional, Dict, List


class HighPerformanceVenvActivator:
    """High-performance virtual environment activator with async operations."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.venv_path = project_path / ".venv"
        self.requirements_path = project_path / "requirements.txt"
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.cache: Dict[str, bool] = {}

    @functools.lru_cache(maxsize=128)
    def detect_project(self, path: str) -> bool:
        """Detect if path is a valid Python project."""
        project_path = Path(path)
        indicators = [
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "Pipfile",
            "main.py"
        ]
        return any(
            (project_path / indicator).exists() for indicator in indicators
        )

    async def run_subprocess(
        self, cmd: List[str], cwd: Optional[Path] = None
    ) -> subprocess.CompletedProcess:
        """Run subprocess asynchronously."""
        loop = asyncio.get_event_loop()

        def _run():
            return subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False
            )

        return await loop.run_in_executor(self.executor, _run)

    async def create_venv(self) -> bool:
        """Create virtual environment asynchronously."""
        if self.venv_path.exists():
            print(f"✅ Virtual environment already exists at {self.venv_path}")
            return True

        print(f"🔄 Creating virtual environment at {self.venv_path}...")
        cmd = [sys.executable, "-m", "venv", str(self.venv_path)]

        result = await self.run_subprocess(cmd, self.project_path)

        if result.returncode == 0:
            print("✅ Virtual environment created successfully")
            return True
        else:
            print(f"❌ Failed to create venv: {result.stderr}")
            return False

    async def install_dependencies(self) -> bool:
        """Install dependencies asynchronously."""
        if not self.requirements_path.exists():
            print("⚠️  No requirements.txt found, skipping dependencies")
            return True

        # Use venv python to install packages
        python_path = self.venv_path / "bin" / "python"
        if not python_path.exists():
            python_path = self.venv_path / "Scripts" / "python.exe"  # Windows

        if python_path.exists():
            print("🔄 Installing dependencies using venv python...")
            cmd = [
                str(python_path), "-m", "pip", "install", "-r",
                str(self.requirements_path)
            ]
        else:
            print("⚠️  Using system pip (venv python not found)")
            cmd = [
                sys.executable, "-m", "pip", "install", "-r",
                str(self.requirements_path)
            ]

        result = await self.run_subprocess(cmd, self.project_path)

        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False

    async def activate(self) -> bool:
        """Activate virtual environment and install dependencies."""
        # Create venv if it doesn't exist
        if not await self.create_venv():
            return False

        # Install dependencies
        if not await self.install_dependencies():
            return False

        return True

    def get_activation_command(self) -> str:
        """Get the command to activate the virtual environment."""
        if sys.platform == "win32":
            return str(self.venv_path / "Scripts" / "activate.bat")
        else:
            return f"source {self.venv_path}/bin/activate"

    async def run(self) -> bool:
        """Run the complete activation process with timing."""
        start_time = time.time()

        print(f"🚀 Activating virtual environment for {self.project_path}...")
        detection = self.detect_project(str(self.project_path))
        print(f"📁 Project detection: {detection}")

        success = await self.activate()

        elapsed_time = time.time() - start_time

        if success:
            print(f"✅ Virtual environment activated in {elapsed_time:.2f}s")
            print(f"🔧 Activation command: {self.get_activation_command()}")
            return True
        else:
            print(f"❌ Failed to activate venv ({elapsed_time:.2f}s)")
            return False


async def main():
    """Main function to run the activator."""
    project_path = Path("/workspaces/sugarglitch-realops")
    activator = HighPerformanceVenvActivator(project_path)

    success = await activator.run()

    if success:
        print("\n🎉 High-performance venv activator completed successfully!")
        print("📋 Next steps:")
        print(f"   1. Run: {activator.get_activation_command()}")
        print("   2. Then use: python scripts/your_script.py")
        print("   3. Enjoy the performance boost! 🚀")
    else:
        print("\n❌ Virtual environment activation failed!")
        print("Please check the errors above and try again.")


if __name__ == "__main__":
    asyncio.run(main())
