###
# EVs arrival and departure probability density functions 
# Obtained from: https://doi.org/10.3390/en13195003
#
# Arrival functions:
# 
# NF1: Normal Function 1
# Time interval: [00:00 - 12:00]
# % of total population: 79%
# Distr. parameters: mu = 09:15 (555m), sigma^2 = 1h30m (90m)
#
# NF2: Normal Function 2
# Time interval: [12:00 - 24:00]
# % of total population: 21%
# Distr. parameters: mu = 14:45 (), sigma^2 = 1h15m
#
###

import numpy as np
import matplotlib.pyplot as plt

# Normal distribution: https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
mu_am, sigma_am = 555, 15 # mean and standard deviation
s =  np.random.normal(mu_am, sigma_am, 126)

x = np.arange(0, 60*24.)
count, bins, ignored = plt.hist(s, 30, density=True)

plt.plot(x,  1/(sigma_am * np.sqrt(2 * np.pi)) *
               np.exp( - (x - mu_am)**2 / (2 * sigma_am**2) ))



mu_pm, sigma_pm = 885, 30
t = np.random.normal(mu_pm, sigma_pm, 34)

count_, bins_, ignored_ = plt.hist(t, 30, density=True)

plt.plot(x,  1/(sigma_pm * np.sqrt(2 * np.pi)) *
               np.exp( - (x - mu_pm)**2 / (2 * sigma_pm**2) ))

plt.title("Car arrival density functions")
plt.grid()


plt.show()