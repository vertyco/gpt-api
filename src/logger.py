import logging
from logging.handlers import RotatingFileHandler

import colorama
from colorama import Back, Fore, Style


class PrettyFormatter(logging.Formatter):
    colorama.init(autoreset=True)
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    formats = {
        logging.DEBUG: Fore.LIGHTGREEN_EX + Style.BRIGHT + fmt,
        logging.INFO: Fore.LIGHTWHITE_EX + Style.BRIGHT + fmt,
        logging.WARNING: Fore.YELLOW + Style.BRIGHT + fmt,
        logging.ERROR: Fore.LIGHTMAGENTA_EX + Style.BRIGHT + fmt,
        logging.CRITICAL: Fore.LIGHTYELLOW_EX + Back.RED + Style.BRIGHT + fmt,
    }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt="%m/%d %I:%M:%S %p")
        return formatter.format(record)


def init_logging():
    datefmt = "%m-%d-%Y %I:%M:%S %p"
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt=datefmt)

    # Console Log
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(PrettyFormatter())
    stdout_handler.setLevel(logging.DEBUG)

    info_file_handler = RotatingFileHandler(
        "logs.log", mode="a", maxBytes=1024 * 1024, backupCount=2
    )
    info_file_handler.setFormatter(log_format)
    info_file_handler.setLevel(logging.INFO)

    # Debug log
    debug_file_handler = RotatingFileHandler(
        "debug-logs.log", mode="a", maxBytes=1024 * 1024, backupCount=2
    )
    debug_file_handler.setFormatter(log_format)
    debug_file_handler.setLevel(logging.DEBUG)

    for handler in [stdout_handler, info_file_handler, debug_file_handler]:
        logging.getLogger("uvicorn").addHandler(handler)
