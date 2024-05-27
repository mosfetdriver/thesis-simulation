### SCENARIO: GRID - CS - EXTERNAL LOAD ###
#
#
#
###

# Libraries and other code
import charging_station as cs
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# FCI Charging Station object creation
name = "FCI Charging Station"
p_nom = 80
n_cs = 12
max_ch_pwr = n_cs * [7.4]
min_ch_pwr = n_cs * [0.0]
n_load = 1
n_res = 0

FCI_ChSt = cs.ChargingStation(name, p_nom, n_cs, max_ch_pwr, min_ch_pwr, n_load, n_res)

# Load csvs with building profile and ev arrival data
ev_arrivals = pd.read_csv('ev_arrivals/ev_arrivals.csv')
load_profile = pd.read_csv('external_load/load_profile.csv')
ev_arr_nth = 0
ev_dep_nth = 0
ev_dep_nth_last = 0
cs_occ = []

# EV charging data
ev_pwr = n_cs * [0.0]
ev_ch = n_cs * [0.0]
ev_id = n_cs * ['']

# Datetime data to run the simulation
start_datetime = datetime(year = 2025, month = 1, day = 1, hour = 0, minute = 0)
end_datetime = datetime(year = 2025, month = 1, day = 31, hour = 23, minute = 59)
time_interval = timedelta(minutes = 1)
current_datetime = start_datetime
current_date = start_datetime.date()

# Results
bs_pwr_results = pd.DataFrame(columns = ['datetime', 'load', 'cs', 'cp0', 'cp1', 'cp2', 'cp3', 'cp4', 'cp5', 'cp6', 'cp7', 'cp8', 'cp9', 'cp10', 'cp11', 'n_ev'])
bs_evch_results = pd.DataFrame(columns = ['id', 'e_dem', 'e_ch', 'satisfaction', 'cp'])

# Run the simulation
while(current_datetime <= end_datetime):
    cs_occ_n = 0

    if(current_datetime.date() > current_date):
        current_date = current_datetime.date()
        ev_dep_nth_last = ev_dep_nth

    while (str(current_datetime.date()) == ev_arrivals.loc[ev_dep_nth, 'date']):
        ev_dep_nth += 1
    
    for i in range(ev_dep_nth_last, ev_dep_nth):
        if(str(current_datetime.time()) == ev_arrivals.loc[i, 't_dep']):
            for j in range(n_cs):
                if(ev_id[j] == ev_arrivals.loc[i, 'id']):
                    ev_id[j] = ''
                    break

    while ((str(current_datetime.date()) == ev_arrivals.loc[ev_arr_nth, 'date']) and (str(current_datetime.time()) == ev_arrivals.loc[ev_arr_nth, 't_arr'])):
        for i in range(n_cs):
            if(ev_id[i] == ''):
                ev_id[i] = ev_arrivals.loc[ev_arr_nth, 'id']
                break
        ev_arr_nth += 1
    
    for i in range(n_cs):
        if ev_id[i] != '':
            cs_occ_n += 1
        
    cs_occ.append(cs_occ_n)
    print(ev_dep_nth_last, ev_dep_nth)

    current_datetime += time_interval

plt.plot(cs_occ)
plt.show()