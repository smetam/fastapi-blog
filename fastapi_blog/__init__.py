import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=str(Path(__file__).parent / ".env"))
CONFIG = Path(__file__).parent / "config" / "config.json"

logging.basicConfig(
    format="%(asctime)s %(levelname)-4s >> %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("KKR Registration")
logger.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))
