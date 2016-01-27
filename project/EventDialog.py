
import sys
from PyQt4 import QtCore, QtGui

class EventDialog(QtGui.QDialog):
    def informationMessage(self,Title,Text):    
        message = QtGui.QMessageBox(self)
        message.setText(Text)
        message.setWindowTitle(Title)
        message.setIcon(QtGui.QMessageBox.Information)
        message.addButton("Ok", QtGui.QMessageBox.AcceptRole)
        message.exec_()
        
class Window(QtGui.QDialog):
    def DoStuff(self,Title,Text):
        parent=None
        QtGui.QWidget.__init__(self, parent)
        self.ui = EventDialog()
        self.ui.informationMessage(Title,Text)

def Run(Title,Text):
    window = Window()
    window.DoStuff(Title,Text)

