import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_random_polynomials(n, vars, num_polynomials):
    polynomials = []
    for _ in range(num_polynomials):
        coeffs = np.random.randint(-10, 11, size=(len(vars), n+1))
        polynomials.append(coeffs)
    return polynomials

def evaluate_polynomial(coeffs, x, y, z):
    result = 0
    for i, var_coeffs in enumerate(coeffs):
        for j, coeff in enumerate(var_coeffs):
            if i == 0:
                result += coeff * x**j
            elif i == 1:
                result += coeff * y**j
            elif i == 2:
                result += coeff * z**j
    return result

# Set parameters
vars = ['x', 'y', 'z']
n = 2  # degree of polynomials
num_polynomials = 10

# Generate random polynomials
polynomials = generate_random_polynomials(n, vars, num_polynomials)

# Create a 3D plot
fig = plt.figure(figsize=(15, 5))

# Generate a grid of points
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Plot each polynomial
for i, poly in enumerate(polynomials[:3]):  # Plot first 3 polynomials
    ax = fig.add_subplot(1, 3, i+1, projection='3d')
    Z = evaluate_polynomial(poly, X, Y, 0)  # Set z=0 for 3D surface plot
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Polynomial {i+1}')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

plt.tight_layout()
plt.show()
