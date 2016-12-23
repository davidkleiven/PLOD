import numpy as np

class PlotHandler:
    def __init__(self):
        self.axes = []
        self.active = 0

    def set_xlim( self, left=None, right=None ):
        assert ( self.active < len(self.axes) )
        if ( not left is None ):
            self.axes[self.active].set_xlim( left=left )

        if ( not right is None ):
            self.axes[self.active].set_xlim( right=right )

    def set_ylim( self, lower=None, upper=None ):
        assert ( self.active < len(self.axes) )
        if ( not lower is None ):
            self.axes[self.active].set_ylim( lower=lower )

        if ( not upper is None ):
            self.axes[self.active].set_ylim( upper=upper )

    def attach( self, ax ):
        self.axes.append(ax)
        self.active = len(self.axes)-1
