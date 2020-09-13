from kafka import KafkaConsumer
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import numpy as np
from collections import deque
from sklearn.linear_model import LinearRegression
from geopy.geocoders import Nominatim
from geopy import distance


def abcd(w):
    for client in w:
        # print(w[client])
        if client == "window_len":
            # print(w["window_len"])
            continue
        # print(w[client])
        df = pd.DataFrame(w[client])
        # df['datetime'] = pd.to_datetime(df['datetime'])
        # print(df['datetime'])

        # fig, ax = plt.subplots()
        # df[['datetime', 'speed']].plot(x='datetime', y='speed')
        # plt.title = f"График скорости для клиента {client}"
        # plt.ylabel = "speed"
        # plt.xlabel = "time"
        # plt.show()

        # x = pd.Serial([d.timestamp() for d in df['datetime']])
        df = df.dropna(axis='index', how='any') # убираем строки с пропущенными данными
        x = df[['datetime', 'speed']].copy()   # аргументы модели - время и скорость
        x['datetime'] = [d.timestamp() for d in x['datetime']]
        y = df[['latitude', 'longitude']] # координаты - зависимые переменные

        # x = x.dropna(axis='index', how='any')  # убираем строки с пропущенными данными
        # y = y.dropna(axis='index', how='any')

        model = LinearRegression()
        # print(x, y)
        model.fit(x, y)

        now = datetime.now().timestamp()
        prediction_time = 60
        x_predict = pd.DataFrame({
            'datetime': [now+i for i in range(prediction_time)]
        })
        x_predict['speed'] = x['speed'].mean()

        # print(f"real x: {x}; predict x : {x_predict}")

        # print(model.predict(x)[0][0]) # попытка предсказаний
        y_predict = model.predict(x_predict)
        geolocator = Nominatim(user_agent="avgurgeo")

        y_elem = len(y)-1
        current_coord = [y.iloc[y_elem]['latitude'], y.iloc[y_elem]['longitude']]
        print(current_coord)
        adress = geolocator.reverse(current_coord)
        print(f"Сейчас клиент {client} на {adress}")

        y_elem = len(y_predict) - 1
        # print(y_predict)
        predict_coord = y_predict[y_elem]
        print(predict_coord)
        adress = geolocator.reverse(predict_coord)
        print(f"Скоро клиент {client} будет на {adress}")
        exit(0)
        for u in y_predict:
            pass
            # print(f"latitude: {u[0]}; longitude: {u[1]}")


consumer = KafkaConsumer('input3', bootstrap_servers=['gpbtask.fun:9092'])
window_size = 800
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










