"""
Used for selecting an item from a list

Passed the custom dialog box's title and text along with a list.

returns the string back to environment.

"""



import sys
from PyQt4 import QtCore, QtGui

class ArkhamDialog(QtGui.QDialog):
    def questionMessage(self,Title,Text,List):    
        message = QtGui.QMessageBox(self)
        message.setText(Text)
        message.setWindowTitle(Title)
        message.setIcon(QtGui.QMessageBox.Question)
        message.addButton("Ok", QtGui.QMessageBox.AcceptRole)
        combo = QtGui.QComboBox(message)
        combo.setGeometry(QtCore.QRect(5, 45, 149, 30))
        combo.addItems( List )
        message.exec_()
        retval = combo.currentText()
        return str(retval)
        
        


class Window(QtGui.QDialog):
    def DoStuff(self,Title,Text,List):
        parent=None
        QtGui.QWidget.__init__(self, parent)
        self.ui = ArkhamDialog()
        return self.ui.questionMessage(Title,Text,List)


def Run(Title,Text,List):
    #app = QtGui.QApplication(sys.argv)
    window = Window()
    return window.DoStuff(Title,Text,List)
