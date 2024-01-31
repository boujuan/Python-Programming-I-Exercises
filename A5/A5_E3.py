import csv
import numpy as np
from scipy import interpolate

# Load data function 
def load_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f) #read line by line (comma-seperated-values)
        next(reader)
        data = [row for row in reader] #list of lists for data (row-wise)
    return data

def interpolate_nan_values(data):
    mask = np.isnan(data) # boolean mask for nan values
    indices = np.where(~mask)[0] # indices of non-nan values
    if indices.size > 0:
        f = interpolate.interp1d(indices, data[indices]) # interpolation function
        data[mask] = f(np.where(mask)[0]) # replace nan values by interpolated values
    return data

# Parameters
rho = 1.225  # kg/m^3
D = 82  # m
T = 8760  # h
A = np.pi * (D / 2) ** 2 # m^2

#load data
timeseries_data = np.genfromtxt('timeseries_la_haute_borne_2017.csv', delimiter=',', skip_header=1) #list [[time, u, v],[time, u, v],....,[time, u, v]]
power_curve_data = np.genfromtxt('Senvion_MM82.csv', delimiter=',', skip_header=1) #list:[[ws, P,c_t, c_p],[ws, P,c_t, c_p],....,[ws, P,c_t, c_p]]

cut_in_ws = min(float(row[0]) for row in power_curve_data if float(row[3]) > 0) #find cut_in_ws
cut_out_ws = max(float(row[0]) for row in power_curve_data if float(row[3]) > 0)

u_component = interpolate_nan_values(timeseries_data[:, 1])
v_component = interpolate_nan_values(timeseries_data[:, 2])
# Calculate module wind speed
timeseries_data = np.c_[timeseries_data, np.sqrt(u_component**2 + v_component**2)]

# Cp interpolation function with the power curve
cp_i = interpolate.interp1d([float(row[0]) for row in power_curve_data], [float(row[3]) for row in power_curve_data])

# Bin the wind speed data
delta_u = 0.5 # m/s bin width
bins = np.arange(cut_in_ws, cut_out_ws, delta_u) 
timeseries_data = np.c_[timeseries_data, np.digitize(timeseries_data[:, 3], bins)]
#*row is used to unpack the elements of the row
#l:[[time, u, v, WS, bin_index],[time, u, v, WS, bin_index]...]
#bin_index= 0 for ws: 4.0 - 4.5 / bin_index= 1 for 4.5 - 5.0 ...

# Calculate the normalized frequency for each bin:
bin_counts = {} #dict with counts for every ws btw cut_in and cut_out in 0.5 steps 
for row in timeseries_data:
    bin_counts[row[4]] = bin_counts.get(row[4], 0) + 1 #key = value, +1 to jump to the next index: {0: 13515, 1: 3617...,}
total_count = len(timeseries_data)

normalized_frequencies = {}  # Create an empty dictionary to store the results
for bin, count in bin_counts.items():
    weighted_value = bin * delta_u + cut_in_ws #representative value for the bin: example: bin 0 = ws 4.0 
    normalized_frequency = count / total_count #normalized frequency for the bin
    normalized_frequencies[weighted_value] = normalized_frequency #result to dict: how often we have for ex.: 4.0 m/s in freq.: 4.0: 0.23073

# Function to calculate APP based on binned timeseries
def calculate_APP_binned_timeseries(normalized_frequencies, cp_i):
    APP = 0
    APP = sum(0.5 * P_i * rho * cp_i(bin_center) * A * bin_center**3 for bin_center, P_i in normalized_frequencies.items())

    print(f"The APP based on the binned timeseries is: {APP/1000:.2f} kW")

    return APP
#bin_center = ws_bin and P_i = normalized freq. iterate over the key-value pairs in the normalized_frequencies dictionary 
APP_BT = calculate_APP_binned_timeseries(normalized_frequencies, cp_i)