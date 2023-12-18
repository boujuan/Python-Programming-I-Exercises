import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('A4/results_farm.csv.gz', delimiter=',', skip_header=1)

states = np.unique(data[:, 0])
turbines = np.unique(data[:, 1])
mean_AMB_P = np.array([np.mean(data[data[:, 0] == state, 6]) for state in states])
mean_P = np.array([np.mean(data[data[:, 0] == state, 7]) for state in states])

plt.figure()
plt.plot(states, mean_AMB_P, label='Mean AMB_P')
plt.plot(states, mean_P, label='Mean P')
plt.xlabel('State')
plt.ylabel('Power')
plt.title('Mean Power vs State')
plt.legend()
plt.show()

# EFF = data[:, 12]
data[:, 12] = np.where(data[:, 12] <= 0, np.nan, data[:, 12])

# Reshape the data to 2D
EFF = data[:, 12].reshape(len(states), len(turbines))
WS = data[:, 3].reshape(len(states), len(turbines))
P = data[:, 7].reshape(len(states), len(turbines))

# 2D plot of EFF vs turbine and state
plt.figure()
plt.pcolormesh(turbines, states, EFF)
plt.xlabel('Turbine')
plt.ylabel('State')
plt.title('EFF vs Turbine and State')
plt.colorbar(label='EFF')
plt.show()

# 2D plot of wind speed vs turbine and state
plt.figure()
plt.pcolormesh(turbines, states, WS, cmap='viridis')
plt.xlabel('Turbine')
plt.ylabel('State')
plt.title('WS vs Turbine and State')
plt.colorbar(label='WS')
plt.show()

# 2D plot of power vs turbine and state
plt.figure()
plt.pcolormesh(turbines, states, P, cmap='inferno')
plt.xlabel('Turbine')
plt.ylabel('State')
plt.title('P vs Turbine and State')
plt.colorbar(label='P')
plt.show()