from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(...)

    model_config = {
        "env_file": ".env",
    }

settings = Settings()
