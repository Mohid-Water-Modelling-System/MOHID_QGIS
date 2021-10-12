from qgis.PyQt.QtGui import QValidator
from qgis.core import Qgis, QgsMessageLog

class NotEmptyValidator(QValidator):
    def validate(self, text, pos):
        QgsMessageLog.logMessage("NotEmptyValidator: validating", 'MOHID plugin', level=Qgis.Info)
        if text.strip():
            state = QValidator.Acceptable
        else:
            state = QValidator.Intermediate
        return state, text, pos