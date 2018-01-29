# Aliens vs. Vampires v1: Polynomial vs. Exponential Growth
# Author: Stephen Davies, PhD

import numpy as np
import matplotlib.pyplot as plt

delta_t = .1                                    # years
time_values = np.arange(1940, 2110, delta_t)    # years

abduction_factor = 300   # (abductees/year)/year
bite_rate = .1           # (vampires/year)/vampire

# Create (empty) arrays for the stocks.
A = np.zeros(len(time_values))
V = np.zeros(len(time_values))

# Initial conditions: start off with no abductees, and one lonely vampire.
A[0] = 0
V[0] = 1


for i in range(1,len(time_values)):

    # Computing single values for A' and V' each time through the loop, since
    # we don't plan on examining an entire vector of them later.
    A_prime = abduction_factor * i * delta_t
    V_prime = bite_rate * V[i-1]

    # Increase each stock by the appropriate amount for this time step.
    A[i] = A[i-1] + A_prime * delta_t
    V[i] = V[i-1] + V_prime * delta_t


plt.clf()
plt.plot(time_values,A, color="green", label="alien abductees")
plt.plot(time_values,V, color="red", label="vampires")
plt.xlabel("year")
plt.legend()
plt.show()