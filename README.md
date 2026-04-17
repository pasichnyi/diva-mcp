# DiVA MCP server

A small MCP server for the DiVA / Cora REST API, ready to open in VS Code and deploy to Render.

## What it exposes

- `diva_get_config`
- `diva_read_record`
- `diva_list_records`
- `diva_incoming_links`
- `diva_search_records`
- `diva_create_record`
- `diva_update_record`
- `diva_delete_record`

These map to the DiVA/Cora REST API endpoints documented by Uppsala University, including `/record/{type}/{id}`, `/record/{type}/`, `/record/{type}/{id}/incomingLinks`, and `/searchResult/{searchId}`. Auth is passed as `authToken`. See the official docs for payload shapes and media types.

## Local development in VS Code

1. Open this folder in VS Code.
2. Open a terminal in VS Code.
3. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the server:

```bash
python -m app.server
```

6. Check health:

```bash
curl http://localhost:8000/health
```

## Use it as a remote MCP server

After deployment, your MCP endpoint will be:

```text
https://YOUR-SERVICE.onrender.com/
```

If your client expects a dedicated path, you can later remount the MCP app at `/mcp`.

## Push to GitHub from VS Code

In the VS Code terminal:

```bash
git init
git add .
git commit -m "Initial DiVA MCP server"
git branch -M main
git remote add origin https://github.com/YOUR-USER/diva-mcp.git
git push -u origin main
```

Or in VS Code:

- Open **Source Control**
- Click **Initialize Repository** if needed
- Stage all changes
- Commit
- Publish to GitHub

## Deploy to Render

Render currently documents free web services, which makes it a simple option for a hobby or test deployment.

1. Create a GitHub repo and push this code.
2. Sign in to Render.
3. Click **New +** → **Blueprint** or **Web Service**.
4. Select your GitHub repo.
5. If using Blueprint, Render will read `render.yaml` automatically.
6. Set the environment variable `DIVA_AUTH_TOKEN` in Render if your DiVA instance requires it.
7. Deploy.

## Notes

- Free instances are not suitable for production.
- Some DiVA operations require a valid auth token.
- Search payloads and record payloads must match the Cora schema your DiVA installation expects.
- The MCP Python SDK supports stdio, SSE, and Streamable HTTP transports, and this repo uses an HTTP deployment approach suitable for cloud hosting.
