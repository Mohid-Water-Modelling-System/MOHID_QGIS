from qgis.PyQt.QtWidgets import QLineEdit
from qgis.PyQt.QtGui import QDoubleValidator
from qgis.PyQt.QtCore import QObject, pyqtSignal
from .greater_than_zero_double_validator import GreaterThanZeroDoubleValidator


class GridDoubleField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, l: QLineEdit):
        super().__init__()
        self.setLineEdit(l)

    def setLineEdit(self, l: QLineEdit):
        validator = QDoubleValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.lineEditTextChanged)
        self.__lineEdit = l

    def getLineEdit(self) -> QLineEdit:
        return self.__lineEdit

    def lineEditTextChanged(self):
        filled = self.isFilled()
        self.filled.emit(filled)

    def isFilled(self) -> bool:
        l = self.getLineEdit()
        filled = l.hasAcceptableInput()
        return filled

    def setValue(self, v: float):
        text = str(v)
        l = self.getLineEdit()
        l.setText(text)

    def getValue(self) -> float:
        l = self.getLineEdit()
        text = l.text()
        value = float(text)
        return value
    
    def setVisible(self, v: bool):
        l = self.getLineEdit()
        l.setVisible(v)

class GridGreaterThanZeroDoubleField(GridDoubleField):
    def setLineEdit(self, l: QLineEdit):
        validator = GreaterThanZeroDoubleValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.lineEditTextChanged)
        self.__lineEdit = l
    
    def getLineEdit(self) -> QLineEdit:
        return self.__lineEdit