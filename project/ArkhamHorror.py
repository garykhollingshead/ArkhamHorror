import sys
"""
This test is meant to be run from the Project folder!
"""
#sys.path.append('../project')
sys.path.append('../tests')
sys.path.append('../GuiProject')

import mainwindow
import Environment
import os
import XmlLoader
import CharSelect
import Deck
import PlayerCharacter
import EnvMap
import ChooseListDialog
from PyQt4.QtGui import *
from PyQt4.QtCore import *
                        
"""Load Characters"""
app = QApplication(sys.argv)
info = [0, "new"]
mainwindow.DisplayMainMenu(app, info)


Environment = Environment.Environment()

Environment.NumOfPlayers=info[0]
Environment.SetupPhase()


#mainwindow.DisplayMainMenu(Environment)


EnvMap.ShowMap(app, Environment)



