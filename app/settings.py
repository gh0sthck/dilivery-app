"""
App settings file. Don't touch anything.
Import `config` from settings and nothing more.
"""

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    "Database connection settings."
    dsn: str = "sqlite+aiosqlite:///database.db"


class AppSettings(BaseSettings):
    """Main project settings."""

    debug: bool = True
    name: str = "Dilivery app"
    version: str = "0.1.0"
    docs_url: str = "/docs/"
    database: DatabaseSettings = DatabaseSettings()


config: AppSettings = AppSettings()
