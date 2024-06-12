### RESULT ANALYSIS FOR SCENARIOS WITH RES ###
# Data for electricity prices in Europe
# https://ember-climate.org/data-catalogue/european-wholesale-electricity-price-data/
# https://transparency.entsoe.eu/dashboard/show

# Libraries
import pandas as pd
import matplotlib.pyplot as plt

#
scenarios = ["e4"]
scenario = scenarios[0]
energy_results = pd.DataFrame(columns = scenarios)
yearly_cost = pd.DataFrame(columns = scenarios)

sat_evs = 0
insat_evs = 0
cs_kwh_grid = 0
cs_kwh_pv = 0
ch_kwh = 0

for j in range(1, 13):
    ch_results = pd.read_csv(f'main/scenarios/results/{scenario}/ch/{scenario}_evch_{j}.csv')
    pwr_results = pd.read_csv(f'main/scenarios/results/{scenario}/pwr/{scenario}_pwr_{j}.csv')

    pwr_results.set_index('datetime', inplace = True)
    pwr_results.plot()
    plt.show()

    pwr_results['subtraction'] = pwr_results['pv'] - pwr_results['cs']
    ch_kwh += ch_results['e_ch'].sum()

    cs_kwh_grid += abs(pwr_results[pwr_results['subtraction'] < 0]['subtraction'].sum() / 60)
    cs_kwh_pv += pwr_results[pwr_results['subtraction'] > 0]['subtraction'].sum() / 60

    sat_ch = ch_results[ch_results['satisfaction'] >= 1]
    insat_ch = ch_results[ch_results['satisfaction'] < 1]

    sat_evs += sat_ch.shape[0]
    insat_evs += insat_ch.shape[0]

print("SAT EVS:", sat_evs)
print("INSAT EVS:", insat_evs)
print("GRID KWH:", cs_kwh_grid)
print("PV KWH:", cs_kwh_pv)

def kwh_to_clp(energy_grid, energy_res):
    #FIXED
    service_adm = 2088.105
    # VARIABLE
    public_service = 0.75
    energy_transport = 34.079
    energy_cost = 96.017

    # CALC
    cost = service_adm + (public_service + energy_transport + energy_cost) * energy_grid - 0.6 * (public_service + energy_transport + energy_cost) * energy_res

    return cost

print("E3 COST:", f"{kwh_to_clp(cs_kwh_grid, cs_kwh_pv):.2e}")


def van_calc(initial_investment, discount_rate, period, cash_flow):
    van_sum = 0
    for i in range(1, period + 1):
        van_sum += cash_flow / pow(1 + discount_rate, i)
    
    van_result = van_sum - initial_investment

    return van_result

# INITIAL INVESTMENT: CHARGING STATION
cs_cost = 750000  
electric_board = 6500000
oocc = 12000000

cs_inv = cs_cost * 12 + electric_board + oocc

# INITIAL INVESTMENT: SOLAR PANELS
sp_cost = 136091 # 560 Watts
sp_struct = 30000 # Frame for the solar panel
sp_cabling = 20000 # Cabling per solar panel
inverter = 500000 # per 5 kVA

n_sp = 90 # 560 * 75 = 42 kW || 560 * 90 = 50 kW
n_inv = 11

# INITIAL INVESTMENT: BATTERY STORAGE SYSTEM

sp_inv = (sp_cost + sp_struct + sp_cabling) * n_sp + inverter * n_inv

e3_ii = sp_inv + cs_inv
discount_rate = 0.05
period = 10
sell_price_kwh = 150 # 107 E3: SELL PRICE 107 to 10 years

bs_cash_flow =  sell_price_kwh * ch_kwh - kwh_to_clp(cs_kwh_grid, cs_kwh_pv)

e3_van = van_calc(e3_ii, discount_rate, period, bs_cash_flow)

print("E3 VAN:", f'{e3_van:.2e}')