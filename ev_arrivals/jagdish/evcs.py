#!/usr/bin/env python3

import math
import random
import sys
import argparse
import csv
import logging
from timeit import default_timer
from random import uniform
from operator import itemgetter

PMAX_EV = 30 # kW
MEAN_ENERGY_DEMAND = 100 # kWh
INTERVAL_ENERGY_DEMAND = 20 # kWh
MEAN_STAY_TIME = 2 # hours
INTERVAL_STAY_TIME = 0.5 # hours
SIM_START_TIME = 0  # simulation start time: no of minutes after midnight the simulation starts. This time matters because the arrival rate depends on the time of the day.
NO_CHARGING_SLOTS = 800  # number of EVs that can be charged simultaeneously


# the average rate of arrival of cars per second
# in a non-homogeneous Poisson process
# in a given interval, the rate of arrival is assumed to be
# constant and independent of each other
def rate(t):
    t = t % 86400
    
    if t >= 0 and t < 28800:
        hourly_rate = 20
    elif t >= 28800 and t < 43200:
        hourly_rate = 90
    elif t >= 43200 and t < 64800:
        hourly_rate = 30
    elif t >= 64800 and t < 72000:
        hourly_rate = 150
    else:
        hourly_rate = 25

    return hourly_rate / 3600


def main():
    occupied_slots = {}
    max_rate = 150 / 3600
    current_time = SIM_START_TIME

    while True:
        arrival_time = -math.log(1.0 - random.random()) / max_rate
        current_time += arrival_time

        store_list = []
        for slot in list(occupied_slots):
            if occupied_slots[slot]["time_to_leave"] <= current_time and occupied_slots[slot]["time_to_leave"] <= 172800: 
                store_list.append((occupied_slots[slot]["time_to_leave"], slot, len(occupied_slots) - 1))
                del occupied_slots[slot]

        store_list = sorted(store_list, key=itemgetter(0))
       
        for elem in store_list:
            print ("departure {} {} {}".format(elem[0], elem[1], elem[2]))
                
        if current_time > 172800:
            break

        if (random.random() <= rate(current_time) / max_rate and len(occupied_slots) < NO_CHARGING_SLOTS): 
            slot_to_use = 0

            for slot in range(1, NO_CHARGING_SLOTS + 1):
                if slot not in occupied_slots:
                    slot_to_use = slot
                    break

            time_to_leave = current_time + (MEAN_STAY_TIME + uniform(-INTERVAL_STAY_TIME, INTERVAL_STAY_TIME)) * 3600 # in seconds
            energy_demand = (MEAN_ENERGY_DEMAND + uniform(-INTERVAL_ENERGY_DEMAND, INTERVAL_ENERGY_DEMAND))
            occupied_slots[slot_to_use] = {"time_to_leave": time_to_leave, "energy_demand": energy_demand}

            print ("arrival {} {} {} {} {}".format(slot_to_use, current_time, len(occupied_slots), time_to_leave, energy_demand))          


if __name__ == '__main__':
    sys.exit(main())