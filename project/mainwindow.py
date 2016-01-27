# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sun Feb 21 13:58:06 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
from PyQt4.phonon import Phonon

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, Env):
        #This sets up the main menu with a size of 1024 by 768, the required
        #size as per our requirements. As a note, everything after the variable
        #name is python bindings to QT4, so any questions can be looked up in
        #the QT4 documentation, which is in C.
        self.Env = Env
        MainWindow.setObjectName("MainWindow")
        bb = Env[2].desktop().size()
        self.MW = MainWindow
        self.videoPlayer = Phonon.VideoPlayer(self.MW)
        self.videoPlayer.setGeometry(QtCore.QRect(0, 0, bb.width(), bb.height()))
        self.videoPlayer.setObjectName("videoPlayer")
        self.tabWidget = QtGui.QGraphicsView(self.MW)
        self.tabWidget.setGeometry(QtCore.QRect(400, 300, 551, 351))
        self.tabWidget.setObjectName("tabWidget")
        self.PlayerNumberSB = QtGui.QSpinBox(self.tabWidget)
        self.PlayerNumberSB.setGeometry(QtCore.QRect(180, 100, 42, 22))
        self.PlayerNumberSB.setFocusPolicy(QtCore.Qt.NoFocus)
        self.PlayerNumberSB.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.PlayerNumberSB.setReadOnly(False)
        self.PlayerNumberSB.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.PlayerNumberSB.setMinimum(1)
        self.PlayerNumberSB.setMaximum(8)
        self.PlayerNumberSB.setObjectName("PlayerNumberSB")
        self.label = QtGui.QLabel(self.tabWidget)
        self.label.setGeometry(QtCore.QRect(40, 100, 91, 16))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.tabWidget)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 61, 16))
        self.label_2.setMargin(1)
        self.label_2.setObjectName("label_2")
        self.GameNameLE = QtGui.QLineEdit(self.tabWidget)
        self.GameNameLE.setEnabled(True)
        self.GameNameLE.setGeometry(QtCore.QRect(110, 60, 113, 20))
        self.GameNameLE.setObjectName("GameNameLE")
        self.LoadGamesTable = QtGui.QTableWidget(self.tabWidget)
        self.LoadGamesTable.setGeometry(QtCore.QRect(0, 160, 421, 101))
        self.LoadGamesTable.setFrameShape(QtGui.QFrame.StyledPanel)
        self.LoadGamesTable.setFrameShadow(QtGui.QFrame.Sunken)
        self.LoadGamesTable.setLineWidth(3)
        self.LoadGamesTable.setMidLineWidth(2)
        self.LoadGamesTable.setAlternatingRowColors(True)
        self.LoadGamesTable.setGridStyle(QtCore.Qt.DashDotLine)
        self.LoadGamesTable.setWordWrap(False)
        self.LoadGamesTable.setObjectName("LoadGamesTable")
        self.LoadGamesTable.setColumnCount(0)
        self.LoadGamesTable.setRowCount(0)
        self.groupBox = QtGui.QGroupBox(self.tabWidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 91, 161))
        self.groupBox.setFocusPolicy(QtCore.Qt.TabFocus)
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.LoadGameRB = QtGui.QRadioButton(self.groupBox)
        self.LoadGameRB.setGeometry(QtCore.QRect(0, 110, 82, 17))
        self.LoadGameRB.setObjectName("LoadGame")
        self.StartGameRB = QtGui.QRadioButton(self.groupBox)
        self.StartGameRB.setGeometry(QtCore.QRect(10, 20, 82, 17))
        self.StartGameRB.setChecked(True)
        self.StartGameRB.setObjectName("StartGameRB")
        self.OkButton = QtGui.QPushButton(self.MW)
        self.OkButton.setGeometry(QtCore.QRect(470, 690, 75, 23))
        self.OkButton.setObjectName("OkButton")
        self.QuitButton = QtGui.QPushButton(self.MW)
        self.QuitButton.setGeometry(QtCore.QRect(840, 690, 75, 23))
        self.QuitButton.setObjectName("QuitButton")
        #below here sets up the A/V of the main menu. videoPlayer is the qt/Phonon back end that
        #plays videos. Might have some trouble with file types on linux. While soundPlayer is a
        #bit more complicated. The sound player is the player for the sound, it handles the playing
        #and stopping. The sound is the audioOutput, which controls volume and other internals.
        #They are mapped together with the Path = Phonon.createPath().
        self.soundPlayer = Phonon.MediaObject(self.MW)
        self.soundPlayer.setCurrentSource(Phonon.MediaSource("des.mp3"))
        self.sound = Phonon.AudioOutput(Phonon.MusicCategory, self.MW)
        Path = Phonon.createPath(self.soundPlayer, self.sound)
        self.soundPlayer.play()
        self.videoPlayer.play(Phonon.MediaSource("tab2.avi"))
        self.retranslateUi(self.MW)
        #These are the signals that connect the buttons to functions. First part is always?
        #the same. The next part is the widget that sends the signal. Next is the signal sent.
        #Be sure to include any variables if the signal sends them. Last is the function to be
        #called
        QtCore.QObject.connect(self.OkButton, QtCore.SIGNAL("clicked()"), self.OkClicked)
        QtCore.QObject.connect(self.QuitButton, QtCore.SIGNAL("clicked()"), self.ExitOut)
        QtCore.QObject.connect(self.videoPlayer, QtCore.SIGNAL("finished()"), self.Replay)
        QtCore.QObject.connect(self.soundPlayer, QtCore.SIGNAL("aboutToFinish()"), self.ReplaySound)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        #translates all the text into unicodeUTF8
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Arkham Horror", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Number of Players", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Game Name", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadGamesTable.setSortingEnabled(True)
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Start New or Load", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadGameRB.setText(QtGui.QApplication.translate("MainWindow", "Load Game", None, QtGui.QApplication.UnicodeUTF8))
        self.StartGameRB.setText(QtGui.QApplication.translate("MainWindow", "Start Game", None, QtGui.QApplication.UnicodeUTF8))
        self.OkButton.setText(QtGui.QApplication.translate("MainWindow", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.QuitButton.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))



    def Replay(self):
        #replays main game video when it finishes
        self.videoPlayer.play(Phonon.MediaSource("tab2.avi"))


    def ReplaySound(self):
        #replays main game song when it finishes
        self.soundPlayer.enqueue(Phonon.MediaSource("des.mp3"))


    def OkClicked(self):
        #If the ok button gets clicked, we check to see what tab is set and what button is set
        #in that tab. 
        if(self.StartGameRB.isChecked() == True):
            #save player number and game name and start a new game
            if(self.GameNameLE.displayText() != ""):
                self.LoadNew(self.PlayerNumberSB.value(), self.GameNameLE.displayText())
                return
        if(self.LoadGameRB.isChecked() == True):
            #load game and start that game up
            return


    def ExitOut(self):
        self.Env[0] = 0
        self.MW.close()
            

    def LoadNew(self, NumPlayers, GameName):
        self.Env[0] = NumPlayers
        self.Env[1] = GameName
        self.MW.close()
            

class MainForm(QtGui.QWidget):
    def __init__(self, X, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, X)


def DisplayMainMenu(app, X):
    #app = QtGui.QApplication(sys.argv)
    X.append(app)
    myapp = MainForm(X)
    myapp.showMaximized()
    app.exec_ ()

