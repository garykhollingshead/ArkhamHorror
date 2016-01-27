# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SingleDie.ui'
#
# Created: Mon Apr 12 14:42:01 2010
#      by: The PyQt User Interface Compiler (pyuic) 3.16
#
# WARNING! All changes made in this file will be lost!



from PyQt4 import QtCore, QtGui
import random
import sys
import os

class Ui_SingleDie(object):
    def setupUi(self, MyEventLoop, SingleDie):
        self.MyEventLoop = MyEventLoop
        self.SingleDie = SingleDie
        SingleDie.setObjectName("SingleDie")
        SingleDie.resize(487, 235)
        self.SingleDie = SingleDie
        self.Background = QtGui.QLabel(SingleDie)
        self.Background.setGeometry(QtCore.QRect(0,0,481, 231))
        self.Background.setObjectName("Background")
        self.Background.setPixmap(QtGui.QPixmap( self.FindItemPath() + "arkham_dice2.jpg"))

        self.RollButton = QtGui.QPushButton(SingleDie)
        self.RollButton.setGeometry(QtCore.QRect(210, 180, 75, 23))
        self.RollButton.setObjectName("RollButton")

        self.ExitButton = QtGui.QPushButton(SingleDie)
        self.ExitButton.setGeometry(QtCore.QRect(210, 210, 75, 23))
        self.ExitButton.setObjectName("pushButton")

        self.die_1 = QtGui.QLabel(SingleDie)
        self.die_1.setGeometry(QtCore.QRect(220,100,51, 51))
        self.die_1.setObjectName("die_1")

        self.retranslateUi(SingleDie)
        QtCore.QObject.connect(self.RollButton, QtCore.SIGNAL("clicked()"), self.WhenClicked)
        QtCore.QObject.connect(self.ExitButton, QtCore.SIGNAL("clicked()"), self.CloseEvent)

        QtCore.QMetaObject.connectSlotsByName(SingleDie)

    def retranslateUi(self, SingleDie):  
        SingleDie.setWindowTitle(QtGui.QApplication.translate("SingleDie", "SingleDie", None, QtGui.QApplication.UnicodeUTF8))
        self.RollButton.setText(QtGui.QApplication.translate("SingleDie", "Roll", None, QtGui.QApplication.UnicodeUTF8))
        self.ExitButton.setText(QtGui.QApplication.translate("SingleDie", "Exit", None, QtGui.QApplication.UnicodeUTF8))

    def FindItemPath(self):
        ItemPath = os.getcwd()
        length = len(os.getcwd())
        ItemPath = ItemPath[0:(length - 7)]
        if(ItemPath[len(ItemPath)-1] == "\\"):
            ItemPath = ItemPath + "data\\Other\\"
        if(ItemPath[len(ItemPath)-1] == "/"):
            ItemPath = ItemPath + "data/Other/"
        return ItemPath    

    #this function will do the actual rolling of the dice. It takes a number of rolls
    #and calls randint() to generate that many random number between 1 and 6.
    #Each random number generated is appended to a list for later use. 
    def Roll(self, rolls):
        if rolls < 0:
            rolls = 0
        dice = []
        
        dice.append(random.randint(1,6))
        self.SingleDie.ReturnVal = dice[0]
        return dice


    #this funtion displays the dice pictures. 
    def PlacePics(self, nums):
        files = []
        files.insert(0, "DicePics/dice_white.jpg")

        path = "DicePics/dice_"

        entry = path
        entry += str(nums[0])
        files[0] = entry

        self.die_1.setPixmap(QtGui.QPixmap(files[0]))

    #this function calls all the function needed to roll and place pics.
    #This function gets called when the Roll Button is clicked. 
    def WhenClicked(self):
        self.PlacePics(self.Roll(1))
        self.RollButton.setDisabled(1)
    def CloseEvent(self):
        self.SingleDie.close()
        self.MyEventLoop.exit(0)
        


class Window2(QtGui.QDialog):
    def DoStuff2(self,MyEventLoop):
        parent=None
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_SingleDie()
        self.ui.setupUi(MyEventLoop,self)

#this function needs to be called in order to display the window
        #this function is for DiceRoller
def ViewRoller():

    MyEventLoop = QtCore.QEventLoop()
    window2 = Window2()
    window2.DoStuff2(MyEventLoop)
    window2.show()
    MyEventLoop.exec_()
    return window2.ReturnVal

