from flask import Flask, render_template
import requests
import csv
from config import GOOGLE_API_KEY  # Importing the API key from the config file

class AppSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.app = Flask(__name__)
        return cls._instance

app_singleton = AppSingleton()

@app_singleton.app.route("/")
def home():
    """Renders the home page."""
    return render_template("Cover page.html")

@app_singleton.app.route("/intro")
def intro():
    """Renders the intro page."""
    return render_template("intro.html")

@app_singleton.app.route("/historical-places")
def historical_places():
    """Renders the historical places page."""
    query = "historical places in Macedonia"
    places_data = get_google_places(query)
    formatted_data = format_place_data(places_data)
    return render_template("historical-places.html", data=formatted_data)

# Removed redundant assignment of GOOGLE_API_KEY here since it's imported from config.py

def get_google_places(query):
    """Fetches places data from Google Places API."""
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'key': GOOGLE_API_KEY
    }

    try:
        # Sending a request to Google Places API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for non-200 status codes
        return response.json().get('results', [])  # Extracting results from response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def format_place_data(places_data):
    """Formats Google Places API data."""
    formatted_data = []
    for place in places_data:
        # Extracting relevant information from the API response
        name = place.get('name', 'N/A')
        address = place.get('formatted_address', 'N/A')
        coordinates = place.get('geometry', {}).get('location', {})
        lat_lng = f"{coordinates.get('lat', 'N/A')}, {coordinates.get('lng', 'N/A')}"

        formatted_data.append({
            'Place Name': name,
            'Address': address,
            'Coordinates': lat_lng
        })
    return formatted_data

if __name__ == "__main__":
    app_singleton.app.run(debug=True)
