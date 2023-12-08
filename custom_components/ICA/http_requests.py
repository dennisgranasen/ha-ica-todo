from __future__ import annotations
from typing import Any, Dict
from requests import Session
import json
from .const import AUTH_TICKET

CONTENT_TYPE = ("Content-Type", "application/json; charset=utf-8")
AUTHORIZATION = (AUTH_TICKET, "%s")
X_REQUEST_ID = ("X-Request-Id", "%s")


def create_headers(
    auth_key: str | None = None,
    with_content: bool = False,
    request_id: str | None = None,
) -> Dict[str, str]:
    headers: Dict[str, str] = {}

    if auth_key:
        headers.update([(AUTHORIZATION[0], AUTHORIZATION[1] % auth_key)])
    if with_content:
        headers.update([CONTENT_TYPE])
    if request_id:
        headers.update([(X_REQUEST_ID[0], X_REQUEST_ID[1] % request_id)])
    return headers


def get(
    session: Session,
    url: str,
    auth_key: str | None = None,
    params: Dict[str, Any] | None = None,
):
    response = session.get(url, params=params, headers=create_headers(auth_key=auth_key))

    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


def post(
    session: Session,
    url: str,
    auth_key: str | None = None,
    data: Dict[str, Any] | None = None,
):
    request_id = data.pop("request_id", None) if data else None

    headers = create_headers(
        auth_key=auth_key, with_content=True if data else False, request_id=request_id
    )

    response = session.post(
        url,
        headers=headers,
        data=json.dumps(data) if data else None,
    )

    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


def delete(
    session: Session,
    url: str,
    auth_key: str | None = None,
    args: Dict[str, Any] | None = None,
):
    request_id = args.pop("request_id", None) if args else None

    headers = create_headers(auth_key=auth_key, request_id=request_id)

    response = session.delete(
        url,
        headers=headers,
    )

    response.raise_for_status()
    return response.ok