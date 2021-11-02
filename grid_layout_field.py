from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QRadioButton
from .grid_layout import GridLayout
from .grid_regular_layout_field import GridRegularLayoutField
from .grid_variable_layout_field import GridVariableLayoutField


class GridLayoutField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, regularLayoutBtn: QRadioButton, regularLayoutField: GridRegularLayoutField,
                 variableLayoutBtn: QRadioButton, variableLayoutField: GridVariableLayoutField):
        super().__init__()
        self.setRegularLayoutBtn(regularLayoutBtn)
        self.setRegularLayoutField(regularLayoutField)
        self.setVariableLayoutBtn(variableLayoutBtn)
        self.setVariableLayoutField(variableLayoutField)

    def setRegularLayoutBtn(self, b: QRadioButton):
        b.toggled.connect(self.regularLayoutBtnToggled)
        self.__regularLayoutBtn = b

    def getRegularLayoutBtn(self) -> QRadioButton:
        return self.__regularLayoutBtn

    def regularLayoutBtnToggled(self):
        regularLayoutBtn = self.getRegularLayoutBtn()
        regularLayoutField = self.getRegularLayoutField()

        visible = regularLayoutBtn.isChecked()
        regularLayoutField.setVisible(visible)

    def setRegularLayoutField(self, f: GridRegularLayoutField):
        f.filled.connect(self.fieldFilled)
        self.__regularLayoutField = f

    def getRegularLayoutField(self) -> GridRegularLayoutField:
        return self.__regularLayoutField

    def setVariableLayoutBtn(self, b: QRadioButton):
        b.toggled.connect(self.variableLayoutBtnToggled)
        self.__variableLayoutBtn = b

    def getVariableLayoutBtn(self) -> QRadioButton:
        return self.__variableLayoutBtn

    def variableLayoutBtnToggled(self):
        variableLayoutBtn = self.getVariableLayoutBtn()
        variableLayoutField = self.getVariableLayoutField()

        visible = variableLayoutBtn.isChecked()
        variableLayoutField.setVisible(visible)

    def setVariableLayoutField(self, f: GridVariableLayoutField):
        f.filled.connect(self.fieldFilled)
        self.__variableLayoutField = f

    def getVariableLayoutField(self) -> GridVariableLayoutField:
        return self.__variableLayoutField

    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())

    def isFilled(self) -> bool:
        regularLayoutBtn = self.getRegularLayoutBtn()
        variableLayoutBtn = self.getVariableLayoutBtn()

        regularLayoutField = self.getRegularLayoutField()
        variableLayoutField = self.getVariableLayoutField()

        if regularLayoutBtn.isChecked():
            return regularLayoutField.isFilled()
        elif variableLayoutBtn.isChecked():
            return variableLayoutField.isFilled()

    def getLayout(self) -> GridLayout:
        regularLayoutBtn = self.getRegularLayoutBtn()
        variableLayoutBtn = self.getVariableLayoutBtn()

        regularLayoutField = self.getRegularLayoutField()
        variableLayoutField = self.getVariableLayoutField()

        if regularLayoutBtn.isChecked():
            return regularLayoutField.getLayout()
        elif variableLayoutBtn.isChecked():
            return variableLayoutField.getLayout()
