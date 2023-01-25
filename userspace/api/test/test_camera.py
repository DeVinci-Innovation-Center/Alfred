from fastapi.testclient import TestClient
import app as p


client = TestClient(p.app)


def test_show_camera():
    response=client.post("/applications/camera/is-connected")
    assert response.status_code == 200
    assert response.json()=={"message": "Camera connected."}
