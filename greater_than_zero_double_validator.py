from qgis.PyQt.QtGui import QDoubleValidator, QValidator
from qgis.PyQt.QtCore import QObject

class GreaterThanZeroDoubleValidator(QDoubleValidator):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.setBottom(0)

    def validate(self, text, pos):
        state, text, pos = super().validate(text, pos)
        if state == QValidator.Acceptable:
            if float(text) == 0:
                state = QValidator.Intermediate
        return state, text, pos
