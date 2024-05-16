import numpy as np
from scipy.stats import norm
import time

# Parameters of the normal distribution
mean_arrival_rate = 10  # Mean arrival rate (vehicles per hour)
std_dev = 2             # Standard deviation

# Function to calculate probability of arrival up to present time
def calculate_probability(mean, std_dev, present_time):
    return norm.cdf(present_time, loc=mean, scale=std_dev)

# Simulate real-time updates
present_time = 0
time_increment = 0.1  # Adjust as needed for the frequency of updates
prob_arrival = 0

while prob_arrival < 1:
    # Calculate the probability of arrival up to the present time
    prob_arrival = calculate_probability(mean_arrival_rate, std_dev, present_time)
    
    # Print the probability
    print("Probability of arrival up to present time:", prob_arrival)
    
    # Increment present time
    present_time += time_increment
    
    # Wait before the next update
    time.sleep(time_increment)