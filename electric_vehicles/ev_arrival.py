### ELECTRIC VEHICLES FOR SIMULATION ###
#
# A class is created to represent the relevant information needed to simulate the behaviour of the electric vehicles in the system
# Models chosen for simulation: 2024 Renault Kwid E-Tech, 2024 Hyundai IONIQ, 2024 BYD Dolphin, 2024 BYD Qin, 
#
###

# Libraries to use
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import weibull_min

# ElectricVehicle class
class ElectricVehicle:
    def __init__(self, model, batt_kwh, start_soc, end_soc, arr_time, dep_time):
        self.model     = model
        self.batt_kwh  = batt_kwh
        self.start_soc = start_soc
        self.end_soc   = end_soc
        self.arr_time  = arr_time
        self.dep_time  = dep_time

    def __str__(self):
        return f"Electric vehicle {self.model} with a battery capacity of {self.batt_kwh} [kWh].\nStart SOC: {100 * self.start_soc:.1f} %. End SOC: {100 * self.end_soc:.1f} %."        

# The vehicle models considered for the simulation and their respectives battery capacities. 
# The probability of each one is also considered   
models = ["Renault Kwid", "Hyundai Ioniq", "BYD Dolphin", "BYD Qin", "Tesla Model 3"]
batt_caps = [26.8, 72.6, 44.9, 53.1, 100.0]
ev_probs = [0.39, 0.1, 0.3, 0.2, 0.01]

# Datetime list is created to store the ev arrival profile generated
# Also, a dataframe is generated to store all the results
start_datetime = datetime(year = 2025, month = 1, day = 1, hour = 0, minute = 0)
end_datetime = datetime(year = 2025, month = 12, day = 31, hour = 23, minute = 59)
time_interval = timedelta(days = 1)
datetime_list = []
current_date = start_datetime

# A pandas dataframe to store the charging events for a day is created
charging_events = pd.DataFrame(columns = ['id', 'date', 't_arr', 't_dep', 'e_dem'])
id_df = []
date_df = []
t_arr_df = []
t_dep_df = []
e_dem_df = []
id_number = 0

# Data are calculated over the selected period of time
while(current_date <= end_datetime):

    # Probability for number of EVs arriving at the CS during the day, for weekday 30 vehicles are considered and for weekends, just 4 
    if(current_date.weekday() < 5):
        n_ev_prob = np.random.normal(30, 2, 1)
        n_ev = round(n_ev_prob[0])
    else:
        n_ev_prob = np.random.normal(4, 2, 1)
        n_ev = round(n_ev_prob[0])

    # Lists for storing daily data are created
    _id = []
    date = [current_date.date()] * n_ev
    t_arr = []
    t_dep = []
    e_dem = []

    # Arrival, departure, model and soc are calculated
    for i in range(n_ev):
        # Probability for arrival and departure of EVs in the station
        ev_arr_group_choice = np.random.choice(["ARR_AM", "ARR_PM"], p = [0.8, 0.2])
        ev_dep_min = 0
        tries = 0

        if ev_arr_group_choice == "ARR_AM":    
            ev_arr_min = np.random.normal(555, 90, 1)
            ev_arr_min = round(ev_arr_min[0])
        else:
            ev_arr_min = np.random.normal(885, 75, 1)
            ev_arr_min = round(ev_arr_min[0])
        
        while((ev_dep_min <= ev_arr_min) and (tries < 3)):
            ev_dep_group_choice = np.random.choice(["DEP_AM", "DEP_PM"], p = [0.3, 0.7])
            if ev_dep_group_choice == "DEP_AM":
                ev_dep_min = weibull_min.rvs(165, loc = 0, scale = 735, size = 1)
                ev_dep_min = round(ev_dep_min[0])
            else:
                ev_dep_min = weibull_min.rvs(195, loc = 0, scale = 1065, size = 1)
                ev_dep_min = round(ev_dep_min[0])
            tries += 1
            print(tries)
        
        ev_mdl_choice = np.random.choice([0, 1, 2, 3, 4], p = ev_probs)
        start_soc_choice = np.random.choice(np.arange(0.2, 0.45, 0.01))
        end_soc_choice = np.random.choice(np.arange(start_soc_choice + 0.3, 0.8, 0.05))

        t_arr.append(ev_arr_min)
        t_dep.append(ev_dep_min)
        e_dem.append((end_soc_choice - start_soc_choice) * batt_caps[ev_mdl_choice])
        _id.append(f"CE{id_number}")
        id_number += 1

    sorted_indexes = sorted(range(len(t_arr)), key = lambda x:t_arr[x])
    t_arr_sorted = sorted(t_arr)
    t_dep_sorted = []
    e_dem_sorted = []

    for i in range(len(t_arr)):
        t_dep_sorted.append(t_dep[sorted_indexes[i]])
        e_dem_sorted.append(e_dem[sorted_indexes[i]])

    for i in range(len(t_arr_sorted)):
        id_df.append(_id[i])
        date_df.append(date[i])
        t_arr_df.append(t_arr_sorted[i])
        t_dep_df.append(t_dep_sorted[i])
        e_dem_df.append(e_dem_sorted[i])

    print(current_date)
    current_date += time_interval

# Data from the lists are stored in the df
charging_events['id'] = id_df
charging_events['date'] = date_df
charging_events['t_arr'] = t_arr_df
charging_events['t_dep'] = t_dep_df
charging_events['e_dem'] = e_dem_df

print(charging_events)
charging_events.to_csv("electric_vehicles/ev_arrivals.csv", index = False)


'''
while (current_date <= end_datetime):
    datetime_list.append(current_date.strftime('%Y-%m-%d %H:%M'))
    current_date += time_interval

    if(current_date.weekday() < 5):
        print("weekday")
    else:
        print("weekend")
'''