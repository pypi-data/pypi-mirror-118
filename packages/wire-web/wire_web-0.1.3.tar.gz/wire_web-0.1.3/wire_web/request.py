from urllib.parse import parse_qsl
import json
from typing import Optional
from multidict import CIMultiDict
from wire_web.typings import CoroutineFunction
from http.cookies import SimpleCookie
from enum import Enum


class ConnectionType(Enum):
    http: str = "http"
    ws: str = "websocket"


class Request:
    asgi3 = "ASGI3"
    asgi2 = "ASGI2"

    def __init__(
        self,
        scope: dict,
        receive: Optional[CoroutineFunction] = None,
        send: Optional[CoroutineFunction] = None,
    ) -> None:
        self._receive = receive
        self._send = send

        # request fields
        self._scope = scope
        self._req_headers: Optional[CIMultiDict] = None
        self._req_cookies: SimpleCookie = SimpleCookie()
        self.http_body = b""
        self.http_has_more_body = True
        self.http_received_body_length = 0

    @property
    def path(self) -> str:
        return self._scope["path"]

    @property
    def method(self) -> str:
        return self._scope["method"].lower()

    @property
    def client(self) -> str:
        return self._scope["client"]

    @property
    def server(self) -> str:
        return self._scope["server"]

    @property
    def headers(self) -> CIMultiDict:
        if not self._req_headers:
            self._req_headers = CIMultiDict(
                [(k.decode("ascii"), v.decode("ascii")) for (k, v) in self._scope["headers"]])
        return self._req_headers

    @property
    def cookies(self) -> SimpleCookie:
        if not self._req_headers:
            self._req_cookies.load(self._req_headers.get("cookie", {}))
        return self._req_cookies

    @property
    def cookies_dict(self) -> dict:
        return {key: m.value for key, m in self._req_cookies.items()}

    @property
    def scope(self) -> dict:
        return self._scope

    @property
    def query(self) -> dict:
        return CIMultiDict(parse_qsl(self.scope.get("query_string", b"").decode("utf-8")))

    @property
    def type(self) -> ConnectionType:
        return ConnectionType.ws if self.scope.get("type") == "websocket" else ConnectionType.http

    async def body_iter(self):
        if not self.type == ConnectionType.http:
            raise Exception("ConnectionType is not http")
        if self.http_received_body_length > 0 and self.http_has_more_body:
            raise Exception("body iter is already started and is not finished")
        if self.http_received_body_length > 0 and not self.http_has_more_body:
            yield self.http_body
        req_body_length = (
            int(self.headers.get("content-length", "0"))
            if not self.headers.get("transfer-encoding") == "chunked"
            else None
        )
        while self.http_has_more_body:
            if req_body_length and self.http_received_body_length > req_body_length:
                raise Exception("body is longer than excepted")
            message = await self._receive()
            message_type = message.get("type")
            await self.handle(message)
            if message_type != "http.request":
                continue
            chunk = message.get("body", b"")
            if not isinstance(chunk, bytes):
                raise RuntimeError("Chunk is not bytes")
            self.http_body += chunk
            self.http_has_more_body = message.get("more_body", False)
            self.http_received_body_length += len(chunk)
            yield chunk

    async def body(self) -> bytes:
        data: bytes = b"".join([chunks async for chunks in self.body_iter()])
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            return data

    async def handle(self, message):
        if message.get("type") == "http.disconnect":
            raise Exception("Disconnected")
