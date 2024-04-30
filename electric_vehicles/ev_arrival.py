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
ev_probs = [0.3, 0.1, 0.3, 0.25, 0.05]

ev_mdl_choice = np.random.choice([0, 1, 2, 3, 4], p = ev_probs)
start_soc_choice = np.random.choice(np.arange(0.2, 0.45, 0.01))
end_soc_choice = np.random.choice(np.arange(0.55, 0.8, 0.01))

EV1 = ElectricVehicle(models[ev_mdl_choice], batt_caps[ev_mdl_choice], start_soc_choice, end_soc_choice, 12, 16)
print(EV1)

# Datetime list is created to store the ev arrival profile generated
# Also, a dataframe is generated to store all the results
start_date = datetime(year = 2025, month = 1, day = 1, hour = 0, minute = 0)
end_date = datetime(year = 2025, month = 12, day = 31, hour = 23, minute = 59)
time_interval = timedelta(minutes = 1)
datetime_list = []
current_date = start_date

while (current_date <= end_date):
    datetime_list.append(current_date.strftime('%Y-%m-%d %H:%M'))
    current_date += time_interval

ev_arr_results = pd.DataFrame(columns=['datetime'])