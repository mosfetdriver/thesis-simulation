### ELECTRIC VEHICLES FOR SIMULATION ###
#
# A class is created to represent the relevant information needed to simulate the behaviour of the electric vehicles in the system
# 
# Models chosen for simulation: 2024 Renault Kwid E-Tech, 2024 Hyundai IONIQ, 2024 BYD Dolphin, 2024 BYD Qin, 
#
###

class ElectricVehicle:
    def __init__(self, model, batt_kwh, start_soc, end_soc, arr_time, dep_time, enrgy_dem):
        self.model     = model
        self.arr_time  = arr_time
        self.dep_time  = dep_time
        self.enrgy_dem = enrgy_dem
        self.batt_kwh  = batt_kwh
        self.start_soc = start_soc
        self.end_soc   = end_soc

    def __str__(self):
        return f"Electric vehicle {self.model} with an energy demand of {self.enrgy_dem}."