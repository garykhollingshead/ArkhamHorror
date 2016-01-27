#Do not compile CharacterScreen.ui into this!

from PyQt4 import QtCore, QtGui
import ViewCard

import os

class Ui_Dialog(object):
    
    def setupUi(self, app, Dialog, Player, Env):

        #Set up variables to be used in the functions
        self.app = app
        Dialog.setObjectName("Dialog")
        Dialog.resize(566, 435)
        self.Dialog = Dialog
        self.Env = Env
        self.Player = Player
        self.Trophy = None
        self.TotalTrophies = []
        self.SelectedCard = self.NoItemCard()
        

        self.InvestigatorImageBox = QtGui.QLabel(Dialog)
        self.InvestigatorImageBox.setGeometry(QtCore.QRect(10, 10, 201, 161))
        self.InvestigatorImageBox.setObjectName("InvestigatorImageBox")

        #Setup Fonts
        MediumFont = QtGui.QFont()
        MediumFont.setFamily("Times New Roman")
        MediumFont.setPointSize(14)
        BigFont = QtGui.QFont()
        BigFont.setFamily("Times New Roman")
        BigFont.setPointSize(16)
        LargeFont = QtGui.QFont()
        LargeFont.setFamily("Times New Roman")
        LargeFont.setPointSize(20)

        #Creation of labels and sliders and whatnot
        #The label_ items are constant and shouldn't change
        self.MegaTabBox = QtGui.QTabWidget(Dialog)
        self.MegaTabBox.setGeometry(QtCore.QRect(220, 10, 321, 381))
        self.MegaTabBox.setObjectName("MegaTabBox")
        self.StatsTab = QtGui.QWidget()
        self.StatsTab.setObjectName("StatsTab")

        self.NameLabel = QtGui.QLabel(self.StatsTab)
        self.NameLabel.setGeometry(QtCore.QRect(20, 20, 250, 180))
        self.NameLabel.setTextFormat(QtCore.Qt.AutoText)
        self.NameLabel.setObjectName("CharacterName")
        self.NameLabel.setFont(LargeFont)
        self.NameLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.NameLabel.setAlignment(QtCore.Qt.AlignTop)
        
        self.SpeedStat = QtGui.QLabel(self.StatsTab)
        self.SpeedStat.setGeometry(QtCore.QRect(20, 160, 100, 30))        
        self.SpeedStat.setTextFormat(QtCore.Qt.AutoText)
        self.SpeedStat.setObjectName("SpeedStat")
        self.SpeedStat.setFont(BigFont)
        
        self.SneakStat = QtGui.QLabel(self.StatsTab)
        self.SneakStat.setGeometry(QtCore.QRect(170, 160, 100, 30))
        self.SneakStat.setTextFormat(QtCore.Qt.AutoText)
        self.SneakStat.setObjectName("SneakStat")
        self.SneakStat.setFont(BigFont)
        
        self.FightStat = QtGui.QLabel(self.StatsTab)
        self.FightStat.setGeometry(QtCore.QRect(20, 200, 100, 30))
        self.FightStat.setTextFormat(QtCore.Qt.AutoText)
        self.FightStat.setObjectName("FightStat")
        self.FightStat.setFont(BigFont)
        
        self.WillStat = QtGui.QLabel(self.StatsTab)
        self.WillStat.setGeometry(QtCore.QRect(170, 200, 100, 30))
        self.WillStat.setTextFormat(QtCore.Qt.AutoText)
        self.WillStat.setObjectName("WillStat")
        self.WillStat.setFont(BigFont)
        
        self.LoreStat = QtGui.QLabel(self.StatsTab)
        self.LoreStat.setGeometry(QtCore.QRect(20, 240, 100, 30))
        self.LoreStat.setTextFormat(QtCore.Qt.AutoText)
        self.LoreStat.setObjectName("LoreStat")
        self.LoreStat.setFont(BigFont)
        
        self.LuckStat = QtGui.QLabel(self.StatsTab)
        self.LuckStat.setGeometry(QtCore.QRect(170, 240, 100, 30))
        self.LuckStat.setTextFormat(QtCore.Qt.AutoText)
        self.LuckStat.setObjectName("LuckStat")
        self.LuckStat.setFont(BigFont)

        self.Clues = QtGui.QLabel(self.StatsTab)
        self.Clues.setGeometry(QtCore.QRect(20, 280, 100, 30))
        self.Clues.setTextFormat(QtCore.Qt.AutoText)
        self.Clues.setObjectName("Clues")
        self.Clues.setFont(MediumFont)

        self.Money = QtGui.QLabel(self.StatsTab)
        self.Money.setGeometry(QtCore.QRect(170, 280, 100, 30))
        self.Money.setTextFormat(QtCore.Qt.AutoText)
        self.Money.setObjectName("Money")
        self.Money.setFont(MediumFont)
        
        self.Statuses = QtGui.QLabel(self.StatsTab)
        self.Statuses.setGeometry(QtCore.QRect(20, 300, 200, 60))
        self.Statuses.setTextFormat(QtCore.Qt.AutoText)
        self.Statuses.setObjectName("Statuses")
        self.Statuses.setFont(MediumFont)
        self.Statuses.setWordWrap(1)
        

            
        self.MegaTabBox.addTab(self.StatsTab, "")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(100, 20, 101, 16))
        self.label.setObjectName("label")
        self.FocusRemainingBox = QtGui.QLabel(self.tab)
        self.FocusRemainingBox.setGeometry(QtCore.QRect(190, 20, 100, 21))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 46, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 46, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(20, 230, 46, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(20, 210, 46, 13))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(20, 320, 46, 13))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(20, 300, 46, 13))
        self.label_7.setObjectName("label_7")

        self.SpeedSneakSlider = QtGui.QSlider(self.tab)
        self.SpeedSneakSlider.setGeometry(QtCore.QRect(80, 80, 231, 31))
        self.SpeedSneakSlider.setMaximum(3)
        self.SpeedSneakSlider.setPageStep(1)
        self.SpeedSneakSlider.setSliderPosition(Player.Slider1)
        self.SpeedSneakSlider.setOrientation(QtCore.Qt.Horizontal)
        self.SpeedSneakSlider.setObjectName("SpeedSneakSlider")
        QtCore.QObject.connect(self.SpeedSneakSlider, QtCore.SIGNAL("valueChanged(int)"), self.SpeedSneakMoved)
        
        self.FightWillSlider = QtGui.QSlider(self.tab)
        self.FightWillSlider.setGeometry(QtCore.QRect(80, 170, 231, 31))
        self.FightWillSlider.setMaximum(3)
        self.FightWillSlider.setPageStep(1)
        self.FightWillSlider.setSliderPosition(Player.Slider2)
        self.FightWillSlider.setOrientation(QtCore.Qt.Horizontal)
        self.FightWillSlider.setObjectName("FightWillSlider")
        QtCore.QObject.connect(self.FightWillSlider, QtCore.SIGNAL("valueChanged(int)"), self.FightWillMoved)

        
        self.LoreLuckSlider = QtGui.QSlider(self.tab)
        self.LoreLuckSlider.setGeometry(QtCore.QRect(80, 250, 231, 31))
        self.LoreLuckSlider.setMaximum(3)
        self.LoreLuckSlider.setPageStep(1)
        self.LoreLuckSlider.setSliderPosition(Player.Slider3)
        self.LoreLuckSlider.setOrientation(QtCore.Qt.Horizontal)
        self.LoreLuckSlider.setObjectName("LoreLuckSlider")
        QtCore.QObject.connect(self.LoreLuckSlider, QtCore.SIGNAL("valueChanged(int)"), self.LoreLuckMoved)

        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 46, 13))
        
        self.SpeedValueBox = QtGui.QLabel(self.tab)
        self.SpeedValueBox.setGeometry(QtCore.QRect(80, 110, 20, 21))
        
        self.SneakValueBox = QtGui.QLabel(self.tab)
        self.SneakValueBox.setGeometry(QtCore.QRect(80, 130, 20, 21))
        self.SpeedValueBox_2 = QtGui.QLabel(self.tab)
        self.SpeedValueBox_2.setGeometry(QtCore.QRect(150, 110, 20, 21))
        self.SneakValueBox_2 = QtGui.QLabel(self.tab)
        self.SneakValueBox_2.setGeometry(QtCore.QRect(150, 130, 20, 21))
        self.SpeedValueBox_3 = QtGui.QLabel(self.tab)
        self.SpeedValueBox_3.setGeometry(QtCore.QRect(220, 110, 20, 21))
        self.SneakValueBox_3 = QtGui.QLabel(self.tab)
        self.SneakValueBox_3.setGeometry(QtCore.QRect(220, 130, 20, 21))
        self.SpeedValueBox_4 = QtGui.QLabel(self.tab)
        self.SpeedValueBox_4.setGeometry(QtCore.QRect(290, 110, 20, 21))
        self.SneakValueBox_4 = QtGui.QLabel(self.tab)
        self.SneakValueBox_4.setGeometry(QtCore.QRect(290, 130, 20, 21))
        self.FightValueBox_3 = QtGui.QLabel(self.tab)
        self.FightValueBox_3.setGeometry(QtCore.QRect(220, 200, 20, 21))
        self.FightValueBox = QtGui.QLabel(self.tab)
        self.FightValueBox.setGeometry(QtCore.QRect(80, 200, 20, 21))
        self.WillValueBox_4 = QtGui.QLabel(self.tab)
        self.WillValueBox_4.setGeometry(QtCore.QRect(290, 220, 20, 21))
        self.WillValueBox_3 = QtGui.QLabel(self.tab)
        self.WillValueBox_3.setGeometry(QtCore.QRect(220, 220, 20, 21))
        self.WillValueBox_2 = QtGui.QLabel(self.tab)
        self.WillValueBox_2.setGeometry(QtCore.QRect(150, 220, 20, 21))
        self.FightValueBox_2 = QtGui.QLabel(self.tab)
        self.FightValueBox_2.setGeometry(QtCore.QRect(150, 200, 20, 21))
        self.WillValueBox = QtGui.QLabel(self.tab)
        self.WillValueBox.setGeometry(QtCore.QRect(80, 220, 20, 21))
        self.FightValueBox_4 = QtGui.QLabel(self.tab)
        self.FightValueBox_4.setGeometry(QtCore.QRect(290, 200, 20, 21))
        self.LoreValueBox_3 = QtGui.QLabel(self.tab)
        self.LoreValueBox_3.setGeometry(QtCore.QRect(220, 290, 20, 21))
        self.LoreValueBox = QtGui.QLabel(self.tab)
        self.LoreValueBox.setGeometry(QtCore.QRect(80, 290, 20, 21))
        self.LuckValueBox_4 = QtGui.QLabel(self.tab)
        self.LuckValueBox_4.setGeometry(QtCore.QRect(290, 310, 20, 21))
        self.LuckValueBox_3 = QtGui.QLabel(self.tab)
        self.LuckValueBox_3.setGeometry(QtCore.QRect(220, 310, 20, 21))
        self.LuckValueBox_2 = QtGui.QLabel(self.tab)
        self.LuckValueBox_2.setGeometry(QtCore.QRect(150, 310, 20, 21))
        self.LoreValueBox_2 = QtGui.QLabel(self.tab)
        self.LoreValueBox_2.setGeometry(QtCore.QRect(150, 290, 20, 21))
        self.LuckValueBox = QtGui.QLabel(self.tab)
        self.LuckValueBox.setGeometry(QtCore.QRect(80, 310, 20, 21))
        self.LoreValueBox_4 = QtGui.QLabel(self.tab)
        self.LoreValueBox_4.setGeometry(QtCore.QRect(290, 290, 20, 21))
        self.MegaTabBox.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_8 = QtGui.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(20, 80, 91, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtGui.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(20, 140, 111, 16))
        self.label_9.setObjectName("label_9")
        self.FixedPossessionText = QtGui.QLabel(self.tab_2)
        self.FixedPossessionText.setGeometry(QtCore.QRect(140, 80, 171, 51))
        self.RandomPossessionText = QtGui.QLabel(self.tab_2)
        self.RandomPossessionText.setGeometry(QtCore.QRect(140, 140, 171, 51))
        self.label_10 = QtGui.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(20, 220, 71, 16))
        self.label_10.setObjectName("label_10")
        self.SpecialPowerText = QtGui.QLabel(self.tab_2)
        self.SpecialPowerText.setGeometry(QtCore.QRect(20, 240, 271, 101))
        self.label_12 = QtGui.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(20, 20, 46, 13))
        self.label_12.setObjectName("label_12")
        self.HomeText = QtGui.QLabel(self.tab_2)
        self.HomeText.setGeometry(QtCore.QRect(140, 20, 171, 31))
        self.MegaTabBox.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_11 = QtGui.QLabel(self.tab_3)
        self.label_11.setGeometry(QtCore.QRect(20, 20, 101, 16))
        self.label_11.setObjectName("label_11")
        self.StoryText = QtGui.QLabel(self.tab_3)
        self.StoryText.setGeometry(QtCore.QRect(20, 40, 281, 301))
        self.StoryText.setAlignment(QtCore.Qt.AlignLeft)
        self.StoryText.setAlignment(QtCore.Qt.AlignTop)
        self.MegaTabBox.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        
        self.HighlightedItemPic = QtGui.QPushButton(self.tab_4)
        self.HighlightedItemPic.setGeometry(QtCore.QRect(10, 190, 111, 161))
        self.HighlightedItemPic.setObjectName("HighlightedItemPic")
        self.HighlightedItemPic.setIconSize(QtCore.QSize(111,161))
        self.HighlightedItemPic.setFlat(1)
        
        self.EquipPic2 = QtGui.QPushButton(self.tab_4)
        self.EquipPic2.setGeometry(QtCore.QRect(140, 10, 111, 161))
        self.EquipPic2.setObjectName("EquipPic2")
        self.EquipPic2.setIconSize(QtCore.QSize(111,161))
        self.EquipPic2.setFlat(1)
        
        self.EquipPic1 = QtGui.QPushButton(self.tab_4)
        self.EquipPic1.setGeometry(QtCore.QRect(10, 10, 111, 161))
        self.EquipPic1.setObjectName("EquipPic1")
        self.EquipPic1.setIconSize(QtCore.QSize(111,161))
        self.EquipPic1.setFlat(1)
        
        self.comboBox = QtGui.QComboBox(self.tab_4)
        self.comboBox.setGeometry(QtCore.QRect(160, 190, 151, 31))
        self.comboBox.setObjectName("comboBox")
        self.UseButton = QtGui.QPushButton(self.tab_4)
        self.UseButton.setGeometry(QtCore.QRect(170, 230, 75, 23))
        self.UseButton.setObjectName("useButton")
        self.DiscardButton = QtGui.QPushButton(self.tab_4)
        self.DiscardButton.setGeometry(QtCore.QRect(170, 310, 75, 23))
        self.DiscardButton.setObjectName("DiscardButton")
        self.UnequipButton = QtGui.QPushButton(self.tab_4)
        self.UnequipButton.setGeometry(QtCore.QRect(170, 270, 75, 23))
        self.UnequipButton.setObjectName("UnequipButton")
        
        self.MegaTabBox.addTab(self.tab_4, "")
        self.StaminaValue = QtGui.QLCDNumber(Dialog)
        self.StaminaValue.setGeometry(QtCore.QRect(160, 202, 41, 41))
        
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        
        self.StaminaValue.setFont(font)
        self.StaminaValue.setObjectName("StaminaValue")
        self.SanityValue = QtGui.QLCDNumber(Dialog)
        self.SanityValue.setGeometry(QtCore.QRect(160, 250, 41, 41))    
        self.SanityValue.setFont(font)
        self.SanityValue.setObjectName("SanityValue")
        self.SanityBrain = QtGui.QLabel(Dialog)
        self.SanityBrain.setGeometry(QtCore.QRect(20, 250, 131, 51))
        self.SanityBrain.setObjectName("SanityBrain")
        self.StaminaHeart = QtGui.QLabel(Dialog)
        self.StaminaHeart.setGeometry(QtCore.QRect(20, 200, 131, 51))
        self.StaminaHeart.setObjectName("StaminaHeart")
        self.CurrentLocationBox = QtGui.QLabel(Dialog)
        self.CurrentLocationBox.setGeometry(QtCore.QRect(20, 310, 181, 31))
        self.OkayButton = QtGui.QPushButton(Dialog)
        self.OkayButton.setGeometry(QtCore.QRect(434, 392, 101, 31))
        self.OkayButton.setObjectName("OkayButton")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.MonsterTrophiePic = QtGui.QLabel(self.tab_5)
        self.MonsterTrophiePic.setGeometry(QtCore.QRect(20, 10, 171, 181))
        self.MonsterTrophiePic.setObjectName("MonsterTrophiePic")
        self.MonsterTrophieComboBox = QtGui.QComboBox(self.tab_5)
        self.MonsterTrophieComboBox.setGeometry(QtCore.QRect(20, 260, 271, 21))
        self.MonsterTrophieComboBox.setObjectName("MonsterTrophieComboBox")
        self.MegaTabBox.addTab(self.tab_5, "")

        #Allow the words to wrap around in several text labels
        self.SpecialPowerText.setWordWrap(1)
        self.NameLabel.setWordWrap(1)
        self.FixedPossessionText.setWordWrap(1)
        self.RandomPossessionText.setWordWrap(1)
        self.SpecialPowerText.setWordWrap(1)
        self.HomeText.setWordWrap(1)
        self.StoryText.setWordWrap(1)
        self.CurrentLocationBox.setWordWrap(1)

        
        
        self.retranslateUi(Dialog, Player)
        self.MegaTabBox.setCurrentIndex(0)

        #Connect buttons to their functions
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("activated(int)"), self.SelectedItem)
        QtCore.QObject.connect(self.MonsterTrophieComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.SelectedTrophie)
        QtCore.QObject.connect(self.UseButton, QtCore.SIGNAL("clicked()"), self.UseItem)
        QtCore.QObject.connect(self.DiscardButton, QtCore.SIGNAL("clicked()"), self.DiscardItem)
        QtCore.QObject.connect(self.UnequipButton, QtCore.SIGNAL("clicked()"), self.UnequipItem)
        QtCore.QObject.connect(self.EquipPic1, QtCore.SIGNAL("clicked()"), self.EquipLeftItem)
        QtCore.QObject.connect(self.EquipPic2, QtCore.SIGNAL("clicked()"), self.EquipRightItem)
        QtCore.QObject.connect(self.HighlightedItemPic, QtCore.SIGNAL("clicked()"), self.ShowBigCard)
        
        QtCore.QObject.connect(self.OkayButton, QtCore.SIGNAL("clicked()"), self.OkayClicked)

        #Investigator screen displays the Players picture
        self.InvestigatorImageBox.setPixmap(QtGui.QPixmap(self.Player.Graphic).scaledToHeight(161))
        
        #161 is the height of Investigator Image Box

        #Fetch the path of stamina/sanity.jpg
        OtherPath = os.getcwd()
        length = len(os.getcwd())
        OtherPath = OtherPath[0:(length - 7)]
        if(OtherPath[len(OtherPath)-1] == "\\"):
             OtherPath = OtherPath + "data\\Other\\"
        if(OtherPath[len(OtherPath)-1] == "/"):
            OtherPath = OtherPath + "data/Other/"
    
        self.StaminaHeart.setPixmap(QtGui.QPixmap(OtherPath + "stamina.jpg"))
        self.SanityBrain.setPixmap(QtGui.QPixmap(OtherPath + "sanity.jpg"))


        #Check and initialize the various labels and buttons
        self.CheckSliders()
        self.SelectedItem(0)
        
        
        self.UpdateComboBox()
        self.UpdatePictures()
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.CheckSliders()

    #All the various updates
    def OnOpen(self):
        self.CheckSliders()
        self.UpdateComboBox()
        self.SelectedItem(0)
        self.UpdatePictures()
        self.UpdateStats()
        self.retranslateUi(self.Dialog, self.Player)

    #Check to see if sliders should be locked
    def CheckSliders(self):
        
        if(self.Player.Stats["Focus"] < 1):
            self.SpeedSneakSlider.setDisabled(1)
            self.FightWillSlider.setDisabled(1)
            self.LoreLuckSlider.setDisabled(1)
        else:
            self.SpeedSneakSlider.setDisabled(0)
            self.FightWillSlider.setDisabled(0)
            self.LoreLuckSlider.setDisabled(0)

    #Make the labels display the correct text/img
    def retranslateUi(self, Dialog, Player):

        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", str(self.Player.Name), None, QtGui.QApplication.UnicodeUTF8))
        self.UpdateStats()
        self.MegaTabBox.setTabText(self.MegaTabBox.indexOf(self.StatsTab), QtGui.QApplication.translate("Dialog", "Stats", None, QtGui.QApplication.UnicodeUTF8))

        self.NameLabel.setText(QtGui.QApplication.translate("Dialog", str(self.Player.Name) + " " + str(self.Player.Title), None, QtGui.QApplication.UnicodeUTF8))

        self.label.setText(QtGui.QApplication.translate("Dialog", "Focus Remaining:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Sneak", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Will", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Fight", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Luck", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Lore", None, QtGui.QApplication.UnicodeUTF8))
        self.MegaTabBox.setTabText(self.MegaTabBox.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Stat Adjustment", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Fixed Possessions:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Random Possessions:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "Special Power:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "Home:", None, QtGui.QApplication.UnicodeUTF8))
        self.MegaTabBox.setTabText(self.MegaTabBox.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "The Story So Far:", None, QtGui.QApplication.UnicodeUTF8))
        self.MegaTabBox.setTabText(self.MegaTabBox.indexOf(self.tab_3), QtGui.QApplication.translate("Dialog", "Story", None, QtGui.QApplication.UnicodeUTF8))
        self.UseButton.setText(QtGui.QApplication.translate("Dialog", "Use", None, QtGui.QApplication.UnicodeUTF8))
        self.DiscardButton.setText(QtGui.QApplication.translate("Dialog", "Discard", None, QtGui.QApplication.UnicodeUTF8))
        self.UnequipButton.setText(QtGui.QApplication.translate("Dialog", "Unequip", None, QtGui.QApplication.UnicodeUTF8))
        self.MegaTabBox.setTabText(self.MegaTabBox.indexOf(self.tab_4), QtGui.QApplication.translate("Dialog", "Inventory", None, QtGui.QApplication.UnicodeUTF8))
        self.MegaTabBox.setTabText(self.MegaTabBox.indexOf(self.tab_5), QtGui.QApplication.translate("Dialog", "Trophies", None, QtGui.QApplication.UnicodeUTF8))

        self.OkayButton.setText(QtGui.QApplication.translate("Dialog", "Okay", None, QtGui.QApplication.UnicodeUTF8))
        
        self.SpeedValueBox.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Speed"])), None, QtGui.QApplication.UnicodeUTF8))
        self.SpeedValueBox_2.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Speed"])+1), None, QtGui.QApplication.UnicodeUTF8))
        self.SpeedValueBox_3.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Speed"])+2), None, QtGui.QApplication.UnicodeUTF8))
        self.SpeedValueBox_4.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Speed"])+3), None, QtGui.QApplication.UnicodeUTF8))
                
        self.SneakValueBox.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Sneak"])), None, QtGui.QApplication.UnicodeUTF8))
        self.SneakValueBox_2.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Sneak"])-1), None, QtGui.QApplication.UnicodeUTF8))
        self.SneakValueBox_3.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Sneak"])-2), None, QtGui.QApplication.UnicodeUTF8))
        self.SneakValueBox_4.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Sneak"])-3), None, QtGui.QApplication.UnicodeUTF8))
                
        self.FightValueBox.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Fight"])), None, QtGui.QApplication.UnicodeUTF8))
        self.FightValueBox_2.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Fight"])+1), None, QtGui.QApplication.UnicodeUTF8))
        self.FightValueBox_3.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Fight"])+2), None, QtGui.QApplication.UnicodeUTF8))
        self.FightValueBox_4.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Fight"])+3), None, QtGui.QApplication.UnicodeUTF8))
                
        self.WillValueBox.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Will"])), None, QtGui.QApplication.UnicodeUTF8))
        self.WillValueBox_2.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Will"])-1), None, QtGui.QApplication.UnicodeUTF8))
        self.WillValueBox_3.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Will"])-2), None, QtGui.QApplication.UnicodeUTF8))
        self.WillValueBox_4.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Will"])-3), None, QtGui.QApplication.UnicodeUTF8))
                
        self.LoreValueBox.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Lore"])), None, QtGui.QApplication.UnicodeUTF8))
        self.LoreValueBox_2.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Lore"])+1), None, QtGui.QApplication.UnicodeUTF8))
        self.LoreValueBox_3.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Lore"])+2), None, QtGui.QApplication.UnicodeUTF8))
        self.LoreValueBox_4.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Lore"])+3), None, QtGui.QApplication.UnicodeUTF8))
                
        self.LuckValueBox.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Luck"])), None, QtGui.QApplication.UnicodeUTF8))
        self.LuckValueBox_2.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Luck"])-1), None, QtGui.QApplication.UnicodeUTF8))
        self.LuckValueBox_3.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Luck"])-2), None, QtGui.QApplication.UnicodeUTF8))
        self.LuckValueBox_4.setText(QtGui.QApplication.translate("Dialog", str(int(Player.BaseStats["Luck"])-3), None, QtGui.QApplication.UnicodeUTF8))




        self.FixedPossessionText.setText(QtGui.QApplication.translate("Dialog", str(Player.FixedPossessions), None, QtGui.QApplication.UnicodeUTF8))
        self.RandomPossessionText.setText(QtGui.QApplication.translate("Dialog", str(Player.RandomPossessions), None, QtGui.QApplication.UnicodeUTF8))
        self.SpecialPowerText.setText(QtGui.QApplication.translate("Dialog", str(Player.UniqueAbilityFlavorText), None, QtGui.QApplication.UnicodeUTF8))
        self.HomeText.setText(QtGui.QApplication.translate("Dialog", str(Player.Home), None, QtGui.QApplication.UnicodeUTF8))
        self.StoryText.setText(QtGui.QApplication.translate("Dialog", str(Player.Story), None, QtGui.QApplication.UnicodeUTF8))
        self.CurrentLocationBox.setText(QtGui.QApplication.translate("Dialog", "Location: " + str(Player.Location.Name), None, QtGui.QApplication.UnicodeUTF8))

        
        

    #Functions called whenever a stat slider is moved 
    def SpeedSneakMoved(self, x):
        self.Player.ChangeMobilitySlider(x - self.Player.Slider1)
        self.Player.Slider1 = x
        
        self.UpdateStats()
        #Check for disable
        if(self.Player.Stats["Focus"] < 1):
            self.SpeedSneakSlider.setDisabled(1)
            self.FightWillSlider.setDisabled(1)
            self.LoreLuckSlider.setDisabled(1)
        
    
    def FightWillMoved(self, x):        
        self.Player.ChangeCombatSlider(x - self.Player.Slider2)
        self.Player.Slider2 = x
        self.UpdateStats()
        if(self.Player.Stats["Focus"] < 1):
            self.SpeedSneakSlider.setDisabled(1)
            self.FightWillSlider.setDisabled(1)
            self.LoreLuckSlider.setDisabled(1)
        
    
    def LoreLuckMoved(self, x):
        self.Player.ChangeMentalSlider(x - self.Player.Slider3)
        self.Player.Slider3 = x
        self.UpdateStats()
        if(self.Player.Stats["Focus"] < 1):
            self.SpeedSneakSlider.setDisabled(1)
            self.FightWillSlider.setDisabled(1)
            self.LoreLuckSlider.setDisabled(1)
    #Makes the screen display the changed stats
    def UpdateStats(self):
        self.SpeedStat.setText(QtGui.QApplication.translate("Dialog", "Speed: " + str(self.Player.Stats["Speed"] + self.Player.BonusStats["Speed"]), None, QtGui.QApplication.UnicodeUTF8))
        self.SneakStat.setText(QtGui.QApplication.translate("Dialog", "Sneak: " + str(self.Player.Stats["Sneak"] + self.Player.BonusStats["Sneak"]), None, QtGui.QApplication.UnicodeUTF8))
        self.FightStat.setText(QtGui.QApplication.translate("Dialog", "Fight: " + str(self.Player.Stats["Fight"] + self.Player.BonusStats["Fight"]), None, QtGui.QApplication.UnicodeUTF8))
        self.WillStat.setText(QtGui.QApplication.translate("Dialog", "Will: " + str(self.Player.Stats["Will"] + self.Player.BonusStats["Will"]), None, QtGui.QApplication.UnicodeUTF8))
        self.LoreStat.setText(QtGui.QApplication.translate("Dialog", "Lore:" + str(self.Player.Stats["Lore"] + self.Player.BonusStats["Lore"]), None, QtGui.QApplication.UnicodeUTF8))
        self.LuckStat.setText(QtGui.QApplication.translate("Dialog", "Luck:" + str(self.Player.Stats["Luck"] + self.Player.BonusStats["Luck"]), None, QtGui.QApplication.UnicodeUTF8))
        self.FocusRemainingBox.setText(QtGui.QApplication.translate("Dialog", str(self.Player.Stats["Focus"] + self.Player.BonusStats["Focus"]), None, QtGui.QApplication.UnicodeUTF8))
        if(self.Player.Environment.CurrentPhase == "Setup"):
            #Lets the user know that they can spend unlimited focus
            self.FocusRemainingBox.setText(str("Unlimited"))
        self.Clues.setText(QtGui.QApplication.translate("Dialog", "Clues:" + str(self.Player.Clues), None, QtGui.QApplication.UnicodeUTF8))
        self.Money.setText(QtGui.QApplication.translate("Dialog", "Money:" + str(self.Player.Money), None, QtGui.QApplication.UnicodeUTF8))
        self.Statuses.setText(QtGui.QApplication.translate("Dialog", "Statuses: " + str(self.CalcStatusText()), None, QtGui.QApplication.UnicodeUTF8))
        
        self.SanityValue.display(int(self.Player.Stats["Sanity"]))
        self.StaminaValue.display(int(self.Player.Stats["Stamina"]))

    def UpdateComboBox(self):
        x = 0
        self.comboBox.clear()
        #Add items to the combobox based on player inventory
        while x < len(self.Player.ItemList):
            self.comboBox.addItem(self.Player.ItemList[x][0])
            x = x + 1
        self.TotalTrophies = self.Player.GateTrophies + self.Player.MonsterTrophies
        for element in self.TotalTrophies:
            self.MonsterTrophieComboBox.addItem(element.Name)
            
    def SelectedItem(self, x):
        #If player owns no cards.  Select a temporary card
        if(len(self.Player.ItemList) < 1):
            self.Player.SelectedCard = self.NoItemCard()
        else:
            self.SelectedCard = self.Player.ItemList[x]

        

        self.UpdatePictures()
        
        
    #A temporary card that displays the no item picture
    def NoItemCard(self):
        card = self.Env.DeckDictionary['Special'].DrawCard("deck", "No Items")
        return card
    #Changes the picture of the selected trophy    
    def SelectedTrophie(self, x):
        if(self.TotalTrophies != []):
            self.Trophy = self.TotalTrophies[x]
        else:
            self.Trophy = None
        self.UpdatePictures()
        

    #Make sure all the elements that should have pictures do
    #Check and make sure we never access the picture of an empty object
    def UpdatePictures(self):
        if(self.Trophy != None):
            self.MonsterTrophiePic.setPixmap(QtGui.QPixmap(self.Trophy.Picture).scaledToHeight(171))
        self.HighlightedItemPic.setIcon(QtGui.QIcon(self.SelectedCard[2]))
        if(self.Player.RightHandItem != []):
            self.EquipPic2.setIcon(QtGui.QIcon(self.Player.RightHandItem[2]))
        else:
            self.Player.RightHandItem = self.NoItemCard()
            self.EquipPic2.setIcon(QtGui.QIcon(self.Player.RightHandItem[2]))
        if(self.Player.LeftHandItem != []):
            self.EquipPic1.setIcon(QtGui.QIcon(self.Player.LeftHandItem[2]))
        else:
            self.Player.LeftHandItem = self.NoItemCard()
            self.EquipPic1.setIcon(QtGui.QIcon(self.Player.LeftHandItem[2]))
            
        

    def EquipLeftItem(self):
        #If the item isn't in the right hand. Unequip the current lefthand
        #Then equip the card.
        if(self.Player.RightHandItem != self.SelectedCard):
            if(self.Player.LeftHandItem[0] != "No Items"):
                self.Player.Unequip(self.Player.LeftHandItem)
            self.Player.LeftHandItem = self.SelectedCard
            print "Equip Item (Left): " + self.Player.LeftHandItem[0]
            self.Player.Equip(self.SelectedCard)
        #If the item is in the right hand. Swap the items
        else:
            self.Player.LeftHandItem, self.Player.RightHandItem = self.Player.RightHandItem, self.Player.LeftHandItem
        self.UpdatePictures()
        self.UpdateStats()
    #Same as EquipLeftHand
    def EquipRightItem(self):
        if(self.Player.LeftHandItem != self.SelectedCard):
            if(self.Player.RightHandItem[0] != "No Items"):
                self.Player.Unequip(self.Player.RightHandItem)
            self.Player.RightHandItem = self.SelectedCard
            print "Equip Item (Right): " + self.Player.RightHandItem[0]
            self.Player.Equip(self.SelectedCard)
        else:
            self.Player.LeftHandItem, self.Player.RightHandItem = self.Player.RightHandItem, self.Player.LeftHandItem
        self.UpdatePictures()
        self.UpdateStats()

    #Make sure the selected card is not the filler card.
    #Then use it
    def UseItem(self):
        if(self.SelectedCard[0] != "No Items"):
            print "Used Item: " + self.SelectedCard[0]
            self.Player.UseItem(self.SelectedCard)
        self.UpdatePictures()
        self.UpdateStats()
        self.UpdateComboBox()
        
    #Make sure the selected card is not the filler card.
    #Then discard it
    def DiscardItem(self):
        if(self.SelectedCard[0] != "No Items"):
            self.UnequipItem()
            print "Discard Item: " + self.SelectedCard[0]
            self.Player.Discard(self.SelectedCard)
        self.SelectedItem(0)
        self.UpdatePictures()
        self.UpdateStats()
        self.UpdateComboBox()
        
    #Unequip all equipped player items
    def UnequipItem(self):
        self.Player.UnequipItems()
        
        self.UpdatePictures()
        self.UpdateStats()
        self.UpdateComboBox()
    #used for testing temp items.  NOT USED
    def FindItemPath(self):
        ItemPath = os.getcwd()
        length = len(os.getcwd())
        ItemPath = ItemPath[0:(length - 7)]
        if(ItemPath[len(ItemPath)-1] == "\\"):
            ItemPath = ItemPath + "data\\Item\\Images\\"
        if(ItemPath[len(ItemPath)-1] == "/"):
            ItemPath = ItemPath + "data/Item/Images/"
        return ItemPath

    #Determine which text to  put in the status part of the screen
    def CalcStatusText(self):
        Text = ""
        if(self.Player.Status["Blessed"] != 0):
            Text = Text + "   Blessed"
        if(self.Player.Status["Cursed"] != 0):
            Text = Text + "   Cursed"
        if(self.Player.Status["Retainer"] != 0):
            Text = Text + "   Retainer"
        if(self.Player.Status["SilverLodgeMember"] != 0):
            Text = Text + "   Silver Lodge Member"            
        if(self.Player.Status["Deputy"] != 0):
            Text = Text + "   Deputy"
        if(self.Player.Status["BankLoan"] != 0):
            Text = Text + "   Bank Loan"
        if(self.Player.Status["Delayed"] != 0):
            Text = Text + "   Delayed"
        if(self.Player.Status["Lost"] != 0):
            Text = Text + "   Lost"

    #When the selected card is clicked.  use ViewCard.py
    def ShowBigCard(self):
        ViewCard.viewCard(self.SelectedCard)

    #Properly close the window
    def OkayClicked(self):
        self.Dialog.close()
        self.app.exit()
        
        
class Window(QtGui.QDialog):
    def DoStuff(self,app, Player, Env):
        parent=None
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(app,self, Player, Env)
        
    def keyPressEvent(self, event):
        if(event.key() == QtCore.Qt.Key_Enter):
            self.ui.OkayClicked()
        if(event.key() == QtCore.Qt.Key_Return):
            self.ui.OkayClicked()
    
def viewPlayer(Player, Env):
    app = QtCore.QEventLoop()
    window = Window()
    window.DoStuff(app,Player,Env)
    window.show()
    app.exec_()

    
    
    
