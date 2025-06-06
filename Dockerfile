# Use Python 3.9-slim as base image for compatibility
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Install system dependencies for Playwright and general usage
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory and set up user
RUN useradd -m -u 1000 appuser
WORKDIR /app

# Copy requirements.txt first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright and Chromium
RUN playwright install chromium && \
    playwright install-deps chromium

# Copy essential project files
COPY tools/ /app/tools/
COPY config/ /app/config/
COPY extractors/ /app/extractors/
COPY launchers/ /app/launchers/
COPY bootstrap.py /app/
COPY README.md /app/
COPY PROJECT_STRUCTURE.md /app/
COPY SETUP.md /app/
COPY src/ultra_dm_conversation_extractor_2025.py /app/src/ultra_dm_conversation_extractor_2025.py

# Create necessary directories for runtime
RUN mkdir -p /app/logs /app/temp /app/results /app/databases /app/extractions

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set working directory to /app/
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; print('Python version:', sys.version); exit(0)" || exit 1

# Expose port if needed (uncomment if your application uses a web server)
# EXPOSE 8000

# Set the default entrypoint for DM extractor
ENTRYPOINT ["python3", "src/ultra_dm_conversation_extractor_2025.py"]
