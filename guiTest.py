import sys
sys.path.append('./')
import numpy as np
from matplotlib import pyplot as plt
from PLOD import controlGUI as cg
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

def main():
    root = tk.Tk()
    control = cg.Control(root)
    x = np.linspace(0,10,101)
    y = x**2
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x,y, color="black")
    ax.set_xlabel("\$x\$")
    ax.set_ylabel("\$x^2\$")
    control.attach(fig, ax, "testPlot.svg")

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1,1,1)
    ax2.plot( x, np.sin(x), color="black" )
    ax2.set_xlabel( "\$x\$" )
    ax2.set_ylabel( "\$\sin x\$" )
    control.attach( fig2, ax2, "sinx.svg" )
    root.mainloop()
    plt.show()

if __name__ == "__main__":
    main()
