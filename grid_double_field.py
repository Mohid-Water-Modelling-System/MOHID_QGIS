from os import replace
from qgis.PyQt.QtWidgets import QLineEdit
from qgis.PyQt.QtGui import QDoubleValidator
from qgis.PyQt.QtCore import QObject, pyqtSignal
from .greater_than_zero_double_validator import GreaterThanZeroDoubleValidator


"""
GridDoubleField controls a QLineEdit of the GridTool that receives a double as input.
The GridDoubleField is used for the fields of the Grid Tool where the user enters the
coordinates of the origin and the angle of the grid.
This class is a child of QObject to be able to have a pyqtSignal attribute.
"""
class GridDoubleField(QObject):
    """
    The filled attribute is a signal that emits a boolean value when the state of the field changes.
    If the field is correctly filled, true is emitted.
    If the field becomes not correctly filled, false is emitted.
    """
    filled = pyqtSignal(bool)

    """
    The GridDoubleField constructor receives a QLineEdit, which is the lineEdit for entering
    double values.
    """
    def __init__(self, l: QLineEdit):
        super().__init__()
        self.setLineEdit(l)

    """
    The LineEdit setter receives a QLineEdit object,
    creates a validator for the LineEdit to accept double values only and connects
    its textChanged signal to the lineEditTextChanged function.
    When the text of the LineEdit changes, the lineEditTextChanged function is called.
    """
    def setLineEdit(self, l: QLineEdit):
        validator = QDoubleValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.lineEditTextChanged)
        self.__lineEdit = l

    def getLineEdit(self) -> QLineEdit:
        return self.__lineEdit

    """
    The lineEditTextChanged function is called when the content of the LineEdit is changed.
    It checks if the field is correctly filled and emits the signal "filled" which has a boolean
    that is true when the field is correctly filled and false when the field is not correctly filled.
    """
    def lineEditTextChanged(self):
        filled = self.isFilled()
        self.filled.emit(filled)

    """
    The isFilled function returns true if the lineEdit is filled with an acceptable value and
    false otherwise.
    """
    def isFilled(self) -> bool:
        l = self.getLineEdit()
        filled = l.hasAcceptableInput()
        return filled

    def setValue(self, v: float):
        text = str(v)
        l = self.getLineEdit()
        l.setText(text)

    """
    The getValue function returns a float with the value written in the lineEdit
    """
    def getValue(self) -> float:
        l = self.getLineEdit()
        text = l.text().replace(",", ".")
        value = float(text)
        return value
    
    """
    The setVisible function displays the lineEdit if the "v" argument is true and hides the lineEdit
    if the "v" argument is false
    """
    def setVisible(self, v: bool):
        l = self.getLineEdit()
        l.setVisible(v)


"""
The  GridGreaterThanZeroDoubleField class is a child of the GridDoubleField class.
It does everything the GridDoubleField class does but uses the GreaterThanZeroDoubleValidator.
Therefore this class does not accept doubles that are negative or 0.
"""
class GridGreaterThanZeroDoubleField(GridDoubleField):
    """
    The setLineEdit function overrides the setLineEdit function of the parent class.
    The only difference is the validator (GreaterThanZeroDoubleValidator instead of QDoubleValidator)
    """
    def setLineEdit(self, l: QLineEdit):
        validator = GreaterThanZeroDoubleValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.lineEditTextChanged)
        self.__lineEdit = l
    
    def getLineEdit(self) -> QLineEdit:
        return self.__lineEdit