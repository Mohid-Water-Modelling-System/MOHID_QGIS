
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QCursor, QIcon
from qgis.PyQt.QtWidgets import QApplication

from qgis.gui import QgsMapToolEmitPoint, QgsMapMouseEvent, QgsMapCanvas
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject

class CapturePointTool(QgsMapToolEmitPoint):
    canvasClicked = pyqtSignal('QgsPointXY')

    def __init__(self, canvas: QgsMapCanvas, crs: QgsCoordinateReferenceSystem):
        self.setCanvas(canvas)
        self.setCrs(crs)
        self.setCursor(QCursor(
            QIcon(':images/themes/default/cursors/mCapturePoint.svg').pixmap(48, 48)))
        QgsMapToolEmitPoint.__init__(self, self.canvas)

    def setCanvas(self, canvas: QgsMapCanvas):
        self.canvas = canvas

    def getCanvas(self) -> QgsMapCanvas:
        return self.canvas

    def setCrs(self, crs: QgsCoordinateReferenceSystem):
        self.crs = crs

    def getCrs(self) -> QgsCoordinateReferenceSystem:
        return self.crs

    def setCursor(self, cursor: QCursor):
        self.cursor = cursor

    def getCursor(self) -> QCursor:
        return self.cursor

    def canvasReleaseEvent(self, event: QgsMapMouseEvent):
        crs_canvas = self.getCanvas().mapSettings().destinationCrs()
        crs = self.getCrs()
        coordinateTransform = QgsCoordinateTransform(
            crs_canvas, crs, QgsProject.instance())
        point_canvas = event.mapPoint()
        point = coordinateTransform.transform(point_canvas)
        self.canvasClicked.emit(point)

    def activate(self):
        cursor = self.getCursor()
        QApplication.setOverrideCursor(cursor)

    def deactivate(self):
        QApplication.restoreOverrideCursor()
