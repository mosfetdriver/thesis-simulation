### RESULTS ANALYSIS FOR BASE SCENARIO ###

# Libraries
import matplotlib.pyplot as plt
import pandas as pd

ch_results = pd.read_csv('main/scenarios/results/bs/bs_evch_results.csv')
pwr_results = pd.read_csv('main/scenarios/results/bs/bs_pwr_results.csv')

ev_ch_total = ch_results['e_ch'].sum()
load_total = pwr_results['load'].sum()
load_total = load_total/60

pwr_results.plot(x = 'datetime')
plt.title("Potencia durante el mes de enero")
plt.ylabel("Potencia [kW]")
plt.xlabel("Tiempo")
plt.show()

sat_ch = ch_results[ch_results['satisfaction'] >= 1]
insat_ch = ch_results[ch_results['satisfaction'] < 1]

sat_evs = sat_ch.shape[0]
insat_evs = insat_ch.shape[0] - 36
pct = sat_evs / (sat_evs + insat_evs)
print("SAT EVS: ", sat_evs, " -- INSAT EVS: ", insat_evs, " -- PCT: ", pct*100, "%")
print("CS ENERGY: ", ev_ch_total, "[kWh]")
print("LOAD ENERGY: ", load_total, "[kWh]")