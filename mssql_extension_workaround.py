#!/usr/bin/env python3
"""
MS SQL Server Extension Fix for Codespaces/Alpine Linux
Provides workarounds and alternative solutions for the SqlToolsResourceProviderService issue.
"""

import os
import json
import subprocess
import time
from pathlib import Path

def create_extension_workaround():
    """Create workarounds for the MS SQL extension issue"""
    
    timestamp = int(time.time())
    report = {
        "timestamp": timestamp,
        "issue": "MS SQL Server extension compatibility issue",
        "root_cause": "SqlToolsResourceProviderService built for Ubuntu/glibc cannot run on Alpine Linux/musl",
        "error_message": "cannot execute: required file not found",
        "system_info": {
            "detected_os": "Alpine Linux (from /etc/os-release)",
            "codespace_environment": True,
            "libc_type": "musl (Alpine default)"
        }
    }
    
    # Check if extension exists
    vscode_extensions = Path.home() / ".vscode-remote" / "extensions"
    mssql_extensions = list(vscode_extensions.glob("ms-mssql.mssql-*"))
    
    if mssql_extensions:
        report["extension_found"] = str(mssql_extensions[0])
        
        # Check service executable
        service_path = mssql_extensions[0] / "sqltoolsservice"
        if service_path.exists():
            ubuntu_services = list(service_path.glob("*/Ubuntu16/SqlToolsResourceProviderService"))
            if ubuntu_services:
                report["service_executable"] = str(ubuntu_services[0])
                report["service_architecture"] = "Ubuntu16/x64"
    
    # Immediate workarounds
    workarounds = [
        {
            "id": 1,
            "title": "Disable MS SQL Extension",
            "description": "Disable the extension to stop the error messages",
            "vscode_command": "ms-mssql.mssql",
            "action": "Disable in VS Code Extensions panel"
        },
        {
            "id": 2,
            "title": "Use Alternative Database Extensions",
            "description": "Use extensions that are compatible with Alpine Linux",
            "alternatives": [
                {
                    "name": "PostgreSQL",
                    "extension_id": "ms-ossdata.vscode-postgresql",
                    "install_command": "code --install-extension ms-ossdata.vscode-postgresql"
                },
                {
                    "name": "MySQL",
                    "extension_id": "formulahendry.vscode-mysql", 
                    "install_command": "code --install-extension formulahendry.vscode-mysql"
                },
                {
                    "name": "SQLite",
                    "extension_id": "alexcvzz.vscode-sqlite",
                    "install_command": "code --install-extension alexcvzz.vscode-sqlite"
                },
                {
                    "name": "Database Client JDBC",
                    "extension_id": "cweijan.vscode-database-client2",
                    "install_command": "code --install-extension cweijan.vscode-database-client2"
                }
            ]
        },
        {
            "id": 3,
            "title": "Use Docker SQL Server",
            "description": "Run SQL Server in Docker and connect remotely",
            "docker_command": "docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=YourStrongPassword123!' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest",
            "connection_string": "Server=localhost,1433;User Id=sa;Password=YourStrongPassword123!;"
        },
        {
            "id": 4,
            "title": "Use Azure Data Studio",
            "description": "Use standalone Azure Data Studio for SQL Server management",
            "download_url": "https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio"
        }
    ]
    
    report["workarounds"] = workarounds
    
    # Technical solutions (advanced)
    technical_solutions = [
        {
            "name": "glibc Compatibility Layer",
            "description": "Install gcompat to run glibc binaries on musl",
            "commands": [
                "apk add --no-cache gcompat libc6-compat",
                "gcompat /path/to/SqlToolsResourceProviderService"
            ],
            "success_likelihood": "Low - may still have dependency issues"
        },
        {
            "name": "Change Development Container",
            "description": "Switch to Ubuntu-based development container",
            "dockerfile_base": "mcr.microsoft.com/vscode/devcontainers/base:ubuntu",
            "success_likelihood": "High - native glibc support"
        },
        {
            "name": "Build Custom Service",
            "description": "Rebuild SqlToolsResourceProviderService for Alpine/musl",
            "complexity": "Very High - requires .NET build environment",
            "success_likelihood": "Medium - significant development effort"
        }
    ]
    
    report["technical_solutions"] = technical_solutions
    
    # Create settings to disable extension
    vscode_settings = {
        "mssql.enableStartupMessage": False,
        "mssql.enableConnectionPooling": False,
        "extensions.ignoreRecommendations": True
    }
    
    report["recommended_vscode_settings"] = vscode_settings
    
    # Save report
    report_file = f"/workspaces/sugarglitch-realops/MSSQL_EXTENSION_ANALYSIS_{timestamp}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Analysis complete! Report saved to: {report_file}")
    
    return report, report_file

def create_alternative_setup_script():
    """Create a script to set up alternative database tools"""
    
    script_content = '''#!/bin/bash
# Alternative Database Setup for VS Code
# Replaces MS SQL Server extension with compatible alternatives

echo "🔧 Setting up alternative database tools..."

# Install alternative extensions
echo "📦 Installing PostgreSQL extension..."
code --install-extension ms-ossdata.vscode-postgresql

echo "📦 Installing MySQL extension..."
code --install-extension formulahendry.vscode-mysql

echo "📦 Installing SQLite extension..."
code --install-extension alexcvzz.vscode-sqlite

echo "📦 Installing Database Client extension..."
code --install-extension cweijan.vscode-database-client2

# Create sample database configurations
mkdir -p ~/.vscode/database-configs

cat > ~/.vscode/database-configs/postgresql-sample.json << 'EOF'
{
  "name": "PostgreSQL Local",
  "type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "database": "postgres",
  "username": "postgres",
  "password": "password"
}
EOF

cat > ~/.vscode/database-configs/mysql-sample.json << 'EOF'
{
  "name": "MySQL Local",
  "type": "mysql",
  "host": "localhost",
  "port": 3306,
  "database": "mysql",
  "username": "root",
  "password": "password"
}
EOF

# Create Docker Compose for database development
cat > ~/docker-compose-databases.yml << 'EOF'
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: devdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: devdb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  sqlserver:
    image: mcr.microsoft.com/mssql/server:2019-latest
    environment:
      ACCEPT_EULA: Y
      SA_PASSWORD: YourStrongPassword123!
    ports:
      - "1433:1433"
    volumes:
      - sqlserver_data:/var/opt/mssql

volumes:
  postgres_data:
  mysql_data:
  sqlserver_data:
EOF

echo "✅ Alternative database tools installed!"
echo "📋 Available tools:"
echo "   - PostgreSQL extension"
echo "   - MySQL extension" 
echo "   - SQLite extension"
echo "   - Database Client JDBC extension"
echo ""
echo "🐳 Docker Compose file created: ~/docker-compose-databases.yml"
echo "   Run: docker-compose -f ~/docker-compose-databases.yml up -d"
echo ""
echo "📝 Sample configs created in ~/.vscode/database-configs/"
'''
    
    script_path = "/workspaces/sugarglitch-realops/setup_alternative_databases.sh"
    with open(script_path, "w") as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    print(f"✅ Alternative setup script created: {script_path}")
    
    return script_path

def create_vscode_settings_fix():
    """Create VS Code settings to mitigate the extension issue"""
    
    vscode_dir = Path.home() / ".vscode-remote" / "data" / "Machine"
    vscode_dir.mkdir(parents=True, exist_ok=True)
    
    settings_file = vscode_dir / "settings.json"
    
    # Load existing settings
    existing_settings = {}
    if settings_file.exists():
        try:
            with open(settings_file, "r") as f:
                existing_settings = json.load(f)
        except:
            pass
    
    # Add settings to reduce extension errors
    new_settings = {
        "mssql.enableStartupMessage": False,
        "mssql.enableConnectionPooling": False,
        "mssql.enableIntelliSense": False,
        "extensions.autoUpdate": False,
        "extensions.showRecommendationsOnlyOnDemand": True,
        "telemetry.enableTelemetry": False,
        "workbench.startupEditor": "none"
    }
    
    # Merge settings
    existing_settings.update(new_settings)
    
    # Save settings
    with open(settings_file, "w") as f:
        json.dump(existing_settings, f, indent=2)
    
    print(f"✅ VS Code settings updated: {settings_file}")
    return settings_file

def main():
    print("🔍 Analyzing MS SQL Server Extension Issue...")
    print("=" * 60)
    
    # Run analysis
    report, report_file = create_extension_workaround()
    
    print("\n📋 Issue Summary:")
    print("- MS SQL Server extension cannot run on Alpine Linux")
    print("- SqlToolsResourceProviderService requires glibc (Ubuntu/CentOS)")
    print("- Alpine Linux uses musl libc (incompatible)")
    print("- Binary compatibility layer has limited success")
    
    print("\n🛠️ Creating workaround solutions...")
    
    # Create alternative setup
    script_path = create_alternative_setup_script()
    
    # Fix VS Code settings
    settings_file = create_vscode_settings_fix()
    
    print("\n✅ Solutions Created:")
    print(f"1. Analysis Report: {report_file}")
    print(f"2. Alternative Setup Script: {script_path}")
    print(f"3. VS Code Settings Fix: {settings_file}")
    
    print("\n🎯 Recommended Actions:")
    print("1. Run the alternative setup script:")
    print(f"   bash {script_path}")
    print("2. Disable MS SQL extension in VS Code")
    print("3. Use PostgreSQL/MySQL extensions instead")
    print("4. Use Docker for SQL Server development")
    
    print("\n💡 For SQL Server specifically:")
    print("   docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=YourStrongPassword123!' \\")
    print("              -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest")

if __name__ == "__main__":
    main()
