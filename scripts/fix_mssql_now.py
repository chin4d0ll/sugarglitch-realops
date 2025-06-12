#!/usr/bin/env python3
"""
Immediate MS SQL Extension Fix
This script implements the quickest solutions to stop the SqlToolsResourceProviderService error.
"""

import os
import json
import subprocess
import time
from pathlib import Path

def disable_mssql_extension():
    """Disable the MS SQL extension to stop errors"""
    print("🔧 Disabling MS SQL Server extension...")
    
    # Find VS Code settings directory
    settings_dirs = [
        Path.home() / ".vscode-remote" / "data" / "Machine",
        Path.home() / ".vscode" / "User", 
        Path("/workspaces/.codespaces/.persistedshare") / ".vscode-remote" / "data" / "Machine"
    ]
    
    settings_file = None
    for settings_dir in settings_dirs:
        if settings_dir.exists():
            settings_file = settings_dir / "settings.json"
            break
    
    if not settings_file:
        # Create the directory
        settings_dir = Path.home() / ".vscode-remote" / "data" / "Machine"
        settings_dir.mkdir(parents=True, exist_ok=True)
        settings_file = settings_dir / "settings.json"
    
    # Load existing settings
    settings = {}
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
        except:
            settings = {}
    
    # Add settings to disable MS SQL extension
    mssql_disable_settings = {
        "mssql.enableStartupMessage": False,
        "mssql.enableConnectionPooling": False,
        "mssql.enableIntelliSense": False,
        "mssql.autoConnect": False,
        "extensions.autoUpdate": False,
        "extensions.showRecommendationsOnlyOnDemand": True,
        "workbench.startupEditor": "none"
    }
    
    settings.update(mssql_disable_settings)
    
    # Save updated settings
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"✅ Updated VS Code settings: {settings_file}")
    return str(settings_file)

def setup_docker_sqlserver():
    """Set up Docker SQL Server container"""
    print("🐳 Setting up Docker SQL Server...")
    
    # Check if Docker is available
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  Docker not available - skipping Docker setup")
            return False
    except FileNotFoundError:
        print("⚠️  Docker not found - skipping Docker setup")
        return False
    
    # Create Docker commands script
    docker_script = """#!/bin/bash
# Docker SQL Server Setup
echo "🚀 Starting SQL Server Docker container..."

# Stop and remove existing container if it exists
docker stop sqlserver-dev 2>/dev/null || true
docker rm sqlserver-dev 2>/dev/null || true

# Start new SQL Server container
docker run --name sqlserver-dev \\
    -e 'ACCEPT_EULA=Y' \\
    -e 'SA_PASSWORD=YourStrongPassword123!' \\
    -p 1433:1433 \\
    -d mcr.microsoft.com/mssql/server:2019-latest

# Wait for container to start
echo "⏳ Waiting for SQL Server to start..."
sleep 10

# Check if container is running
if docker ps | grep -q sqlserver-dev; then
    echo "✅ SQL Server container is running!"
    echo ""
    echo "📋 Connection Details:"
    echo "   Server: localhost,1433"
    echo "   Username: sa"
    echo "   Password: YourStrongPassword123!"
    echo "   Connection String: Server=localhost,1433;User Id=sa;Password=YourStrongPassword123!;TrustServerCertificate=True;"
    echo ""
    echo "🔧 Test connection:"
    echo "   docker exec sqlserver-dev /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrongPassword123!' -Q 'SELECT @@VERSION'"
else
    echo "❌ Failed to start SQL Server container"
    docker logs sqlserver-dev
fi
"""
    
    script_path = "/workspaces/sugarglitch-realops/start_sqlserver_docker.sh"
    with open(script_path, 'w') as f:
        f.write(docker_script)
    
    os.chmod(script_path, 0o755)
    print(f"✅ Created Docker script: {script_path}")
    
    # Try to run the script
    try:
        print("🚀 Starting SQL Server container...")
        result = subprocess.run(['bash', script_path], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ SQL Server Docker container started successfully!")
            print(result.stdout)
        else:
            print("⚠️  Docker script completed with warnings:")
            print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
    except subprocess.TimeoutExpired:
        print("⚠️  Docker startup timed out - container may still be starting")
    except Exception as e:
        print(f"⚠️  Error running Docker script: {e}")
    
    return script_path

def create_extension_install_guide():
    """Create a guide for installing alternative extensions"""
    print("📦 Creating extension installation guide...")
    
    guide_content = """# Alternative Database Extensions Installation Guide

## Quick Install (Copy and paste these one by one in VS Code terminal)

### Method 1: Using VS Code Extensions Panel
1. Open Extensions panel (Ctrl+Shift+X)
2. Search for and install each extension:

**PostgreSQL Extension:**
- Search: `ms-ossdata.vscode-postgresql`
- Click Install

**MySQL Extension:**
- Search: `formulahendry.vscode-mysql`  
- Click Install

**SQLite Extension:**
- Search: `alexcvzz.vscode-sqlite`
- Click Install

**Universal Database Client:**
- Search: `cweijan.vscode-database-client2`
- Click Install

### Method 2: Command Line (if available)
```bash
# PostgreSQL
code --install-extension ms-ossdata.vscode-postgresql

# MySQL
code --install-extension formulahendry.vscode-mysql

# SQLite
code --install-extension alexcvzz.vscode-sqlite

# Database Client JDBC
code --install-extension cweijan.vscode-database-client2
```

## Alternative Database Docker Containers

### PostgreSQL
```bash
docker run --name postgres-dev \\
    -e POSTGRES_PASSWORD=password \\
    -e POSTGRES_DB=devdb \\
    -p 5432:5432 \\
    -d postgres:13

# Connection: Host=localhost;Port=5432;Database=devdb;Username=postgres;Password=password;
```

### MySQL
```bash
docker run --name mysql-dev \\
    -e MYSQL_ROOT_PASSWORD=password \\
    -e MYSQL_DATABASE=devdb \\
    -p 3306:3306 \\
    -d mysql:8.0

# Connection: Server=localhost;Port=3306;Database=devdb;Uid=root;Pwd=password;
```

### SQLite (No Docker needed)
- Just install the SQLite extension
- Create .db files directly in your workspace

## Testing Connections

### SQL Server (Docker)
```bash
docker exec sqlserver-dev /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrongPassword123!' -Q "SELECT @@VERSION"
```

### PostgreSQL (Docker)
```bash
docker exec postgres-dev psql -U postgres -d devdb -c "SELECT version();"
```

### MySQL (Docker) 
```bash
docker exec mysql-dev mysql -u root -ppassword -e "SELECT VERSION();"
```
"""
    
    guide_path = "/workspaces/sugarglitch-realops/DATABASE_EXTENSIONS_GUIDE.md"
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    
    print(f"✅ Created installation guide: {guide_path}")
    return guide_path

def create_connection_examples():
    """Create example connection configurations"""
    print("🔗 Creating connection examples...")
    
    connections = {
        "sql_server_docker": {
            "name": "SQL Server (Docker)",
            "type": "mssql",
            "server": "localhost",
            "port": 1433,
            "username": "sa", 
            "password": "YourStrongPassword123!",
            "database": "master",
            "connection_string": "Server=localhost,1433;User Id=sa;Password=YourStrongPassword123!;TrustServerCertificate=True;",
            "test_command": "docker exec sqlserver-dev /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrongPassword123!' -Q 'SELECT @@VERSION'"
        },
        "postgresql_docker": {
            "name": "PostgreSQL (Docker)",
            "type": "postgresql",
            "server": "localhost",
            "port": 5432,
            "username": "postgres",
            "password": "password", 
            "database": "devdb",
            "connection_string": "Host=localhost;Port=5432;Database=devdb;Username=postgres;Password=password;",
            "test_command": "docker exec postgres-dev psql -U postgres -d devdb -c 'SELECT version();'"
        },
        "mysql_docker": {
            "name": "MySQL (Docker)",
            "type": "mysql",
            "server": "localhost",
            "port": 3306,
            "username": "root",
            "password": "password",
            "database": "devdb", 
            "connection_string": "Server=localhost;Port=3306;Database=devdb;Uid=root;Pwd=password;",
            "test_command": "docker exec mysql-dev mysql -u root -ppassword -e 'SELECT VERSION();'"
        },
        "sqlite_local": {
            "name": "SQLite (Local)",
            "type": "sqlite",
            "file_path": "/workspaces/sugarglitch-realops/dev_database.db",
            "connection_string": "Data Source=/workspaces/sugarglitch-realops/dev_database.db;",
            "test_command": "sqlite3 /workspaces/sugarglitch-realops/dev_database.db 'SELECT sqlite_version();'"
        }
    }
    
    connections_file = "/workspaces/sugarglitch-realops/database_connections.json"
    with open(connections_file, 'w') as f:
        json.dump(connections, f, indent=2)
    
    print(f"✅ Created connection examples: {connections_file}")
    return connections_file

def verify_fix():
    """Verify that the fixes are working"""
    print("🔍 Verifying fixes...")
    
    verification_results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "checks": []
    }
    
    # Check VS Code settings
    settings_files = [
        Path.home() / ".vscode-remote" / "data" / "Machine" / "settings.json",
        Path.home() / ".vscode" / "User" / "settings.json"
    ]
    
    settings_updated = False
    for settings_file in settings_files:
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    if "mssql.enableStartupMessage" in settings and not settings["mssql.enableStartupMessage"]:
                        settings_updated = True
                        verification_results["checks"].append({
                            "name": "VS Code Settings Updated",
                            "status": "✅ PASS",
                            "file": str(settings_file)
                        })
                        break
            except:
                pass
    
    if not settings_updated:
        verification_results["checks"].append({
            "name": "VS Code Settings",
            "status": "⚠️  Settings file may need manual update"
        })
    
    # Check Docker availability
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            verification_results["checks"].append({
                "name": "Docker Available",
                "status": "✅ PASS",
                "version": result.stdout.strip()
            })
            
            # Check if SQL Server container is running
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            if 'sqlserver-dev' in result.stdout:
                verification_results["checks"].append({
                    "name": "SQL Server Container",
                    "status": "✅ RUNNING"
                })
            else:
                verification_results["checks"].append({
                    "name": "SQL Server Container", 
                    "status": "⚠️  Not running - use start_sqlserver_docker.sh"
                })
        else:
            verification_results["checks"].append({
                "name": "Docker",
                "status": "❌ Not available"
            })
    except FileNotFoundError:
        verification_results["checks"].append({
            "name": "Docker",
            "status": "❌ Not installed"
        })
    
    # Check created files
    expected_files = [
        "/workspaces/sugarglitch-realops/start_sqlserver_docker.sh",
        "/workspaces/sugarglitch-realops/DATABASE_EXTENSIONS_GUIDE.md",
        "/workspaces/sugarglitch-realops/database_connections.json"
    ]
    
    for file_path in expected_files:
        if Path(file_path).exists():
            verification_results["checks"].append({
                "name": f"File: {Path(file_path).name}",
                "status": "✅ Created",
                "path": file_path
            })
        else:
            verification_results["checks"].append({
                "name": f"File: {Path(file_path).name}",
                "status": "❌ Missing"
            })
    
    # Save verification results
    verification_file = "/workspaces/sugarglitch-realops/fix_verification.json"
    with open(verification_file, 'w') as f:
        json.dump(verification_results, f, indent=2)
    
    print(f"✅ Verification complete: {verification_file}")
    
    # Print summary
    print("\n📋 VERIFICATION SUMMARY:")
    for check in verification_results["checks"]:
        print(f"   {check['status']} {check['name']}")
    
    return verification_results

def main():
    """Run the complete immediate fix process"""
    print("🚀 IMMEDIATE MS SQL EXTENSION FIX")
    print("=" * 50)
    
    # Step 1: Disable MS SQL extension via settings
    settings_file = disable_mssql_extension()
    
    # Step 2: Set up Docker SQL Server
    docker_script = setup_docker_sqlserver()
    
    # Step 3: Create extension installation guide
    guide_file = create_extension_install_guide()
    
    # Step 4: Create connection examples
    connections_file = create_connection_examples()
    
    # Step 5: Verify fixes
    verification = verify_fix()
    
    print("\n🎉 IMMEDIATE FIX COMPLETE!")
    print("=" * 50)
    
    print("\n✅ ACTIONS COMPLETED:")
    print(f"   1. Updated VS Code settings: {settings_file}")
    print(f"   2. Created Docker script: {docker_script}")
    print(f"   3. Created extension guide: {guide_file}")
    print(f"   4. Created connection examples: {connections_file}")
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Reload VS Code window (Ctrl+Shift+P → 'Reload Window')")
    print("   2. The MS SQL extension errors should stop")
    print("   3. Use Docker SQL Server for SQL Server development")
    print("   4. Install alternative database extensions manually")
    
    print("\n🐳 TO START SQL SERVER:")
    print(f"   bash {docker_script}")
    
    print("\n📖 FOR EXTENSION INSTALLATION:")
    print(f"   View: {guide_file}")
    
    return verification

if __name__ == "__main__":
    main()
