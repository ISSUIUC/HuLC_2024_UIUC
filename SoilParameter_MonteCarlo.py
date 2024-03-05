import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
# Define your function here
def my_function(D, sigma, c, alpha, tau_coh, A_coh):
    # Example function, replace with your actual function
    #starship @ 10m
    term1 = (-0.794148045844479*A_coh)*np.sqrt((sigma*D**2)/(1+13.5438993961456*np.sqrt(2))+1.29520013646852 * 10**-7)/(c*sigma*D**3)
    term2 = (-0.000285805059267867 * A_coh)/(sigma*c*D**3)
    term3 = -7.79059232973434*D*np.sqrt((sigma*D**2)/(1+13.5438993961456*np.sqrt(2))+1.29520013646852 * 10**-7)*np.tan(alpha)
    term4 = -0.000285805059267867*D*np.tan(alpha)
    term5 = -(0.794148045844479*tau_coh)*np.sqrt((sigma*D**2)/(1+13.5438993961456*np.sqrt(2))+1.29520013646852 * 10**-7)/(c*sigma)
    term6 = -0.000285805059267867 * tau_coh / (sigma*c)
    term7 = (575.0678278807931)*np.sqrt((sigma*D**2)/(1+13.5438993961456*np.sqrt(2))+1.29520013646852 * 10**-7)/(c*sigma)
    term8 = 0.206960522625117/(c*sigma)
    dy_dt = (term1+term2+term3+term4+term5+term6+term7+term8)*1000
    return dy_dt
# Define the parameter ranges (min, max) for each parameter
param_ranges = {
    #https://www.lpi.usra.edu/publications/books/lunar_sourcebook/pdf/Chapter09.pdf
    'D': (3e-6, 300e-6),
    'sigma': (1.07e3, 1.92e3),
    'c': (0.415, 0.6598),
    'alpha': (41*np.pi/180, 43*np.pi/180), #pdf above page 36
    'A_coh': (6.779089741E-17, 6.779089741E-17),
    #I wish I fucking knew why tau_coh is 0 if A_coh is nonzero but Robert said so, oh well
    'tau_coh': (0, 0),
}
# Number of simulations
n_simulations = 10000
# Store simulation results
results = []
# Run Monte Carlo simulations
for _ in range(n_simulations):
    params = {param: np.random.uniform(low, high) for param, (low, high) in param_ranges.items()}
    result = my_function(**params)
    results.append(result)
# Analyze the results
mean_result = np.mean(results)
std_dev_result = np.std(results)
print(f"Mean of the simulation results: {mean_result}")
print(f"Standard deviation of the simulation results: {std_dev_result}")
# Plot histogram
hist, bin_edges, _ = plt.hist(results, bins=50, alpha=0.75, label='Simulation Results', edgecolor='black', color='c')
xmin, xmax = plt.xlim()
# Uncomment for Gaussian Fit
# x = np.linspace(xmin, xmax, 100)
# p = norm.pdf(x, mean_result, std_dev_result)
# ymax = max(hist)
# plt.plot(x, p*ymax/max(p), 'k', linewidth=2, label='Gaussian Fit')
################################################################
plt.title('Monte Carlo Simulation Results')
plt.xlabel('Crater Depth Erosion Rate (mm/s)')
plt.ylabel('Frequency')
plt.xlim(0,4)
plt.legend()
plt.grid(linewidth=0.1, color='k')
plt.show()