# Docker Guide for CVAudioStudio

This comprehensive guide will teach you how to use Docker with the CVAudioStudio Text-to-Speech application.

## Table of Contents

1. [What is Docker?](#what-is-docker)
2. [Why Use Docker?](#why-use-docker)
3. [Prerequisites](#prerequisites)
4. [Quick Start](#quick-start)
5. [Docker Commands](#docker-commands)
6. [Understanding the Files](#understanding-the-files)
7. [Common Workflows](#common-workflows)
8. [Troubleshooting](#troubleshooting)
9. [Production Deployment](#production-deployment)
10. [Best Practices](#best-practices)

---

## What is Docker?

Docker is a platform that uses containerization technology to package applications with all their dependencies into a standardized unit called a **container**. Think of it like a lightweight virtual machine, but much more efficient.

**Key Concepts:**

- **Image**: A read-only template containing the application and dependencies (like a blueprint)
- **Container**: A running instance of an image (like a house built from a blueprint)
- **Dockerfile**: A script that tells Docker how to build an image
- **Docker Compose**: A tool for defining and running multi-container applications

---

## Why Use Docker?

### Benefits for CVAudioStudio:

1. **Consistency** - Works exactly the same on your laptop, a server, or the cloud
2. **Isolation** - No conflicts with other Python projects or system packages
3. **Portability** - Run anywhere Docker is installed
4. **Reproducibility** - Same environment every time
5. **Easy Deployment** - Deploy to any cloud platform with Docker support
6. **Version Control** - Track infrastructure changes alongside code

---

## Prerequisites

### Install Docker Desktop

**macOS:**
```bash
# Download from https://www.docker.com/products/docker-desktop
# Or use Homebrew
brew install --cask docker
```

**Windows:**
```bash
# Download from https://www.docker.com/products/docker-desktop
# WSL2 backend recommended
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in for group change to take effect
```

### Verify Installation

```bash
docker --version
docker-compose --version
```

Expected output:
```
Docker version 20.10.x or higher
Docker Compose version 2.x.x or higher
```

---

## Quick Start

### 1. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Example `.env` file:
```bash
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_ORG_ID=org-your-org-id
LOG_LEVEL=INFO
MAX_TEXT_LENGTH=5000
```

### 2. Build and Run with Docker Compose

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Access the Application

Open your browser and go to: **http://localhost:8501**

---

## Docker Commands

### Building Images

```bash
# Build using Docker Compose (recommended)
docker-compose build

# Build with no cache (force rebuild)
docker-compose build --no-cache

# Build using Docker directly
docker build -t cvaudiostudio:latest .
```

### Running Containers

```bash
# Start all services in detached mode (background)
docker-compose up -d

# Start with logs visible
docker-compose up

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# Stop and remove containers, networks, and volumes
docker-compose down -v
```

### Viewing Logs

```bash
# Follow logs (real-time)
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app

# View last 100 lines
docker-compose logs --tail=100 app

# View logs since specific time
docker-compose logs --since=2024-03-09T10:00:00 app
```

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Execute command in running container
docker-compose exec app bash

# Execute command in container (direct)
docker exec -it cvaudiostudio bash

# View container stats (CPU, memory, etc.)
docker stats cvaudiostudio
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi cvaudiostudio:latest

# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect cvaudiostudio_audio-data

# Remove unused volumes
docker volume prune
```

### Network Management

```bash
# List networks
docker network ls

# Inspect network
docker network inspect cvaudiostudio-network

# Connect container to network
docker network connect cvaudiostudio-network container_name
```

---

## Understanding the Files

### Dockerfile Explained

```dockerfile
# Base image - Python 3.11 with minimal packages
FROM python:3.11-slim

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Working directory inside container
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y curl

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Create directories and set permissions
RUN mkdir -p /app/audio /app/logs

# Non-root user for security
RUN useradd -m -u 1000 appuser
USER appuser

# Expose port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "streamlit_app.py", ...]
```

**Key Instructions:**
- `FROM`: Base image
- `WORKDIR`: Set working directory
- `COPY`: Copy files from host to container
- `RUN`: Execute commands during build
- `ENV`: Set environment variables
- `EXPOSE`: Document exposed ports
- `USER`: Set user for running commands
- `CMD`: Default command to run

### docker-compose.yml Explained

```yaml
version: '3.8'

services:
  app:
    build:
      context: .          # Build context directory
      dockerfile: Dockerfile
    
    container_name: cvaudiostudio
    
    ports:
      - "8501:8501"      # host:container
    
    environment:
      - KEY=value        # Environment variables
    
    volumes:
      - ./:/app          # Mount code
      - ./audio:/app/audio  # Persist audio
    
    restart: unless-stopped
```

**Key Concepts:**
- **Services**: Define containers to run
- **Ports**: Map container ports to host
- **Volumes**: Persist data outside containers
- **Networks**: Enable container communication
- **Environment**: Pass configuration

### .dockerignore Explained

This file works like `.gitignore` but for Docker. It excludes files from the build context:

```
# Exclude these from Docker image
.git/
__pycache__/
*.pyc
.env
logs/
audio/*.mp3
```

**Benefits:**
- Smaller image size
- Faster builds
- Better security (don't copy secrets)
- Avoid caching issues

---

## Common Workflows

### Development Workflow

```bash
# 1. Start development environment
docker-compose up

# 2. Make code changes (hot reload enabled)
# Changes reflect immediately in container

# 3. View logs
docker-compose logs -f

# 4. Stop when done
docker-compose down
```

### Production Build

```bash
# 1. Build optimized image
docker build -t cvaudiostudio:prod .

# 2. Tag for registry
docker tag cvaudiostudio:prod username/cvaudiostudio:latest

# 3. Push to registry
docker push username/cvaudiostudio:latest

# 4. Run on production server
docker run -d \
  --name cvaudiostudio \
  -p 8501:8501 \
  -v /path/to/audio:/app/audio \
  -v /path/to/logs:/app/logs \
  --env-file .env \
  username/cvaudiostudio:latest
```

### Updating Dependencies

```bash
# 1. Update requirements.txt
# 2. Rebuild image
docker-compose build --no-cache

# 3. Restart container
docker-compose up -d
```

### Debugging

```bash
# 1. Check container status
docker-compose ps

# 2. View logs
docker-compose logs -f app

# 3. Enter container for debugging
docker-compose exec app bash

# 4. Check environment variables
docker-compose exec app env

# 5. Test from inside container
docker-compose exec app curl http://localhost:8501
```

---

## Troubleshooting

### Container Won't Start

**Problem:** Container exits immediately

```bash
# Check logs
docker-compose logs app

# Common issues:
# - Missing .env file
# - Port 8501 already in use
# - Invalid OPENAI_API_KEY
```

**Solution:**
```bash
# Check what's using port 8501
lsof -i :8501

# Kill process if needed
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 on host
```

### Permission Issues

**Problem:** Can't write to audio/ or logs/

```bash
# Fix permissions on host
sudo chown -R $USER:$USER audio/
sudo chown -R $USER:$USER logs/

# Or run with correct user ID
docker-compose run --user $(id -u):$(id -g) app
```

### Image Build Fails

**Problem:** Build fails with errors

```bash
# Clean build
docker-compose down
docker system prune -a
docker-compose build --no-cache
```

### Out of Disk Space

**Problem:** Docker using too much space

```bash
# Clean up
docker system prune -a --volumes

# Check space usage
docker system df
```

### Container Not Accessible

**Problem:** Can't access http://localhost:8501

```bash
# Check if container is running
docker-compose ps

# Check if port is exposed
docker port cvaudiostudio

# Check firewall settings
sudo ufw status
```

---

## Production Deployment

### Deploy to Docker Hub

```bash
# 1. Login to Docker Hub
docker login

# 2. Build and tag
docker build -t username/cvaudiostudio:latest .

# 3. Push to Docker Hub
docker push username/cvaudiostudio:latest

# 4. Pull and run on server
docker pull username/cvaudiostudio:latest
docker run -d -p 8501:8501 username/cvaudiostudio:latest
```

### Deploy to Cloud Platforms

**AWS ECS:**
```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag cvaudiostudio:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/cvaudiostudio:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/cvaudiostudio:latest
```

**Google Cloud Run:**
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/cvaudiostudio

# Deploy
gcloud run deploy cvaudiostudio --image gcr.io/PROJECT_ID/cvaudiostudio --platform managed
```

**Azure Container Instances:**
```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create container
az container create \
  --resource-group myResourceGroup \
  --name cvaudiostudio \
  --image username/cvaudiostudio:latest \
  --ports 8501
```

---

## Best Practices

### Security

1. **Use Non-Root User**
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

2. **Don't Copy Secrets**
   ```dockerignore
   .env
   *.key
   *.pem
   ```

3. **Scan Images for Vulnerabilities**
   ```bash
   docker scan cvaudiostudio:latest
   ```

4. **Use Specific Versions**
   ```dockerfile
   FROM python:3.11-slim
   # Not: FROM python:latest
   ```

### Performance

1. **Use .dockerignore**
   - Reduces build context size
   - Faster builds
   - Smaller images

2. **Layer Caching**
   - Copy requirements.txt before code
   - Changes in code won't reinstall dependencies

3. **Multi-Stage Builds**
   - Build in one stage, copy artifacts to another
   - Smaller final image

4. **Resource Limits**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1.0'
         memory: 1G
   ```

### Maintenance

1. **Regular Updates**
   ```bash
   # Update base image
   docker pull python:3.11-slim
   docker-compose build --no-cache
   ```

2. **Clean Up**
   ```bash
   # Remove unused resources
   docker system prune -a --volumes
   ```

3. **Monitor Resources**
   ```bash
   # Check container stats
   docker stats cvaudiostudio
   ```

4. **Backup Data**
   ```bash
   # Backup volumes
   docker run --rm -v cvaudiostudio_audio-data:/data \
     -v $(pwd):/backup ubuntu \
     tar czf /backup/audio-backup.tar.gz /data
   ```

---

## Advanced Topics

### Multi-Stage Build Example

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["streamlit", "run", "streamlit_app.py"]
```

### Custom Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1
```

### Docker Compose Override

Create `docker-compose.override.yml` for development:
```yaml
version: '3.8'
services:
  app:
    volumes:
      - ./:/app:ro  # Read-only mount
    environment:
      - STREAMLIT_LOGGER_LEVEL=debug
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

---

## Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/deploy)

---

## Getting Help

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify Docker is running: `docker ps`
3. Check port availability: `lsof -i :8501`
4. Review this guide's troubleshooting section
5. Open an issue on GitHub

---

**Happy Containerizing! 🐳**