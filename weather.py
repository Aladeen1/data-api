# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests
from datetime import datetime

BASE_URI = "https://weather.lewagon.com"


def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    url = f"{BASE_URI}/geo/1.0/direct?q={query}"
    response = requests.get(url).json()
    return response[0]

def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    weather_forecast_list = []
    url = f"{BASE_URI}/data/2.5/forecast?lat={lat}&lon={lon}&units=metric"
    response = requests.get(url).json()
    five_days_forecast_list = [response.get('list', "no list key in forecast response")[i] for i in [4,12,20,28,36]] # get the weather at 12:00pm
    for forecast in five_days_forecast_list:
        weather_forecast_list.append(create_forecast_dict(forecast))
    return weather_forecast_list

def create_forecast_dict(raw_dict):
    '''Return the dictionary in right format from a timestamp dictionnary'''
    day = datetime.fromtimestamp(raw_dict['dt']).strftime('%Y-%m-%d')
    return {'day' : day, 'weather' : f"{raw_dict['weather'][0]['description'].title()} {raw_dict['main']['temp']}°C"}

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)
    forecast_list = weather_forecast(city["lat"], city["lon"])
    for forecast in forecast_list:
        print(f"{forecast['day']}: {forecast['weather']}")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
