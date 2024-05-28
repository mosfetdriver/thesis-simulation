### EXTERNAL LOAD PROFILE FOR SIMULATION ###
# 
# Data for energy consumption downloaded from: https://ieee-dataport.org/documents/electricity-consumption-buildings-hourly-and-monthly-consumption#files
# Used Building C and data gathered for the year 2021
# Data is stored in kWh in steps of 1 hour
# Data must be converted to [p.u.] and must be linearized to time intervals of 1 minute
# Shift data by 6 months !!
#
###

# Libraries
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta

# The csv where the data is stored is read. It is worth to mention that the data is stored per day and in columns of 1 hour
building_energy_raw = pd.read_csv('external_load/building_consumption.csv')

# A list is created to order the data from the csv into two columns: [datetime, power] (To transform from kWh to kW you just divide by 1)
# The list for datetime is created here:
start_date = datetime(year = 2025, month = 1, day = 1, hour = 0)
end_date = datetime(year = 2025, month = 12, day = 31, hour = 23)
time_interval = timedelta(hours = 1)
datetime_list_hour = []
current_date = start_date
while (current_date <= end_date):
    datetime_list_hour.append(current_date.strftime('%Y-%m-%d %H:%M'))
    current_date += time_interval

# The list created for energy is created here:
building_power_hour = []
for i in range(365):
    for j in range(24):
        j_string = str(j)
        building_power_hour.append(building_energy_raw.loc[i,j_string])

# A dataframe is created to store the data in order
# The maximum power consumption is calculated from the power list (It is 303, so the value to divide will be 300) to transform the value to [p.u.]
building_consumption_hr = pd.DataFrame(columns = ['datetime', 'power'])
building_consumption_hr['datetime'] = datetime_list_hour
building_consumption_hr['power'] = building_power_hour
building_consumption_hr.loc[:, 'power'] /= 450

building_pu_hour = building_consumption_hr['power'].to_list()

# To interpolate the data from hours to minutes, we create new lists for datetime and for energy
start_date = datetime(year = 2025, month = 7, day = 4, hour = 0, minute = 0)
end_date = datetime(year = 2026, month = 7, day = 3, hour = 23, minute = 59)
time_interval = timedelta(minutes = 1)
datetime_list_min = []
current_date = start_date
while (current_date <= end_date):
    datetime_list_min.append(current_date.strftime('%Y-%m-%d %H:%M:%S'))
    current_date += time_interval

index = np.linspace(start_date.timestamp(), end_date.timestamp(), num = 8760)
index_interp = np.linspace(start_date.timestamp(), end_date.timestamp(), num = 525600)
building_pwr_min = np.interp(index_interp, index, building_pu_hour)

building_consumption_min = pd.DataFrame(columns = ['datetime', 'power'])
building_consumption_min['datetime'] = datetime_list_min
building_consumption_min['power'] = building_pwr_min

building_consumption_min['datetime'] = building_consumption_min['datetime'].str[5:]
building_consumption_min['datetime'] = '2025-' + building_consumption_min['datetime']

building_consumption_min = building_consumption_min.sort_values(by = 'datetime')

# The results are exported to a csv file
building_consumption_min.to_csv("external_load/load_profile.csv", index = False)