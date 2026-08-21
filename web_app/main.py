"""FastAPI application for looking up city coordinates."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from geopy.geocoders import Nominatim  # type: ignore[import-untyped]
from pydantic import BaseModel

app = FastAPI(title="Reuben Jackson Web App")
geolocator = Nominatim(user_agent="reuben_jackson_web_app")


class LocationInput(BaseModel):
    """A city and state used for a geocoding lookup."""

    city: str
    state: str


@app.get("/", response_class=HTMLResponse)
async def read_root() -> str:
    """Return the application home page."""
    return """
    <html>
        <head>
            <title>Cumulative Exercise</title>
        </head>
        <body>
            <h1>Reuben Jackson Web App</h1>
            <p>Use the API documentation to test the coordinate endpoints.</p>
            <a href="/docs">Go to Interactive Test Page</a>
        </body>
    </html>
    """


def _geocode(data: LocationInput):
    """Find the location represented by a city and state."""
    return geolocator.geocode(f"{data.city}, {data.state}")


@app.post("/coordinates")
async def get_coordinates(data: LocationInput) -> dict:
    """Return the complete coordinate record for a location."""
    location = _geocode(data)
    if location is None:
        return {"error": "Location could not be found."}

    return {
        "city": data.city,
        "state": data.state,
        "latitude": location.latitude,
        "longitude": location.longitude,
    }


@app.post("/lat-long-lookup")
async def get_lat_long_lookup(data: LocationInput) -> dict:
    """Return only latitude and longitude for a location."""
    location = _geocode(data)
    if location is None:
        return {"error": "Coordinates not found for this city/state."}

    return {"lat": location.latitude, "long": location.longitude}
