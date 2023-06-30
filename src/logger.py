import logging
from logging.handlers import RotatingFileHandler

import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

try:
    import src.config as config
except ModuleNotFoundError:
    import config


def init_logging():
    datefmt = "%m-%d-%Y %I:%M:%S %p"
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt=datefmt)

    # Console Log
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(log_format)
    stdout_handler.setLevel(logging.DEBUG)

    info_file_handler = RotatingFileHandler(
        f"{config.LOGS_PATH}logs.log", mode="a", maxBytes=1024 * 1024, backupCount=2
    )
    info_file_handler.setFormatter(log_format)
    info_file_handler.setLevel(logging.INFO)

    # Debug log
    debug_file_handler = RotatingFileHandler(
        f"{config.LOGS_PATH}debug-logs.log", mode="a", maxBytes=1024 * 1024, backupCount=2
    )
    debug_file_handler.setFormatter(log_format)
    debug_file_handler.setLevel(logging.DEBUG)

    for handler in [stdout_handler, info_file_handler, debug_file_handler]:
        logging.getLogger("uvicorn").addHandler(handler)

    logging.basicConfig(
        level=logging.DEBUG,
        datefmt=datefmt,
        handlers=[stdout_handler, info_file_handler, debug_file_handler],
    )


def init_sentry(dsn: str = None) -> None:
    if dsn:
        sentry_sdk.init(dsn=dsn, integrations=[AioHttpIntegration()])
