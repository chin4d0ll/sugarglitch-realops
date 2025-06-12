# Docker Compose Setup for SugarGlitch RealOps

This document explains how to run SugarGlitch RealOps using Docker Compose with PostgreSQL database.

## 🐳 Architecture Overview

The Docker Compose setup includes:

- **Database Service (`db`)**: PostgreSQL 14 with initialized schema
- **Application Service (`app`)**: Main SugarGlitch RealOps application
- **Shared Network**: `sg_network` for service communication
- **Persistent Volumes**: PostgreSQL data persistence

## 🚀 Quick Start

### 1. Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+ (or docker-compose 1.29+)

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables (optional)
nano .env
```

### 3. Start Services

```bash
# Using the management script (recommended)
./docker-compose-scripts.sh start

# Or using docker-compose directly
docker-compose up -d
```

### 4. Check Status

```bash
# Check service status
./docker-compose-scripts.sh status

# View logs
./docker-compose-scripts.sh logs

# View specific service logs
./docker-compose-scripts.sh logs app
./docker-compose-scripts.sh logs db
```

## 📋 Service Configuration

### Database Service (db)

```yaml
- Image: postgres:14
- Container: sugarglitch_db
- Port: 5432
- Database: sgdb
- User: sguser
- Password: sgpass
```

**Connection String**: `postgresql://sguser:sgpass@db:5432/sgdb`

### Application Service (app)

```yaml
- Build: From local Dockerfile
- Container: sugarglitch_app
- Command: python3 tools/system_health_monitor_2025.py
- Depends on: db (with health check)
```

**Volume Mounts**:
- `./data` → `/app/data`
- `./logs` → `/app/logs`
- `./results` → `/app/results`
- `./config` → `/app/config` (read-only)
- `./databases` → `/app/databases`
- `./extractions` → `/app/extractions`

## 🛠️ Management Commands

### Using docker-compose-scripts.sh

```bash
# Start all services
./docker-compose-scripts.sh start

# Stop all services
./docker-compose-scripts.sh stop

# Restart services
./docker-compose-scripts.sh restart

# Build/rebuild services
./docker-compose-scripts.sh build

# View logs (all services)
./docker-compose-scripts.sh logs

# View logs (specific service)
./docker-compose-scripts.sh logs app
./docker-compose-scripts.sh logs db

# Check service status
./docker-compose-scripts.sh status

# Clean up everything
./docker-compose-scripts.sh clean
```

### Using Docker Compose directly

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Build services
docker-compose build

# Execute commands in containers
docker-compose exec app python3 tools/your_script.py
docker-compose exec db psql -U sguser -d sgdb
```

## 🔧 Environment Variables

Key environment variables (defined in `.env`):

```bash
# Database
POSTGRES_USER=sguser
POSTGRES_PASSWORD=sgpass
POSTGRES_DB=sgdb
DATABASE_URL=postgresql://sguser:sgpass@db:5432/sgdb

# Application
PYTHONUNBUFFERED=1
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
COMPOSE_PROJECT_NAME=sugarglitch-realops
```

## 💾 Database Management

### Accessing PostgreSQL

```bash
# Connect to database
docker-compose exec db psql -U sguser -d sgdb

# Run SQL commands
docker-compose exec db psql -U sguser -d sgdb -c "SELECT * FROM app_status;"

# Backup database
docker-compose exec db pg_dump -U sguser sgdb > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T db psql -U sguser -d sgdb
```

### Database Schema

The database is automatically initialized with:
- `app_status` - Application status tracking
- `extraction_logs` - Operation logging
- `dm_data` - Direct message data storage

## 🏥 Health Checks

Both services include health checks:

- **Database**: PostgreSQL connection test
- **Application**: Python execution test

Health check status is visible in `docker-compose ps` output.

## 📁 Data Persistence

### Volumes

- **PostgreSQL Data**: `postgres_data` named volume
- **Application Data**: Host directory mounts

### Backup Locations

```
./data/          # Application data
./logs/          # Application logs
./results/       # Extraction results
./databases/     # Local database files
./extractions/   # Extraction outputs
```

## 🚨 Troubleshooting

### Common Issues

1. **Port 5432 already in use**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "5433:5432"  # Use different host port
   ```

2. **Permission errors**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER ./data ./logs ./results
   ```

3. **Database connection fails**
   ```bash
   # Check database logs
   ./docker-compose-scripts.sh logs db
   
   # Restart services
   ./docker-compose-scripts.sh restart
   ```

4. **Application fails to start**
   ```bash
   # Check app logs
   ./docker-compose-scripts.sh logs app
   
   # Rebuild image
   ./docker-compose-scripts.sh build
   ```

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# Follow logs in real-time  
docker-compose logs -f

# View specific service logs
docker-compose logs app
docker-compose logs db

# Execute shell in containers
docker-compose exec app bash
docker-compose exec db bash
```

## 🔒 Security Considerations

### Production Deployment

1. **Change default passwords**:
   ```bash
   # Update .env file
   POSTGRES_PASSWORD=your-secure-password
   ```

2. **Use secrets management**:
   ```yaml
   # In docker-compose.yml
   secrets:
     db_password:
       file: ./secrets/db_password.txt
   ```

3. **Network security**:
   ```yaml
   # Remove port exposure for database
   # ports:
   #   - "5432:5432"
   ```

4. **Resource limits**:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1G
         cpus: '0.5'
   ```

## 🎯 Docker Compose Configuration

Complete `docker-compose.yml` configuration:

```yaml
services:
  # PostgreSQL Database Service
  db:
    image: postgres:14
    container_name: sugarglitch_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-sguser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-sgpass}
      POSTGRES_DB: ${POSTGRES_DB:-sgdb}
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./databases/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"
    networks:
      - sg_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sguser -d sgdb"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s

  # Main Application Service
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: sugarglitch_app
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: ${DATABASE_URL:-postgresql://sguser:sgpass@db:5432/sgdb}
      PYTHONUNBUFFERED: ${PYTHONUNBUFFERED:-1}
      PLAYWRIGHT_BROWSERS_PATH: ${PLAYWRIGHT_BROWSERS_PATH:-/ms-playwright}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./results:/app/results
      - ./config:/app/config:ro
      - ./databases:/app/databases
      - ./extractions:/app/extractions
    networks:
      - sg_network
    command: python3 tools/system_health_monitor_2025.py
    healthcheck:
      test: ["CMD", "python3", "-c", "import sys; print('App healthy'); exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'

# Named volumes for data persistence
volumes:
  postgres_data:
    driver: local

# Shared network
networks:
  sg_network:
    driver: bridge
    name: sg_network
```

## 🎯 Next Steps

1. **Customize Configuration**: Edit `docker-compose.yml` for your needs
2. **Add Services**: Extend with Redis, monitoring, etc.
3. **CI/CD Integration**: Use with GitHub Actions or similar
4. **Production Deployment**: Deploy to cloud platforms

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [SugarGlitch RealOps Documentation](./documentation/)

---

**Created**: June 6, 2025  
**Updated**: Auto-generated Docker Compose setup
