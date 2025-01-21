from pydantic_settings import BaseSettings

class UserConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "USER_"
        extra = "ignore"

    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    
user_config = UserConfig()