# Libraries
import pandas as pd
import matplotlib.pyplot as plt

# Scenarios are loaded
scenarios = ["bs", "wfa", "std", "s1", "s2", "s3", "s4", "s5"]
scenario = scenarios[7]

# Data is stored monthly, so a variable to access them is created
month = 12

# Dataframe to store energy results
summary = pd.DataFrame()
summary['description'] = ["insat_evs", "sat_evs", "total_evs", "pct_to_bs", "cs_energy", "load_energy", "res_energy", "grid_energy"]

for col in range(len(scenarios)):
    summary[scenarios[col]] = ""

# Lists to store monthly energy are created
bs_energy = []
wfa_energy = []
std_energy = []
s1_energy = []
s2_energy = []
s3_energy = []
s4_energy = []
s5_energy = []
s6_energy = []
s7_energy = []

for i in range(8):
    ev_ch_total = 0
    load_total = 0
    sat_evs = 0
    insat_evs = 0
    scenario = scenarios[i]

    for month in range(1, 13):
        ch_results = pd.read_csv(f'main/scenarios/results/{scenario}/ch/{scenario}_evch_{month}.csv')
        pwr_results = pd.read_csv(f'main/scenarios/results/{scenario}/pwr/{scenario}_pwr_{month}.csv')

        monthly_ch = ch_results['e_ch'].sum()
        ev_ch_total += ch_results['e_ch'].sum()
        load_total += pwr_results['load'].sum() / 60

        sat_ch = ch_results[ch_results['satisfaction'] >= 1]
        insat_ch = ch_results[ch_results['satisfaction'] < 1]

        sat_evs += sat_ch.shape[0]
        insat_evs += insat_ch.shape[0]

    pct = sat_evs / (sat_evs + (insat_evs - 316)) # -316 is the base scenario number of insatisfied evs

    summary.loc[0, scenario] = insat_evs
    summary.loc[1, scenario] = sat_evs
    summary.loc[2, scenario] = insat_evs + sat_evs
    summary.loc[3, scenario] = pct
    summary.loc[4, scenario] = ev_ch_total
    summary.loc[5, scenario] = load_total

print(summary)