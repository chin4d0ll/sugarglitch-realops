#!/bin/bash
# Quick SQL Server Docker Setup
echo "🚀 Starting SQL Server Docker container..."

# Stop and remove existing container if it exists
docker stop sqlserver-dev 2>/dev/null || true
docker rm sqlserver-dev 2>/dev/null || true

# Start new SQL Server container
docker run --name sqlserver-dev \
    -e 'ACCEPT_EULA=Y' \
    -e 'SA_PASSWORD=YourStrongPassword123!' \
    -p 1433:1433 \
    -d mcr.microsoft.com/mssql/server:2019-latest

# Wait for container to start
echo "⏳ Waiting for SQL Server to start..."
sleep 15

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
    
    # Try to test the connection
    echo ""
    echo "🧪 Testing connection..."
    docker exec sqlserver-dev /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrongPassword123!' -Q 'SELECT @@VERSION' 2>/dev/null && echo "✅ Connection test successful!" || echo "⚠️  Connection test failed - container may still be starting"
else
    echo "❌ Failed to start SQL Server container"
    echo "📋 Container logs:"
    docker logs sqlserver-dev
fi
