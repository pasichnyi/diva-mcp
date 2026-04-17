
from __future__ import annotations
import os

import json
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from app.diva_api import DEFAULT_ACCEPT, DIVA_AUTH_TOKEN, DIVA_BASE_URL, diva_request

mcp = FastMCP(
    "diva-api",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "localhost:*",
            "127.0.0.1:*",
            "diva-mcp.onrender.com",
            "diva-mcp.onrender.com:*",
        ],
        allowed_origins=[
            "http://localhost:*",
            "https://diva-mcp.onrender.com",
        ],
    ),
)


@mcp.tool()
def diva_get_config() -> dict[str, Any]:
    """Return current DiVA MCP configuration."""
    return {
        "base_url": DIVA_BASE_URL,
        "has_auth_token": bool(DIVA_AUTH_TOKEN),
        "accept_header": DEFAULT_ACCEPT,
    }


@mcp.tool()
async def diva_read_record(record_type: str, record_id: str) -> dict[str, Any]:
    """Read a single record from DiVA/Cora: GET /record/{type}/{id}"""
    return await diva_request("GET", f"record/{record_type}/{record_id}")


@mcp.tool()
async def diva_list_records(record_type: str, filter_xml: str | None = None) -> dict[str, Any]:
    """Read a list of records from DiVA/Cora: GET /record/{type}/?filter=<xml>"""
    params = {"filter": filter_xml} if filter_xml else None
    return await diva_request("GET", f"record/{record_type}/", params=params)


@mcp.tool()
async def diva_incoming_links(record_type: str, record_id: str) -> dict[str, Any]:
    """Read incoming links for a record: GET /record/{type}/{id}/incomingLinks"""
    return await diva_request("GET", f"record/{record_type}/{record_id}/incomingLinks")


@mcp.tool()
async def diva_search_records(search_id: str, search_data_xml: str) -> dict[str, Any]:
    """Search DiVA/Cora records: GET /searchResult/{searchId}?searchData=<xml>"""
    return await diva_request("GET", f"searchResult/{search_id}", params={"searchData": search_data_xml})


@mcp.tool()
async def diva_create_record(
    record_type: str,
    record_payload: dict[str, Any] | str,
    payload_format: Literal["json", "xml"] = "json",
) -> dict[str, Any]:
    """Create a record: POST /record/{type}"""
    if payload_format == "json":
        return await diva_request(
            "POST",
            f"record/{record_type}",
            json_body=record_payload,
            content_type="application/vnd.cora.recordgroup+json",
            accept="application/vnd.cora.record+json, application/json",
        )
    content = record_payload if isinstance(record_payload, str) else json.dumps(record_payload)
    return await diva_request(
        "POST",
        f"record/{record_type}",
        content=content,
        content_type="application/vnd.cora.recordgroup+xml",
        accept="application/vnd.cora.record+xml, application/xml",
    )


@mcp.tool()
async def diva_update_record(
    record_type: str,
    record_id: str,
    record_payload: dict[str, Any] | str,
    payload_format: Literal["json", "xml"] = "json",
) -> dict[str, Any]:
    """Update a record: POST /record/{type}/{id}"""
    if payload_format == "json":
        return await diva_request(
            "POST",
            f"record/{record_type}/{record_id}",
            json_body=record_payload,
            content_type="application/vnd.cora.recordgroup+json",
            accept="application/vnd.cora.record+json, application/json",
        )
    content = record_payload if isinstance(record_payload, str) else json.dumps(record_payload)
    return await diva_request(
        "POST",
        f"record/{record_type}/{record_id}",
        content=content,
        content_type="application/vnd.cora.recordgroup+xml",
        accept="application/vnd.cora.record+xml, application/xml",
    )


@mcp.tool()
async def diva_delete_record(record_type: str, record_id: str) -> dict[str, Any]:
    """Delete a record: DELETE /record/{type}/{id}"""
    return await diva_request("DELETE", f"record/{record_type}/{record_id}", accept="text/plain")


app = mcp.streamable_http_app()



if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
