import pathlib
from typing import Any

from pydantic import BaseModel, PostgresDsn, AmqpDsn, RedisDsn

from pydantic_settings import BaseSettings, SettingsConfigDict

BASEDIR = pathlib.Path(__file__).parent.parent


class ApiV1(BaseModel):
    prefix: str = "/v1"


class Rabbit(BaseModel):
    url: AmqpDsn
    exchange_name: str = "appointments.events"
    routing_key: str = "appointment.created"


class RedisSettings(BaseModel):
    ttl: int = 60 * 60 * 24  # 24 hours
    url: RedisDsn


class Database(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_pre_ping: bool = True
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def naming_convention(self) -> dict[str, str]:
        return {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }

    @property
    def engine_kwargs(self) -> dict[str, Any]:
        return {
            "echo_pool": self.echo_pool,
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "pool_pre_ping": self.pool_pre_ping,
        }


class Uvicorn(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    api_v1: ApiV1 = ApiV1()
    uvicorn: Uvicorn = Uvicorn()
    db: Database
    redis: RedisSettings
    rabbit: Rabbit


settings = Settings()  # type: ignore
