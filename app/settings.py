"""
App settings file. Don't touch anything.
Import `config` from settings and nothing more.
"""

from pathlib import Path
from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

BASE_DIR = Path(__file__).parent


class PostgresData(BaseSettings):
    """PostgreSQL data to connection. Recevies date from env file."""
    NAME: str
    USER: str
    PASSWD: str
    HOST: str
    PORT: str

    model_config = SettingsConfigDict(env_file=".env")


class DatabaseSettings(BaseSettings):
    "Database connection settings."
    
    pg_data: PostgresData = PostgresData()
    postgres: PostgresDsn = (
        f"postgresql+asyncpg://{pg_data.USER}:{pg_data.PASSWD}"
        f"@{pg_data.HOST}:{pg_data.PORT}/{pg_data.NAME}"
    )

    @property
    def dsn(self) -> str:
        return self.postgres.unicode_string()


class JWTAuth(BaseSettings):
    """JWT authentication settings."""
    
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem" 
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 4


class LoggingSettings(BaseSettings):
    fmt: str = "[{levelname}] {asctime} {filename}, {lineno} | {message}"
    datefmt: str = "%H:%M:%S" 
    style: str = "{" 


class AppSettings(BaseSettings):
    """Main project settings."""

    debug: bool = True
    name: str = "Dilivery app"
    version: str = "0.2.0"
    docs_url: str = "/docs/"
    
    database: DatabaseSettings = DatabaseSettings()
    auth: JWTAuth = JWTAuth() 
    logs: LoggingSettings = LoggingSettings()

config: AppSettings = AppSettings()
