### CS MODEL FOR SIMULATION ###
#
# A charging station class with n charging points with variable power is created to assign power to the electric vehicles located in it
#
###

# A class is created to implement the charging station
class ChargingStation:
    def __init__(self, name, P_nom, n_cs, P_ch_max, P_ch_min, n_load, n_res):
        self.name        = name           ## Charging station identifier
        self.P_nom       = P_nom          ## Maximum power from electrical network
        self.n_cs        = n_cs           ## Number of charging points
        self.P_ch_max    = P_ch_max       ## Maximum charging power
        self.P_ch_min    = P_ch_min       ## Minimum charging power
        self.n_load      = n_load         ## Number of external loads
        self.n_res       = n_res          ## Number of renewable energy sources

    def __str__(self):
        return f"Charging station {self.name} with {self.n_cs} charging points with {self.P_ch_max} [kW] of maximum power."
    
    def water_filling_algorithm(self, E_dem, E_ch, t_in, t_out, P_load, P_res, actual_time):
        P_ref         = [0, 0, 0, 0]                        # Potencia de referencia de cada vehículo
        P_load_sum    = 0.0                                 # Suma de las potencias de las cargas externas
        P_res_sum     = 0.0                                 # Suma de las potencias de la generación local
        cp_occupation = [0, 0, 0, 0]                        # Vector que muestra la disponibilidad de puntos de carga
        ev_n          = 0                                   # Número de vehículos presentes en la estación
        w             = [0, 0, 0, 0]                        # Pesos
        P_dem         = [0.0, 0.0, 0.0, 0.0]                # Demanda de potencia media de cada vehículo
        P_ref_sum = 0

        def wfa_function(power_budget, dem_power, max_power, occupation):
            sum_power = 0.0
            n_ev = 0
            n_cp = 4
            ref_power = [0.0] * n_cp
            is_max_power_vector = [0] * n_cp
            is_max_power = 0
            max_power_n = 0
            dem_power_subt = [0.0] * (n_cp - 1)

            # La potencia máxima y la demanda de los vehículos se asigna en 0 si es que el vehículo no está presente en la estación
            for i in range(n_cp):
                max_power[i] = occupation[i] * max_power[i]
                dem_power[i] = occupation[i] * dem_power[i]
                if occupation[i]:
                    n_ev += 1
            
            # Se ejecuta el código solo si hay vehículos presentes en la estación y si la potencia disponible es mayor a 0
            if (n_ev > 0) and (power_budget > 0):
                # Se ordenan las potencias medias demandadas de mayor a menor
                dem_power_sorted = sorted(dem_power, reverse=True)
                dem_power_index = [index for index, _ in sorted(enumerate(dem_power), key = lambda x: x[1], reverse = True)]

                # Se restan las potencias demandadas para organizarlas de acuerdo al gráfico
                for i in range(len(dem_power_subt)):
                    dem_power_subt[i] = dem_power_sorted[i] - dem_power_sorted[i+1]

                # Se asigna potencia, dependiendo de la potencia disponible y de la diferencia que existe entre la demanda mayor y la que la sigue
                for i in range(1, len(dem_power) + 1):
                    if i < len(dem_power):
                        sum_power = min((power_budget / i), dem_power_subt[i - 1])
                    else:
                        sum_power = power_budget / i

                    for j in range(i):
                        ref_power[dem_power_index[j]] += sum_power
                    # Se resta la potencia asignada a la potencia disponible
                    power_budget -= i * sum_power
                
                sum_power = 0
                power_budget = 0

                # Esta parte del código verifica si hay vehículos a los que se les haya asignado más potencia de la potencia máxima
                while(not(is_max_power)):
                    for j in range(n_cp):
                        for i in range(n_cp):
                            if(ref_power[i] > max_power[i]):
                                power_budget += ref_power[i] - max_power[i]
                                ref_power[i] = max_power[i]
                                is_max_power_vector[i] = 1
                        
                        # Si ya no queda potencia extra se declara la variable is_max_power como verdadera
                        if(power_budget == 0):
                            is_max_power = 1
                            
                        max_power_n = sum(1 for i in is_max_power_vector if i == 1)

                        if((max_power_n > 0) and (max_power_n < n_cp)):
                            sum_power = power_budget / (n_cp - max_power_n)

                            for i in range(n_cp):
                                if((not is_max_power_vector[i])):
                                    ref_power[i] += sum_power
                            power_budget -= sum_power * (n_cp - max_power_n)

                        # Si la cantidad de vehículos que llegan a su potencia máxima se declara is_max_power como verdadera    
                        elif(max_power_n >= n_ev):
                            is_max_power = 1

            # En caso de no haber vehículos en la estación o si no hay potencia disponible, las referencias se hacen 0
            else:
                ref_power = [0.0] * len(ref_power)

            return ref_power

        for i in range(self.n_load):
            P_load_sum += P_load[i]

        for i in range(self.n_res):
            P_res_sum += P_res[i] 

        P_ava = self.P_nom - P_load_sum + P_res_sum

        for i in range(self.n_cs):
            if((actual_time < t_out[i]) and (t_in[i] < actual_time) and (E_dem[i] > E_ch[i])):
                cp_occupation[i] = 1
                ev_n += 1
            else:
                cp_occupation[i] = 0

        for i in range(self.n_cs):
            if cp_occupation[i]:
                P_dem[i] = 60.0 * ((E_dem[i] - E_ch[i]) / (t_out[i] - actual_time))
            else:
                P_dem[i] = 0.0
            
            if P_dem[i] > 22.0:
                P_dem[i] = 22.0

            if P_dem[i] < 0.0:
                P_dem[i] = 0.0

        P_ref = wfa_function(P_ava, P_dem, [22.0, 22.0, 22.0, 22.0], cp_occupation)

        for i in range(self.n_cs):
            P_ref_sum += P_ref[i]
        
        if P_ref_sum > 0:
            for i in range(self.n_cs):
                w[i] = P_ref[i] / P_ref_sum 
        else:
            w = [0.0] * self.n_cs
        
        return P_ref, w