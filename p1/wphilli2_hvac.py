#!/usr/bin/env python3

import numpy as np; 
import matplotlib.pyplot as plt; 
import math; 
import sys; 

def p1(freeze, sweater, tea):

    #is there a cold snap?
    if(freeze == 'false'):
        isFreeze = False;
    else:
        isFreeze = True; 
    #person wearinga sweater to stay warm?
    if(sweater == 'false'):
        atHomeHeat = 74;
    else: 
        atHomeHeat = 68 ; 
    #person drinking tea to stay cooler
    if(tea == 'false'):
        atHomeHeat = 74;
        atHomeCool = 79
    else: 
        atHomeHeat = 68; 
        atHomeCool = 83; 


    #temp ranges from climate.gov
    april_temp_high = 69; 
    april_temp_low = 41; 
    may_temp_high = 77; 
    may_temp_low = 51; 
    june_temp_high = 100; #changed from 85
    june_temp_low = 60; 

    #constants as number of days
    april_days = 30; 
    april_days_alt = 23; #for the freeze
    may_days = 31; 
    june_days = 30;
    freeze_days = 7; 

    #five minute time chunks
    delta_t = 5/60;

    #vacation time frame
    vacay_time = np.arange(8640, 10656, 1); 
    #freezing weather time
    freeze_time = np.arange(0, 4032, 1); 

    #time values for each month
    if(isFreeze==True):
        freeze_time_values = np.arange(0, 24*freeze_days, delta_t); 
        april_time_values = np.arange(0, 24*april_days_alt, delta_t);
        may_time_values = np.arange(0, 24*may_days, delta_t); 
        june_time_values = np.arange(0, 24*june_days, delta_t);
    else:
        april_time_values = np.arange(0, 24*april_days, delta_t); 
        may_time_values = np.arange(0, 24*may_days, delta_t); 
        june_time_values = np.arange(0, 24*june_days, delta_t);


    #variable sine wave as outside temperature
    #temp swing is the halved value of the difference between high and low
    #centered on the high value minus the swing

    if(isFreeze==True):
        #april
        freeze_temp = (np.sin(2*math.pi/24*freeze_time_values) + 11); 
        april_temp = ((april_temp_high - april_temp_low)/2)*np.sin(2*math.pi/24*april_time_values) + \
         april_temp_high - ((april_temp_high - april_temp_low)/2);
        #may
        may_temp = ((may_temp_high - may_temp_low)/2)*np.sin(2*math.pi/24*may_time_values) + \
         may_temp_high - ((may_temp_high - may_temp_low)/2); 
        #june
        june_temp = ((june_temp_high - june_temp_low)/2)*np.sin(2*math.pi/24*june_time_values) + \
         june_temp_high - ((june_temp_high - june_temp_low)/2); 
    else:
        #april
        april_temp = ((april_temp_high - april_temp_low)/2)*np.sin(2*math.pi/24*april_time_values) + \
         april_temp_high - ((april_temp_high - april_temp_low)/2);
        #may
        may_temp = ((may_temp_high - may_temp_low)/2)*np.sin(2*math.pi/24*may_time_values) + \
         may_temp_high - ((may_temp_high - may_temp_low)/2); 
        #june
        june_temp = ((june_temp_high - june_temp_low)/2)*np.sin(2*math.pi/24*june_time_values) + \
         june_temp_high - ((june_temp_high - june_temp_low)/2); 

    #no of days to run simulation
    CONST_DAYS = april_days + may_days + june_days; 

    #cost per hour to run heat
    #calculated at ((1.06 per therm * 13.8 therm) / day) / 24 hours
    heating_cost_rate = .613 #dollar/hr
    #cost per hour to run air conditioner
    #calculated at 4,320 watts / 1,000 -> 4.32 KW/hr * avg KW/hr of 8.72 for VA
    ac_cost_rate = .376 #dollar/hr

    #0-no of days in 5 minute chunks
    time_values = np.arange(0, 24*CONST_DAYS, delta_t);

    #smash together all the different temps for the months
    if(isFreeze==True):
        outside_temp = np.concatenate([freeze_temp, april_temp, may_temp, june_temp]);  
    else:
        outside_temp = np.concatenate([april_temp, may_temp, june_temp]); 

    #heater thermostat settings for normal times
    normal_day_heat = np.concatenate([np.repeat(68, int(9 / delta_t)),
                              np.repeat(atHomeHeat, int(6 / delta_t)), 
                              np.repeat(70, int(9 / delta_t))]); 
    #heater thermostat settings for vacation times
    vacay_day_heat = np.concatenate([np.repeat(55, int(24 / delta_t))]); 
    #air conditioner thermostat settings for normal times
    normal_day_airc = np.concatenate([np.repeat(82, int(9 / delta_t)),
                              np.repeat(atHomeCool, int(6 / delta_t)), 
                              np.repeat(79, int(9 / delta_t))]); 
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
    	if i in vacay_time:
    		thermostat_heat[i-1] = vacay_thermo_heat[i-1]; 
    		thermostat_airc[i-1] = vacay_thermo_cool[i-1]; 
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
    plt.ylabel("Temp degF"); 
    plt.xlabel("Clock Tix in Simulation"); 
    plt.title("3-Month Simulation"); 
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

if __name__ == "__main__":
    try:
        arg1 = sys.argv[1];
    except IndexError:
        print("Usage: wphilli2_hvac.py <arg1>");
        print("Please specify (true or false) if there is a cold snap in the first argument");  
        sys.exit(1);

    try:
        arg2 = sys.argv[2];
    except IndexError:
        print("Usage: wphilli2_hvac.py <arg2>");
        print("Please specify (true or false) if person is wearing sweaters to stay warm");  
        sys.exit(1);

    try:
        arg3 = sys.argv[3];
    except IndexError:
        print("Usage: wphilli2_hvac.py <arg3>");
        print("Please specify (true or false) if person is drinking tea to stay cooler");  
        sys.exit(1);

    # start the program
p1(arg1, arg2, arg3); 