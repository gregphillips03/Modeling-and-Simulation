# Simple Python program for basic numerical differential equations.
# Author: Stephen Davies, PhD

import numpy as np
import matplotlib.pyplot as plt


delta_t = .5   # hours

# 1. Integrate speed to get distance.
#
# Let's start with a vector showing our speed every delta_t hours. We'll just
# make it (uniformly) random for now: 50 points between 0 and 100.
speed = np.random.uniform(0,100,50)    # miles/hour

# Our distance vector will be one larger than our speed vector. Start it off
# with all zeros for no particular reason.
distance = np.zeros(1+len(speed))      # miles


# Initial condition: we'll assume the distance traveled at time 0 is "zero."
distance[0] = 0

# The total distance traveled at each point in time is the distance traveled
# the previous point plus the new distance during the current time interval.
# And that new distance, of course, is just the speed times the duration of
# the interval.
for i in range(1,len(distance)):
    distance[i] = distance[i-1] + speed[i-1] * delta_t

# Plot speed and distance on the same axis (inflate speed by 10 so it's more
# easily visible.)
plt.figure(1)
plt.plot(speed*10,color="red")
plt.plot(distance,color="blue")
plt.show()


# 2. Now go the other way: reset our speed vector to all zeros, and recover it
# by differentiating the distance vector to get the speed.
#
# Wipe out our old speed vector.
speed = np.zeros(len(speed))

# The speed at each point in time is the amount of distance traveled in that
# time interval divided by the length of that time interval.
for i in range(0, len(speed)):
    speed[i] = (distance[i+1] - distance[i]) / delta_t


# Let's plot both vectors again in a separate window so we can compare and
# verify that they're the same: the processes of integration and
# differentiation are inverses.
plt.figure(2)
plt.plot(speed*10,color="green")
plt.plot(distance,color="purple")
plt.show()