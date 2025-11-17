from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = 80
    database_url: str = 'sqlite:///../../database.sqlite3'

    jwt_sercret: str = 'I9b1WCWByTM9D6DOIDi-yTRQsieCZgNAaUzdaqwqc_Q'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600

settings = Settings()