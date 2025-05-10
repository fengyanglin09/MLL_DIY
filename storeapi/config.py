# storeapi/config.py

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: Optional[bool] = False
    LOG_LEVEL: Optional[str] = "INFO"
    LOG_FILE: Optional[str] = "app.log"


class DevConfig(GlobalConfig):
    LOG_LEVEL: Optional[str] = "DEBUG"
    class Config:
        env_prefix = "DEV_"



class ProdConfig(GlobalConfig):
    class Config:
        env_prefix = "PROD_"


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///./test.db"
    DB_FORCE_ROLL_BACK: bool = True

    class Config:
        env_prefix = "TEST_"


@lru_cache()
def get_config():
    env_state = BaseConfig().ENV_STATE
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    if env_state not in configs:
        raise ValueError(f"Invalid ENV_STATE: {env_state}")
    return configs[env_state]()
