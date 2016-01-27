"""
Environment class file
---------------------------------
The environment is incharge of managing, what in the real world would be, the game space.
This includes holding the data structures for the players, decks, board, etc.
It also controls the flow of the game's phases, turns, and mechanics such as combat, casting a spell, etc.
by: Aaron and Zack
---------------------------------
Environment class
---------------------------------
Variable-PlayerDictionary--------
Contains the playercharacter objects as values to the keys which are set to the strings "player1" to "player'n'" so that similar or weird player nicknames do not interfere with program functionality.
Usage:
PlayerDictionary["player1"] will access the object for the first player.
---------------------------------
Variable-DeckDictionary----------
Contains the deck objects as values to the keys which are set to the strings that identify each individual deck
Usage:
DeckDictionary["common"].DrawCard() will access the common deck and draw a card object.
Standards:
Common Items Deck         'Common'   
Unique Items Deck         'Unique'
Ally Card Deck            'Ally'
Skill Card Deck           'Skill'
Spell Card Deck           'Spell'

Other Decks:
Mythos Deck               'Mythos'

Encounter Decks:
<location name>           'xxxxxx'
etc,...
There must be a standard naming convention for the location decks
that is congruitous between the deck identifier on the location struct and
the key on the DeckTable. This is to be hammered out in the future however.

For the location encounter decks, the locations themselves have a variable for their deck
that gives you the key for their deck in this table. The actual deck classes are stored here.
exa: location: Grampa Joe's General Store, has the variable deck = 'purple'
when drawing an encounter card for this location it would reference DeckTable[deck].DrawCard()
where deck is the key that points to the correct encounter deck
---------------------------------
Variable-MythosCard--------------
This variable holds the current mythos card object so that the game can run its effects correctly.

---------------------------------
Variable-RumorCard---------------
This variable holds the current Rumor card object so that the game can run its effects correctly.

---------------------------------
Variable-AncientOne--------------
This varaible holds the current Ancient One object.

---------------------------------
Variable-CurrentPlayer-----------
Used to keep track of the current player.

---------------------------------
Variable-CurrentPhase------------
Used to keep track of the current phase.

---------------------------------

SaveGame:
Got the function stack working to where I can now save what is on the stack into a
list and then save that to xml.  It still needs some formating work, but the function
stack is there.
by:  Ryan Savage
----------------------------------
LoadGame and SaveGame:
I now have the function stack loading from an xml file and getting object references back corrctly.
I have to do a lot of string cleanup to convert it all, but it does work.  I also have
SaveGame sending out properly formated xml documents.
by:  Ryan Savage
"""

from xml.dom import minidom
import random
import os
import XmlLoader
import PlayerCharacter
import LocationClass
import AncientOne
import MonsterClass
import GateClass
import CharSelect
import characterscreen
import DiceRoller
import SingleDie
import BFSArkham
import ChooseDialog
import ChooseListDialog
import EventDialog
import combat
import final
import EncounterFunction
import Deck
import CardFunctions
import SelectCard
from types import *
 

class Environment:
    def __init__(self):
        self.PlayerDictionary = dict()
        self.DeckDictionary = dict()
        self.Locations = dict()
        self.MythosCard = None
        self.RumorCard = None
        self.AncientOne = None
        self.TerrorLevel = 0
        self.GateLimit = 0
        self.MonsterLimit = 0
        self.OutskirtsLimit = 0
        self.CurrentPlayer = None
        self.CurrentPhase = None
        self.CurrentStack = []
        self.TurnStack = []
        self.Gates = []
        self.Monsters = []
        self.Investigators = []
        #self.GameName = GetGameName()
        self.PlayerIncoming = []        #ordered list of players who haven't had a turn this phase
        self.PlayerOutgoing = []        #ordered list of players who have already had their turn this phase
        self.MainStack = 0
        self.NumOfPlayers = 0
        self.MapScreen = ""
        self.CheckRet = ""
        self.Type = "Environment"
        self.ExhaustedCardList = []
        
                
    def GetGameName(self):
        """
        This should ask a user for a game name that will make the .xml
        files unique.
        """
                
    def SaveGame(self, GameName):
        """
        This function is what will save the current state of the game
        into an xml file that can be loaded later.
        """
        f = open(GameName + '.xml', 'w')
        f.write("<?xml version='1.0' ?>\n")
        f.write("<game>\n")
        f.write("  <name>" + GameName + "</name>\n")

        #get the function stack with names and args into a list.
        fstack = []
        for row in self.CurrentStack:
            temp = []
            temp.append('self.' + row[0].func_name)
            for arg in range(1, len(row)):
                    temp.append(row[arg])
            fstack.append(temp)
                
        fstack = map(lambda(x): str(x), fstack)  #make it all strings
        f.write("  <functionStack>")
        f.writelines(fstack)
        f.write("</functionStack>\n")
        f.write("</game>")
        f.close()

    def LoadGame(self, GameName):
        """
        This function is what will load a saved game xml file.
        """
        xmldoc = minidom.parse(GameName + '.xml')
        fStack = xmldoc.getElementsByTagName('functionStack')[0].firstChild.data
        fStack = fStack.split(']')
        fStack = map(lambda(x): str(x), fStack)  #get rid of unicode
        fStack = fStack[0:-1]  #dump last element, which is always empty
        for x in range(0, len(fStack)):
            fStack[x] = fStack[x].strip('[')

        for x in range(0, len(fStack)):
            fStack[x] = eval(fStack[x])

        for x in range(0, len(fStack)):
            if isinstance(fStack[x], tuple):
                fStack[x] = list(fStack[x])
            else:
                fStack[x] = list(tuple(str(s) for s in fStack[x].split(',')))

        for x in range(0, len(fStack)):
            fStack[x][0] = eval(fStack[x][0])

        self.CurrentStack = fStack
            
    def AddPlayer(self,NewPlayer):
        PlayerIndex = len(self.PlayerDictionary) + 1
        NewPlayerId = "Player" + str(PlayerIndex)
        self.PlayerDictionary[NewPlayerId] = NewPlayer
        self.CalcLimits()

    def AddDeck(self,DeckKey):
        self.DeckDictionary[DeckKey] = Deck.Deck(DeckKey)
            
    def CalcLimits(self):
        NumberPlayers = len(self.PlayerDictionary)
        self.GateLimit = NumberPlayers
        if self.TerrorLevel < 10 and self.MonsterLimit < 100 :
            self.MonsterLimit = NumberPlayers + 3
        else :
            self.MonsterLimit = 9999
        self.OutskirtsLimit = 8 - NumberPlayers

    def AddTurn(self, Function):
        self.TurnStack.append(Function)
        
    def RunNextTurn(self):
        if self.TurnStack == []:
            return 1
        CurrentTurn = self.TurnStack.pop(0)
        CurrentTurn()
        return 0

    def UpkeepPhase(self):
        UpkeepStack = []
        self.CurrentStack = UpkeepStack
        self.CurrentPhase = "Upkeep"
        for Player in self.Investigators:
            self.RunFunctionStack(Player.EOPStack)
        self.MapScreen.log.addLine("Upkeep Phase has started.")
        self.SetFirstPlayer()
        for x in self.PlayerIncoming :       
            self.AddTurn(self.UpkeepTurn)  
        self.RunNextTurn()

    def MovementPhase(self):
        MovementStack = []
        self.CurrentStack = MovementStack
        self.CurrentPhase = "Movement"
        for Player in self.Investigators:
            self.RunFunctionStack(Player.EOPStack)
        self.MapScreen.log.addLine("Movement Phase has started.")
        self.SetFirstPlayer()
        for x in self.PlayerIncoming :       
            self.AddTurn(self.MovementTurn)        
        self.RunNextTurn()

    def EncounterPhase(self):
        EncounterStack = []
        self.CurrentStack = EncounterStack
        self.CurrentPhase = "Encounter"
        for Player in self.Investigators:
            self.RunFunctionStack(Player.EOPStack)
        self.MapScreen.log.addLine("Encounter Phase has started.")
        self.SetFirstPlayer()
        for x in self.PlayerIncoming :       
            self.AddTurn(self.EncounterTurn)        
        self.RunNextTurn()     


    def UpkeepTurn(self):
        FunctionStack = []
        self.CurrentStack = FunctionStack
        for P in self.Investigators:
            self.MapScreen.sceneItems[P.Name].pulseAnimationEnd()        

        Player = self.SetCurrentPlayer()
        if Player == None :
            return
        self.RunFunctionStack(Player.EOTStack)
        self.MapScreen.updateLabels()
        self.MapScreen.log.addBreak()
        self.MapScreen.log.addLine( Player.Name+"'s upkeep turn has started.")
        self.MapScreen.sceneItems[Player.Name].pulseAnimationStart()
        
        testlist = list()

        
        #if card doesn't have an imagepath give it one based on name
        import os
        path = os.getcwd()
        length = len(os.getcwd())
        path = path[0:(length - 7)]
        xmlPaths = []
        if(path[len(path)-1] == "\\"):
            path = path + "data\\Item\\items.xml"
        if(path[len(path)-1] == "/"):
            path = path + "data/Item/items.xml"

        """
        temp = self.DeckDictionary["Common"].DrawCard( Player, "Axe")
        if (temp[2] == ""):
            temp[2] = path + temp[0] + ".jpg"
        print "draw 1 card", temp        
        testlist.append( temp)
        
        temp1 = self.DeckDictionary["Common"].DrawCard( Player, "Bullwhip")
        if (temp[2] == ""):
            temp[2] = path + temp[0] + ".jpg"            
        print "draw 1 card", temp1
        testlist.append( temp1)
        
        temp2 = self.DeckDictionary["Common"].DrawCard( Player, "Knife")
        if (temp[2] == ""):
            temp[2] = path + temp[0] + ".jpg"
        print "draw 1 card", temp2
        testlist.append( temp2)
        """
               
        #Refresh Items here!
        self.RefreshCards()
        if Player.Status["Blessed"] == 1 :
            self.MapScreen.log.addLine( Player.Name+" is blessed and must make a single roll.")
            if (self.RollDie() != 1):      
                self.MapScreen.log.addLine( Player.Name+" continues to be blessed.")
            else:
                Player.Status["Blessed"]= 0
                self.MapScreen.log.addLine( Player.Name+" is no longer blessed.")
                        
        if Player.Status["Cursed"] == 1  :
            #Do Check
            if  self.RollDie() != 1 :      
                self.MapScreen.log.addLine( Player.Name+" continues to be cursed.")
            else:
                Player.Status["Cursed"] = 0
                self.MapScreen.log.addLine( Player.Name+" is no longer cursed.")
        if Player.Status["BankLoan"] == 1  :
            #Do Check
            if  self.RollDie() <= 3 :
                self.MapScreen.log.addLine( Player.Name+" must pay his bank loan payment of $1.")
                if Player.Money > 0:
                    Player.Money -= 1
                else:
                    print "Must discard Items"
            else:
                self.MapScreen.log.addLine( Player.Name+" doesn't have to make a payment on his/her bank loan.")                    
                    
        while Player.Status["Retainer"] > 0 :
            Player.Money = Player.Money + 2
            #Do Check
            if (self.RollDie() != 1):
                self.MapScreen.log.addLine( Player.Name+" gains $2 from his/her retainer and gets to keep the retainer.")
            else:
                Player.Status["Retainer"] = Player.Status["Retainer"] - 1
                self.MapScreen.log.addLine( Player.Name+" gains $2 from his/her retainer but loses the retainer.")

        Player.GiveMoneyPerUpkeep()
        

            
        if (Player.Location.Type == "LITAS") :
                if Player.Status["Delayed"] == 1 :
                    Player.Status["Delayed"] = 0
                    self.MapScreen.log.addLine( Player.Name+" is no longer delayed.")

                else :
                    self.MapScreen.log.addLine( Player.Name+" is no longer Lost in Time and Space.")
                    Target = None
                    for Location in self.Locations :
                        if Location.IsInArkham() :
                            templist.append( Location.Name )
                    Target = self.ListChoose( "Choose a destination", "Choose a location in arkham to be transported to.", templist )
                    while Target.IsInArkham() == 0 :
                        Target = self.ListChoose( "Choose a destination", "Invalid selection, Target destination must be in arkham.", templist )
                    self.Teleport(Player, Target)
                
        #Ability to move sliders begins
        Player.RefillFocus()

        #Do players special
        Player.UpkeepFunction()

        #Dialog to prompt skill adjustment
        characterscreen.viewPlayer(Player, self)

            
        
        Player.DrainFocus()
        #Ability to move sliders ended
                        
        self.RunFunctionStack(self.CurrentStack)


    def MovementTurn(self):
        FunctionStack = []
        self.CurrentStack = FunctionStack
        for P in self.Investigators:
            self.MapScreen.sceneItems[P.Name].pulseAnimationEnd() 
        Player = self.SetCurrentPlayer()
        if Player == None :
                return
            
        self.RunFunctionStack(Player.EOTStack)
        self.MapScreen.log.addBreak()
        self.MapScreen.log.addLine( Player.Name+"'s movement turn has started.")                    
        self.MapScreen.sceneItems[Player.Name].pulseAnimationStart()
        Player.CurrentMovementPoints = Player.Stats["Speed"] + Player.BonusStats["Speed"] + Player.BonusStats["Movement"]
        self.MapScreen.updateLabels()
        if len(Player.Location.MonsterList) > 0:
            self.PrintEvent("Monsters appear!","You must engage or evade nearby monsters!")
            self.Combat( Player, Player.Location.MonsterList )
            
        if Player.Status["Delayed"] == 1 :
            if Player.Location.Type != "LITAS" :
                self.MapScreen.log.addLine( Player.Name+" is no longer delayed.")                    
                Player.Status["Delayed"] = 0
            Player.CurrentMovementPoints = 0
            self.MapScreen.updateLabels()
        elif Player.Location.Type == "Otherworld" :
            if Player.Location.Connections == [] :  #in 2nd area of otherworld
                DestinationList = []
                Player.CurrentMovementPoints = 0
                self.MapScreen.updateLabels()
                for Gate in self.Gates :
                    if str(Gate.Destination+"2") == Player.Location.Name and Gate.Location != None :
                        DestinationList.append(Gate.Location.Name)
                if DestinationList == [] :
                    #No portals open to your zone, you are lost in time and space
                    self.PrintEvent("No where to go!","There are no active gates connecting to your dimension. You have been stranded and are now lost in time and space!")
                    self.Teleport(Player,self.Locations["Lost in Time and Space"])
                    Player.Status["Delayed"] = 1
                else :
                    Target = self.ListChoose( "Choose a destination.", "You can exit this dimension to any location with a gate open to it.",DestinationList )
                    Target = self.Locations[Target]
                    self.Teleport(Player,Target) 
                    Target.Gate.ExploredBy(Player)       
                
            elif Player.Location.Connections != [] :
                Player.CurrentMovementPoints = 1
                self.Movement(Player, Player.Location.Connections[0])
                Player.CurrentMovementPoints = 0
                self.MapScreen.updateLabels()

    def MultiSpaceMovement(self,Player,Destination):
        if Player.CurrentMovementPoints == 0:
            return
        Path = self.FindShortestPath(Player.Location, Destination)
        while Path != [] and Player.CurrentMovementPoints > 0:
            if len(Player.Location.MonsterList) > 0:
                self.PrintEvent("Monsters appear!","You must engage or evade nearby monsters!")
                self.Combat( Player, Player.Location.MonsterList )
                if Player.CurrentMovementPoints == 0 :
                    #player's actions were interrupted, turn over
                    break
            Target = self.Locations[Path.pop(0)]
            if Target == Player.Location and len(Path) != 0 :
                Target = self.Locations[Path.pop(0)]
            self.Movement(Player,Target )
            self.MapScreen.updateLabels()
        if len(Player.Location.MonsterList) > 0:
            self.PrintEvent("Monsters appear!","You must engage or evade nearby monsters!")
            self.Combat( Player, Player.Location.MonsterList )
            self.MapScreen.updateLabels()



    def FindShortestPath(self, start, goal):

        FSP = BFSArkham.MapSolver(start, goal, self)
        print FSP
        return FSP

    def Movement(self,Player,Target):
        if Player.Location == Target :
            return 0
        if Player.Location.Gate != None :
            Player.Location.Gate.RemoveExplorer(Player)
            self.MapScreen.log.addLine( Player.Name+" has lost his gate explorer token.")
        if Player.CurrentMovementPoints < 1 or Target.IsClosed == 1:
            return 0
        if Target in Player.Location.Connections :
            Player.CurrentMovementPoints = Player.CurrentMovementPoints - 1
            Target.AddPlayer(Player)
            self.MapScreen.log.addLine( Player.Name+" has arrived at "+Player.Location.Name)
            self.MapScreen.moveInvestigatorImage(Player, Player.Location)
            self.MapScreen.updateLabels()



    def Teleport(self,Player,Target):

        #Sister Mary Special ability
        if(Target == "Lost in Time and Space"):
            if(Player.Name == "Sister Mary"):
                if(Player.Stats["Stamina"] <= 0):
                    Target = self.Location["St Marys Hospital"]
                elif(Player.Stats["Sanity"] <= 0):
                    Target = self.Location["Arkham Asylum"]
                else:
                    Target = self.Location["South Church"]
        if Player.Location.Gate != None :
            Player.Location.Gate.RemoveExplorer(Player)
        Target.AddPlayer(Player)
        self.MapScreen.log.addLine( Player.Name+" has been transported to "+Player.Location.Name)
        self.MapScreen.moveInvestigatorImage(Player, Player.Location)
        
    def Choose(self,Title,BodyText,Option1,Option2,Detailed):
        return ChooseDialog.Run(Title,BodyText,Option1,Option2,Detailed)
    
    def ListChoose(self,Title,Text,List):
        return ChooseListDialog.Run(Title,Text,List)

    def ItemChoose(self,Text,ItemList):
        return SelectCard.browseList(Text, ItemList)

    def PrintEvent(self,Title,Text):
        EventDialog.Run(Title,Text)

    def RollDie(self):
        return SingleDie.ViewRoller()

    def SkillCheck(self, Type, Player, Difficulty, Penalty ):
        if Type == "Combat" :
            Dice = Player.Stats["Fight"] + Player.BonusStats["Fight"] + Player.CheckBonus["Combat"] + Player.BonusStats["Combat"]+ Penalty
            try:
                if Player.FightingMonster.Abilities["PhysicalImmunity"]+ Player.CancelAbilities["PhysicalImmunity"] > 0:
                    Dice += 0 * Player.BonusStats["Physical"]
                elif Player.FightingMonster.Abilities["PhysicalResistance"] + Player.CancelAbilities["PhysicalResistance"] > 0:
                    Dice +=  int(Player.BonusStats["Physical"] / 2)
                else:
                    Dice += Player.BonusStats["Physical"]
            except(AttributeError,ValueError,TypeError):
                Dice += Player.BonusStats["Physical"]
                
            try:
                if Player.FightingMonster.Abilities["MagicalImmunity"] + Player.CancelAbilities["MagicalImmunity"] > 0:
                    Dice +=  0 * Player.BonusStats["Magical"]
                elif Player.FightingMonster.Abilities["MagicalResistance"] + Player.CancelAbilities["MagicalResistance"] > 0:
                    Dice +=  int(Player.BonusStats["Magical"] / 2)
                else:
                    Dice += Player.BonusStats["Magical"]
            except(AttributeError,ValueError,TypeError):
                Dice += Player.BonusStats["Magical"]

        elif Type == "Spell" :
            Dice = Player.Stats["Lore"] + Player.BonusStats["Lore"] + Player.CheckBonus["Spell"] + Penalty
        elif Type == "Horror" :
            Dice = Player.Stats["Will"] + Player.BonusStats["Will"] + Player.CheckBonus["Horror"] + Penalty
        elif Type == "Evade" :
            Dice = Player.Stats["Sneak"] + Player.BonusStats["Sneak"] + Player.CheckBonus["Evade"] + Penalty
        else :
            Dice = Player.Stats[Type] + Player.BonusStats[Type] + Player.CheckBonus[Type] + Penalty
            
        if Player.Status["Cursed"] > 0 :
            ReqSuccess = 6
        elif Player.Status["Blessed"] > 0 :
            ReqSuccess = 4
        else :
            ReqSuccess = 5

        if DiceRoller.ViewRoller(Type,Player,Dice,ReqSuccess,Difficulty) >= Difficulty:
            self.CheckRet = "Pass"
        else:
            self.CheckRet = "Fail"
        self.RunFunctionStack(Player.EOSStack)
        print self.CheckRet
        if type(self.CheckRet).__name__ == 'list':
            if self.CheckRet[1] == Type:
                self.CheckRet = self.CheckRet[0]
        return self.CheckRet
    #There are many instances where you want the number of success. use this function
    def SuccessCheck(self, Type, Player, Difficulty, Penalty ):
        if Type == "Combat" :
            Dice = Player.Stats["Fight"] + Player.BonusStats["Fight"] + Player.CheckBonus["Combat"] + Penalty
            try:
                if Player.FightingMonster.Abilities["PhysicalImmunity"]+ Player.CancelAbilities["PhysicalImmunity"] > 0:
                    Dice += 0 * Player.BonusStats["Physical"]
                elif Player.FightingMonster.Abilities["PhysicalResistance"] + Player.CancelAbilities["PhysicalResistance"] > 0:
                    Dice +=  int(Player.BonusStats["Physical"] / 2)
                else:
                    Dice += Player.BonusStats["Physical"]
            except(AttributeError,ValueError,TypeError):
                Dice += Player.BonusStats["Physical"]
                
            try:
                if Player.FightingMonster.Abilities["MagicalImmunity"] + Player.CancelAbilities["MagicalImmunity"] > 0:
                    Dice +=  0 * Player.BonusStats["Magical"]
                elif Player.FightingMonster.Abilities["MagicalResistance"] + Player.CancelAbilities["MagicalResistance"] > 0:
                    Dice +=  int(Player.BonusStats["Magical"] / 2)
                else:
                    Dice += Player.BonusStats["Magical"]
            except(AttributeError,ValueError,TypeError):
                Dice += Player.BonusStats["Magical"]
        elif Type == "Spell" :
            Dice = Player.Stats["Lore"] + Player.BonusStats["Lore"] + Player.CheckBonus["Spell"] + Penalty
        elif Type == "Horror" :
            Dice = Player.Stats["Will"] + Player.BonusStats["Will"] + Player.CheckBonus["Horror"] + Penalty
        elif Type == "Evade" :
            Dice = Player.Stats["Sneak"] + Player.BonusStats["Sneak"] + Player.CheckBonus["Evade"] + Penalty
        else :
            Dice = Player.Stats[Type] + Player.BonusStats[Type] + Player.CheckBonus[Type] + Penalty
            
        if Player.Status["Cursed"] > 0 :
            ReqSuccess = 6
        elif Player.Status["Blessed"] > 0 :
            ReqSuccess = 4
        else :
            ReqSuccess = 5

        successes = DiceRoller.ViewRoller(Type,Player,Dice,ReqSuccess,Difficulty)
        self.RunFunctionStack(Player.EOSStack)
        return successes

        
    def CloseGate(self,Player,Gate):
        if Player not in Gate.Explorers :
            self.MapScreen.log.addLine( Player.Name+" cannot close this gate as you have not explored its dimension yet.")
        Choice = self.Choose("Closing the Gate", "Would you like to use your lore or fight value to close this gate.","Fight","Lore",
                    "\n Your current lore is "+str(Player.Stats["Lore"]+Player.BonusStats["Lore"])+"\n Your current fight is "+str(Player.Stats["Fight"]+Player.BonusStats["Fight"]))
        if Choice == "Lore" :
            Check = self.SkillCheck("Lore",Player,1,Gate.Difficulty)
        elif Choice == "Fight" :
            Check = self.SkillCheck("Fight",Player,1,Gate.Difficulty)
        if Check == "Fail" :
            self.PrintEvent("Closing the Gate","You have failed to close the gate.")
            return
        elif Check == "Pass" :
            self.MapScreen.deleteGateImage(Gate)
            if Gate in self.Gates:
                self.Gates.remove(Gate)
            Gate.Location.RemoveGate(Gate)
            Player.AddGateTrophy(Gate)
            for Monster in self.Monsters :
                if Monster.HomeDimension == Gate.DimensionalShape :
                    self.MapScreen.deleteMonster(Monster)
                    self.ReturnMonster(Monster)
                
            Choice2 = self.Choose("Sealing the Gate", "You have closed the gate and sent related monsters back to their dimensional prison! The gate is now one of your trophies! Would you like to seal the gate permanently?","Yes","No","Sealing a gate requires you to spend either 5 clue tokens or an elder sign.")
            if Choice2 == "Yes" :
                Choice3 = self.Choose("Sealing the Gate", "Spend 5 clue tokens or a elder sign?","5 Clue Tokens","Elder Sign","Sealing a gate requires you to spend either 5 clue tokens or an elder sign.")
                if Choice3 == "5 Clue Tokens" :
                    if Player.Clues >= 5:
                        self.PrintEvent("Sealing the Gate","You have successfully sealed the gate at this location. No more gates can spawn here for the remainder of the game.")
                        Player.Clues -= 5
                        Player.Location.AddElderSign()
                    else:
                        self.PrintEvent("Sealing the Gate","You do not have enough Clue Tokens to seal the gate.")
                elif Choice3 == "Elder Sign":
                    #Placeholder
                    self.PrintEvent("Sealing the Gate","You have successfully sealed the gate at this location. No more gates can spawn here for the remainder of the game.")
                    Player.Location.AddElderSign()
            
               
    def Combat(self, Player, MonsterList):
        DefeatedList = []
        EvadedList = []
        combat.Combat(Player, MonsterList,DefeatedList,EvadedList, self)

        for Monster in DefeatedList :
            try:
                self.MapScreen.deleteMonster(Monster)
            except(ValueError,AttributeError,KeyError):
                print "Nothin to see"
            try:
                self.Monsters.remove(Monster)
            except(ValueError,AttributeError,KeyError):
                print "Nothin to see"            
            if Monster not in Player.MonsterTrophies :
                self.ReturnMonster(Monster)
        for Monster in EvadedList :
            MonsterList.append(Monster)
                
        if Player.Stats["Stamina"] <= 0 :
            self.Unconscious(Player)
        if Player.Stats["Sanity"] <= 0 :
            self.Insane(Player)

    def FinalCheck(self):
        #doomtrack full
        if self.AncientOne.CurrentDoom >= self.AncientOne.MaxDoom :
            self.FinalBattle()
        #too many gates
        if len(self.Investigators) <= 2 and len(self.Gates) >= 8:
            self.FinalBattle()
        elif len(self.Investigators) > 2 and len(self.Investigators) <= 4 and len(self.Gates) >= 7:
            self.FinalBattle()
        elif len(self.Investigators) > 4 and len(self.Investigators) <= 6 and len(self.Gates) >= 6:
            self.FinalBattle()
        elif len(self.Investigators) > 6 and len(self.Investigators) <= 8 and len(self.Gates) >= 5:
            self.FinalBattle()  
        #no gate markers
        if len(self.DeckDictionary["Gate"]) < 1 :
            self.FinalBattle()  

        #no monsters in cup
        if len(self.DeckDictionary["Monster"]) < 1 :
            self.FinalBattle()  
        monstercount = 0
        for mon in self.Monsters :
            if mon.Location.Name != "Outskirts":
                monstercount += 1
        #terror=10 and monsters == 2*normal limit
        if self.TerrorLevel == 10 and monstercount >= 2*(len(self.Investigators) + 3):
            self.FinalBattle()
    def FinalBattle(self):
        self.CurrentPhase = "Final"
        result = "Defeat"
        self.PrintEvent("The Ancient One Awakes!","Despite the actions of the investigators, the Ancient Evil has awoken and now must be defeated in battle!")
        DevourQueue = []
        for Player in self.Investigators :
            if Player.Location.Type == "LITAS":
                DevourQueue.append( Player )
        for item in DevourQueue:
            self.Devour( item )

        self.AncientOne.AwakenFunction()
        if self.Investigators :
            result = final.viewFinal(self)
        if result == "Victory" :
            self.PrintEvent("The Final Battle has been Won!", "The Investigators have defeated the Ancient One and have saved Arkham from a Gruesome fate. All Players Win!")
            self.MapScreen.close()
        elif result == "Defeat" :
            self.PrintEvent("The Final Battle has been Lost!","With the Investigators defeated by the Ancient One, there is nothing stopping the destruction of Arkham.  All Players Lose!")
            self.MapScreen.close()

    def Unconscious(self,Player):
        if Player.Stats["Sanity"] <= 0 and Player.Stats["Stamina"] <= 0 :
            self.Devour(Player)
            return 1
        self.PrintEvent( "Unconscious!",Player.Name+" has gone unconscious. That investigator must pay the penalties for going Unconscious.")
        Player.CurrentMovementPoints = 0
        Player.Status["Retainer"] = 0
        Player.Clues = int(( Player.Clues / 2 ))
        """Commented out until items are working
        Goal = int(len(Player.ItemList)/2)
        TempList = list()
        for Item in Player.ItemList :
            TempList.append(Item[0])    #ItemName
        while len (Player.ItemList) > Goal :
            Target = self.ListChoose( "Choose an Item","You must discard half of your items, please select an item to discard.", TempList )
            Player.Discard(Target)
            TempList.remove(Target)
            """
        if Player.Location.Type == "LITAS":
            self.Teleport(Player, self.Locations["Lost in Time and Space"])
        else:
            self.Teleport(Player, self.Locations["St Marys Hospital"])
        Player.Stats["Stamina"] = 1

    def Insane(self,Player):
        if Player.Stats["Sanity"] <= 0 and Player.Stats["Stamina"] <= 0 :
            self.Devour(Player)
            return 1
        self.PrintEvent( "Insane!",Player.Name+" has gone insane. That investigator must pay the penalties for going insane.")
        Player.CurrentMovementPoints = 0
        Player.Status["Retainer"] = 0
        Player.Clues = int(( Player.Clues / 2 ))
        """Commented out until items are working
        Goal = int(len(Player.ItemList)/2)
        TempList = list()
        for Item in Player.ItemList :
            TempList.append(Item[0])    #ItemName
        while len (Player.ItemList) > Goal :
            Target = self.ListChoose( "Choose an Item","You must discard half of your items, please select an item to discard.", TempList )
            Player.Discard(Target)
            TempList.remove(Target)
        """
        if Player.Location.Type == "LITAS":
            self.Teleport(Player, self.Locations["Lost in Time and Space"])
        else:
            self.Teleport(Player, self.Locations["Arkham Asylum"])
        Player.Stats["Sanity"] =  1
            
    def Devour(self,Player):
        #Discard all cards
        self.PrintEvent( "Devoured!",Player.Name+" has been devoured. The investigator is utterly destroyed.")
        #for Item in Player.ItemList :
        #    Player.Discard(Item)
        while Player.GateTrophies :
            Trophy = Player.GateTrophies.pop()
            self.ReturnGate(Trophy)
        while Player.MonsterTrophies :
            Monster = Player.MonsterTrophies.pop()
            self.ReturnMonster(Monster)
        if self.CurrentPhase == "Final" :
            self.EliminatePlayer(Player)
        else:
            self.RestartPlayer(Player)
        return 1

    def EliminatePlayer(self,Player):
        if Player in self.Investigators :
            self.Investigators.remove(Player)
        if Player in self.PlayerIncoming:
            self.PlayerIncoming.remove(Player)
        if Player in self.PlayerOutgoing:
            self.PlayerOutgoing.remove(Player)
        if self.CurrentPlayer == Player :
            self.CurrentPlayer = None

    def RestartPlayer(self,Player):
        self.EliminatePlayer(Player) #placeholder, all players are eliminated
        #Player = None
        #NewInvestigator = Choose(1, self.DeckDictionary["Investigator"])
        #Player = NewInvestigator
        #Do Setup stuff for new investigator
        #Put investigator on map
        #Draw random and fixed items
        #Add more stuff here
            

    def AddClue(self,Target):
        if Target.Gate == None:
            Target.AddClue()
            if type(self.MapScreen) != StringType:
                self.MapScreen.addClueImage(Target)

    def NewGate(self,Gate,Target):
        if len(self.DeckDictionary["Gate"]) == 0:
            self.FinalCheck()
        if Target.GetStability() == "Stable" or Target.Type == "Street" :
            return 
        elif Target.ElderSign == 1:
            self.MapScreen.log.addLine( "The Elder Sign at "+Target.Name+" has blocked the formation of a Gate!")
            return 
        elif Target.Gate == None :
            Target.AddGate(Gate)
            self.IncreaseDoomTrack()
            self.MapScreen.deleteClueImage(Target)
            self.Gates.append(Gate)
            self.MapScreen.addGateImage(Gate)
            self.MapScreen.log.addLine( "A New Gate has opened at "+Target.Name)
            RandomMonster = self.DrawMonster()  
            self.NewMonster( RandomMonster, Target )
            if len(self.Investigators) >= 5:
                RandomMonster = self.DrawMonster()  
                self.NewMonster( RandomMonster, Target )                
            if len(Target.PlayerList) > 0:
                for Player in Target.PlayerList :
                    if Player.Location == Target:
                        self.Teleport(Player,self.Locations[Gate.Destination])
                        Player.Status["Delayed"] = 1
                    else:
                        Target.RemovePlayer(Player)
        elif Target.Gate != None :
            #Monster Surge
            self.MapScreen.log.addLine( "Monster Surge! Monsters are pouring out of all open gates!")
            N = max( len(self.Gates) , len(self.Investigators) )
            random.shuffle(self.DeckDictionary["Monster"])
            MonsterSurge = list()
            while len(MonsterSurge) < N :
                MonsterSurge.append( self.DrawMonster() )
            i = 0
            while MonsterSurge != [] :      #cycles through all open gates, spawning monsters until done
                self.NewMonster( MonsterSurge.pop(0) , self.Gates[ (i % len(self.Gates) ) ].Location )
                i = i + 1
        #update map        
        return 
        

    def NewMonster(self,Monster,Target):
        if len(self.DeckDictionary["Monster"]) == 0:
            self.FinalCheck()
        if Target.ElderSign == 1:
            return
        monstercount = 0
        for mon in self.Monsters :
            if mon.Location.Name != "Outskirts":
                monstercount += 1
        if monstercount >= self.MonsterLimit :
            self.Locations["Outskirts"].AddMonster(Monster)
            self.Monsters.append(Monster)
            self.MapScreen.SpawnMonster(Monster, Monster.Location)
            self.MapScreen.log.addLine( Monster.Name+" has appeared at "+Monster.Location.Name)
        else:
            Target.AddMonster(Monster)
            self.Monsters.append(Monster)
            self.MapScreen.SpawnMonster(Monster, Monster.Location)
            self.MapScreen.log.addLine( Monster.Name+" has appeared at "+Monster.Location.Name)
        
        if( len(self.Locations["Outskirts"].MonsterList) > self.OutskirtsLimit ):
            self.MapScreen.log.addLine( "The Outskirts of Arkham are overflowing with monsters!")
            while self.Locations["Outskirts"].MonsterList != [] :
                temp = self.Locations["Outskirts"].MonsterList.pop()
                self.MapScreen.log.addLine( temp.Name+" has dispersed from the outskirts.")
                self.MapScreen.deleteMonster(temp)
                self.ReturnMonster( temp )
            random.shuffle(self.DeckDictionary["Monster"])
            self.IncrementTerrorTrack()
    
    def DrawMonster(self):
        if len(self.DeckDictionary["Monster"]) == 0:
            return
        self.ShuffleMonsters() 
        return self.DeckDictionary["Monster"].pop(random.randint(0, len(self.DeckDictionary["Monster"]) - 1))
    
    def ReturnMonster(self,Monster):
        try:
            Monster.Location.RemoveMonster(Monster)
        except(ValueError,KeyError,AttributeError):
            print "returnmonster, non-threatening exception"            
        try:
            self.Monsters.remove(Monster)        
        except(ValueError,KeyError,AttributeError):
            print "returnmonster, non-threatening exception"  
        self.DeckDictionary["Monster"].append( Monster )
        self.ShuffleMonsters()

    def DrawGate(self):
        if len(self.DeckDictionary["Gate"]) == 0:
            return []
        self.ShuffleGates()
        return self.DeckDictionary["Gate"].pop(random.randint(0, len(self.DeckDictionary["Gate"]) - 1))
    
    def ReturnGate(self,Gate):
        try:
            Gate.Location.RemoveGate(Gate)
        except(ValueError,KeyError,AttributeError):
            print "returngate, non-threatening exception"            
        try:
            self.Gates.remove( Gate )
        except(ValueError,KeyError,AttributeError):
            print "returngate, non-threatening exception"  
        self.DeckDictionary["Gate"].append( Gate )
        self.ShuffleGates()

    def ShuffleMonsters(self):
        random.shuffle(self.DeckDictionary["Monster"])
            
    def ShuffleGates(self):
        random.shuffle(self.DeckDictionary["Gate"])
            
    def ShuffleInvestigators(self):
        random.shuffle(self.DeckDictionary["Investigator"])
    
    def Trade(self,Player1,Player2):
        """
        #The following is designed with a single computer mode in mind, 1 player is playing
        #the game at a time
        while Player1 is NotReady
                Player1 selects/deselects
                items/money/etc he wishes to trade
                Choose( Ready or NotReady )
        while Player2 is NotReady
                Player2 selects/deselects
                items/money/etc he wishes to trade
                Choose( Ready or NotReady)
        Confirm( Player1 & Player2 )
        Do Transaction()
        
        """
        return 0

    def Victory(self):
        return

    def Defeat(self):
        return
    
    def GateVictoryCheck(self):
        if self.Gates == [] :
            trophycount = 0
            for Player in self.Investigators:
                trophycount += len(Player.GateTrophies)
            if trophycount >= len(self.Investigators) :
                self.PrintEvent("Victory!","The investigators have prevented the Ancient One from awakening by closing gates equal to the number of players. Game Over.")
        eldersigncount = 0
        for Location in self.Locations :
            eldersigncount += self.Locations[Location].ElderSign
        if eldersigncount >= 6 :
            self.PrintEvent("Victory!","The investigators have prevented the Ancient One from awakening by sealing 6 gates. Game Over.")


    def EncounterTurn(self):
        FunctionStack = []
        self.CurrentStack = FunctionStack
        for P in self.Investigators:
            self.MapScreen.sceneItems[P.Name].pulseAnimationEnd() 
        Player = self.SetCurrentPlayer()
        if Player == None :
            return
        
        self.MapScreen.sceneItems[Player.Name].pulseAnimationStart()        
        self.RunFunctionStack(Player.EOTStack)
        Player.CurrentMovementPoints = 0
        Player.Location.CollectClues(Player)
        self.MapScreen.deleteClueImage(Player.Location)
        #remove clues here
        self.MapScreen.log.addBreak()
        self.MapScreen.log.addLine( Player.Name+"'s encounter turn has started.")
        if Player.Location.Gate != None :
            if Player in Player.Location.Gate.Explorers :
                Choice = self.Choose("Close the Gate","Would you like to attempt to close the gate?","Yes","No",
                                     "Closing the gate can only be done after exploring the gate's dimension and only before leaving the gates location.")
                if Choice == "Yes":
                    self.CloseGate(Player,Player.Location.Gate)
                    self.GateVictoryCheck()
            else:
                self.Teleport(Player, self.Locations[Player.Location.Gate.Destination])
                self.MapScreen.log.addLine( Player.Name+" has been sucked through the gateway into a different dimension.")
        if Player.Location.Type == "Arkham":   #normal encounter turn
            print "encounter"
            Choice = "Draw"
            if Player.Location.Name in EncounterFunction.LocationEncounterDict:
                Choice = self.Choose("Encounter Turn", "Would you like to draw an encounter card or do the special encounter for your loction","Draw","Special"," ")
                if Choice == "Special":
                    Encounter = "EncounterFunction."+EncounterFunction.LocationEncounterDict[Player.Location.Name]
                    exec Encounter+"(self, Player)"
            if Choice == "Draw":
                rng = random.randint(1,7)
                print rng
                try:
                    Encounter = "EncounterFunction."+EncounterFunction.EncounterDict[Player.Location.Name]+str(rng)+"(self, Player)"
                    exec Encounter
                except(ValueError,AttributeError):
                    print "No encounter", Player.Name , Player.Location.Name
        elif Player.Location.Type == "Otherworld" :  #Otherworld encounter turn
            #self.PrintEvent("Encounter!","Otherworld Encounter here!")
            print "otherworld encounter"
        try:
            self.MapScreen.sceneItems[self.CurrentPlayer.Name].pulseAnimationEnd()        
        except(KeyError):
            print "nothing to stop"


    def SetupTurn(self):
        FunctionStack = []
        self.CurrentStack = FunctionStack
        Player = self.SetCurrentPlayer()

        if Player == None :
                return
        tempLoc = Player.Location
        Player.Location = None
        self.Locations[tempLoc].AddPlayer(Player)



    def MythosPhase(self):
        MythosStack = []
        self.CurrentStack = MythosStack
        self.CurrentPhase = "Mythos"
        for P in self.Investigators:
            self.MapScreen.sceneItems[P.Name].pulseAnimationEnd() 
        self.MapScreen.log.addBreak()
        self.MapScreen.log.addLine("The Mythos phase has started.")
        for Player in self.Investigators:
            self.RunFunctionStack(Player.EOPStack)
            self.RunFunctionStack(Player.EOTStack)
        self.MapScreen.updateLabels()
        """ THE BELOW IS MOSTLY PLACEHOLDER FOR TESTING AND PRESENTATION PURPOSES """
        #Spawn random gate with monster
        spawnloc = list()
        for key in self.Locations :
            if self.Locations[key].Type == "Arkham" and self.Locations[key].GetStability() == "Unstable" :
                spawnloc.append( self.Locations[key])
        random.shuffle(spawnloc)
        target= random.randint(0, len(spawnloc) - 1)
        self.NewGate( self.DrawGate() , spawnloc[ target ])
        
        #Random clues
        i = 0
        j = random.randint(1,3)
        cluelocs = list()
        while i < j:
            randkey = random.choice(self.Locations.keys())
            if self.Locations[randkey].GetStability() == "Unstable" and self.Locations[randkey].Gate == None:
                self.AddClue(self.Locations[randkey])
                cluelocs.append(randkey)
                i += 1
        cluelocs = list(set(cluelocs))
        cluelocsstring = ""
        for locs in cluelocs :
            cluelocsstring += locs+",  "
        self.MapScreen.log.addLine("Clues have appeared around arkham! You should consider checking the following locations for clues: " +cluelocsstring)
        
        #set random movements
        PossibleSymbols = [ "hexagon","star","moon","diamond","Square","circle","crescent","triangle"]
        random.shuffle(PossibleSymbols)
        WhiteSymbols = list()
        BlackSymbols = list()
        i = 0
        j = random.randint(0,3)
        while i < j :
            random.shuffle(PossibleSymbols)
            WhiteSymbols.append(PossibleSymbols.pop(0))
            i += 1
        i = 0
        j = random.randint(0,3)
        while i < j :
            random.shuffle(PossibleSymbols)
            BlackSymbols.append(PossibleSymbols.pop(0))
            i += 1
        for Monster in self.Monsters :
            if Monster.Location != None:
                if Monster.HomeDimension in BlackSymbols :
                    self.MonsterMovement(Monster,"Black")
                elif Monster.HomeDimension in WhiteSymbols :
                    self.MonsterMovement(Monster,"White")


    def MonsterMovement(self,Monster,MovementColor):
        
        if Monster.Location.Name == "Outskirts":
            return
        if Monster.Location.PlayerList :
            return
        CurrentLocation = Monster.Location

        if Monster.Location.Connections != [] :
            if MovementColor == "White":
                TargetLocation = CurrentLocation.WhiteStreet
            elif MovementColor == "Black":
                TargetLocation = CurrentLocation.BlackStreet
        else:
            TargetLocation = Monster.Location
        if Monster.Movement == "yellow" :
            #yellow == stationary
            return
        elif Monster.Movement == "green":
            #green == special
            if Monster.Name == "Chthonian":
                Monster.ChthonianMove()
            if Monster.Name == "Hound of Tindalos":
                Monster.HoundOfTindalosMove()
        elif Monster.Movement == "black" :
            #black == normal, one move
            TargetLocation.AddMonster(Monster)
            self.MapScreen.moveMonsterImage(Monster, TargetLocation)
            self.MapScreen.log.addLine(Monster.Name+" has moved to "+Monster.Location.Name)
            Monster.execMonsterMove()
        elif Monster.Movement == "red" :
            #red == fast movement
            TargetLocation.AddMonster(Monster)
            self.MapScreen.moveMonsterImage(Monster, TargetLocation)
            Monster.execMonsterMove()
            if Monster.Location.PlayerList != [] :
                return
            #2nd movement
            CurrentLocation = Monster.Location
            if MovementColor == "White":
                TargetLocation = CurrentLocation.WhiteStreet
            elif MovementColor == "Black":
                TargetLocation = CurrentLocation.BlackStreet
            CurrentLocation.RemoveMonster(Monster)
            TargetLocation.AddMonster(Monster)
            self.MapScreen.moveMonsterImage(Monster, TargetLocation)
            self.MapScreen.log.addLine(Monster.Name+" has moved to "+Monster.Location.Name)
            Monster.execMonsterMove()

        elif Monster.Movement == "blue" :
            #blue == flying movement
            if Monster.Location.Name == "Sky" :
                print "Monster detected to be in sky"
                PossibleTargets = list()
                LowestSneak = 1000
                for TarLoc in self.Locations :
                    print "SEARCHING:", self.Locations[TarLoc].Name , self.Locations[TarLoc].PlayerList
                    if self.Locations[TarLoc].Type == "Street" and self.Locations[TarLoc].PlayerList:
                        print "Found occupied street!"
                        for Player in self.Locations[TarLoc].PlayerList :
                            if (Player.Stats["Sneak"] + Player.BonusStats["Sneak"] ) < LowestSneak :
                                LowestSneak = (Player.Stats["Sneak"] + Player.BonusStats["Sneak"])
                                print "Found new lowest sneak!"
                                PossibleTargets = []
                                PossibleTargets.append(TarLoc)
                            if (Player.Stats["Sneak"] + Player.BonusStats["Sneak"]) == LowestSneak :
                                LowestSneak = (Player.Stats["Sneak"] + Player.BonusStats["Sneak"])
                                PossibleTargets.append(TarLoc)
                                print "Found equal sneak!"
                if PossibleTargets :
                    NewTarget = self.Locations[random.choice(PossibleTargets)]
                    print "There exists possible targets to swoop down."
                    NewTarget.AddMonster(Monster)
                    self.MapScreen.moveMonsterImage(Monster, NewTarget)
                    Monster.execMonsterMove()
                    self.MapScreen.log.addLine(Monster.Name+" has moved to "+Monster.Location.Name)
                return    
            elif Monster.Location.Type != "Street" and TargetLocation.PlayerList :
                print " flying monster: i am not in street and have targets near by "
                TargetLocation.AddMonster(Monster)
                self.MapScreen.moveMonsterImage(Monster, TargetLocation)
                Monster.execMonsterMove()
                self.MapScreen.log.addLine(Monster.Name+" has moved to "+Monster.Location.Name)
                return
            elif not Monster.Location.PlayerList:
                print "flying monster: I have no targets near by, returning to sky"
                self.Locations["Sky"].AddMonster(Monster)
                self.MapScreen.moveMonsterImage(Monster, self.Locations["Sky"])
                Monster.execMonsterMove()
            self.MapScreen.log.addLine(Monster.Name+" has moved to "+Monster.Location.Name)


    def SetupPhase(self):
        SetupStack = []
        self.CurrentStack = SetupStack
        self.CurrentPhase = "Setup"
        random.seed()

        #Setting up map
        
        Loader = XmlLoader.XmlLoader()
        
        XmlPath = os.getcwd()
        
        length = len(os.getcwd())
        
        XmlPath = XmlPath[0:(length - 7)]
        if(XmlPath[len(XmlPath)-1] == "\\"):
            XmlPath = XmlPath + "data\\Map\\Map.xml"
        if(XmlPath[len(XmlPath)-1] == "/"):
            XmlPath = XmlPath + "data/Map/Map.xml"
        Loader.LoadLocations(XmlPath)
        for Location in Loader.Locations :
            key = Location["Name"]
            self.Locations[key] = LocationClass.Location()
            self.Locations[key].Name = Location["Name"]
        for Location in Loader.Locations :
            key = Location["Name"]
            LocDict = Location["Map"]
            if "Other" in LocDict :
                self.Locations[key].AddConnection( self.Locations[LocDict["Other"]] )
            if "White" in LocDict :
                self.Locations[key].AddConnection( self.Locations[LocDict["White"]] )
                self.Locations[key].WhiteStreet = self.Locations[LocDict["White"]]
            if "Black" in LocDict :
                self.Locations[key].AddConnection( self.Locations[LocDict["Black"]] )
                self.Locations[key].BlackStreet = self.Locations[LocDict["Black"]]

            if "Neighborhood" in Location :
                        self.Locations[key].Neighborhood = Location["Neighborhood"]
            if "Stable" in Location :
                if Location["Stable"] == "True" :
                    self.Locations[key].Stability = "Stable"
                elif Location["Stable"] == "False" :
                    self.Locations[key].Stability = "Unstable"
                else :
                    self.Locations[key].Stability = "Stable"
            if "Location" in Location :
                if Location["Location"] == "False" :
                    self.Locations[key].Type = "Street"
                else :
                    self.Locations[key].Type = "Arkham"
            else :
                self.Locations[key].Type = "Arkham"
            if "Expected" in Location :
                self.Locations[key].Expected = Location["Expected"]
            if "Action" in Location :
                self.Locations[key].OptionalEncounter = Location["Action"]
                


        #Terror Limits
        self.Locations["General Store"].MaxTerrorLevel = 3
        self.Locations["Curiositie Shoppe"].MaxTerrorLevel = 6
        self.Locations["Ye Olde Magick Shoppe"].MaxTerrorLevel = 9
        #Misc Locations      
       
        #sky
        self.Locations["Sky"] = LocationClass.Location()
        self.Locations["Sky"].Name = "Sky"
        self.Locations["Sky"].Type = "Sky"
        self.Locations["Sky"].Neighborhood = "None"
        self.Locations["Sky"].FlavorText = "The Sky is a holding area considered to be a street that is connected to every street area in Arkham.Flying monsters in the Sky can swoop down on investigators on any street during the Monster movement portion of the Mythos phase. Monsters in the Sky still count towards the monster limit."
        #outskirts
        self.Locations["Outskirts"] = LocationClass.Location()
        self.Locations["Outskirts"].Name = "Outskirts"
        self.Locations["Outskirts"].Type = "Outskirts"
        self.Locations["Outskirts"].Neighborhood = "None"
        self.Locations["Outskirts"].FlavorText = "The Outskirts is a space on the board for monsters that should be in Arkham, but exceed the monster limit. The Outskirts has its own limit, equal to (8 - the number of investigators). If a monster should enter the Outskirts when it is at the limit, all monsters in the Outskirts are returned to the monster cup, and the Terror level goes up by one."                
        #LITAS
        self.Locations["Lost in Time and Space"] = LocationClass.Location()
        self.Locations["Lost in Time and Space"].Name = "Lost in Time and Space"
        self.Locations["Lost in Time and Space"].Type = "LITAS"
        self.Locations["Lost in Time and Space"].Neighborhood = "None"
        self.Locations["Lost in Time and Space"].FlavorText = "Lost in Time and Space."
        #Otherworld
        self.Locations["The Abyss"] = LocationClass.Location()
        self.Locations["The Abyss"].Name = "The Abyss"
        self.Locations["The Abyss"].Type = "Otherworld"
        self.Locations["The Abyss"].Neighborhood = ["Blue","Red"]
        self.Locations["The Abyss2"] = LocationClass.Location()
        self.Locations["The Abyss2"].Name = "The Abyss2"
        self.Locations["The Abyss2"].Type = "Otherworld"
        self.Locations["The Abyss2"].Neighborhood = ["Blue","Red"]
        self.Locations["The Abyss"].Connections.append( self.Locations["The Abyss2"] )
        
        self.Locations["Another Dimension"] = LocationClass.Location()
        self.Locations["Another Dimension"].Name = "Another Dimension"
        self.Locations["Another Dimension"].Type = "Otherworld"
        self.Locations["Another Dimension"].Neighborhood = ["Blue","Green","Red","Yellow"]
        self.Locations["Another Dimension2"] = LocationClass.Location()
        self.Locations["Another Dimension2"].Name = "Another Dimension2"
        self.Locations["Another Dimension2"].Type = "Otherworld"
        self.Locations["Another Dimension2"].Neighborhood = ["Blue","Green","Red","Yellow"]
        self.Locations["Another Dimension"].Connections.append( self.Locations["Another Dimension2"] )

        self.Locations["The City of the Great Race"] = LocationClass.Location()
        self.Locations["The City of the Great Race"].Name = "The City of the Great Race"
        self.Locations["The City of the Great Race"].Type = "Otherworld"
        self.Locations["The City of the Great Race"].Neighborhood = ["Green","Yellow"]
        self.Locations["The City of the Great Race2"] = LocationClass.Location()
        self.Locations["The City of the Great Race2"].Name = "The City of the Great Race2"
        self.Locations["The City of the Great Race2"].Type = "Otherworld"
        self.Locations["The City of the Great Race2"].Neighborhood = ["Blue","Red"]
        self.Locations["The City of the Great Race"].Connections.append( self.Locations["The City of the Great Race2"] )        

        self.Locations["Great Hall of Celeano"] = LocationClass.Location()
        self.Locations["Great Hall of Celeano"].Name = "Great Hall of Celeano"
        self.Locations["Great Hall of Celeano"].Type = "Otherworld"
        self.Locations["Great Hall of Celeano"].Neighborhood = ["Blue","Green"]
        self.Locations["Great Hall of Celeano2"] = LocationClass.Location()
        self.Locations["Great Hall of Celeano2"].Name = "Great Hall of Celeano2"
        self.Locations["Great Hall of Celeano2"].Type = "Otherworld"
        self.Locations["Great Hall of Celeano2"].Neighborhood = ["Blue","Green"]
        self.Locations["Great Hall of Celeano"].Connections.append( self.Locations["Great Hall of Celeano2"] )

        self.Locations["Plateau of Leng"] = LocationClass.Location()
        self.Locations["Plateau of Leng"].Name = "Plateau of Leng"
        self.Locations["Plateau of Leng"].Type = "Otherworld"
        self.Locations["Plateau of Leng"].Neighborhood = ["Green","Red"]
        self.Locations["Plateau of Leng2"] = LocationClass.Location()
        self.Locations["Plateau of Leng2"].Name = "Plateau of Leng2"
        self.Locations["Plateau of Leng2"].Type = "Otherworld"
        self.Locations["Plateau of Leng2"].Neighborhood = ["Green","Red"]
        self.Locations["Plateau of Leng"].Connections.append( self.Locations["Plateau of Leng2"] )

        self.Locations["R'lyeh"] = LocationClass.Location()
        self.Locations["R'lyeh"].Name = "R'lyeh"
        self.Locations["R'lyeh"].Type = "Otherworld"
        self.Locations["R'lyeh"].Neighborhood = ["Red","Yellow"]
        self.Locations["R'lyeh2"] = LocationClass.Location()
        self.Locations["R'lyeh2"].Name = "R'lyeh2"
        self.Locations["R'lyeh2"].Type = "Otherworld"
        self.Locations["R'lyeh2"].Neighborhood = ["Red","Yellow"]
        self.Locations["R'lyeh"].Connections.append( self.Locations["R'lyeh2"] )

        self.Locations["The Dreamlands"] = LocationClass.Location()
        self.Locations["The Dreamlands"].Name = "The Dreamlands"
        self.Locations["The Dreamlands"].Type = "Otherworld"
        self.Locations["The Dreamlands"].Neighborhood = ["Blue","Green","Red","Yellow"]
        self.Locations["The Dreamlands2"] = LocationClass.Location()
        self.Locations["The Dreamlands2"].Name = "The Dreamlands2"
        self.Locations["The Dreamlands2"].Type = "Otherworld"
        self.Locations["The Dreamlands2"].Neighborhood = ["Blue","Green","Red","Yellow"]
        self.Locations["The Dreamlands"].Connections.append( self.Locations["The Dreamlands2"] )

        self.Locations["Yuggoth"] = LocationClass.Location()
        self.Locations["Yuggoth"].Name = "Yuggoth"
        self.Locations["Yuggoth"].Type = "Otherworld"
        self.Locations["Yuggoth"].Neighborhood = ["Blue","Yellow"]
        self.Locations["Yuggoth2"] = LocationClass.Location()
        self.Locations["Yuggoth2"].Name = "Yuggoth2"
        self.Locations["Yuggoth2"].Type = "Otherworld"
        self.Locations["Yuggoth2"].Neighborhood = ["Blue","Yellow"]
        self.Locations["Yuggoth"].Connections.append( self.Locations["Yuggoth2"] )        

        #Load Items here

        CardFunctions.StartDecks(self)
        self.DeckDictionary["Common"].Shuffle()
        self.DeckDictionary["Spell"].Shuffle()
        self.DeckDictionary["Skill"].Shuffle()
        self.DeckDictionary["Unique"].Shuffle()
        self.DeckDictionary["Ally"].Shuffle()



        #Loading Investigators

        XmlPath = os.getcwd()
        
        length = len(os.getcwd())
        
        XmlPath = XmlPath[0:(length - 7)]
        
        if(XmlPath[len(XmlPath)-1] == "\\"):
            XmlPath = XmlPath + "data\\Investigators\\Investigators.xml"
        if(XmlPath[len(XmlPath)-1] == "/"):
            XmlPath = XmlPath + "data/Investigators/Investigators.xml"

        Loader.LoadInvestigators(XmlPath)
        self.DeckDictionary["Investigator"] = list()
        for Investigator in Loader.Investigators :
            Investigator["SpSkillText"] = "Special Skill Text"
            Investigator["SpSkillFunc"] = "GenerateME"
            P = PlayerCharacter.PlayerChar(Investigator)
            P.Environment = self
            self.DeckDictionary["Investigator"].append( P )
        self.ShuffleInvestigators()



        #Choosing Investigators
        """
        Temporary
        """
        

        i = 1
        while (i <= self.NumOfPlayers):
            Player = CharSelect.browseList("Select your Player",self.DeckDictionary["Investigator"])
            self.AddPlayer(Player)
            self.Investigators.append(Player)
            self.PlayerIncoming.append(Player)
            self.DeckDictionary["Investigator"].remove(Player)
            Player.DrawRandomPossessions()
            i = i + 1

        
        #Loading AncientOnes
        
        XmlPath = os.getcwd()
        
        length = len(os.getcwd())
        
        XmlPath = XmlPath[0:(length - 7)]
        if(XmlPath[len(XmlPath)-1] == "\\"):
            XmlPath = XmlPath + "data\\AncientOnes\\AncientOnes.xml"
        if(XmlPath[len(XmlPath)-1] == "/"):
            XmlPath = XmlPath + "data/AncientOnes/AncientOnes.xml"
        Loader.LoadAncientOnes(XmlPath)
        self.DeckDictionary["AncientOne"] = list()
        for AO in Loader.AncientOnes :
            A = AncientOne.AncientOne( AO )
            A.Environment = self
            self.DeckDictionary["AncientOne"].append( A )

        #Choose ancient one
        self.AncientOne = CharSelect.browseList("Choose an Ancient One", self.DeckDictionary["AncientOne"])

        


        #Loading Monsters
                        
        XmlPath = os.getcwd()
        
        length = len(os.getcwd())
        
        XmlPath = XmlPath[0:(length - 7)]
        if(XmlPath[len(XmlPath)-1] == "\\"):
            XmlPath = XmlPath + "data\\Monster\\Monsters.xml"
        if(XmlPath[len(XmlPath)-1] == "/"):
            XmlPath = XmlPath + "data/Monster/Monsters.xml"
        Loader.LoadMonsters(XmlPath)
        self.DeckDictionary["Monster"] = list()
        self.DeckDictionary["Mask"] = list()
        for Monster in Loader.Monsters :  
            n = int(Monster["Amount"])
            while n > 0 :
                M = MonsterClass.Monster( Monster )
                M.Environment = self
                if M.Abilities["Mask"] == 1:
                    self.DeckDictionary["Mask"].append(M)
                else:    
                    self.DeckDictionary["Monster"].append( M )
                n = n - 1
        self.ShuffleMonsters()
        
        #Loading Gates

        XmlPath = os.getcwd()
        
        length = len(os.getcwd())
        
        XmlPath = XmlPath[0:(length - 7)]
        if(XmlPath[len(XmlPath)-1] == "\\"):
            XmlPath = XmlPath + "data\\Otherworld\\Gatemarkers\\OtherworldGatemarkers.xml"
        if(XmlPath[len(XmlPath)-1] == "/"):
            XmlPath = XmlPath + "data/Otherworld/Gatemarkers/OtherworldGatemarkers.xml"
        Loader.LoadGates(XmlPath)
        self.DeckDictionary["Gate"] = list()
        for Gate in Loader.Gates :  
            self.DeckDictionary["Gate"].append( GateClass.Gate( Gate ) )
        self.ShuffleGates()
        
        self.SetFirstPlayer()
        for x in self.PlayerIncoming :       
            self.AddTurn(self.SetupTurn)
        while self.TurnStack != [] :
            self.RunNextTurn()

        
    def InitialClueLocations(self):
        for Loc in self.Locations:
            if self.Locations[Loc].GetStability() == "Unstable":
                self.AddClue(self.Locations[Loc])

    def IncrementTerrorTrack(self):
        if self.TerrorLevel < 10:
            self.TerrorLevel = self.TerrorLevel + 1
            self.MapScreen.log.addLine("The terror level has increased to "+str(self.TerrorLevel))
            self.CheckForClosures()
        else:
            #increment Doomtrack
            self.MapScreen.log.addLine("The Terror level has reached its maximum and now is increasing the doom counter")
        self.MapScreen.updateLabels()

    def DecrementTerrorTrack(self):
        if self.TerrorLevel > 0:
            self.TerrorLevel = self.TerrorLevel - 1
            self.MapScreen.log.addLine("The terror level has decreased to "+str(self.TerrorLevel))
            self.CheckForClosures()
            self.MapScreen.updateLabels()

    def IncreaseDoomTrack(self):
        self.AncientOne.IncrementDoomTrack()
        self.MapScreen.updateLabels()
        self.FinalCheck()
    def DecreaseDoomTrack(self):
        self.AncientOne.DecrementDoomTrack()
        self.MapScreen.updateLabels()
        self.FinalCheck()
    def CheckForClosures(self):
        for key in self.Locations :
            if self.Locations[key].MaxTerrorLevel != 0 and self.Locations[key].MaxTerrorLevel <= self.TerrorLevel and self.Locations[key].Gate == None :
                self.Closure(self.Locations[key])
            
    def Closure(self,Location):
        if Location.IsClosed == 1:
            return
        self.MapScreen.log.addLine( Location.Name+" has closed due to the increased terror level!")
        Location.IsClosed = 1
        if len(Location.MonsterList) > 0:
            while Location.MonsterList :
                Monster = Location.MonsterList.pop()
                Location.Connections[0].AddMonster(Monster)
        if len(Location.PlayerList) > 0:
            while Location.PlayerList :
                Player = Location.PlayerList.pop()
                self.Teleport(Player, Location.Connections[0] )
            


    def SetCurrentPlayer(self):
        if( self.CurrentPlayer != None ):
            self.PlayerOutgoing.append( self.CurrentPlayer )
            self.CurrentPlayer = None
        if ( self.PlayerIncoming != [] ):
            self.CurrentPlayer = self.PlayerIncoming.pop(0)
            if type(self.MapScreen) != StringType:
                self.MapScreen.updateLabels()
            return self.CurrentPlayer
        else:
            return None

    def SetFirstPlayer(self):
        if( self.PlayerIncoming != [] ):
            for Player in self.PlayerIncoming :
                self.PlayerOutgoing.append( Player )
        if( self.CurrentPlayer != None ):
            self.PlayerOutgoing.append( self.CurrentPlayer )
        self.CurrentPlayer = None
        self.PlayerIncoming = self.PlayerOutgoing
        self.PlayerOutgoing = []
        OldFirstPlayer = self.PlayerIncoming.pop(0)
        self.PlayerIncoming.append(OldFirstPlayer)

            
    

    def AddCurrentStack(self, FunctionList):
        self.CurrentStack.append(FunctionList)
        """
        To use function stacks the following rules must be observed:
        Functions must be in form:  Function(ArgumentList)
        ex.  MyCards([CardName, CardType])
        
        Adding to the stack is done by:
        Environment.addCurrentStack([FunctionName, Arg1, Arg2, ...])
        No Arguments:  Environment.addCurrentStack([FunctionName])
        """

    def RunFunctionStack(self, FunctionStack):
        SaveStack = self.CurrentStack
        while (len(FunctionStack) > 0):
            FuncList = FunctionStack.pop()
            Function = FuncList.pop()
            if (len(FuncList) == 0):
                Function()
                self.CurrentStack = SaveStack
            else:
                Function(FuncList)
                self.CurrentStack = SaveStack
                
        """
        Insert in correct order or Append in reverse order
        
        This function simply represents the main loop that the start menu creates
        
        Add functionallity for argument lists
        Try and figure out how to add decks I suppose.
        """
    def FakeFunctionStack(self):
        BigStack = []
        
        BigStack.insert(0,[self.UpkeepPhase])
        BigStack.insert(0,[self.MovementPhase])
        BigStack.insert(0,[self.EncounterPhase])
        BigStack.insert(0,[self.MythosPhase])
        self.RunFunctionStack(BigStack)

    def PlayerByName(self, Name):
        for x in self.Investigators:
            if (Name == x.Name):
                return x

    def ChooseArkhamLocation(self):
        ArkhamLocations = []
        for loc in self.Locations:
            if(loc.Type == "Arkham"):
                ArkhamLocations.append(loc)
        Text = []
        for loc in ArkhamLocations:
            Text.append(loc.Name)
        selected = ChooseListDialog.Run("Choose One", "Choose a Location", Text)
        return self.Locations[selected]

    def PickPlayer(self):
        TotalPlayers = []
        TotalPlayers.append(self.CurrentPlayer)
        TotalPlayers = TotalPlayers + self.PlayerIncoming + self.PlayerOutgoing
        Text = []
        for player in TotalPlayers:
            Text.append(player.Name)
        selected = ChooseListDialog.Run("Choose One", "Choose a Player", Text)
        for invest in self.Investigators:
            if invest.Name == selected:
                return invest

        return self.CurrentPlayer
    
    def RefreshCards(self):
        for card in self.ExhaustedCardList:
            card[4](card, "refresh")
        self.ExhaustedCardList = []
