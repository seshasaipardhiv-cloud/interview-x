import os
import sys
import asyncio
from typing import Any
import httpx2
from mcp.client.streamable_http import streamable_http_client
from mcp.client.session import ClientSession
from mcp.server import MCPServer
import mcp.types as types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("BREETH_API_KEY")
if not API_KEY:
    print("Error: BREETH_API_KEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

BASE_URL = os.getenv("BREETH_BASE_URL", "https://mcp.thebreeth.com/mcp")

mcp = MCPServer("breeth-local-bridge")
upstream_session = None

async def proxy_list_tools(ctx: Any, params: types.PaginatedRequestParams | None) -> types.ListToolsResult:
    if not upstream_session:
        # Fallback empty response
        return types.ListToolsResult(tools=[])
    try:
        return await upstream_session.list_tools(params=params)
    except Exception as e:
        # On error returning empty list is safe
        return types.ListToolsResult(tools=[])

async def proxy_call_tool(ctx: Any, params: types.CallToolRequestParams) -> types.CallToolResult | types.InputRequiredResult:
    if not upstream_session:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text="Error: Not connected to upstream Breeth server.")],
            is_error=True
        )
    
    try:
        return await upstream_session.call_tool(params.name, params.arguments or {})
    except Exception as e:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"Upstream Tool Failure: {type(e).__name__} - {str(e)}")],
            is_error=True
        )

# Override default tool handlers to proxy dynamically
mcp._lowlevel_server.add_request_handler("tools/list", types.PaginatedRequestParams, proxy_list_tools)
mcp._lowlevel_server.add_request_handler("tools/call", types.CallToolRequestParams, proxy_call_tool)

async def run_server():
    global upstream_session
    
    http_client = httpx2.AsyncClient(
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30.0
    )
    
    try:
        async with streamable_http_client(BASE_URL, http_client=http_client) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                try:
                    await session.initialize()
                    upstream_session = session
                    
                    # Run the downstream stdio server once upstream is connected
                    await mcp.run_stdio_async()
                    
                except Exception as e:
                    print(f"Error initializing upstream Breeth MCP session: {e}", file=sys.stderr)
                    sys.exit(1)
    except Exception as e:
        print(f"Upstream Breeth MCP connection failure: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_server())