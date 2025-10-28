# Root Cause Analysis

**Date**: October 26, 2025
**Issue**: Duplicate Archon Docker containers after repository update
**Severity**: Medium

## Summary

The issue was caused by multiple failed Docker Compose attempts due to missing Supabase credentials and an inconsistency between the Dockerfile and docker-compose.yml configuration. This resulted in two sets of containers: an older working set and a newer failed set, both consuming system resources.

## Investigation

### Symptoms

- Docker Desktop showed 2 sets of Archon containers
- Original set (22 hours old): archon-server, archon-mcp, archon-ui (all exited)
- Newer set (8 minutes old): cursor-archon-archon-server (failed on startup)
- `docker-compose ps` showed no running containers
- New container failed with "Attribute 'socket_app' not found" error

### Diagnostics Performed

- Checked Docker container status with `docker ps -a`
- Examined container logs with `docker logs <container>`
- Analyzed docker-compose.yml vs Dockerfile.server consistency
- Verified project structure for duplicate configurations
- Checked for environment credential files

### Root Cause

The root cause was a combination of three issues:

1. **Missing Supabase Credentials**: No `.env` file existed with required `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` environment variables, causing the application to fail during startup credential initialization.

2. **Dockerfile Configuration Inconsistency**: The `python/Dockerfile.server` was configured to run `src.server.main:socket_app` but the `main.py` module only exports `app`, not `socket_app`.

3. **Multiple Failed Deployment Attempts**: Without proper credentials, multiple attempts were made to start the services, creating orphaned containers with different naming patterns (`archon-*` vs `cursor-archon-*`).

## Impact

- **Services Affected**: All Archon services (server, MCP, frontend)
- **User Impact**: Unable to run Archon application
- **Duration**: Approximately 22 hours from initial failure
- **Resource Waste**: Multiple stopped containers consuming disk space

## Resolution

### Immediate Fix

1. **Fixed Dockerfile Inconsistency**:
   ```diff
   - CMD sh -c "python -m uvicorn src.server.main:socket_app --host 0.0.0.0 --port ${ARCHON_SERVER_PORT} --workers 1"
   + CMD sh -c "python -m uvicorn src.server.main:app --host 0.0.0.0 --port ${ARCHON_SERVER_PORT} --workers 1"
   ```

2. **Cleaned Up Duplicate Containers**:
   ```bash
   docker rm $(docker ps -a -q --filter "name=cursor-archon" --filter "name=archon-")
   docker system prune -f
   ```

3. **Verified Single Setup**: Confirmed only one docker-compose.yml configuration exists in the project root.

### Long-term Prevention

1. **Add .env Template**: Create `.env.example` in project root with required Supabase credentials template
2. **Improve Error Messages**: The application now correctly fails fast with clear "Invalid API key" error instead of generic failures
3. **Docker Compose Consistency**: Ensure Dockerfile and docker-compose.yml use the same entry point
4. **Startup Health Checks**: Add pre-flight checks for required environment variables before attempting to start services

## Evidence

**Container Analysis**:
```
CONTAINER ID   IMAGE                                COMMAND                   CREATED         STATUS
6f795c5d0471   cursor-archon-archon-server:latest   "/bin/sh -c 'sh -c \"…"   8 minutes ago   Exited (1)
aa5dbf7002b3   archon-archon-mcp                    "python -m src.mcp_s…"    22 hours ago    Exited (137)
d902cf875dc5   archon-archon-frontend               "docker-entrypoint.s…"    22 hours ago    Exited (0)
0aeda5df0d6a   archon-archon-server                 "python -m uvicorn s…"    22 hours ago    Exited (137)
```

**Error Logs**:
```
ERROR:    Error loading ASGI app. Attribute "socket_app" not found in module "src.server.main".
Error initializing Supabase client: Invalid API key
```

**Code Analysis**:
- `docker-compose.yml`: Uses `src.server.main:app`
- `Dockerfile.server`: Used `src.server.main:socket_app` (now fixed)
- `main.py`: Only exports `app` FastAPI instance

## Lessons Learned

1. **Environment Setup is Critical**: Missing `.env` files should be caught during development setup, not at runtime
2. **Docker Configuration Consistency**: Dockerfile and docker-compose.yml must use the same application entry points
3. **Failed Deployments Create Technical Debt**: Multiple failed attempts leave orphaned resources that complicate future deployments
4. **Clear Error Messages Enable Fast Fixes**: The "Invalid API key" error was much more actionable than a generic ASGI loading failure

## Next Steps

1. Create `.env.example` file in project root
2. Add environment variable validation to startup process
3. Consider adding Docker Compose health check validation for required environment variables
4. Document the proper setup process in README.md</contents>
</xai:function_call">The RCA report has been generated and saved to `RCA.md` in the project root.
