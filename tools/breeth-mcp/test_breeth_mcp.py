import pytest
from unittest.mock import AsyncMock
import mcp.types as types

@pytest.fixture
def mock_session():
    session = AsyncMock()
    # Mock session.list_tools
    session.list_tools.return_value = types.ListToolsResult(
        tools=[
            types.Tool(
                name="test_tool",
                description="Test",
                inputSchema={"type": "object", "properties": {}}
            )
        ]
    )
    # Mock session.call_tool
    session.call_tool.return_value = types.CallToolResult(
        content=[types.TextContent(type="text", text="Success")]
    )
    return session

@pytest.fixture
def mock_env_and_session(monkeypatch, mock_session):
    monkeypatch.setenv("BREETH_API_KEY", "test_key")
    import breeth_mcp
    monkeypatch.setattr(breeth_mcp, "API_KEY", "test_key")
    monkeypatch.setattr(breeth_mcp, "upstream_session", mock_session)
    return breeth_mcp, mock_session

@pytest.mark.asyncio
async def test_proxy_list_tools(mock_env_and_session):
    breeth_mcp, mock_session = mock_env_and_session
    
    result = await breeth_mcp.proxy_list_tools(None, None)
    
    assert len(result.tools) == 1
    assert result.tools[0].name == "test_tool"
    mock_session.list_tools.assert_called_once()

@pytest.mark.asyncio
async def test_proxy_call_tool(mock_env_and_session):
    breeth_mcp, mock_session = mock_env_and_session
    
    params = types.CallToolRequestParams(name="test_tool", arguments={"key": "value"})
    result = await breeth_mcp.proxy_call_tool(None, params)
    
    assert result.content[0].text == "Success"
    mock_session.call_tool.assert_called_once_with("test_tool", {"key": "value"})

@pytest.mark.asyncio
async def test_proxy_call_tool_error(mock_env_and_session):
    breeth_mcp, mock_session = mock_env_and_session
    
    # Setup error
    mock_session.call_tool.side_effect = Exception("Upstream tool crashed")
    
    params = types.CallToolRequestParams(name="test_tool", arguments={"key": "value"})
    result = await breeth_mcp.proxy_call_tool(None, params)
    
    assert result.is_error
    assert "Upstream tool crashed" in result.content[0].text

@pytest.mark.asyncio
async def test_no_upstream_connection(monkeypatch):
    import breeth_mcp
    monkeypatch.setattr(breeth_mcp, "upstream_session", None)
    
    # Test list_tools when disconnected
    list_result = await breeth_mcp.proxy_list_tools(None, None)
    assert len(list_result.tools) == 0
    
    # Test call_tool when disconnected
    params = types.CallToolRequestParams(name="test_tool", arguments={})
    call_result = await breeth_mcp.proxy_call_tool(None, params)
    assert call_result.is_error
    assert "Not connected" in call_result.content[0].text
