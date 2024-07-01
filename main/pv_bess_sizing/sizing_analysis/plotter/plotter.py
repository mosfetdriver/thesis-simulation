import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

economic_summary = pd.read_csv('main/pv_bess_sizing/sizing_analysis/economic_results/sizing_economic_summary.csv')

economic_summary = economic_summary.transpose()
economic_summary = economic_summary.reset_index(drop=False)
economic_summary.columns = economic_summary.iloc[0]
economic_summary = economic_summary.drop(economic_summary.index[0])
economic_summary["item"] = ["30P", "60P", "90P", "30P-25kWh", "30P-50kWh", "30P-75kWh", "60P-25kWh", "60P-50kWh", "60P-75kWh", "90P-25kWh", "90P-50kWh", "90P-75kWh"]
economic_summary['irr'] = economic_summary['irr'] * 100


print(economic_summary)
pv_sizing = economic_summary.head(3)
bess_sizing_30p = economic_summary.iloc[3:6]
bess_sizing_60p = economic_summary.iloc[6:9]
bess_sizing_90p = economic_summary.iloc[9:12]


fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, figsize=(8, 10))

pv_sizing.plot(x = 'item', y = 'irr', ax = ax1, kind = 'bar')
ax1.set_title('PV Sizing Configurations IRR')
ax1.set_xlabel('')
ax1.set_ylabel('IRR [%]')
ax1.grid(True)
ax1.set_xticklabels(pv_sizing['item'], rotation=0, ha='center')  # Rotate x-axis labels

if ax1.get_legend() is not None:
    ax1.get_legend().remove()

bess_sizing_30p.plot(x = 'item', y = 'irr', ax = ax2, kind = 'bar')
ax2.set_title('BESS Sizing Configurations IRR (30P)')
ax2.set_xlabel('')
ax2.set_ylabel('IRR [%]')
ax2.grid(True)
ax2.set_xticklabels(bess_sizing_30p['item'], rotation=0, ha='center')  # Rotate x-axis labels


# Remove the legend from the second subplot if it exists
if ax2.get_legend() is not None:
    ax2.get_legend().remove()

bess_sizing_60p.plot(x = 'item', y = 'irr', ax = ax3, kind = 'bar')
ax3.set_title('BESS Sizing Configurations IRR (60P)')
ax3.set_xlabel('')
ax3.set_ylabel('IRR [%]')
ax3.grid(True)
ax3.set_xticklabels(bess_sizing_60p['item'], rotation=0, ha='center')  # Rotate x-axis labels


# Remove the legend from the second subplot if it exists
if ax3.get_legend() is not None:
    ax3.get_legend().remove()


bess_sizing_90p.plot(x = 'item', y = 'irr', ax = ax4, kind = 'bar')
ax4.set_title('BESS Sizing Configurations IRR (90P)')
ax4.set_xlabel('')
ax4.set_ylabel('IRR [%]')
ax4.grid(True)
ax4.set_xticklabels(bess_sizing_90p['item'], rotation=0, ha='center')  # Rotate x-axis labels


# Remove the legend from the second subplot if it exists
if ax4.get_legend() is not None:
    ax4.get_legend().remove()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()