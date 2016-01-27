# -*- coding: utf-8 -*-

#GUI for the player versus monster interaction

import characterscreen
import DiceRoller
import EventDialog


from PyQt4 import QtCore, QtGui

class Ui_CombatUI(object):
    def setupUi(self, app, CombatUI, Player, MonsterList,DefeatedList,EvadedList, env):
        self.app = app
        self.Env = env
        self.CombatUI = CombatUI
        self.Player = Player
        self.Location = Player.Location
        self.AutoWin = False
        if self.Player.Status["Cursed"] > 0 :
            self.ReqSuccess = 6
        elif self.Player.Status["Blessed"] > 0 :
            self.ReqSuccess = 4
        else :
            self.ReqSuccess = 5
        self.Horror = 0
        self.DefeatedList = DefeatedList
        self.EvadedList = EvadedList
        self.MonsterList = MonsterList
        self.Monster = self.MonsterList[0]
        self.Player.FightingMonster = self.Monster
        #Creates MonsterList in GUI
        self.MonsterText = ""
        for x in MonsterList:
            self.MonsterText = self.MonsterText + x.Name + "\n"
            
        CombatUI.setObjectName("CombatUI")
        CombatUI.resize(552, 407)
        self.line = QtGui.QFrame(CombatUI)
        self.line.setGeometry(QtCore.QRect(-3, 180, 341, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtGui.QFrame(CombatUI)
        self.line_2.setGeometry(QtCore.QRect(330, 0, 20, 431))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.Combat = QtGui.QPushButton(CombatUI)
        self.Combat.setGeometry(QtCore.QRect(160, 190, 75, 23))
        self.Combat.setObjectName("Combat")
        self.Flee = QtGui.QPushButton(CombatUI)
        self.Flee.setGeometry(QtCore.QRect(77, 190, 75, 23))
        self.Flee.setObjectName("Flee")
        self.Evade = QtGui.QPushButton(CombatUI)
        self.Evade.setGeometry(QtCore.QRect(0, 190, 75, 23))
        self.Evade.setObjectName("Evade")
        self.Equip = QtGui.QPushButton(CombatUI)
        self.Equip.setGeometry(QtCore.QRect(240, 190, 75, 23))
        self.Equip.setObjectName("Equip")
        self.MonsterListLabel = QtGui.QLabel(CombatUI)
        self.MonsterListLabel.setGeometry(QtCore.QRect(350, 0, 91, 31))
        self.MonsterListLabel.setObjectName("self.MonsterListLabel")
        self.MonsterListBox = QtGui.QLabel(CombatUI)
        self.MonsterListBox.setGeometry(QtCore.QRect(350, 30, 191, 371))
        self.MonsterListBox.setObjectName("self.MonsterListBox")
        self.PlayerPictureBox = QtGui.QLabel(CombatUI)
        self.PlayerPictureBox.setGeometry(QtCore.QRect(0, 0, 201, 181))
        self.PlayerPictureBox.setObjectName("self.PlayerPictureBox")
        self.MonsterPictureBox = QtGui.QLabel(CombatUI)
        self.MonsterPictureBox.setGeometry(QtCore.QRect(0, 220, 201, 181))
        self.MonsterPictureBox.setObjectName("self.MonsterPictureBox")
        self.line_4 = QtGui.QFrame(CombatUI)
        self.line_4.setGeometry(QtCore.QRect(200, 0, 20, 191))
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.StaminaLabel = QtGui.QLabel(CombatUI)
        self.StaminaLabel.setGeometry(QtCore.QRect(220, 00, 46, 21))
        self.StaminaLabel.setObjectName("StaminaLabel")
        self.SanityLabel = QtGui.QLabel(CombatUI)
        self.SanityLabel.setGeometry(QtCore.QRect(220, 40, 46, 20))
        self.SanityLabel.setObjectName("SanityLabel")
        self.SneakLabel = QtGui.QLabel(CombatUI)
        self.SneakLabel.setGeometry(QtCore.QRect(220, 80, 46, 20))
        self.SneakLabel.setObjectName("SneakLabel")
        self.FightLabel = QtGui.QLabel(CombatUI)
        self.FightLabel.setGeometry(QtCore.QRect(220, 120, 46, 20))
        self.FightLabel.setObjectName("FightLabel")
        self.WillLabel = QtGui.QLabel(CombatUI)
        self.WillLabel.setGeometry(QtCore.QRect(220, 160, 46, 20))
        self.WillLabel.setObjectName("WillLabel")
        self.CombatRatingLabel = QtGui.QLabel(CombatUI)
        self.CombatRatingLabel.setGeometry(QtCore.QRect(220, 230, 81, 20))
        self.CombatRatingLabel.setObjectName("CombatRatingLabel")
        self.ToughnessLabel = QtGui.QLabel(CombatUI)
        self.ToughnessLabel.setGeometry(QtCore.QRect(220, 260, 81, 20))
        self.ToughnessLabel.setObjectName("ToughnessLabel")
        self.line_6 = QtGui.QFrame(CombatUI)
        self.line_6.setGeometry(QtCore.QRect(200, 220, 20, 211))
        self.line_6.setFrameShape(QtGui.QFrame.VLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtGui.QFrame(CombatUI)
        self.line_7.setGeometry(QtCore.QRect(0, 210, 341, 20))
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_3 = QtGui.QFrame(CombatUI)
        self.line_3.setGeometry(QtCore.QRect(560, 0, 20, 431))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.StaminaBox = QtGui.QLabel(CombatUI)
        self.StaminaBox.setGeometry(QtCore.QRect(280, 0, 31, 21))
        self.StaminaBox.setObjectName("StaminaBox")
        self.SanityBox = QtGui.QLabel(CombatUI)
        self.SanityBox.setGeometry(QtCore.QRect(280, 40, 31, 21))
        self.SanityBox.setObjectName("SanityBox")
        self.SneakBox = QtGui.QLabel(CombatUI)
        self.SneakBox.setGeometry(QtCore.QRect(280, 80, 31, 21))
        self.SneakBox.setObjectName("SneakBox")
        self.FightBox = QtGui.QLabel(CombatUI)
        self.FightBox.setGeometry(QtCore.QRect(280, 120, 31, 21))
        self.FightBox.setObjectName("FightBox")
        self.WillBox = QtGui.QLabel(CombatUI)
        self.WillBox.setGeometry(QtCore.QRect(280, 160, 31, 21))
        self.WillBox.setObjectName("WillBox")
        self.CombatRatingBox = QtGui.QLabel(CombatUI)
        self.CombatRatingBox.setGeometry(QtCore.QRect(310, 230, 31, 21))
        self.CombatRatingBox.setObjectName("CombatRatingBox")
        self.ToughnessBox = QtGui.QLabel(CombatUI)
        self.ToughnessBox.setGeometry(QtCore.QRect(310, 260, 31, 21))
        self.ToughnessBox.setObjectName("ToughnessBox")
        self.CombatDamageLabel = QtGui.QLabel(CombatUI)
        self.CombatDamageLabel.setGeometry(QtCore.QRect(220, 290, 81, 20))
        self.CombatDamageLabel.setObjectName("CombatDamageLabel")
        self.CombatDamageBox = QtGui.QLabel(CombatUI)
        self.CombatDamageBox.setGeometry(QtCore.QRect(310, 290, 31, 21))
        self.CombatDamageBox.setObjectName("CombatDamageBox")
        self.SanityDamageLabel = QtGui.QLabel(CombatUI)
        self.SanityDamageLabel.setGeometry(QtCore.QRect(220, 320, 81, 20))
        self.SanityDamageLabel.setObjectName("SanityDamageLabel")
        self.SanityDamageBox = QtGui.QLabel(CombatUI)
        self.SanityDamageBox.setGeometry(QtCore.QRect(310, 320, 31, 21))
        self.SanityDamageBox.setObjectName("SanityDamageBox")
        self.SneakCheckLabel = QtGui.QLabel(CombatUI)
        self.SneakCheckLabel.setGeometry(QtCore.QRect(220, 350, 81, 20))
        self.SneakCheckLabel.setObjectName("SneakCheckLabel")
        self.HorrorCheckLabel = QtGui.QLabel(CombatUI)
        self.HorrorCheckLabel.setGeometry(QtCore.QRect(220, 380, 81, 20))
        self.HorrorCheckLabel.setObjectName("HorrorCheckLabel")
        self.SneakCheckBox = QtGui.QLabel(CombatUI)
        self.SneakCheckBox.setGeometry(QtCore.QRect(310, 350, 31, 21))
        self.SneakCheckBox.setObjectName("SneakCheckBox")
        self.HorrorCheckBox = QtGui.QLabel(CombatUI)
        self.HorrorCheckBox.setGeometry(QtCore.QRect(310, 380, 31, 21))
        self.HorrorCheckBox.setObjectName("HorrorCheckBox")


        QtCore.QObject.connect(self.Combat, QtCore.SIGNAL("clicked()"), self.CombatFunction)
        QtCore.QObject.connect(self.Flee, QtCore.SIGNAL("clicked()"), self.FleeFunction)
        QtCore.QObject.connect(self.Evade, QtCore.SIGNAL("clicked()"), self.EvadeFunction)
        QtCore.QObject.connect(self.Equip, QtCore.SIGNAL("clicked()"), self.EquipFunction)

        
        self.Flee.setDisabled(1)

        self.retranslateUi(CombatUI)
        QtCore.QMetaObject.connectSlotsByName(CombatUI)

        
        


        

    def retranslateUi(self, CombatUI):

        if self.Player.Stats["Stamina"] <= 0 :
            #EventDialog.Run("Combat Over","You have lost all your stamina and have gone unconscious!")
            self.Flee.setDisabled(1)
            self.Evade.setDisabled(1)
            self.Combat.setDisabled(1)
            self.Player.RunExecStack(self.Player.ExecEOCStack)
            self.CloseEvent()
            return

        if self.Player.Stats["Sanity"] <= 0 :
            #EventDialog.Run("Combat Over","You have lost all your sanity and have gone insane!")
            self.Flee.setDisabled(1)
            self.Evade.setDisabled(1)
            self.Combat.setDisabled(1)
            self.Player.RunExecStack(self.Player.ExecEOCStack)
            self.CloseEvent()
            return

        if self.Player.Location != self.Location:
            self.Player.RunExecStack(self.Player.ExecEOCStack)
            self.CloseEvent()
            return

        if not self.MonsterList :
            self.CloseEvent()
            return
        #Always set current monster to top monster of monsterlist.
                    
        self.Monster = self.MonsterList[0]
        self.Player.FightingMonster = self.Monster
        

        #Recreates MonsterList in GUI
        self.MonsterText = ""
        for x in self.MonsterList:
            self.MonsterText = self.MonsterText + x.Name + "\n"
        
        CombatUI.setWindowTitle(QtGui.QApplication.translate("CombatUI", "Form", None, QtGui.QApplication.UnicodeUTF8))

        self.Combat.setText(QtGui.QApplication.translate("CombatUI", "Combat", None, QtGui.QApplication.UnicodeUTF8))

        self.Flee.setText(QtGui.QApplication.translate("CombatUI", "Flee", None, QtGui.QApplication.UnicodeUTF8))

        self.Evade.setText(QtGui.QApplication.translate("CombatUI", "Evade", None, QtGui.QApplication.UnicodeUTF8))

        self.Equip.setText(QtGui.QApplication.translate("CombatUI", "Equip", None, QtGui.QApplication.UnicodeUTF8))

        self.MonsterListLabel.setText(QtGui.QApplication.translate("CombatUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Monsters</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        self.MonsterListBox.setText(QtGui.QApplication.translate("CombatUI", self.MonsterText, None, QtGui.QApplication.UnicodeUTF8))

        self.PlayerPictureBox.setPixmap(QtGui.QPixmap(self.Player.Graphic).scaledToHeight(181))

        self.MonsterPictureBox.setPixmap(QtGui.QPixmap(self.Monster.Picture).scaledToHeight(181))

        self.StaminaLabel.setText(QtGui.QApplication.translate("CombatUI", "Stamina", None, QtGui.QApplication.UnicodeUTF8))

        self.SanityLabel.setText(QtGui.QApplication.translate("CombatUI", "Sanity", None, QtGui.QApplication.UnicodeUTF8))

        self.SneakLabel.setText(QtGui.QApplication.translate("CombatUI", "Sneak", None, QtGui.QApplication.UnicodeUTF8))

        self.FightLabel.setText(QtGui.QApplication.translate("CombatUI", "Fight", None, QtGui.QApplication.UnicodeUTF8))

        self.WillLabel.setText(QtGui.QApplication.translate("CombatUI", "Will", None, QtGui.QApplication.UnicodeUTF8))

        self.CombatRatingLabel.setText(QtGui.QApplication.translate("CombatUI", "Combat Rating", None, QtGui.QApplication.UnicodeUTF8))

        self.ToughnessLabel.setText(QtGui.QApplication.translate("CombatUI", "Toughness", None, QtGui.QApplication.UnicodeUTF8))

        self.StaminaBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Player.Stats["Stamina"])+
                                                                           int(self.Player.BonusStats["Stamina"])), None, QtGui.QApplication.UnicodeUTF8))

        self.SanityBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Player.Stats["Sanity"]) +
                                                                          int(self.Player.BonusStats["Sanity"])), None, QtGui.QApplication.UnicodeUTF8))

        self.SneakBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Player.Stats["Sneak"]) +
                                                                         int(self.Player.BonusStats["Sneak"])), None, QtGui.QApplication.UnicodeUTF8))

        self.FightBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Player.Stats["Fight"]) +
                                                                         int(self.Player.BonusStats["Fight"])), None, QtGui.QApplication.UnicodeUTF8))

        self.WillBox.setText(QtGui.QApplication.translate("Dialog", str(int(self.Player.Stats["Will"]) +
                                                                         int(self.Player.BonusStats["Will"])), None, QtGui.QApplication.UnicodeUTF8))

        self.CombatRatingBox.setText(QtGui.QApplication.translate("Dialog", str(self.Monster.CombatRating), None, QtGui.QApplication.UnicodeUTF8))

        self.ToughnessBox.setText(QtGui.QApplication.translate("Dialog", str(self.Monster.Toughness), None, QtGui.QApplication.UnicodeUTF8))

        self.CombatDamageLabel.setText(QtGui.QApplication.translate("CombatUI", "Combat Damage", None, QtGui.QApplication.UnicodeUTF8))

        self.CombatDamageBox.setText(QtGui.QApplication.translate("Dialog", str(self.Monster.StaminaDamage), None, QtGui.QApplication.UnicodeUTF8))


        self.SanityDamageLabel.setText(QtGui.QApplication.translate("CombatUI", "Sanity Damage", None, QtGui.QApplication.UnicodeUTF8))

        self.SanityDamageBox.setText(QtGui.QApplication.translate("Dialog", str(self.Monster.SanityDamage), None, QtGui.QApplication.UnicodeUTF8))

        self.SneakCheckLabel.setText(QtGui.QApplication.translate("CombatUI", "Sneak Check", None, QtGui.QApplication.UnicodeUTF8))

        self.HorrorCheckLabel.setText(QtGui.QApplication.translate("CombatUI", "Horror Check", None, QtGui.QApplication.UnicodeUTF8))

        self.SneakCheckBox.setText(QtGui.QApplication.translate("Dialog", str(self.Monster.Awareness), None, QtGui.QApplication.UnicodeUTF8))

        self.HorrorCheckBox.setText(QtGui.QApplication.translate("Dialog", str(self.Monster.HorrorRating), None, QtGui.QApplication.UnicodeUTF8))

    def CloseEvent(self):
        
        self.CombatUI.close()
        self.app.exit(0)
        return

    def CombatFunction(self):
        self.Combat.setDisabled(1)
        self.Player.CurrentMovementPoints = 0
        self.Evade.setDisabled(1)

        self.Player.RunExecStack(self.Player.ExecSOCStack)
        if self.Monster.Abilities["Ambush"] == 0:
            self.Flee.setDisabled(0)


        
        #Checks to see if horror check has been made (one per monster) if not does horror check.
        if self.Horror == 0:
            Continue = self.Monster.execBeforeHorror()
            if(self.Player.Location != self.Monster.Location):
                
                self.CloseEvent()
                
            self.Horror = 1

            HorrorResult = self.Player.Environment.SkillCheck( "Horror",self.Player, 1 ,self.Monster.HorrorRating )
            if(Continue == "Pass"):
                if HorrorResult == "Pass" :
                    if self.Monster.Abilities["Nightmarish"] +self.Player.CancelAbilities["Nightmarish"] > 0:
                        self.Player.ModSanity( -self.Monster.Abilities["Nightmarish"])
                        EventDialog.Run("Nightmarish!", "The creature is nightmarish, you take partial sanity damage.\n You have lost "+str(self.Monster.Abilities["Nightmarish"])+" Sanity")
                        self.retranslateUi(self.CombatUI)
                    else:
                        EventDialog.Run("Success!", "You passed the horror check")       
                elif HorrorResult == "Fail" :
                    self.Player.ModSanity( -self.Monster.SanityDamage)
                    EventDialog.Run("Failure!", "You failed the horror check.\n You have lost "+str(self.Monster.SanityDamage)+" Sanity")
                    self.retranslateUi(self.CombatUI)
                    #Take horror damage
                if(self.Player.Location != self.Monster.Location):
                    self.Player.RunExecStack(self.Player.ExecEOCStack)
                    self.CloseEvent()
                
        self.Monster.execAfterHorror()
        if(self.Player.Location != self.Monster.Location):
            self.Player.RunExecStack(self.Player.ExecEOCStack)
            self.CloseEvent()


        
        self.retranslateUi(self.CombatUI)        
        if self.Player.Stats["Sanity"] <= 0 or self.Player.Location != self.Monster.Location:
            return
        if(self.Monster.Name == "The Dark Pharoah"):
            CombatResult = self.Player.Environment.SkillCheck( "Lore",self.Player,self.Monster.Toughness,self.Monster.CombatRating )
        else:
            CombatResult = self.Player.Environment.SkillCheck( "Combat",self.Player,self.Monster.Toughness,self.Monster.CombatRating )
            
        if CombatResult == "Pass" or self.AutoWin == True:        #<---pass = monster defeated
            if self.Monster.Abilities["Overwhelming"] + self.Player.CancelAbilities["Overwhelming"] > 0:
                self.Player.ModHealth( -self.Monster.Abilities["Overwhelming"] )
                EventDialog.Run("Overwhelming!", "The creature is Overwhelming, you take partial stamina damage even in victory.\n You have lost "+str(self.Monster.Abilities["Overwhelming"])+" Stamina")
                self.retranslateUi(self.CombatUI)
            EventDialog.Run("Success!", "You defeated the "+self.Monster.Name+", now it is your trophy.")
            
            self.MonsterList.remove(self.Monster)
            self.DefeatedList.append(self.Monster)
            if(self.Monster.Name != "Mi-Go"):
                self.Player.AddMonsterTrophy(self.Monster)
            if(self.Monster.Name == "Mi-Go"):
                self.Player.ItemList.append(self.Player.Environment.DeckDictionary["Unique"].
                                            DrawCard(self.Player, "none"))
            
            self.Evade.setDisabled(0)
            if self.Monster.Abilities["Ambush"] > 0:
                self.Flee.setDisabled(1)
            self.Horror = 0
            
        elif CombatResult == "Fail":
            self.Player.ModHealth( -self.Monster.StaminaDamage)
            EventDialog.Run("Failure!", "You failed the combat check, the monster attacks!.\n You have lost "+str(self.Monster.StaminaDamage)+" Stamina")
            self.Monster.execMonsterAttack()
            if(self.Player.Location != self.Monster.Location):
                self.Player.RunExecStack(self.Player.ExecEOCStack)
                self.CloseEvent()
            #Monster attacks player
        

        #Redraw Screen - Makes stat changes, updates monsterlist.
        if(self.Player.Stats["Stamina"] > 0 and self.Player.Stats["Sanity"] > 0):
            self.Player.RunExecStack(self.Player.ExecEOCStack)
        self.Combat.setDisabled(0)
        self.retranslateUi(self.CombatUI)
        
    def EvadeFunction(self):
        self.Evade.setDisabled(1)
        self.Player.RunExecStack(self.Player.ExecSOCStack)
        if self.Player.AutoPass['Evade'] == 1:
            EvadeResult = "Pass"
        else:
            EvadeResult = self.Player.Environment.SkillCheck( "Evade",self.Player,1,self.Monster.Awareness )

        if EvadeResult == "Fail" :
            self.Player.CurrentMovementPoints = 0
            self.Player.Stats["Stamina"] = self.Player.Stats["Stamina"] - self.Monster.StaminaDamage
            EventDialog.Run("Failure!", "You failed to evade "+self.Monster.Name+".\n The monster attacks! You lose "+str(self.Monster.StaminaDamage)+" Stamina and now you must battle it.")
            #Monster deals combat damage to player here           

        elif EvadeResult == "Pass" :
            self.MonsterList.remove(self.Monster)
            self.EvadedList.append(self.Monster)
            self.Horror = 0
            EventDialog.Run("Success!", "You have evaded "+self.Monster.Name+" and it has been removed from battle.")

        self.Flee.setDisabled(0) 
        if EvadeResult == "Pass" :
            self.Evade.setDisabled(0)
            self.Flee.setDisabled(1)
        #Redraw Screen - Makes stat changes, updates monsterlist.
        self.Player.RunExecStack(self.Player.ExecEOCStack)
        self.retranslateUi(self.CombatUI)
        

            
    def FleeFunction(self):
        self.Flee.setDisabled(1)
        self.Player.CurrentMovementPoints = 0
        self.Player.RunExecStack(self.Player.ExecSOCStack)
        if self.Monster.Abilities["Ambush"] > 0:
            EventDialog.Run("Cannot flee!", "The monster has ambushed you, it is impossible to flee.")
            return


        #Checks to see if horror check has been made (one per monster) if not does horror check.
        if self.Horror == 0 :
            self.Horror = 1
            
            HorrorResult = self.Player.Environment.SkillCheck( "Horror",self.Player, 1 ,self.Monster.HorrorRating )

            if HorrorResult == "Pass" :
                EventDialog.Run("Success!", "You passed the horror check")
                if self.Monster.Abilities["Nightmarish"] > 0:
                    self.Player.ModSanity( -self.Monster.Abilities["Nightmarish"])
                    EventDialog.Run("Nightmarish!", "The creature is nightmarish, you take partial sanity damage.\n You have lost "+str(self.Monster.Abilities["Nightmarish"])+" Sanity")
                    self.retranslateUi(self.CombatUI)
                else:
                    EventDialog.Run("Success!", "You passed the horror check")                    
            elif HorrorResult == "Fail" :
                self.Player.ModSanity( -self.Monster.SanityDamage)
                EventDialog.Run("Failure!", "You failed the horror check.\n You have lost "+str(self.Monster.SanityDamage)+" Sanity")
                self.retranslateUi(self.CombatUI)
                
        if self.Player.Stats["Sanity"] <= 0 or self.Player.Location != self.Monster.Location:
            return
        
        FleeResult = self.Player.Environment.SkillCheck( "Evade",self.Player,1,self.Monster.Awareness )            

        
        if FleeResult == "Pass" :
            self.MonsterList.remove(self.Monster)
            self.EvadedList.append(self.Monster)
            self.Evade.setDisabled(0)
            self.Horror = 0
            EventDialog.Run("Success!", "You have fled from "+self.Monster.Name+" and it has been removed from battle.")
            self.Flee.setDisabled(1)
            
        elif FleeResult == "Fail" :
            #Monster attacks player
            self.Player.ModHealth( -self.Monster.StaminaDamage)
            EventDialog.Run("Failure!", "You failed to flee from "+self.Monster.Name+".\n The monster attacks! You lose "+str(self.Monster.StaminaDamage)+" Stamina.")
            self.Flee.setDisabled(0)
        #Redraw Screen - Makes stat changes, updates monsterlist.
        self.Player.RunExecStack(self.Player.ExecEOCStack)
        self.retranslateUi(self.CombatUI)

        
            
    def EquipFunction(self):
        characterscreen.viewPlayer(self.Player, self.Env)
        self.retranslateUi(self.CombatUI)

class Window(QtGui.QDialog):

    def DoStuff(self, app, Player, MonsterList,DefeatedList,EvadedList, env):
        parent=None
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_CombatUI()
        self.ui.setupUi(app, self, Player, MonsterList,DefeatedList,EvadedList, env)

    def keyPressEvent(self, event):
        if(event.key() == QtCore.Qt.Key_K):
            self.ui.AutoWin = True
        
def Combat(Player, MonsterList, DefeatedList, EvadedList, Env):
    
    MyEventLoop = QtCore.QEventLoop()
    window = Window()
    window.DoStuff(MyEventLoop,Player, MonsterList,DefeatedList,EvadedList, Env)
    window.show()
    MyEventLoop.exec_ ()
    

        
        

