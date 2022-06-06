# LightingTools
Collection of tools for lighting artists in Maya (WIP)
Tested so far on Windows 10 - Maya 2022.1 - mtoa 5.0.0.2

# Installation:
1. Copy and paste the cgxLightingTools folder to your favorite scripts folder.
Ex: C:\Users\xxxx\Documents\maya\scripts\cgxLightingTools
2. Open your Maya.env file with a text editor. It's usually located at C:\Users\xxxx\Documents\maya\2018
3. Add the same folder path in 1. to your Maya.env
MAYA_MODULE_PATH=C:\Users\xxxx\Documents\maya\scripts\cgxLightingTools;

# Launching:
```python
import cgxLightingTools.launch as lgtTools
lgtTools.launch()
```
