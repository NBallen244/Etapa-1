from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_evaluate_success():
    response = client.post("/api/v1/evaluate", json={"expression": "12.5 + 3 * (4 - 1.5) / 2"})
    assert response.status_code == 200
    assert response.json() == {"result": 16.25}

def test_api_evaluate_division_by_zero():
    response = client.post("/api/v1/evaluate", json={"expression": "10 / 0"})
    assert response.status_code == 400
    assert "Division by zero" in response.json()["detail"]

def test_api_evaluate_invalid_characters():
    response = client.post("/api/v1/evaluate", json={"expression": "10 + x"})
    assert response.status_code == 400
    assert "contains invalid characters" in response.json()["detail"]

def test_api_evaluate_syntax_error():
    response = client.post("/api/v1/evaluate", json={"expression": "12 + * 3"})
    assert response.status_code == 400
    assert "Syntax error" in response.json()["detail"]

def test_cors_headers():
    # CORS preflight options request
    response = client.options("/api/v1/evaluate", headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    })
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
