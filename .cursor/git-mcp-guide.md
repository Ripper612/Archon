# GitMCP Server Guide

## What is GitMCP?

GitMCP is a **remote Model Context Protocol (MCP) server** that transforms any GitHub repository into a documentation hub for AI assistants. It eliminates code hallucinations by providing access to up-to-date documentation and code directly from GitHub.

**Purpose**: Give AI assistants (Cursor, Claude, Windsurf, etc.) accurate, current information about any GitHub project without requiring the AI to have pre-trained knowledge.

## Setup (3 Options)

### Option 1: Specific Repository (Recommended)
```json
{
  "mcpServers": {
    "gitmcp": {
      "url": "https://gitmcp.io/{owner}/{repo}"
    }
  }
}
```
**Use when**: You work with specific libraries regularly.

### Option 2: Dynamic/Any Repository
```json
{
  "mcpServers": {
    "gitmcp": {
      "url": "https://gitmcp.io/docs"
    }
  }
}
```
**Use when**: You switch between different repositories frequently.

### Option 3: Via npx (Claude Desktop, Augment Code)
```json
{
  "mcpServers": {
    "gitmcp": {
      "command": "npx",
      "args": ["mcp-remote", "https://gitmcp.io/{owner}/{repo}"]
    }
  }
}
```

## Available Tools

### `fetch_<repo-name>_documentation`
**What**: Gets primary documentation (llms.txt → README.md → docs)
**When to use**: General questions about project purpose/features
**Example**: "What does this library do?"

### `search_<repo-name>_documentation`
**What**: Intelligent search through repository docs
**When to use**: Specific questions about features/functions
**Example**: "How do I configure authentication?"

### `search_<repo-name>_code`
**What**: Searches actual code using GitHub's code search
**When to use**: Need code examples or implementation details
**Example**: "Show me how to implement error handling"

### `fetch_url_content`
**What**: Retrieves content from links mentioned in docs
**When to use**: Documentation references external resources
**Example**: Following API reference links

## Tool Naming (Important!)

**For specific repo servers**: `fetch_tensorflow_documentation`, `search_tensorflow_code`
**For dynamic servers**: `fetch_generic_documentation`, `search_generic_code`

## When to Use GitMCP

✅ **New/niche libraries** - AI hasn't seen them before
✅ **Rapidly changing projects** - Need latest docs/code
✅ **Complex APIs** - Avoid hallucinated implementations
✅ **Code reviews** - Verify against actual documentation
✅ **Learning new tools** - Get accurate examples

❌ **Well-known libraries** - AI already knows these (React, Django, etc.)
❌ **Private repos** - Only works with public GitHub repos
❌ **Non-GitHub projects** - Only supports GitHub repositories

## Configuration Files by IDE

### Cursor: `~/.cursor/mcp.json`
### Windsurf: `~/.codeium/windsurf/mcp_config.json`
### VSCode: `.vscode/mcp.json`
### Claude Desktop: Settings → Developer → Edit Config

## Example Usage

**Prompt**: "How do I create a custom React hook for data fetching?"
- **Without GitMCP**: AI might give outdated or incorrect patterns
- **With GitMCP**: AI searches React docs/code and gives current best practices

**Result**: More accurate code, fewer debugging sessions, faster development.

## Cost & Privacy

- **Cost**: Completely free
- **Privacy**: No authentication required, no query storage, respects robots.txt
- **Data**: Only accesses public GitHub content when requested

## Quick Start

1. Pick a GitHub repo: `https://github.com/microsoft/vscode`
2. Convert to MCP URL: `https://gitmcp.io/microsoft/vscode`
3. Add to your IDE's MCP config
4. Ask AI: "How do I create VS Code extensions?"
5. AI will search VS Code docs/code for accurate answers

That's it! GitMCP turns any GitHub repository into an AI-accessible knowledge base.
