import characterscreen
import sys
import os
import PlayerCharacter
import XmlLoader
import combat
import DiceRoller
import SingleDie
import final
"""
Uses Environment.  Requires an environment to be passed to it to work

sava0751 - This file now has all of my code updates from map3.py, which is my
    test file.  It will now be pulled into this file for use with the rest
    of the program.  :)
"""

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class stationaryPixmap(QGraphicsPixmapItem):
    def __init__(self, pixmap, named, Map):        
        QPixmap.__init__(self, pixmap)
        self.Map = Map
        self.name = named
        self.setAcceptHoverEvents(True)
        self.timeLine = QTimeLine()
        self.animation = QGraphicsItemAnimation()

    def animatedMove(self, destPoint):
        self.animation.setItem(self)
        self.animation.setTimeLine(self.timeLine)
        self.animation.setPosAt(0, self.sceneBoundingRect().topLeft())
        self.animation.setPosAt(1, destPoint)

        self.timeLine.setDuration(2000)
        if self.timeLine.state() == QTimeLine.NotRunning:
            self.timeLine.start()

    def hoverEnterEvent(self, event):
        self.setZValue(1)
        self.setScale(.15)

    def hoverLeaveEvent(self, event):
        self.setZValue(0)
        self.setScale(.1)

class clueToken(QGraphicsPixmapItem):
    def __init__(self, pixmap, Map, Location):
        QPixmap.__init__(self, pixmap)
        self.Location = Location
        self.Map = Map
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setZValue(1)
        number = self.Location.ClueTokens
        self.Map.sceneItems[self.Location.Name + "clueNumber"] = self.Map.scene.addText(str(self.Location.ClueTokens))
        self.Map.sceneItems[self.Location.Name + "clueNumber"].setDefaultTextColor(Qt.darkBlue)
        brect = self.Map.sceneItems[self.Location.Name + "clue"].sceneBoundingRect()
        self.Map.sceneItems[self.Location.Name + "clueNumber"].setPos(brect.left(), (brect.bottom() - (brect.height() / 2)))
        self.Map.sceneItems[self.Location.Name + "clueNumber"].setScale(4)
        self.Map.view.update()

    def hoverLeaveEvent(self, event):
        self.setZValue(0)
        self.Map.scene.removeItem(self.Map.sceneItems[self.Location.Name + "clueNumber"])
        self.Map.scene.update()
    
class custPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, named, Map):
        border = pixmap.rect().adjusted(0, 0, 100, 100)
        self.pixmap2 = QPixmap(border.width(), border.height())
        self.painter = QPainter(self.pixmap2)
        self.painter.save()
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(Qt.darkRed)
        self.painter.drawRoundRect(border, 15, 15)
        self.painter.drawPixmap(50, 50, pixmap)
        self.painter.restore()
        
        QGraphicsPixmapItem.__init__(self, self.pixmap2)
        self.Map = Map
        self.name = named
        self.timeLine = QTimeLine()
        self.pulseTimeLine = QTimeLine()
        self.animation = QGraphicsItemAnimation()
        self.pulseAnimation = QGraphicsItemAnimation()
        self.setAcceptHoverEvents(True)

    def animatedMove(self, destPoint):
        self.animation.setItem(self)
        self.animation.setTimeLine(self.timeLine)
        self.animation.setPosAt(0, self.sceneBoundingRect().topLeft())
        self.animation.setPosAt(1, destPoint)

        self.timeLine.setDuration(2000)
        if self.timeLine.state() == QTimeLine.NotRunning:
            self.timeLine.start()

    def pulseAnimationStart(self):
        self.pulseAnimation.setItem(self)
        self.pulseAnimation.setTimeLine(self.pulseTimeLine)
        self.pulseAnimation.setScaleAt(0, 1, 1)
        self.pulseAnimation.setScaleAt(.5, 1.5, 1.5)
        self.pulseAnimation.setScaleAt(1, 1, 1)

        self.pulseTimeLine.setDuration(1000)
        self.pulseTimeLine.setLoopCount(0)
        if self.pulseTimeLine.state() == QTimeLine.NotRunning:
            self.pulseTimeLine.start()

    def pulseAnimationEnd(self):
        if self.pulseTimeLine.state() == QTimeLine.Running:
            self.pulseTimeLine.stop()
        

    def hoverEnterEvent(self, event):
        self.setZValue(1)
        self.setScale(.15)

    def hoverLeaveEvent(self, event):
        self.setZValue(0)
        self.setScale(.1)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            event.ignore()
            return

        if self.Map.Environment.PlayerByName(self.name) != self.Map.Environment.CurrentPlayer:
            event.ignore()
            return

        if self.Map.Environment.CurrentPhase != "Movement":
            event.ignore()
            return
        
        self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        drag = QDrag(event.widget())
        mime = QMimeData()
        mime.setText(self.name)
        drag.setMimeData(mime)
        print self.name + " is moving"
        temp = self.pixmap()

        #temp.setMask(temp.createHeuristicMask())
        
        drag.setPixmap(temp.scaledToHeight(40))
        drag.setHotSpot(QPoint(15, 20))
        drag.exec_()
        

class mapLocationBox(QGraphicsRectItem):
    def __init__(self, rectF, name, Map):
        QGraphicsRectItem.__init__(self, rectF)
        self.name = name
        self.Map = Map
        self.rect = rectF
        pen = QPen()
        pen.setStyle(Qt.NoPen)
        self.setAcceptDrops(True)
        self.setBrush(Qt.green)
        self.setPen(pen)
        self.setOpacity(.001)

    def dragEnterEvent(self, event):
        event.setAccepted(True)
        #self.setBrush(Qt.red)
        self.setOpacity(.5)

    def dragLeaveEvent(self, event):
        #self.setBrush(Qt.darkGray)
        self.setOpacity(.001)

    def dropEvent(self, event):
        self.setOpacity(.001)
        print event.mimeData().text() + " went to " + self.name

        if self.Map.Environment.PlayerByName(event.mimeData().text()) == self.Map.Environment.CurrentPlayer :
            if self.Map.Environment.CurrentPlayer.CurrentMovementPoints == 0:
                return self.Map.Environment.PrintEvent("Movement","You have no more movement points. Click 'Done' to end your turn.")
            self.Map.Environment.MultiSpaceMovement(self.Map.Environment.PlayerByName(event.mimeData().text()), self.Map.Environment.Locations[self.name])
        
class logWindow(QTextEdit):
    def __init__(self):
        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)

    def addLine(self, Line):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(Line)
        self.insertPlainText("\n")

    def addBreak(self):
        column = self.width() / 7.5
        self.addLine("-" * int(column))

class MapWindow(QWidget):
    zoomLevel = 1
    sceneItems = {}
    MapBoxes = {}
    animationQueue = QSequentialAnimationGroup()
    
    def __init__(self, Envir):
        parent = None
        QWidget.__init__(self, parent)
        self.CurrentTurn = 0
        self.setWindowTitle(QApplication.translate("", "Arkham Horror", None, QApplication.UnicodeUTF8))
        self.Environment = Envir

        self.TestMons = ""

        self.view = QGraphicsView()
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.resizeEvent = self.viewResizeEvent

        self.ancientOneView = QGraphicsView()
        self.ancientOneView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ancientOneView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.zoomInButton = QPushButton(self.tr("&Zoom In"))
        self.zoomOutButton = QPushButton(self.tr("Zoom &Out"))
        self.rotateButton = QPushButton(self.tr("&Rotate Map"))
        self.investigatorButton = QPushButton(self.tr("&Investigator"))
       
        self.turnButton = QPushButton(self.tr("&Done"))
        self.FinalButton = QPushButton(self.tr("&Final"))
        self.phaseLabel = QLabel(self.tr(self.Environment.CurrentPhase + " Phase"))
        self.curPlayerLabel = QLabel(self.tr(self.Environment.CurrentPlayer.Name + "'s turn"))
        self.curPlayerMovePointsLabel = QLabel(self.tr("Movement Points Remaining: " + str(self.Environment.CurrentPlayer.CurrentMovementPoints)))
        self.doomLabel = QLabel(self.tr("Doom Level: " + str(self.Environment.AncientOne.CurrentDoom)))
        self.terrorLabel = QLabel(self.tr("Terror Level: " + str(self.Environment.TerrorLevel)))
        self.log = logWindow()
        self.centerCurPlayerButton = QPushButton(self.tr("&Center on Current Player"))
        
        self.phaseLabel.setFrameStyle(QFrame.Box)
        self.curPlayerLabel.setFrameStyle(QFrame.Box)
        self.curPlayerMovePointsLabel.setFrameStyle(QFrame.Box)
        self.curPlayerMovePointsLabel.setVisible(False)
        self.doomLabel.setFrameStyle(QFrame.Box)
        self.terrorLabel.setFrameStyle(QFrame.Box)
        
        self.connect(self.zoomInButton, SIGNAL("clicked()"), self.zoomIn)
        self.connect(self.zoomOutButton, SIGNAL("clicked()"), self.zoomOut)
        self.connect(self.rotateButton, SIGNAL("clicked()"), self.rotateMap)
        self.connect(self.investigatorButton, SIGNAL("clicked()"), self.showInvestigator)
        self.connect(self.centerCurPlayerButton, SIGNAL("clicked()"), self.centerOnCurPlayer)
       
        self.connect(self.turnButton, SIGNAL("clicked()"), self.endTurn)
        self.connect(self.FinalButton, SIGNAL("clicked()"), self.Final)
        
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.terrorLabel, 0, 0)
        buttonLayout.addWidget(self.doomLabel, 0, 1)
        buttonLayout.addWidget(self.zoomInButton, 1, 1)
        buttonLayout.addWidget(self.phaseLabel, 1, 0)
        buttonLayout.addWidget(self.zoomOutButton, 2, 1)
        buttonLayout.addWidget(self.curPlayerLabel, 2, 0)
        buttonLayout.addWidget(self.rotateButton, 3, 1)
        buttonLayout.addWidget(self.curPlayerMovePointsLabel, 3, 0)
        buttonLayout.addWidget(self.investigatorButton, 4, 1)
        
        buttonLayout.addWidget(self.turnButton, 5, 1)
        buttonLayout.addWidget(self.centerCurPlayerButton, 6, 0)
        buttonLayout.addWidget(self.FinalButton, 6, 1)
        buttonLayout.addWidget(self.log, 7, 0, 7, 2)
       
        
        buttonLayout.setRowStretch(7, 2)

        rightLayout = QVBoxLayout()
        rightLayout.addLayout(buttonLayout, 1)
        rightLayout.addWidget(self.ancientOneView)

        layout = QHBoxLayout()
        layout.addWidget(self.view, 2)
        layout.addLayout(rightLayout)
        self.setLayout(layout)

        self.createBoard()
        
        self.addAncientOne()

        self.InitPlayerLocation()
        """
        self.TestMonsterSpawn()
        self.TestMonsterSpawn()
        self.TestMonsterSpawn()
        spawn three monsters at trainstation
        """
        Load = XmlLoader.XmlLoader()
        cordPath = os.path.join(os.pardir, 'data', 'MapLocations.txt')
        Load.LoadMapCoordinates(cordPath)
        for element in Load.MapCoordinates:
            self.addMapLocationBox(QRectF(element["Startpointx"], element["Startpointy"], element["BoxWidth"], element["BoxHeight"]), element["Name"])
        

        
        
    def createBoard(self):

        boardPath = os.path.join(os.pardir, 'data', 'Other', 'Board.jpg')
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.sceneItems['board'] = self.scene.addPixmap(QPixmap(boardPath))
        self.sceneItems['board'].setZValue(-100)

        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.view.update()

    def viewResizeEvent(self, event):
        self.zoomLevel = 1
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def updateLabels(self):
        self.phaseLabel.setText(self.tr(self.Environment.CurrentPhase + " Phase"))
        self.curPlayerLabel.setText(self.tr(self.Environment.CurrentPlayer.Name + "'s turn"))
        if self.Environment.CurrentPhase == "Movement":
            self.curPlayerMovePointsLabel.setText(self.tr("Movement Points Remaining: " + str(self.Environment.CurrentPlayer.CurrentMovementPoints)))
            self.curPlayerMovePointsLabel.setVisible(True)
        else:
            self.curPlayerMovePointsLabel.setVisible(False)
        self.doomLabel.setText(self.tr("Doom Level: " + str(self.Environment.AncientOne.CurrentDoom)))
        self.terrorLabel.setText(self.tr("Terror Level: " + str(self.Environment.TerrorLevel)))

    def centerOnCurPlayer(self):
        #self.view.centerOn(self.sceneItems[self.Environment.CurrentPlayer.Name].sceneBoundingRect().center())
        self.centerOn(self.Environment.CurrentPlayer.Name)

    def centerOn(self, uniqueID):
        self.view.centerOn(self.sceneItems[uniqueID].sceneBoundingRect().center())
            
    def zoomIn(self):
        if self.zoomLevel <= 6:
            self.zoomLevel += 1
            self.view.scale(1.5, 1.5)

    def zoomOut(self):
        if self.zoomLevel > 1:
            self.zoomLevel -= 1
            self.view.scale(.666666666, .666666666)

    def rotateMap(self):
        self.view.rotate(90)
        
    def addAncientOne(self):
        """
        This function will add the ancientone image to the board.  Lower right-hand corner below buttons.
        """
        imagePath = self.Environment.AncientOne.Picture
        self.ancientOneScene = QGraphicsScene()
        self.ancientOneView.setScene(self.ancientOneScene)
        temp = self.ancientOneScene.addPixmap(QPixmap(os.path.abspath(imagePath)))
        temp.setZValue(-100)
        self.ancientOneView.update()
        
    def addMonsterImage(self, Monster):
        """
        This function will add a monster image to the board, and give it the correct color border.
        """

        while(Monster.UniqueID in self.sceneItems):
           Monster.UniqueID = Monster.UniqueID + "1"

        #lets draw a pretty boarder around the monster...
        pixmap = QPixmap(Monster.Picture)
        border = pixmap.rect().adjusted(0, 0, 24, 24)
        Monster.pixmap2 = QPixmap(border.width(), border.height())
        Monster.painter = QPainter(Monster.pixmap2)
        Monster.painter.save()
        Monster.painter.setPen(Qt.NoPen)
        Monster.painter.setBrush(eval("Qt." + Monster.Movement))
        Monster.painter.drawRect(border)
        Monster.painter.drawPixmap(12, 12, pixmap)
        Monster.painter.restore()
        
        self.sceneItems[Monster.UniqueID] = stationaryPixmap(Monster.pixmap2.scaledToHeight(900), Monster.UniqueID, self)
        self.sceneItems[Monster.UniqueID].setScale(.1)
        self.scene.addItem(self.sceneItems[Monster.UniqueID])
        
        self.view.update()

    def deleteMonster(self, Monster):
        Indexes = self.scene.items()
        if(Indexes.count(self.sceneItems[Monster.UniqueID]) > 0):
           self.scene.removeItem(self.sceneItems[Monster.UniqueID])
           self.view.update()

    def addGateImage(self, gate):
        """
        This function will add a gate image to the map.
        """
        while(gate.UniqueID in self.sceneItems):
            gate.UniqueID = gate.UniqueID + "1"

        picPath = os.path.join(os.pardir, 'data', 'Otherworld', 'Images', gate.Picture)
        pic = QPixmap(picPath)
        pic.setMask(pic.createHeuristicMask())  #makes the edges transparent
        self.sceneItems[gate.UniqueID] = stationaryPixmap(pic.scaledToHeight(900), gate.UniqueID, self)
        self.sceneItems[gate.UniqueID].setScale(.1)
        self.scene.addItem(self.sceneItems[gate.UniqueID])
        self.sceneItems[gate.UniqueID].setPos(self.MapBoxes[gate.Location.Name].rect.topLeft())

        self.view.update()

    def deleteGateImage(self, gate):
        """
        This function removes the map image from the map.
        """
        if gate.UniqueID in self.sceneItems:
            self.scene.removeItem(self.sceneItems[gate.UniqueID])
            self.view.update()

    def addClueImage(self, location):
        """
        This function adds a clue token image to the bottom-center on the location.
        """
        picPath = os.path.join(os.pardir, 'data', 'Other', 'clue.png')
        pic = QPixmap(picPath)
        self.sceneItems[location.Name + "clue"] = clueToken(pic, self, location)
        self.sceneItems[location.Name + "clue"].setScale(.5)
        self.scene.addItem(self.sceneItems[location.Name + "clue"])
        xCoord = self.MapBoxes[location.Name].rect.left() + (self.MapBoxes[location.Name].rect.width() / 2) - ((pic.width()/2) * .5)
        yCoord = self.MapBoxes[location.Name].rect.bottom() - (pic.height() * .5)
        self.sceneItems[location.Name + "clue"].setPos(xCoord, yCoord)
        self.view.update()

    def deleteClueImage(self, location):
        """
        This function removes a clue token image from the target loation.
        """
        str = location.Name + "clue"
        if str in self.sceneItems:
            self.scene.removeItem(self.sceneItems[location.Name + "clue"])
            self.view.update()
        
    def addInvestigatorImage(self, Player):
        """
        This function will add an investigators image to the board and set it to movable.
        """
        
        self.sceneItems[Player.Name] = custPixmapItem(QPixmap(Player.Graphic), Player.Name, self)
        self.sceneItems[Player.Name].setScale(.1)
        self.scene.addItem(self.sceneItems[Player.Name])
        
        self.view.update()    

    def moveInvestigatorImage(self, Player, Location):
        """
        Moves the investigator 'name' to x, y position in scene.
        """
        Coords = self.GetCoordsByName(Location.Name)
        x = Coords[0]
        y = Coords[1]
        self.sceneItems[Player.Name].animatedMove(QPointF(x - 50, y - (100 - (20 * (1 + len(Location.PlayerList))))))

    def moveMonsterImage(self, Monster, Location):
        Coords = self.GetCoordsByName(Location.Name)
        x = Coords[0]
        y = Coords[1]
        self.sceneItems[Monster.UniqueID].animatedMove(QPointF(x - 50, y - (100 - (20 * (1 + len(Location.MonsterList))))))

    def addMapLocationBox(self, qrectf, name):
        self.MapBoxes[name] = mapLocationBox(qrectf, name, self)
        self.scene.addItem(self.MapBoxes[name])
        self.MapBoxes[name].setZValue(-99)  #shows over map, under all other images.


    def showInvestigator(self):
        
        """
        This is the only function the button needs to call
        """
        if self.Environment.CurrentPhase == "Setup":
            temp = []
            for x in self.Environment.PlayerDictionary:
                temp.append(x)
            Choice = self.Environment.ListChoose("Setup", "Who do you want to view?", temp)
            Player1 = self.Environment.PlayerDictionary[Choice]
        if self.Environment.CurrentPhase != "Setup":
            Player1 = self.Environment.CurrentPlayer
        characterscreen.viewPlayer(Player1, self.Environment)

    def showCombat(self):
        result = self.Environment.ListChoose("How Many Monsters?","Choose how many monsters you wish to face.",["1","2","3","4","5"])
        monlist = list()
        i = 0
        while i < int(result) :
            monlist.append(self.Environment.DrawMonster())
            i += 1
        self.Environment.Combat(self.Environment.CurrentPlayer, monlist)   
        #combat.Combat(self.Environment.CurrentPlayer, self.Environment.DeckDictionary["Monster"])

    def endTurn(self):
        if self.Environment.TurnStack != [] :
            self.Environment.RunNextTurn()

        else:
            if self.Environment.CurrentPhase == "Setup":
                self.Environment.InitialClueLocations()
                self.Environment.MythosPhase()
            elif self.Environment.CurrentPhase == "Upkeep":
                self.Environment.MovementPhase()
            elif self.Environment.CurrentPhase == "Movement":
                self.Environment.EncounterPhase()
            elif self.Environment.CurrentPhase == "Encounter":
                self.Environment.MythosPhase()
            elif self.Environment.CurrentPhase == "Mythos":
                self.Environment.UpkeepPhase()
        

    def Dice(self):
        #print "DiceRoller got: " + DiceRoller.ViewRoller(self.Environment.CurrentPlayer, 6, 5, 4)
        checktype = self.Environment.ListChoose("Choose a Stat","Choose a stat to do a skill check with",["Speed","Sneak","Will","Fight","Lore","Luck"])
        difficulty = int(self.Environment.ListChoose("Choose a difficulty","Choose how many dice you need for success",["1","2","3","4","5","6"]))
        penalty = int(self.Environment.ListChoose("Choose a penalty","Choose how many dice you are penalized",["-3","-2","-1","0","1","2","3"])) 
        result = self.Environment.SkillCheck(checktype,self.Environment.CurrentPlayer, difficulty, penalty)
        self.Environment.PrintEvent("Skillcheck Result","The "+checktype+" check with difficulty "+str(difficulty)+" and penalty of "+str(penalty)+" returned the result: "+result)
        return

    
    def Die(self):
        #print "Single got: " + str(SingleDie.ViewRoller())
        result = self.Environment.RollDie()
        self.Environment.PrintEvent("Single Die Result","The single dice roll returned the result: "+str(result))
        return

    def Final(self):
        self.Environment.FinalBattle()

    def GetCoordsByName(self, Location):
        Coordinates = dict()
        Coordinates["Train Station"] = [351,135]
        Coordinates["Bank Of Arkham"] = [663,141]
        Coordinates["Arkham Asylum"] = [973,139]
        Coordinates["Independence Square"] = [1277,143]
        Coordinates["Newspaper"] = [157,391]
        Coordinates["Curiositie Shoppe"] = [159,643]
        Coordinates["Northside"] = [523,583]
        Coordinates["Downtown"] = [947,585]
        Coordinates["Hibb\'s Roadhouse"] = [1281,473]
        Coordinates["Hibbs Roadhouse"] = [1281,473]
        Coordinates["Velma\'s Diner"] = [1593,467]
        Coordinates["Velmas Diner"] = [1593,467]
        Coordinates["Easttown"] = [1149,899]
        Coordinates["Police Station"] = [1593,747]
        Coordinates["Jail"] = [1431,949]
        Coordinates["Unvisited Isle"] = [165,1035]
        Coordinates["Merchant District"] = [677,1163]
        Coordinates["Rivertown"] = [1121,1163]
        Coordinates["Graveyard"] = [1593,1153]
        Coordinates["River Docks"] = [164,1285]
        Coordinates["The Unnameable"] = [471,1419]
        Coordinates["General Store"] = [1245,1403]
        Coordinates["Black Cave"] = [1593,1425]
        Coordinates["Science Building"] = [167,1649]
        Coordinates["Miskatonic University"] = [679,1681]
        Coordinates["French Hill"] = [1129,1743]
        Coordinates["The Witch House"] = [1587,1819]
        Coordinates["Administration Building"] = [329,2001]
        Coordinates["Administration"] = [329,2001]
        Coordinates["Library"] = [615,1905]
        Coordinates["Silver Twilight Lodge"] = [1315,1971]
        Coordinates["St. Mary\'s Hospital"] = [165,2361]
        Coordinates["St Marys Hospital"] = [165,2361]
        Coordinates["Uptown"] = [751,2373]
        Coordinates["Southside"] = [1161,2369]
        Coordinates["Ma\'s Boarding House"] = [1591,2277]
        Coordinates["Mas Boarding House"] = [1591,2277]
        Coordinates["Ye Olde Magick Shoppe"] = [387,2701]
        Coordinates["Woods"] = [775,2741]
        Coordinates["Historical Society"] = [1125,2739]
        Coordinates["South Church"] = [1475,2669]
        Coordinates["Outskirts"] = [1097,3169]
        Coordinates["Sky"] = [1353,3165]
        Coordinates["Lost in Time and Space"] = [1609,3165]
        Coordinates["Another Dimension"] = [2001,3131]
        Coordinates["Another Dimension2"] = [2001,2997]
        Coordinates["The Abyss"] = [1991,2727]
        Coordinates["The Abyss2"] = [1991,2601]
        Coordinates["The City of the Great Race"] = [1999,2321]
        Coordinates["The City of the Great Race2"] = [1999,2189]
        Coordinates["The City Of The Great Race"] = [1999,2321]
        Coordinates["The City Of The Great Race2"] = [1999,2189]
        Coordinates["The Dreamlands"] = [1993,1111]
        Coordinates["The Dreamlands2"] = [1991,993]
        Coordinates["Plateau of Leng"] = [1995,711]
        Coordinates["Plateau of Leng2"] = [1989,583]
        Coordinates["R'lyeh"] = [1991,311]
        Coordinates["R'lyeh2"] = [1991,193]
        Coordinates["Yuggoth"] = [1991,1929]
        Coordinates["Yuggoth2"] = [1987,1793]
        Coordinates["Great Hall of Celano"] = [1989,1523]
        Coordinates["Great Hall of Celano2"] = [1989,1391]
        Coordinates["Great Hall of Celeano"] = [1989,1523]
        Coordinates["Great Hall of Celeano2"] = [1989,1391]

        return  Coordinates[Location]
    
    def InitPlayerLocation(self):
        i = 0
        PlayerList = []
        PlayerList.append(self.Environment.CurrentPlayer)
        PlayerList = PlayerList + self.Environment.PlayerIncoming + self.Environment.PlayerOutgoing
        while (i < len(PlayerList)):
            self.addInvestigatorImage(PlayerList[i])
            self.moveInvestigatorImage(PlayerList[i], PlayerList[i].Location)
            
            i = i + 1
        
        
    """Needs to be called at monster spawn"""       
    def SpawnMonster(self, Monster, Location):
        self.addMonsterImage(Monster)
        self.moveMonsterImage(Monster, Location)

    def TestMonsterSpawn(self):
        
        TestLoc = self.Environment.Locations["Train Station"]
        self.TestMons = self.Environment.DrawMonster()
        self.SpawnMonster(self.TestMons, TestLoc)
        TestLoc.MonsterList.append(self.TestMons)


    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Enter):
            self.endTurn()
        if(event.key() == Qt.Key_Return):
            self.endTurn()

            

def ShowMap(app, Envir):
    
    window = MapWindow(Envir)
    Envir.MapScreen = window
    
    window.showMaximized()

    
    app.exec_ ()
    

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MapWindow([])
    
    window.show()
    
    sys.exit(app.exec_ ())

#    sys.exit(app.exec_())
            
