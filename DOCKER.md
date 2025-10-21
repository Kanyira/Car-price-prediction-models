# 🐳 Docker Guide

Comprehensive guide for working with Docker containers for the Car Price Predictor.

## 📋 Quick Start

### Run Everything with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access:**
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🏗️ Architecture

### Services

1. **Backend** (FastAPI)
   - Port: 8000
   - Image: `car-price-backend`
   - Health check: `GET /`

2. **Frontend** (React + Nginx)
   - Port: 80
   - Image: `car-price-frontend`
   - Proxies `/api/*` to backend

### Network

- Custom bridge network: `car-price-network`
- Services communicate using service names
- Frontend accesses backend at `http://backend:8000`

---

## 🔨 Building Images

### Backend

```bash
# Build
docker build -t car-price-backend .

# Build with specific tag
docker build -t car-price-backend:v1.0 .

# Build with no cache
docker build --no-cache -t car-price-backend .
```

### Frontend

```bash
# Build
docker build -t car-price-frontend ./frontend

# Build with build args
docker build \
  --build-arg REACT_APP_API_URL=https://api.example.com \
  -t car-price-frontend \
  ./frontend
```

---

## 🚀 Running Containers

### Backend

```bash
# Run backend
docker run -d \
  --name car-price-backend \
  -p 8000:8000 \
  car-price-backend

# Run with environment variables
docker run -d \
  --name car-price-backend \
  -p 8000:8000 \
  -e PYTHONUNBUFFERED=1 \
  car-price-backend

# Run with volume mount (for development)
docker run -d \
  --name car-price-backend \
  -p 8000:8000 \
  -v $(pwd):/app \
  car-price-backend
```

### Frontend

```bash
# Run frontend
docker run -d \
  --name car-price-frontend \
  -p 80:80 \
  car-price-frontend

# Run with custom API URL
docker run -d \
  --name car-price-frontend \
  -p 80:80 \
  -e REACT_APP_API_URL=http://localhost:8000 \
  car-price-frontend
```

---

## 🔍 Debugging

### View Logs

```bash
# Backend logs
docker logs car-price-backend

# Follow logs
docker logs -f car-price-backend

# Last 100 lines
docker logs --tail 100 car-price-backend

# Frontend logs
docker logs car-price-frontend
```

### Execute Commands in Container

```bash
# Backend - Python shell
docker exec -it car-price-backend python

# Backend - bash shell
docker exec -it car-price-backend bash

# Frontend - nginx status
docker exec -it car-price-frontend nginx -t

# Frontend - shell
docker exec -it car-price-frontend sh
```

### Inspect Container

```bash
# View container details
docker inspect car-price-backend

# View container stats
docker stats car-price-backend

# View container processes
docker top car-price-backend
```

---

## 🧹 Cleanup

### Stop and Remove Containers

```bash
# Stop containers
docker stop car-price-backend car-price-frontend

# Remove containers
docker rm car-price-backend car-price-frontend

# Stop and remove
docker rm -f car-price-backend car-price-frontend
```

### Remove Images

```bash
# Remove images
docker rmi car-price-backend car-price-frontend

# Remove all unused images
docker image prune -a
```

### Complete Cleanup

```bash
# Remove everything (containers, images, volumes, networks)
docker-compose down -v --rmi all

# System-wide cleanup
docker system prune -a --volumes
```

---

## 📦 Multi-Stage Builds

### Frontend Dockerfile Explained

```dockerfile
# Stage 1: Build React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Benefits:**
- Final image only contains production files
- Smaller image size (~30MB vs ~1GB)
- Faster deployment
- More secure (no dev dependencies)

---

## 🔒 Security Best Practices

### 1. Use Specific Base Images

```dockerfile
# ❌ Bad - latest tag
FROM python:latest

# ✅ Good - specific version
FROM python:3.11-slim
```

### 2. Run as Non-Root User

```dockerfile
# Create non-root user
RUN adduser -D appuser
USER appuser
```

### 3. Minimize Layers

```dockerfile
# ❌ Bad - multiple RUN commands
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get clean

# ✅ Good - single RUN command
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 4. Use .dockerignore

Exclude unnecessary files:
```
node_modules
.git
.env
*.md
__pycache__
```

---

## 🎯 Optimization Tips

### Reduce Image Size

1. **Use Alpine-based images**
   ```dockerfile
   FROM python:3.11-alpine
   FROM node:18-alpine
   ```

2. **Multi-stage builds**
   - Build in one stage, copy artifacts to final stage

3. **Remove cache and temporary files**
   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   RUN npm ci --only=production && npm cache clean --force
   ```

### Faster Builds

1. **Order Dockerfile commands by change frequency**
   ```dockerfile
   # Changes rarely - cache these layers
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   # Changes often - run last
   COPY . .
   ```

2. **Use BuildKit cache**
   ```bash
   DOCKER_BUILDKIT=1 docker build -t myapp .
   ```

3. **Layer caching**
   ```bash
   docker build --cache-from myapp:latest -t myapp:new .
   ```

---

## 🌐 Docker Compose Advanced

### Override Configuration

Create `docker-compose.override.yml` for local development:

```yaml
version: '3.8'

services:
  backend:
    volumes:
      - ./:/app
    environment:
      - DEBUG=True
    
  frontend:
    volumes:
      - ./frontend/src:/app/src
```

### Environment-Specific Configs

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Profiles

```yaml
services:
  backend:
    profiles: ["app"]
  
  db:
    profiles: ["db"]

# Run specific profiles
docker-compose --profile app up
```

---

## 📊 Health Checks

### Backend Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/')" || exit 1
```

### Check Health Status

```bash
# View health status
docker ps

# Inspect health
docker inspect --format='{{.State.Health.Status}}' car-price-backend

# View health logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' car-price-backend
```

---

## 🔄 Development Workflow

### Hot Reload Setup

**Backend:**
```yaml
services:
  backend:
    volumes:
      - ./:/app
    command: uvicorn main:app --reload --host 0.0.0.0
```

**Frontend:**
```yaml
services:
  frontend:
    volumes:
      - ./frontend/src:/app/src
    command: npm start
```

### Testing in Docker

```bash
# Run tests
docker-compose run backend python test_api.py

# Run specific command
docker-compose run backend python -m pytest

# Override command
docker-compose run frontend npm test
```

---

## 📝 Useful Commands

### Docker

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# List images
docker images

# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# View disk usage
docker system df

# Full system info
docker system info
```

### Docker Compose

```bash
# Start services
docker-compose up

# Start specific service
docker-compose up backend

# Rebuild images
docker-compose build

# Restart service
docker-compose restart backend

# View running services
docker-compose ps

# Execute command
docker-compose exec backend bash

# View logs
docker-compose logs -f backend
```

---

## 🐛 Troubleshooting

### Container Exits Immediately

```bash
# Check logs
docker logs car-price-backend

# Run interactively
docker run -it car-price-backend bash
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Use different port
docker run -p 8001:8000 car-price-backend
```

### Network Issues

```bash
# List networks
docker network ls

# Inspect network
docker network inspect car-price-network

# Create network manually
docker network create car-price-network
```

### Permission Issues

```bash
# Run as root
docker exec -u root -it car-price-backend bash

# Fix permissions
docker exec car-price-backend chown -R appuser:appuser /app
```

---

## 📚 Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)

---

**Last Updated:** 2025-10-19
