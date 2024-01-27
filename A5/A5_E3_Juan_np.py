import csv
import numpy as np
from scipy import interpolate

# Load data
def load_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        data = [row for row in reader]
    return data

# Function to calculate APP based on binned timeseries
def calculate_APP_binned_timeseries(normalized_frequencies, cp_i):
    APP = 0
    APP = sum(0.5 * P_i * rho * cp_i(bin_center) * A * bin_center**3 for bin_center, P_i in normalized_frequencies.items())

    print(f"The APP based on the binned timeseries is: {APP/1000:.2f} kW")

    return APP

timeseries_data = load_csv('A5/files/timeseries_la_haute_borne_2017.csv')
power_curve_data = load_csv('A5/files/Senvion_MM82.csv')

# Parameters
rho = 1.225  # kg/m^3
D = 82  # m
T = 8760  # h
A = np.pi * (D/2)** 2 # m^2
cut_in_ws = min(float(row[0]) for row in power_curve_data if float(row[3]) > 0)
cut_out_ws = max(float(row[0]) for row in power_curve_data if float(row[3]) > 0)

# Fix empty values
timeseries_data = [row for row in timeseries_data if row[1] != 'NaN' and row[2] != 'NaN']
# Calculate module wind speed
timeseries_data = [row + [np.sqrt(float(row[1])**2 + float(row[2])**2)] for row in timeseries_data]

# Cp interpolation with the power curve
cp_i = interpolate.interp1d([float(row[0]) for row in power_curve_data], [float(row[3]) for row in power_curve_data])

# Bin the wind speed data
delta_u = 0.5 # m/s bin width
bins = np.arange(cut_in_ws, cut_out_ws, delta_u)
timeseries_data = [[*row, np.digitize(row[3], bins)] for row in timeseries_data]

# Calculate the normalized frequency for each bin
bin_counts = {}
for row in timeseries_data:
    bin_counts[row[4]] = bin_counts.get(row[4], 0) + 1
total_count = len(timeseries_data)
normalized_frequencies = {bin * delta_u + cut_in_ws: count / total_count for bin, count in bin_counts.items()}

APP_BT = calculate_APP_binned_timeseries(normalized_frequencies, cp_i)