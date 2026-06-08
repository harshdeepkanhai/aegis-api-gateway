from fastapi import Depends, FastAPI
from aegis.adapters.auth import CurrentUser, issue_dev_token, require_scope
from aegis.adapters.graphql import build_graphql_router
from aegis.adapters.upstream import UpstreamClient
from aegis.config import get_settings
from aegis.logging import configure_logging

configure_logging(get_settings().log_level)
app = FastAPI(title="aegis-api-gateway")
client = UpstreamClient()
app.include_router(build_graphql_router(client))


@app.post("/auth/token", tags=["dev"])
def dev_token() -> dict:
    return {"access_token": issue_dev_token("dev-user", ["read:authors"]), "token_type": "bearer"}


@app.get("/authors", tags=["rest-fallback"])  # auto-documented at /docs (OpenAPI/Swagger)
async def rest_authors(user: CurrentUser = Depends(require_scope("read:authors"))) -> list[dict]:
    return await client.list_authors()


@app.get("/healthz", tags=["ops"])
def healthz() -> dict:
    return {"status": "ok"}