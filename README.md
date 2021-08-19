# MOHID plugin for QGIS
This repository holds the [QGIS](https://qgis.org/) plugin of the [MOHID](http://www.mohid.com/) model.

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
- [ ] Read grid from .grd file
- [ ] Write grit to .grd file
- [ ] Read grid from .grd file
- [ ] Write grid to .grd file
- [x] Optimize definition of points and polygons