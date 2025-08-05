import logging
from logging.handlers import RotatingFileHandler
import sys

logger = logging.getLogger("task_automation_api")
logger.setLevel(logging.DEBUG)

fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(fmt)

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
console.setFormatter(formatter)

file = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=5, encoding="utf-8")
file.setLevel(logging.DEBUG)
file.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file)

logger.propagate = False
