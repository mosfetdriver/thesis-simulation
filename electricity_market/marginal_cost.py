import pandas as pd

marginal_data = pd.read_csv('electricity_market\marginal_cost_valdivia.csv')

marginal_data = marginal_data.drop('nombre', axis = 1)
marginal_data = marginal_data.drop('barra_mnemotecnico', axis = 1)
marginal_data = marginal_data.drop('barra_referencia_mnemotecnico', axis = 1)
marginal_data = marginal_data.drop('fecha', axis = 1)
marginal_data = marginal_data.drop('hora', axis = 1)


marginal_data = marginal_data.rename(columns = {'costo_en_dolares':'usd',
                                                'costo_en_pesos':'clp'})

marginal_data['usd'] = marginal_data['usd'].str.replace(',', '').astype(float)
marginal_data['clp'] = marginal_data['clp'].str.replace(',', '').astype(float)

last_index = marginal_data.index[-1]
marginal_data = marginal_data.drop(last_index)

start_date = '2025-01-01 00:00:00'
end_date = '2025-12-31 23:00:00'
date_range = pd.date_range(start=start_date, end=end_date, freq='h')
marginal_data['datetime'] = date_range
marginal_data['clpusd'] = marginal_data['clp'] / marginal_data['usd']

indexes = marginal_data[marginal_data['clpusd'] < 150].index

marginal_data.loc[marginal_data['clpusd'] < 150, 'clp'] *= 10
marginal_data['clpusd'] = marginal_data['clp'] / marginal_data['usd']

print(indexes)
print(marginal_data)