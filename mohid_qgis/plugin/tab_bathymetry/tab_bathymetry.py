import os

from qgis.PyQt import uic
from PyQt5.QtWidgets import QTabWidget, QTreeWidgetItem

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QPushButton, QFileDialog
from qgis.core import QgsProject
from ..mohid.batymetry import MOHIDBathymetry

from mohid_qgis.core.utils.gridConverter import grid2shp
from mohid_qgis.core.utils.polygonConverter import polygon2shp
from mohid_qgis.core.utils.xyzConverter import XYZ2shp
from mohid_qgis.core.utils.bathymetryConverter import MOHIDBathymetry2shp, saveToMohidFile, \
    saveGenerateMohidFile
from mohid_qgis.plugin.base.thread import ProgramThread
import logging

logger = logging.getLogger(__name__)

CRS_ID_DEFAULT = 4326

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tab_bathymetry.ui'))

class BathymetryTab(QTabWidget, FORM_CLASS):

    def __init__(self, iface, loadedBatLayers) -> None:
        super().__init__()
        logger.debug("Bathymetry tab init")
        # Setup UI elements
        self.setupUi(self)

        self.iface = iface
        # Connect signals
        self.bat_loadGrdBtn.clicked.connect(self.addGridToLayer)
        self.bat_removeGrdBtn.clicked.connect(self.removeGridLayer)

        self.bat_loadXYZBtn.clicked.connect(self.addXYZToLayer)
        self.bat_removeXYZBtn.clicked.connect(self.removeXYZLayer)

        self.bat_loadLandBtn.clicked.connect(self.addLandToLayer)
        self.bat_removeLandBtn.clicked.connect(self.removeLandLayer)

        self.bat_fsOutput.clicked.connect(self.openGenerateBrowser)
        self.bat_generateBtn.clicked.connect(self.generateBatMohidFile)

        self.bat_loadBatBtn.clicked.connect(self.loadBatToLayer)
        self.bat_saveBatBtn.clicked.connect(self.saveBatToMohidFile)
        QgsProject.instance().layersAdded.connect(self.updatebatComboBoxes)
        QgsProject.instance().layersRemoved.connect(self.updatebatComboBoxes)
        self.loadedBatLayers = loadedBatLayers  

    def addGridToLayer(self):
        logger.debug("Pressed Grid Add button")
        
        vlayer = self.bat_gridBox.currentData()
        if vlayer is not None:
            item = QTreeWidgetItem(self.bat_gridTree)
            item.setText(0, os.path.basename(vlayer.name()).replace("MOHID Grid - ", ""))
            item.setText(1, vlayer.source().replace(".shp", ".grd"))
    
    def removeGridLayer(self):

        selItems = self.bat_gridTree.selectedItems()
        # Check if any layer is selected
        if not selItems:
            # TODO: add message for no layers selected
            return
        # Invisible parent item
        root = self.bat_gridTree.invisibleRootItem()
        for item in selItems:
            # Remove item from item tree
            root.removeChild(item)

    def addXYZToLayer(self):
        """
        .xyz file contents:
        latitude longitude attribute
        <begin_xyz>
        -8.7500838888889    38.4880172222222    0.820
        <end_xyz>
        """
        logger.debug("Pressed XYZ Add button")
        
        vlayer = self.bat_XYZBox.currentData()
        if vlayer is not None:
            item = QTreeWidgetItem(self.bat_xyzTree)
            item.setText(0, os.path.basename(vlayer.name()).replace("MOHID Points - ", ""))
            item.setText(1, vlayer.source().replace(".shp", ".xyz"))
    
    def removeXYZLayer(self):

        selItems = self.bat_xyzTree.selectedItems()
        # Check if any layer is selected
        if not selItems:
            # TODO: add message for no layers selected
            return
        # Invisible parent item
        root = self.bat_xyzTree.invisibleRootItem()
        for item in selItems:
            # Remove item from item tree
            root.removeChild(item)

    def addLandToLayer(self):

        logger.debug("Pressed Land Add button")
        
        vlayer = self.bat_landBox.currentData()
        if vlayer is not None:
            item = QTreeWidgetItem(self.bat_landTree)
            item.setText(0, os.path.basename(vlayer.name()).replace("MOHID Land - ", ""))
            item.setText(1, vlayer.source().replace(".shp", ".xy"))
    
    def removeLandLayer(self):

        selItems = self.bat_landTree.selectedItems()
        # Check if any layer is selected
        if not selItems:
            # TODO: add message for no layers selected
            return
        # Invisible parent item
        root = self.bat_landTree.invisibleRootItem()
        for item in selItems:
            # Remove item from item tree
            root.removeChild(item)
    
    def openGenerateBrowser(self):
        # filepath = QFileDialog.getExistingDirectory(None, "Select output Directory")
        filepath = QFileDialog.getSaveFileName(None, 'Generate MOHID Bathymetry file', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        self.bat_outputPath.setText(filepath)

    def generateBatMohidFile(self):
        batPath = self.bat_outputPath.text()
        logger.debug(f"Saving bathymetry to {batPath}")
        
        if not batPath.endswith(".dat"):
            batPath = f"{batPath}.dat"

        gridPaths = []
        itemCtn = self.bat_gridTree.topLevelItemCount()
        logger.debug(f"Grid count: {itemCtn}")
        for id in range(0, itemCtn):
            gridPaths.append(self.bat_gridTree.topLevelItem(id).text(1))
        logger.debug(f"DTC grids: {gridPaths}")
        xyzPaths = []
        itemCtn = self.bat_xyzTree.topLevelItemCount()
        for id in range(0, itemCtn):
            xyzPaths.append(self.bat_xyzTree.topLevelItem(id).text(1))
        
        logger.debug(f"DTC xyz: {xyzPaths}")
        landPaths = []
        itemCtn = self.bat_landTree.topLevelItemCount()
        for id in range(0, itemCtn):
            landPaths.append(self.bat_landTree.topLevelItem(id).text(1))
        logger.debug(f"DTC land: {landPaths}")

        DTCdir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                            '../..',
                                            'core/Digital_Terrain_Creator/'))
        DTCOptionsPath = os.path.join(DTCdir, "CreateBathymetry.dat")
        # TODO: get options
        # Generate CreateBathymetry.dat options file
        if gridPaths and xyzPaths:
            saveGenerateMohidFile(DTCOptionsPath, batPath, gridPaths[0], xyzPaths, landPaths)
        else:
            logger.debug("Can't generate bathymetry, missing files")

        if os.path.exists(DTCOptionsPath):
            # Run DTC tool
            logger.debug("Running DTC...")
            self._runDigitalTerrain()

    def loadBatToLayer(self):
        
        logger.debug("Pressed bathymetry Load button")
        filepaths = QFileDialog.getOpenFileNames(None, 'Load MOHID Bathymetry files', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        # self.bat_batPath.setText(filepaths)
        logger.debug(f"Loading {filepaths}")
        for filepath in filepaths:
            if filepath != "":
                # check file type
                bat = MOHIDBathymetry(filepath)
                MOHIDBathymetry2shp(filepath, bat)
                shpPath = filepath.split(".")[0] + ".shp"
                vlayer = self.iface.addVectorLayer(
                                shpPath,
                                f"MOHID Bathymetry - {bat.filename}",
                                "ogr")
                if not vlayer:
                    print("Layer failed to load!")
                else:
                    stylePath = os.path.abspath(os.path.join(
                        os.path.dirname( __file__ ), 'bathymetry.qml'))
                    vlayer.loadNamedStyle(stylePath)
                    self.iface.layerTreeView().refreshLayerSymbology(vlayer.id())
                    crs = vlayer.crs()
                    crs.createFromId(CRS_ID_DEFAULT) 
                    vlayer.setCrs(crs)
                    self.loadedBatLayers[vlayer.name()] = bat

            else:
                logger.debug(f"Filename is empty")
    
    def saveBatToMohidFile(self):
        
        lyr = self.iface.activeLayer()
        if lyr.name() not in self.loadedBatLayers:
            logger.debug("No bathymetry to save")
            return
        bat = self.loadedBatLayers[lyr.name()]
        filepath = QFileDialog.getSaveFileName(None, 'Save MOHID Bathymetry file', 
                            filter='Mohid Bathymetry (*.dat)')[0]
        logger.debug(f"Will save to {filepath}")
        if filepath != "":
            
            # TODO: for now this is sufficient, but we should choose the layer 
            # from a comboBox
           
            data2D = []
            for feat in lyr.getFeatures():
                data2D.append(feat.attributes()[feat.fieldNameIndex("depth")])
            bat.gridData['DATA_2D'] = data2D
            saveToMohidFile(filepath, bat)

        else:
            logger.debug(f"Filename is empty")
    
    def updatebatComboBoxes(self):
        
        self.bat_gridBox.clear()
        self.bat_XYZBox.clear()
        self.bat_landBox.clear()
        # self.bat_bathyBox.clear()
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name().startswith("MOHID Grid"):
                self.bat_gridBox.addItem(layer.name(), layer)
            elif layer.name().startswith("MOHID Points"):
                self.bat_XYZBox.addItem(layer.name(), layer)
            elif layer.name().startswith("MOHID Land"):
                self.bat_landBox.addItem(layer.name(), layer)
            # elif layer.name().startswith("MOHID Bathymetry"):
            #     self.bat_bathyBox.addItem(layer.name(), layer)
        # QgsProject.instance().mapLayersByName("Mohid")
    
    def convert(self, input, convertFunction, output=None,):

        if output is None:
            # TODO: check if convertFunctions needs outputh path
            convertFunction(input)
        else:
            return convertFunction(input)

    def loadLayer(self):
        raise NotImplementedError

    def _runDigitalTerrain(self):
        # TODO: remove hardcoded configurations after implementing options solution
        # Check the other plugin to see how output is passed
        DTCpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
        '../..',
        'core/Digital_Terrain_Creator/DigitalTerrainCreator_release_double_x64.exe'))
        thread = ProgramThread(DTCpath)

        def on_output(out: str) -> None:
            logger.debug("on_output callback")
            # self.stdout_textarea.appendPlainText(out)
            # vert_scrollbar = self.stdout_textarea.verticalScrollBar()
            # vert_scrollbar.setValue(vert_scrollbar.maximum())

        def on_finished() -> None:
            # When lines come in fast, then the highlighter is not called on each line.
            # Re-highlighting at the end is a work-around to at least have correct
            # highlighting after program termination.
            # self.stdout_highlighter.rehighlight()
            logger.debug("on_finished callback")
            if thread.exc_info:
                # on_done(path, None)
                raise thread.exc_info[0].with_traceback(*thread.exc_info[1:])
            # on_done(path, thread.error)
        thread.output.connect(on_output)
        thread.finished.connect(on_finished)
        thread.start()
        # so that we can kill the program later if requested
        self.thread = thread