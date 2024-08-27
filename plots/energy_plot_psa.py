import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

plot_date = datetime(year = 2025, month = 2, day = 11)
plot_rer_scenarios = False
plot_psa_scenarios = False
plot_all_scenarios = True

bs_data = pd.read_csv('main/scenarios/results/bs/pwr/bs_pwr_2.csv')
wfa_data = pd.read_csv('main/scenarios/results/wfa/pwr/wfa_pwr_2.csv')
std_data = pd.read_csv('main/scenarios/results/std/pwr/std_pwr_2.csv')
s1_data = pd.read_csv('main/scenarios/results/s1/pwr/s1_pwr_2.csv')
s2_data = pd.read_csv('main/scenarios/results/s2/pwr/s2_pwr_2.csv')
s3_data = pd.read_csv('main/scenarios/results/s3/pwr/s3_pwr_2.csv')
s4_data = pd.read_csv('main/scenarios/results/s4/pwr/s4_pwr_2.csv')
s5_data = pd.read_csv('main/scenarios/results/s5/pwr/s5_pwr_2.csv')

bs_data['datetime'] = pd.to_datetime(bs_data['datetime'])
wfa_data['datetime'] = pd.to_datetime(wfa_data['datetime'])
std_data['datetime'] = pd.to_datetime(std_data['datetime'])
s1_data['datetime'] = pd.to_datetime(s1_data['datetime'])
s2_data['datetime'] = pd.to_datetime(s2_data['datetime'])
s3_data['datetime'] = pd.to_datetime(s3_data['datetime'])
s4_data['datetime'] = pd.to_datetime(s4_data['datetime'])
s5_data['datetime'] = pd.to_datetime(s5_data['datetime'])

bs_data = bs_data[bs_data['datetime'].dt.date == pd.to_datetime('2025-02-11').date()]
wfa_data = wfa_data[wfa_data['datetime'].dt.date == pd.to_datetime('2025-02-11').date()]
std_data = std_data[std_data['datetime'].dt.date == pd.to_datetime('2025-02-11').date()]
s1_data = s1_data[s1_data['datetime'].dt.date == pd.to_datetime('2025-02-11').date()]
s2_data = s2_data[s2_data['datetime'].dt.date == pd.to_datetime('2025-02-11').date()]
s3_data = s3_data[s3_data['datetime'].dt.date == pd.to_datetime('2025-02-11').date()]
s4_data = s4_data[s4_data['datetime'].dt.date == pd.to_datetime('2025-02-11').date()]
s5_data = s5_data[s5_data['datetime'].dt.date == pd.to_datetime('2025-02-11').date()]

bs_data.set_index('datetime', inplace=True)
wfa_data.set_index('datetime', inplace=True)
std_data.set_index('datetime', inplace=True)
s1_data.set_index('datetime', inplace=True)
s2_data.set_index('datetime', inplace=True)
s3_data.set_index('datetime', inplace=True)
s4_data.set_index('datetime', inplace=True)
s5_data.set_index('datetime', inplace=True)

drop_ev_powers = ["cp0", "cp1", "cp2", "cp3", "cp4", "cp5", "cp6", "cp7", "cp8", "cp9", "cp10", "cp11", "n_ev"]
drop_powers = ["pcc", "load", "cs", "n_ev"]




if(plot_psa_scenarios):
    bs_data.drop(drop_powers, axis=1, inplace=True)
    wfa_data.drop(drop_powers, axis=1, inplace=True)
    std_data.drop(drop_powers, axis=1, inplace=True)
    fig, axs = plt.subplots(3, 1, figsize=(8, 16))  # 3 rows, 2 columns

    # First plot
    bs_data.plot(ax=axs[0], legend=True)
    axs[0].legend(['CP0', 'CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CP7', 'CP8', 'CP9', 'CP10', 'CP11'])  # Change the legend text
    axs[0].axhline(y=7.4, color='red', linestyle='--')  # Dashed horizontal line at y=0.5
    axs[0].set_title('Base Scenario')
    axs[0].set_xlabel("")
    axs[0].set_ylabel('Power [kW]')

    # Second plot
    wfa_data.plot(ax=axs[1], legend=False)
    axs[1].set_title('WF Scenario')
    axs[1].axhline(y=7.4, color='red', linestyle='--')  # Dashed horizontal line at y=0.5
    axs[1].set_xlabel("")
    axs[1].set_ylabel('Power [kW]')
    #axs[0, 1].set_ylabel('Y2 axis')

    # Third plot - Span across the bottom row
    std_data.plot(ax=axs[2], legend=False)
    axs[2].set_title('STD Scenario')
    axs[2].axhline(y=7.4, color='red', linestyle='--')  # Dashed horizontal line at y=0.5
    axs[2].set_xlabel("")
    axs[2].set_ylabel('Power [kW]')

    # Adjust spacing between plots
    plt.tight_layout()

    plt.savefig('main/images/psa_results.png')  # Saves the plot as a PNG file

    # Show the plot
    plt.show()

if(plot_all_scenarios):
    bs_data.drop(drop_ev_powers, axis=1, inplace=True)
    bs_cs_data = bs_data['cs']
    bs_data.drop("cs", axis=1, inplace=True)
    bs_data['pv'] = [0.0] * 1440
    bs_data['bess'] = [0.0] * 1440
    bs_data['cs'] = bs_cs_data

    wfa_data.drop(drop_ev_powers, axis=1, inplace=True)
    wfa_cs_data = wfa_data['cs']
    wfa_data.drop("cs", axis=1, inplace=True)
    wfa_data['pv'] = [0.0] * 1440
    wfa_data['bess'] = [0.0] * 1440
    wfa_data['cs'] = wfa_cs_data

    std_data.drop(drop_ev_powers, axis=1, inplace=True)
    std_cs_data = std_data['cs']
    std_data.drop("cs", axis=1, inplace=True)
    std_data['pv'] = [0.0] * 1440
    std_data['bess'] = [0.0] * 1440
    std_data['cs'] = std_cs_data

    s1_data.drop(drop_ev_powers, axis=1, inplace=True)
    s2_data.drop(drop_ev_powers, axis=1, inplace=True)
    s3_data.drop(drop_ev_powers, axis=1, inplace=True)
    s3_cs_data = s3_data['cs']
    s3_data.drop("cs", axis=1, inplace=True)
    s3_data['pv'] = [0.0] * 1440
    s3_data['bess'] = [0.0] * 1440
    s3_data['cs'] = s3_cs_data
    s4_data.drop(drop_ev_powers, axis=1, inplace=True)
    s5_data.drop(drop_ev_powers, axis=1, inplace=True)

    print(bs_data)
    print(s1_data)
    # Create a figure and a set of subplots
    fig, axs = plt.subplots(4, 2, figsize=(16, 12))  # 3 rows, 2 columns

    # First plot
    bs_data.plot(ax=axs[0, 0], legend=True)
    axs[0, 0].legend(['Grid', 'Local Load', 'PV System', 'Local Storage', 'Charging Station'])  # Change the legend text
    axs[0, 0].set_title('Base Scenario')
    axs[0, 0].set_xlabel("")
    axs[0, 0].set_ylabel('Power [kW]')

    # First plot
    wfa_data.plot(ax=axs[0, 1], legend=False)
    axs[0, 1].set_title('WF Scenario')
    axs[0, 1].set_xlabel("")
    axs[0, 1].set_ylabel('Power [kW]')

    # First plot
    std_data.plot(ax=axs[1, 0], legend=False)
    axs[1, 0].set_title('STD Scenario')
    axs[1, 0].set_xlabel("")
    axs[1, 0].set_ylabel('Power [kW]')

    # First plot
    s1_data.plot(ax=axs[1, 1], legend=False)
    axs[1, 1].set_title('Scenario 1')
    axs[1, 1].set_xlabel("")
    axs[1, 1].set_ylabel('Power [kW]')

    # Second plot
    s2_data.plot(ax=axs[2, 0], legend=False)
    axs[2, 0].set_title('Scenario 2')
    axs[2, 0].set_xlabel("")
    axs[2, 0].set_ylabel('Power [kW]')

    # Third plot - Span across the bottom row
    s3_data.plot(ax=axs[2, 1], legend=False)
    axs[2, 1].set_title('Scenario 3')
    axs[2, 1].set_xlabel("")
    axs[2, 1].set_ylabel('Power [kW]')

    # Fourth plot - Span across the bottom row
    s4_data.plot(ax=axs[3, 0], legend=False)
    axs[3, 0].set_title('Scenario 4')
    axs[3, 0].set_xlabel("")
    axs[3, 0].set_ylabel('Power [kW]')

    # Fifth plot - Span across the bottom row

    s5_data.plot(ax=axs[3, 1], legend=False)
    axs[3, 1].set_title('Scenario 5')
    axs[3, 1].set_xlabel("")
    axs[3, 1].set_ylabel('Power [kW]')

    # Adjust spacing between plots
    plt.tight_layout()

    plt.savefig('main/images/all_power_results.png')  # Saves the plot as a PNG file

    # Show the plot
    plt.show()

if(plot_rer_scenarios):
    s1_data.drop(drop_ev_powers, axis=1, inplace=True)
    s2_data.drop(drop_ev_powers, axis=1, inplace=True)
    s3_data.drop(drop_ev_powers, axis=1, inplace=True)
    s3_cs_data = s3_data['cs']
    s3_data.drop("cs", axis=1, inplace=True)
    s3_data['pv'] = [0.0] * 1440
    s3_data['bess'] = [0.0] * 1440
    s3_data['cs'] = s3_cs_data
    s4_data.drop(drop_ev_powers, axis=1, inplace=True)
    s5_data.drop(drop_ev_powers, axis=1, inplace=True)

    # Create a figure and a set of subplots
    fig, axs = plt.subplots(3, 2, figsize=(16, 12))  # 3 rows, 2 columns

    # First plot
    s1_data.plot(ax=axs[0, 0], legend=False)
    axs[0, 0].set_title('Scenario 1')
    axs[0, 0].set_xlabel("")
    axs[0, 0].set_ylabel('Power [kW]')

    # Second plot
    s2_data.plot(ax=axs[0, 1], legend=True)
    axs[0, 1].legend(['Grid', 'Local Load', 'PV System', 'Local Storage', 'Charging Station'])  # Change the legend text
    axs[0, 1].set_title('Scenario 2')
    axs[0, 1].set_xlabel("")
    #axs[0, 1].set_ylabel('Y2 axis')

    # Third plot - Span across the bottom row
    s3_data.plot(ax=axs[1, 0], legend=False)
    axs[1, 0].set_title('Scenario 3')
    axs[1, 0].set_xlabel("")
    axs[1, 0].set_ylabel('Power [kW]')

    # Fourth plot - Span across the bottom row
    s4_data.plot(ax=axs[1, 1], legend=False)
    axs[1, 1].set_title('Scenario 4')
    axs[1, 1].set_xlabel("")
    #axs[1, 1].set_ylabel('Y3 axis')

    # Fifth plot - Span across the bottom row

    s5_data.plot(ax=axs[2, 0], legend=False)
    axs[2, 0].set_title('Scenario 5')
    axs[2, 0].set_xlabel("")
    axs[2, 0].set_ylabel('Power [kW]')

    axs[2, 1].axis("off")

    # Adjust spacing between plots
    plt.tight_layout()

    plt.savefig('main/images/power_results.png')  # Saves the plot as a PNG file

    # Show the plot
    plt.show()