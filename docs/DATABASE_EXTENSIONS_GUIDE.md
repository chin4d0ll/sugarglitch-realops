# 📦 Alternative Database Extensions - Installation Guide

## 🎯 Quick Fix Summary
The MS SQL Server extension fails on Alpine Linux due to binary incompatibility. Here are working alternatives:

## ✅ IMMEDIATE ACTIONS

### 1. Disable MS SQL Extension
- Open VS Code Extensions panel (`Ctrl+Shift+X`)
- Search for "ms-mssql" 
- Click "Disable" on the SQL Server (mssql) extension
- Reload VS Code (`Ctrl+Shift+P` → "Reload Window")

### 2. Install Compatible Extensions

#### Method A: VS Code Extensions Panel (Recommended)
1. Open Extensions panel (`Ctrl+Shift+X`)
2. Install each extension by searching:

**🐘 PostgreSQL Extension**
- Search: `ms-ossdata.vscode-postgresql`
- Publisher: Microsoft
- Click "Install"

**🐬 MySQL Extension**  
- Search: `formulahendry.vscode-mysql`
- Publisher: Jun Han
- Click "Install"

**💾 SQLite Extension**
- Search: `alexcvzz.vscode-sqlite`
- Publisher: alexcvzz
- Click "Install"

**🌐 Universal Database Client**
- Search: `cweijan.vscode-database-client2`
- Publisher: cweijan
- Click "Install"

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
docker run --name postgres-dev \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=devdb \
    -p 5432:5432 \
    -d postgres:13

# Connection: Host=localhost;Port=5432;Database=devdb;Username=postgres;Password=password;
```

### MySQL
```bash
docker run --name mysql-dev \
    -e MYSQL_ROOT_PASSWORD=password \
    -e MYSQL_DATABASE=devdb \
    -p 3306:3306 \
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
