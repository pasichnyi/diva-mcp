# DiVA MCP Server

This repository provides an MCP (Model Context Protocol) server for interacting with the DiVA / Cora REST API.

It exposes DiVA functionality as MCP tools that can be used by compatible MCP clients and LLM applications.

## Deployed endpoint

Public MCP endpoint:

```text
https://diva-mcp.onrender.com/mcp
```

## Available tools

The server currently exposes these MCP tools:

- `diva_get_config`
- `diva_read_record`
- `diva_list_records`
- `diva_incoming_links`
- `diva_search_records`
- `diva_create_record`
- `diva_update_record`
- `diva_delete_record`

These tools wrap DiVA/Cora REST endpoints such as `/record/{type}/{id}`, `/record/{type}/`, `/record/{type}/{id}/incomingLinks`, and `/searchResult/{searchId}`.

## How to use the deployed server

This is a remote MCP server. Its URL is:

```text
https://diva-mcp.onrender.com/mcp
```

To use it, your client must support MCP over HTTP and follow the normal MCP lifecycle:

1. `initialize`
2. `notifications/initialized`
3. `tools/list` or `tools/call`

Requests must include these headers:

```text
Content-Type: application/json
Accept: application/json, text/event-stream
```

After `initialize`, reuse the returned `Mcp-Session-Id` header in subsequent requests.

## Testing with curl

### 1. Initialize a session

```bash
curl -i -X POST https://diva-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"initialize",
    "params":{
      "protocolVersion":"2025-03-26",
      "capabilities":{},
      "clientInfo":{"name":"curl","version":"1.0"}
    }
  }'
```

Copy the `Mcp-Session-Id` value from the response headers.

### 2. Send initialized notification

```bash
curl -i -X POST https://diva-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: YOUR_SESSION_ID" \
  -d '{
    "jsonrpc":"2.0",
    "method":"notifications/initialized"
  }'
```

### 3. List available tools

```bash
curl -i -X POST https://diva-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: YOUR_SESSION_ID" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/list"
  }'
```

### 4. Call a tool

Example using `diva_get_config`:

```bash
curl -i -X POST https://diva-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: YOUR_SESSION_ID" \
  -d '{
    "jsonrpc":"2.0",
    "id":3,
    "method":"tools/call",
    "params":{
      "name":"diva_get_config",
      "arguments":{}
    }
  }'
```

### 5. One-shot shell test

```bash
RESP=$(curl -s -D /tmp/diva_headers.txt -X POST https://diva-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}')

SESSION_ID=$(grep -i '^mcp-session-id:' /tmp/diva_headers.txt | awk '{print $2}' | tr -d '\r')

curl -s -X POST https://diva-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' > /dev/null

curl -s -X POST https://diva-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

## Example MCP responses

A successful deployment should allow:

- `initialize` → `200 OK` and an `Mcp-Session-Id`
- `notifications/initialized` → `202 Accepted`
- `tools/list` → a list of exposed tools
- `tools/call` → structured tool output or a structured error

## Using it with MCP clients

### ChatGPT

If your ChatGPT account has custom MCP / Apps developer access, add the server using:

```text
https://diva-mcp.onrender.com/mcp
```

If you only see the consumer Apps UI and no way to create a custom connection, your account likely does not yet have that feature enabled.

### Claude Desktop

Add this to your MCP configuration:

```json
{
  "mcpServers": {
    "diva": {
      "url": "https://diva-mcp.onrender.com/mcp"
    }
  }
}
```

### Python example

```python
import requests

URL = "https://diva-mcp.onrender.com/mcp"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}

resp = requests.post(
    URL,
    headers=headers,
    json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "python", "version": "1.0"},
        },
    },
)

session_id = resp.headers["mcp-session-id"]
headers["Mcp-Session-Id"] = session_id

requests.post(
    URL,
    headers=headers,
    json={
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
    },
)

resp = requests.post(
    URL,
    headers=headers,
    json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "diva_get_config",
            "arguments": {},
        },
    },
)

print(resp.text)
```

## Local development

Open the folder in VS Code and run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.server
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.server
```

Local MCP endpoint:

```text
http://localhost:8000/mcp
```

## Deployment notes

The server is currently deployed on Render.

Important deployment requirements:

- bind to `0.0.0.0`
- use the `PORT` environment variable provided by the platform
- serve HTTPS via the hosting platform
- keep MCP host/origin security settings aligned with the deployed domain

## Notes and limitations

- Some DiVA operations require a valid `authToken`.
- `diva_search_records` requires a valid `search_id` and correctly formed XML payload.
- A fake `search_id` will produce an upstream 404 from DiVA, which is expected.
- Free cloud instances may sleep between requests and are not suitable for production workloads.
