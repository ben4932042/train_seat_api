from fastapi.testclient import TestClient

from .router import payment

client = TestClient(app)
