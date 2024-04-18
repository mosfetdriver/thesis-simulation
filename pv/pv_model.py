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
# Output: pv module power output for 30 years
#
# Utilization: from the csv data we generate predictions of the irradiance behaviour for the next 30 years
#
###

# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# PV module characteristics
days = 0
I_s = 1000
C_r = 560
alpha = -0.0039  # conversion used to insert directly into formula -0.39 [%/°C]
T_s = 25
D_pv = (1 - 0.00001369863 * days) # degradation considered to be 0.001369863 [%/day] or 15 [%] for 30 [years] 

print(D_pv)