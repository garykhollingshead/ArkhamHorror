#Final Battle UI CODE


import characterscreen
import DiceRoller
from PyQt4 import QtCore, QtGui

class Ui_FinalBattleUI(object):
    def setupUi(self, app, FinalBattleUI, Envir):
        self.app = app
        self.FinalBattleUI = FinalBattleUI
        self.FinalBattleUI.ReturnVal = "Defeat"
        self.Environment = Envir
        self.AncientOne = self.Environment.AncientOne
        self.TotalPlayers = 0

        #Set Doomtrack to Maximum just in case. (rules say to do this when entering final battle)
        self.AncientOne.CurrentDoom = self.AncientOne.MaxDoom

        #This keeps track of the current amount of hits made on the ancient one on his current doom level.
        self.Successes = 0

        self.TotalPlayers = self.Environment.NumOfPlayers

        #We now need to take out all the players from the playerlist entering final battle that are devoured.

        #Now to reconstruct the player list for its final form...

        self.PlayerList = ""

        for x in self.Environment.Investigators:
            self.PlayerList = self.PlayerList + x.Name + "\n"

        #Set Current Player
        self.Environment.CurrentPlayer = self.Environment.Investigators[0]

        

        #Create Turn Counters to be used as indexes
        self.TurnCounter = 0
        self.TurnCounterMax = len(self.Environment.Investigators) - 1
        self.AncientOneTurnToggle = 0
        
        
        self.Dialog = FinalBattleUI
        FinalBattleUI.setObjectName("FinalBattleUI")
        FinalBattleUI.resize(607, 400)
        self.PlayerListBox = QtGui.QLabel(FinalBattleUI)
        self.PlayerListBox.setGeometry(QtCore.QRect(0, 30, 141, 361))
        self.PlayerListBox.setObjectName("PlayerListBox")
        self.PlayerListLabel = QtGui.QLabel(FinalBattleUI)
        self.PlayerListLabel.setGeometry(QtCore.QRect(0, 0, 141, 21))
        self.PlayerListLabel.setObjectName("PlayerListLabel")
        self.line = QtGui.QFrame(FinalBattleUI)
        self.line.setGeometry(QtCore.QRect(140, 0, 20, 401))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtGui.QFrame(FinalBattleUI)
        self.line_2.setGeometry(QtCore.QRect(380, 0, 20, 401))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.CurrentPlayerLabel = QtGui.QLabel(FinalBattleUI)
        self.CurrentPlayerLabel.setGeometry(QtCore.QRect(160, 0, 221, 21))
        self.CurrentPlayerLabel.setObjectName("CurrentPlayerLabel")
        self.PlayerPictureBox = QtGui.QLabel(FinalBattleUI)
        self.PlayerPictureBox.setGeometry(QtCore.QRect(160, 20, 221, 181))
        self.PlayerPictureBox.setObjectName("PlayerPictureBox")
        self.AncientOneLabel = QtGui.QLabel(FinalBattleUI)
        self.AncientOneLabel.setGeometry(QtCore.QRect(400, 0, 201, 21))
        self.AncientOneLabel.setObjectName("AncientOneLabel")
        self.AncientOneBox = QtGui.QLabel(FinalBattleUI)
        self.AncientOneBox.setGeometry(QtCore.QRect(400, 30, 201, 281))
        self.AncientOneBox.setObjectName("AncientOneBox")
        self.line_3 = QtGui.QFrame(FinalBattleUI)
        self.line_3.setGeometry(QtCore.QRect(150, 200, 241, 20))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.SneakLabel = QtGui.QLabel(FinalBattleUI)
        self.SneakLabel.setGeometry(QtCore.QRect(160, 330, 46, 20))
        self.SneakLabel.setObjectName("SneakLabel")
        self.StaminaLabel = QtGui.QLabel(FinalBattleUI)
        self.StaminaLabel.setGeometry(QtCore.QRect(160, 250, 46, 21))
        self.StaminaLabel.setObjectName("StaminaLabel")
        self.FightBox = QtGui.QLabel(FinalBattleUI)
        self.FightBox.setGeometry(QtCore.QRect(220, 370, 31, 21))
        self.FightBox.setObjectName("FightBox")
        self.SanityBox = QtGui.QLabel(FinalBattleUI)
        self.SanityBox.setGeometry(QtCore.QRect(320, 250, 31, 21))
        self.SanityBox.setObjectName("SanityBox")
        self.SanityLabel = QtGui.QLabel(FinalBattleUI)
        self.SanityLabel.setGeometry(QtCore.QRect(260, 250, 46, 20))
        self.SanityLabel.setObjectName("SanityLabel")
        self.SneakBox = QtGui.QLabel(FinalBattleUI)
        self.SneakBox.setGeometry(QtCore.QRect(220, 330, 31, 21))
        self.SneakBox.setObjectName("SneakBox")
        self.StaminaBox = QtGui.QLabel(FinalBattleUI)
        self.StaminaBox.setGeometry(QtCore.QRect(220, 250, 31, 21))
        self.StaminaBox.setObjectName("StaminaBox")
        self.FightLabel = QtGui.QLabel(FinalBattleUI)
        self.FightLabel.setGeometry(QtCore.QRect(160, 370, 46, 20))
        self.FightLabel.setObjectName("FightLabel")
        self.LoreLabel = QtGui.QLabel(FinalBattleUI)
        self.LoreLabel.setGeometry(QtCore.QRect(260, 330, 46, 20))
        self.LoreLabel.setObjectName("LoreLabel")
        self.WillLabel = QtGui.QLabel(FinalBattleUI)
        self.WillLabel.setGeometry(QtCore.QRect(160, 290, 46, 21))
        self.WillLabel.setObjectName("WillLabel")
        self.LuckBox = QtGui.QLabel(FinalBattleUI)
        self.LuckBox.setGeometry(QtCore.QRect(320, 370, 31, 21))
        self.LuckBox.setObjectName("LuckBox")
        self.SpeedBox = QtGui.QLabel(FinalBattleUI)
        self.SpeedBox.setGeometry(QtCore.QRect(320, 290, 31, 21))
        self.SpeedBox.setObjectName("SpeedBox")
        self.SpeedLabel = QtGui.QLabel(FinalBattleUI)
        self.SpeedLabel.setGeometry(QtCore.QRect(260, 290, 46, 20))
        self.SpeedLabel.setObjectName("SpeedLabel")
        self.LoreBox = QtGui.QLabel(FinalBattleUI)
        self.LoreBox.setGeometry(QtCore.QRect(320, 330, 31, 21))
        self.LoreBox.setObjectName("LoreBox")
        self.WillBox = QtGui.QLabel(FinalBattleUI)
        self.WillBox.setGeometry(QtCore.QRect(220, 290, 31, 21))
        self.WillBox.setObjectName("WillBox")
        self.LuckLabel = QtGui.QLabel(FinalBattleUI)
        self.LuckLabel.setGeometry(QtCore.QRect(260, 370, 46, 20))
        self.LuckLabel.setObjectName("LuckLabel")
        self.line_4 = QtGui.QFrame(FinalBattleUI)
        self.line_4.setGeometry(QtCore.QRect(390, 310, 221, 20))
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.DoomtrackLabel = QtGui.QLabel(FinalBattleUI)
        self.DoomtrackLabel.setGeometry(QtCore.QRect(400, 330, 91, 21))
        self.DoomtrackLabel.setObjectName("DoomtrackLabel")
        self.DoomtrackBox = QtGui.QLabel(FinalBattleUI)
        self.DoomtrackBox.setGeometry(QtCore.QRect(510, 330, 31, 21))
        self.DoomtrackBox.setObjectName("DoomtrackBox")
        self.Trade = QtGui.QPushButton(FinalBattleUI)
        self.Trade.setGeometry(QtCore.QRect(310, 210, 75, 23))
        self.Trade.setObjectName("Trade")
        self.line_5 = QtGui.QFrame(FinalBattleUI)
        self.line_5.setGeometry(QtCore.QRect(150, 230, 241, 20))
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.SuccessLabel = QtGui.QLabel(FinalBattleUI)
        self.SuccessLabel.setGeometry(QtCore.QRect(400, 350, 91, 21))
        self.SuccessLabel.setObjectName("SuccessLabel")
        self.SuccessBox = QtGui.QLabel(FinalBattleUI)
        self.SuccessBox.setGeometry(QtCore.QRect(510, 350, 31, 21))
        self.SuccessBox.setObjectName("SuccessBox")
        self.PlayerNumberLabel = QtGui.QLabel(FinalBattleUI)
        self.PlayerNumberLabel.setGeometry(QtCore.QRect(400, 370, 91, 16))
        self.PlayerNumberLabel.setObjectName("PlayerNumberLabel")
        self.PlayerNumberBox = QtGui.QLabel(FinalBattleUI)
        self.PlayerNumberBox.setGeometry(QtCore.QRect(510, 370, 31, 21))
        self.PlayerNumberBox.setObjectName("PlayerNumberBox")
        self.Equip = QtGui.QPushButton(FinalBattleUI)
        self.Equip.setGeometry(QtCore.QRect(230, 210, 75, 23))
        self.Equip.setObjectName("Equip")
        self.Combat = QtGui.QPushButton(FinalBattleUI)
        self.Combat.setGeometry(QtCore.QRect(150, 210, 75, 23))
        self.Combat.setObjectName("Combat")

        self.retranslateUi(FinalBattleUI)
        QtCore.QObject.connect(self.Trade, QtCore.SIGNAL("clicked()"), self.TradeFunction)
        QtCore.QObject.connect(self.Equip, QtCore.SIGNAL("clicked()"), self.EquipFunction)
        QtCore.QObject.connect(self.Combat, QtCore.SIGNAL("clicked()"), self.CombatFunction)
        QtCore.QMetaObject.connectSlotsByName(FinalBattleUI)

    def CloseEvent(self):
        self.FinalBattleUI.close()
        self.app.exit(0)

    def retranslateUi(self, FinalBattleUI):
        FinalBattleUI.setWindowTitle(QtGui.QApplication.translate("FinalBattleUI", "Final Battle", None, QtGui.QApplication.UnicodeUTF8))

        self.PlayerListBox.setText(self.PlayerList)

        self.PlayerListLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Players</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        self.CurrentPlayerLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Current Player</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        self.PlayerPictureBox.setPixmap(QtGui.QPixmap(self.Environment.CurrentPlayer.Graphic).scaledToHeight(181))

        self.AncientOneLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">The Ancient One</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        self.AncientOneBox.setPixmap(QtGui.QPixmap(self.Environment.AncientOne.Picture).scaledToHeight(320))

        self.SneakLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Sneak", None, QtGui.QApplication.UnicodeUTF8))

        self.StaminaLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Stamina", None, QtGui.QApplication.UnicodeUTF8))

        self.FightBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Environment.CurrentPlayer.Stats["Fight"]) +
                                                                         int(self.Environment.CurrentPlayer.BonusStats["Fight"])), None, QtGui.QApplication.UnicodeUTF8))

        self.SanityBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Environment.CurrentPlayer.Stats["Sanity"]) +
                                                                         int(self.Environment.CurrentPlayer.BonusStats["Sanity"])), None, QtGui.QApplication.UnicodeUTF8))

        self.SanityLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Sanity", None, QtGui.QApplication.UnicodeUTF8))

        self.SneakBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Environment.CurrentPlayer.Stats["Sneak"]) +
                                                                         int(self.Environment.CurrentPlayer.BonusStats["Sneak"])), None, QtGui.QApplication.UnicodeUTF8))

        self.StaminaBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Environment.CurrentPlayer.Stats["Stamina"]) +
                                                                         int(self.Environment.CurrentPlayer.BonusStats["Stamina"])), None, QtGui.QApplication.UnicodeUTF8))

        self.FightLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Fight", None, QtGui.QApplication.UnicodeUTF8))

        self.LoreLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Lore", None, QtGui.QApplication.UnicodeUTF8))

        self.WillLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Will", None, QtGui.QApplication.UnicodeUTF8))

        self.LuckBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Environment.CurrentPlayer.Stats["Luck"]) +
                                                                         int(self.Environment.CurrentPlayer.BonusStats["Luck"])), None, QtGui.QApplication.UnicodeUTF8))

        self.SpeedBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Environment.CurrentPlayer.Stats["Speed"]) +
                                                                         int(self.Environment.CurrentPlayer.BonusStats["Speed"])), None, QtGui.QApplication.UnicodeUTF8))

        self.SpeedLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Speed", None, QtGui.QApplication.UnicodeUTF8))

        self.LoreBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Environment.CurrentPlayer.Stats["Lore"]) +
                                                                         int(self.Environment.CurrentPlayer.BonusStats["Lore"])), None, QtGui.QApplication.UnicodeUTF8))

        self.WillBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Environment.CurrentPlayer.Stats["Will"]) +
                                                                         int(self.Environment.CurrentPlayer.BonusStats["Will"])), None, QtGui.QApplication.UnicodeUTF8))


        self.LuckLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Luck", None, QtGui.QApplication.UnicodeUTF8))

        self.DoomtrackLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Current Doomtrack", None, QtGui.QApplication.UnicodeUTF8))

        self.DoomtrackBox.setText(str(self.AncientOne.CurrentDoom))

        self.Trade.setText(QtGui.QApplication.translate("FinalBattleUI", "Trade", None, QtGui.QApplication.UnicodeUTF8))



        self.SuccessLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Successes", None, QtGui.QApplication.UnicodeUTF8))

        self.SuccessBox.setText(str(self.Successes))

        self.PlayerNumberLabel.setText(QtGui.QApplication.translate("FinalBattleUI", "Number of Players", None, QtGui.QApplication.UnicodeUTF8))

        self.PlayerNumberBox.setText(str(self.TotalPlayers))

        self.Equip.setText(QtGui.QApplication.translate("FinalBattleUI", "Equip", None, QtGui.QApplication.UnicodeUTF8))



        self.Combat.setText(QtGui.QApplication.translate("FinalBattleUI", "Combat", None, QtGui.QApplication.UnicodeUTF8))

        

    def CombatFunction(self):

        #Player deals damage
        if self.Environment.CurrentPlayer.Status["Cursed"] > 0 :
            self.ReqSuccess = 6
        elif self.Environment.CurrentPlayer.Status["Blessed"] > 0 :
            self.ReqSuccess = 4
        else :
            self.ReqSuccess = 5
        
        NumDice = self.Environment.CurrentPlayer.Stats["Fight"] + self.Environment.CurrentPlayer.BonusStats["Fight"] + self.AncientOne.CombatRating
        NumDice += self.Environment.CurrentPlayer.BonusStats["Combat"]
        
        if self.AncientOne.Abilities["PhysicalImmunity"] == 1:
            NumDice += 0 * self.Environment.CurrentPlayer.BonusStats["Physical"]
        elif self.AncientOne.Abilities["PhysicalResistance"] == 1:
            NumDice +=  int(self.Environment.CurrentPlayer.BonusStats["Physical"] / 2)
        if self.AncientOne.Abilities["MagicalImmunity"] == 1:
            NumDice +=  0 * self.Environment.CurrentPlayer.BonusStats["Magical"]
        elif self.AncientOne.Abilities["MagicalResistance"] == 1:
            NumDice +=  int(self.Environment.CurrentPlayer.BonusStats["Magical"] / 2)

        CombatResult = DiceRoller.ViewRoller("Combat", self.Environment.CurrentPlayer, NumDice, self.ReqSuccess, 0)

        self.Successes = self.Successes + CombatResult

        while (self.Successes >= self.TotalPlayers):
             self.Successes = self.Successes - self.TotalPlayers
             self.AncientOne.CurrentDoom = self.AncientOne.CurrentDoom - 1
             
            

        #Player turn incremented. Check if everyone has had turn, if not increment, if so reset and set toggle.
        if (self.TurnCounter == self.TurnCounterMax):         
            self.TurnCounter = 0
            self.AncientOneTurnToggle = 1
        else:
            self.TurnCounter = self.TurnCounter + 1

        self.Environment.CurrentPlayer = self.Environment.Investigators[self.TurnCounter]
        
        #Check if its Ancient One's turn.
        if (self.AncientOneTurnToggle == 1):

            #Call Attack Function from XML
            self.AncientOne.AttackFunction()
            
            self.AncientOneTurnToggle = 0           

    #Check to see if any investigators are devoured

        #Check for Sanity
        templist = list()
        for player in self.Environment.Investigators:
            if (player.Stats["Sanity"] <= 0):
                templist.append(player)

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)

        #Check for Stamina
        templist = list()
        for player in self.Environment.Investigators:
            if (player.Stats["Stamina"] <= 0):
                templist.append(player)

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)

        #Check win and loss conditions.

        if(self.Victory()):
            print "Victory"
            self.FinalBattleUI.ReturnVal = "Victory"
            self.Dialog.close()
            self.app.exit()
            
        elif(self.Lose()):
            print "Defeat"
            self.FinalBattleUI.ReturnVal = "Defeat"
            self.Dialog.close()
            self.app.exit()

        self.retranslateUi(self.FinalBattleUI)
            
    def Victory(self):
        
        if(self.Environment.AncientOne.CurrentDoom <= 0):
            return True
        
        else:
            return False
        
    def Lose(self):
        if(self.Environment.Investigators == []):
            return True
        else:
            return False
                    
    def TradeFunction(self):
        print "Trade"
        
    def EquipFunction(self):
        characterscreen.viewPlayer(self.Environment.CurrentPlayer, self.Environment)

class Window(QtGui.QDialog):
    
    def DoStuff(self,app, Envir):
        parent=None
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_FinalBattleUI()
        self.ui.setupUi(app,self, Envir)
    
def viewFinal(Envir):
    app = QtCore.QEventLoop()
    window = Window()
    window.DoStuff(app,Envir)
    window.show()
    app.exec_()
    return window.ReturnVal


