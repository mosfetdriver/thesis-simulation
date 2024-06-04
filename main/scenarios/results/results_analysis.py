### RESULTS ANALYSIS FOR BASE SCENARIO ###

# Libraries
import pandas as pd

scenarios = ["bs", "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "e11", "e12", "e13", "e14"]
energy_results = pd.DataFrame(columns = scenarios)
economic_results = pd.DataFrame(columns = scenarios)

for i in range(3):
    ev_ch_total = 0
    load_total = 0
    sat_evs = 0
    insat_evs = 0
    scenario = scenarios[i]

    for j in range(1, 13):
        ch_results = pd.read_csv(f'main/scenarios/results/{scenario}/{scenario}_evch_{j}.csv')
        pwr_results = pd.read_csv(f'main/scenarios/results/{scenario}/{scenario}_pwr_{j}.csv')

        ev_ch_total += ch_results['e_ch'].sum()
        load_total += pwr_results['load'].sum()
        load_total += load_total / 60

        sat_ch = ch_results[ch_results['satisfaction'] >= 1]
        insat_ch = ch_results[ch_results['satisfaction'] < 1]

        sat_evs += sat_ch.shape[0]
        insat_evs += insat_ch.shape[0]

    pct = sat_evs / (sat_evs + (insat_evs - 316))
    print("SCENARIO:", scenario)
    print("EVs:", sat_evs + insat_evs,"-- SAT EVS:", sat_evs, "-- INSAT EVS:", insat_evs - 316, "-- PCT:", pct*100, "%")
    print("CS ENERGY:", ev_ch_total, "[kWh]")
    print("LOAD ENERGY:", load_total, "[kWh]")
    print("--")