# storeapi/app_conf.py

# import os
# print(f"[DEBUG] ENV_STATE from os.environ: {os.getenv('ENV_STATE')}")

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent / "tests"  # e.g. "storeapi"
TEST_DB_PATH = BASE_DIR / "test.db"


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
    DEV_LOGTAIL_API_KEY: Optional[str] = None


class DevConfig(GlobalConfig):
    LOG_LEVEL: Optional[str] = "DEBUG"

    class Config:
        env_prefix = "DEV_"


class ProdConfig(GlobalConfig):
    class Config:
        env_prefix = "PROD_"


class TestConfig(GlobalConfig):
    class Config:
        env_prefix = "TEST_"

print(f"[DEBUG] TestConfig raw: {TestConfig().model_dump()}")

@lru_cache()
def get_config():
    env_state = BaseConfig().ENV_STATE
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}

    print(f"ENV_STATE: {env_state}")

    if env_state not in configs:
        raise ValueError(f"Invalid ENV_STATE: {env_state}")
    return configs[env_state]()
