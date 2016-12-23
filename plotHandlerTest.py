import numpy as np
from matplotlib import pyplot as plt
import plotHandler as ph
import time

def main():
    x = np.linspace(0, 10, 100 )
    y = x**2
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x,y,color="black")
    handler = ph.PlotHandler()
    handler.attach(ax)
    plt.show( block=False )
    time.sleep(5)
    handler.set_xlim( right=1 )
    plt.show()

if __name__ == "__main__":
    main()
