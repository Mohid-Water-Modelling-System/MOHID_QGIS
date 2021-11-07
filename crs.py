from qgis.core import QgsCoordinateReferenceSystem

"""
The CRS class is a child of the QgsCoordinateReferenceSystem class.
It holds Coordinate Reference System with which the grid is represented.
"""
class CRS(QgsCoordinateReferenceSystem):
    """
    The toString function is used to write the Coordinate Reference System of the grid
    in MOHID format.
    The string is built according to the first argument of the function, which is
    the configuration provided in form of a dictionary.
    This configuration was previously read from the config.json file.
    This configuration translates the QGis CRS EPSG codes to the MOHID format codes 
    """
    def toString(self, config: dict) -> str:
        fmt = config["fmt"]
        key = config["keys"][type(self).__name__]
        epsg = self.authid()
        if epsg not in config["CRSTypes"]:
            raise Exception("Coordinate Type not supported")
        value = config["CRSTypes"][epsg]
        return fmt.format(key, value)