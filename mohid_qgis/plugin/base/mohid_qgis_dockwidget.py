# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MohidPluginDockWidget
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

import os
import json
from PyQt5.QtWidgets import QTabWidget, QDockWidget
from qgis.gui import QgisInterface
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from mohid_qgis.plugin.tab_bathymetry.tab_bathymetry import BathymetryTab
from mohid_qgis.plugin.tab_grid.tab_grid import GridTab

from ..utils import WhiteScroll

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'mohid_qgis_dockwidget_base.ui'))

"""
This class and this entire file was automatically generated with the PBT tool.
There should be no need to touch it or understand it.
"""
class MohidPluginDockWidget(QDockWidget):

    closingPlugin = pyqtSignal()

    def __init__(self, iface: QgisInterface, dockWidget: QDockWidget, config):
        """Constructor."""
        super(MohidPluginDockWidget, self).__init__("MOHID QGIS")
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        # self.setupUi(self)

        # Set up tabs
        tabs = QTabWidget()
        tabs.addTab(WhiteScroll(GridTab(iface, config)), "Grid")
        tabs.addTab(WhiteScroll(BathymetryTab(iface)), "Bathymetry")
        self.setWidget(tabs)
        self.tabs = tabs

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()