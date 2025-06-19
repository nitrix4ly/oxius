import asyncio
import ssl
from urllib.parse import urlparse
from .response import Response
from .exceptions import HTTPException
from .utils import build_headers
from .cache import exiosCache

class ClientSession:
    def __init__(self, default_headers=None, timeout=10, cache_enabled=True):
        self.default_headers = {
            "User-Agent": "oxius/1.0",
            "Accept": "*/*",
            "Connection": "close"
        }
        if default_headers:
            self.default_headers.update(default_headers)
        self.timeout = timeout
        self.cache = exiosCache() if cache_enabled else None

    async def request(self, method, url, headers=None, body=None):
        method = method.upper()
        cache_key = f"{method}:{url}"
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached:
                return Response(cached.encode())

        parsed = urlparse(url)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        path = parsed.path or "/"
        if parsed.query:
            path += f"?{parsed.query}"
        scheme = parsed.scheme

        ssl_context = ssl.create_default_context() if scheme == "https" else None

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port, ssl=ssl_context),
                timeout=self.timeout
            )

            payload = body.encode("utf-8") if body else None
            request_data = build_headers(method, host, path, self.default_headers, headers, payload)

            writer.write(request_data.encode("utf-8"))
            if payload:
                writer.write(payload)
            await writer.drain()

            raw_data = b""
            try:
                while True:
                    chunk = await asyncio.wait_for(reader.read(4096), timeout=self.timeout)
                    if not chunk:
                        break
                    raw_data += chunk
            except asyncio.TimeoutError:
                writer.close()
                await writer.wait_closed()
                raise HTTPException("Timeout while reading response")

            writer.close()
            await writer.wait_closed()

        except asyncio.TimeoutError:
            raise HTTPException("Connection timed out")
        except Exception as e:
            raise HTTPException(f"Request failed: {e}")

        if self.cache:
            self.cache.set(cache_key, raw_data.decode(errors="ignore"))

        return Response(raw_data)

    async def get(self, url, headers=None):
        return await self.request("GET", url, headers=headers)

    async def post(self, url, headers=None, body=None):
        return await self.request("POST", url, headers=headers, body=body)

    async def put(self, url, headers=None, body=None):
        return await self.request("PUT", url, headers=headers, body=body)

    async def delete(self, url, headers=None):
        return await self.request("DELETE", url, headers=headers)

    async def head(self, url, headers=None):
        return await self.request("HEAD", url, headers=headers)

    async def options(self, url, headers=None):
        return await self.request("OPTIONS", url, headers=headers)

    def close(self):
        pass
