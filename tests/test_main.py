import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test__convert_km_to_miles__success():
    response = client.get("/convert?km=10")
    
    assert response.status_code == 200
    data = response.json()
    assert "kilometers" in data
    assert "miles" in data
    assert data["kilometers"] == 10.0
    assert data["miles"] == 6.2137


def test__convert_km_to_miles_decimal__success():
    response = client.get("/convert?km=5.5")
    
    assert response.status_code == 200
    data = response.json()
    assert data["kilometers"] == 5.5
    assert data["miles"] == pytest.approx(3.4175, abs=0.0001)


def test__convert_km_to_miles_string__error():
    response = client.get("/convert?km=abc")
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("km" in str(error).lower() for error in data["detail"])


def test__convert_km_to_miles_negative_missing_parameter__error():
    response = client.get("/convert")

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
