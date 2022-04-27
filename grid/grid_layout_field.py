from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QRadioButton
from .grid_layout import GridLayout
from .grid_regular_layout_field import GridRegularLayoutField
from .grid_variable_layout_field import GridVariableLayoutField


"""
The GridLayoutField controls the regular layout field and the variable layout field.
Since the layout of the grid can be either regular or variable. There are two radio button that
display one layout field and hide the other.
The layout specified in this field is used to construct the grid.
This class is a child of QObject to be able to have a pyqtSignal attribute.
"""
class GridLayoutField(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the state of the field changes.
    If the field is correctly filled, true is emitted.
    If the field becomes not correctly filled, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The GridLayoutField constructor receives:
        - two QRadioButtons, when one is checked the other is automatically unchecked. They are
        used to select which type of layout the grid will have (regular or variable). According
        to the selected option either the regularLayoutField or the variableLayoutField is displayed.
        - a field for setting a regular layout
        - a field for setting a variable layout
    """
    def __init__(self, regularLayoutBtn: QRadioButton, regularLayoutField: GridRegularLayoutField,
                 variableLayoutBtn: QRadioButton, variableLayoutField: GridVariableLayoutField):
        super().__init__()
        self.setRegularLayoutBtn(regularLayoutBtn)
        self.setRegularLayoutField(regularLayoutField)
        self.setVariableLayoutBtn(variableLayoutBtn)
        self.setVariableLayoutField(variableLayoutField)

    """
    The regular layout button setter receives a QRadioButton object and connects
    its toggled signal to the regularLayoutBtnToggled function.
    When the button is toggled, the regularLayoutBtnToggled function is called.
    """
    def setRegularLayoutBtn(self, b: QRadioButton):
        b.toggled.connect(self.regularLayoutBtnToggled)
        self.__regularLayoutBtn = b

    def getRegularLayoutBtn(self) -> QRadioButton:
        return self.__regularLayoutBtn

    """
    The regularLayoutBtnToggled function is called when the regularLayout button is toggled.
    It checks if the regular layout button is checked.
    Then if the button is checked, the regularlayoutfield is displayed.
    If it is unchecked, the regularLayoutField is hidden.
    """
    def regularLayoutBtnToggled(self):
        regularLayoutBtn = self.getRegularLayoutBtn()
        regularLayoutField = self.getRegularLayoutField()

        visible = regularLayoutBtn.isChecked()
        regularLayoutField.setVisible(visible)

    """
    The RegularLayoutField setter receives a GridRegularLayoutField object and connects its
    "filled" signal to the fieldFilled function.
    When the layout is changed, the fieldFilled function is called.
    """
    def setRegularLayoutField(self, f: GridRegularLayoutField):
        f.filled.connect(self.fieldFilled)
        self.__regularLayoutField = f

    def getRegularLayoutField(self) -> GridRegularLayoutField:
        return self.__regularLayoutField

    """
    The variable layout button setter receives a QRadioButton object and connects
    its toggled signal to the variableLayoutBtnToggled function.
    When the button is toggled, the variableLayoutBtnToggled function is called.
    """
    def setVariableLayoutBtn(self, b: QRadioButton):
        b.toggled.connect(self.variableLayoutBtnToggled)
        self.__variableLayoutBtn = b

    def getVariableLayoutBtn(self) -> QRadioButton:
        return self.__variableLayoutBtn

    """
    The variableLayoutBtnToggled function is called when the variableLayout button is toggled.
    It checks if the variable layout button is checked.
    Then if the button is checked, the variablelayoutfield is displayed.
    If it is unchecked, the variableLayoutField is hidden.
    """
    def variableLayoutBtnToggled(self):
        variableLayoutBtn = self.getVariableLayoutBtn()
        variableLayoutField = self.getVariableLayoutField()

        visible = variableLayoutBtn.isChecked()
        variableLayoutField.setVisible(visible)

    """
    The VariableLayoutField setter receives a GridVariableLayoutField object and connects its
    "filled" signal to the fieldFilled function.
    When the layout is changed, the fieldFilled function is called.
    """
    def setVariableLayoutField(self, f: GridVariableLayoutField):
        f.filled.connect(self.fieldFilled)
        self.__variableLayoutField = f

    def getVariableLayoutField(self) -> GridVariableLayoutField:
        return self.__variableLayoutField

    """
    The fieldFilled function is called when the filled signal of a field emits a new state.
    If the state is false, it means that the field was correctly field and became unfilled.
    In this case the fieldFilled function emits a filled signal with false too.
    Otherwise it checks whether everything is filled with an acceptable input and emits a signal
    that can either be true or false.
    """
    def fieldFilled(self, filled: bool):
        if not filled:
            self.filled.emit(False)
        else:
            self.filled.emit(self.isFilled())

    """
    The isFilled function returns true if the field corresponding to the selected layout type
    is filled with an acceptable layout and false otherwise.
    """
    def isFilled(self) -> bool:
        regularLayoutBtn = self.getRegularLayoutBtn()
        variableLayoutBtn = self.getVariableLayoutBtn()

        regularLayoutField = self.getRegularLayoutField()
        variableLayoutField = self.getVariableLayoutField()

        if regularLayoutBtn.isChecked():
            return regularLayoutField.isFilled()
        elif variableLayoutBtn.isChecked():
            return variableLayoutField.isFilled()

    """
    The getLayout function returns a GridLayout object, that is either a GridVariableLayout or
    a GridRegularLayout, depending on the layout type that is selected.
    """
    def getLayout(self) -> GridLayout:
        regularLayoutBtn = self.getRegularLayoutBtn()
        variableLayoutBtn = self.getVariableLayoutBtn()

        regularLayoutField = self.getRegularLayoutField()
        variableLayoutField = self.getVariableLayoutField()

        if regularLayoutBtn.isChecked():
            return regularLayoutField.getLayout()
        elif variableLayoutBtn.isChecked():
            return variableLayoutField.getLayout()
