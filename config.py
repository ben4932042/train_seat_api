from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    host: str = "127.0.0.1"
    port: str = "6379"
    user: str = ''
    password: str = ''
    db: int = 0
    class Config:
        env_file = ".env"

settings = RedisSettings()
