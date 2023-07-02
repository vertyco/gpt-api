import logging
import unittest

from src.logger import init_logging


class TestLogger(unittest.TestCase):
    def test_init_logging(self):
        init_logging()
        logger = logging.getLogger("uvicorn")
        self.assertEqual(len(logger.handlers), 3)
