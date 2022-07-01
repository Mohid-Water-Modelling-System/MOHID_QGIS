# Development notes

- [Overview](#overview)

# Overview

## Package structure suggestion

- `mohid_qgis.core` contains all non-QGIS-dependent code
- `mohid_qgis.plugin` is the QGIS plugin and uses `gis4wrf.core`

## External packages

mohid_qgis uses external Python packages to read and write data.
On windows, some are available with every QGIS installation, like GDAL, 
while others are installed separately, like netCDF4. 

For now and for the purpose of developing, these packages are manually installed.

In the future this might be automated and different versions of Python might be
supported at the same time, see `gis4wrf/bootstrap.py` in the gis4wrf
plugin code for more details on handling external packages.


## Useful websites

TODO:

- [Python GDAL/OGR Cookbook](https://pcjericks.github.io/py-gdalogr-cookbook/)
- Python QGIS cookbook
- QGIS documentation