### BATTERY STORAGE FOR SIMULATION ###
#
# A class is created to represent the power and energy behaviour of the battery system
#
# The battery is recharged only by the pv array
# SOC cannot be under 20% and cannot be over 80%
# The efficiency for charging and discharging the battery must be considered
#
###

class BatteryStorage:
    def __init__(self, model, capacity, max_pwr, min_soc, max_soc, efficiency):
        self.model = model
        self.capacity = capacity
        self.max_pwr = max_pwr
        self.min_soc = min_soc
        self.max_soc = max_soc
        self.efficiency = efficiency