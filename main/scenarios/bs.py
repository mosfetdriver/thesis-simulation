### SCENARIO: GRID - CS - EXTERNAL LOAD ###
#
#
#
###

# Libraries and other code
import charging_station as cs
from datetime import datetime, timedelta
import pandas as pd

# Variable names
name = "FCI Charging Station"
p_nom = 80
n_cs = 12
max_ch_pwr = n_cs * [7.4]
min_ch_pwr = n_cs * [0.0]
n_load = 1
n_res = 0

# Object creation
FCI_ChSt = cs.ChargingStation(name, p_nom, n_cs, max_ch_pwr, min_ch_pwr, n_load, n_res)

# Datetime data to run the simulation
start_datetime = datetime(year = 2025, month = 1, day = 1, hour = 0, minute = 0)
end_datetime = datetime(year = 2025, month = 12, day = 31, hour = 23, minute = 59)
time_interval = timedelta(minutes = 1)

# Run the simulation