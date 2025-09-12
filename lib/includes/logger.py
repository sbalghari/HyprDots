from .paths import LOG_FILE

import logging
from logging import Logger

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    filemode="a"
)

logger: Logger = logging.getLogger()


def log_heading(title: str):
    separator = "=" * 50
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{separator}\n")
        f.write(f"{title}\n")
        f.write(f"{separator}\n")
