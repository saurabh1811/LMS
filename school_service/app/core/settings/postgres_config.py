from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field, BaseModel, SecretStr
from pydantic import BaseSettings, PostgresDsn, validator


class PostgresConfig(BaseSettings):
    POSTGRES_SERVER: str = "35.239.96.148"
    POSTGRES_USER: str = "root"
    POSTGRES_PASSWORD: str ="admin"
    POSTGRES_DB: str = "postgres"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )