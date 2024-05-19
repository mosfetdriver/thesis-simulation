#!/usr/bin/env python3

import math
import random
import sys
import argparse
import csv
import logging
from timeit import default_timer
import json
from math import ceil
import matplotlib.pyplot as plt
from statistics import mean

def main():
    data = open("data.txt")
    lines = data.readlines()
    dict_store = {}
    isArrival = False
    oldTime = 1

    for line in lines:
        splitted = line.split()
        if splitted[0] == "arrival":
            isArrival = True
            time = float(splitted[2])
        else:
            isArrival = False
            time = float(splitted[1])
        noEVs = int(splitted[3])

        if time <= 86400:
            continue

        time = ceil(time)
        time = time % 86400
        
        if oldTime > time + 1:
            while oldTime <= 86400:
                if oldTime not in dict_store:
                    dict_store[oldTime] = []
                if isArrival:
                    dict_store[oldTime].append(noEVs - 1)
                else:
                    dict_store[oldTime].append(noEVs + 1)

                oldTime += 1
            
            oldTime = 1

        while oldTime < time:
            if oldTime not in dict_store:
                dict_store[oldTime] = []
            if isArrival:
                dict_store[oldTime].append(noEVs - 1)
            else:
                dict_store[oldTime].append(noEVs + 1)
            
            oldTime += 1
        
        if oldTime not in dict_store:
            dict_store[oldTime] = []
        dict_store[oldTime].append(noEVs)
        
        oldTime += 1
        
    # print (dict_store[3])
    # print (dict_store[4])
    # print (dict_store[5])
    # print (dict_store[6])
    #print (dict_store)
    
    length = len(dict_store.keys())
    value = dict_store[length]
    index = length + 1
    while index <= 86400:
        dict_store[index] = value
        index = index + 1

    #print (dict_store)

    new_dict_store = {}
    for key, value in dict_store.items():
        new_dict_store[key] = value[0]


    # for every 15 minute, now compute the min, max, and average number of connected EVs
    interval = 15*60 # 900
    coarse_min_dict = {}
    coarse_max_dict = {}
    coarse_mean_dict = {}
    slots = int(86400 / interval) # 96
    print (slots)

    for x in range(slots): 
        list_values = []
        for y in range(1, interval + 1):
            #print (x * interval + y)
            list_values.append(new_dict_store[x * interval + y])
        
        for y in range(1, interval + 1):
            coarse_min_dict[x * interval + y] = min(list_values)
            coarse_max_dict[x * interval + y] = max(list_values)
            coarse_mean_dict[x * interval + y] = mean(list_values)

    #print (new_dict_store)
    #print (new_dict_store.values())
    fig = plt.figure()
    plt.plot(list(new_dict_store.values()), label= "realization")
    plt.plot(list(coarse_min_dict.values()), label= "min")
    plt.plot(list(coarse_max_dict.values()), label= "max")
    plt.plot(list(coarse_mean_dict.values()), label= "mean")
    plt.ylabel('# connected EVs')
    plt.xlabel('time (seconds)')
    plt.legend()
    fig.savefig('one_sec_realization_with_min_max_avg_over_15minutes.png', dpi=fig.dpi)

if __name__ == '__main__':
    sys.exit(main())