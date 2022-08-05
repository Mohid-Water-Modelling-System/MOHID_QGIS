import os

from qgis.PyQt import uic
from PyQt5.QtWidgets import QTabWidget

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QPushButton, QFileDialog
from qgis.core import QgsProject
from .mohidBathymetry import MOHIDBathymetry

from mohid_qgis.core.utils.gridConverter import grid2shp
from mohid_qgis.core.utils.polygonConverter import polygon2shp
from mohid_qgis.core.utils.xyzConverter import XYZ2shp
from mohid_qgis.core.utils.bathymetryConverter import MOHIDBathymetry2shp, saveToMohidFile, \
    saveGenerateMohidFile
import logging

logger = logging.getLogger(__name__)

CRS_ID_DEFAULT = 4326

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tab_load.ui'))

class LoadTab(QTabWidget, FORM_CLASS):

    def __init__(self, iface) -> None:
        super().__init__()
        logger.debug("Load tab init")
        # Setup UI elements
        self.setupUi(self)

        self.iface = iface
        # Connect signals
        # self.bat_fsGrid.clicked.connect(self.openGridBrowser)
        self.bat_loadGrdBtn.clicked.connect(self.loadGridToLayer)
        # self.bat_removeGrdBtn.clicked.connect(self.removeGridLayer)

        # self.bat_fsXYZ.clicked.connect(self.openXYZBrowser)
        self.bat_loadXYZBtn.clicked.connect(self.loadXYZToLayer)
        # self.bat_removeXYZBtn.clicked.connect(self.removeXYZLayer)

        # self.bat_fsLand.clicked.connect(self.openLandBrowser)
        self.bat_loadLandBtn.clicked.connect(self.loadLandToLayer)
        # self.bat_removeLandBtn.clicked.connect(self.removeLandLayer)

        # self.bat_fsOutput.clicked.connect(self.openGenerateBrowser)
        # self.bat_generateBtn.clicked.connect(self.generateBatMohidFile)

        # self.bat_fsBat.clicked.connect(self.openBatBrowser)
        self.bat_loadBatBtn.clicked.connect(self.loadBatToLayer)
        self.bat_saveBatBtn.clicked.connect(self.saveBatToMohidFile)
        self.loadedBatLayers = {}     

    def loadGridToLayer(self):
        logger.debug("Pressed Grid Load button")
        file = QFileDialog.getOpenFileName(None, 'Load MOHID Grid file', 
                            filter='Mohid file (*.grd)')[0]
        # for file in filepaths:
            # TODO: Verify is layer is already loaded
            # Add item to item tree
            # item = QTreeWidgetItem(self.bat_gridTree)
            # item.setText(0, os.path.basename(file))
            # item.setText(1, file)

            # Load grid layer
        logger.debug(f"Loading {file}")
        if file != "":
            # check file type

            # Convert grid to shapefile
            shpPath = grid2shp(file)
            if not shpPath:
                return
            # shpPath = self.bat_gridPath.text().split(".")[0] + ".shp"
            filename = os.path.basename(shpPath).split(".")[0]
            vlayer = self.iface.addVectorLayer(shpPath, f"MOHID Grid - {filename}", "ogr")
            
            if not vlayer:
                logger.warning("Grid layer failed to load")
            else:
                crs = vlayer.crs()
                crs.createFromId(CRS_ID_DEFAULT) 
                vlayer.setCrs(crs)
        else:
            logger.debug(f"Filename is empty")

    def loadXYZToLayer(self):
        """
        .xyz file contents:
        latitude longitude attribute
        <begin_xyz>
        -8.7500838888889    38.4880172222222    0.820
        <end_xyz>
        """
        logger.debug("Pressed XYZ Load button")
        file = QFileDialog.getOpenFileName(None, 'Load MOHID XYZ file', 
                            filter='Mohid file (*.xyz)')[0]
        # for file in filepaths:
            # TODO: Verify is layer is already loaded
            # Add item to item tree
            # item = QTreeWidgetItem(self.bat_xyzTree)
            # item.setText(0, os.path.basename(file))
            # item.setText(1, file)

        logger.debug(f"Loading {file}")
        
        if file != "":
            # check file type

            shpPath = XYZ2shp(file)
            # shpPath = self.bat_XYZPath.text().split(".")[0] + ".shp"
            filename = os.path.basename(shpPath).split(".")[0]
            vlayer = self.iface.addVectorLayer(shpPath, f"MOHID Points - {filename}", "ogr")

            if not vlayer:
                print("Layer failed to load!")
            else:
                crs = vlayer.crs()
                crs.createFromId(CRS_ID_DEFAULT) 
                vlayer.setCrs(crs)
        else:
            logger.debug(f"Filename is empty")

    def loadLandToLayer(self):

        logger.debug("Pressed Land Load button")
        file = QFileDialog.getOpenFileName(None, 'Load MOHID Land file', 
                            filter='Mohid file (*.xy)')[0]
        # for file in filepaths:
            # TODO: Verify is layer is already loaded
            # Add item to item tree
            # item = QTreeWidgetItem(self.bat_landTree)
            # item.setText(0, os.path.basename(file))
            # item.setText(1, file)

        logger.debug(f"Loading {file}")
        if file != "":
            # check file type

            shpPath = polygon2shp(file)
            filename = os.path.basename(shpPath).split(".")[0]
            vlayer = self.iface.addVectorLayer(shpPath, f"MOHID Land - {filename}", "ogr")
            
            if not vlayer:
                print("Layer failed to load!")
            else:
                crs = vlayer.crs()
                crs.createFromId(CRS_ID_DEFAULT) 
                vlayer.setCrs(crs)
        else:
            logger.debug(f"Filename is empty")
    
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

        gridPath = self.bat_gridPath.text()
        xyzPath = self.bat_XYZPath.text()
        landPath = self.bat_landPath.text()

        DTCdir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                            '../..',
                                            'core/Digital_Terrain_Creator/'))
        DTCOptionsPath = os.path.join(DTCdir, "CreateBathymetry.dat")
        # TODO: get options
        # Generate CreateBathymetry.dat options file
        if gridPath and xyzPath:
            saveGenerateMohidFile(DTCOptionsPath, batPath, gridPath, xyzPath, landPath)
        else:
            logger.debug("Can't generate bathymetry, missing files")

        if os.path.exists(DTCOptionsPath):
            # Run DTC tool
            logger.debug("Running DTC")
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
                MOHIDBathymetry2shp(filepath, bat.gridData)
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
                data2D.append(feat.attributes()[0])
            bat.gridData['DATA_2D'] = data2D
            saveToMohidFile(filepath, bat.gridData)

        else:
            logger.debug(f"Filename is empty")
    
    def updatebatComboBox(self):

        pass
        # for layer in QgsProject.instance().mapLayers().values():
        #     if layer.name().startswith("MOHID Bathymetry"):
        #         self.bat_layerComboBox.addItem(layer.name(), layer)
        # QgsProject.instance().mapLayersByName("Mohid")
    
    def convert(self, input, convertFunction, output=None,):

        if output is None:
            # TODO: check if convertFunctions needs outputh path
            convertFunction(input)
        else:
            return convertFunction(input)

    def loadLayer(self):
        raise NotImplementedError