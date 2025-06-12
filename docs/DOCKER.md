# Docker Deployment Guide

This document provides comprehensive instructions for containerizing and deploying the SugarGlitch RealOps project using Docker.

## Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 1.29+)
- At least 2GB of available RAM
- Internet connection for downloading dependencies

## Quick Start

### 1. Using the Management Script (Recommended)

The project includes a `docker-scripts.sh` management script that simplifies Docker operations:

```bash
# Make the script executable (first time only)
chmod +x docker-scripts.sh

# Build the Docker image
./docker-scripts.sh build

# Run the container with default settings
./docker-scripts.sh run

# Start services with docker-compose
./docker-scripts.sh compose

# Open a shell in the container for debugging
./docker-scripts.sh shell

# View logs
./docker-scripts.sh logs

# Stop services
./docker-scripts.sh stop

# Clean up unused Docker resources
./docker-scripts.sh cleanup
```

### 2. Manual Docker Commands

If you prefer to use Docker commands directly:

```bash
# Build the image
docker build -t sugarglitch-realops:latest .

# Run the container
docker run --rm -it \
    --name sugarglitch-realops \
    -v "$(pwd)/logs:/app/logs" \
    -v "$(pwd)/databases:/app/databases" \
    -v "$(pwd)/extractions:/app/extractions" \
    -v "$(pwd)/results:/app/results" \
    sugarglitch-realops:latest

# Run with custom command
docker run --rm -it sugarglitch-realops:latest tools/generate_dm_timeline.py
```

### 3. Using Docker Compose

For production deployments or when you need persistent services:

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

## Configuration

### Environment Variables

The following environment variables can be configured:

- `PYTHONUNBUFFERED=1` - Ensures Python output is not buffered
- `PLAYWRIGHT_BROWSERS_PATH=/ms-playwright` - Playwright browser installation path

### Volume Mounts

The following directories are mounted as volumes for data persistence:

- `./logs:/app/logs` - Application logs
- `./databases:/app/databases` - SQLite databases
- `./extractions:/app/extractions` - Extraction results
- `./results:/app/results` - Processing results
- `./config:/app/config` - Configuration files

### Network Configuration

The container uses a custom bridge network (`realops-network`) for isolation and security.

## Customization

### Running Different Scripts

You can run any script in the container by specifying it as an argument:

```bash
# Run DM timeline generator
./docker-scripts.sh run tools/generate_dm_timeline.py

# Run bootstrap script
./docker-scripts.sh run bootstrap.py

# Run a specific extractor
./docker-scripts.sh run extractors/advanced_stable_dm_extractor.py
```

### Development Mode

For development, you can mount the entire source code directory:

```bash
docker run --rm -it \
    --name sugarglitch-realops-dev \
    -v "$(pwd):/app" \
    --entrypoint /bin/bash \
    sugarglitch-realops:latest
```

### Custom Entrypoint

Override the default entrypoint for debugging:

```bash
docker run --rm -it \
    --entrypoint /bin/bash \
    sugarglitch-realops:latest
```

## Production Deployment

### Resource Limits

The docker-compose.yml includes resource limits:

- Memory: 1GB limit, 512MB reservation
- CPU: 0.5 cores limit, 0.25 cores reservation

### Health Checks

The container includes health checks to ensure it's running properly:

- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 40 seconds

### Security

- Container runs as non-root user (`appuser`)
- Minimal base image (python:3.12-slim)
- Only necessary system packages installed

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure the host directories have proper permissions

   ```bash
   chmod 755 logs databases extractions results
   ```

2. **Memory Issues**: Increase Docker's memory allocation if you encounter OOM errors

3. **Playwright Issues**: The container automatically installs Playwright dependencies

### Debugging

Access the container shell for debugging:

```bash
./docker-scripts.sh shell
# or
docker exec -it sugarglitch-realops /bin/bash
```

View container logs:

```bash
./docker-scripts.sh logs
# or
docker logs sugarglitch-realops
```

### Performance Optimization

1. **Build Cache**: Use `.dockerignore` to exclude unnecessary files
2. **Layer Optimization**: Requirements are installed before copying source code
3. **Multi-stage Builds**: Consider using multi-stage builds for production

## Image Details

- **Base Image**: python:3.12-slim
- **Python Version**: 3.12
- **Playwright**: Chromium browser included
- **Working Directory**: `/app`
- **Default User**: `appuser` (non-root)
- **Health Check**: Included
- **Size**: Approximately 1.2GB (includes Chromium)

## Maintenance

### Updating Dependencies

1. Update `requirements.txt`
2. Rebuild the image: `./docker-scripts.sh build`
3. Restart services: `docker-compose up --build -d`

### Cleanup

Regular cleanup to free disk space:

```bash
./docker-scripts.sh cleanup
# or
docker system prune -a
docker volume prune
```

## Examples

### Batch Processing

```bash
# Process multiple files
for file in data/*.json; do
    ./docker-scripts.sh run tools/process_data.py "$file"
done
```

### Scheduled Tasks

Use cron or systemd to schedule regular processing:

```bash
# Add to crontab
0 2 * * * cd /path/to/project && ./docker-scripts.sh run tools/daily_processing.py
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Build and test Docker image
  run: |
    docker build -t sugarglitch-realops:test .
    docker run --rm sugarglitch-realops:test python -m pytest
```

## Support

For issues related to Docker deployment:

1. Check the logs: `./docker-scripts.sh logs`
2. Verify Docker installation: `docker --version`
3. Check available resources: `docker system df`
4. Review container status: `docker ps -a`

For application-specific issues, refer to the main README.md and project documentation.
