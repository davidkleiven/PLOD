# PLOD
Plot Designer (PLOD) is a small GUI for modifying matplotlib axis while being able to save as ps+ps_tex using Inkscape.

# Usage
Using the Plot Designer in a script requires a few extra lines of code.
First import the tkinter package
```python
import tkinter as tk
```

Import the control GUI
```python
from PLOD import controlGUI as cgui
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
The axes can either be altered by the sliders provided in the GUI or
by using the standard zooms and pan funcionality that comes with *matplotlib*.

# Installation
To install the pacakge, run the *setup.py* script
```bash
python3 setup.py install/develop--user
```
if *install* is given, the module files will be copied and new changes will only
be effective when the module is reinstalled.
If *develop* is given, only a link is required and new changes is effective.
Omit *--user* if the install should be available for all users.
