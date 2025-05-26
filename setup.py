#!/usr/bin/env python3
"""
Setup script for SugarGlitch RealOps
"""

from setuptools import setup, find_packages
import os

# Read README
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Advanced Intelligence & Session Management Platform"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="sugarglitch-realops",
    version="2.1.0",
    description="Advanced Intelligence & Session Management Platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="SugarGlitch Team",
    python_requires=">=3.8",
    packages=find_packages(include=["scripts*", "utils*"]),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "sugarglitch-setup=setup:main",
            "sugarglitch-cleanup=cleanup_workspace:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    zip_safe=False,
)
