import numpy as np
import matplotlib as mpl
mpl.rcParams["svg.fonttype"] = "none"
mpl.rcParams["font.size"] = 36
mpl.rcParams["axes.unicode_minus"]=False
from matplotlib import pyplot as plt

class Plot:
    def __init__(self):
        self.ax = None
        self.name = "None"
        self.fig = None
        self.xminDefault = 0.0
        self.xmaxDefault = 0.0
        self.yminDefault = 0.0
        self.ymaxDefault = 0.0

class PlotHandler:
    def __init__(self):
        self.axes = []
        self.active = 0

    def set_xlim( self, left=None, right=None ):
        if ( self.active >= len(self.axes) ):
            return

        if ( not left is None ):
            self.axes[self.active].ax.set_xlim( left=left )

        if ( not right is None ):
            self.axes[self.active].ax.set_xlim( right=right )

    def set_ylim( self, bottom=None, top=None ):
        if (self.active >= len(self.axes) ):
            return

        if ( not bottom is None ):
            self.axes[self.active].ax.set_ylim( bottom=bottom )

        if ( not top is None ):
            self.axes[self.active].ax.set_ylim( top=top )

    def nameExists( self, newname ):
        for plot in self.axes:
            if ( newname == plot.name ):
                return True
        return False

    def attach( self, fig, ax, name ):
        newPlot = Plot()
        newPlot.ax = ax
        newPlot.fig = fig
        newPlot.xminDefault, newPlot.xmaxDefault = ax.get_xlim()
        newPlot.yminDefault, newPlot.ymaxDefault = ax.get_ylim()
        if ( self.nameExists(name) ):
            print ("Figure name already exists!")
            return

        newPlot.name = name
        newPlot.fig.canvas.set_window_title(name)
        self.axes.append(newPlot)
        self.active = len(self.axes)-1
        ax.locator_params(nbins=5)

    def getActive( self ):
        if ( self.active >= len(self.axes)):
            print ("Warning: No plots added!")
            return None
        return self.axes[self.active]

    def updateActive( self, newname ):
        for i in range(0, len(self.axes)):
            if ( self.axes[i].name == newname ):
                self.active = i
                return self.axes[i].ax
        self.active = 0
        print ("Warning: Did not find any plots with the name %s"%(newname))
        return self.axes[0].ax
