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
# Irradiance downloaded from: https://solar.minenergia.cl/exploracion
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
# Code explanation: from the csv data, we generate predictions of the irradiance behaviour for the next 30 years with 1 minute interval
#
###

# A PV module class is created to define objects with the characteristics needed for the power calculation
class PV_Module:
    def __init__(self, model, nom_power, temp_coeff, year_deg):
        self.model = model
        self.nom_power = nom_power
        self.temp_coeff = temp_coeff
        self.year_deg = year_deg

    def __str__(self):
        return f"PV Module {self.model} with {self.nom_power} [W] nominal power, {self.temp_coeff} [%] temperature coefficient and {self.year_deg} [%] yearly degradation."

    def pv_power_calculation(self, irr, temp, init_timestamp, curr_timestamp):
        stc_temp = 25
        stc_irr = 1000

        days = (curr_timestamp - init_timestamp) / 86400000

        pv_power = (irr / stc_irr) * (1 + (days * 0.01 * self.year_deg) / 365.25) * self.nom_power * (1 + 0.01 * self.temp_coeff * (temp - stc_temp)) 

        return pv_power

# RestarSolar RT8I -- Power = 560 [W] -- Temperature coefficient = -0.39 [%] -- Yearly degradation = -0.5 [%]
restarsolar_rt8i = PV_Module("RestarSolar RT8I", 560, -0.39, -0.5)

# Import pandas
import pandas as pd

# The data for the irradiation and temperature is imported from the csv and the columns that will not be used are dropped
irradiance_readings = pd.read_csv("pv\solar_irradiance.csv")
irradiance_readings.drop(columns = ['dir', 'dif', 'sct', 'ghi', 'dirh', 'difh', 'dni', 'vel', 'shadow', 'cloud'], inplace = True)

print(type(irradiance_readings['temp'][0]))