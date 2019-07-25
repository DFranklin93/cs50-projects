import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def getLocation(location):
    """ Get Geo Location from user input """
    #Contact Google Geocoding API
    try:
        # print(location)
        api_key = 'API KEY NEEDED'
        response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(location)}&key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        location_response = response.json()
        return {
            'formatted_address': location_response['results'][0]['formatted_address'],
            'address_components': location_response['results'][0]['address_components'],
            'lat': location_response['results'][0]['geometry']['location']['lat'],
            'lon': location_response['results'][0]['geometry']['location']['lng'],
            # 'addressLength': len(location_response['results'][0]['address_components'])
        }
    except (KeyError, TypeError, ValueError):
        return None

def getCurrentWeather(lat, lon):
    """Look up weather using lat and lng"""

    #Contact API
    try:
        api_key = 'API KEY NEEDED'
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid=e2726fffd273704862fcc263496db4b3")
        response.raise_for_status()
    except request.RequestExecption:
        return None

    # Parse response
    try:
        weather_response = response.json()
        return {
            'description': weather_response['weather'],
            'weather_details': weather_response['main'],
            'visibility': weather_response['visibility'],
            'wind': weather_response['wind'],
            'sun': {'sunrise': weather_response['sys']['sunrise'], 'sunset': weather_response['sys']['sunset']}
        }
    except (KeyError, TypeError, ValueError):
        return None

def darkSkies(lat, lon):
    """Gets hourly weather"""

    # Contact API
    try:
        api_key = 'API KEY NEEDED'
        response = requests.get(f"https://api.darksky.net/forecast/{api_key}/{lat},{lon}")
        response.raise_for_status()
    except request.ResquestExecption:
        return None

    # Parse response
    try:
        dark_skies_response = response.json()
        return {
            'currently': dark_skies_response['currently'],
            'hourly': dark_skies_response['hourly'],
            'daily': dark_skies_response['daily']
        }
    except (KeyError, TypeError, ValueError):
        return None