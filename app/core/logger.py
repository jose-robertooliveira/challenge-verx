import sys
from pathlib import Path

from loguru import logger

Path("logs").mkdir(exist_ok=True)

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>",
)

logger.add("logs/api.log", rotation="1 week", retention="1 month", level="INFO")
