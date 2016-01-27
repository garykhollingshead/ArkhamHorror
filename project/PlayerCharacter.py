"""
PlayerCharacter class file
----------------------------
----------------------------------------------------------------------
Trophies
When a monster/gate is defeated by a player, it is removed from its location
and put into the players inventory, or in our case the Trophies variable.
The trophies are housed within the variable, as players should be able
to view the trophies and/or exchange them for goods,services,etc.
-----------------------------------------------------------------------
-----------------------------------------------------------------------
Updated: Zack 03/01/2010
-Sliders are divided into three categories: Mobility, Combat, Mental
-When the GUI calls these functions, they are passed 'magnitude', which
    is the change in the slider since the last call, NOT the position of the
    slider.
-First the functions check that the slider has not escaped the bounds
    of 0 to 3.
-Second the functions check that the user has enough focus to move the slider.

-Third, if the previous two checks haven't put up red flags, the function
    recalculates the slider, and combines the base stats and the slider to
    formulate the new stat value.

-The return value is the new position of the combat slider in all three cases. This
    is still experimental but the thought is that it will tell the gui where to set
    the slider after calling the changeXXXXXXXslider function.
-A future feature might be to provide feedback as to why the stat slide failed,
    but for now basic functionality suffices.
------------------------------------------------------------

Zack: Note that the BASE stats for our slider attributes are
the far left values (at the moment).  However, XML has them stored
as the the right most value for the stats inversely affected by a positive movement
it is easier to translate them into their leftmost value.
Example:        |   XML     |   Base stat
Speed 1 2 3 4   |   1       |   1
Sneak 5 4 3 2   |   2       |   5

To translate an inverted stat from XML to Base, simply add 3, as our sliders are 0 - 3.

-------------------------------------------------------------
Further Update: Zack 03/03/2010 - Using dictionary instead of list
Updated: Zack 03/01/2010   ***Temporarily Paused while seeking council***
The major change that is going to happen with this class' creation, is it will, instead of taking
23 arguments, it takes a giant Dictionary.
"""
#XXXXXXXXXXXXXXXXXXXXXXXXXXXX===IMPORTANT===XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#This input dictionary as of 3-3-10 has the following keys:
#[ Name , Title, Story, Home, Sanity, Stamina,
#  Focus, Speed, Sneak, Fight, Will, Lore, Luck,
#  Image, Fixed[ list of fixed items ], Random[ list of random items ]
#  SpSkillText, SpSkillFunc
#]
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
COPY AND PASTE THIS EXAMPLE DICTIONARY FOR TESTING PURPOSES:
                        {'Name': "Terry" ,
                         'Title': "the Test Dummy",
                         'Story': "Terry was made in 1952 in order to crash test rockets",
                         'Home': "Lost in Time and Space",
                         'Sanity': 3,
                         'Stamina': 5,
                         'Focus': 2,
                         'Speed': 1,
                         'Sneak': 4,
                         'Fight': 2,
                         'Will': 5,
                         'Lore': 0,
                         'Luck': 3,
                         'Picture': "Placeholder.jpg",
                         'Fixed': [ "$5", "Gun" ],
                         'Random': [ "Skill(1)", "CommonItem(1)" ],
                         'SpSkillText': [ "Crash" , "You lose all stamina and sanity, and are lost in time and space."],
                         'SpSkillFunc': ["Placeholder"]
                         }
                         
list of fixed and random items have the following sub order
[ money , spell, item, skill, clue, ally ]
Quality Control and Input sanitation is handled when the investigator info is
extracted from file. Assume all inputs are valid once __init__ has them.
---------------------------------------------------------------------------------------------------------
FUTURE MILESTONES:
         -zack: Implement player inventory, as currently, no such capabilities exist.
        
CHANGE LOG:
03/03/2010:Zack: Formatting changes, fixed PC creation by adding dictionary and plugging into variables.

02/27/2010:Zack: Major overhawl of the class has begun. It shall be brought up to speed.
to               Removed much of the variable explanation stubs, as it was not needed for most
03/02/2010       of these variables (e.g. Name, Location, etc...)

01/29/2010:Miguel: I added more functionality to Move(), CloseGate(), SealGate(), ChangeSkillSlider() methods
I also created merged Stamina, Sanity, Focus, etc.. variable into one dictionary and called it 'Stats'. I also
merged the IsBlessed, IsCursed, Lost variables into one dictionary and called it StatusTable. 
01/21/2010:Miguel:I created file and the basic skeleton of the
class (all the attributes, and methods).
"""
import LocationClass
import characterscreen
import os

class PlayerChar:
    def __init__(self, InvDict):

        self.Name = InvDict["Name"] 
        self.Title = InvDict["Title"]
        self.Story = InvDict["Story"]
        self.MoneyPerUpkeep = 0
        self.Type = "Player"

        #Find image path for the investigators

        InvestigatorPicturePath = os.getcwd()
        length = len(os.getcwd())
        InvestigatorPicturePath = InvestigatorPicturePath[0:(length - 7)]
        if(InvestigatorPicturePath[len(InvestigatorPicturePath)-1] == "\\"):
            InvestigatorPicturePath = InvestigatorPicturePath + "data\\Investigators\\Images\\"
        if(InvestigatorPicturePath[len(InvestigatorPicturePath)-1] == "/"):
            InvestigatorPicturePath = InvestigatorPicturePath + "data/Investigators/Images/"
            
        self.Graphic = InvestigatorPicturePath + InvDict["Picture"]
        self.SelectionPicture = self.Graphic[0:len(self.Graphic) - 4] + "front.jpg"
        
        #XML uses top end stats, we're going to use bottom
        InvDict["Sneak"] = InvDict["Sneak"] + 3
        InvDict["Will"] = InvDict["Will"] + 3
        InvDict["Luck"] = InvDict["Luck"] + 3

        #The basic, modifyable stats
        self.Stats =    {'Stamina':InvDict["Stamina"],
                         'Sanity':InvDict["Sanity"],
                         'Focus':InvDict["Focus"],
                         'Speed':InvDict["Speed"],
                         'Sneak':InvDict["Sneak"],
                         'Fight':InvDict["Fight"],
                         'Will':InvDict["Will"],
                         'Lore':InvDict["Lore"],
                         'Luck':InvDict["Luck"],
                         'MaxSanity':InvDict["Sanity"],
                         'MaxStam':InvDict["Stamina"],
                         'MaxFocus':InvDict["Focus"]}

        #NEVER to be modified stats.  The stats on the card
        self.BaseStats= {'Speed':InvDict["Speed"],
                         'Sneak':InvDict["Sneak"],
                         'Fight':InvDict["Fight"],
                         'Will':InvDict["Will"],
                         'Lore':InvDict["Lore"],
                         'Luck':InvDict["Luck"]}

        #Stats that are given as bonuses
        self.BonusStats = {'Stamina': 0 ,
                           'Sanity': 0 ,
                           'Focus': 0 ,
                           'Speed': 0 ,
                           'Sneak': 0 ,
                           'Fight': 0 ,
                           'Will': 0 ,
                           'Lore': 0 ,
                           'Luck': 0 ,
                           'MaxSanity': 0 ,
                           'MaxStam':  0,
                           'MaxFocus': 0,
                           'Combat': 0,
                           'Physical':0,    #physical combat rating
                           'Magical':0,      #magical combat rating
                           'Movement':0}     

        self.FixedPossessions = InvDict["Fixed"]
        self.RandomPossessions = InvDict["Random"]
        
        self.Location = InvDict["Home"]
        self.Home = InvDict["Home"]
        
        self.UniqueAbilityFlavorText = InvDict["SpSkillText"]
        self.UniqueAbilityInstructions = InvDict["SpSkillFunc"]
        self.IsUniqueAbilityExhausted = 0

        self.GateTrophies = []
        self.MonsterTrophies = []

        self.CurrentMovementPoints = 0
        
        self.MobilitySlider = 0
        self.CombatSlider = 0
        self.MentalSlider = 0

        self.AutoPass = { 'Evade':0,
                          'Combat':0}

        
        self.Clues = self.FixedPossessions["clue"]
        self.Money = self.FixedPossessions["money"]

        #The various buffs and debuffs a character can get
        self.Status =   {   'Blessed': 0,
                            'Cursed': 0,
                            'Retainer': 0,
                            'SilverLodgeMember': 0,
                            'Deputy': 0,
                            'BankLoan': 0,
                            'Delayed': 0,
                            'Lost': 0}

        #Character screen sliders
        self.Slider1 = 0
        self.Slider2 = 0
        self.Slider3 = 0

        #Equipped items
        self.LeftHandItem = []
        self.RightHandItem = []

        #Total Items
        self.ItemList = []

        #The monster the player is fighting
        self.FightingMonster = None
        
        self.EOPStack = []  #end of Phase
        self.EOTStack = []  #end of Turn
        self.EOCStack = []  #end of Combat
        self.EOSStack = []  #end of Skillcheck

        self.ExecSOCStack = [] #Start of combat, elements are strings
        self.ExecEOCStack = [] #End of combat, elements are strings

        #These are bonuses to checks, but not to stats themselves
        self.CheckBonus = {'Combat': 0 ,
                           'Evade': 0 ,
                           'Fight': 0 ,
                           'Speed': 0 ,
                           'Sneak': 0 ,
                           'Fight': 0 ,
                           'Will': 0 ,
                           'Lore': 0 ,
                           'Luck': 0 ,
                           'Horror': 0 ,
                           'Spell': 0}

        #The number of dies a character rolls per clue token spent
        self.CluetoDie = {'Combat': 1 ,
                           'Evade': 1 ,
                           'Fight': 1 ,
                           'Speed': 1 ,
                           'Sneak': 1 ,
                           'Fight': 1 ,
                           'Will': 1 ,
                           'Lore': 1 ,
                           'Luck': 1 ,
                           'Horror': 1 ,
                           'Spell': 1}

        #A list of cards that give rerolls, sorted by stats
        self.Reroll = {'Combat': [] ,
                           'Evade': [] ,
                           'Fight': [] ,
                           'Speed': [] ,
                           'Sneak': [] ,
                           'Fight': [] ,
                           'Will': [] ,
                           'Lore': [] ,
                           'Luck': [] ,
                           'Horror': [] ,
                           'Spell': [],
                           'Any':[]}

        #Activating these (toggle to 1) will negate a monsters abilities
        self.CancelAbilities = {'PhysicalResistance': 0,
                          'PhysicalImmunity': 0,
                          'MagicalResistance': 0,
                          'MagicalImmunity': 0,
                          'Ambush': 0,
                          'Endless': 0,
                          'Mask': 0,
                          'Nightmarish': 0,
                          'Overwhelming': 0,
                          'Undead': 0}

        #Absorbs that are not one time use
        self.PassiveAbsorb = {"Stamina": 0,
                              "Sanity":0}

        #Absorbs that expire after absorbing the stamina/sanity
        self.ActiveAbsorb = {"Stamina": 0,
                              "Sanity":0}

        #Load various character specials
        if(self.Name == "Harvey Walters"):
            print "Special Loaded: Harvey Walters"
            self.PassiveAbsorb["Sanity"] += 1
        if(self.Name == "Michael McGlen"):
            print "Special Loaded: Michael McGlen"
            self.PassiveAbsorb["Stamina"] += 1
        if(self.Name == "Jenny Barnes"):
            print "Special Loaded: Jenny Barnes"
            self.MoneyPerUpkeep += 1
        if(self.Name == "Joe Diamond"):
            print "Special Loaded: Joe Diamond"
            for key in self.CluetoDie:
                self.CluetoDie[key] += 1

        

    def DrawRandomPossessions(self):
        if "unique" in self.RandomPossessions:
            x = int(self.RandomPossessions["unique"])
            while (x > 0):
                self.ItemList.append(
                    self.Environment.DeckDictionary["Unique"].DrawCard(self, "none"))
                x = x - 1
        if "common" in self.RandomPossessions:
            x = int(self.RandomPossessions["common"])
            while (x > 0):
                self.ItemList.append(
                    self.Environment.DeckDictionary["Common"].DrawCard(self, "none"))
                x = x - 1
        if "skill" in self.RandomPossessions:
            x = int(self.RandomPossessions["skill"])
            while (x > 0):
                self.ItemList.append(
                    self.Environment.DeckDictionary["Skill"].DrawCard(self, "none"))
                x = x - 1
        if "ally" in self.RandomPossessions:
            x = int(self.RandomPossessions["ally"])
            while (x > 0):
                self.ItemList.append(
                    self.Environment.DeckDictionary["Ally"].DrawCard(self, "none"))
                x = x - 1
        if "spell" in self.RandomPossessions:
            x = int(self.RandomPossessions["spell"])
            while (x > 0):
                self.ItemList.append(
                    self.Environment.DeckDictionary["Spell"].DrawCard(self, "none"))
                x = x - 1

    #Unused, print for debugging
    def UsesSpecialSkill(self):
        print "UsesSpecialSkill method invoked"
        return 1

    #Change a players stats based on sliding the circle on the card
    def ChangeMobilitySlider(self,magnitude):
        if self.Environment.CurrentPhase == "Setup":
            self.MobilitySlider = self.MobilitySlider + magnitude
            self.Stats["Speed"] = self.BaseStats["Speed"] + self.MobilitySlider
            self.Stats["Sneak"] = self.BaseStats["Sneak"] - self.MobilitySlider
            return self.MobilitySlider #success
        elif  (magnitude + self.MobilitySlider) < 0 or (magnitude + self.MobilitySlider) > 3 :
            return self.MobilitySlider #illegal move
        elif abs(magnitude) > self.Stats["Focus"] :
            return self.MobilitySlider #not enough focus for move
        else:
            self.MobilitySlider = self.MobilitySlider + magnitude
            self.Stats["Focus"] = self.Stats["Focus"] - abs(magnitude)
            self.Stats["Speed"] = self.BaseStats["Speed"] + self.MobilitySlider
            self.Stats["Sneak"] = self.BaseStats["Sneak"] - self.MobilitySlider
            return self.MobilitySlider #success
        
    def ChangeCombatSlider(self,magnitude):
        if self.Environment.CurrentPhase == "Setup":
            self.CombatSlider = self.CombatSlider + magnitude
            self.Stats["Fight"] = self.BaseStats["Fight"] + self.CombatSlider
            self.Stats["Will"] = self.BaseStats["Will"] - self.CombatSlider
            return self.CombatSlider #success
        elif  (magnitude + self.CombatSlider) < 0 or (magnitude + self.CombatSlider) > 3 :
            return self.CombatSlider #illegal move
        elif abs(magnitude) > self.Stats["Focus"] :
            return self.CombatSlider #not enough focus for move
        else:
            self.CombatSlider = self.CombatSlider + magnitude
            self.Stats["Focus"] = self.Stats["Focus"] - abs(magnitude)
            self.Stats["Fight"] = self.BaseStats["Fight"] + self.CombatSlider
            self.Stats["Will"] = self.BaseStats["Will"] - self.CombatSlider
            return self.CombatSlider #success
        
    def ChangeMentalSlider(self,magnitude):
        if self.Environment.CurrentPhase == "Setup":
            self.MentalSlider = self.MentalSlider + magnitude
            self.Stats["Lore"] = self.BaseStats["Lore"] + self.MentalSlider
            self.Stats["Luck"] = self.BaseStats["Luck"] - self.MentalSlider
            return self.MentalSlider #success
        elif  (magnitude + self.MentalSlider) < 0 or (magnitude + self.MentalSlider) > 3 :
            return self.MentalSlider #illegal move
        elif abs(magnitude) > self.Stats["Focus"] :
            return self.MentalSlider #not enough focus for move
        else:
            self.MentalSlider = self.MentalSlider + magnitude
            self.Stats["Focus"] = self.Stats["Focus"] - abs(magnitude)
            self.Stats["Lore"] = self.BaseStats["Lore"] + self.MentalSlider
            self.Stats["Luck"] = self.BaseStats["Luck"] - self.MentalSlider
            return self.MentalSlider #success

    #Increases and decreases stamina and accounts for absorbtion and checks for death
    def ModHealth(self, magnitude):
        if magnitude < 0:
            magnitude = min( 0 , magnitude - self.PassiveAbsorb["Stamina"])
        if magnitude < 0:
            while self.ActiveAbsorb["Stamina"] > 0 and magnitude < 0:
                self.ActiveAbsorb["Stamina"] -= 1
                magnitude += 1
        self.Stats["Stamina"] = min( max(0, self.Stats["Stamina"] + magnitude), self.Stats["MaxStam"] + self.BonusStats["MaxStam"])
        if magnitude > 0:
            self.Environment.MapScreen.log.addLine(self.Name+" has gained "+str(magnitude)+" stamina.")
        elif magnitude < 0:
            self.Environment.MapScreen.log.addLine(self.Name+" has lost "+str(magnitude)+" stamina.")                                                 
        if self.Stats["Stamina"] <= 0:
            if(self.Environment.CurrentPhase != "Final"):
                self.Environment.Unconscious(self)

    #Increases and decreases stamina and accounts for absorbtion, checks for insane
    def ModSanity(self, magnitude):
        if magnitude < 0:
            magnitude = min( 0 , magnitude - self.PassiveAbsorb["Sanity"])
        if magnitude < 0:
            while self.ActiveAbsorb["Sanity"] > 0 and magnitude < 0:
                self.ActiveAbsorb["Sanity"] -= 1
                magnitude += 1  
        self.Stats["Sanity"] = min( max(0, self.Stats["Sanity"] + magnitude), self.Stats["MaxSanity"] + self.BonusStats["MaxSanity"])
        if self.Stats["Sanity"] <= 0:
            if(self.Environment.CurrentPhase != "Final"):
                self.Environment.Insane(self)

    #These functions perform various actions related to items
    def AddItem(self, Item):
        if Item[0] != "No cards to draw":
            self.ItemList.append(Item)

    def Curse(self):
        if self.Status["Blessed"] > 0:
            self.Status["Blessed"] = 0
        else:
            self.Status["Cursed"] = 1
            
    def Bless(self):
        if self.Status["Cursed"] > 0:
            self.Status["Cursed"] = 0
        else:
            self.Status["Blessed"] = 1
        
    def UseItem(self, card):
        print "UseItem method invoked"
        card[4](card, "use")

        return 1

    def CastSpell(self, card):
        print "CastSpell method invoked"
        card[4](card, "use")

        return 1


    def Equip(self, card):
        print "Equip method invoked"
        card[4](card, "equip")
        return 1

    #Checks to see if a hand is empty or a placeholder, If it isn't unequip
    def UnequipItems(self):
        if(self.LeftHandItem != []):
            if(self.RightHandItem[0] != "No Items"):
                self.Unequip(self.LeftHandItem)
        if(self.RightHandItem != []):
            if(self.RightHandItem[0] != "No Items"):
                self.Unequip(self.RightHandItem)
        self.LeftHandItem = []
        self.RightHandItem = []
            
    def Unequip(self, card):
        print "Unequip method invoked"
        print card
        print card[4]
        card[4](card, "unequip")

    def Discard(self,card):
        print "Discard method invoked"
        card[4](card, "discard")
        return 1
    #Gives a player a gate trophy
    def AddGateTrophy(self,GateTrophy):
        try:
            GateTrophy.Location.RemoveGate(GateTrophy)
        except(ValueError,KeyError,AttributeError):
            print "nonthreatening exception"
        self.GateTrophies.append(GateTrophy)
    #Removes a player gate trophy
    def RemoveGateTrophy(self,GateTrophy):
        self.GateTrophies.remove(GateTrophy)
    #Add monster trophy
    def AddMonsterTrophy(self,MonsterTrophy):
        try:
            MonsterTrophy.Location.RemoveMonster(MonsterTrophy)
        except(ValueError,KeyError,AttributeError):
            print "nonthreatening exception"
        self.MonsterTrophies.append(MonsterTrophy)
    #Remove monster trophy from player    
    def RemoveMonsterTrophy(self,MonsterTrophy):
        self.MonsterTrophies.remove(MonsterTrophy)
        
    #refills a players focus to max
    def RefillFocus(self):
        print "Refilling Focus"
        self.Stats["Focus"] = self.Stats["MaxFocus"] + self.BonusStats["MaxFocus"]
        
    #drain a players unspent focus
    def DrainFocus(self):
        print "Draining Focus"
        self.Stats["Focus"] = 0
    #Removes the monster from the board and gives the trophy to the player (unless it is endless)
    def DefeatMonster(self, Monster):
        if(Monster.Abilities["Endless"] != 1):
            self.AddMonsterTrophy(Monster)
        else:
            self.Environment.ReturnMonster(Monster)
    #uses Exec on a stack
    def RunExecStack(self, stack):
        if(stack != []):
            for element in stack:
                exec(element)
    #Gives the player their "salary"            
    def GiveMoneyPerUpkeep(self):
        self.Money = self.Money + self.MoneyPerUpkeep
    #Does each investigators Upkeep Function
    def UpkeepFunction(self):
        #Remove Mandy's reroll
        for card in self.Reroll["Any"]:
            if(card[0] == "Mandys Reroll"):
                self.Reroll["Any"].remove(card)
                
        if(self.Name == "Carolyn Fern"):
            TextList = []
            for player in self.Location.PlayerList:
                if player.Stats["Sanity"] < (player.Stats["MaxSanity"]+player.BonusStats["MaxSanity"]):
                    TextList.append(player.Name)
            if not TextList :
                return
            choice = self.Environment.ListChoose("Carolyn Fern Special", "Choose a Player to give Sanity to", TextList)
            for player in self.Location.PlayerList:
                if(player.Name == choice):
                    Ans = player
            Ans.ModSanity(1)
        if(self.Name == "Vincent Lee"):
            TextList = []
            for player in self.Location.PlayerList:
                if player.Stats["Stamina"] < (player.Stats["MaxStam"]+player.BonusStats["MaxStam"]):
                    TextList.append(player.Name)
            if not TextList :
                return
            choice = self.Environment.ListChoose("Vincent Lee Special", "Choose a Player to give Stamina to", TextList)
            for player in self.Location.PlayerList:
                if(player.Name == choice):
                    Ans = player
            Ans.ModHealth(1)
        if(self.Name == "Mandy Thompson"):
            PlayerList = []
            TextList = []
            PlayerList = self.Environment.Investigators
            for Player in PlayerList:
                TextList.append(Player.Name)
            choice = self.Environment.ListChoose("Mandy Thompson Special", "Choose a Player recieve your Reroll for the turn", TextList)
            for player in PlayerList:
                if(player.Name == choice):
                    Ans = player
            Ans.Reroll["Any"].append(["Mandys Reroll",  "","","",self.MandyReroll])
        
        pass
    #Mandy's Reroll (blank function)
    def MandyReroll(self, card, Usage):
        pass
