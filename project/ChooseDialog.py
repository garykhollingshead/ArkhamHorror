"""
by zack:

This is for choosing between two options.

All text is passed in and the response is returned all the
way back into Environment
"""

import sys
from PyQt4 import QtCore, QtGui

class ArkhamDialog(QtGui.QDialog):
    def questionMessage(self,Title,BodyText,Option1,Option2,Detailed):    
        message = QtGui.QMessageBox(self)
        message.setText( BodyText )
        message.setWindowTitle( Title )
        message.setIcon(QtGui.QMessageBox.Question)
        message.addButton(Option1, QtGui.QMessageBox.AcceptRole)
        message.addButton(Option2, QtGui.QMessageBox.RejectRole)
        message.setDetailedText(Detailed)
        message.exec_()
        response = message.clickedButton().text()
        if response == Option1 :
            return Option1
        elif response == Option2 :
            return Option2
        


class Window(QtGui.QDialog):
    def DoStuff(self,Title,BodyText,Option1,Option2,Detailed):
        parent=None
        QtGui.QWidget.__init__(self, parent)
        self.ui = ArkhamDialog()
        return self.ui.questionMessage(Title,BodyText,Option1,Option2,Detailed)


def Run(Title,BodyText,Option1,Option2,Detailed):
    #app = QtGui.QApplication(sys.argv)
    window = Window()
    return window.DoStuff(Title,BodyText,Option1,Option2,Detailed)

