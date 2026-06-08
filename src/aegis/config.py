from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AEGIS_", extra="ignore")
    jwt_secret: str = "dev-secret-change-me"
    jwt_alg: str = "HS256"
    jwt_audience: str = "aegis"
    upstream_url: str = "http://upstreams:9000"
    redis_url: str = "redis://redis:6379/0"
    cache_ttl: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()