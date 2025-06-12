#!/bin/bash
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
