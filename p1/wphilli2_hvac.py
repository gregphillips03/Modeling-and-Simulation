#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math

CONST_DAYS = 3; 
#five minute time chunks
delta_t = 5/60;
#0-72 in 5 minute chunks
time_values = np.arange(0, 24*CONST_DAYS, delta_t);
#variable sine wave as outside temperature
outside_temp = 25*np.sin(2*math.pi/24*time_values) + 20;
#heater thermostat settings for normal times
normal_day_heat = np.concatenate([np.repeat(68, int(8 / delta_t)),
                          np.repeat(74, int(8 / delta_t)), 
                          np.repeat(70, int(8 / delta_t))]); 
#heater thermostat settings for vacation times
vacay_day_heat = np.concatenate([np.repeat(55, int(24 / delta_t))]); 
#air conditioner thermostat settings for normal times
normal_day_airc = np.concatenate([np.repeat(82, int(8 / delta_t)),
                          np.repeat(79, int(8 / delta_t)), 
                          np.repeat(79, int(8 / delta_t))]); 
#air conditioner thermostat settings for vacation times
vacay_day_cool = np.concatenate([np.repeat(88, int(24 / delta_t))]); 
#rep the daily settings 
thermostat_heat = np.tile(normal_day_heat, CONST_DAYS); 
thermostat_airc = np.tile(normal_day_airc, CONST_DAYS); 
#rep the vacation settings
vacay_thermo_heat = np.tile(vacay_day_heat, CONST_DAYS); 
vacay_thermo_cool = np.tile(vacay_day_cool, CONST_DAYS); 
#how hard the furnace heats
furnace_rate = 2.0;             # degF/hr
#how hard the a/c cools
aircon_rate = -1.5;            # degF/hr
#level of insulation
house_leakage_factor = .02;     # (degF/hr)/degF
#vector containing if the heater was on
heater_on = np.empty(len(time_values));
#initially set to off
heater_on[0] = False;
#vector containing if the a/c was on
aircon_on = np.empty(len(time_values)); 
#initially set to off
aircon_on[0] = False; 
#stock vector containing the inside temperature of the house
T = np.empty(len(time_values));
#initially 55 degrees in the house
T[0] = 55;
#buffer to ensure systems don't rapidly turn on and off
BUFFER = 1.0;                 # for hysterisis (degF)
#simulation loop
for i in range(1,len(time_values)):
    #if the heater is on
    if heater_on[i-1]:
        #if current temperature - heat setting is greater than buffer
        #82 - 80 > 1
        if T[i-1] - thermostat_heat[i-1] > BUFFER:
            #turn off heater
            heater_on[i] = False;
            #no more furnace heat
            furnace_heat = 0;             # degF/hr
        #if current temperature - heat setting is not greater than buffer
        #81 - 80 = 1 is not greater 1
        else:
            #keep heater on
            heater_on[i] = True;
            #keep pushing out heat
            furnace_heat = furnace_rate;   # degF/hr
    #if the air conditioner is on
    elif aircon_on[i-1]:
        #if current temperature - cooling setting is less than -buffer
        #68 - 70 = -2 < -1
        if T[i-1] - thermostat_airc[i-1] < -BUFFER:
            #turn off a/c
            aircon_on[i] = False;
            #no more cold air
            aircon_cool = 0;
        #if current temperature - coolsing setting is not less than -buffer
        # 69 - 70 = -1 is not less than -1
        else:
            #keep a/c on
            aircon_on[i] = True; 
            #keep pushing out cold air
            aircon_cool = aircon_rate; 
    #if the heater and air conditioner are not on
    else:
        #if it's just too cold
        if T[i-1] - thermostat_heat[i-1] < BUFFER:
            heater_on[i] = True;
            furnace_heat = furnace_rate;   # degF/hr
        #if it's warm enough but not too warm
        elif T[i-1] - thermostat_heat[i-1] > BUFFER and T[i-1] < thermostat_airc[i-1]:
            heater_on[i] = False;
            furnace_heat = 0;              # degF/hr
            aircon_on[i] = False;
            aircon_cool = 0; 
        #if it's just too hot
        elif T[i-1] - thermostat_airc[i-1] > BUFFER:
            aircon_on[i] = True; 
            aircon_cool = aircon_rate; 

    leakage_rate = (house_leakage_factor * (T[i-1] - outside_temp[i-1]));      # degF/hr

    if heater_on[i]:
        T_prime = furnace_heat - leakage_rate;
    elif aircon_on[i]:
        T_prime = aircon_cool - leakage_rate; 
    else:
        T_prime = 0 - leakage_rate; 

    T[i] = T[i-1] + T_prime * delta_t


plt.plot(time_values,T,color="brown",label="inside temp",
    linewidth=2,linestyle="-")
plt.plot(time_values, outside_temp,color="green",
        label="outside temp",linewidth=2,linestyle="-")
plt.plot(time_values,thermostat_heat,color="red",
        label="thermostat",linewidth=1,linestyle=":")
plt.plot(time_values,thermostat_airc,color="blue",
        label="thermostat",linewidth=1,linestyle=":")
plt.plot(time_values,5*heater_on,color="red",label="heater")
plt.plot(time_values,10*aircon_on, color="blue", label="a/c")
plt.legend()
plt.show()

print("The heater was on about " + str(np.round(heater_on.mean() * 100, 2)) +
    "% of the day.")
print("The a/c was on about " + str(np.round(aircon_on.mean() * 100, 2)) +
    "% of the day.")