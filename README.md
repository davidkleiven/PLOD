# PLOD
Plot Designer (PLOD) is a small GUI for modifying matplotlib axis while being able to save as ps+ps_tex using Inkscape.

# Usage
Using the Plot Designer in a script requires a few extra lines of code.
First import the tkinter package
```python
import Tkinter as tk
```

Import the control GUI
```python
import controlGUI as cgui
```

Then create an instance of the Tk object
```python
root = tk.Tk()
```

After this create an instance of the *Control* object
```python
  control = cgui.Control(root)
```

At the end of the main function call the *mainloop*
```python
root.mainloop()
```

Each plot that can be modified by Plot Designer has to be attached.
This is done by providing a *figure* instance, *axes* instance and a
filename in case the figure should be stored.

```python
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
control.attach( fig, ax, "emptyFig.svg" )
```

An example is provided in the *guiTest.py* script.
