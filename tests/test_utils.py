import unittest

from src.utils import compile_messages


class TestUtils(unittest.TestCase):
    def test_compile_messages(self):
        messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
        result = compile_messages(messages)
        self.assertIn("Hello", result)
        self.assertIn("Hi", result)
