#!pip install requests
# !pip install plotly

import requests
import plotly.express as px
import pandas as pd
from Haversham import haversine
import json
from tkinter import simpledialog, messagebox

ISS_API = "http://api.open-notify.org/iss-now.json"
AREA_API = "https://geocode.maps.co/reverse?lat=latitude&lon=longitude"


def get_latlong():
    res = requests.get(url=ISS_API)
    results = res.json()
    lat = results['iss_position']['latitude']
    long = results['iss_position']['longitude']
    return lat, long


def get_location(latitude, longitude):
    get_loc = AREA_API.replace('latitude', latitude)
    get_loc = get_loc.replace('longitude', longitude)
    loc_res = requests.get(url=get_loc)
    location = loc_res.json()
    if 'error' in location.keys():
        text = 'Somewhere over the ocean'
    else:
        text = location['address']['state'] + ' ' + location['address']['country']
    return text


def plot_location():
    lat, long = get_latlong()
    loc = get_location(lat, long)
    df = pd.DataFrame(
        {
            'Station': ['ISS'],
            'lat': [lat],
            'long': [long],
            'text': [loc]
        }
    )

    fig = px.scatter_geo(df, lat='lat', lon='long')
    fig.update_traces(textposition='bottom left',
                      marker=dict(size=12, symbol='star-dot',
                                  line=dict(width=3, color='indianred')),
                      selector=dict(mode='markers'))
    title = f'Location:\t' + loc
    fig.update_layout(title=title, title_x=0.5)
    fig.show()


def current_location():
    try:
        with open('current_location.json') as json_file:
            loc_dict = json.load(json_file)
    except FileNotFoundError:
        text = "Your current location is not available\n"
        text += 'Please enter your latlong by following the instructions at https://www.latlong.net '
        get_lat = simpledialog.askfloat(title='Latitude:', prompt='Enter your latitude')
        get_long = simpledialog.askfloat(title='Longitude:', prompt='Enter your longitude')
        loc_dict = {'latitude': get_lat, 'longitude': get_long}
        with open('current_location.json', 'w') as json_file:
            json.dump(loc_dict, json_file)
    return loc_dict


def calc_dist(current_location, lat2, long2):
    lat1 = current_location['latitude']
    long1 = current_location['longitude']
    dist = haversine(lat1, long1, float(lat2), float(long2))
    return dist


def display_dist():
    loc_dist = current_location()
    lat, long = get_latlong()
    dist = calc_dist(loc_dist, lat, long)
    text = f'The ISS is {dist:.3f} kms away from you and 402 kms above you'
    messagebox.showinfo('Distance from ISS', text)
