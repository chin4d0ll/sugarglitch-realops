# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import sys
import subprocess
import os

REQUIRED_PYTHON = (3, 8)
REQUIREMENTS = "requirements.txt"
REQUIRED_PACKAGES = ["requests", "playwright", "pandas", "SQLAlchemy"]
def check_python_version():
    print(f"[1/4] Checking Python version...")
    if sys.version_info < REQUIRED_PYTHON:
        sys.exit(f"❌ Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+ required. Found: {sys.version}")
    print(f"✅ Python version OK: {sys.version.split()[0]}")
def ensure_requirements_file():
    if not os.path.exists(REQUIREMENTS):
        print(f"requirements.txt not found. Creating with required packages...")
        with open(REQUIREMENTS, "w") as f:
            for pkg in REQUIRED_PACKAGES:
                f.write(pkg + "\n")
    else:
        # Ensure all required packages are present
        with open(REQUIREMENTS, "r+") as f:
            lines = [line.strip() for line in f.readlines()]
            missing = [pkg for pkg in REQUIRED_PACKAGES if pkg not in lines]
            if missing:
                f.write("\n" + "\n".join(missing))
def install_dependencies():
    print(f"[2/4] Installing dependencies from {REQUIREMENTS} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS])
    print(f"✅ Dependencies installed.")
def install_playwright_chromium():
    print(f"[3/4] Installing Playwright Chromium browser...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    print(f"✅ Playwright Chromium installed.")
def print_summary():
    print(f"[4/4] Environment summary:")
    import requests
    try:
        from playwright.sync_api import sync_playwright
        import playwright
        playwright_version = playwright.__version__
    except Exception:
        playwright_version = "not installed"
    print(f"- Python: {sys.version.split()[0]}")
    print(f"- requests: {requests.__version__}")
    print(f"- playwright: {playwright_version}")
def main():
    check_python_version()
    ensure_requirements_file()
    install_dependencies()
    install_playwright_chromium()
    print_summary()

if __name__ == "__main__":
    main()
