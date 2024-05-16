import numpy as np
import matplotlib.pyplot as plt
import scipy.special

# Parámetros de la distribución normal
mu = 555  # media
sigma = 100  # desviación estándar

# Generar datos para el eje x
x = np.linspace(0, 24*60, 24*60)

# Calcular la CDF de la distribución normal
cdf = 0.5 * (1 + scipy.special.erf((x - mu) / (np.sqrt(2) * sigma)))

# Graficar la CDF
plt.plot(x, cdf)
plt.title('Normal distribution CDF')
plt.xlabel('Minutes [min]')
plt.ylabel('CDF')
plt.grid(True)
plt.show()