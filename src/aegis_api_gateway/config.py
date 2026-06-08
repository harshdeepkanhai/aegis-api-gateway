from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    service_name: str = "service"
    log_level: str = "INFO"
    # subclass per repo with DB/broker URLs, secrets, etc.


@lru_cache
def get_settings() -> Settings:
    return Settings()