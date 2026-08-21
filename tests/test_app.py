"""Tests for the FastAPI application."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from web_app.main import app

client = TestClient(app)


def test_home_page() -> None:
    """The home page is available."""
    response = client.get("/")

    assert response.status_code == 200
    assert "Reuben Jackson Web App" in response.text


def test_coordinates_returns_location() -> None:
    """The complete coordinate endpoint returns geocoder data."""
    location = type("Location", (), {"latitude": 33.75, "longitude": -84.39})()
    with patch("web_app.main.geolocator.geocode", return_value=location):
        response = client.post("/coordinates", json={"city": "Atlanta", "state": "GA"})

    assert response.status_code == 200
    assert response.json() == {
        "city": "Atlanta",
        "state": "GA",
        "latitude": 33.75,
        "longitude": -84.39,
    }
