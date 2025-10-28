 Archon Installation & Configuration Plan                                                                                                   │
     │                                                                                                                                            │
     │ Repository Overview                                                                                                                        │
     │                                                                                                                                            │
     │ Archon is a knowledge management MCP server that connects AI IDEs (Cursor, Windsurf, Claude Code) to your centralized knowledge base with: │
     │ - Web crawling & document processing (PDF, DOCX, MD)                                                                                       │
     │ - RAG (Retrieval Augmented Generation) search with vector embeddings                                                                       │
     │ - Project & task management                                                                                                                │
     │ - Real-time updates via Socket.IO                                                                                                          │
     │ - 14 MCP tools for AI agent integration                                                                                                    │
     │                                                                                                                                            │
     │ Architecture: Microservices (FastAPI backend, React frontend, MCP server, AI agents service)                                               │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 1: Environment Prerequisites & Verification                                                                                          │
     │                                                                                                                                            │
     │ 1. Verify Node.js 18+ installation (required for frontend)                                                                                 │
     │   - Check: node --version and npm --version                                                                                                │
     │   - Install if missing: <https://nodejs.org>                                                                                                 │
     │ 2. Verify Python 3.12+ installation                                                                                                        │
     │   - Check: python --version                                                                                                                │
     │   - Install if missing: <https://python.org>                                                                                                 │
     │ 3. Install uv package manager (recommended for Python deps)                                                                                │
     │   - pip install uv or use official installer                                                                                               │
     │   - Alternative: Use pip/poetry if preferred                                                                                               │
     │ 4. Verify Docker Desktop is running                                                                                                        │
     │   - Already confirmed available                                                                                                            │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 2: Repository Setup                                                                                                                  │
     │                                                                                                                                            │
     │ 1. Move/Clone repository from extraction to your project directory                                                                         │
     │   - Copy from: c:\cursor\cursor-archon\REPO\Archon-main\Archon-main\                                                                       │
     │   - To: c:\cursor\cursor-archon\ (clean structure)                                                                                         │
     │ 2. Initialize Git (if forking)                                                                                                             │
     │   - Remove existing .git folder                                                                                                            │
     │   - Initialize fresh repo: git init                                                                                                        │
     │   - Add remote to your fork                                                                                                                │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 3: Supabase Database Setup                                                                                                           │
     │                                                                                                                                            │
     │ 1. Create Supabase project (free tier)                                                                                                     │
     │   - Go to <https://supabase.com>                                                                                                             │
     │   - Create new project                                                                                                                     │
     │ 2. Get credentials from Settings → API                                                                                                     │
     │   - Copy SUPABASE_URL                                                                                                                      │
     │   - Copy service_role key (NOT anon key - critical!)                                                                                       │
     │ 3. Run database migrations in SQL Editor                                                                                                   │
     │   - Execute migration/complete_setup.sql                                                                                                   │
     │   - This creates all tables, functions, and initial settings                                                                               │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 4: Environment Configuration                                                                                                         │
     │                                                                                                                                            │
     │ 1. Create .env file from template                                                                                                          │
     │ cp .env.example .env                                                                                                                       │
     │ 2. Configure essential variables:                                                                                                          │
     │ SUPABASE_URL=<https://your-project.supabase.co>                                                                                              │
     │ SUPABASE_SERVICE_KEY=your-service-role-key                                                                                                 │
     │                                                                                                                                            │
     │ # Optional but recommended                                                                                                                 │
     │ OPENAI_API_KEY=sk-your-key  # Or use Ollama/Gemini                                                                                         │
     │ LOGFIRE_TOKEN=  # Optional monitoring                                                                                                      │
     │ LOG_LEVEL=INFO                                                                                                                             │
     │                                                                                                                                            │
     │ # Ports (defaults work fine)                                                                                                               │
     │ HOST=localhost                                                                                                                             │
     │ ARCHON_SERVER_PORT=8181                                                                                                                    │
     │ ARCHON_MCP_PORT=8051                                                                                                                       │
     │ ARCHON_AGENTS_PORT=8052                                                                                                                    │
     │ ARCHON_UI_PORT=3737                                                                                                                        │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 5: Install Dependencies                                                                                                              │
     │                                                                                                                                            │
     │ Python (Backend):                                                                                                                          │
     │ cd python                                                                                                                                  │
     │ uv sync --group all  # Installs all dependencies                                                                                           │
     │ # OR: pip install -e ".[all]"                                                                                                              │
     │                                                                                                                                            │
     │ Node.js (Frontend):                                                                                                                        │
     │ cd archon-ui-main                                                                                                                          │
     │ npm install                                                                                                                                │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 6: Docker Setup                                                                                                                      │
     │                                                                                                                                            │
     │ 1. Build and start services:                                                                                                               │
     │ docker compose up --build -d                                                                                                               │
     │ 2. Verify services:                                                                                                                        │
     │   - Frontend UI: <http://localhost:3737>                                                                                                     │
     │   - API Server: <http://localhost:8181/health>                                                                                               │
     │   - MCP Server: <http://localhost:8051/health>                                                                                               │
     │   - Agents: <http://localhost:8052/health> (optional)                                                                                        │
     │ 3. Check logs if issues:                                                                                                                   │
     │ docker compose logs -f archon-server                                                                                                       │
     │ docker compose logs -f archon-mcp                                                                                                          │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 7: Initial Configuration via UI                                                                                                      │
     │                                                                                                                                            │
     │ 1. Open Web Interface: <http://localhost:3737>                                                                                               │
     │ 2. Go to Settings → Add API keys (OpenAI, etc.)                                                                                            │
     │ 3. Start MCP Server from MCP Dashboard                                                                                                     │
     │ 4. Test crawling: Knowledge Base → Crawl a docs site                                                                                       │
     │ 5. Test upload: Upload a test PDF                                                                                                          │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 8: Context7 MCP Integration (Optional)                                                                                               │
     │                                                                                                                                            │
     │ Considerations:                                                                                                                            │
     │ - Context7 provides session memory/continuity with Redis backend                                                                           │
     │ - You have Neo4j available (may be useful for graph memory)                                                                                │
     │ - Two integration approaches:                                                                                                              │
     │                                                                                                                                            │
     │ Option A: Separate Context7 Setup                                                                                                          │
     │ - Keep Context7 as separate MCP server                                                                                                     │
     │ - Configure in global Cursor MCP config alongside Archon                                                                                   │
     │ - Both servers run independently                                                                                                           │
     │                                                                                                                                            │
     │ Option B: Integrated with Archon                                                                                                           │
     │ - Add Context7 as additional service in docker-compose.yml                                                                                 │
     │ - Share database/networking with Archon                                                                                                    │
     │ - More complex but unified deployment                                                                                                      │
     │                                                                                                                                            │
     │ Recommendation: Start with Option A (separate), assess integration needs later                                                             │
     │                                                                                                                                            │
     │ Configuration Location:                                                                                                                    │
     │ - Cursor: C:\Users\wenge\.cursor\mcp.json                                                                                                  │
     │ - Add both Archon and Context7 servers in same config                                                                                      │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 9: MCP Client Configuration (Cursor/Windsurf)                                                                                        │
     │                                                                                                                                            │
     │ For Cursor (~/.cursor/mcp.json):                                                                                                           │
     │ {                                                                                                                                          │
     │   "mcpServers": {                                                                                                                          │
     │     "archon": {                                                                                                                            │
     │       "command": "docker",                                                                                                                 │
     │       "args": [                                                                                                                            │
     │         "exec", "-i",                                                                                                                      │
     │         "-e", "TRANSPORT=stdio",                                                                                                           │
     │         "-e", "HOST=localhost",                                                                                                            │
     │         "-e", "PORT=8051",                                                                                                                 │
     │         "archon-mcp",                                                                                                                      │
     │         "python", "src/mcp_server.py"                                                                                                      │
     │       ]                                                                                                                                    │
     │     }                                                                                                                                      │
     │   }                                                                                                                                        │
     │ }                                                                                                                                          │
     │                                                                                                                                            │
     │ Note: This connects to the running Docker container                                                                                        │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Phase 10: Testing & Verification                                                                                                           │
     │                                                                                                                                            │
     │ 1. Test knowledge crawl: Crawl a small docs site                                                                                           │
     │ 2. Test RAG search: Query your knowledge base                                                                                              │
     │ 3. Test MCP tools: From Cursor/Windsurf, test Archon tools                                                                                 │
     │ 4. Test projects: Create a test project and tasks                                                                                          │
     │ 5. Monitor logs: Check for errors in Docker logs                                                                                           │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Additional Recommendations                                                                                                                 │
     │                                                                                                                                            │
     │ Windows-Specific Considerations:                                                                                                           │
     │ - Use PowerShell 7 (you already have this setup)                                                                                           │
     │ - Line endings: Git may need core.autocrlf=false                                                                                           │
     │ - Docker Desktop: WSL2 backend recommended                                                                                                 │
     │ - Path handling: Forward slashes work in PowerShell 7                                                                                      │
     │                                                                                                                                            │
     │ Neo4j Utilization:                                                                                                                         │
     │ - Archon uses Supabase (PostgreSQL + pgvector), not Neo4j                                                                                  │
     │ - Your existing Neo4j can remain for Context7/Graphiti                                                                                     │
     │ - Consider separate graph memory architecture if needed                                                                                    │
     │                                                                                                                                            │
     │ Development Workflow:                                                                                                                      │
     │ - Hybrid mode: Backend in Docker, frontend local for hot reload                                                                            │
     │ docker compose --profile backend up -d                                                                                                     │
     │ cd archon-ui-main && npm run dev                                                                                                           │
     │ - Full Docker mode: All services in containers                                                                                             │
     │ docker compose up -d                                                                                                                       │
     │                                                                                                                                            │
     │ Tools You Already Have:                                                                                                                    │
     │ - fd, ripgrep (rg), ast-grep, fzf - useful for codebase navigation                                                                         │
     │ - PowerShell 7 with modern CLI tools - optimal for this project                                                                            │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Troubleshooting Resources                                                                                                                  │
     │                                                                                                                                            │
     │ - Documentation: <http://localhost:3838> (after startup)                                                                                     │
     │ - API Docs: <http://localhost:8181/docs>                                                                                                     │
     │ - GitHub Issues: <https://github.com/coleam00/archon/issues>                                                                                 │
     │ - CLAUDE.md: In-repo development guide                                                                                                     │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Estimated Time                                                                                                                             │
     │                                                                                                                                            │
     │ - Prerequisites check: 10-15 minutes                                                                                                       │
     │ - Repository setup: 5 minutes                                                                                                              │
     │ - Supabase setup: 10 minutes                                                                                                               │
     │ - Configuration: 15 minutes                                                                                                                │
     │ - Installation: 20-30 minutes (depending on network)                                                                                       │
     │ - Testing: 15 minutes                                                                                                                      │
     │ - Total: 75-90 minutes                                                                                                                     │
     │                                                                                                                                            │
     │ ---                                                                                                                                        │
     │ Success Criteria                                                                                                                           │
     │                                                                                                                                            │
     │ ✅ All Docker services running and healthy                                                                                                  │
     │ ✅ Web UI accessible and responsive                                                                                                         │
     │ ✅ Successfully crawled at least one documentation site                                                                                     │
     │ ✅ MCP server connected to Cursor/Windsurf                                                                                                  │
     │ ✅ RAG search returns relevant results                                                                                                      │
     │ ✅ Can create projects and tasks
