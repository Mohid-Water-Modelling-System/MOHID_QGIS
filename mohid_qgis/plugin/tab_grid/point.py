from qgis.core import QgsPointXY
import math
from .angle import Angle

"""
The Point class implements a corner of a cell of the grid.
This class is a child of the QgsPointXY, providing all the method of QgsPointXY plus a rotate
method used to rotate the point around an origin. 
"""
class Point(QgsPointXY):
    """
    The rotate function rotates the point around an origin point.
    The coordinates of the point are updated with the coordinates calculated from the original
    coordinates, the origin and the angle.
    """
    def rotate(self, origin: 'Point', angle: Angle):
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        x = self.x()
        y = self.y()
        xO = origin.x()
        yO = origin.y()
        self.setX(xO + cos * (x - xO) - sin * (y - yO))
        self.setY(yO + sin * (x - xO) + cos * (y - yO))

"""
The Origin class is a child of the Point class.
It is a point, which coordinates can be written in the MOHID format of the origin coordinates.
"""
class Origin(Point):
    """
    The toString function is used to write the coordinates of the origin of the grid in MOHID format.
    The string is built according to the first argument of the function, which is
    the configuration provided in form of a dictionary.
    This configuration was previously read from the config.json file.
    """
    def toString(self, config: dict) -> str:
        fmt = config["fmt"]
        keyX = config["keys"][type(self).__name__]["x"]
        x = self.x()
        keyY = config["keys"][type(self).__name__]["y"]
        y = self.y()
        return fmt.format("ORIGIN", f"{x} {y}")