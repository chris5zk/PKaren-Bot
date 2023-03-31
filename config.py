import os

from logging.config import dictConfig
from dotenv import load_dotenv


load_dotenv()

DISCORD_API_SECRET = os.getenv('TOKEN')
BACKEND_CHANNEL = os.getenv('BACKEND')
WELCOME_CHANNEL = os.getenv('WELCOME')
LEAVE_CHANNEL = os.getenv('LEAVE')
ANNOUNCE_CHANNEL = os.getenv('ANNOUNCEMENT')

os.makedirs('./logs', exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)-10s] %(name)s: %(message)s",
            "datefmt": '%Y-%m-%d %H:%M:%S'
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "class": "tools.log.MyTimedRotatingFileHandler",
            "filename": f"logs/logfile.log",
            "formatter": "default",
            "when": "midnight",
            "backupCount": 0,
        }
    },
    "loggers": {
        "discord": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    },
    "disable_existing_loggers": False
}

dictConfig(LOGGING_CONFIG)
