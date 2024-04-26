### PV MODEL FOR SIMULATION ###
#
# Model from: https://doi.org/10.1016/j.enconman.2023.117501
# P_pv = (I_p / I_s) * D_pv * C_r [1 + alpha(T - T_s)]
#
# P_pv: photovoltaic power [W]
# I_p: incident solar irradiation [W/m^2]
# I_s: incident radiation at STC [W/m^2]
# D_pv: PV derating factor [%/year]
# C_r: rated capacity of the PV array [W]
# alpha: temperature coefficient [%/°C]
# T: operating temperature [°C]
# T_s: STC temperature [°C]
# 
# Irradiance downloaded from tmy (typical meteorological year) data located in: https://solar.minenergia.cl/exploracion
# Location:
# (Lat, Long) = (-39.8332, -73.2452)
# Method: average hourly for a 10 min sample 
# USE GLOBAL RADIATION FOR SIMULATION
# 
# Solar panel model: https://enertik.com/wp-content/uploads/sites/2/documentos/folletos/folleto-panel-solar-restarsolar-rt8i-560mp.pdf
# P_module = 560 [W] (at STC)
# Dimensions = 2274x1134x35 [mm]
# Efficiency = 21.66 [%]
# Lifetime = 30 years
#
# Input/Output Parameters
# Inputs: irradiance, temperature, pv module characteristics
# Output: pv module power
#
###

# Libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# A PV module class is created to define objects with the characteristics needed for the power calculation
class PV_Module:
    def __init__(self, model, nom_power, temp_coeff, year_deg):
        self.model = model
        self.nom_power = nom_power
        self.temp_coeff = temp_coeff
        self.year_deg = year_deg

    def __str__(self):
        return f"PV Module {self.model} with {self.nom_power} [W] nominal power, {self.temp_coeff} [%] temperature coefficient and {self.year_deg} [%] yearly degradation."

    def pv_power_calculation(self, irr, temp, year, current_timestamp):
        stc_temp = 25
        stc_irr = 1000
        initial_datetime = datetime(year = 2025, month = 1, day = 1, hour = 0, minute = 0)
        derating_factor = 1 + ((0.01 * self.year_deg * year) + (0.01 * self.year_deg * ((current_timestamp - initial_datetime.timestamp())/(365 * 24 * 60 * 60))))
        pv_power = (irr / stc_irr) * derating_factor * self.nom_power * (1 + 0.01 * self.temp_coeff * (temp - stc_temp))
        return pv_power

# RestarSolar RT8I -- Power = 560 [W] -- Temperature coefficient = -0.39 [%] -- Yearly degradation = -0.5 [%]
restarsolar_rt8i = PV_Module("RestarSolar RT8I", 560, -0.39, -0.5)

# The data for the irradiation and temperature is imported from the csv and the columns that will not be used are dropped
solar_readings = pd.read_csv("pv_system/solar_irradiance.csv")
solar_readings.drop(columns = ['dir', 'dif', 'sct', 'ghi', 'dirh', 'difh', 'dni', 'vel', 'shadow', 'cloud'], inplace = True)

# To store the interpolated data (1 reading per minute instead of 1 reading per hour), a new empty dataframe is created
pv_results = pd.DataFrame(columns = ['datetime', 'glb', 'temp'])

# New interpolated data is created
start_date = datetime(year = 2025, month = 1, day = 1, hour = 0, minute = 0)
end_date = datetime(year = 2025, month = 12, day = 31, hour = 23, minute = 59)
time_interval = timedelta(minutes = 1)
datetime_list = []
current_date = start_date

index = np.linspace(start_date.timestamp(), end_date.timestamp(), num = 8760)
temp = solar_readings['temp'].tolist()
irr = solar_readings['glb'].tolist()

while (current_date <= end_date):
    datetime_list.append(current_date.strftime('%Y-%m-%d %H:%M'))
    current_date += time_interval

index_interp = np.linspace(start_date.timestamp(), end_date.timestamp(), num = 525600)
temp_interp = np.interp(index_interp, index, temp)
irr_interp = np.interp(index_interp, index, irr)
pv_results['datetime'] = datetime_list
pv_results['glb'] = irr_interp
pv_results['temp'] = temp_interp
pv_power_list = []

for i in range(len(datetime_list)):
    pv_power = restarsolar_rt8i.pv_power_calculation(pv_results.loc[i, 'glb'],
                                                     pv_results.loc[i, 'temp'],
                                                     0,
                                                     datetime.strptime(pv_results.loc[i, 'datetime'], '%Y-%m-%d %H:%M').timestamp())
    pv_power_list.append(pv_power)

pv_results['pv_power'] = pv_power_list
pv_results.to_csv("pv_system/pv_results.csv", index = False)

# The calculation is made to 30 years
pv_results_30y = pd.DataFrame(columns=['pv_power'])
pv_power_30y = 0
pv_power_30y_list = []

for i in range(30):
    print("Year: ", i)
    for j in range(len(datetime_list)):
        pv_power_30y = restarsolar_rt8i.pv_power_calculation(pv_results.loc[j, 'glb'],
                                                        pv_results.loc[j, 'temp'],
                                                        i,
                                                        datetime.strptime(pv_results.loc[j, 'datetime'], '%Y-%m-%d %H:%M').timestamp())
        pv_power_30y_list.append(pv_power_30y)

pv_results_30y['pv_power'] = pv_power_30y_list
pv_results_30y.to_csv("pv_system/pv_results_30y.csv", index = False)