"""
App settings file. Don't touch anything.
Import `config` from settings and nothing more.
"""
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    "Database connection settings." 
    ...


class AppSettings(BaseSettings):
    """Main project settings."""
    name: str = "Dilivery app"
    version: str = "0.1.0" 
    database: DatabaseSettings = DatabaseSettings()


config: AppSettings = AppSettings()
