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


zstances = [["55.554771", "37.924931"], ["60.765833", "28.808552"], ["55.798510", "37.534730"],
     ["55.862126", "37.466772"], ["55.848817", "36.805567"], ["53.041525", "158.637171"]]

buildings = [["55.558834", "37.815781"], ["55.900693", "37.478917"]]

banks = [["55.728849", "37.620321"], ["56.342179", "37.523720"], ["56.007639", "37.484526"], ["55.782977, 37.640659"],
         ["53.019530", "158.647842"], ["55.630446", "37.658377"], ["55.633323", "37.650055"], ["55.909247", "37.590461"]]


def check_for_poi(coords):
    for zstance in zstances:
        distance_to_poi = distance.distance(coords, zstance).km
        if distance_to_poi < 0.5:
            return {'triggered': True, 'object': "заправка", 'client_coords': coords, 'poi_coords': zstance, 'distance': distance_to_poi}

    for building in buildings:
        distance_to_poi = distance.distance(coords, building).km
        if distance_to_poi < 0.5:
            return {'triggered': True, 'object': "стройка", 'client_coords': coords, 'poi_coords': building, 'distance': distance_to_poi}

    for bank in banks:
        distance_to_poi = distance.distance(coords, bank).km
        if distance_to_poi < 0.5:
            return {'triggered': True, 'object': "стройка", 'client_coords': coords, 'poi_coords': bank, 'distance': distance_to_poi}

    return {'triggered': False}
