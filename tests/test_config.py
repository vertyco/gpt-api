import os
import unittest

from decouple import config


class TestConfig(unittest.TestCase):
    def test_config_values(self):
        self.assertEqual(config("HOST", default="127.0.0.1"), "127.0.0.1")
        self.assertEqual(config("WORKERS", default=1, cast=int), 1)
        self.assertEqual(config("SENTRY_DSN", default=None), None)
        self.assertEqual(config("LOGS_PATH", default=""), "")
        self.assertEqual(
            config("MODEL_NAME", default="orca-mini-3b.ggmlv3.q4_0.bin"),
            "orca-mini-3b.ggmlv3.q4_0.bin",
        )
        self.assertEqual(config("MODEL_PATH", default=None), None)
        self.assertEqual(config("THREADS", default=None), None)
        self.assertEqual(config("MAX_TOKENS", default=750, cast=int), 750)
        self.assertEqual(config("EMBED_MODEL", default="all-MiniLM-L12-v2"), "all-MiniLM-L12-v2")
        self.assertEqual(config("LOW_MEMORY", default=False, cast=bool), False)
