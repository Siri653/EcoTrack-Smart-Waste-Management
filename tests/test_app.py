import pytest
import app as app_module

@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(app_module, "DATABASE", str(db_path))
    app_module.init_db()
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as test_client:
        yield test_client

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Smart Waste Management" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_create_report(client):
    response = client.post("/report", data={
        "reporter": "Test User", "location": "Main Road",
        "waste_type": "Plastic", "description": "Waste near the bus stop"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Main Road" in response.data

def test_update_status(client):
    client.post("/report", data={
        "reporter": "Test User", "location": "Park Gate",
        "waste_type": "Household", "description": "Waste pile"
    })
    response = client.post("/report/1/status", data={"status": "Completed"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Completed" in response.data
