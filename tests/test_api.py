from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_chat_completions():
    # Define a sample payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Name 3 colors"}],
        "temperature": 0.7,
    }

    # Make a request to the API and get the response
    response = client.post("/chat/completions", json=payload)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response is a JSON object
    assert response.headers["content-type"] == "application/json"

    # Check that the response body contains the expected keys
    assert "model" in response.json()
    assert "usage" in response.json()
    assert "choices" in response.json()

    # Check that the 'choices' key in the response body is a list
    assert isinstance(response.json()["choices"], list)

    # Check that each choice in the 'choices' list contains the expected keys
    for choice in response.json()["choices"]:
        assert "message" in choice
        assert "role" in choice["message"]
        assert "content" in choice["message"]
