import asyncio
import unittest

from fastapi.testclient import TestClient

from src.api import app, startup_event


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Manually run the startup event
        loop = asyncio.get_event_loop()
        loop.run_until_complete(startup_event())

    def test_chat(self):
        response = self.client.post(
            "/v1/chat/completions",
            json={"model": "gpt-3", "messages": [{"role": "user", "content": "Hello"}]},
        )
        self.assertEqual(response.status_code, 200)

    def test_embed(self):
        response = self.client.post("/v1/embeddings", json={"model": "gpt-3", "input": "Hello"})
        self.assertEqual(response.status_code, 200)
