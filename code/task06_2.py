# Import necessary libraries
import numpy as np
from scipy.optimize import minimize

def objective_function(x):
    return x[0]**2 + x[1]**2

def constraint_function(x):
    return x[0] - 2*x[1]

bounds = [(0, None), (None, None)]

result = minimize(
    objective_function,
    [1, 1],
    method='SLSQP',
    bounds=bounds,
    constraints={'type': 'eq', 'fun': constraint_function}
)

print(result)
