import numpy as np
from matplotlib import pyplot as plt
import controlGUI as cg
import tkinter as tk

def main():
    root = tk.Tk()
    control = cg.Control(root)
    x = np.linspace(0,10,101)
    y = x**2
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x,y)
    control.attach(fig, ax, "testPlot.svg")
    root.mainloop()
    plt.show()

if __name__ == "__main__":
    main()
