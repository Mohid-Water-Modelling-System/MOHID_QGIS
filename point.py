from qgis.core import QgsPointXY
import math
from .angle import Angle


class Point(QgsPointXY):
    def rotate(self, origin: 'Point', angle: Angle):
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        x = self.x()
        y = self.y()
        xO = origin.x()
        yO = origin.y()
        self.setX(xO + cos * (x - xO) - sin * (y - yO))
        self.setY(yO + sin * (x - xO) + cos * (y - yO))

class Origin(Point):
    def toString(self, config: dict) -> str:
        fmt = config["fmt"]
        keyX = config["keys"][type(self).__name__]["x"]
        x = self.x()
        keyY = config["keys"][type(self).__name__]["y"]
        y = self.y()
        return fmt.format(keyX, x) + fmt.format(keyY, y)