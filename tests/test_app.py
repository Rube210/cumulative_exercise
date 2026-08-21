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


def test_weather_returns_forecast() -> None:
    """The weather endpoint returns the upstream forecast."""
    forecast = {
        "current": {"temperature_2m": 78.0, "weather_code": 1},
        "daily": {"time": ["2026-08-19"], "temperature_2m_max": [85.0]},
    }
    with patch("web_app.main.requests.get") as get:
        get.return_value.json.return_value = forecast
        response = client.post(
            "/weather", json={"latitude": 33.75, "longitude": -84.39}
        )

    assert response.status_code == 200
    assert response.json() == forecast
    get.return_value.raise_for_status.assert_called_once_with()


def test_weather_rejects_invalid_coordinates() -> None:
    """The weather endpoint validates coordinate ranges."""
    response = client.post("/weather", json={"latitude": 91, "longitude": 0})

    assert response.status_code == 422
