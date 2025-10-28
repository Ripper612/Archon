# 🎯 Using Archon Features in Other Repositories

This guide shows how to integrate Archon's powerful AI and knowledge management features into your other projects and repositories.

## Table of Contents
- [MCP Integration (Recommended)](#1--mcp-integration-recommended)
- [API Integration](#2--api-integration)
- [Knowledge Base Integration](#3--knowledge-base-integration)
- [Development Workflow Integration](#4---development-workflow-integration)
- [CI/CD Integration](#5---cicd-integration)
- [UI Integration](#6---ui-integration)
- [Monitoring & Analytics](#7---monitoring--analytics)
- [Setup Checklist](#setup-checklist-for-new-repository)
- [Quick Start](#quick-start-for-new-projects)

## 1. 🚀 MCP Integration (Recommended)

### Connect AI IDEs to Archon's Knowledge Base

**For Cursor:**
```json
// .cursor/settings.json or MCP settings
{
  "mcpServers": {
    "archon": {
      "uri": "http://localhost:8051/sse"
    }
  }
}
```

**For Windsurf:**
```json
{
  "mcp.servers": {
    "archon": {
      "uri": "http://localhost:8051/sse"
    }
  }
}
```

**For Claude Code:**
```bash
claude mcp add --transport sse archon http://localhost:8051/sse
```

### Available MCP Tools in Your IDE:
- 🧠 **RAG Search**: `perform_rag_query(query="your question")`
- 📝 **Code Search**: `search_code_examples(query="pattern")`
- 🌐 **Web Crawling**: `crawl_single_page(url="https://example.com")`
- 📊 **Project Management**: `manage_project(action="create", title="My Project")`
- 📋 **Task Tracking**: `manage_task(action="create", project_id="...", title="My Task")`

## 2. 🔗 API Integration

### Direct REST API Access

**Base URL:** `http://localhost:8181/api`

**Key Endpoints:**
```bash
# Knowledge Base
GET  /api/knowledge/search?q=your+query
POST /api/knowledge/crawl  # Crawl websites
POST /api/knowledge/upload # Upload documents

# Projects & Tasks
GET  /api/projects
POST /api/projects
GET  /api/projects/{id}/tasks
POST /api/projects/{id}/tasks

# Health Check
GET  /api/health
```

**Example API Usage:**
```python
import requests

# Search knowledge base
response = requests.get("http://localhost:8181/api/knowledge/search",
                       params={"q": "authentication patterns"})
results = response.json()

# Create a project
project_data = {"title": "My Project", "description": "Project description"}
response = requests.post("http://localhost:8181/api/projects",
                        json=project_data)
```

## 3. 📚 Knowledge Base Integration

### Access Crawled Content

**Search Examples:**
- Technical documentation you've crawled
- Code snippets with AI-generated summaries
- Web pages indexed with embeddings
- Custom documents you've uploaded

**Query Types:**
```bash
# Semantic search
GET /api/knowledge/search?q=authentication+JWT

# Code-specific search
GET /api/knowledge/search?type=code&language=python

# Source filtering
GET /api/knowledge/search?source_id=your-source-id
```

## 4. 🛠️ Development Workflow Integration

### Project Management

Use Archon to track development tasks across repositories:

```bash
# Create project for your other repo
curl -X POST http://localhost:8181/api/projects \
  -H "Content-Type: application/json" \
  -d '{"title": "My Other Project", "description": "Features for repo XYZ"}'

# Add tasks
curl -X POST http://localhost:8181/api/projects/{project-id}/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Implement feature X", "status": "todo"}'
```

### Document Versioning

Track changes to specifications, designs, and documentation:

```bash
# Upload and version documents
curl -X POST http://localhost:8181/api/projects/{project-id}/documents \
  -F "file=@requirements.md" \
  -F "title=Requirements v2.0"
```

## 5. 🔄 CI/CD Integration

### Automated Knowledge Updates

Add to your CI pipeline:

```yaml
# .github/workflows/update-knowledge.yml
name: Update Knowledge Base
on:
  push:
    paths:
      - 'docs/**'
      - 'README.md'

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - name: Update Archon Knowledge
        run: |
          curl -X POST http://your-archon-instance:8181/api/knowledge/upload \
            -F "file=@README.md" \
            -F "source_type=documentation"
```

## 6. 🎨 UI Integration

### Embed Archon Components

If building a web app, you can integrate Archon's UI components:

```bash
# Install as dependency (if published)
npm install @archon/ui-components

# Or embed via iframe
<iframe src="http://localhost:3737/embed/search" width="100%" height="400px"></iframe>
```

## 7. 📊 Monitoring & Analytics

### Access Archon Metrics

```bash
# Health and performance metrics
GET /api/health

# Tool usage statistics
GET /api/analytics/tools

# Search analytics
GET /api/analytics/searches
```

## Setup Checklist for New Repository:

- ✅ **Start Archon**: `cd ARCHON && docker-compose up -d`
- ✅ **Configure MCP**: Add Archon to your IDE's MCP settings
- ✅ **Test Connection**: Try `perform_rag_query(query="test")` in your IDE
- ✅ **API Access**: Verify `http://localhost:8181/api/health` responds
- ✅ **Documentation**: Upload your repo's docs to Archon's knowledge base

## Quick Start for New Projects:

1. **Start Archon** (if not already running)
2. **Connect your IDE** via MCP
3. **Upload project documentation** to knowledge base
4. **Create project structure** in Archon for task tracking
5. **Begin development** with AI assistance from your knowledge base

## Prerequisites for Integration

- **Archon Instance**: Running on your local machine or server
- **MCP-Compatible IDE**: Cursor, Windsurf, or Claude Desktop
- **Network Access**: Your development environment can reach Archon's ports
- **API Credentials**: For direct API integration (optional)

## Troubleshooting Integration

### MCP Connection Issues
```bash
# Check Archon MCP server health
curl http://localhost:8051/health

# Verify SSE endpoint
curl -N http://localhost:8051/sse
```

### API Access Problems
```bash
# Test basic connectivity
curl http://localhost:8181/api/health

# Check CORS settings if using browser
curl -H "Origin: http://localhost:3000" http://localhost:8181/api/health
```

### Knowledge Base Empty
```bash
# Upload documentation
curl -X POST http://localhost:8181/api/knowledge/upload \
  -F "file=@README.md"

# Crawl websites
curl -X POST http://localhost:8181/api/knowledge/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.example.com"}'
```

## Advanced Integration Patterns

### Custom MCP Tools
Create tools that integrate with your specific workflow:

```python
# In your MCP server integration
@tool
def search_my_project_docs(query: str) -> str:
    """Search documentation specific to my project"""
    # Use Archon API to search
    response = requests.get(f"http://localhost:8181/api/knowledge/search",
                          params={"q": query, "source_id": "my-project-docs"})
    return response.json()
```

### Automated Project Tracking
```python
# Git hooks integration
#!/bin/bash
# .git/hooks/post-commit

# Auto-update task status in Archon
curl -X PATCH http://localhost:8181/api/projects/$PROJECT_ID/tasks/$TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

## Security Considerations

- **Network Security**: Ensure Archon ports are only accessible from trusted networks
- **API Authentication**: Use proper authentication for production API access
- **Data Privacy**: Be aware of what data is indexed in the knowledge base
- **Rate Limiting**: Implement appropriate rate limits for API usage

---

**Archon transforms any repository into an AI-powered development environment with comprehensive knowledge management, project tracking, and intelligent assistance!** 🚀

*Last updated: October 26, 2025*
