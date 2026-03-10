# Use Python 3.11 slim image for a lightweight base
# slim variant is smaller than full image but includes all necessary tools
FROM python:3.11-slim

# Set environment variables
# PYTHONUNBUFFERED: Ensures Python output is sent straight to terminal (useful for logs)
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files (saves space)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory inside container
# All subsequent commands will run from this directory
WORKDIR /app

# Install system dependencies if needed
# These are minimal - only essential packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker caching
# Docker caches each layer, so if requirements.txt doesn't change,
# this layer won't be rebuilt, speeding up subsequent builds
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir prevents pip from caching downloaded packages
# --upgrade pip ensures we have the latest pip version
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
# Copy everything after installing dependencies ensures
# code changes don't trigger dependency reinstallations
COPY . .

# Create necessary directories with proper permissions
# These directories will store generated content
RUN mkdir -p /app/audio /app/logs && \
    chmod 755 /app/audio /app/logs

# Create non-root user for security
# Running as root is a security risk
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Streamlit default port
# Streamlit runs on port 8501 by default
EXPOSE 8501

# Health check
# Docker will use this to determine if the container is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit application
# --server.address=0.0.0.0: Listen on all interfaces (required for Docker)
# --server.port=8501: Use default Streamlit port
# --server.enableCORS=false: Allow cross-origin requests if needed
# --server.enableXsrfProtection=true: Security feature
# --server.headless=true: Run without opening browser
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=true", \
     "--server.headless=true"]