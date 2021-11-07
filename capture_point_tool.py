from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QCursor, QIcon
from qgis.PyQt.QtWidgets import QToolButton
from qgis.gui import QgsMapToolEmitPoint, QgsMapMouseEvent, QgisInterface
from qgis.core import QgsCoordinateTransform, QgsProject
from .crs import CRS

"""
The CapturePointTool class implements the tool to capture the origin coordinates from the map with
a mouse click.
"""
class CapturePointTool(QgsMapToolEmitPoint):
    """
    The canvasClicked attribute is a signal that emits a QgsPointXY when the user clicks on the
    canvas.
    """
    canvasClicked = pyqtSignal('QgsPointXY')

    """
    The CapturePointTool constructor receives:
        - the Qgis interface to retreive the current map canvas
        - the currently selected Coordinate Reference System
        - the button that activates and deactivates the CapturePointTool
    """
    def __init__(self, interface: QgisInterface, crs: CRS, btn: QToolButton):
        canvas = interface.mapCanvas()
        super().__init__(canvas)
        self.setCrs(crs)
        self.setInterface(interface)
        self.setButton(btn)

        icon = QIcon(':images/themes/default/cursors/mCapturePoint.svg')
        pixmap = icon.pixmap(48, 48)
        cursor = QCursor(pixmap)
        self.setCursor(cursor)

    def setCrs(self, crs: CRS):
        self.__crs = crs

    def getCrs(self) -> CRS:
        return self.__crs

    def setInterface(self, i: QgisInterface):
        self.__interface = i

    def getInterface(self) -> QgisInterface:
        return self.__interface

    """
    The button setter receives a QToolButton object and connects its toggled signal
    to the buttonToggled function.
    When the button is toggled, the buttonToggled function is called.
    """

    def setButton(self, b: QToolButton):
        icon = QIcon(":images/themes/default/cursors/mCapturePoint.svg")
        b.setIcon(icon)
        super().setButton(b)
        b.toggled.connect(self.buttonToggled)

    """
    The buttonToggled function is called when the button is toggled.
    If the button is checked the CapturePointTool is activated.
    If the button is unchecked the CapturePointTool is deactivated.
    """
    def buttonToggled(self):
        interface = self.getInterface()
        b = self.button()

        if b.isChecked():
            interface.mapCanvas().setMapTool(self)
        else:
            interface.mapCanvas().unsetMapTool(self)

    """
    The canvasReleaseEvent function executes when the map is clicked with the mouse.
    This function translates the coordinates of the point that was clicked to the
    coordinate reference system selected by the user.
    The point with the translated coordinates is emitted with the canvasClicked
    signal.
    This signal is received by the GridOriginField class.
    After emitting the signal the CapturePointTool is deactivated
    """
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

    """
    The close function deactivates the CapturePointTool.
    This function is called when the plugin is closed.
    """
    def close(self):
        b = self.button()
        if b.isChecked():
            b.toggle()
