"""
App settings file. Don't touch anything.
Import `config` from settings and nothing more.
"""

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class PostgresData(BaseSettings):
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


class AppSettings(BaseSettings):
    """Main project settings."""

    debug: bool = True
    name: str = "Dilivery app"
    version: str = "0.1.0"
    docs_url: str = "/docs/"
    database: DatabaseSettings = DatabaseSettings()


config: AppSettings = AppSettings()
