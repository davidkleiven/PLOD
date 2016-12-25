import tkinter as tk
import plotHandler as ph
from matplotlib import pyplot as plt
import subprocess
import numpy as np

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

        # Control x-min
        self.xminLab = tk.Label( self.master, text="xmin:")
        self.xmin = tk.Entry( self.master, width=10 )
        self.xmaxLab = tk.Label( self.master, text="xmax:")
        self.xmax = tk.Entry( self.master, width=10)
        self.yminLab = tk.Label( self.master, text="ymin:")
        self.ymin = tk.Entry( self.master, width=10 )
        self.ymaxLab = tk.Label( self.master, text="ymax:")
        self.ymax = tk.Entry( self.master, width=10 )

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
        self.updateEntries(ax)
        self.availablePlotsMenu.destroy()
        self.availablePlotsMenu = tk.OptionMenu( self.master, self.activePlot, *self.availablePlots, command=self.changePlot )
        self.pack()

    def updateEntries( self, ax ):
        active = self.plots.getActive()
        if ( active is None ):
            return

        xmin, xmax = ax.get_xlim()
        self.xmin.delete(0, tk.END )
        self.xmax.delete(0, tk.END)
        self.xmin.insert(0, xmin)
        self.xmax.insert(0,xmax)

        ymin, ymax = ax.get_ylim()
        self.ymin.delete(0, tk.END )
        self.ymax.delete(0, tk.END )
        self.ymin.insert(0,ymin)
        self.ymax.insert(0,ymax)

    def updateXmin( self, value ):
        self.plots.set_xlim( left=value )

    def updateXmax( self, value ):
        self.plots.set_xlim(right=value)

    def updateYmin( self, value ):
        self.plots.set_ylim( bottom=value )

    def updateYmax( self, value ):
        self.plots.set_ylim( top=value )

    def replot( self ):
        if ( self.plots.getActive() is None ):
            return

        # Update xmin
        try:
            xmin = float(self.xmin.get())
            self.updateXmin( xmin )
        except Exception as exc:
            print (str(exc))
            xmin, xmax = self.plots.getActive().ax.get_xlim()
            self.xmin.delete(0, tk.END)
            self.xmin.insert(0, str(xmin))

        # Update xmax
        try:
            xmax = float( self.xmax.get() )
            self.updateXmax(xmax)
        except Exception as exc:
            print (str(exc))
            xmin, xmax = self.plots.getActive().ax.get_xlim()
            self.xmax.delete(0, tk.END)
            self.xmax.insert(0, str(xmax))

        # Update ymin
        try:
            ymin = float( self.ymin.get() )
            self.updateYmin( ymin )
        except Exception as exc:
            print (str(exc))
            ymin, ymax = self.plots.getActive().ax.get_ylim()
            self.ymin.delete(0,tk.END)
            self.ymin.insert(0, ymin)

        # Update ymax
        try:
            ymax = float( self.ymax.get() )
            self.updateYmax( ymax )
        except Exception as exc:
            print (str(exc))
            ymin, ymax = self.plots.getActive().ax.get_ylim()
            self.ymax.delete(0,tk.END)
            self.ymax.insert(0, ymax)

        plt.show( block=False )

    def pack( self ):
        self.availablePlotsMenu.grid(row=0)
        self.xminLab.grid(row=1, column=0)
        self.xmin.grid(row=1,column=1)
        self.xmaxLab.grid(row=1,column=2)
        self.xmax.grid(row=1,column=3)
        self.yminLab.grid(row=2,column=0)
        self.ymin.grid(row=2, column=1)
        self.ymaxLab.grid(row=2,column=2)
        self.ymax.grid(row=2,column=3)
        self.replotButton.grid(row=3,column=0)
        self.saveButton.grid(row=3,column=1)
        self.saveAllButton.grid(row=3,column=2)
        self.closeAllButton.grid(row=3,column=3)

    def disableControls( self ):
        self.replotButton.config(state="disabled")
        self.saveButton.config(state="disabled")
        self.isDisabled = True

    def enableControls( self ):
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
            self.updateEntries( activeAx )

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
