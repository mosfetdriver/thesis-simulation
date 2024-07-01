# Libraries
import pandas as pd
from tabulate import tabulate
import numpy as np
import numpy_financial as npf

# Scenarios are loaded
scenarios = ["n30", "n60", "n90", 
             "n30_25kwh", "n30_50kwh", "n30_75kwh",
             "n60_25kwh", "n60_50kwh", "n60_75kwh",
             "n90_25kwh", "n90_50kwh", "n90_75kwh"]

# Economic results
economic_summary = pd.DataFrame()
economic_summary['item'] = ["electricity bill", "initial_investment", "10-year price", "npv", "irr"]
for col in range(len(scenarios)):
    economic_summary[scenarios[col]] = ""

# Energy results from the energy analysis are imported
monthly_cs_kwh = pd.read_csv('main/pv_bess_sizing/sizing_analysis/energy_results/sizing_monthly_cs_kwh.csv')
monthly_grid_kwh = pd.read_csv('main/pv_bess_sizing/sizing_analysis/energy_results/sizing_monthly_grid_kwh.csv')
monthly_injected_kwh = pd.read_csv('main/pv_bess_sizing/sizing_analysis/energy_results/sizing_monthly_injected_kwh.csv')
energy_summary = pd.read_csv('main/pv_bess_sizing/sizing_analysis/energy_results/sizing_summary.csv')

# Energy price calculation
def kwh2clp(grid_kwh, injected_kwh):
    # Fixed
    service_adm = 2088.105
    # Variable
    public_service = 0.75
    energy_transport = 34.079
    energy_cost = 96.017
    # Injection
    injection_price = 74.003

    return service_adm + (public_service + energy_transport + energy_cost) * grid_kwh - injection_price * injected_kwh

# Annual energy price calculation
for i in range(3):#len(scenarios)):
    economic_summary.loc[0, scenarios[i]] = kwh2clp(energy_summary.loc[6, scenarios[i]], energy_summary.loc[5, scenarios[i]])

# Transformer initial investment
transformer_cost = 10e6
cables = 500e3
transformer_installation = 3e6 
pole_post = 600e3

trafo_ii = transformer_cost + cables +transformer_installation + pole_post

# CS initial investment
cp_cost = 750e3
cp_n = 12
cs_construction_cost = 15e6

cs_ii = cp_n * cp_cost + cs_construction_cost

# PV system initial investment
pv_modules_cost = 150e3
pv_n = 90
inverter_cost = 500e3
inverter_n = 10
pv_construction_cost = 5e6

pv_ii = pv_modules_cost * pv_n + inverter_cost * inverter_n + pv_construction_cost

# BESS initial investment
bess_cost_25kwh = 5e6
bess_cost_50kwh = 14e6
bess_cost_75kwh = 40e6
bess_construction_cost = 2.0e6

bess_25wkh_ii = bess_cost_25kwh + bess_construction_cost
bess_50wkh_ii = bess_cost_50kwh + bess_construction_cost
bess_75wkh_ii = bess_cost_75kwh + bess_construction_cost


for i in range(3):
    if i < 3:
        ii = 10000000

    economic_summary.loc[1, scenarios[i]] = ii

# 10 year energy price return price
return_rate = 0.1
years = 10

def tenyearprice(rate, term, cs_energy, electr_bill, initial_investment):
    cs_energy_term = 0
    electr_bill_term = 0

    for i in range(1, term -1):
        cs_energy_term += cs_energy / pow(1 + rate, i)
        electr_bill_term += electr_bill / pow(1 + rate, i)
    
    return (initial_investment + electr_bill_term) / (cs_energy_term)

for i in range(3):
    economic_summary.loc[2, scenarios[i]] =  tenyearprice(return_rate, years, energy_summary.loc[4, scenarios[i]] ,economic_summary.loc[0, scenarios[i]], economic_summary.loc[1, scenarios[i]])

# NPV analysis
npv_rate = 0.1
npv_years = 10
sell_price = 180

def npv(rate, term, sell_price, cs_energy, electr_bill, initial_investment):
    income = 0
    for i in range(1,term-1):
        income += (cs_energy * sell_price - electr_bill) / pow(1 + rate, i)

    return income - initial_investment

for i in range(3):
    economic_summary.loc[3, scenarios[i]] = npv(npv_rate, npv_years, sell_price, energy_summary.loc[4, scenarios[i]] ,economic_summary.loc[0, scenarios[i]], economic_summary.loc[1, scenarios[i]])

# IRR analysis
irr_years = 10
irr_sell_price = 180

def irr(term, sell_price, cs_energy, electr_bill, initial_investment):
    cash_flow_1 = cs_energy * sell_price - electr_bill
    income_cash_flows = [cash_flow_1] * (term-1) 
    cash_flows = []
    cash_flows.append(-initial_investment)
    cash_flows.extend(income_cash_flows)

    return npf.irr(cash_flows)

for i in range(3):
    economic_summary.loc[4, scenarios[i]] = irr(irr_years, irr_sell_price, energy_summary.loc[4, scenarios[i]] ,economic_summary.loc[0, scenarios[i]], economic_summary.loc[1, scenarios[i]])


print(tabulate(economic_summary, headers = 'keys', tablefmt = 'pretty', showindex = False))