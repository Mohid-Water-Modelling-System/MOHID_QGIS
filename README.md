# MOHID plugin for QGIS
This repository holds the [QGIS](https://qgis.org/) plugin of the 
[MOHID](http://www.mohid.com/) model.

- [Overview](#overview)
- [Supported features](#supported-features)
- [Development](#development)
    - [Setup](#setup)
    - [Plugin structure suggestion](#plugin-structure-suggestion)

# Overview

# Supported features

## MOHID Grids (.grd)

### Generation

Regular and irregular grids are supported.
Curvillinear grids are not supported.

### Visualization

Regular, irregular and curvillinear grids are supported.

### Editing

Regular grids are supported.
Irregular and curvillinear grids are not supported.

## MOHID Land polygon files (.xy)

Visualization supported.

## MOHID XYZ files (.xyy)

Visualization supported. 
When loading, a default style is applied to the layer that uses the "Spectral"
color ramp and takes as minimum as maximum values the minimum and maximum depth
values found in the layer.

## MOHID Bathymetry files

### View and editing 

Regular and curvillinear grid bathymetries are supported.

Note that editing refers to the bathymetry depth values.

When loading, a default style is applied to the layer in order to better 
visualize the depth data.

### Generation

Bathymetries can be generated with any of the MOHID files mention so far.

## Notes
- COORD_TIP
    ```
        1 - Geographic coordinates
        2 - UTM coordinates
        3 - Portuguese military coordinates
        4 - Simplified geographic coordinates: in Degrees
        5 - Metric coordinates referred to the origin of the grid
        6 - Circular coordinates
        7 - NRLD - Dutch metric coordinate system
    ```
- Cells coordinates represent the Lower left corner

For now, grid will default to COORD_TIP 4.
# Development

`Python` version: 3.9

`QGIS` version: 3.22

OS: `Windows 10`

## Setup

    git clone https://github.com/Mohid-Water-Modelling-System/mohid_qgis.git

This plugin uses external Python packages to read and write data.
On windows, some are available with every QGIS installation, like GDAL, 
while others are installed separately, like netCDF4. 

For now and for the purpose of developing, these packages are manually 
installed.

### External packages

QGIS for Windows ships with its own python installation, this means if a 
third-party python module is required it has to be installed in the QGIS python 
environment and not on the system's.

To install python packages follow the following steps:

Find the "OSGeo4W Shell" that should be in the desktop shortcuts, installed 
during QGIS setup, and execute it. Then run the following instructions on the 
shell:

    cd C:\Users\{USER}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\mohid_qgis

where {USER} corresponds to the current Windows user account.

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

### QGIS plugin install (via symbolic link)

Installing a QGIS plugin can be done through the repositories manually.
For developing the plugin should be installed manually.

Different versions of QGIS might consider different locations for its plugins. 
To avoid working from the QGIS plugin folder directly, it is recommended to set 
the repository elsewhere and create a symbolic link to the the plugin folder:

In windows (cmd.exe):

    mklink /D C:\Users\<USER>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\mohid_qgis <cloned_repository_dir>\mohid_qgis

To activate the MOHID plugin on [QGIS](https://qgis.org/):
1. Select `Plugins` on the Menu Toolbar
2. Select `Manage and Install Plugins...`
3. Select `Installed` on the left-side menu
4. Use the `MOHID` checkbox to activate the MOHID plugin

Once activated, a new plugin button should appear in the Toolbar.
QGIS should now be running with the MOHID plugin.

**NOTES:** 

To find the QGIS _plugin path_, open QGIS and do as follows:
1. Select `Settings` on the Menu Toolbar
2. Select `User profiles` -> `Open active profile folder`
3. Open the `python/plugins` subdirectory - that is the plugin path for QGIS.

If the plugins folder under python does not exist, it can be created manually.

AppData is usually a hidden folder.

### Debugger setup for vscode

There is a plugin for QGIS called `debugvs` that allows easy debugging for 
VS Code. To use it just enable the plugin from QGIS and add a `Remote Attach` 
debug configuration to VS Code that should look like the following:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": ".",
                    "remoteRoot": "C:/Users/{USER}/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/mohid_qgis/"
                }
            ],
            "justMyCode": true
        }
    ]
}
```
From this point you can start debugging.

## Plugin structure suggestion

For ease of development, the plugin is divided in two main directories, core 
and plugin:

    mohid_qgis/
        core/
        plugin/

The `plugin` directory will hold the plugin itself, with the UI elements and 
everything related to their interface logic.

The `core` directory will hold all non-QGIS-dependent code, additional tools 
such as utilities, algorithms, conversion scripts, etc...

## User Interface

QGIS uses `.ui` files to represent an UI and a `Python` file to hold the logic 
of the UI ( e.g.: button actions).

The UI for this plugin is based on a `QDockWidget` with an empty `QTabWidget`. 
Individual tabs are added on top. This allows the individual development and 
isolation of each tab which allows for an organized scaling of the plugin.
Each tab will then consist of at least a `.ui` and a `Python` files. The 
`plugin/tab_bathymetry` directory holds the bathymetry tab code and can be 
consulted for reference.

### Add new tab

To add a new tab, one must first create the respective UI interface. The best
way of doing this is to use QT Designer, which should come with the QGIS 
installation. This will generate a `.ui` file that is used by QGIS to render 
the UI. This can also be done manually by writing every UI element and its 
attributes into a `.ui` file. However, this approach is not recommended as it 
takes more time and is prone to errors. 

# Useful websites

- [Python GDAL/OGR Cookbook](https://pcjericks.github.io/py-gdalogr-cookbook/)
- Python QGIS cookbook
- QGIS documentation

# Future Work

- Conversion tab
- CRSTypes do not correspond to COORD_TIP correctly
- Configure MOHID coordinate types in config.json
- Remove variable layout items from layout table
- Integrate conversions between the various formats used and mohid formats