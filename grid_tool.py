from qgis.PyQt.QtWidgets import QPushButton
from .grid_form import GridForm
from qgis.core import QgsProject, Qgis, QgsMessageLog
from .grid import Grid

class GridTool:
    def __init__(self, f: GridForm, previewBtn: QPushButton, loadBtn: QPushButton, saveBtn: QPushButton):
        QgsMessageLog.logMessage("GridTool: initiating", 'MOHID plugin', level=Qgis.Info)
        self.setForm(f)
        self.setPreviewBtn(previewBtn)
        self.setLoadBtn(loadBtn)
        self.setSaveBtn(saveBtn)

    def setForm(self, f: GridForm):
        QgsMessageLog.logMessage("GridTool: set form", 'MOHID plugin', level=Qgis.Info)
        f.filled.connect(self.formFilled)
        self.__form = f
    
    def getForm(self) -> GridForm:
        QgsMessageLog.logMessage("GridTool: get form", 'MOHID plugin', level=Qgis.Info)
        return self.__form
    
    def setPreviewBtn(self, b: QPushButton):
        QgsMessageLog.logMessage("GridTool: set previewBtn", 'MOHID plugin', level=Qgis.Info)
        b.clicked.connect(self.previewBtnClicked)
        self.__previewBtn = b
    
    def getPreviewBtn(self) -> QPushButton:
        QgsMessageLog.logMessage("GridTool: get previewBtn", 'MOHID plugin', level=Qgis.Info)
        return self.__previewBtn
    
    def setLoadBtn(self, b: QPushButton):
        QgsMessageLog.logMessage("GridTool: set loadBtn", 'MOHID plugin', level=Qgis.Info)
        b.clicked.connect(self.loadBtnClicked)
        self.__loadBtn = b
    
    def getLoadBtn(self) -> QPushButton:
        QgsMessageLog.logMessage("GridTool: get loadBtn", 'MOHID plugin', level=Qgis.Info)
        return self.__loadBtn
    
    def setSaveBtn(self, b: QPushButton):
        QgsMessageLog.logMessage("GridTool: set saveBtn", 'MOHID plugin', level=Qgis.Info)
        b.clicked.connect(self.saveBtnClicked)
        self.__saveBtn = b
    
    def getSaveBtn(self) -> QPushButton:
        QgsMessageLog.logMessage("GridTool: get saveBtn", 'MOHID plugin', level=Qgis.Info)
        return self.__saveBtn

    def formFilled(self, filled: bool):
        QgsMessageLog.logMessage("GridTool: form filled", 'MOHID plugin', level=Qgis.Info)
        previewBtn = self.getPreviewBtn()
        previewBtn.setEnabled(filled)

        saveBtn = self.getSaveBtn()
        saveBtn.setEnabled(filled)
    
    def previewBtnClicked(self):
        QgsMessageLog.logMessage("GridTool: previewBtn clicked", 'MOHID plugin', level=Qgis.Info)
        form = self.getForm()
        grid = form.toGrid()
        nameField = form.getLayerNameField()
        name = nameField.getText()
        project = QgsProject.instance()

        layers = project.mapLayersByName(name)
        if layers:
            for layer in layers:
                if layer.customProperty(Grid.MohidGridLayer):
                    grid.updateQgsVectorLayer(layer)
                    break
        else:
            layer = grid.toQgsVectorLayer(name)
            project.addMapLayer(layer)

    def loadBtnClicked(self):
        QgsMessageLog.logMessage("GridTool: loadBtn clicked", 'MOHID plugin', level=Qgis.Info)
        pass

    def saveBtnClicked(self):
        QgsMessageLog.logMessage("GridTool: saveBtn clicked", 'MOHID plugin', level=Qgis.Info)
        pass

    def close(self):
        f = self.getForm()
        f.close()