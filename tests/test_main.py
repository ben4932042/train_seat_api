from fastapi.testclient import TestClient

try:
    from .main import app
except:
    import os
    import sys
    path = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(path)
    from main import app

client = TestClient(app)


def test_get_all_order():
    response = client.get('/ping', headers={'accept': 'application/json'})
    assert response.status_code == 200
