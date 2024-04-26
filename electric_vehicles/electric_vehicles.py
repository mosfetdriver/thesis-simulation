### ELECTRIC VEHICLES FOR SIMULATION ###
#
# A class is created to represent the relevant information needed to simulate the behaviour of the electric vehicles in the system
# 
###

class ElectricVehicle:
    def __init__(self, model, arr_time, dep_time, enrgy_dem):
        self.model = model
        self.arr_time = arr_time
        self.dep_time = dep_time
        self.enrgy_dem = enrgy_dem

    def __str__(self):
        return f"Electric vehicle {self.model} with {self.enrgy_dem} [kWh] of energy demand."