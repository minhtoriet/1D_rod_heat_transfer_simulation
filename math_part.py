import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy import sympify, symbols, lambdify
import tkinter as tk
from tkinter import ttk, messagebox

# Dictionary of thermal diffusivities (alpha) for common metals (m²/s)
metals = {
    'copper': 1.17e-4,
    'aluminum': 9.7e-5,
    'iron': 2.3e-5,
    'steel': 1.4e-5,
    'gold': 1.27e-4,
    'silver': 1.65e-4
}

def start_simulation():
    try:
        L = float(entry_length.get())
        if L <= 0:
            raise ValueError("Length must be positive.")
        
        metal = combo_metal.get().lower()
        alpha = metals.get(metal, None)
        if alpha is None:
            raise ValueError("Invalid metal selected.")
        
        init_expr = entry_expr.get()
        x_sym = symbols('x')
        expr = sympify(init_expr)
        f = lambdify(x_sym, expr, modules='numpy')
        
        # Close the input window
        root.destroy()
        
        # Proceed with simulation
        run_simulation(L, alpha, f)
        
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid expression or input: {e}. Example: sin(pi * x / L)")

def run_simulation(L, alpha, f):
    # Simulation parameters
    nx = 101  # Number of spatial points
    dx = L / (nx - 1)
    x = np.linspace(0, L, nx)
    
    # Initial condition
    u = f(x)
    
    # Time step
    sigma = 0.5
    dt = sigma * dx**2 / alpha
    r = alpha * dt / dx**2
    
    # Build implicit matrix
    M_imp = np.zeros((nx, nx))
    for i in range(1, nx-1):
        M_imp[i, i-1] = -r / 2
        M_imp[i, i] = 1 + r
        M_imp[i, i+1] = -r / 2
    # Neumann BC adjustments
    M_imp[0, 0] = 1 + r
    M_imp[0, 1] = -r
    M_imp[nx-1, nx-1] = 1 + r
    M_imp[nx-1, nx-2] = -r
    
    # Build explicit matrix
    M_exp = np.zeros((nx, nx))
    for i in range(1, nx-1):
        M_exp[i, i-1] = r / 2
        M_exp[i, i] = 1 - r
        M_exp[i, i+1] = r / 2
    # Neumann BC adjustments
    M_exp[0, 0] = 1 - r
    M_exp[0, 1] = r
    M_exp[nx-1, nx-1] = 1 - r
    M_exp[nx-1, nx-2] = r
    
    # Set up plot for animation
    fig, ax = plt.subplots()
    ax.set_xlim(0, L)
    ax.set_ylim(np.min(u) - 1, np.max(u) + 1)
    ax.set_xlabel('Position (x)')
    ax.set_ylabel('Temperature (u)')
    ax.set_title('Heat Distribution Over Time')
    line, = ax.plot(x, u)
    
    # Animation parameters
    steps_per_frame = 10
    num_frames = 200
    
    def update(frame):
        nonlocal u
        for _ in range(steps_per_frame):
            u = np.linalg.solve(M_imp, M_exp @ u)
        line.set_ydata(u)
        return line,
    
    ani = FuncAnimation(fig, update, frames=num_frames, interval=50, blit=True)
    plt.show()

# Create GUI window
root = tk.Tk()
root.title("Heat Transfer Simulator")
root.geometry("400x250")

# Labels and entries
tk.Label(root, text="Rod Length (meters):").pack(pady=5)
entry_length = tk.Entry(root)
entry_length.pack()
entry_length.insert(0, "1.0")  # Default value

tk.Label(root, text="Metal Type:").pack(pady=5)
combo_metal = ttk.Combobox(root, values=list(metals.keys()), state="readonly")
combo_metal.pack()
combo_metal.set("copper")  # Default

tk.Label(root, text="Initial Temperature Expression (f(x)):").pack(pady=5)
entry_expr = tk.Entry(root)
entry_expr.pack()
entry_expr.insert(0, "sin(pi * x / L)")  # Default example

# Start button
tk.Button(root, text="Start Simulation", command=start_simulation).pack(pady=20)

root.mainloop()