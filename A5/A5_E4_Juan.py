import numpy as np
from scipy.stats import weibull_min
import scipy.integrate as integrate
from scipy import interpolate
import matplotlib.pyplot as plt

# Global Parameters
rho = 1.225  # air density [kg/m^3]
D = 82  # rotor diameter [m]
T = 8760  # total hours/years [h]
A = np.pi * (D/2)**2  # swept area [m^2]

def load_data():
    timeseries_data = np.genfromtxt('A5/files/timeseries_la_haute_borne_2017.csv', delimiter=',', skip_header=1)
    power_curve_data = np.genfromtxt('A5/files/Senvion_MM82.csv', delimiter=',', skip_header=1)
    return timeseries_data, power_curve_data

def process_data(timeseries_data, power_curve_data):
    timeseries_windspeed = np.sqrt(np.nan_to_num(timeseries_data[:, 1])**2 + np.nan_to_num(timeseries_data[:, 2])**2)
    cut_in_windspeed = power_curve_data[power_curve_data[:, 3] > 0, 0].min()
    cut_out_windspeed = power_curve_data[power_curve_data[:, 3] > 0, 0].max()
    cp_interpolated = interpolate.interp1d(power_curve_data[:, 0], power_curve_data[:, 3])
    return timeseries_windspeed, cut_in_windspeed, cut_out_windspeed, cp_interpolated

def fit_weibull(timeseries_windspeed):
    shape, _, scale = weibull_min.fit(timeseries_windspeed, floc=0) # floc=0 => location parameter defaults to 0
    return shape, scale

def weibull_pdf(ws, shape, scale):
    return weibull_min.pdf(ws, shape, loc=0, scale=scale)

def integrand(U, shape, scale, cp_interpolated):
    P = weibull_pdf(U, shape, scale)
    return 0.5 * P * rho * cp_interpolated(U) * A * (U**3)

def calculate_APP(integrand, cut_in_windspeed, cut_out_windspeed):
    APP, error = integrate.quad(integrand, cut_in_windspeed, cut_out_windspeed, limit=100, epsabs=1e-05, epsrel=1e-05)
    return APP, error

def plot(timeseries_windspeed, shape, scale):
    plt.hist(timeseries_windspeed, bins=50, density=True, alpha=0.6, color='b')
    xmin, xmax = timeseries_windspeed.min(), timeseries_windspeed.max()
    x = np.linspace(xmin, xmax, 100)
    p = weibull_min.pdf(x, shape, loc=0, scale=scale)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: shape = %.2f, scale = %.2f" % (shape, scale)
    plt.xlabel('Wind Speed')
    plt.ylabel('Probability Density')
    plt.title(title)
    plt.show()

timeseries_data, power_curve_data = load_data()
timeseries_windspeed, cut_in_windspeed, cut_out_windspeed, cp_interpolated = process_data(timeseries_data, power_curve_data)
shape, scale = fit_weibull(timeseries_windspeed)
integrand_func = lambda U: integrand(U, shape, scale, cp_interpolated) # lambda function to pass the parameters to the integrand
APP, error = calculate_APP(integrand_func, cut_in_windspeed, cut_out_windspeed)
print(f"APP: {APP/1000} kW")
print(f"Estimated error: {error/1000} kW")
plot(timeseries_windspeed, shape, scale)