import os
import json

from qgis.PyQt import uic
from PyQt5.QtWidgets import QTabWidget
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tab_grid.ui'))

from qgis.core import QgsProject
from mohid_qgis.plugin.tab_grid.grid_tool import GridTool
from mohid_qgis.plugin.tab_grid.grid_form import GridForm
from mohid_qgis.plugin.tab_grid.grid_layout_field import GridLayoutField
from mohid_qgis.plugin.tab_grid.grid_layer_name_field import GridLayerNameField
from mohid_qgis.plugin.tab_grid.capture_point_tool import CapturePointTool
from mohid_qgis.plugin.tab_grid.grid_double_field import GridDoubleField, GridGreaterThanZeroDoubleField
from mohid_qgis.plugin.tab_grid.grid_layout_table import GridLayoutTable
from mohid_qgis.plugin.tab_grid.grid_variable_spacing_field import GridVariableSpacingField
from mohid_qgis.plugin.tab_grid.grid_origin_field import GridOriginField
from mohid_qgis.plugin.tab_grid.grid_regular_layout_field import GridRegularLayoutField
from mohid_qgis.plugin.tab_grid.grid_item_adder import GridColAdder, GridRowAdder
from mohid_qgis.plugin.tab_grid.grid_variable_layout_field import GridVariableLayoutField
from mohid_qgis.plugin.tab_grid.crs import CRS
from qgis.PyQt.QtCore import QObject

class GridTab(QTabWidget, FORM_CLASS):

    def __init__(self, iface, config) -> None:
        super().__init__()

        self.setupUi(self)

        crs = CRS(QgsProject.instance().crs())
        crsField = self.mQgsProjectionSelectionWidget
        crsField.setCrs(crs)
        latitudeField = GridDoubleField(self.lineEditOriginLatitude)
        longitudeField = GridDoubleField(self.lineEditOriginLongitude)
        capturePointTool = CapturePointTool(iface, crs, self.toolButtonCapturePoint)
        originField = GridOriginField(latitudeField, longitudeField, capturePointTool)
        angleField = GridDoubleField(self.lineEditAngle)
        colSpacingField = GridGreaterThanZeroDoubleField(self.lineEditRegularColumnsSpacing)
        rowSpacingField = GridGreaterThanZeroDoubleField(self.lineEditRegularRowsSpacing)
        regularLayoutField = GridRegularLayoutField(self.spinBoxColumnsQuantity, self.spinBoxRowsQuantity, colSpacingField, rowSpacingField, self.labelRegularSpacing)
        gridLayoutTable = GridLayoutTable(self.labelLayout, self.tableWidgetLayout)
        colSpacingStartField = GridGreaterThanZeroDoubleField(self.lineEditVariableSpacedColumnsSpacingStart)
        colSpacingEndField = GridGreaterThanZeroDoubleField(self.lineEditVariableSpacedColumnsSpacingEnd)
        rowSpacingStartField = GridGreaterThanZeroDoubleField(self.lineEditVariableSpacedRowsSpacingStart)
        rowSpacingEndField = GridGreaterThanZeroDoubleField(self.lineEditVariableSpacedRowsSpacingEnd)
        colVariableSpacingField = GridVariableSpacingField(colSpacingStartField, colSpacingEndField)
        rowVariableSpacingField = GridVariableSpacingField(rowSpacingStartField, rowSpacingEndField)
        colAdder = GridColAdder(self.spinBoxColumnsQuantity, colVariableSpacingField, self.toolButtonAddColumns)
        rowAdder = GridRowAdder(self.spinBoxRowsQuantity, rowVariableSpacingField, self.toolButtonAddRows)
        variableLayoutField = GridVariableLayoutField(gridLayoutTable, self.labelSpacingRange, colAdder, rowAdder)
        layoutField = GridLayoutField(self.radioButtonRegular, regularLayoutField, self.radioButtonVariableSpaced, variableLayoutField)
        layerNameField = GridLayerNameField(self.lineEditLayerName, self.toolButtonLayerName)
        form = GridForm(crsField, originField, angleField, layoutField, layerNameField)

        self.gridTool = GridTool(form, self.pushButtonPreview, self.pushButtonLoad, self.pushButtonSave, config)