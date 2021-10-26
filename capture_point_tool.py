
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QCursor, QIcon
from qgis.PyQt.QtWidgets import QToolButton
from qgis.gui import QgsMapToolEmitPoint, QgsMapMouseEvent, QgisInterface
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject


class CapturePointTool(QgsMapToolEmitPoint):
    canvasClicked = pyqtSignal('QgsPointXY')

    def __init__(self, interface: QgisInterface, crs: QgsCoordinateReferenceSystem, btn: QToolButton):
        canvas = interface.mapCanvas()
        super().__init__(canvas)
        self.setCrs(crs)
        self.setInterface(interface)
        self.setButton(btn)

        icon = QIcon(':images/themes/default/cursors/mCapturePoint.svg')
        pixmap = icon.pixmap(48, 48)
        cursor = QCursor(pixmap)
        self.setCursor(cursor)

    def setCrs(self, crs: QgsCoordinateReferenceSystem):
        self.__crs = crs

    def getCrs(self) -> QgsCoordinateReferenceSystem:
        return self.__crs

    def setInterface(self, i: QgisInterface):
        self.__interface = i

    def getInterface(self) -> QgisInterface:
        return self.__interface

    def setButton(self, b: QToolButton):
        icon = QIcon(":images/themes/default/cursors/mCapturePoint.svg")
        b.setIcon(icon)
        super().setButton(b)
        b.toggled.connect(self.buttonToggled)

    def buttonToggled(self):
        interface = self.getInterface()
        b = self.button()

        if b.isChecked():
            interface.mapCanvas().setMapTool(self)
        else:
            interface.mapCanvas().unsetMapTool(self)

    def canvasReleaseEvent(self, event: QgsMapMouseEvent):
        crs_canvas = self.canvas().mapSettings().destinationCrs()
        crs = self.getCrs()
        interface = self.getInterface()
        coordinateTransform = QgsCoordinateTransform(
            crs_canvas, crs, QgsProject.instance())
        point_canvas = event.mapPoint()
        point = coordinateTransform.transform(point_canvas)
        self.canvasClicked.emit(point)
        interface.mapCanvas().unsetMapTool(self)
    
    def close(self):
        b = self.button()
        if b.isChecked():
            b.toggle()
