import charging_station as cs

test_cs = cs.ChargingStation("TEST", 30, 6, [6,6,6,6,6,6], [0,0,0,0,0,0], 0, 0)

print(test_cs)

print(test_cs.power_allocation([1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 0, 0], [0,0,0,0,0,0], [6,6,6,6,6,6], [0], [0], 1))