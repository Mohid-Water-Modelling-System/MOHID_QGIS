
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QCursor, QIcon

from qgis.gui import QgsMapToolEmitPoint, QgsMapMouseEvent, QgsMapCanvas
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject

class CapturePointTool(QgsMapToolEmitPoint):
    canvasClicked = pyqtSignal('QgsPointXY')

    def __init__(self, canvas: QgsMapCanvas, crs: QgsCoordinateReferenceSystem):
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.setCrs(crs)
        self.setCursor(QCursor(
            QIcon(':images/themes/default/cursors/mCapturePoint.svg').pixmap(48, 48)))

    def setCrs(self, crs: QgsCoordinateReferenceSystem):
        self.crs = crs

    def getCrs(self) -> QgsCoordinateReferenceSystem:
        return self.crs

    def canvasReleaseEvent(self, event: QgsMapMouseEvent):
        crs_canvas = self.canvas().mapSettings().destinationCrs()
        crs = self.getCrs()
        coordinateTransform = QgsCoordinateTransform(
            crs_canvas, crs, QgsProject.instance())
        point_canvas = event.mapPoint()
        point = coordinateTransform.transform(point_canvas)
        self.canvasClicked.emit(point)