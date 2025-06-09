# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔧 VS CODE SETTINGS FIXER
ปิด linting และ error reporting ที่ไม่จำเป็น
"""

import json
import os
from pathlib import Path

def create_vscode_settings():
    """สร้าง VS Code settings ที่เหมาะสมสำหรับ hacking workspace"""

    settings = {
        # ปิด Python linting ที่เข้มงวด
        "python.linting.enabled": False,
        "python.linting.pylintEnabled": False,
        "python.linting.flake8Enabled": False,
        "python.linting.mypyEnabled": False,
        "python.linting.banditEnabled": False,
        "python.linting.prospectorEnabled": False,
        "python.linting.pydocstyleEnabled": False,
        "python.linting.pylamaEnabled": False,

        # ปิด type checking
        "python.analysis.typeCheckingMode": "off",
        "python.analysis.autoImportCompletions": False,

        # ปิด markdown linting
        "markdownlint.config": {
            "default": False
        },

        # ปิด JSON schema validation
        "json.validate.enable": False,

        # ปิด JavaScript/TypeScript checking
        "javascript.validate.enable": False,
        "typescript.validate.enable": False,

        # ปิด spell checking
        "cSpell.enabled": False,

        # Editor settings สำหรับ hacking
        "editor.formatOnSave": False,
        "editor.formatOnPaste": False,
        "editor.formatOnType": False,
        "editor.acceptSuggestionOnCommitCharacter": False,
        "editor.quickSuggestions": {
            "other": False,
            "comments": False,
            "strings": False
        },

        # ปิด Git warnings
        "git.ignoreLimitWarning": True,
        "git.ignoreSubmodules": True,

        # Performance settings
        "files.watcherExclude": {
            "**/.git/objects/**": True,
            "**/.git/subtree-cache/**": True,
            "**/node_modules/*/**": True,
            "**/.hg/store/**": True,
            "**/__pycache__/**": True,
            "**/*.pyc": True,
            "**/hijacked_sessions/**": True,
            "**/tools/__pycache__/**": True
        },

        # ปิด extension recommendations
        "extensions.ignoreRecommendations": True,
        "extensions.showRecommendationsOnlyOnDemand": True,

        # Security settings
        "security.workspace.trust.untrustedFiles": "open",
        "security.workspace.trust.enabled": False,

        # Terminal settings
        "terminal.integrated.defaultProfile.linux": "bash",
        "terminal.integrated.inheritEnv": False,

        # Python interpreter
        "python.defaultInterpreterPath": "/usr/bin/python3",

        # File associations
        "files.associations": {
            "*.py": "python",
            "*.json": "json",
            "*.md": "markdown"
        }
    }

    return settings

def main():
    print("🔧 VS CODE SETTINGS FIXER")
    print("=" * 40)

    # สร้าง .vscode directory
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    # สร้าง settings.json
    settings_file = vscode_dir / "settings.json"
    settings = create_vscode_settings()

    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)

    print(f"✅ Created: {settings_file}")

    # สร้าง launch.json สำหรับ debugging
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "justMyCode": False,
                "env": {
                    "PYTHONPATH": "${workspaceFolder}"
                }
            },
            {
                "name": "Python: DM Extractor",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/quick-dm-extractor.py",
                "console": "integratedTerminal",
                "justMyCode": False
            },
            {
                "name": "Python: Hacking Menu",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/hacking-menu.py",
                "console": "integratedTerminal",
                "justMyCode": False
            }
        ]
    }

    launch_file = vscode_dir / "launch.json"
    with open(launch_file, 'w') as f:
        json.dump(launch_config, f, indent=2)

    print(f"✅ Created: {launch_file}")

    # สร้าง extensions.json
    extensions_config = {
        "recommendations": [
            "ms-python.python",
            "ms-python.debugpy",
            "ms-vscode.vscode-json"
        ],
        "unwantedRecommendations": [
            "ms-python.pylint",
            "ms-python.flake8",
            "ms-python.mypy-type-checker",
            "davidanson.vscode-markdownlint",
            "streetsidesoftware.code-spell-checker"
        ]
    }

    extensions_file = vscode_dir / "extensions.json"
    with open(extensions_file, 'w') as f:
        json.dump(extensions_config, f, indent=2)

    print(f"✅ Created: {extensions_file}")

    print("\n🎯 SUMMARY:")
    print("✅ Disabled Python linting")
    print("✅ Disabled type checking")
    print("✅ Disabled markdown linting")
    print("✅ Disabled spell checking")
    print("✅ Optimized performance settings")
    print("✅ Added debugging configurations")

    print("\n💡 RELOAD VS CODE to apply settings!")
    print("   Command Palette → Developer: Reload Window")

if __name__ == "__main__":
    main()
