from pydantic_settings import BaseSettings

class GlobalConfig(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str
    SECRET_KEY: str
    ALGORITHM: str
    AUTH_TOKEN_URL: str
    DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEVICE_STATUS_EXPIRE_SECONDS: int

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_prefix": "GLOBAL_",
        "extra": "ignore"
    }

global_config = GlobalConfig()