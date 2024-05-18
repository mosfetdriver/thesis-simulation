###
# EVs arrival and departure probability density functions 
# Obtained from: https://doi.org/10.3390/en13195003
#
# Departure functions:
#
# WF1: Weibull Function 1
# Time interval: [00:00 - 14:00]
# % of total population: 32%
# Distr. parameters: lambda = 12:15 (735m), k = 2h45m (165m)
#
# WF2: Weibull Function 2
# Time interval: [14:00 - 24:00]
# % of total population: 68%
# Distr. parameters: lambda = 17:45 (1065m), k = 3h15m (195m)
#
# k: shape (a in np)
# lambda: scale (n in np)
#
###

# Libraries 
# Weibull Distribution: https://numpy.org/doc/stable/reference/random/generated/numpy.random.weibull.html
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 60*24.)
def weib(x, n, a):
    return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)

shape_am = 20 #a 165
scale_am = 735 #n 

count, bins, ignored = plt.hist(scale_am * np.random.weibull(shape_am, 51))
scale_ = count.max()/weib(x, scale_am, shape_am).max()
plt.plot(x, weib(x, scale_am, shape_am)*scale_)

shape_pm = 15
scale_pm = 1065

count, bins, ignored = plt.hist(scale_pm * np.random.weibull(shape_pm, 109))
scale_ = count.max()/weib(x, scale_pm, shape_pm).max()
plt.plot(x, weib(x, scale_pm, shape_pm)*scale_)
plt.title("Car departure rate")

plt.grid()
plt.show()