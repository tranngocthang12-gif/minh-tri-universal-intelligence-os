"""Authenticated loopback HTTP host for the read-only brain transport.

This is a local transport host, not a public service. It binds only to loopback,
uses a fixed brain path configured at process start, requires a bearer token,
and delegates only to BrainTransport's read-only method allowlist.
"""
from __future__ import annotations

import hmac
import ipaddress
import json
import threading
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .brain_transport import BrainTransport, BrainTransportError, PROTOCOL

HTTP_PROTOCOL = "minhtri-brain-http/v1"
PATH = "/v1/brain"
MAX_REQUEST_BYTES = 16 * 1024
MAX_RESPONSE_BYTES = 256 * 1024
MIN_TOKEN_CHARS = 32
BRAIN_TOKEN_ENV = "MINHTRI_BRAIN_TOKEN"


class BrainHTTPError(ValueError):
    pass


class _Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], transport: BrainTransport, token: str):
        super().__init__(address, _Handler)
        self.transport = transport
        self.token = token


class _Handler(BaseHTTPRequestHandler):
    server: _Server

    def log_message(self, format: str, *args: Any) -> None:
        # Do not leak bearer tokens, queries, or brain metadata to default stderr logs.
        return

    def _json(self, status: int, body: dict[str, Any]) -> None:
        raw = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        if len(raw) > MAX_RESPONSE_BYTES:
            status = 500
            raw = b'{"error":"RESPONSE_TOO_LARGE"}'
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self) -> None:
        if self.path != PATH:
            self._json(404, {"error": "NOT_FOUND"})
            return
        expected = "Bearer " + self.server.token
        provided = self.headers.get("Authorization", "")
        if not hmac.compare_digest(provided, expected):
            self._json(401, {"error": "UNAUTHORIZED"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._json(400, {"error": "INVALID_CONTENT_LENGTH"})
            return
        if length <= 0 or length > MAX_REQUEST_BYTES:
            self._json(413, {"error": "REQUEST_SIZE_INVALID"})
            return
        try:
            request = json.loads(self.rfile.read(length).decode("utf-8"))
            result = self.server.transport.dispatch(request)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"error": "INVALID_JSON"})
            return
        except BrainTransportError as exc:
            self._json(400, {"error": "TRANSPORT_REJECTED", "detail": str(exc)})
            return
        self._json(200, {"http_protocol": HTTP_PROTOCOL, **result})


class BrainHTTPHost:
    """Loopback-only authenticated host for BrainTransport."""

    def __init__(self, fixed_home: str | Path, token: str, host: str = "127.0.0.1", port: int = 0):
        try:
            if not ipaddress.ip_address(host).is_loopback:
                raise BrainHTTPError("brain HTTP host must bind to loopback")
        except ValueError as exc:
            raise BrainHTTPError("brain HTTP host must use a literal loopback address") from exc
        if not isinstance(token, str) or len(token) < MIN_TOKEN_CHARS:
            raise BrainHTTPError(f"token must be at least {MIN_TOKEN_CHARS} characters")
        if type(port) is not int or not 0 <= port <= 65535:
            raise BrainHTTPError("port must be an integer from 0 to 65535")
        self._server = _Server((host, port), BrainTransport(fixed_home), token)
        self._thread: threading.Thread | None = None

    @property
    def url(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}{PATH}"

    def start(self) -> "BrainHTTPHost":
        if self._thread is not None:
            raise BrainHTTPError("host already started")
        self._thread = threading.Thread(target=self._server.serve_forever, name="minhtri-brain-http", daemon=True)
        self._thread.start()
        return self

    def serve_forever(self) -> None:
        """Run the local host in the current process until interrupted."""
        if self._thread is not None:
            raise BrainHTTPError("host already started in background")
        try:
            self._server.serve_forever()
        finally:
            self._server.server_close()

    def close(self) -> None:
        if self._thread is not None:
            self._server.shutdown()
            self._thread.join(timeout=5)
            self._thread = None
        self._server.server_close()

    def __enter__(self) -> "BrainHTTPHost":
        return self.start()

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()


class BrainHTTPClient:
    """Minimal authenticated client suitable for a local connector process."""

    def __init__(self, url: str, token: str, timeout: float = 5.0):
        if not isinstance(url, str):
            raise BrainHTTPError("client URL must target loopback")
        try:
            parsed = urlsplit(url)
            port = parsed.port
            host = parsed.hostname
            address = ipaddress.ip_address(host) if host is not None else None
        except ValueError as exc:
            raise BrainHTTPError("client URL must target loopback") from exc
        if (
            parsed.scheme != "http"
            or address is None
            or not address.is_loopback
            or port is None
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path != PATH
            or parsed.query
            or parsed.fragment
        ):
            raise BrainHTTPError("client URL must target loopback")
        if not isinstance(token, str) or len(token) < MIN_TOKEN_CHARS:
            raise BrainHTTPError(f"token must be at least {MIN_TOKEN_CHARS} characters")
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise BrainHTTPError("timeout must be positive")
        self.url = url
        self.token = token
        self.timeout = float(timeout)

    def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({
            "protocol": PROTOCOL,
            "method": method,
            "params": params or {},
        }, separators=(",", ":")).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=payload,
            method="POST",
            headers={
                "Authorization": "Bearer " + self.token,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read(MAX_RESPONSE_BYTES + 1)
        except urllib.error.HTTPError as exc:
            detail = exc.read(MAX_RESPONSE_BYTES).decode("utf-8", "replace")
            raise BrainHTTPError(f"HTTP_{exc.code}: {detail}") from exc
        except OSError as exc:
            raise BrainHTTPError(f"CONNECT_FAILED: {exc}") from exc
        if len(raw) > MAX_RESPONSE_BYTES:
            raise BrainHTTPError("response exceeds client limit")
        try:
            body = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise BrainHTTPError("invalid JSON response") from exc
        if body.get("http_protocol") != HTTP_PROTOCOL or body.get("protocol") != PROTOCOL:
            raise BrainHTTPError("protocol mismatch")
        result = body.get("result")
        if not isinstance(result, dict):
            raise BrainHTTPError("missing result")
        return result
