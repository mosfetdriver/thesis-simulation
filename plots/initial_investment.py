import matplotlib.pyplot as plt
import matplotlib as mpl


mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman']

bar_font_size = 22
font_size = 22

# Define the initial investments
investments = {
    'Transformer': 12690,
    'Charging Station': 21600,
    'PV System': 30375,
    'Local Storage': 6300
}

# Correct the scenarios so that all include the charging station
scenarios_corrected = {
    'BS': ['Transformer', 'Charging Station'],
    'STD': ['Charging Station'],
    'WF': ['Charging Station'],
    'S1': ['Charging Station', 'PV System'],
    'S2': ['Charging Station', 'PV System', 'Local Storage'],
    'S3': ['Charging Station'],
    'S4': ['Charging Station', 'PV System'],
    'S5': ['Charging Station', 'PV System', 'Local Storage']
}

# Reorder the scenarios so that 'Base Scenario' is on top
scenario_order = ['BS', 'STD', 'WF', 'S1', 'S2', 'S3', 'S4', 'S5']
scenario_order = ['S5', 'S4', 'S3', 'S2', 'S1', 'WF', 'STD', 'BS']

scenario_investments_corrected = {scenario: sum(investments[item] for item in scenarios_corrected[scenario]) for scenario in scenario_order}

# Define custom colors
colors = {
    'Charging Station': '#CCE5FF',
    'Transformer': '#FFCC99',
    'PV System': '#CDEB8B',
    'Local Storage': '#FFCCCC'
}

# Create the horizontal stacked bar plot
plt.figure(figsize=(10, 6))

# Initialize the left position for the stacked bars
lefts = [0] * len(scenario_investments_corrected)

# Ensure Charging Station is always on the left
components_order = ['Charging Station', 'Transformer', 'PV System', 'Local Storage']

# Plot each investment component separately in the correct order with custom colors
for component in components_order:
    component_values = [investments[component] if component in scenarios_corrected[scenario] else 0 for scenario in scenario_order]
    bars = plt.barh(scenario_order, component_values, left=lefts, label=component, color=colors[component])
    lefts = [lefts[i] + component_values[i] for i in range(len(lefts))]

    # Add value labels for each segment
    for bar, xval in zip(bars, component_values):
        if xval > 0:
            plt.text(bar.get_x() + xval/2, bar.get_y() + bar.get_height()/2, f'${xval}', ha='center', va='center', color='black', fontsize=bar_font_size)

# Add total investment labels at the end of each bar, ensuring they are inside the plot frame
#for scenario, total in scenario_investments_corrected.items():
#    plt.text(total - 1000, scenario, f'${total}', va='center', ha='right', color='black')

# Set plot labels and title
plt.title('Initial Investment [$USD]', fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.xticks([], fontsize=font_size)
#plt.title('Initial Investment by Scenario and Component')
plt.legend(fontsize=font_size)
plt.tight_layout()

# Show the plot
plt.show()
