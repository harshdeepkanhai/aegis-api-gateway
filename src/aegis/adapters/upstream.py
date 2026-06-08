import json, httpx, redis.asyncio as aioredis
from aegis.config import get_settings


class UpstreamClient:
    def __init__(self) -> None:
        s = get_settings()
        self._http = httpx.AsyncClient(base_url=s.upstream_url, timeout=5.0)
        self._redis = aioredis.from_url(s.redis_url, decode_responses=True)
        self._ttl = s.cache_ttl
        self._fails = 0  # circuit-breaker stub: open after N consecutive failures

    async def _get(self, path: str, params: dict | None = None) -> object:
        key = f"cache:{path}:{json.dumps(params, sort_keys=True)}"
        if (hit := await self._redis.get(key)) is not None:
            return json.loads(hit)
        if self._fails >= 5:
            raise RuntimeError("upstream circuit open")
        try:
            resp = await self._http.get(path, params=params)
            resp.raise_for_status()
            self._fails = 0
        except httpx.HTTPError:
            self._fails += 1
            raise
        data = resp.json()
        await self._redis.set(key, json.dumps(data), ex=self._ttl)
        return data

    async def list_authors(self) -> list[dict]:
        return await self._get("/authors")  # type: ignore[return-value]

    async def books_for_authors(self, author_ids: list[int]) -> list[dict]:
        ids = ",".join(map(str, author_ids))
        return await self._get("/books", {"author_ids": ids})  # type: ignore[return-value]