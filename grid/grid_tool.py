from qgis.PyQt.QtWidgets import QPushButton, QFileDialog
from .grid_form import GridForm
from qgis.core import QgsProject
from .grid import Grid
import os.path

"""
The GridTool class manages the tool of the mohid_qgis plugin for creating and visualizing MOHID grids.
"""
class GridTool:
    """
    The constructor of the GridTool receives:
        - a form for the user to enter the properties of the grid to create
        - a button to visualize the grid in the map
        - a button for loading a grid from a file
        - a button for saving a grid to a file
        - a configuration provided in form of a dictionary. This configuration was previously read from the config.json file
        and is used to read and write grids according to the MOHID format.
    """
    def __init__(self, f: GridForm, previewBtn: QPushButton, loadBtn: QPushButton, saveBtn: QPushButton, config: dict):
        self.setForm(f)
        self.setPreviewBtn(previewBtn)
        self.setLoadBtn(loadBtn)
        self.setSaveBtn(saveBtn)
        self.setConfig(config)

    """
    The Form setter receives a GridForm object and connects its "filled"
    signal to the formFilled function.
    When the fields in the grid form are changed, the fieldFilled function is called.
    """
    def setForm(self, f: GridForm):
        f.filled.connect(self.formFilled)
        self.__form = f
    
    def getForm(self) -> GridForm:
        return self.__form
    
    """
    The preview button setter receives a QPushButton object and connects its clicked signal
    to the previewBtnClicked function.
    When the preview button is clicked, the previewBtnClicked function is called.
    """
    def setPreviewBtn(self, b: QPushButton):
        b.clicked.connect(self.previewBtnClicked)
        self.__previewBtn = b
    
    def getPreviewBtn(self) -> QPushButton:
        return self.__previewBtn
    
    """
    The load button setter receives a QPushButton object and connects its clicked signal
    to the loadBtnClicked function.
    When the load button is clicked, the loadBtnClicked function is called.
    """
    def setLoadBtn(self, b: QPushButton):
        b.clicked.connect(self.loadBtnClicked)
        self.__loadBtn = b
    
    def getLoadBtn(self) -> QPushButton:
        return self.__loadBtn
    
    """
    The save button setter receives a QPushButton object and connects its clicked signal
    to the saveBtnClicked function.
    When the save button is clicked, the saveBtnClicked function is called.
    """
    def setSaveBtn(self, b: QPushButton):
        b.clicked.connect(self.saveBtnClicked)
        self.__saveBtn = b
    
    def getSaveBtn(self) -> QPushButton:
        return self.__saveBtn
    
    def setConfig(self, c: dict):
        self.__config = c
    
    def getConfig(self) -> dict:
        return self.__config

    """
    The formFilled function is called when the form changes.
    The "filled" argument is a boolean that tells whether properties
    of the form are acceptable for creating a grid.
    If they are the preview and save buttons are enabled, otherwise they are disabled and the user cannot click them. 
    """
    def formFilled(self, filled: bool):
        previewBtn = self.getPreviewBtn()
        previewBtn.setEnabled(filled)

        saveBtn = self.getSaveBtn()
        saveBtn.setEnabled(filled)
    
    """
    The previewBtnClicked function is called when the preview button is clicked.
    It creates a grid from the properties specified in the form.
    Then it reads the name entered in the layerNameField.
    If Qgis already has a layer with that name and it is a grid layer, this grid is updated with
    the new properties.
    If no layer is found with the specified name, a new layer is created to visualize the grid.
    """
    def previewBtnClicked(self):
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

    """
    The loadBtnClicked function is called when the load button is clicked.
    This function reads a MOHID grid from a file, fills the form and displays
    the grid on a layer.
    """
    def loadBtnClicked(self):
        filename = QFileDialog.getOpenFileName(None, 'Load grid', filter='*.dat')[0]
        if filename == "":
            return None
        grid = Grid()
        grid.fromGridFile(filename)
        name = os.path.basename(filename).replace(".dat", "")
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
    """
    The saveBtnClicked function is called when the save button is clicked.
    This function creates a grid from the properties entered in the form,
    Opens a dialog for the user to enter the destination file, writes the grid
    to the file in the MOHID format.
    The MOHID format is specified in the config dictionary.
    This configuration was previously read from the config.json file.
    """
    def saveBtnClicked(self):
        form = self.getForm()
        config = self.getConfig()
        grid = form.toGrid()
        nameField = form.getLayerNameField()
        name = nameField.getText()
        fileName = QFileDialog.getSaveFileName(None, 'Save grid', name +'.dat', '*.dat')[0]

        fmt = config["fmt"]
        key = config["keys"]["fileName"]
        output = fmt.format(key, os.path.splitext(fileName)[0] + ".grd") + grid.toString(config)

        #TODO: change to with context
        if fileName:
            with open(fileName, "w") as f:
                f.write(output)        
    """
    The close function deactivates the CapturePointTool.
    This function is called when the plugin is closed.
    """
    def close(self):
        f = self.getForm()
        f.close()