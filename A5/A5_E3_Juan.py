import pandas as pd
import numpy as np
from scipy import interpolate

# Load data
timeseries_df = pd.read_csv('A5/files/timeseries_la_haute_borne_2017.csv')
power_curve_df = pd.read_csv('A5/files/Senvion_MM82.csv')

# Constants
rho = 1.225  # density [kg/m^3]
D = 82  # rotor_diameter [m]
T = 8760  # total hours/years [h]
A = np.pi * (D / 2) ** 2 # swept area [m^2]
cut_in_ws = power_curve_df[power_curve_df['P'] > 0]['ws'].min()
cut_out_ws = power_curve_df[power_curve_df['P'] > 0]['ws'].max()

# Clear NaN Values & Calcualte WS
timeseries_df.dropna(subset=['U', 'V'], inplace=True) # Drop rows where specific columns have NaN values. 'Inplace=True' => modify the data frame directly and'Inplace=False' will return a new data frame.
timeseries_df['WS'] = np.sqrt(timeseries_df['U']**2 + timeseries_df['V']**2)

# Interpolate cp using the power curve
cp_i = interpolate.interp1d(power_curve_df['ws'], power_curve_df['cp'])

# Bin the wind speed data
delta_u = 0.5
bins = np.arange(cut_in_ws, cut_out_ws, delta_u)
timeseries_df['WS_bin'] = pd.cut(timeseries_df['WS'], bins, labels=(bins[:-1] + bins[1:]) / 2)

# Calculate the normalized frequency for each bin
timeseries_df['WS_bin'].value_counts(normalize=True, sort=False)

# Function to calculate APP based on binned timeseries
def calculate_APP_binned_timeseries(timeseries_df, cp_i):
    APP = 0
    for bin_center in timeseries_df['WS_bin'].cat.categories:
        P_i = timeseries_df[timeseries_df['WS_bin'] == bin_center].shape[0] / timeseries_df.shape[0]
        cp = cp_i(bin_center)
        APP += 0.5 * P_i * rho * cp * A * bin_center**3

    print(f"The APP based on the binned timeseries is: {APP/1000:.2f} kW")

    return APP

# Execution
APP_BT = calculate_APP_binned_timeseries(timeseries_df, cp_i)