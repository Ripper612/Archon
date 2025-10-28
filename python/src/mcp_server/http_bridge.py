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

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Add the project root to Python path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import MCP tool functions
from src.mcp_server.features.rag.rag_tools import (
    rag_search_knowledge_base,
    rag_get_available_sources,
    rag_search_code_examples,
)
from src.mcp_server.features.projects.project_tools import manage_project
from src.mcp_server.features.tasks.task_tools import manage_task
from src.mcp_server.features.documents.document_tools import manage_document

# Import context and client
from src.mcp_server.mcp_server import ArchonContext
from mcp.server.fastmcp import Context

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

        # Create context for MCP tools
        context = ArchonContext(
            service_client=None
        )  # MCP tools handle their own HTTP calls
        mcp_context = Context(deps=context)

        # Route to appropriate MCP tool based on method name
        try:
            if method == "perform_rag_query":
                result = await rag_search_knowledge_base(
                    mcp_context,
                    query=params.get("query", ""),
                    source_id=params.get("source"),
                    match_count=params.get("match_count", 5),
                )
                return {"jsonrpc": "2.0", "id": request_id, "result": result}

            elif method == "get_available_sources":
                result = await rag_get_available_sources(mcp_context)
                return {"jsonrpc": "2.0", "id": request_id, "result": result}

            elif method == "search_code_examples":
                result = await rag_search_code_examples(
                    mcp_context,
                    query=params.get("query", ""),
                    source_id=params.get("source_id"),
                    match_count=params.get("match_count", 5),
                )
                return {"jsonrpc": "2.0", "id": request_id, "result": result}

            elif method == "manage_project":
                result = await manage_project(
                    mcp_context,
                    action=params.get("action"),
                    **{k: v for k, v in params.items() if k != "action"},
                )
                return {"jsonrpc": "2.0", "id": request_id, "result": result}

            elif method == "manage_document":
                result = await manage_document(
                    mcp_context,
                    action=params.get("action"),
                    project_id=params.get("project_id"),
                    **{
                        k: v
                        for k, v in params.items()
                        if k not in ["action", "project_id"]
                    },
                )
                return {"jsonrpc": "2.0", "id": request_id, "result": result}

            elif method == "manage_task":
                result = await manage_task(
                    mcp_context,
                    action=params.get("action"),
                    project_id=params.get("project_id"),
                    **{
                        k: v
                        for k, v in params.items()
                        if k not in ["action", "project_id"]
                    },
                )
                return {"jsonrpc": "2.0", "id": request_id, "result": result}

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
