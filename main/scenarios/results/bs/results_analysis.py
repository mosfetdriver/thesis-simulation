### RESULTS ANALYSIS FOR BASE SCENARIO ###

# Libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

ch_results = pd.read_csv('main/scenarios/results/bs/bs_evch_results.csv')
pwr_results = pd.read_csv('main/scenarios/results/bs/bs_pwr_results.csv')

pwr_results.plot(x = 'datetime')
plt.show()

print(ch_results)