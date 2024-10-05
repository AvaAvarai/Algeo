import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def plot_polynomials(vars, n):
    # Generate random polynomials
    polynomials = generate_random_polynomials(n, vars, 3)

    # Create a 3D plot
    fig = plt.figure(figsize=(15, 5))

    # Generate a grid of points
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)

    # Plot each polynomial
    for i, poly in enumerate(polynomials):
        ax = fig.add_subplot(1, 3, i+1, projection='3d')
        Z = evaluate_polynomial(poly, X, Y, 0)  # Set z=0 for 3D surface plot
        surf = ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Polynomial {i+1}')
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

    plt.tight_layout()
    return fig

class PolynomialPlotter:
    def __init__(self, master):
        self.master = master
        self.master.title("Polynomial Plotter")

        # Create UI widgets
        self.var_frame = ttk.Frame(master)
        self.var_frame.grid(row=0, column=0, padx=5, pady=5)

        self.var_x = tk.BooleanVar()
        self.var_y = tk.BooleanVar()
        self.var_z = tk.BooleanVar()

        ttk.Checkbutton(self.var_frame, text="x", variable=self.var_x).pack(side=tk.LEFT)
        ttk.Checkbutton(self.var_frame, text="y", variable=self.var_y).pack(side=tk.LEFT)
        ttk.Checkbutton(self.var_frame, text="z", variable=self.var_z).pack(side=tk.LEFT)

        self.degree_frame = ttk.Frame(master)
        self.degree_frame.grid(row=1, column=0, padx=5, pady=5)

        ttk.Label(self.degree_frame, text="Degree:").pack(side=tk.LEFT)
        self.degree_selection = ttk.Scale(self.degree_frame, from_=1, to=25, orient=tk.HORIZONTAL, command=self.update_degree_label)
        self.degree_selection.set(2)
        self.degree_selection.pack(side=tk.LEFT)

        self.degree_label = ttk.Label(self.degree_frame, text="2")
        self.degree_label.pack(side=tk.LEFT, padx=(5, 0))

        self.plot_button = ttk.Button(master, text="Plot Polynomials", command=self.on_button_clicked)
        self.plot_button.grid(row=2, column=0, padx=5, pady=5)

        self.continuous_button = ttk.Button(master, text="Toggle Continuous Generation", command=self.toggle_continuous_generation)
        self.continuous_button.grid(row=2, column=1, padx=5, pady=5)

        self.canvas = None
        self.figure = None
        self.continuous_generation = False
        self.after_id = None

        # Set up the close on exit behavior
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_degree_label(self, value):
        self.degree_label.config(text=str(int(float(value))))

    def on_button_clicked(self):
        self.plot_polynomials()

    def plot_polynomials(self):
        vars = []
        if self.var_x.get():
            vars.append('x')
        if self.var_y.get():
            vars.append('y')
        if self.var_z.get():
            vars.append('z')
        
        if not vars:
            messagebox.showwarning("Warning", "Please select at least one variable.")
            return

        n = int(self.degree_selection.get())
        
        # Close previous figure if it exists
        if self.figure:
            plt.close(self.figure)
        
        self.figure = plot_polynomials(vars, n)
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def toggle_continuous_generation(self):
        self.continuous_generation = not self.continuous_generation
        if self.continuous_generation:
            self.continuous_button.config(text="Stop Continuous Generation")
            self.continuous_plot()
        else:
            self.continuous_button.config(text="Start Continuous Generation")
            if self.after_id:
                self.master.after_cancel(self.after_id)

    def continuous_plot(self):
        if self.continuous_generation:
            self.plot_polynomials()
            self.after_id = self.master.after(3000, self.continuous_plot)

    def on_closing(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
        plt.close('all')  # Close all matplotlib figures
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PolynomialPlotter(root)
    root.mainloop()
