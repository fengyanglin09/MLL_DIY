from pydantic import BaseSettings
from functools import lru_cache
from typing import Optional

class BaseConfig(BaseSettings):
    """
    Base configuration class for the application.
    """
    ENV_STATE: Optional[str] = None
    class Config:
        env_file: str = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class GlobalConfig(BaseConfig):
    """
    Global configuration class for the application.
    """
    # Global settings can be added here
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: Optional[bool] = False


class DevConfig(GlobalConfig):
    """
    Development configuration class for the application.
    """
    # Development-specific settings can be added here
    class Config:
        env_prefix = "DEV_"


class ProdConfig(GlobalConfig):
    """
    Production configuration class for the application.
    """
    # Production-specific settings can be added here
    class Config:
        env_prefix = "PROD_"


class TestConfig(GlobalConfig):
    """
    Test configuration class for the application.
    """
    # Test-specific settings can be added here
    DATABASE_URL: str = "sqlite:///./test.db"
    DB_FORCE_ROLL_BACK: bool = True
    class Config:
        env_prefix = "TEST_"


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)