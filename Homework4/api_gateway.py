from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

USER_SERVICE_URL = "http://localhost:5001/users"
HISTORICAL_PLACES_SERVICE_URL = "http://localhost:5002/historical-places"

@app.route("/")
def home():
    # Forward request to the web_interface_service
    return requests.get("http://localhost:5000/").content

@app.route("/intro")
def intro():
    # Forward request to the web_interface_service
    return requests.get("http://localhost:5000/intro").content

@app.route("/historical-places")
def historical_places():
    # Forward request to the historical_places_service
    return requests.get(HISTORICAL_PLACES_SERVICE_URL).content

if __name__ == "__main__":
    app.run(port=5003, debug=True)
