import numpy as np
from scipy.stats import weibull_min as weibull
from scipy.integrate import quad as integrate
from scipy.interpolate import interp1d as interpolate
from matplotlib import pyplot as plt

class APP_Processor:
    T = 8760  # total hours/years [h]

    def __init__(self, timeseries_file, power_curve_file, rho=1.225, D=82):
        self.rho = rho  # air density [kg/m^3]
        self.D = D  # rotor diameter [m]
        self.A = np.pi * (self.D/2)**2  # swept area [m^2]
        self.timeseries_data = np.genfromtxt(timeseries_file, delimiter=',', skip_header=1)
        self.power_curve_data = np.genfromtxt(power_curve_file, delimiter=',', skip_header=1)
        self._timeseries_windspeed = None
        self._cut_in_windspeed = None
        self._cut_out_windspeed = None
        self._cp_interpolated = None
        self._shape = None
        self._scale = None

    # INTERPOLATE NAN VALUES IN TIMESERIES DATA
    def interpolate_nan_values(self, data):
        mask = np.isnan(data) # boolean mask for nan values
        indices = np.where(~mask)[0] # indices of non-nan values
        if indices.size > 0:
            f = interpolate(indices, data[indices]) # interpolation function
            data[mask] = f(np.where(mask)[0]) # replace nan values by interpolated values
        return data

    def calculate_windspeed(self, u_component, v_component):
        return np.sqrt(u_component**2 + v_component**2)

    def timeseries_windspeed(self):
        if self._timeseries_windspeed is None:
            u_component = self.interpolate_nan_values(self.timeseries_data[:, 1])
            v_component = self.interpolate_nan_values(self.timeseries_data[:, 2])
            self._timeseries_windspeed = self.calculate_windspeed(u_component, v_component)
        return self._timeseries_windspeed

    def cut_in_windspeed(self):
        if self._cut_in_windspeed is None:
            self._cut_in_windspeed = self.power_curve_data[self.power_curve_data[:, 3] > 0, 0].min()
        return self._cut_in_windspeed

    def cut_out_windspeed(self):
        if self._cut_out_windspeed is None:
            self._cut_out_windspeed = self.power_curve_data[self.power_curve_data[:, 3] > 0, 0].max()
        return self._cut_out_windspeed

    def cp_interpolated(self):
        if self._cp_interpolated is None:
            self._cp_interpolated = interpolate(self.power_curve_data[:, 0], self.power_curve_data[:, 3])
        return self._cp_interpolated

    def calculate_weibull_fit(self):
        if self._shape is None or self._scale is None:
            self._shape, _, self._scale = weibull.fit(self.timeseries_windspeed(), floc=0) # floc=0 => location parameter defaults to 0
        return self._shape, self._scale

    def weibull_pdf(self, ws):
        shape, scale = self.calculate_weibull_fit()
        return weibull.pdf(ws, shape, loc=0, scale=scale)

    def integrand(self, U):
        P = self.weibull_pdf(U)
        return 0.5 * P * self.rho * self.cp_interpolated()(U) * self.A * (U**3)

    def calculate_APP(self):
        APP, error = integrate(self.integrand, self.cut_in_windspeed(), self.cut_out_windspeed(), limit=100, epsabs=1e-05, epsrel=1e-05)
        return APP, error

    def plot(self):
        plt.hist(self.timeseries_windspeed(), bins=50, density=True, alpha=0.6, color='b')
        xmin, xmax = self.timeseries_windspeed().min(), self.timeseries_windspeed().max()
        x = np.linspace(xmin, xmax, 100)
        p = weibull.pdf(x, self._shape, loc=0, scale=self._scale)
        plt.plot(x, p, 'k', linewidth=2)
        plt.xlabel('Wind Speed')
        plt.ylabel('Probability Density')
        plt.show()

rho = 1.225  # air density [kg/m^3]
D = 82  # rotor diameter [m]
E4_Data = APP_Processor('A5/files/timeseries_la_haute_borne_2017.csv', 'A5/files/Senvion_MM82.csv', rho, D)
APP, error = E4_Data.calculate_APP()
print(f"APP: {APP/1000} kW")
print(f"Estimated error: {error/1000} kW")
E4_Data.plot()