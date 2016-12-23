import tkinter as tk
import plotHandler as ph
from matplotlib import pyplot as plt
import subprocess
import numpy as np

class MaxMinSlider:
    def __init__(self, master ):
        self.master = master
        self.minCallback = None
        self.maxCallback = None
        self.min = tk.Scale(self.master, from_=0.0, to_=100, length=600, width=50, orient="horizontal", command=self.updateMin, label="Min", resolution=-1, digits=4 )
        self.max = tk.Scale(self.master, from_=0.0, to_=100, length=600, width=50, orient="horizontal", command=self.updateMax, label="Max", resolution=-1, digits=4 )

    def updateMin( self, value ):
        value = float(value)
        delta = 1E-4*np.abs(value)
        self.max.configure(from_=value+delta)
        if ( not self.minCallback is None ):
            self.minCallback(float(value))

    def updateMax( self, value ):
        value = float(value)
        delta = 1E-4*np.abs(value)
        self.min.configure(to_=value-delta)
        if ( not self.maxCallback is None ):
            self.maxCallback(float(value))

    def disable( self ):
        self.min.config(state="disabled")
        self.max.config(state="disabled")

    def enable( self ):
        self.min.config(state="normal")
        self.max.config(state="normal")

    def pack(self):
        self.min.pack()
        self.max.pack()

    def pack_forget( self ):
        self.min.pack_forget()
        self.max.pack_forget()

class Control:
    def __init__( self, master ):
        self.master = master
        self.plots = ph.PlotHandler()

        # GUI entries
        self.master.wm_title("Plot Designer")
        self.activePlot = tk.StringVar( self.master )
        self.activePlot.set("None")
        self.availablePlots = ["None"]
        self.availablePlotsMenu = tk.OptionMenu( self.master, self.activePlot, *self.availablePlots, command=self.changePlot )

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

        # Button for saving all plots
        self.saveAllButton = tk.Button(self.master, text="Save all", command=self.saveall)

        # Button for closing all plots
        self.closeAllButton = tk.Button(self.master, text="Close all", command=self.closeall)

        # Pack all
        self.pack()

        # Controls disabled
        self.isDisabled = False

    def attach( self, fig, ax, name ):
        plt.show(block=False)
        self.plots.attach(fig, ax,name)
        self.availablePlots.append(name)
        self.activePlot.set(name)
        self.updateSliders(ax)
        self.availablePlotsMenu.destroy()
        self.availablePlotsMenu = tk.OptionMenu( self.master, self.activePlot, *self.availablePlots, command=self.changePlot )
        self.pack_forget()
        self.pack()

    def updateSliders( self, ax ):
        active = self.plots.getActive()
        if ( active is None ):
            return

        dx = 1E-3*(active.xmaxDefault-active.xminDefault)
        self.xlim.min.configure(from_=active.xminDefault, to_=active.xmaxDefault-dx)
        self.xlim.max.configure(from_=active.xminDefault+dx, to_=active.xmaxDefault)
        self.xlim.min.set(active.xminDefault)
        self.xlim.max.set(active.xmaxDefault)

        ymin, ymax = ax.get_ylim()
        dy = 1E-3*(active.ymaxDefault-active.yminDefault)
        self.ylim.min.configure(from_=active.yminDefault, to_=active.ymaxDefault-dy)
        self.ylim.max.configure(from_=active.yminDefault+dy, to_=active.ymaxDefault)
        self.ylim.min.set(active.yminDefault)
        self.ylim.max.set(active.ymaxDefault)

    def updateXmin( self, value ):
        self.plots.set_xlim( left=value )

    def updateXmax( self, value ):
        self.plots.set_xlim(right=value)

    def updateYmin( self, value ):
        self.plots.set_ylim( bottom=value )

    def updateYmax( self, value ):
        self.plots.set_ylim( top=value )

    def replot( self ):
        # Update all axes
        self.updateXmin( float(self.xlim.min.get()) )
        self.updateXmax( float(self.xlim.max.get()) )
        self.updateYmin( float(self.ylim.min.get()) )
        self.updateYmax( float(self.ylim.max.get()) )
        plt.show( block=False )

    def pack( self ):
        self.availablePlotsMenu.pack()
        self.xminLabel.pack()
        self.xlim.pack()
        self.ylabel.pack()
        self.ylim.pack()
        self.replotButton.pack(side="left")
        self.saveButton.pack(side="left")
        self.saveAllButton.pack(side="left")
        self.closeAllButton.pack(side="left")

    def pack_forget( self ):
        self.availablePlotsMenu.pack_forget()
        self.xminLabel.pack_forget()
        self.xlim.pack_forget()
        self.ylabel.pack_forget()
        self.ylim.pack_forget()
        self.replotButton.pack_forget()
        self.saveButton.pack_forget()
        self.saveAllButton.pack_forget()
        self.closeAllButton.pack_forget()

    def disableControls( self ):
        self.xlim.disable()
        self.ylim.disable()
        self.replotButton.config(state="disabled")
        self.saveButton.config(state="disabled")
        self.isDisabled = True

    def enableControls( self ):
        self.xlim.enable()
        self.ylim.enable()
        self.replotButton.config(state="normal")
        self.saveButton.config(state="normal")

    def changePlot( self, newentry ):
        if ( newentry == "None" ):
            self.disableControls()
            return

        if ( self.isDisabled ):
            self.enableControls()
            self.isDisabled = False

        activeAx = self.plots.updateActive( newentry )
        if ( not activeAx is None ):
            self.updateSliders( activeAx )

    def save( self ):
        obj = self.plots.getActive()
        if ( obj is None ):
            return

        obj.fig.savefig( obj.name )
        print ("Figure written to %s"%(obj.name), end="")

        # Export to ps_tex if filename is an svg
        if ( obj.name[-3:] == "svg" ):
            psname = obj.name[:-3]+"ps"
            subprocess.call(["inkscape", "--export-ps=%s"%(psname), "--export-latex", obj.name] )
            print (" ...and ps+ps_tex written to %s"%(psname), end="")
        print ("")

    def saveall( self ):
        for i in range(0, len(self.plots.axes)):
            self.plots.active = i
            self.save()
        self.changePlot( self.activePlot.get() )

    def closeall(self):
        plt.close("all")
        self.disableControls()
        self.saveAllButton.configure(state="disabled")
        self.closeAllButton.configure(state="disabled")
