# Breeth Local MCP Bridge

This directory contains a lightweight Python stdio MCP server that acts as a bridge to the Breeth memory service REST API.

## Why a Bridge?
The direct Antigravity -> Breeth remote Streamable HTTP connection occasionally fails during the `notifications/initialized` phase. To ensure a stable connection while still utilizing Breeth's core endpoints, we implemented this local stdio bridge. Antigravity communicates with this bridge reliably over standard input/output (stdio), and the bridge translates those MCP tool calls into standard HTTP POST requests securely sent to Breeth's API.

## Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API key:
   - Copy `.env.example` to `.env`.
   - Add your `BREETH_API_KEY` to the `.env` file.
   - **Note:** The `.env` file is excluded via `.gitignore` to prevent leaking credentials.

## Usage

This bridge exposes 4 tools to the MCP client:
- `add_episode`: Corresponds to `POST /v1/episodes`
- `record_fact`: Corresponds to `POST /v1/facts`
- `search`: Corresponds to `POST /v1/search`
- `retract`: Corresponds to `POST /v1/retract`

The server runs on stdio:
```bash
python breeth_mcp.py
```

### IDE Configuration
In your MCP config, use the following configuration to point to this bridge:

```json
{
    "mcpServers": {
        "breeth-local": {
            "command": "python",
            "args": [
                "tools/breeth-mcp/breeth_mcp.py"
            ]
        }
    }
}
```
*Note: Make sure the command points to the python executable in the virtual environment where dependencies are installed if not installed globally.*

## Running Tests

Tests use `pytest` and mock HTTP endpoints to ensure no real network requests are made.

```bash
pytest test_breeth_mcp.py -v
```
