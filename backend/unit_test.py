import os
import tempfile
import pytest
import json

from backend import app as backend_app

@pytest.fixture
def client():
    return backend_app.test_client()

def test_ping(client):
    data = {
        "command": "ping",
        "arguments": []
    }
    response = client.post("/command/ping", data=json.dumps(data))
    assert response.status_code == 200
    assert response.json["response"] == "Pong!"

