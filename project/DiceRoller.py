"""
Miguel: 
"""


from PyQt4 import QtCore, QtGui
import sys
import random 
import os
import SingleDie
import EventDialog
random.seed()

class Ui_DiceRoller(object):
    def setupUi(self, app, DiceRoller, Type,Player, NumDice, Required, Diff):
        self.app = app
        DiceRoller.setObjectName("DiceRoller")
        DiceRoller.resize(659, 340)
        DiceRoller.RETURNVALUE = "Fail"
        self.DiceRoller = DiceRoller
        self.Player = Player
        self.NumDice = max(0,NumDice)
        self.Required = Required
        self.Diff = Diff
        self.DiceRoller.AutoWin = 0
        self.Type = Type
        self.Numbers = []

        
        
        self.Background = QtGui.QLabel(DiceRoller)
        self.Background.setGeometry(QtCore.QRect(0,0,661, 341))
        self.Background.setObjectName("Background")
        self.Background.setPixmap(QtGui.QPixmap(self.FindItemPath() + "arkham_dice.jpg"))

        self.label_2 = QtGui.QLabel(DiceRoller)
        self.label_2.setGeometry(QtCore.QRect(500,70,151, 16))
        self.label_2.setObjectName("TypeOfRoll1")

        self.label = QtGui.QLabel(DiceRoller)
        self.label.setGeometry(QtCore.QRect(10,70,151, 16))
        self.label.setObjectName("TypeOfRoll2")

        self.Rolls = QtGui.QLabel(DiceRoller)
        self.Rolls.setText(str(self.NumDice))
        self.Rolls.setGeometry(QtCore.QRect(10, 280, 71, 20))
        self.Rolls.setObjectName("Rolls")

        self.Successes = QtGui.QLabel(DiceRoller)
        self.Successes.setText(str(self.Required))
        self.Successes.setGeometry(QtCore.QRect(100, 280, 71, 20))
        self.Successes.setObjectName("Successes")

        self.DiffNumber = QtGui.QLabel(DiceRoller)
        self.DiffNumber.setText(str(self.Diff))
        self.DiffNumber.setGeometry(QtCore.QRect(190, 280, 71, 20))
        self.DiffNumber.setObjectName("Diff")

        self.DisplaySuccesses = QtGui.QLCDNumber(DiceRoller)
        self.DisplaySuccesses.setGeometry(QtCore.QRect(250, 280, 64, 23))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.DisplaySuccesses.setFont(font)
        self.DisplaySuccesses.setObjectName("DisplaySuccesses")
    

        self.RollButton = QtGui.QPushButton(DiceRoller)
        self.RollButton.setGeometry(QtCore.QRect(350, 280, 75, 23))
        self.RollButton.setObjectName("RollButton")

        self.SpendClueButton = QtGui.QPushButton(DiceRoller)
        self.SpendClueButton.setGeometry(QtCore.QRect(440, 280, 75, 23))
        self.SpendClueButton.setObjectName("SpendClueButton")

        self.RerollButton = QtGui.QPushButton(DiceRoller)
        self.RerollButton.setGeometry(QtCore.QRect(530, 280, 61, 23))
        self.RerollButton.setObjectName("RerollButton")

        self.ExitButton = QtGui.QPushButton(DiceRoller)
        self.ExitButton.setGeometry(QtCore.QRect(610, 280, 41, 23))
        self.ExitButton.setObjectName("ExitButton")

        self.NumOfDiceText = QtGui.QLabel(DiceRoller)
        self.NumOfDiceText.setGeometry(QtCore.QRect(10, 310, 81, 16))
        self.NumOfDiceText.setObjectName("NumOfDiceText")

        self.SuccessesNeededText = QtGui.QLabel(DiceRoller)
        self.SuccessesNeededText.setGeometry(QtCore.QRect(100, 310, 100, 30))
        self.SuccessesNeededText.setObjectName("SuccessesNeededText")

        self.NumOfSuccessesText = QtGui.QLabel(DiceRoller)
        self.NumOfSuccessesText.setGeometry(QtCore.QRect(250, 310, 100, 16))
        self.NumOfSuccessesText.setObjectName("NumOfSuccessesText")

        self.DiffText = QtGui.QLabel(DiceRoller)
        self.DiffText.setGeometry(QtCore.QRect(190, 310, 100, 16))
        self.DiffText.setObjectName("DiffText")

        self.Die1 = QtGui.QLabel(DiceRoller)
        self.Die1.setGeometry(QtCore.QRect(40,150,51, 51))
        self.Die1.setObjectName("Die1")

        self.Die2 = QtGui.QLabel(DiceRoller)
        self.Die2.setGeometry(QtCore.QRect(110,150,51, 51))
        self.Die2.setObjectName("Die2")                                  

        self.Die3 = QtGui.QLabel(DiceRoller)
        self.Die3.setGeometry(QtCore.QRect(190,150,51, 51))
        self.Die3.setObjectName("Die3")

        self.Die4 = QtGui.QLabel(DiceRoller)
        self.Die4.setGeometry(QtCore.QRect(260,150,51, 51))
        self.Die4.setObjectName("Die4")

        self.Die5 = QtGui.QLabel(DiceRoller)
        self.Die5.setGeometry(QtCore.QRect(330,150,51, 51))
        self.Die5.setObjectName("Die5")

        self.Die6 = QtGui.QLabel(DiceRoller)
        self.Die6.setGeometry(QtCore.QRect(400,150,51, 51))
        self.Die6.setObjectName("Die6")

        self.Die7 = QtGui.QLabel(DiceRoller)
        self.Die7.setGeometry(QtCore.QRect(470,150,51, 51))
        self.Die7.setObjectName("Die7")

        self.Die8 = QtGui.QLabel(DiceRoller)
        self.Die8.setGeometry(QtCore.QRect(540,150,51, 51))
        self.Die8.setObjectName("Die8")

        self.Die9 = QtGui.QLabel(DiceRoller)
        self.Die9.setGeometry(QtCore.QRect(40,220,51, 51))
        self.Die9.setObjectName("Die9")

        self.Die10 = QtGui.QLabel(DiceRoller)
        self.Die10.setGeometry(QtCore.QRect(110,220,51, 51))
        self.Die10.setObjectName("Die10")

        self.Die11 = QtGui.QLabel(DiceRoller)
        self.Die11.setGeometry(QtCore.QRect(190,220,51, 51))
        self.Die11.setObjectName("Die11")

        self.Die12 = QtGui.QLabel(DiceRoller)
        self.Die12.setGeometry(QtCore.QRect(260,220,51, 51))
        self.Die12.setObjectName("Die12")

        self.Die13 = QtGui.QLabel(DiceRoller)
        self.Die13.setGeometry(QtCore.QRect(330,220,51, 51))
        self.Die13.setObjectName("Die13")

        self.Die14 = QtGui.QLabel(DiceRoller)
        self.Die14.setGeometry(QtCore.QRect(400,220,51, 51))
        self.Die14.setObjectName("Die14")

        self.Die15 = QtGui.QLabel(DiceRoller)
        self.Die15.setGeometry(QtCore.QRect(470,220,51, 51))
        self.Die15.setObjectName("Die15")

        self.Die16 = QtGui.QLabel(DiceRoller)
        self.Die16.setGeometry(QtCore.QRect(540,220,51, 51))
        self.Die16.setObjectName("Die16")

        self.retranslateUi(DiceRoller)
        QtCore.QObject.connect(self.RollButton, QtCore.SIGNAL("clicked()"), self.WhenRollClicked)
        QtCore.QObject.connect(self.ExitButton, QtCore.SIGNAL("clicked()"), self.CloseEvent)
        QtCore.QObject.connect(self.SpendClueButton, QtCore.SIGNAL("clicked()"), self.WhenClueTokenClicked)
        QtCore.QObject.connect(self.RerollButton, QtCore.SIGNAL("clicked()"), self.WhenReRollClicked)

        #reroll
        if self.Player.Reroll[self.Type] or self.Player.Reroll["Any"] :
            #reroll option available do not lock button
            self.RerollButton.setDisabled(0)
        else:
            self.RerollButton.setDisabled(1)

        QtCore.QMetaObject.connectSlotsByName(DiceRoller)

    def retranslateUi(self, DiceRoller):  
        DiceRoller.setWindowTitle(QtGui.QApplication.translate("DiceRoller", "DiceRoller", None, QtGui.QApplication.UnicodeUTF8))
        self.NumOfDiceText.setText(QtGui.QApplication.translate("DiceRoller", "Num Of Dice", None, QtGui.QApplication.UnicodeUTF8))
        self.SuccessesNeededText.setText(QtGui.QApplication.translate("DiceRoller", "Requirement \n for Success", None, QtGui.QApplication.UnicodeUTF8))
        #self.setText(QtGui.QApplication.translate("DiceRoller", "Requirement for Success", None, QtGui.QApplication.UnicodeUTF8))
        #self.SuccessesNeededText.setText(QtGui.QApplication.translate("DiceRoller", "Requirement for Success", None, QtGui.QApplication.UnicodeUTF8))
        self.NumOfSuccessesText.setText(QtGui.QApplication.translate("DicerRoller", "Num of Successes", None, QtGui.QApplication.UnicodeUTF8))
        self.DiffText.setText(QtGui.QApplication.translate("DicerRoller", "Difficulty", None, QtGui.QApplication.UnicodeUTF8))
        self.RollButton.setText(QtGui.QApplication.translate("DiceRoller", "Roll", None, QtGui.QApplication.UnicodeUTF8))
        self.SpendClueButton.setText(QtGui.QApplication.translate("DiceRoller", "Spend Clue", None, QtGui.QApplication.UnicodeUTF8))
        self.RerollButton.setText(QtGui.QApplication.translate("DiceRoller", "Reroll", None, QtGui.QApplication.UnicodeUTF8))
        self.ExitButton.setText(QtGui.QApplication.translate("DiceRoller", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        

    def FindItemPath(self):
        ItemPath = os.getcwd()
        length = len(os.getcwd())
        ItemPath = ItemPath[0:(length - 7)]
        if(ItemPath[len(ItemPath)-1] == "\\"):
            ItemPath = ItemPath + "data\\Other\\"
        if(ItemPath[len(ItemPath)-1] == "/"):
            ItemPath = ItemPath + "data/Other/"
        return ItemPath    

    #this function takes the number of dice to roll number entered by the user
    #if that number is bigger than 16 it will set the number to 16.
    #since the limit dice for the system is 16 this check will prevent that
    #an invalid input breaks things 
    def LimitRolls(self, n):
        temp = str(n)
        temp2 = int(temp)
        if temp2 > 16:
            temp2 = 16
        return temp2

    #this function takes as an argument a list of numbers. These numbers
    #are the results of the rolls done. This function will check the number of successes
    #the player got ofter rolling
    def Successes1(self, rolls2):
        tempstr = self.Successes.text()
        tempint = int(tempstr)
        i = len(rolls2)
        x = 0
        s = 0
        while x < i:
            if rolls2[x] >= tempint:
                s += 1
            x += 1
        return s

    #this function will do the actual rolling of the dice. It takes a number of rolls
    #and calls randint() to generate that many random number between 1 and 6.
    #Each random number generated is appended to a list for later use. 
    def Roll(self, rolls):
        if rolls < 0:
            rolls = 0
        dice = []
        while rolls > 0:
            dice.append(random.randint(1,6))
            rolls -= 1
        return dice

    #this funtion displays the dice pictures. 
    def PlacePics(self, nums):
       
        self.DisplaySuccesses.display(self.Successes1(nums))
        files = []
        x = 0
        while x < 16:
            files.insert(x, "DicePics/dice_white.jpg")
            x += 1
            
        length = len(nums)
        i = 0
        path = "DicePics/dice_"
        while i < length:
            entry = path
            entry += str(nums[i])
            entry += ".jpg"
            files[i] = entry
            i += 1
            
        self.Die1.setPixmap(QtGui.QPixmap(files[0]))
        self.Die2.setPixmap(QtGui.QPixmap(files[1]))
        self.Die3.setPixmap(QtGui.QPixmap(files[2]))
        self.Die4.setPixmap(QtGui.QPixmap(files[3]))
        self.Die5.setPixmap(QtGui.QPixmap(files[4]))
        self.Die6.setPixmap(QtGui.QPixmap(files[5]))
        self.Die7.setPixmap(QtGui.QPixmap(files[6]))
        self.Die8.setPixmap(QtGui.QPixmap(files[7]))
        self.Die9.setPixmap(QtGui.QPixmap(files[8]))
        self.Die10.setPixmap(QtGui.QPixmap(files[9]))
        self.Die11.setPixmap(QtGui.QPixmap(files[10]))
        self.Die12.setPixmap(QtGui.QPixmap(files[11]))
        self.Die13.setPixmap(QtGui.QPixmap(files[12]))
        self.Die14.setPixmap(QtGui.QPixmap(files[13]))
        self.Die15.setPixmap(QtGui.QPixmap(files[14]))
        self.Die16.setPixmap(QtGui.QPixmap(files[15]))

    #this function calls all the function needed to roll and place pics.
    #This function gets called when the Roll Button is clicked.
    def WhenRollClicked(self):
        self.Numbers = self.Roll(self.LimitRolls(self.Rolls.text()))
        self.PlacePics(self.Numbers)
        self.RollButton.setDisabled(1)

    #This function calls all the functions needed to perform a re-roll (when available)
    #This function gets called when the ReRoll Button is clicked.
    def WhenReRollClicked(self):
        self.RerollButton.setDisabled(1)
        if self.Player.Reroll[self.Type] :
            card = self.Player.Reroll[self.Type].pop(0)
        elif self.Player.Reroll["Any"] :
            card = self.Player.Reroll["Any"].pop(0)
        else:
            return
        
        card[4](card,"Use")
        
        self.Numbers = self.Roll(self.LimitRolls(self.Rolls.text()))
        self.PlacePics(self.Numbers)
        if self.Player.Reroll[self.Type] :
            self.RerollButton.setDisabled(0)
        elif self.Player.Reroll["Any"] :
            self.RerollButton.setDisabled(0)
        else:
            self.RerollButton.setDisabled(1)
            return
    #This function calls the singleDie widget whenever a player wants to spend a
    #clue token
    def WhenClueTokenClicked(self):
        if self.Player.Clues <= 0:
            self.SpendClueButton.setDisabled(1)
            EventDialog.Run("Extra Dice","You have insufficient clues to spend on extra rolls. \n Each extra die costs 1 clue token.")
            return
            #no clues
        else:
            self.Player.Clues -= 1

        #self.SpendClueButton.setDisabled(1)
        #result = SingleDie.ViewRoller()

        NumtoRoll = self.Player.CluetoDie[self.Type]
        i = 1
        while (i <= NumtoRoll):
            result = random.randint(1,6)
            self.Numbers.append(result)
            self.NumDice += 1
            self.Rolls.setText(str(self.NumDice))
            self.PlacePics(self.Numbers)
            i = i + 1
    
    #This function is called when quit button is pressed, instead of just directly
    #closing the window.  It will first figure out whether or not you have
    #passed or failed the roll check. then it will set the retval to it
    #and then close the window
    def CloseEvent(self):
        self.DiceRoller.ReturnVal = self.DisplaySuccesses.intValue()
        self.DiceRoller.close()
        self.app.exit(0)

class Window(QtGui.QDialog):
    def DoStuff(self,app, Type, Player, NumDice, Required, Diff):
        parent=None
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DiceRoller()
        self.ui.setupUi(app,self,Type, Player, NumDice, Required, Diff)

    def keyPressEvent(self, event):
        if(event.key() == QtCore.Qt.Key_K):
            self.AutoWin = 1


def RollDice():
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.DoStuff([], 5, 4, 3)
    window.show()
    sys.exit(app.exec_())

def ViewRoller(Type,Player, NumDice, Required, Diff):
    app = QtCore.QEventLoop()
    window = Window()
    window.DoStuff(app,Type,Player, NumDice, Required, Diff)
    window.show()
    app.exec_()
    if(window.AutoWin == 1):
       return 100
    return window.ReturnVal
    

  
        





        


