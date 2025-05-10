from logging.config import dictConfig
import os

from storeapi.config import get_config

def configure_logging() -> None:
    # config = get_config()
    # print(config.dict())

    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {"format": "%(name)s:%(lineno)d - %(message)s"},
                "file": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s - %(levelname)-8s - %(name)s:%(lineno)d - %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "rich.logging.RichHandler",
                    "formatter": "default",
                    "level": get_config().LOG_LEVEL,
                },
                "file_handler": {
                    "class": "logging.FileHandler",
                    "filename": get_config().LOG_FILE,
                    "formatter": "file",
                    "level": get_config().LOG_LEVEL,
                },
                "rotating_file_handler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "logs/" + get_config().LOG_FILE,
                    "maxBytes": 1024 * 1024 * 5,  # 5 MB
                    "backupCount": 5,
                    "formatter": "file",
                    "encoding": "utf-8",
                    "level": get_config().LOG_LEVEL,
                }
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["console", "rotating_file_handler"],
                    "level": "INFO",
                    "propagate": False,
                },
                "storeapi": {
                    "handlers": ["console", "rotating_file_handler"],
                    "level": get_config().LOG_LEVEL,
                    "propagate": False,
                },
                "databases": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "aiosqlite": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                }
            },
        }
    )