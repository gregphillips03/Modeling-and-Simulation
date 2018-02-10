#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math

april_temp_high = 69; 
april_temp_low = 41; 
may_temp_high = 77; 
may_temp_low = 51; 
jun_temp_high = 85; 
jun_temp_low = 60; 

april_days = 30; 
may_days = 31; 
june_days = 30;
april_time_values = np.arange(0, 24*april_days, 5/60); 
may_time_values = np.arange(0, 24*may_days, 5/60); 
june_time_values = np.arange(0, 24*june_days, 5/60); 

#no of days to run simulation
CONST_DAYS = 3; 
#cost per hour to run heat
#calculated at ((1.06 per therm * 13.8 therm) / day) / 24 hours
heating_cost_rate = .613 #dollar/hr
#cost per hour to run air conditioner
#calculated at 4,320 watts / 1,000 -> 4.32 KW/hr * avg KW/hr of 8.72 for VA
ac_cost_rate = .376 #dollar/hr

#five minute time chunks
delta_t = 5/60;
#0-no of days in 5 minute chunks
time_values = np.arange(0, 24*CONST_DAYS, delta_t);
#variable sine wave as outside temperature
outside_temp = ((april_temp_high - april_temp_low)/2)*np.sin(2*math.pi/24*time_values) + \
 april_temp_high - ((april_temp_high - april_temp_low)/2);
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
#stock vector containing what's been spent on heat
heat_money = np.empty(len(time_values)); 
#stock vector containing what's been spent on cooling
cool_money = np.empty(len(time_values)); 
#buffer to ensure systems don't rapidly turn on and off
BUFFER = .5;                 # for hysterisis (degF)
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
    #difference between the inside temperature of the house and outside temperature
    #multiplied by the leakage factor where lower is better
    leakage_rate = (house_leakage_factor * (T[i-1] - outside_temp[i-1]));      # degF/hr
    #if heater is on
    if heater_on[i]:
        #rate is however much heat the furnace is making, minus what's leaking out
        T_prime = furnace_heat - leakage_rate;
        #pay for it
        heat_money[i] = heating_cost_rate * delta_t; 
    #if air is on
    elif aircon_on[i]:
        #rate is however much is cooling, minus what's leaking out/in
        T_prime = aircon_cool - leakage_rate; 
        #pay for it
        cool_money[i] = ac_cost_rate * delta_t; 
    #neither system is on
    else:
        #no productionn of heat or air, so it's just the difference
        T_prime = 0 - leakage_rate; 
    #current temp becomes last temp plus the product of our time value and prime
    T[i] = T[i-1] + T_prime * delta_t;



plt.plot(time_values,T,
    color="brown",
    label="Inside Temp",
    linewidth=2,linestyle="-");
plt.plot(time_values, outside_temp,
    color="green",
    label="Outside Temp",
    linewidth=2,
    linestyle="-");
plt.plot(time_values,thermostat_heat,
    color="red",
    label="Heat Setting",
    linewidth=1,
    linestyle=":");
plt.plot(time_values,thermostat_airc,
    color="blue",
    label="A/C Setting",
    linewidth=1,
    linestyle=":");
plt.plot(time_values,5*heater_on,
    color="red",
    label="Heater");
plt.plot(time_values,10*aircon_on, 
    color="blue", 
    label="Aircon");
plt.legend();
plt.show();

print("The heater was on about " + 
    str(np.round(heater_on.mean() * 100, 2)) +
    "% of the day.");
print("The a/c was on about " + 
    str(np.round(aircon_on.mean() * 100, 2)) +
    "% of the day.");
print("Simulation generated a total of $" +
	str(np.round(heat_money.sum(), 2)) +
	" in heating costs."); 
print("Simulation generated a total of $" +
	str(np.round(cool_money.sum(), 2)) +
	" in cooling costs."); 