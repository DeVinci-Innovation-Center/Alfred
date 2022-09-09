from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_show_camera():
    response=client.post("/applications/camera/is-connected")
    assert response.status_code == 200
    assert response.json()=={"message": "Camera connected."}
