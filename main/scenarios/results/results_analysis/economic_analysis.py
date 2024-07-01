# Libraries
import pandas as pd
from tabulate import tabulate
import numpy as np
import numpy_financial as npf

# Scenarios are loaded
scenarios = ["bs", "wfa", "std", "s1", "s2", "s3", "s4", "s5"]

# Economic results
economic_summary = pd.DataFrame()
economic_summary['item'] = ["electricity bill", "initial_investment", "10-year price", "npv", "irr"]

for col in range(len(scenarios)):
    economic_summary[scenarios[col]] = ""

month_elec_bill = pd.DataFrame(columns = scenarios)

# Energy results from the energy analysis are imported
monthly_cs_kwh = pd.read_csv('main/scenarios/results/results_analysis/energy_results/monthly_cs_kwh.csv')
monthly_grid_kwh = pd.read_csv('main/scenarios/results/results_analysis/energy_results/monthly_grid_kwh.csv')
monthly_injected_kwh = pd.read_csv('main/scenarios/results/results_analysis/energy_results/monthly_injected_kwh.csv')
monthly_max_pwr = pd.read_csv('main/scenarios/results/results_analysis/energy_results/monthly_max_power.csv')
monthly_max_pwr_peak_hour = pd.read_csv('main/scenarios/results/results_analysis/energy_results/monthly_max_power_peak_hour.csv')
energy_summary = pd.read_csv('main/scenarios/results/results_analysis/energy_results/annual_summary.csv')

print(monthly_max_pwr)
print(monthly_max_pwr_peak_hour)

# Energy price calculation
def kwh2clp(grid_kwh, injected_kwh, max_peak_hour_pwr, max_pwr):
    # Fixed
    service_adm = 2088.105
    # Variable
    public_service = 0.75
    energy_transport = 34.079
    energy_cost = 96.017
    # Power
    peak_power_cost = 4710.955
    peak_hour_power_cost = 12999.345  # 18 --> 22 hrs [abril --> septiembre]
    # Injection
    injection_price = 74.003

    return service_adm + (public_service + energy_transport + energy_cost) * grid_kwh - injection_price * injected_kwh + max_peak_hour_pwr * peak_hour_power_cost + max_pwr * peak_power_cost

for i in range(len(scenarios)):
    for j in range(12):
        month_elec_bill.loc[j, scenarios[i]] = kwh2clp(monthly_grid_kwh.loc[j, scenarios[i]], monthly_injected_kwh.loc[j, scenarios[i]], 
                                                       monthly_max_pwr_peak_hour.loc[j, scenarios[i]], monthly_max_pwr.loc[j, scenarios[i]])


# Annual energy price calculation
for i in range(len(scenarios)):
    if i > 4:
        economic_summary.loc[0, scenarios[i]] = month_elec_bill[scenarios[i]].sum() - 150e3 * 12
    else:
        economic_summary.loc[0, scenarios[i]] = month_elec_bill[scenarios[i]].sum()

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
inverter_cost = 750e3
inverter_n = 11
pv_construction_cost = 2e6
pv_roof = 10e6

pv_ii = pv_modules_cost * pv_n + inverter_cost * inverter_n + pv_construction_cost + pv_roof

# BESS initial investment
bess_cost = 5e6
bess_construction_cost = 2e6

bess_ii = bess_cost + bess_construction_cost

for i in range(len(scenarios)):
    if scenarios[i] == "bs":
        ii = cs_ii + trafo_ii
    elif scenarios[i] == "wfa" or scenarios[i] == "std" or scenarios[i] == "s3":
        ii = cs_ii
    elif scenarios[i] == "s1" or scenarios[i] == "s4":
        ii = cs_ii + pv_ii
    elif scenarios[i] == "s2" or scenarios[i] == "s5":
        ii = cs_ii + pv_ii + bess_ii

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

for i in range(len(scenarios)):
    economic_summary.loc[2, scenarios[i]] =  tenyearprice(return_rate, years, energy_summary.loc[4, scenarios[i]] ,economic_summary.loc[0, scenarios[i]], economic_summary.loc[1, scenarios[i]])

# NPV analysis
npv_rate = 0.1
npv_years = 10
sell_price = 200

def npv(rate, term, sell_price, cs_energy, electr_bill, initial_investment):
    income = 0
    for i in range(1,term-1):
        income += (cs_energy * sell_price - electr_bill) / pow(1 + rate, i)

    return income - initial_investment

for i in range(len(scenarios)):
    economic_summary.loc[3, scenarios[i]] = npv(npv_rate, npv_years, sell_price, energy_summary.loc[4, scenarios[i]] ,economic_summary.loc[0, scenarios[i]], economic_summary.loc[1, scenarios[i]])

# IRR analysis
irr_years = 10
irr_sell_price = sell_price

def irr(term, sell_price, cs_energy, electr_bill, initial_investment):
    cash_flow_1 = cs_energy * sell_price - electr_bill
    income_cash_flows = [cash_flow_1] * (term-1) 
    cash_flows = []
    cash_flows.append(-initial_investment)
    cash_flows.extend(income_cash_flows)

    return npf.irr(cash_flows)

for i in range(len(scenarios)):
    economic_summary.loc[4, scenarios[i]] = irr(irr_years, irr_sell_price, energy_summary.loc[4, scenarios[i]] ,economic_summary.loc[0, scenarios[i]], economic_summary.loc[1, scenarios[i]])

economic_summary.to_csv('main/scenarios/results/results_analysis/economic_results/economic_summary.csv', index = False)


def sci_notation(x):
    return f"{x:.2e}"

for i in range(len(scenarios)):
    economic_summary[scenarios[i]] = economic_summary[scenarios[i]].apply(sci_notation)

print(tabulate(economic_summary, headers = 'keys', tablefmt = 'pretty', showindex = False))