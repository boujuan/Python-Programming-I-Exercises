import time

def wind_speed(u_0, ct, D, sigma):
    # Calculate wind speed at a certain distance behind a turbine based on the wake model equation
    a = 1 - (ct * D ** 2) / (8 * sigma ** 2)
    return u_0 * a ** 0.5

def sigma(k, x, beta, D):
    # Calculate sigma value based on the wake model equation
    return k * x + 0.25 * beta ** 0.5 * D

# Turbine parameters
uniform_wind_speed = 9  # m/s
D = 154  # m
ct = 0.763
k = 0.02
beta = 0.5 * (1 + (1 - ct) ** 0.5) / ((1 - ct) ** 0.5)

# Threshold parameters
threshold = 8.95 # m/s
increment = 1  # m

def method_for(k, beta, D, ct, threshold, increment):
    start_time = time.time()
    for x in range(0, int(1e5), increment):
        sigma_value = sigma(k, x, beta, D)
        u = wind_speed(uniform_wind_speed, ct, D, sigma_value)
        
        if u >= threshold:
            break
    end_time = time.time()
    return end_time - start_time
        
def method_while(k, beta, D, ct, threshold, increment):
    start_time = time.time()
    x = 0
    while x < 100000:        
        if wind_speed(uniform_wind_speed, ct, D, sigma(k, x, beta, D)) >= threshold:
            break
        x += increment
    end_time = time.time()
    return end_time - start_time

def method_generator(k, beta, D, ct, threshold, increment):
    start_time = time.time()
    x = next((x for x in range(0, 100000, increment) if wind_speed(uniform_wind_speed, ct, D, sigma(k, x, beta, D)) >= threshold), None)    
    end_time = time.time()
    return end_time - start_time

def method_map(k, beta, D, ct, threshold, increment):
    start_time = time.time()
    x_values = range(0, 100000, increment)
    u_values = list(map(lambda x: wind_speed(uniform_wind_speed, ct, D, sigma(k, x, beta, D)), x_values))
    x = next((x for x, u in zip(x_values, u_values) if u >= threshold), None)
    end_time = time.time()
    return end_time - start_time

def method_for_optim(k, beta, D, ct, threshold, increment):
    start_time = time.time()
    for x in range(0, 100000, increment):
        if wind_speed(uniform_wind_speed, ct, D, sigma(k, x, beta, D)) >= threshold:
            break
    end_time = time.time()
    return end_time - start_time

number_times = 100
method_1_times = [method_for_optim(k, beta, D, ct, threshold, increment)  for i in range(number_times)]
method_2_times = [method_while(k, beta, D, ct, threshold, increment)  for i in range(number_times)]
method_3_times = [method_generator(k, beta, D, ct, threshold, increment)  for i in range(number_times)]

print('Method 1: ', sum(method_1_times)/len(method_1_times))
print('Method 2: ', sum(method_2_times)/len(method_2_times))
print('Method 3: ', sum(method_3_times)/len(method_3_times))

print('Best method is the: ', ['first', 'second', 'third'][[sum(method_1_times)/len(method_1_times), sum(method_2_times)/len(method_2_times), sum(method_3_times)/len(method_3_times)].index(min([sum(method_1_times)/len(method_1_times), sum(method_2_times)/len(method_2_times), sum(method_3_times)/len(method_3_times)]))])