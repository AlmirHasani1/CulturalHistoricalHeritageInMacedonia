import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Replace 'YOUR_GOOGLE_API_KEY' with your actual Google Maps API key
GOOGLE_API_KEY = 'AIzaSyAkjgnSLpQeQv28Oui8wAkjU9pnfi9e3Ks'

# Descriptions for heritage sites
descriptions = [
    "Skopje has been inhabited since at least 4200 BC, making it one of the oldest cities in Europe...",
    "The sacred architecture of Ohrid is prominent within the urban landscape. It includes early basilicas...",
    "Heraclea Lyncestis was an ancient Greek city in Macedon, ruled later by the Romans...",
    "Bargala is an archaeological site in Karbinci Municipality, North Macedonia, 10 km east of the city of Štip...",
    "Markovi Kuli or Marko's Towers are situated in the northwest of Prilep, North Macedonia...",
    "Stobi was an ancient town of Paeonia, later conquered by Macedon, and finally turned into the capital of the Roman province of Macedonia Salutaris...",
    "Kokino is a Bronze Age archaeological site in the Republic of North Macedonia..."
]


def scrape_heritage_sites_list(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract relevant information based on the HTML structure of the website
        # Modify the following line based on the actual structure of the website
        heritage_sites = [element.get_text().strip().replace('\n', ' ') for element in soup.find_all('h2')]

        return heritage_sites

    else:
        print(f"Error: Unexpected status code {response.status_code}")
        return None


def get_google_info(place_name, country="North Macedonia"):
    # Use the Google Maps Geocoding API to geocode place name to get coordinates
    formatted_place_name = f"{place_name}, {country}"
    google_api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={formatted_place_name}&key={GOOGLE_API_KEY}"

    response = requests.get(google_api_url)

    if response.status_code == 200:
        result = response.json()

        if 'results' in result and result['results']:
            location = result['results'][0]['geometry']['location']
            coordinates = f"{location['lat']}, {location['lng']}"
            return {'coordinates': coordinates}

    return None


def filter_add_descriptions(data, descriptions):
    # Add descriptions to the data
    for site_data, description in zip(data, descriptions):
        site_data['Description'] = description

    return data


def filter_scrape_tripadvisor_data(data):
    base_url_tripadvisor = "https://www.tripadvisor.com/Attractions-g295109-Activities-c47-t17-Republic_of_North_Macedonia.html"

    try:
        response = requests.get(base_url_tripadvisor)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return data

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract relevant information based on the HTML structure of the TripAdvisor website
        # Modify the following line based on the actual structure of the website
        tripadvisor_info = [element.get_text().strip().replace('\n', ' ') for element in
                            soup.find_all('h2', class_='something')]

        # Add TripAdvisor info to the data
        for site_data, tripadvisor_data in zip(data, tripadvisor_info):
            site_data['TripAdvisor Info'] = tripadvisor_data

    return data


class Pipe:
    def __init__(self):
        self.filters = list()

    def add(self, filter, *args, **kwargs):
        self.filters.append((filter, args, kwargs))

    def execute(self, data):
        print("Executing pipeline...")
        for data_filter, args, kwargs in self.filters:
            print('Filtering with', data_filter)
            data = data_filter(data, *args, **kwargs)
        print("Done.")
        return data


if __name__ == "__main__":
    base_url = "https://www.thetravel.com/historical-and-cultural-spots-in-north-macedonia/"

    # Step 1: Scrape Heritage Sites List
    heritage_sites_list = scrape_heritage_sites_list(base_url)

    if heritage_sites_list:
        data = []

        # Step 2: Get Coordinates using Google Maps Geocoding API
        for site_name in heritage_sites_list:
            site_info = get_google_info(site_name, country="North Macedonia")

            if site_info:
                data.append({
                    'Name place': site_name,
                    'Coordinates': site_info.get('coordinates'),
                })

        # Step 3: Pipe and Filter
        my_pipe = Pipe()
        my_pipe.add(filter_add_descriptions, descriptions)
        my_pipe.add(filter_scrape_tripadvisor_data)
        data = my_pipe.execute(data)

        # Step 4: Create a Row Table using Pandas
        df = pd.DataFrame(data)

        # Step 5: Export to CSV
        df.to_csv('heritage_sites_data.csv', index=False, quoting=csv.QUOTE_ALL)

        # Print the resulting table
        print(df)
