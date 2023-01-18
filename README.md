# MOHID plugin for QGIS
This repository holds the [QGIS](https://qgis.org/) plugin of the [MOHID](http://www.mohid.com/) model.

## Notes

python version: 3.9
qgis version: 3.22
tested in windows 10 and ubuntu 20.04

## Development setup

### Clone repository

    git clone https://github.com/Mohid-Water-Modelling-System/mohid_qgis.git

### Create a symbolic link for the plugin 

Different versions of QGIS might consider different locations for its plugins. To avoid working from the QGIS plugin folder, it is recommended to set the repository elsewhere and create a symbolic link to the the plugin folder, for e.g.:

In windows (cmd.exe):

    mklink /D C:\Users\<USER>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\mohid_qgis \C:\Users\<USER>\GitHub\mohid_qgis\mohid_qgis
   

**NOTE:**  To find the QGIS _plugin path_, open QGIS and do as follows:
1. Select `Settings` on the Menu Toolbar
2. Select `User profiles` -> `Open active profile folder`
3. Open the `python/plugins` subdirectory - that is the plugin path for QGIS.

### Debugger setup

TODO

## Activate the MOHID plugin

To activate the MOHID plugin on [QGIS](https://qgis.org/):
1. Select `Plugins` on the Menu Toolbar
2. Select `Manage and Install Plugins...`
3. Select `Installed` on the left-side menu
4. Use the `MOHID` checkbox to activate the MOHID plugin

Once activated, a new plugin button should appear in the Toolbar.

## Task list

- [x] Regular grid creator
- [x] Variable spaced grid creator
- [x] Set coordinates with mouse capture
- [x] Dock widget
- [ ] Write grid to .dat file
- [ ] Write grid to .grd file
- [ ] Read grid from .grd file
- [x] Read frid from .dat file
- [x] Optimize definition of points and polygons
- [ ] Configure MOHID coordinate types in config.json
- [ ] Remove variable layout items from layout table
- [ ] Integrate conversions between the various formats used and mohid formats
- [ ] Move expensive processing tasks to separate thread

## Dev environment

    sudo apt install qgis qgis-plugin-grass pyqt5-dev-tools python3-pip --install-recommends --yes

## Issues

- Double validation is unstable, validates only comma separated values, but then it can't convert them to strings
- CRSTypes do not correspond to COORD_TIP correctly

    COORD_TIP
    ```
    1 - Geographic coordinates
    2 - UTM coordinates
    3 - Portuguese military coordinates
    4 - Simplified geographic coordinates: in Degrees
    5 - Metric coordinates referred to the origin of the grid
    6 - Circular coordinates
    7 - NRLD - Dutch metric coordinate system
    ```

    For now, grid will default to COORD_TIP 4.

# Plugin

## Grid origin

Lower left corner

## Load to layer support

[x] - .grd
[x] - .xy
[x] - .xyz
[ ] - .dat

## Convert options

gridConverter.py functions

- grid2netcdf
- grid2shpfile

polygonConverter.py functions

- 

