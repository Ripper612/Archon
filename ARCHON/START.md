# Archon Quick Start Guide

## Prerequisites
- Docker Desktop installed and running
- Supabase project with API credentials
- At least 8GB RAM available for Docker

## Quick Start

### 1. Navigate to Project Directory
```bash
cd C:\cursor\cursor-archon\ARCHON
```

### 2. Start All Services
```bash
docker-compose up --build -d
```

### 3. Verify Services Are Running
```bash
docker-compose ps
```

**Expected Output:**
```
NAME            IMAGE                           STATUS
archon-server   cursor-archon-archon-server     Up (healthy)
archon-mcp      cursor-archon-archon-mcp        Up (healthy)
archon-ui       cursor-archon-archon-frontend   Up (healthy)
```

## Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3737 | Web UI |
| API Server | http://localhost:8181 | REST API |
| MCP Server | http://localhost:8051 | AI Tools |

## Health Checks

### Check All Services Health
```bash
# API Server
curl http://localhost:8181/health

# MCP Server (may not respond directly)
curl http://localhost:8051/health

# UI (should return HTML)
curl -I http://localhost:3737
```

### Check Docker Resource Usage
```bash
docker stats --no-stream
```

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f archon-server
docker-compose logs -f archon-mcp
docker-compose logs -f archon-ui
```

## Environment Setup

### Required Environment Variables
Create `.env` file in `ARCHON/` directory:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key-here
```

### Optional Variables
```bash
OPENAI_API_KEY=your-openai-key
LOG_LEVEL=INFO
```

## Troubleshooting

### Services Not Starting
```bash
# Check for errors
docker-compose logs

# Restart services
docker-compose restart

# Full rebuild
docker-compose down
docker-compose up --build -d
```

### Port Conflicts
```bash
# Check what's using ports
netstat -ano | findstr "8181\|8051\|3737"

# Stop conflicting services or change ports in docker-compose.yml
```

### Memory Issues
```bash
# Increase Docker Desktop memory allocation
# Or reduce concurrent services
docker-compose up -d archon-server archon-ui  # Skip MCP
```

## Development Workflow

### Stop Services
```bash
docker-compose down
```

### Clean Everything
```bash
docker-compose down -v  # Remove volumes
docker system prune -a  # Remove unused images
```

### Update Services
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up --build -d
```

## Port Reference

| Port | Service | Internal Use |
|------|---------|--------------|
| 8181 | archon-server | FastAPI + WebSocket |
| 8051 | archon-mcp | MCP Protocol Server |
| 3737 | archon-ui | React Frontend |
| 8052 | archon-agents | AI Agents (optional) |

## Success Indicators

✅ **All services show "Up (healthy)" in `docker-compose ps`**
✅ **Frontend loads at http://localhost:3737**
✅ **API responds at http://localhost:8181/health**
✅ **No port conflicts**
✅ **Memory usage stable**

## Emergency Stop
```bash
# Stop everything
docker-compose down

# Force stop
docker-compose down --timeout 0

# Kill containers
docker kill $(docker ps -q)
```
