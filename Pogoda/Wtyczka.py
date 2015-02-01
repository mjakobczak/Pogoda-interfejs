# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Wtyczka
                                 A QGIS plugin
 Wtyczka
                              -------------------
        begin                : 2015-01-06
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Marta Jakóbczak
        email                : jakobczakmarta@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py

# Import the code for the dialog
from Wtyczka_dialog import WtyczkaDialog
import urllib
import json
import os.path, time
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication,QVariant
from PyQt4.QtGui import QAction, QIcon
from qgis.core import *
from pprint import pprint
import urllib
import json
import os.path, time
import sys
import os
from PyQt4 import  QtCore, QtGui
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication,QVariant
from PyQt4.QtGui import QAction, QIcon
from qgis.core import *

from pprint import pprint

difference=0
jsonPath="C:\Users\Marta\Desktop\WTYCZKA QGIS+interfejs\weather.json"

        


        
class Wtyczka:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Wtyczka_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = WtyczkaDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Wtyczka')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Wtyczka')
        self.toolbar.setObjectName(u'Wtyczka')
        self.w=QtGui.QWidget()
        
        
        
        
    def pogoda(self, iface):
        if difference<-600:
            answer = json.load(urllib.urlopen("http://api.openweathermap.org/data/2.5/group?id=3093133,3088972,3089578,756867,3103709,3080251,759123,3087497,3094170,3080414,3093902,3082197,3085978,3093066,763111&units=metric"))
            with open(jsonPath, 'w') as outfile:
                json.dump(answer, outfile)
            print "Updating JSON weather file"
        else:
            print "Wait for 10 minutes!"


        weatherJson = json.loads(open(jsonPath).read())
        #pprint(weatherJson)

        layer1=QgsVectorLayer("C:\Users\Marta\Desktop\WTYCZKA QGIS+interfejs/powiaty_lodzkie.shp", "Dane", "ogr")
        layer=QgsVectorLayer("C:\Users\Marta\Desktop\WTYCZKA QGIS+interfejs/powiaty_lodzkie.shp", "Podklad", "ogr")
        #QgsMapLayerRegistry.instance().addMapLayer(layer)
        layer1.startEditing()
        layer.startEditing()
        layer1.loadNamedStyle("layerMoj.qml")
        layer.loadNamedStyle("layerPODKL.qml")
        #layer.LayerData=layer.dataProvider()
        #layer.LayerData.addAttributes


        #attributes=["TEMP","TEMP_MAX","TEMP_MIN", "PRESSURE","HUMIDITY","WIND_SPEED","WIND_ANGLE","CLOUDS","CITY_NAME"]
        attributes=["MOJ_ATR"]
        for i in attributes:
            if layer.dataProvider().fieldNameIndex(i)==-1:
                layer.dataProvider().addAttributes([QgsField(i,QVariant.Double)])
        layer.updateFields()


        cities=weatherJson['list']
        print len(cities), 'dlugosc'
            


            
        for i in range(0, len(cities)):
            
            temp=cities[i]['main']['temp']
            tempMax=cities[i]['main']['temp_max']
            tempMin=cities[i]['main']['temp_min']
            pressure=cities[i]['main']['pressure']
            humidity=cities[i]['main']['humidity']
            windSpeed=cities[i]['wind']['speed']
            windAngle=cities[i]['wind']['deg']
            clouds=cities[i]['clouds']['all']
            cityName=cities[i]['name']
            longitude=cities[i]['coord']['lon']
            latitude=cities[i]['coord']['lat']
            #attributesValues=[temp, tempMax, tempMin, pressure, humidity, windSpeed, windAngle,clouds,cityName]
            if self.rb1.isChecked():
                self.attributesValues=[temp]
            elif self.rb2.isChecked():
                self.attributesValues=[tempMax]
            elif self.rb3.isChecked():
                self.attributesValues=[tempMin]
            elif self.rb4.isChecked():
                self.attributesValues=[pressure]
            elif self.rb5.isChecked():
                self.attributesValues=[humidity]
            elif self.rb6.isChecked():
                self.attributesValues=[windSpeed]
            elif self.rb7.isChecked():
                self.attributesValues=[windAngle]
            elif self.rb8.isChecked():
                self.attributesValues=[clouds]
                

            print(self.attributesValues)
            print "longitude", longitude
            print "latitude", latitude
            
            point=QgsPoint(longitude,latitude)
            for region in layer.getFeatures():
                    if region.geometry().contains(QgsGeometry.fromPoint(point)):
                        for i in xrange(0, len(attributes)):
                            region.setAttribute(attributes[i], self.attributesValues[i])
                        layer.updateFeature(region)
            
        layer.commitChanges()
        layer1.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(layer1)
        QgsMapLayerRegistry.instance().addMapLayer(layer)
    
    
    
    
    
    
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
        return QCoreApplication.translate('Wtyczka', message)


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

        icon_path = ':/plugins/Wtyczka/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Wtyczka'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Wtyczka'),
                action)
            self.iface.removeToolBarIcon(action)


   

    def run(self):
        """Run method that performs all the real work"""


        print "last modified: %s" % time.ctime(os.path.getmtime(jsonPath))


        now = time.time()
        later =os.path.getmtime(jsonPath)
        difference = int(later - now)
        print "difference: %d"
        print difference

        obraz=QtGui.QPixmap("C:\Users\Marta\Desktop\WTYCZKA QGIS+interfejs\pic.jpg","png")
        self.w.resize (300,420)
        self.w.setWindowTitle('Pogoda Lodzkie')



        self.b=QtGui.QPushButton("Sprawdz",self.w)
        self.b.resize(150,50)
        self.b.move(80,350)

        label=QtGui.QLabel("moj label",self.w)
        label.move(80,20)
        label.resize(150,150)
        label.setScaledContents(True)
        label.setPixmap(obraz)

        self.rb1=QtGui.QRadioButton("Temperatura",self.w)
        self.rb1.move (80,180)

        self.rb2=QtGui.QRadioButton("Temperatura maksymalna",self.w)
        self.rb2.move (80,200)

        self.rb3=QtGui.QRadioButton("Temperatura minimalna",self.w)
        self.rb3.move (80,220)

        self.rb4=QtGui.QRadioButton("Cisnienie atmosferyczne",self.w)
        self.rb4.move (80,240)

        self.rb5=QtGui.QRadioButton("Wilgotnosc ",self.w)
        self.rb5.move (80,260)

        self.rb6=QtGui.QRadioButton("Predkosc wiatru ",self.w)
        self.rb6.move (80,280)

        self.rb7=QtGui.QRadioButton("Kierunek wiatru ",self.w)
        self.rb7.move (80,300)

        self.rb8=QtGui.QRadioButton("Informacje o chmurach ",self.w)
        self.rb8.move (80,320)


        self.b.clicked.connect(self.pogoda)
        self.w.show()


        pass


