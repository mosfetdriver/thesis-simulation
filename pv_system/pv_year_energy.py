### PV ENERGY CALCULATION ###

# Libraries
import pandas as pd

pv_results = pd.read_csv("pv_system/pv_results.csv")
#pv_results_30y = pd.read_csv("pv_system/pv_results_30y.csv")

pv_power = pv_results['pv_power'].to_list()
#pv_power_30y = pv_results_30y['pv_power'].to_list()

pv_energy = 0
#pv_energy_30y = 0
n_pv = 1
pv_price = 136091 # CLP
pv_lifetime = 30 # years

pv_cost_per_year = pv_price / pv_lifetime

for i in range(len(pv_power)):
    pv_energy += 0.001 * (pv_power[i] / 60)

'''''
for i in range(len(pv_power_30y)):
    pv_energy_30y += 0.001 * (pv_power_30y[i] / 60)
'''''

print("Total pv energy production per year is:", n_pv *  pv_energy, "[kWh] per", n_pv, "pv-module(s).")
print("")
#print("Total pv energy production during its lifetime is:", n_pv * pv_energy_30y, "[kWh] per", n_pv, "pv_module(s).")
#print("")
#print("The cost of the energy produced by the pv-module is", pv_price / pv_energy_30y, "[CLP/kWh].")