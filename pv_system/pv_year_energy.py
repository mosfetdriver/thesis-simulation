### PV ENERGY CALCULATION ###

# Libraries
import pandas as pd

pv_results = pd.read_csv("pv/pv_results.csv")

pv_power = pv_results['pv_power'].to_list()
pv_energy = 0
n_pv = 1

for i in range(len(pv_power)):
    pv_energy += 0.001 * (pv_power[i] / 60)

print("Total PV energy production is:", n_pv *  pv_energy, "[kWh] per year per", n_pv, "pv-module(s).")