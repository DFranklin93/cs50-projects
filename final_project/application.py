import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime

from helpers import getLocation, getCurrentWeather, darkSkies

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    """Shows 3 major cities and a weather radar"""
    location = request.form.get('location')

    if request.method == 'POST':
        location_info = getLocation(location)
        return redirect(url_for('location', location_name = location_info['formatted_address']))
    if request.method == 'GET':
        index_locations = []
        ca_location = getLocation("Los Angeles,California")
        tx_location = getLocation("Dallas, Texas")
        ny_location = getLocation("New York City, New York")
        locations = [ca_location, tx_location, ny_location]
        for i in locations:
            current_weather = getCurrentWeather(i['lat'], i['lon'])
            dark_skies_weather = darkSkies(i['lat'], i['lon'])
            index_locations.append({'place': i, 'current_weather': current_weather, 'dark_skies': dark_skies_weather})
    return render_template("index.html", locations = index_locations)

@app.route("/location/<location_name>", methods=["GET"])
def location(location_name):
    location_info = []
    input_location = getLocation(location_name)
    current_weather = getCurrentWeather(input_location['lat'], input_location['lon'])
    dark_skies_weather = darkSkies(input_location['lat'], input_location['lon'])
    location_info.append({'place': input_location, 'current_weather': current_weather, 'dark_skies': dark_skies_weather})

    # Converts hourly UNIX time to 24 hrs
    for i in range(len(location_info[0]['dark_skies']['hourly']['data'])):
        ts = location_info[0]['dark_skies']['hourly']['data'][i]['time']
        location_info[0]['dark_skies']['hourly']['data'][i]['time'] = datetime.utcfromtimestamp(ts).strftime('%H:%M')
        location_info[0]['dark_skies']['hourly']['data'][i]['date'] = datetime.utcfromtimestamp(ts).strftime('%m-%d-%Y')

    # Converts daily UNIX time to 24 hrs
    for j in range(len(location_info[0]['dark_skies']['daily']['data'])):
        tt = location_info[0]['dark_skies']['daily']['data'][j]['time']
        location_info[0]['dark_skies']['daily']['data'][j]['time'] = datetime.utcfromtimestamp(tt).strftime('%H:%M')
        location_info[0]['dark_skies']['daily']['data'][j]['date'] = datetime.utcfromtimestamp(tt).strftime('%m-%d-%Y')

    return render_template("location.html", location = location_info)