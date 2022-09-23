# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MohidPlugin
                                 A QGIS plugin
 QGIS plugin for the MOHID model
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2021 by MARETEC
        email                : vasco.guita@tecnico.ulisboa.pt
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
import json

# Initialize Qt resources from file resources.py
from mohid_qgis.plugin.resources.resources import *

# Import the code for the DockWidget
from mohid_qgis.plugin.base.mohid_qgis_dockwidget import MohidPluginDockWidget
from mohid_qgis import settings
import os.path

import logging
import logging.config

logging.config.dictConfig(settings.LOGGING)

logger = logging.getLogger(__name__)

"""
The MohidPlugin is the main class of the plugin.
It was generated with the PBT tool and the only functions that matter to the programmer are:
    - run: function that runs when the user opens the plugin. This function composes the Grid Tool,
    with objects that handle the fields of the Grid Tool interface.
    - onClosePlugin: function that is called when the user closes the plugin. This function is
    useful to deactivate the CapturePointTool if it is active when the user closes the plugin.
"""
class MohidPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        # debug

        debug = False
        waitForAttach = True

        if debug:
            import debugpy
            debugpy.listen(address=("localhost", 8765))
            if waitForAttach:
                debugpy.wait_for_client()
                # debugpy.breakpoint()

        # Save reference to the QGIS interface
        # time.sleep(10)
        logger.debug("MohidPlugin init")
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MohidPlugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&MOHID')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MohidPlugin')
        self.toolbar.setObjectName(u'MohidPlugin')

        # print "** INITIALIZING MohidPlugin"

        self.pluginIsActive = False
        self.loadedBatLayers = {}
        self.dockWidget = None
        pluginDir = self.getPluginDir()
        with open(pluginDir + '/config.json') as f:
            self.loadConfig(f)
        # self.dockwidget = None

    # noinspection PyMethodMayBeStatic

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MohidPlugin', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        logger.debug("MohidPlugin initGui")
        icon_path = ':/plugins/mohid_qgis/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'MOHID plugin'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True
    # --------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # print "** CLOSING MohidPlugin"

        # disconnects
        self.dockWidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        # gridTool = self.getGridTool()
        # gridTool.close()
        # TODO: write unload functions for each tab
        # this way future tabs dont need to touch this file
        # for tab in tabs:
            #tab.unload()

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        # print "** UNLOAD MohidPlugin"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MOHID'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
            
    # --------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""
        if not self.dockWidget:
            self.dockWidget = MohidPluginDockWidget(self.iface, 
                                            self.dockWidget, self.getConfig())
        # if self.first_start == True:
        #     self.first_start = False
        #     # Create the dockwidget (after translation) and keep reference
        #     self.dockwidget = MohidPluginDockWidget()

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # print "** STARTING MohidPlugin"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            
            # connect to provide cleanup on closing of dockwidget
            self.dockWidget.closingPlugin.connect(self.onClosePlugin)

            
            
            
            
            # time.sleep(20)
            # self.batTool = BathymetryTool(self.dockwidget, self.loadedBatLayers)
            # self.dockwidget.bat_fsBrowser.clicked.connect(self.batLoadClicked)
            # self.batTool.setIface(self.iface)
            
            # Update bathymetry combobox when bathymetry layer changes
            # QgsMapCanvas.layersChanged.connect(self.batTool.updatebatComboBox)
            # self.iface.legendInterface().currentLayerChanged.connect(test)
            # gridTool = GridTool(form, self.dockwidget.pushButtonPreview, self.dockwidget.pushButtonLoad, self.dockwidget.pushButtonSave, config)
            # self.setGridTool(gridTool)
            
            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
            # self.dockwidget.show()
    
    # def batLoadClicked(self):
    #     logger.debug("Pressed load button")
        
    # def setGridTool(self, t: GridTool):
    #     self.__gridTool = t
    
    # def getGridTool(self) -> GridTool:
    #     return self.__gridTool

    def getPluginDir(self) -> str:
        return self.plugin_dir
    
    def setConfig(self, c: dict):
        self.__config = c
    
    def getConfig(self) -> dict:
        return self.__config

    def loadConfig(self, f):
        c = json.load(f)
        self.setConfig(c)