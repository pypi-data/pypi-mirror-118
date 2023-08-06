import logging
import os.path
from logging.config import dictConfig

logger = logging.getLogger("queen")


def config(log_directory):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "verbose": {"format": "%(levelname)s %(asctime)s %(message)s"},
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "verbose",
                    "filename": os.path.join(log_directory, "queen.log"),
                    "level": "INFO",
                },
                "file_verbose": {
                    "class": "logging.FileHandler",
                    "formatter": "verbose",
                    "filename": os.path.join(log_directory, "queen_verbose.log"),
                    "level": "DEBUG",
                },
            },
            "loggers": {
                "queen": {
                    "handlers": ["file", "file_verbose"],
                    "level": "DEBUG",
                },
            },
        }
    )
