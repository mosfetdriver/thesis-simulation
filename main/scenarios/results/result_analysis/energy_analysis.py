# Libraries
import pandas as pd
import matplotlib.pyplot as plt

# Scenarios are loaded
scenarios = ["bs", "wfa", "std", "s1", "s2", "s3", "s4", "s5"]
scenario = scenarios[7]

# Data is stored monthly, so a variable to access them is created
month = 12

# Dataframe to store energy results
energy_results = pd.DataFrame(columns = scenarios)
summary = pd.DataFrame()
summary['description'] = ["insat_evs", "sat_evs", "total_evs", "pct_to_bs", "cs_energy", "load_energy"]

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

        if(i == 0):
            bs_energy.append(monthly_ch)
        elif(i == 1):
            wfa_energy.append(monthly_ch)
        elif(i == 2):
            std_energy.append(monthly_ch)
        elif(i == 3):
            s1_energy.append(monthly_ch)
        elif(i == 4):
            s2_energy.append(monthly_ch)
        elif(i == 5):
            s3_energy.append(monthly_ch)
        elif(i == 6):
            s4_energy.append(monthly_ch)
        elif(i == 7):
            s5_energy.append(monthly_ch)

    pct = sat_evs / (sat_evs + (insat_evs - 316)) # -316
    print("SCENARIO:", scenario)
    print("EVs:", sat_evs + insat_evs,"-- SAT EVS:", sat_evs, "-- INSAT EVS:", insat_evs - 316, "-- PCT:", pct*100, "%")
    print("CS ENERGY:", ev_ch_total, "[kWh]")
    print("LOAD ENERGY:", load_total, "[kWh]")
    print("--")

    summary.loc[0, scenario] = insat_evs
    summary.loc[1, scenario] = sat_evs
    summary.loc[2, scenario] = insat_evs + sat_evs
    summary.loc[3, scenario] = pct
    summary.loc[4, scenario] = ev_ch_total
    summary.loc[5, scenario] = load_total

energy_results['bs'] = bs_energy
energy_results['wfa'] = wfa_energy
energy_results['std'] = std_energy
energy_results['s1'] = s1_energy
energy_results['s2'] = s2_energy
energy_results['s3'] = s3_energy
energy_results['s4'] = s4_energy
energy_results['s5'] = s5_energy


bs_energy = energy_results['bs'].sum()
wfa_energy = energy_results['wfa'].sum()
std_energy = energy_results['std'].sum()
s1_energy = energy_results['s1'].sum()
s2_energy = energy_results['s2'].sum()
s3_energy = energy_results['s3'].sum()
s4_energy = energy_results['s4'].sum()
s5_energy = energy_results['s5'].sum()

print(summary)