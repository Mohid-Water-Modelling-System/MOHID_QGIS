# MOHID plugin for QGIS
This repository holds the [QGIS](https://qgis.org/) plugin of the [MOHID](http://www.mohid.com/) model.

## Notes

python version: 3.9
qgis version: 3.16+
tested in windows 10 and ubuntu 20.04

## Compile and Deploy

Use [pb_tool](https://github.com/g-sherman/plugin_build_tool) to compile and deploy the MOHID plugin, specifying the directory where to deploy the plugin:

```bash
pbt deploy -p PATH
```

>  **_NOTE:_**  To find the plugin path open [QGIS](https://qgis.org/):
> 1. Select `Settings` on the Menu Toolbar
> 2. Select `User profiles` -> `Open active profile folder`
> 3. Open the `python/plugins` subdirectory - that is the plugin path for QGIS.

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

