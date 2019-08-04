# LightingTools
Collection of tools for lighting artists in Maya (WIP)
Tested so far with Maya 2018.6- mtoa 3.2.0.2

# Installation:
1. Copy and paste the contents of the downloaded files to your favorite scripts folder.
2. Open the file named CGXLightingTools.mod with a simple text editor
3. Change the path on the first line to where the CGXLightingTools.mod file is located.
Ex: C:\Users\xxxx\Documents\maya\scripts\cgxLightingTools
4. Add the same directory path to your Maya.env, usually located at C:\Users\xxxx\Documents\maya\2018
MAYA_MODULE_PATH=C:\Users\xxxx\Documents\maya\scripts\cgxLightingTools;

# Launching:
```python
import cgxLightingTools.launch as lgtTools
lgtTools.launch()
```
