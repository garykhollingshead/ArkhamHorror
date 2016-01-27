

from PyQt4 import QtCore, QtGui


    
class Ui_ViewCard(object):
    def setupUi(self, app, ViewCard, Card):
        self.Card = Card
        self.app = app
        self.ViewCard = ViewCard
        ViewCard.setObjectName("Dialog")
        ViewCard.resize(407, 557)
        self.Picture = QtGui.QLabel(ViewCard)
        self.Picture.setGeometry(QtCore.QRect(20, 10, 361, 501))
        self.Picture.setObjectName("Picture")
        self.OkayButton = QtGui.QPushButton(ViewCard)
        self.OkayButton.setGeometry(QtCore.QRect(310, 520, 75, 23))
        self.OkayButton.setObjectName("OkayButton")
        
        
        self.retranslateUi(ViewCard)
        QtCore.QObject.connect(self.OkayButton, QtCore.SIGNAL("clicked()"), self.CloseMe)
        QtCore.QMetaObject.connectSlotsByName(ViewCard)

    def retranslateUi(self, ViewCard):
        ViewCard.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.Picture.setPixmap(QtGui.QPixmap(self.Card[2]).scaledToHeight(500))
        self.OkayButton.setText(QtGui.QApplication.translate("Dialog", "Okay", None, QtGui.QApplication.UnicodeUTF8))

    def CloseMe(self):
        self.ViewCard.close()
        self.app.exit()

    

class Window(QtGui.QDialog):
    def DoStuff(self, app, Card):
        parent=None
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ViewCard()
        self.ui.setupUi(app, self, Card)

    
def viewCard(card):
    import sys
    MyEventLoop = QtCore.QEventLoop()
    window = Window()
    window.DoStuff(MyEventLoop, card)
    window.show()
    MyEventLoop.exec_ ()
