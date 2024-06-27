# Libraries
import pandas as pd
import numpy as np

# Data frame is generated from the csv
marginal_data = pd.read_csv('electricity_market/marginal_cost_valdivia.tsv', sep = '\t')

# The columns that will not be used are dropped
marginal_data = marginal_data.drop('nombre', axis = 1)
marginal_data = marginal_data.drop('barra_mnemotecnico', axis = 1)
marginal_data = marginal_data.drop('barra_referencia_mnemotecnico', axis = 1)
marginal_data = marginal_data.drop('fecha', axis = 1)
marginal_data = marginal_data.drop('hora', axis = 1)
marginal_data = marginal_data.drop('costo_en_pesos', axis = 1)

# Columns are renamed
marginal_data = marginal_data.rename(columns = {'costo_en_dolares':'usd'})

# String values are transformed to float
marginal_data['usd'] = marginal_data['usd'].str.replace(',', '.').astype(float)



# Datetime values are generated
start_date = '2025-01-01 00:00:00'
end_date = '2026-01-01 00:00:00'
date_range = pd.date_range(start=start_date, end=end_date, freq='h')
marginal_data['datetime'] = date_range

# A scaling function is defined
def scale(data, new_min, new_max):
    old_min = np.min(data)
    old_max = np.max(data)
    return new_min + (data - old_min) * (new_max - new_min) / (old_max - old_min)

# Scaled to demand response (1 for low cost - 0.5 for high cost)
marginal_data['demand_response'] = scale(marginal_data['usd'], 1.0, 0.5)

# Data is interpolated to generate 1-minute values
marginal_data.set_index('datetime', inplace = True)
marginal_data_min = marginal_data.resample('min').asfreq()
marginal_data_int = marginal_data_min.interpolate(method = 'linear')

print(marginal_data_int)

# File is exported as csv
marginal_data_int.to_csv('electricity_market/demand_response.csv', index = False)