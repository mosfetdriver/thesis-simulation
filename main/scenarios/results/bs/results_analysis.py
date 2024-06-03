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
plt.show()

print(ch_results)
print("CS ENERGY: ", ev_ch_total, "LOAD ENERGY: ", load_total)
print("ENERGY COST: ", (ev_ch_total + load_total) * 200)