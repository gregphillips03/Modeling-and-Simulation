# Thermostat: two competing balancing loops
# Author: Stephen Davies, PhD

import numpy as np
import matplotlib.pyplot as plt
import math

delta_t = 5/60
time_values = np.arange(0, 24*3, delta_t)

outside_temp = 25*np.sin(2*math.pi/24*time_values) + 20
thermostat = 70              # degF

furnace_rate = 2             # degF/hr
house_leakage_factor = .02   # (degF/hr)/degF

heater_on = np.empty(len(time_values))
heater_on[0] = False
T = np.empty(len(time_values))
T[0] = 55

SMIDGE = .5                  # for hysterisis (degF)

for i in range(1,len(time_values)):
    
    if heater_on[i-1]:
        if T[i-1] - thermostat > SMIDGE:
            heater_on[i] = False
            furnace_heat = 0              # degF/hr
        else:
            heater_on[i] = True
            furnace_heat = furnace_rate   # degF/hr
    else:
        if T[i-1] - thermostat < -SMIDGE:
            heater_on[i] = True
            furnace_heat = furnace_rate   # degF/hr
        else:
            heater_on[i] = False
            furnace_heat = 0              # degF/hr

    leakage_rate = (house_leakage_factor * 
        (T[i-1] - outside_temp[i-1]))      # degF/hr

    T_prime = furnace_heat - leakage_rate

    T[i] = T[i-1] + T_prime * delta_t


plt.plot(time_values,T,color="brown",label="inside temp",
    linewidth=2,linestyle="-")
plt.plot(time_values, outside_temp,color="blue",
        label="outside temp",linewidth=2,linestyle="-")
plt.plot(time_values,
    np.repeat(thermostat,len(time_values)),color="red",
        label="thermostat",linewidth=1,linestyle=":")
plt.plot(time_values,5*heater_on,color="purple",label="heater")
plt.legend()
plt.show()

print("The heater was on about " + str(heater_on.mean() * 100) +
    "% of the day.")