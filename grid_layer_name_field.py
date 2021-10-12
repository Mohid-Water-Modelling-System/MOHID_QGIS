from qgis.PyQt.QtWidgets import QLineEdit, QToolButton
from qgis.PyQt.QtCore import QObject, pyqtSignal
from .not_empty_validator import NotEmptyValidator

class GridLayerNameField(QObject):
    filled = pyqtSignal(bool)

    def __init__(self, l: QLineEdit, b: QToolButton):
        super().__init__()
        self.setLineEdit(l)
        self.setButton(b)

    def setLineEdit(self, l: QLineEdit):
        validator = NotEmptyValidator(l)
        l.setValidator(validator)
        l.textChanged.connect(self.lineEditTextChanged)
        self.__lineEdit = l

    def getLineEdit(self) -> QLineEdit:
        return self.__lineEdit

    def setButton(self, b: QToolButton):
        self.__button = b

    def getButton(self) -> QToolButton:
        return self.__button

    def lineEditTextChanged(self):
        filled = self.isFilled()
        self.filled.emit(filled)

    def isFilled(self) -> bool:
        l = self.getLineEdit()
        filled = l.hasAcceptableInput()
        return filled

    def getText(self) -> str:
        l = self.getLineEdit()
        text = l.text()
        return text
