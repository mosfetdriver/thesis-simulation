### RESULT ANALYSIS FOR SCENARIOS WITHOUT RES ###

# Libraries
import pandas as pd

scenarios = ["bs", "e1", "e2"]
energy_results = pd.DataFrame(columns = scenarios)
yearly_cost = pd.DataFrame(columns = scenarios)
economic_analysis = pd.DataFrame(columns = scenarios)

bs_energy = []
e1_energy = []
e2_energy = []

for i in range(3):
    ev_ch_total = 0
    load_total = 0
    sat_evs = 0
    insat_evs = 0
    scenario = scenarios[i]

    for j in range(1, 13):
        ch_results = pd.read_csv(f'main/scenarios/results/{scenario}/ch/{scenario}_evch_{j}.csv')
        pwr_results = pd.read_csv(f'main/scenarios/results/{scenario}/pwr/{scenario}_pwr_{j}.csv')

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
            e1_energy.append(monthly_ch)
        elif(i == 2):
            e2_energy.append(monthly_ch)

    pct = sat_evs / (sat_evs + (insat_evs - 316)) # -316
    print("SCENARIO:", scenario)
    print("EVs:", sat_evs + insat_evs,"-- SAT EVS:", sat_evs, "-- INSAT EVS:", insat_evs - 316, "-- PCT:", pct*100, "%")
    print("CS ENERGY:", ev_ch_total, "[kWh]")
    print("LOAD ENERGY:", load_total, "[kWh]")
    print("--")

energy_results['bs'] = bs_energy
energy_results['e1'] = e1_energy
energy_results['e2'] = e2_energy

bs_energy = energy_results['bs'].sum()
e1_energy = energy_results['e1'].sum()
e2_energy = energy_results['e2'].sum()

def kwh_to_clp(energy):
    #FIXED
    service_adm = 2088.105
    # VARIABLE
    public_service = 0.75
    energy_transport = 34.079
    energy_cost = 96.017

    # CALC
    cost = service_adm + (public_service + energy_transport + energy_cost) * energy

    return cost

print("BS COST:", f"{kwh_to_clp(bs_energy):.2e}")
print("E1 COST:", f"{kwh_to_clp(e1_energy):.2e}")
print("E2 COST:", f"{kwh_to_clp(e2_energy):.2e}")



### ECONOMIC ANALYSIS ###
yearly_inflation = 0.03
monthly_inflation = 0.00246627
bs_cost = []
e1_cost = []
e2_cost = []

def kwh_to_clp(energy):
    #FIXED
    service_adm = 2088.105
    # VARIABLE
    public_service = 0.75
    energy_transport = 34.079
    energy_cost = 96.017

    # CALC
    cost = service_adm + (public_service + energy_transport + energy_cost) * energy

    return cost

for i in range(12):
    bs_cost.append(kwh_to_clp(energy_results.loc[i, 'bs']) * (1 + monthly_inflation * i))
    e1_cost.append(kwh_to_clp(energy_results.loc[i, 'e1']) * (1 + monthly_inflation * i))
    e2_cost.append(kwh_to_clp(energy_results.loc[i, 'e2']) * (1 + monthly_inflation * i))

yearly_cost['bs'] = bs_cost
yearly_cost['e1'] = e1_cost
yearly_cost['e2'] = e2_cost

bs_cost_year = []
e1_cost_year = []
e2_cost_year = []

for i in range(20):
    bs_cost_year.append(yearly_cost['bs'].sum() * pow((1 + yearly_inflation), i))
    e1_cost_year.append(yearly_cost['e1'].sum() * pow((1 + yearly_inflation), i))
    e2_cost_year.append(yearly_cost['e2'].sum() * pow((1 + yearly_inflation), i))

economic_analysis['bs'] = bs_cost_year
economic_analysis['e1'] = e1_cost_year
economic_analysis['e2'] = e2_cost_year

# INITIAL INVESTMENT: GRID
transformer_cost = 9000000 # https://www.tiendatecnored.cl/transformador-trifasico-100kva-23kv.html
cables = 500000 # LONG AND WIDTH
transformer_installation = 5000000 # SAESA
pole_post = 300000 # 2X https://www.rielec.cl/108801-poste-horm-10m-450-kr-chilq 

grid_inv = transformer_cost + cables + transformer_installation + 2 * pole_post

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

sp_inv = (sp_cost + sp_struct + sp_cabling) * n_sp + inverter * n_inv
print("")
print("SOLAR INVESTMENT: ", f"{sp_inv:.2e}")


# OTHER ECONOMIC FACTORS
discount_rate = 0.05
period = 10
inflation = 0.03
bs_ii = grid_inv + cs_inv
scenario_ii = cs_inv

kwh_price = 185

bs_cash_flow = (68823) * kwh_price - 9.152825e6
e1_cash_flow = (68671) * kwh_price - 9.132815e6
e2_cash_flow = (65261) * kwh_price - 8.680817e6

def van_calc(initial_investment, discount_rate, period, cash_flow):
    van_sum = 0
    for i in range(1, period + 1):
        van_sum += cash_flow / pow(1 + discount_rate, i)
    
    van_result = van_sum - initial_investment

    return van_result

bs_van = van_calc(bs_ii, discount_rate, period, bs_cash_flow)
e1_van = van_calc(scenario_ii, discount_rate, period, e1_cash_flow)
e2_van = van_calc(scenario_ii, discount_rate, period, e2_cash_flow)


print()
print()
print("kWh PRICE:", kwh_price, "[CLP]")
print("BS VAN:", f"{bs_van:.2e}", "[CLP]")  # 213 - 214 CLP
print("E1 VAN:", f"{e1_van:.2e}", "[CLP]")  # 184 - 185 CLP
print("E2 VAN:", f"{e2_van:.2e}", "[CLP]")  # 187 - 188 CLP
print()
print()