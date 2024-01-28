import requests
import csv

GOOGLE_API_KEY = 'AIzaSyAkjgnSLpQeQv28Oui8wAkjU9pnfi9e3Ks'


def get_google_places(query):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'key': GOOGLE_API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    result = response.json()

    if 'results' in result:
        places = result['results']
        return places

    return None


def export_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-16') as csvfile:
            fieldnames = ['Place Name', 'Address', 'Coordinates']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in data:
                writer.writerow(entry)
        print(f"Data exported to {filename}")
    except Exception as e:
        print(f"Error during CSV export: {e}")


if __name__ == "__main__":
    query = "historical places in Macedonia"


    places_data = get_google_places(query)

    if places_data:
        data = []


        for place in places_data:
            name = place.get('name', 'N/A')
            address = place.get('formatted_address', 'N/A')
            coordinates = place['geometry']['location'] if 'geometry' in place else None

            if coordinates:
                data.append({
                    'Place Name': name,
                    'Address': address,
                    'Coordinates': f"{coordinates['lat']}, {coordinates['lng']}"
                })

        # Step 3: Display or save the data
        for entry in data:
            print(entry)

