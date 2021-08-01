from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field, BaseModel, SecretStr
from pydantic import BaseSettings, PostgresDsn, validator

class JWTConfig(BaseSettings):
    secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm = "HS256"
    access_token_expire_minutes = 86400