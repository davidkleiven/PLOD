import tkinter as tk
import plotHandler as ph
from matplotlib import pyplot as plt
import subprocess

class MaxMinSlider:
    def __init__(self, master ):
        self.master = master
        self.minCallback = None
        self.maxCallback = None
        self.min = tk.Scale(self.master, from_=0.0, to_=100, length=600, width=50, orient="horizontal", command=self.updateMin, label="Min", resolution=-1, digits=4 )
        self.max = tk.Scale(self.master, from_=0.0, to_=100, length=600, width=50, orient="horizontal", command=self.updateMax, label="Max", resolution=-1, digits=4 )
        self.resolution = 100.0

    def updateMin( self, value ):
        self.max.configure(from_=value)
        if ( not self.minCallback is None ):
            self.minCallback(float(value))

    def updateMax( self, value ):
        self.min.configure(to_=value)
        if ( not self.maxCallback is None ):
            self.maxCallback(float(value))

    def pack(self):
        self.min.pack()
        self.max.pack()

class Control:
    def __init__( self, master ):
        self.master = master
        self.plots = ph.PlotHandler()

        # GUI entries
        self.title = tk.Label(self.master, text="PLOD")
        self.activePlot = tk.StringVar( self.master )
        self.activePlot.set("Default")
        self.availablePlots = []
        self.availablePlotsMenu = tk.OptionMenu( self.master, self.activePlot, "Default", command=self.changePlot )

        # Create scale for the x-axis
        self.xminLabel = tk.Label( self.master, text="Adjust x-axis")
        self.xlim = MaxMinSlider( master )
        self.xlim.minCallback = self.updateXmin
        self.xlim.maxCallback = self.updateXmax

        # Create scale for y-axis
        self.ylabel = tk.Label(self.master, text="Adjust y-axis")
        self.ylim = MaxMinSlider( master )
        self.ylim.minCallback = self.updateYmin
        self.ylim.maxCallback = self.updateYmax

        # Button for replotting
        self.replotButton = tk.Button(self.master, text="Replot", command=self.replot)

        # Button for saving
        self.saveButton = tk.Button(self.master, text="Save", command=self.save)


        # Pack all
        self.pack()

    def attach( self, fig, ax, name ):
        plt.show(block=False)
        self.plots.attach(fig, ax,name)
        self.availablePlots.append(name)
        self.activePlot.set(name)
        self.availablePlotsMenu = tk.OptionMenu( self.master, self.activePlot, self.availablePlots )
        self.updateSliders(ax)
        self.availablePlotsMenu = tk.OptionMenu( self.master, self.activePlot, self.availablePlots, command=self.changePlot )

    def updateSliders( self, ax ):
        xmin, xmax = ax.get_xlim()
        self.xlim.min.configure(from_=xmin, to_=xmax)
        self.xlim.max.configure(from_=xmin, to_=xmax)

        ymin, ymax = ax.get_ylim()
        self.ylim.min.configure(from_=ymin, to_=ymax)
        self.ylim.max.configure(from_=ymin, to_=ymax)

    def updateXmin( self, value ):
        self.plots.set_xlim( left=value )

    def updateXmax( self, value ):
        self.plots.set_xlim(right=value)

    def updateYmin( self, value ):
        self.plots.set_ylim( bottom=value )

    def updateYmax( self, value ):
        self.plots.set_ylim( top=value )

    def replot( self ):
        plt.show( block=False )

    def pack( self ):
        self.title.pack()
        self.availablePlotsMenu.pack()
        self.xminLabel.pack()
        self.xlim.pack()
        self.ylabel.pack()
        self.ylim.pack()
        self.replotButton.pack()
        self.saveButton.pack()

    def changePlot( self, newentry ):
        activeAx = self.plots.updateActive( newentry )
        if ( not activeAx is None ):
            self.updateSliders( activeAx )

    def save( self ):
        obj = self.plots.getActive()
        obj.fig.savefig( obj.name )
        print ("Figure written to %s"%(obj.name), end="")

        # Export to ps_tex if filename is an svg
        if ( obj.name[-3:] == "svg" ):
            psname = obj.name[:-3]+".ps"
            print (psname)
            #subprocess.call(["inkscape", "--export-ps="%(psname), "--export-latex", obj.name] )
            print (" ...and ps+ps_tex written to %s"%(psname), end="")
        print ("")
