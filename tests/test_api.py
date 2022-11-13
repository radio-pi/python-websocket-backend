from radiopi import main
from fastapi.testclient import TestClient


client = TestClient(main.app)


def test_read_index():
    response = client.get("/")
    assert response.status_code == 200


def test_volume_endpoint():
    data = {"volume": "99"}

    response = client.post("/volume", json=data)
    assert response.status_code == 200
    assert response.json() == {}

    response = client.get("/volume")
    assert response.status_code == 200
    assert response.json() == data


def test_play_endpoint():
    data = {"url": "https://some.url"}

    response = client.post("/play", json=data)
    assert response.status_code == 200
    assert response.json() == {}


def test_stop_endpoint():
    response = client.post("/stop")
    assert response.status_code == 200
    assert response.json() == {}


def test_timer_endpoint():
    data = {"time": "2"}

    response = client.post("/sleeptimer", json=data)
    assert response.status_code == 200
    assert response.json() == {}

    response = client.get("/sleeptimer")
    assert response.status_code == 200
    assert response.json() == {"sleeptimer": "1"}

    response = client.post("/sleeptimer/cancle")
    assert response.status_code == 200
    assert response.json() == {}
