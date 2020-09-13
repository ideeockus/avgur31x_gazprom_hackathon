from kafka import KafkaConsumer
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import numpy as np
from collections import deque
from sklearn.linear_model import LinearRegression


def abcd(w):
    for client in w:
        if client == "window_len":
            print(w["window_len"])
            continue
        # print(w[client])
        df = pd.DataFrame(w[client])
        # df['datetime'] = pd.to_datetime(df['datetime'])
        # print(df['datetime'])

        # x = pd.Serial([d.timestamp() for d in df['datetime']])
        x = df[['datetime', 'speed']].copy()   # аргументы модели - время и скорость
        x['datetime'] = [d.timestamp() for d in x['datetime']]
        y = df[['latitude', 'longitude']] # координаты - зависимые переменные


        # y = df['datetime'].apply(lambda t: t.timestamp())
        # x = df[['latitude', 'longitude']]



        # y = df[['latitude', 'longitude']]
        # x = df[['datetime']]
        # y = df['latitude']
        print(x)
        print(y)
        model = LinearRegression()
        model.fit(x, y)

        print(model.predict(x)) # попытка предсказаний


consumer = KafkaConsumer('input3', bootstrap_servers=['gpbtask.fun:9092'])
window_size = 4
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

        abcd(window)

        for i in range(window_slide):
            window[client_id]['datetime'].pop(0)
            window[client_id]['latitude'].pop(0)
            window[client_id]['longitude'].pop(0)
            window['window_len'] -= 1
            window[client_id]['speed'].pop(0)
    else:
        print("Something went wrong (Window size bigger than it should be)")










