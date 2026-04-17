from __future__ import annotations

import os
from typing import Any, Optional

import httpx

DIVA_BASE_URL = os.getenv("DIVA_BASE_URL", "https://diva.cora.epc.ub.uu.se/rest").rstrip("/")
DIVA_AUTH_TOKEN = os.getenv("DIVA_AUTH_TOKEN")
DEFAULT_ACCEPT = "application/vnd.cora.record+json, application/vnd.cora.recordList+json, application/json"


def _headers(accept: Optional[str] = None) -> dict[str, str]:
    headers = {"Accept": accept or DEFAULT_ACCEPT}
    if DIVA_AUTH_TOKEN:
        headers["authToken"] = DIVA_AUTH_TOKEN
    return headers


async def diva_request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: Any = None,
    content: bytes | str | None = None,
    content_type: str | None = None,
    accept: str | None = None,
) -> dict[str, Any]:
    url = f"{DIVA_BASE_URL}/{path.lstrip('/')}"
    headers = _headers(accept)
    if content_type:
        headers["Content-Type"] = content_type

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            content=content,
            headers=headers,
        )

    resp.raise_for_status()

    content_type = resp.headers.get("content-type", "").lower()
    data: Any
    if "json" in content_type:
        data = resp.json()
    elif content_type.startswith("text/"):
        data = resp.text
    else:
        data = {
            "binary": True,
            "content_type": content_type,
            "size_bytes": len(resp.content),
        }

    return {
        "status_code": resp.status_code,
        "url": str(resp.request.url),
        "data": data,
    }
