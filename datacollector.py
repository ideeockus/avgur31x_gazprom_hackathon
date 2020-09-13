from kafka import KafkaConsumer
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import os
from geopy import distance


consumer = KafkaConsumer('input2', bootstrap_servers=['gpbtask.fun:9092'])
i = 0

clients_data = {}
poi_coord = ["55.554771", "37.924931"]

for msg in consumer:
    jsonmsg = json.loads(msg.value)

    client_id = jsonmsg.get('client_id', np.nan)
    time = jsonmsg.get('time', np.nan)
    datetime = dt.strptime(time, "%d.%m.%Y %H:%M")  # if not np.isnan(time) else np.nan
    latitude = jsonmsg.get('latitude', np.nan)
    longitude = jsonmsg.get('longitude', np.nan)
    # altitude = jsonmsg.get('altitude (m)', np.nan)
    speed = jsonmsg.get('speed (km/h)', np.nan)
    course = jsonmsg.get('course', np.nan)

    distance_to_poi = distance.distance([latitude, longitude], poi_coord).km

    if not os.path.exists(f"data{client_id}normalized.csv"):
        with open(f"data{client_id}.csv", 'w') as csv_data_file:
            csv_headers = "client_id,datetime,latitude,longitude,speed,course,distance_to_poi\n"
            csv_data_file.write(csv_headers)

    update = ",".join([str(client_id), str(datetime), str(latitude), str(longitude), str(speed), str(course), str(distance_to_poi)]) + "\n"
    with open(f"data{client_id}.csv", 'a') as csv_data_file:
        csv_data_file.write(update)

    i += 1
    if i >= 100:
        break




