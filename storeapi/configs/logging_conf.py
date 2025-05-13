import logging
import os
from logging.config import dictConfig

from storeapi.app_conf import DevConfig, get_config

logging_handler = ["console_handler", "rotating_file_handler"]

if isinstance(get_config(), DevConfig):
    logging_handler = ["console_handler", "rotating_file_handler"]


def obfuscated(email: str, length: int = 3) -> str:
    """
    Obfuscate the email address by replacing the first part with asterisks.
    """
    if "@" in email:
        local_part, domain = email.split("@", 1)
        obfuscated_local_part = "*" * length + local_part[length:]
        return f"{obfuscated_local_part}@{domain}"
    return email


class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", length: int = 3):
        super().__init__(name)
        self.length = length

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, "email"):
            record.email = obfuscated(record.email, self.length)
        return True


def configure_logging() -> None:
    current_dir = os.path.dirname(__file__)

    # Ensure the logs directory exists relative to the current file
    logs_dir = os.path.join(current_dir, "../logs")
    os.makedirs(logs_dir, exist_ok=True)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 32,
                },
                "email_obfuscation": {"()": EmailObfuscationFilter, "length": 3},
            },
            "formatters": {
                "default": {
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s"
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                "console_handler": {
                    "class": "rich.logging.RichHandler",
                    "formatter": "default",
                    "level": get_config().LOG_LEVEL,
                    "filters": ["correlation_id", "email_obfuscation"],
                },
                # "file_handler": {
                #     "class": "logging.FileHandler",
                #     "filename": get_config().LOG_FILE,
                #     "formatter": "file",
                #     "level": get_config().LOG_LEVEL,
                #     "filters": ["correlation_id", "email_obfuscation"],
                # },
                "rotating_file_handler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(logs_dir, get_config().LOG_FILE),
                    "maxBytes": 1024 * 1024 * 5,  # 5 MB
                    "backupCount": 5,
                    "formatter": "file",
                    "encoding": "utf-8",
                    "level": get_config().LOG_LEVEL,
                    "filters": ["correlation_id", "email_obfuscation"],
                },
            },
            "loggers": {
                "uvicorn": {
                    "handlers": logging_handler,
                    "level": "INFO",
                    "propagate": False,
                },
                "storeapi": {
                    "handlers": logging_handler,
                    "level": get_config().LOG_LEVEL,
                    "propagate": False,
                },
                "databases": {
                    "handlers": logging_handler,
                    "level": "WARNING",
                    "propagate": False,
                },
                "aiosqlite": {
                    "handlers": logging_handler,
                    "level": "WARNING",
                    "propagate": False,
                },
            },
        }
    )
