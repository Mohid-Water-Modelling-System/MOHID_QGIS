from qgis.core import QgsPointXY
import math


class Point(QgsPointXY):
    def rotate(self, origin: 'Point', angle: float):
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        x = self.x()
        y = self.y()
        xO = origin.x()
        yO = origin.y()
        self.setX(xO + cos * (x - xO) - sin * (y - yO))
        self.setY(yO + sin * (x - xO) + cos * (y - yO))
