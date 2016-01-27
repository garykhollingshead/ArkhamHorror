# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import pyqtSignature
from xml.dom.minidom import Document

from Ui_xml_data_creator import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        This is called when the user clicks the save button.  This then figures
        out which tab the user is on and then calls the proper method to save
        the tabs xml data.
        """
        tabIndex = self.tabWidget.currentIndex()
        tabName = self.tabWidget.tabText(tabIndex)
        
        if(str(tabName) == "Ancient One"):
            self.ancientOne()
        
        
        
    def ancientOne(self):
        """"
        This will save all the Ancient One's xml data.
        """
        doc = Document()
        
        #create the root level element
        root = doc.createElement("ancientone")
        
        #create first level elements (sube elements to root element)
        name = doc.createElement("name") 
        title = doc.createElement("title")
        combatRating = doc.createElement("combatrating")
        doomTrack = doc.createElement("doomtrack")
        worshipers = doc.createElement("worshipers")
        defence = doc.createElement("defence")
        power = doc.createElement("power")
        attack = doc.createElement("attack")
        
        #create second level elements.  Will attack to first level elements.
        
        worshipersDescription = doc.createElement("description")
        worshipersType = doc.createElement("type")
        worshipersMods = doc.createElement("mods")
        powerName = doc.createElement("name")
        powerDescription = doc.createElement("description")
 
        #time to put the basic structure together
        doc.appendChild(root)
        root.appendChild(name)
        root.appendChild(title)
        root.appendChild(combatRating)
        root.appendChild(doomTrack)
        root.appendChild(worshipers)
        root.appendChild(defence)
        root.appendChild(power)
        root.appendChild(attack)
        
        worshipers.appendChild(worshipersDescription)
        worshipers.appendChild(worshipersMods)
        worshipers.appendChild(worshipersType)
        power.appendChild(powerName)
        power.appendChild(powerDescription)
        
        #now that the structure is all there, we need to get the values.
        nameTxt = doc.createTextNode(str(self.txtAncientOneName.displayText()))
        titleTxt = doc.createTextNode(str(self.txtAncientOneTitle.displayText()))
        combatRatingTxt = doc.createTextNode(str(self.txtAncientOneCombatRating.displayText()))
        
        
        name.appendChild(nameTxt)
        
        
      
        print doc.toprettyxml(indent="  ")
        
