from kafka import KafkaConsumer
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from collections import deque
from sklearn.linear_model import LinearRegression
from geopy.geocoders import Nominatim
from geopy import distance


def abcd(w, prediction_time=120):
    for client in w:
        if client == "window_len":
            continue
        df = pd.DataFrame(w[client])

        df = df.dropna(axis='index', how='any')  # убираем строки с пропущенными данными
        x = df[['datetime', 'speed']].copy()   # аргументы модели - время и скорость
        x['datetime'] = [d.timestamp() for d in x['datetime']]
        y = df[['latitude', 'longitude']]  # координаты

        model = LinearRegression()
        # print(x, y)
        model.fit(x, y)

        now = datetime.now().timestamp()

        x_predict = pd.DataFrame({
            'datetime': [now+i for i in range(prediction_time)]
        })
        x_predict['speed'] = x['speed'].mean()

        y_predict = model.predict(x_predict)
        geolocator = Nominatim(user_agent="avgurgeo")

        y_elem = len(y)-1
        current_coord = [y.iloc[y_elem]['latitude'], y.iloc[y_elem]['longitude']]
        print(current_coord)
        adress = geolocator.reverse(current_coord)
        print(f"Сейчас client{client} на {adress}")

        y_elem = len(y_predict) - 1
        # print(y_predict)
        predict_coord = y_predict[y_elem]
        print(predict_coord)
        adress = geolocator.reverse(predict_coord)
        print(f"Через {prediction_time//2}  client{client} будет на {adress}")
        for u in y_predict:
            pass
            # print(f"latitude: {u[0]}; longitude: {u[1]}")
        # print(f"current: {y};predict: {y_predict}")
