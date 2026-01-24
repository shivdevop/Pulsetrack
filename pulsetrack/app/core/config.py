from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(...)
    DATABASE_URL_SYNC: str= Field(...)
    ACCESS_TOKEN_SECRET_KEY: str = Field(...)
    ALGORITHM: str= Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int=Field(...)
    REFRESH_TOKEN_EXPIRE_DAYS: int=Field(...)

    model_config = {
        "env_file": ".env",
    }

settings = Settings()
