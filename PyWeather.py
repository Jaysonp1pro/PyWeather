import openmeteo_requests
import requests
from openmeteo_sdk.Variable import Variable

#Built with open-meteo weather and geocoding api, no key required - 10k requests max per day

om = openmeteo_requests.Client()
base_geocoding_url = "https://geocoding-api.open-meteo.com/v1/search?"
weatherParams = {
    "current": ["temperature_2m"],
    "temperature_unit": "fahrenheit",
}

def request_coords():
    search_term = input("Please enter town name: ")

    url = f"{base_geocoding_url}name={search_term}&count=1&language=en&format=json"
    geocode_response = requests.get(url)

    response_status = geocode_response.status_code
    if response_status != 200:
        print(f"Geocode error! HTTP Code {response_status}")

    response_data = geocode_response.json()
    location_results = response_data.get("results")
    if location_results is None:
        return

    location = location_results[0]

    output = dict()
    output["latitude"] = location["latitude"]
    output["longitude"] = location["longitude"]

    return output

def get_Weather():
    coordinates = request_coords()

    if coordinates is None:
        print("Location not found!")
        return
    
    weatherParams["latitude"] = coordinates["latitude"]
    weatherParams["longitude"] = coordinates["longitude"]

    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=weatherParams)
    response = responses[0]

    currentData = response.Current()
    currentVariables = list(map(lambda i: currentData.Variables(i), range(0, currentData.VariablesLength())))
    current_temp = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude () == 2, currentVariables)).Value()

    print(round(current_temp, 1))

get_Weather()