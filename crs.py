from qgis.core import QgsCoordinateReferenceSystem

class CRS(QgsCoordinateReferenceSystem):
    def toString(self, config: dict) -> str:
        fmt = config["fmt"]
        key = config["keys"][type(self).__name__]
        epsg = self.authid()
        if epsg not in config["CRSTypes"]:
            raise Exception("Coordinate Type not supported")
        value = config["CRSTypes"][epsg]
        return fmt.format(key, value)