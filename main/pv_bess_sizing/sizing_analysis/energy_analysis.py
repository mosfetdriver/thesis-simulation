# Libraries
import pandas as pd
from tabulate import tabulate

# Scenarios are loaded
scenarios = ["n30", "n60", "n90", 
             "n30_25kwh", "n30_50kwh", "n30_75kwh",
             "n60_25kwh", "n60_50kwh", "n60_75kwh",
             "n90_25kwh", "n90_50kwh", "n90_75kwh"]

# Dataframe to store energy results
summary = pd.DataFrame()
summary['description'] = ["insat_evs", "sat_evs", "total_evs", "sat_pct", "cs_energy", "injected_energy", "grid_energy"]
for col in range(len(scenarios)):
    summary[scenarios[col]] = ""

# Dataframe to store monthly energy results
monthly_grid_summ = pd.DataFrame(columns = scenarios)
monthly_injected_summ = pd.DataFrame(columns = scenarios)
monthly_cs_summ = pd.DataFrame(columns = scenarios)

# Base scenario unsatisfied EVs are located
for month in range(1, 13):
    bs_ch_results = pd.read_csv(f'main/scenarios/results/bs/ch/bs_evch_{month}.csv')
    bs_insat_ch = bs_ch_results[bs_ch_results['satisfaction'] < 1]
    #print(bs_insat_ch)


# Economic analysis is generated
for i in range(3):
    ev_ch_total = 0
    load_total = 0
    sat_evs = 0
    insat_evs = 0
    scenario = scenarios[i]
    injected_energy = 0
    grid_energy = 0
    monthly_grid_list = []
    monthly_injected_list = []
    monthly_cs_list = []

    for month in range(1, 13):
        if (i < 3):
            ch_results = pd.read_csv(f'main/pv_bess_sizing/sizing_results/pv/{scenario}/ch/{scenario}_evch_{month}.csv')
            pwr_results = pd.read_csv(f'main/pv_bess_sizing/sizing_results/pv/{scenario}/pwr/{scenario}_pwr_{month}.csv')
        else:
            ch_results = pd.read_csv(f'main/pv_bess_sizing/sizing_results/bess/{scenario}/ch/{scenario}_evch_{month}.csv')
            pwr_results = pd.read_csv(f'main/pv_bess_sizing/sizing_results/bess/{scenario}/pwr/{scenario}_pwr_{month}.csv')

        monthly_ch = ch_results['e_ch'].sum()
        ev_ch_total += ch_results['e_ch'].sum()
        load_total += pwr_results['load'].sum() / 60

        pwr_results['subtraction'] = pwr_results['pv'] + pwr_results['bess'] - pwr_results['cs']

        monthly_grid = abs(pwr_results[pwr_results['subtraction'] < 0]['subtraction'].sum() / 60)
        monthly_injected = pwr_results[pwr_results['subtraction'] > 0]['subtraction'].sum() / 60

        grid_energy += abs(pwr_results[pwr_results['subtraction'] < 0]['subtraction'].sum() / 60)
        injected_energy += pwr_results[pwr_results['subtraction'] > 0]['subtraction'].sum() / 60

        sat_ch = ch_results[ch_results['satisfaction'] >= 1]
        insat_ch = ch_results[ch_results['satisfaction'] < 1]

        sat_evs += sat_ch.shape[0]
        insat_evs += insat_ch.shape[0]

        monthly_grid_list.append(monthly_grid)
        monthly_injected_list.append(monthly_injected)
        monthly_cs_list.append(monthly_ch)

    pct = sat_evs / (sat_evs + (insat_evs)) # -316 is the base scenario number of insatisfied evs

    summary.loc[0, scenario] = insat_evs
    summary.loc[1, scenario] = sat_evs
    summary.loc[2, scenario] = insat_evs + sat_evs
    summary.loc[3, scenario] = pct
    summary.loc[4, scenario] = ev_ch_total
    summary.loc[5, scenario] = injected_energy
    summary.loc[6, scenario] = grid_energy

    monthly_grid_summ[scenarios[i]] = monthly_grid_list
    monthly_injected_summ[scenarios[i]] = monthly_injected_list
    monthly_cs_summ[scenarios[i]] = monthly_cs_list


print(tabulate(summary, headers = 'keys', tablefmt = 'pretty', showindex = False))

summary.to_csv('main/pv_bess_sizing/sizing_analysis/energy_results/sizing_summary.csv', index = False)
monthly_grid_summ.to_csv('main/pv_bess_sizing/sizing_analysis/energy_results/sizing_monthly_grid_kwh.csv', index = False)
monthly_injected_summ.to_csv('main/pv_bess_sizing/sizing_analysis/energy_results/sizing_monthly_injected_kwh.csv', index = False)
monthly_cs_summ.to_csv('main/pv_bess_sizing/sizing_analysis/energy_results/sizing_monthly_cs_kwh.csv', index = False)