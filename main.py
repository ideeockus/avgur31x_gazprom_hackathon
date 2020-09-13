from kafka import KafkaConsumer
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import numpy as np
from collections import deque
from geopy.geocoders import Nominatim
from geopy import distance
from predictor import abcd
from avgurgeo import check_for_poi

consumer = KafkaConsumer('input3', bootstrap_servers=['gpbtask.fun:9092'])
window_size = 400
window_slide = window_size//2
window = {}

for msg in consumer:
    jsonmsg = json.loads(msg.value)

    client_id = jsonmsg.get('client_id', np.nan)
    time = jsonmsg.get('time', np.nan)
    datetime = dt.strptime(time, "%d.%m.%Y %H:%M") # if not np.isnan(time) else np.nan
    latitude = jsonmsg.get('latitude', np.nan)
    longitude = jsonmsg.get('longitude', np.nan)
    # altitude = jsonmsg.get('altitude (m)', np.nan)
    speed = jsonmsg.get('speed (km/h)', np.nan)
    # course = jsonmsg.get('course', np.nan)
    # print(" ".join([str(client_id), str(datetime), str(latitude), str(longitude), str(speed)]))

    if client_id not in window:
        window[client_id] = {'datetime': [], 'latitude': [], 'longitude': [], 'speed': []}
        window['window_len'] = 0

    if window['window_len'] < window_size:
        # window.append([datetime, client_id, latitude, longitude, speed])
        window[client_id]['datetime'].append(datetime)
        window[client_id]['latitude'].append(latitude)
        window[client_id]['longitude'].append(longitude)
        window['window_len'] += 1
        window[client_id]['speed'].append(speed)

    elif window['window_len'] == window_size:

        predict_coords = abcd(window, prediction_time=120)
        poi_trigger = check_for_poi(predict_coords)
        print(poi_trigger)

        for i in range(window_slide):
            # print(f"wsize: {window_size}; wslide: {window_slide}")
            try:
                window[client_id]['datetime'].pop(0)
                window[client_id]['latitude'].pop(0)
                window[client_id]['longitude'].pop(0)
                window['window_len'] -= 1
                window[client_id]['speed'].pop(0)
            except IndexError:
                print(window)
    else:
        print("Something went wrong (Window size bigger than it should be)")










