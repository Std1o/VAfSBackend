from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = 80

    @property
    def database_url(self) -> str:
        # Если запущено в Docker
        if os.path.exists('/.dockerenv'):
            return 'sqlite:///./database.sqlite3'
        else:
            return 'sqlite:///../../database.sqlite3'

    jwt_sercret: str = 'I9b1WCWByTM9D6DOIDi-yTRQsieCZgNAaUzdaqwqc_Q'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600

settings = Settings()