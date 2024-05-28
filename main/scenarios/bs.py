### SCENARIO: GRID - CS - EXTERNAL LOAD ###

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
p_load = [0.0] * n_load
p_res = []
itr = 0

# EV charging data
ev_pwr = n_cs * [0.0]
ev_ch = n_cs * [0.0]
ev_dem = n_cs * [0.0]
ev_tin = n_cs * [0.0]
ev_tout = n_cs * [0.0]
ev_id = n_cs * ['']

# Datetime data to run the simulation
start_datetime = datetime(year = 2025, month = 1, day = 1, hour = 0, minute = 0)
end_datetime = datetime(year = 2025, month = 1, day = 2, hour = 23, minute = 59)
time_interval = timedelta(minutes = 1)
current_datetime = start_datetime
current_date = start_datetime.date()

# Results
bs_pwr_results = pd.DataFrame(columns = ['datetime', 'load', 'cs', 'cp0', 'cp1', 'cp2', 'cp3', 'cp4', 'cp5', 'cp6', 'cp7', 'cp8', 'cp9', 'cp10', 'cp11', 'n_ev'])
bs_evch_results = pd.DataFrame(columns = ['id', 'e_dem', 'e_ch', 'satisfaction', 'cp'])

# Run the simulation
while(current_datetime <= end_datetime):
    # The number of EVs in the CS is resetted every minute
    cs_occ_n = 0

    # The external load power is measured here
    p_load[0] = load_profile.loc[itr, 'power'] * p_nom

    # We update the number to not run the entire charging events
    if(current_datetime.date() > current_date):
        current_date = current_datetime.date()
        ev_dep_nth_last = ev_dep_nth

    # The number of departures per day are counted
    while (str(current_datetime.date()) == ev_arrivals.loc[ev_dep_nth, 'date']):
        ev_dep_nth += 1
    
    # The minute for the departures are compared and the EVs left the station when is needed
    for i in range(ev_dep_nth_last, ev_dep_nth):
        if(str(current_datetime.time()) == ev_arrivals.loc[i, 't_dep']):
            for j in range(n_cs):
                if(ev_id[j] == ev_arrivals.loc[i, 'id']):
                    ev_ch_results = {'id': ev_id[j], 'e_dem': ev_dem[j], 'e_ch': ev_ch[j], 'satisfaction': ev_ch[j]/ev_dem[j], 'cp': f"cp{j}"}
                    bs_evch_results = bs_evch_results._append(ev_ch_results, ignore_index = True)
                    ev_id[j] = ''

                    ev_dem[j] = 0.0
                    ev_tin[j] = 0.0
                    ev_tout[j] = 0.0
                    ev_ch[j] = 0.0

                    break

    # Code for the arrival of the EVs to the station
    while ((str(current_datetime.date()) == ev_arrivals.loc[ev_arr_nth, 'date']) and (str(current_datetime.time()) == ev_arrivals.loc[ev_arr_nth, 't_arr'])):
        for i in range(n_cs):
            if(ev_id[i] == ''):
                ev_id[i] = ev_arrivals.loc[ev_arr_nth, 'id']

                ev_dem[i] = ev_arrivals.loc[ev_arr_nth, 'e_dem']
                ev_tin[i] = current_datetime.timestamp()

                dep_str = str(current_datetime.date()) + " " + ev_arrivals.loc[ev_arr_nth, 't_dep']
                dep_datetime = datetime.strptime(dep_str, '%Y-%m-%d %H:%M:%S')
                ev_tout[i] = dep_datetime.timestamp()

                break
        ev_arr_nth += 1

    # Function to allocate power to the EVs
    ev_pwr = FCI_ChSt.power_allocation(ev_dem, ev_ch, ev_tin, ev_tout, p_load, p_res, current_datetime.timestamp())

    
    
    # The amount of EVs present at the station is counted and the charged energy is updated
    for i in range(n_cs):
        ev_ch[i] += ev_pwr[i] * 0.01666666666

        if ev_id[i] != '':
            cs_occ_n += 1

    # Power data is stored
    pwr_results = {'datetime': current_datetime, 'load': p_load[0], 'cs': sum(ev_pwr),
                    'cp0': ev_pwr[0], 'cp1': ev_pwr[1], 'cp2': ev_pwr[2], 'cp3': ev_pwr[3], 'cp4': ev_pwr[4], 'cp5': ev_pwr[5],
                      'cp6': ev_pwr[6], 'cp7': ev_pwr[7], 'cp8': ev_pwr[8], 'cp9': ev_pwr[9], 'cp10': ev_pwr[10], 'cp11': ev_pwr[11], 'n_ev': cs_occ_n}
    
    bs_pwr_results = bs_pwr_results._append(pwr_results, ignore_index = True)

    # The time is updated
    current_datetime += time_interval
    itr += 1



print(bs_pwr_results)
print(bs_evch_results)