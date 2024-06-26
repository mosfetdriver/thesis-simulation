# Libraries
import pandas as pd
import matplotlib.pyplot as plt

# Scenarios are loaded
scenarios = ["bs", "wfa", "std", "s1", "s2", "s3", "s4", "s5"]
scenario = scenarios[7]

month = 6

pwr_results = pd.read_csv(f'main/scenarios/results/{scenario}/pwr/{scenario}_pwr_{month}.csv')

pwr_results.set_index('datetime', inplace = True)
pwr_results.plot()
plt.show()