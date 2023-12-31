# Homework 1- Macedonian Historical Heritage Sites Scraper

## API Reference
Replace 'YOUR_GOOGLE_API_KEY' in the code with your actual Google Maps API key.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `GOOGLE_API_KEY` | `string` | **Required**. Your API key |




## Description
This project is a web scraper that extracts information about historical and cultural spots in North Macedonia from a travel website. It utilizes web scraping techniques to gather data about heritage sites, fetches coordinates using the Google Maps Geocoding API, and includes additional information from TripAdvisor.
This project utilizes a pipe and filter architecture to enhance modularity and maintainability. 
## Installation

Ensure you have Python installed

Install the required libraries: requests, beautifulsoup4, pandas.

```bash
pip install requests
pip install beautifulsoup4
pip install pandas
```

    

## Contributors
[AlmirHasani]



## API Reference
Replace 'YOUR_GOOGLE_API_KEY' in the code with your actual Google Maps API key.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `GOOGLE_API_KEY` | `string` | **Required**. Your API key |




## Description
This project is a web scraper that extracts information about historical and cultural spots in North Macedonia from a travel website. It utilizes web scraping techniques to gather data about heritage sites, fetches coordinates using the Google Maps Geocoding API, and includes additional information from TripAdvisor.
## Installation

Ensure you have Python installed

Install the required libraries: requests, beautifulsoup4, pandas.

```bash
pip install requests
pip install beautifulsoup4
pip install pandas
```
    

## Contributors
[AlmirHasani]


## Exporting to .csv file
If you want your data exported into a .csv files add the following code at the end. 
```python
 df.to_csv('heritage_sites_data.csv', index=False, quoting=csv.QUOTE_ALL)
```

