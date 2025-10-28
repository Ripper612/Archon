# Archon Installation & Setup Plan - Final Version

## 📋 Overview

**Project**: Archon - Knowledge Management MCP Server for AI IDEs
**Root Directory**: `C:\cursor\cursor-archon\ARCHON`
**Python Strategy**: Local Python 3.12 virtual environment + Docker for services
**Database**: Fresh Supabase project (PostgreSQL + pgvector)
**Target IDE**: Cursor (with existing Context7 MCP server)

---

## 🎯 Architecture Summary

**Archon Components:**
- **Backend API**: FastAPI server (Port 8181)
- **MCP Server**: Model Context Protocol interface (Port 8051)
- **Frontend UI**: React + Vite web dashboard (Port 3737)
- **AI Agents**: PydanticAI service for ML operations (Port 8052)
- **Database**: Supabase (PostgreSQL + pgvector)

**Features:**
- 14 MCP tools for AI agent integration
- Web crawling & document processing (PDF, DOCX, MD, TXT)
- RAG search with vector embeddings
- Project & task management
- Real-time updates via Socket.IO

---

## Phase 0: Prerequisites Verification ✅

### 0.1 Check Installed Software
```powershell
# Node.js (required for frontend)
node --version    # Should be 18+
npm --version

# Docker Desktop (required for services)
docker --version
docker compose version

# Git (for version control)
git --version
```

### 0.2 Install Python 3.12
**Download**: https://www.python.org/downloads/
- ✅ Check "Add Python 3.12 to PATH"
- ✅ Check "Install pip"
- Install location: `C:\Users\wenge\AppData\Local\Programs\Python\Python312`

**Verify Installation:**
```powershell
py -3.12 --version    # Should show Python 3.12.x
py -3.12 -m pip --version
```

### 0.3 Verify Docker Desktop Running
```powershell
docker ps    # Should not error
```

---

## Phase 1: Repository Setup

### 1.1 Create Clean Directory Structure
```powershell
# Root project directory
cd C:\cursor\cursor-archon

# Create ARCHON root (if not exists)
New-Item -ItemType Directory -Force -Path "C:\cursor\cursor-archon\ARCHON"

# Copy extracted files to clean structure
Copy-Item -Path "C:\cursor\cursor-archon\REPO\Archon-main\Archon-main\*" `
          -Destination "C:\cursor\cursor-archon\ARCHON\" `
          -Recurse -Force
```

**Final Structure:**
```
C:\cursor\cursor-archon\
├── ARCHON\                         ← PROJECT ROOT
│   ├── .env                        ← Create in Phase 2
│   ├── .venv312\                   ← Create in Phase 1.2
│   ├── docker-compose.yml
│   ├── python\
│   │   ├── pyproject.toml
│   │   ├── src\
│   │   └── tests\
│   ├── archon-ui-main\
│   │   ├── package.json
│   │   └── src\
│   ├── docs\
│   ├── migration\
│   │   └── complete_setup.sql
│   └── README.md
├── REPO\                           ← Original (can archive)
└── user_markdowns\                 ← Documentation
```

### 1.2 Create Python 3.12 Virtual Environment
```powershell
cd C:\cursor\cursor-archon\ARCHON

# Create venv
py -3.12 -m venv .venv312

# Activate venv (do this in every new terminal)
.\.venv312\Scripts\Activate.ps1

# Verify activation
python --version    # Should show Python 3.12.x
which python        # Should point to .venv312
```

**PowerShell Execution Policy (if activation fails):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 1.3 Install Python Package Manager (uv)
```powershell
# With venv activated
pip install uv

# Verify
uv --version
```

---

## Phase 2: Supabase Database Setup (Fresh Project)

### 2.1 Create New Supabase Project
1. Go to: https://supabase.com/dashboard
2. Click **"New Project"**
3. Choose organization (or create one)
4. Project settings:
   - **Name**: `archon-knowledge` (or your choice)
   - **Database Password**: Generate strong password (save it!)
   - **Region**: Choose closest to you
   - **Pricing Plan**: Free tier is fine
5. Wait ~2 minutes for project creation

### 2.2 Get Supabase Credentials
1. In your new project, go to: **Settings → API**
2. Copy these values (you'll need them for `.env`):
   - **Project URL**: `https://xxxxx.supabase.co`
   - **Project API keys** → **`service_role`** key (NOT anon!)
     - ⚠️ **CRITICAL**: Use the LONGER key labeled `service_role`
     - ❌ **DO NOT use**: `anon` (public) key

### 2.3 Run Database Setup Script
1. In Supabase dashboard, go to: **SQL Editor** (left sidebar)
2. Click **"New Query"**
3. Open local file: `C:\cursor\cursor-archon\ARCHON\migration\complete_setup.sql`
4. Copy entire contents and paste into SQL Editor
5. Click **"Run"** (or press F5)
6. Wait ~30 seconds for execution
7. **Verify Success**: Should see "Success. No rows returned" or similar

**What This Creates:**
- ✅ PostgreSQL extensions (pgvector, pg_trgm)
- ✅ `archon_settings` table (credentials & config)
- ✅ `sources` table (crawled websites & documents)
- ✅ `documents` table (text chunks with embeddings)
- ✅ `code_examples` table (extracted code snippets)
- ✅ `archon_projects` & `archon_tasks` tables (project management)
- ✅ Initial settings with default values

---

## Phase 3: Environment Configuration

### 3.1 Create `.env` File
```powershell
cd C:\cursor\cursor-archon\ARCHON

# Copy template
Copy-Item .env.example .env

# Open in editor
code .env
# or: notepad .env
```

### 3.2 Configure Essential Variables
```env
# ========================================
# REQUIRED: Supabase Credentials
# ========================================
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=eyJhbG...your-service-role-key-here

# ========================================
# REQUIRED: OpenAI API Key (or use Ollama)
# ========================================
OPENAI_API_KEY=sk-proj-...your-openai-key

# ========================================
# OPTIONAL: Monitoring (Pydantic Logfire)
# ========================================
LOGFIRE_TOKEN=
LOG_LEVEL=INFO

# ========================================
# Service Ports (defaults work fine)
# ========================================
HOST=localhost
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_AGENTS_PORT=8052
ARCHON_UI_PORT=3737
ARCHON_DOCS_PORT=3838

# ========================================
# Feature Flags
# ========================================
AGENTS_ENABLED=false    # Set to true if using AI agents service

# ========================================
# Frontend Configuration
# ========================================
VITE_SHOW_DEVTOOLS=false
PROD=false
```

**Note on API Keys:**
- **OpenAI**: Get from https://platform.openai.com/api-keys
- **Alternative**: Use Ollama (free, local) - configure in UI later

---

## Phase 4: Install Python Dependencies

### 4.1 Install Backend Dependencies
```powershell
cd C:\cursor\cursor-archon\ARCHON\python

# Ensure venv is activated
.\.venv312\Scripts\Activate.ps1

# Install all dependencies (server + mcp + agents + dev)
uv sync --group all

# This installs:
# - FastAPI, uvicorn (web framework)
# - Supabase client
# - OpenAI SDK
# - Crawl4AI (web crawling)
# - Document processing (pypdf2, python-docx, etc.)
# - Testing tools (pytest)
# - All MCP and agents dependencies
```

**Expected Output:**
```
Resolved XX packages in X.XXs
Installed XX packages in X.XXs
```

### 4.2 Verify Python Installation
```powershell
# Check installed packages
uv pip list

# Should see: fastapi, supabase, openai, crawl4ai, mcp, etc.
```

---

## Phase 5: Install Frontend Dependencies

### 5.1 Install Node Packages
```powershell
cd C:\cursor\cursor-archon\ARCHON\archon-ui-main

# Install all dependencies
npm install

# This installs:
# - React 18.3, React Router
# - TanStack Query (data fetching)
# - Radix UI (component library)
# - Tailwind CSS, Framer Motion
# - TypeScript, Vite
```

**Expected Duration**: 2-5 minutes depending on network

### 5.2 Verify Installation
```powershell
# Check for node_modules
ls node_modules

# Verify key packages
npm list react @tanstack/react-query
```

---

## Phase 6: Docker Setup

### 6.1 Build Docker Images
```powershell
cd C:\cursor\cursor-archon\ARCHON

# Build all services
docker compose build

# This builds:
# - archon-server (FastAPI backend)
# - archon-mcp (MCP server)
# - archon-frontend (React UI)
# - archon-agents (optional AI service)
```

**Expected Duration**: 5-10 minutes (first time)

### 6.2 Start Services
```powershell
# Start all services in detached mode
docker compose up -d

# Check running containers
docker compose ps

# Expected output:
# NAME                STATUS              PORTS
# archon-server       Up X minutes        0.0.0.0:8181->8181/tcp
# archon-mcp          Up X minutes        0.0.0.0:8051->8051/tcp
# archon-ui           Up X minutes        0.0.0.0:3737->3737/tcp
```

### 6.3 Verify Services Health
```powershell
# API Server
curl http://localhost:8181/health
# Expected: {"status":"healthy"}

# MCP Server
curl http://localhost:8051/health
# Expected: {"status":"ok"}

# Frontend (open in browser)
start http://localhost:3737

# View logs if any issues
docker compose logs -f archon-server
docker compose logs -f archon-mcp
```

---

## Phase 7: Initial Configuration via Web UI

### 7.1 Access Web Interface
```powershell
# Open in default browser
start http://localhost:3737
```

### 7.2 Configure Settings
1. **Navigate to Settings** (gear icon or `/settings`)
2. **Add OpenAI API Key** (if not in `.env`):
   - Go to: Settings → API Keys
   - Enter your OpenAI key
   - Click "Save"
3. **Verify Database Connection**:
   - Settings should show "Connected" status
   - If not, check Supabase credentials in `.env`

### 7.3 Start MCP Server
1. **Navigate to MCP Dashboard** (`/mcp`)
2. Click **"Start MCP Server"**
3. Verify status shows "Running"
4. **Copy MCP Configuration** for Cursor (we'll use this in Phase 8)

---

## Phase 8: MCP Client Configuration (Cursor IDE)

### 8.1 Locate Cursor MCP Config
```powershell
# Open config file
code C:\Users\wenge\.cursor\mcp.json

# If file doesn't exist, create it:
New-Item -ItemType File -Force -Path "$env:USERPROFILE\.cursor\mcp.json"
```

### 8.2 Add Archon MCP Server

**Edit `mcp.json`:**
```json
{
  "mcpServers": {
    "context7": {
      // ... your existing Context7 config (keep as-is)
    },
    "archon": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "-e", "TRANSPORT=stdio",
        "-e", "HOST=localhost",
        "-e", "PORT=8051",
        "archon-mcp",
        "python", "src/mcp_server.py"
      ]
    }
  }
}
```

**If Context7 doesn't have memory/Redis configured:**
```json
{
  "mcpServers": {
    "archon": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "-e", "TRANSPORT=stdio",
        "-e", "HOST=localhost",
        "-e", "PORT=8051",
        "archon-mcp",
        "python", "src/mcp_server.py"
      ]
    }
  }
}
```

### 8.3 Restart Cursor
1. Close Cursor completely
2. Reopen Cursor
3. Verify MCP connection:
   - Look for Archon tools in MCP tools panel
   - Should see 14 tools available

---

## Phase 9: Testing & Verification

### 9.1 Test Web Crawling
1. **Open Web UI**: http://localhost:3737
2. **Navigate to**: Knowledge Base → Crawl Website
3. **Test URL**: `https://docs.pydantic.dev/latest/`
4. **Monitor Progress**: Should see real-time updates
5. **Verify Completion**: Check for success message

### 9.2 Test Document Upload
1. **Navigate to**: Knowledge Base → Upload Document
2. **Select a test PDF** (any small PDF file)
3. **Add tags**: "test", "documentation"
4. **Upload**: Verify processing completes
5. **Check Results**: Document should appear in knowledge base

### 9.3 Test RAG Search
1. **Navigate to**: Knowledge Base → Search
2. **Enter query**: "what is pydantic" (or relevant to your uploaded content)
3. **Verify Results**: Should return relevant chunks with sources
4. **Check Performance**: Search should complete in <2 seconds

### 9.4 Test MCP Tools (From Cursor)
**In Cursor chat, try:**
```
Use archon to search for "validation" in the knowledge base
```

**Expected Behavior:**
- Cursor calls `archon:rag_search_knowledge_base` tool
- Returns relevant documentation chunks
- Shows source attribution

**Test All 14 Tools:**
```
# List available sources
Use archon to list all available knowledge sources

# Search code examples
Use archon to find Python code examples related to validation

# Create a project (if projects enabled)
Use archon to create a new project called "Test Project"
```

### 9.5 Test Projects & Tasks (Optional)
1. **Navigate to**: Projects
2. **Create Test Project**: Click "New Project"
3. **Add Tasks**: Create sample tasks
4. **Test MCP Integration**: From Cursor, ask archon to list projects
5. **Verify Sync**: Changes should appear in both UI and MCP

---

## Phase 10: Context7 Integration Verification

### 10.1 Check Existing Context7 Setup
```powershell
# Read your existing Cursor MCP config
Get-Content C:\Users\wenge\.cursor\mcp.json | jq .mcpServers.context7

# If jq not installed:
type C:\Users\wenge\.cursor\mcp.json
```

### 10.2 Verify Both MCP Servers Work
**In Cursor, test both:**
```
# Test Context7 (if configured)
Use context7 to store this information: "Archon setup completed on [today's date]"

# Test Archon
Use archon to search the knowledge base for "pydantic"
```

**Expected Result:**
- Both MCP servers respond independently
- No conflicts
- Each serves its specific purpose

### 10.3 Integration Architecture
```
Your Cursor IDE
      ↓
      ├─→ Context7 MCP Server (Session Memory / Redis)
      │     └─→ Stores conversation context & continuity
      │
      └─→ Archon MCP Server (Knowledge Base / Supabase)
            └─→ RAG search, documents, projects, tasks
```

**No Migration Needed**: These run independently and serve different purposes.

---

## Development Workflows

### Option A: Hybrid Mode (Recommended for Development)
**Backend in Docker, Frontend Local:**
```powershell
# Terminal 1: Start backend services only
docker compose --profile backend up -d

# Terminal 2: Run frontend locally (hot reload)
cd archon-ui-main
npm run dev

# Access: http://localhost:5173 (Vite dev server)
```

**Pros:**
- ✅ Instant frontend hot reload
- ✅ Better debugging with React DevTools
- ✅ Backend services isolated in Docker

### Option B: Full Docker Mode (Recommended for Testing)
```powershell
# Start all services in Docker
docker compose up -d

# Access: http://localhost:3737 (containerized frontend)
```

**Pros:**
- ✅ Production-like environment
- ✅ Consistent across machines
- ✅ Easy to share/deploy

### Option C: Full Local Development
```powershell
# Terminal 1: Run backend locally (with venv)
cd python
..\..\.venv312\Scripts\Activate.ps1
uvicorn src.server.main:app --reload --port 8181

# Terminal 2: Run MCP server locally
cd python
..\..\.venv312\Scripts\Activate.ps1
python -m src.mcp_server.main

# Terminal 3: Run frontend locally
cd archon-ui-main
npm run dev
```

**Pros:**
- ✅ Full control and debugging
- ✅ No Docker overhead
- ❌ **Cons**: Need to manage 3+ terminals, database connections, etc.

---

## Troubleshooting

### Issue: Docker Container Won't Start
```powershell
# Check logs
docker compose logs archon-server

# Common issues:
# 1. Port already in use
netstat -ano | findstr :8181

# 2. Environment variables not set
docker compose exec archon-server env | Select-String "SUPABASE"

# 3. Rebuild containers
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Issue: Python Module Not Found
```powershell
# Verify venv is activated
python --version    # Should show 3.12.x
which python        # Should point to .venv312

# Reinstall dependencies
cd python
uv sync --group all
```

### Issue: Supabase Connection Failed
```powershell
# Test connection
curl -H "apikey: YOUR_SERVICE_KEY" `
     "$env:SUPABASE_URL/rest/v1/archon_settings"

# Check .env file
Get-Content .env | Select-String "SUPABASE"

# Verify credentials in Supabase dashboard
```

### Issue: MCP Server Not Showing in Cursor
1. **Restart Cursor completely**
2. **Check Docker container running**: `docker ps | Select-String archon-mcp`
3. **Verify mcp.json syntax**: `Get-Content ~/.cursor/mcp.json | ConvertFrom-Json`
4. **Check Cursor logs**: `%APPDATA%\Cursor\logs\`

### Issue: Frontend Can't Connect to Backend
```powershell
# Check backend is running
curl http://localhost:8181/health

# Check proxy configuration in vite.config.ts
# Should proxy /api to http://localhost:8181
```

---

## Quick Reference Commands

### Daily Usage
```powershell
# Activate Python venv
cd C:\cursor\cursor-archon\ARCHON
.\.venv312\Scripts\Activate.ps1

# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f

# Restart specific service
docker compose restart archon-server
```

### Health Checks
```powershell
# API Server
curl http://localhost:8181/health

# MCP Server
curl http://localhost:8051/health

# Frontend
start http://localhost:3737

# All containers
docker compose ps
```

### Development Commands
```powershell
# Backend: Run tests
cd python
pytest tests/

# Backend: Lint code
ruff check src/

# Backend: Type check
mypy src/

# Frontend: Run tests
cd archon-ui-main
npm test

# Frontend: Lint code
npm run lint

# Frontend: Build production
npm run build
```

---

## Success Criteria Checklist

### ✅ Phase Completion Checklist
- [ ] Python 3.12 installed and venv created
- [ ] Supabase project created and `complete_setup.sql` executed
- [ ] `.env` file configured with valid credentials
- [ ] Python dependencies installed (`uv sync --group all`)
- [ ] Node.js dependencies installed (`npm install`)
- [ ] Docker containers built and running
- [ ] All health checks pass (API, MCP, Frontend)
- [ ] Web UI accessible at http://localhost:3737
- [ ] MCP server configured in Cursor `mcp.json`
- [ ] Successfully crawled at least one documentation site
- [ ] Successfully uploaded at least one document
- [ ] RAG search returns relevant results
- [ ] Archon MCP tools visible and working in Cursor
- [ ] Context7 and Archon both working (if Context7 configured)

### ✅ Final Verification
```powershell
# All services healthy
docker compose ps    # All should show "Up" status

# Test API
curl http://localhost:8181/health | ConvertFrom-Json

# Test MCP
curl http://localhost:8051/health | ConvertFrom-Json

# Test Frontend
start http://localhost:3737

# Test from Cursor
# In Cursor chat: "Use archon to list available sources"
```

---

## Estimated Timeline

| Phase | Task | Duration |
|-------|------|----------|
| 0 | Prerequisites & Python 3.12 install | 15 min |
| 1 | Repository setup & venv creation | 10 min |
| 2 | Supabase project & database setup | 10 min |
| 3 | Environment configuration | 5 min |
| 4 | Python dependencies installation | 10 min |
| 5 | Frontend dependencies installation | 5 min |
| 6 | Docker build & service startup | 15 min |
| 7 | Initial UI configuration | 5 min |
| 8 | MCP client configuration | 5 min |
| 9 | Testing & verification | 15 min |
| 10 | Context7 integration check | 5 min |
| **Total** | | **~90 minutes** |

---

## Next Steps After Setup

1. **Build Your Knowledge Base**:
   - Crawl your project documentation sites
   - Upload relevant PDFs and documents
   - Organize with tags and categories

2. **Optimize RAG Settings** (in Web UI):
   - Enable/disable contextual embeddings
   - Configure hybrid search
   - Tune reranking settings

3. **Integrate with Workflows**:
   - Use Archon from Cursor for code documentation
   - Create projects for active work
   - Track tasks via MCP tools

4. **Explore Advanced Features**:
   - Code example extraction
   - Version control for documents
   - Custom RAG strategies

---

## Support & Resources

- **Local Documentation**: http://localhost:3838 (when running)
- **API Documentation**: http://localhost:8181/docs
- **GitHub Repository**: https://github.com/coleam00/archon
- **GitHub Issues**: https://github.com/coleam00/archon/issues
- **In-Repo Guide**: `C:\cursor\cursor-archon\ARCHON\CLAUDE.md`

---

## Notes

- **Python 3.11 vs 3.12**: Project requires 3.12+ (specified in `pyproject.toml`)
- **Context7**: Runs independently, no migration or integration needed
- **Neo4j**: Not used by Archon (uses Supabase); your existing Neo4j setup unaffected
- **Windows Paths**: Use forward slashes in configs, they work in PowerShell 7
- **Line Endings**: Git may need `git config core.autocrlf false` if issues occur

---

**Ready to execute when Python 3.12 installation is complete!** 🚀