from qgis.PyQt.QtGui import QValidator

class NotEmptyValidator(QValidator):
    def validate(self, text, pos):
        if text.strip():
            state = QValidator.Acceptable
        else:
            state = QValidator.Intermediate
        return state, text, pos