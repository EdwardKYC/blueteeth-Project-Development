from pydantic_settings import BaseSettings

class GlobalConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "GLOBAL_"
        extra = "ignore"

    DATABASE_URL: str
    API_PREFIX: str
    SECRET_KEY: str
    ALGORITHM: str
    AUTH_TOKEN_URL: str
    DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES: int

global_config = GlobalConfig()