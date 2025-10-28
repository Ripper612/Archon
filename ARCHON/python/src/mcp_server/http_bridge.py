"""
HTTP Bridge for MCP Tools - Allows agents to call MCP tools via HTTP

This provides a simple HTTP API that agents can use to call MCP tools,
bridging the gap between the agents (which expect JSON-RPC over HTTP)
and the MCP server (which uses FastMCP with SSE).
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Add the project root to Python path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# We'll call server endpoints directly instead of importing MCP tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Archon MCP HTTP Bridge",
    description="HTTP API bridge for MCP tools used by agents",
    version="1.0.0",
)


@app.post("/rpc")
async def rpc_endpoint(request: dict):
    """JSON-RPC endpoint for agents to call MCP tools."""
    try:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id", 1)

        if not method:
            return JSONResponse(
                status_code=400,
                content={
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32600, "message": "Method not specified"},
                },
            )

        # Route to server endpoints based on method name
        try:
            # Get server URL from environment
            server_host = os.getenv("ARCHON_SERVER_PORT", "8181")
            server_url = f"http://archon-server:{server_host}"

            if method == "perform_rag_query":
                # Call RAG query endpoint
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{server_url}/api/rag/query",
                        json={
                            "query": params.get("query", ""),
                            "source_id": params.get("source"),
                            "match_count": params.get("match_count", 5),
                        },
                    )
                    response.raise_for_status()
                    result = response.json()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": json.dumps(result),
                    }

            elif method == "get_available_sources":
                # Call sources endpoint
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{server_url}/api/rag/sources")
                    response.raise_for_status()
                    result = response.json()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": json.dumps(result),
                    }

            elif method == "search_code_examples":
                # Call code examples search endpoint
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{server_url}/api/rag/code-examples",
                        json={
                            "query": params.get("query", ""),
                            "source_id": params.get("source_id"),
                            "match_count": params.get("match_count", 5),
                        },
                    )
                    response.raise_for_status()
                    result = response.json()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": json.dumps(result),
                    }

            elif method == "manage_project":
                # Call project management endpoint
                async with httpx.AsyncClient() as client:
                    action = params.get("action")
                    if action == "create":
                        response = await client.post(
                            f"{server_url}/api/projects",
                            json={k: v for k, v in params.items() if k != "action"},
                        )
                    elif action == "get":
                        project_id = params.get("project_id")
                        response = await client.get(
                            f"{server_url}/api/projects/{project_id}"
                        )
                    else:
                        # For other actions, use PATCH
                        project_id = params.get("project_id", "")
                        response = await client.patch(
                            f"{server_url}/api/projects/{project_id}",
                            json={k: v for k, v in params.items() if k != "action"},
                        )
                    response.raise_for_status()
                    result = response.json()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": json.dumps(result),
                    }

            elif method == "manage_task":
                # Call task management endpoint
                async with httpx.AsyncClient() as client:
                    action = params.get("action")
                    project_id = params.get("project_id", "")
                    if action == "create":
                        response = await client.post(
                            f"{server_url}/api/projects/{project_id}/tasks",
                            json={
                                k: v
                                for k, v in params.items()
                                if k not in ["action", "project_id"]
                            },
                        )
                    else:
                        task_id = params.get("task_id", "")
                        response = await client.patch(
                            f"{server_url}/api/projects/{project_id}/tasks/{task_id}",
                            json={
                                k: v
                                for k, v in params.items()
                                if k not in ["action", "project_id", "task_id"]
                            },
                        )
                    response.raise_for_status()
                    result = response.json()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": json.dumps(result),
                    }

            elif method == "manage_document":
                # Call document management endpoint
                async with httpx.AsyncClient() as client:
                    action = params.get("action")
                    project_id = params.get("project_id", "")
                    if action == "create":
                        response = await client.post(
                            f"{server_url}/api/projects/{project_id}/documents",
                            json={
                                k: v
                                for k, v in params.items()
                                if k not in ["action", "project_id"]
                            },
                        )
                    else:
                        doc_id = params.get("doc_id", "")
                        response = await client.patch(
                            f"{server_url}/api/projects/{project_id}/documents/{doc_id}",
                            json={
                                k: v
                                for k, v in params.items()
                                if k not in ["action", "project_id", "doc_id"]
                            },
                        )
                    response.raise_for_status()
                    result = response.json()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": json.dumps(result),
                    }

            else:
                return JSONResponse(
                    status_code=404,
                    content={
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method '{method}' not found",
                        },
                    },
                )

        except Exception as tool_error:
            logger.error(f"Error calling MCP tool {method}: {tool_error}")
            return JSONResponse(
                status_code=500,
                content={
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32603, "message": str(tool_error)},
                },
            )

    except Exception as e:
        logger.error(f"RPC endpoint error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": "Internal server error"},
            },
        )


@app.get("/health")
async def health_endpoint():
    """Health check endpoint."""
    return {"status": "healthy", "service": "mcp-http-bridge", "tools_available": True}


if __name__ == "__main__":
    # Get port from environment or default
    port = int(os.getenv("ARCHON_MCP_HTTP_PORT", "8053"))

    logger.info(f"Starting MCP HTTP Bridge on port {port}")
    uvicorn.run(
        "src.mcp_server.http_bridge:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False,
    )
