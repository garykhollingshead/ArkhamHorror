import random
from PyQt4 import QtCore, QtGui
import sys



class Ui_SelectAnElement(object):
    def setupUi(self, app, SelectAnElement, Text, List):
        self.List = List
        self.MessageText = Text
        self.ListIndex = 0
        self.SelectAnElement = SelectAnElement
        self.app = app
        SelectAnElement.setObjectName("SelectAnElement")
        SelectAnElement.resize(549, 628)
        self.SelectedPicture = QtGui.QLabel(SelectAnElement)
        self.SelectedPicture.setGeometry(QtCore.QRect(20, 10, 501, 531))
        self.SelectedPicture.setObjectName("SelectedPicture")
        
        self.NextItem = QtGui.QPushButton(SelectAnElement)
        self.NextItem.setGeometry(QtCore.QRect(310, 550, 71, 61))
        self.NextItem.setObjectName("NextItem")
        self.NextItem.setAutoDefault(False)
        self.Select = QtGui.QPushButton(SelectAnElement)
        self.Select.setGeometry(QtCore.QRect(230, 550, 71, 61))
        self.Select.setObjectName("Select")
        self.Select.setAutoDefault(True)
        self.PreviousItem = QtGui.QPushButton(SelectAnElement)
        self.PreviousItem.setGeometry(QtCore.QRect(150, 550, 71, 61))
        self.PreviousItem.setObjectName("PreviousItem")
        self.PreviousItem.setAutoDefault(False)
        self.RandomButton = QtGui.QPushButton(SelectAnElement)
        self.RandomButton.setGeometry(QtCore.QRect(10, 590, 75, 23))
        self.RandomButton.setObjectName("RandomButton")
        self.RandomButton.setAutoDefault(False)

        MediumFont = QtGui.QFont()
        MediumFont.setFamily("Times New Roman")
        MediumFont.setPointSize(12)
        
        self.Message = QtGui.QLabel(SelectAnElement)
        self.Message.setGeometry(QtCore.QRect(400,550,150,61))
        self.Message.setWordWrap(1)
        self.Message.setObjectName("Message")
        self.Message.setFont(MediumFont)

        self.retranslateUi(SelectAnElement)
        QtCore.QMetaObject.connectSlotsByName(SelectAnElement)

        
        QtCore.QObject.connect(self.NextItem, QtCore.SIGNAL("clicked()"), self.NextElement)
        QtCore.QObject.connect(self.PreviousItem, QtCore.SIGNAL("clicked()"), self.PrevElement)
        QtCore.QObject.connect(self.Select, QtCore.SIGNAL("clicked()"), self.CloseMe)
        QtCore.QObject.connect(self.RandomButton, QtCore.SIGNAL("clicked()"), self.RandomElement)

        self.UpdatePicture()
        

    def retranslateUi(self, SelectAnElement):
        SelectAnElement.setWindowTitle(QtGui.QApplication.translate("SelectAnElement", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.NextItem.setText(QtGui.QApplication.translate("SelectAnElement", "->", None, QtGui.QApplication.UnicodeUTF8))
        self.Select.setText(QtGui.QApplication.translate("SelectAnElement", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.PreviousItem.setText(QtGui.QApplication.translate("SelectAnElement", "<-", None, QtGui.QApplication.UnicodeUTF8))
        self.RandomButton.setText(QtGui.QApplication.translate("SelectAnElement", "Random", None, QtGui.QApplication.UnicodeUTF8))
        self.Message.setText(self.MessageText)

    def UpdatePicture(self):
        self.Element = self.List[self.ListIndex]
        self.SelectedPicture.setPixmap(QtGui.QPixmap(self.Element.Picture).scaledToHeight(530))
        self.FINALANSWER = self.Element
        

    def NextElement(self):
        
        self.ListIndex = self.ListIndex + 1
        if(self.ListIndex >= len(self.List)):
            self.ListIndex = 0
        
        self.UpdatePicture()

    def PrevElement(self):
        
        self.ListIndex = self.ListIndex - 1
        if(self.ListIndex < 0):
            self.ListIndex = len(self.List) - 1
        
        self.UpdatePicture()

    def RandomElement(self):
        
        self.ListIndex = random.randrange(0,len(self.List))
        self.UpdatePicture()

    def CloseMe(self):
        self.SelectAnElement.close()
        self.app.exit()



class Window(QtGui.QWidget):
    def DoStuff(self, app,Text,  List):
        parent=None        
        QtGui.QWidget.__init__(self, parent)        
        self.ui = Ui_SelectAnElement()        
        self.ui.setupUi(app, self, Text, List)
        

def browseList(Text, List):
    MyEventLoop = QtCore.QEventLoop()    
    window = Window()   
    window.DoStuff(MyEventLoop, Text, List)    
    window.show()    
    MyEventLoop.exec_ ()    
    return window.ui.FINALANSWER



