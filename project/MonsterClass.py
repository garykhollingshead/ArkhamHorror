"""
Monster class file
-------------------
This class would hold the basic info of the monsters (name, Toughness,etc..)

-------------------
Monsters that need actions:
Bloated Woman, Black Man, Dark Pharoah, Warlock, NightGaunt
-------------------
CHANGE LOG:
01/21/2010:Miguel:I created the file and the basic skeleton of the class
(attributes, methods)

4/20
Zack: Changing input to init to be a dictionary, which is recieved from xml loader.  Also changed the Setabilities to work with the input we're given.
Removed spaces in some of dictionary keys in Abilities.
"""

class Monster:
    def __init__(self,  MonsterDict ):
        self.Name = MonsterDict["Name"]
        self.Environment = ""
        self.UniqueID = self.Name
        self.Picture = MonsterDict["Picture"]
        self.SpecialActivated = 0
        self.Type = "Monster"
        if "MoveFunction" in MonsterDict:
            self.MoveFunction = MonsterDict["MoveFunction"]
        self.Location = None
        if "AttackFunction" in MonsterDict:
            self.AttackFunction = MonsterDict["AttackFunction"]
        if "BeforeHorror" in MonsterDict:
            self.BeforeHorror = MonsterDict["BeforeHorror"]
        if "AfterHorror" in MonsterDict:
            self.AfterHorror = MonsterDict["AfterHorror"]
        if "Movement" in MonsterDict :
            self.Movement = MonsterDict["Movement"]
        else:
            self.Movement = "None"
        if "SneakCheck" in MonsterDict :
            self.Awareness = int(MonsterDict["SneakCheck"])
        else:
            self.Awareness = 0
        if "CombatCheck" in MonsterDict :
            if len(MonsterDict["CombatCheck"]) <= 2 :
                self.CombatRating = int(MonsterDict["CombatCheck"])
            else:
                self.CombatRating = 0
        else:
            self.CombatRating = 0
        if "CombatDamage" in MonsterDict :
            if len(MonsterDict["CombatDamage"]) <= 2 :
                self.StaminaDamage = int(MonsterDict["CombatDamage"])
            else:
                 self.StaminaDamage = 0  
        else:
            self.StaminaDamage = 0
        if "HorrorCheck" in MonsterDict :
            if len(MonsterDict["HorrorCheck"]) <= 2 :
                self.HorrorRating = int(MonsterDict["HorrorCheck"])
            else:
                self.HorrorRating = 0
        else:
            self.HorrorRating = 0
        if "SanityDamage" in MonsterDict :
            if len(MonsterDict["SanityDamage"]) <= 2 :
                self.SanityDamage = int(MonsterDict["SanityDamage"])
            else:
                 self.SanityDamage = 0  
        else:
            self.SanityDamage = 0
        if "Toughness" in MonsterDict :
            self.Toughness = int(MonsterDict["Toughness"])
        else:
            self.Toughness = 0
        self.BaseAbilities = {'PhysicalResistance': 0,
                          'PhysicalImmunity': 0,
                          'MagicalResistance': 0,
                          'MagicalImmunity': 0,
                          'Ambush': 0,
                          'Endless': 0,
                          'Mask': 0,
                          'Nightmarish': 0,
                          'Overwhelming': 0,
                          'Undead': 0}
        self.Abilities = {'PhysicalResistance': 0,
                          'PhysicalImmunity': 0,
                          'MagicalResistance': 0,
                          'MagicalImmunity': 0,
                          'Ambush': 0,
                          'Endless': 0,
                          'Mask': 0,
                          'Nightmarish': 0,
                          'Overwhelming': 0,
                          'Undead': 0}
        self.SetAbilities(MonsterDict)
        for key in self.BaseAbilities.keys():
            self.Abilities[key] = self.BaseAbilities[key]
        if "Description" in MonsterDict :
            self.FlavorText = MonsterDict["Description"]
        else:
            self.FlavorText = ""
        if "Symbol" in MonsterDict :
            self.HomeDimension = MonsterDict["Symbol"]
        else:
            self.HomeDimension = "None"
    def execMonsterMove(self):
        print self.Name, "moving", self.HomeDimension
        exec(self.MoveFunction)

    def execMonsterAttack(self):
        exec(self.AttackFunction)

    def execBeforeHorror(self):
        if(self.Name != "The Bloated Woman"):
            exec(self.BeforeHorror)
            return "Pass"
        else:
            return FailHorrorandCombat(self)
    def execAfterHorror(self):
        exec(self.AfterHorror)

    def SetAbilities(self, MonsterDict):
        for key in MonsterDict.keys() :
            if key in self.BaseAbilities :
                self.BaseAbilities[key] = 1

    def HoundOfTindalosMove(self):
        print self.Name, "is moving"


    def ChthonianMove(self):
        print self.Name, "moving?"
        self.Environment.MapScreen.log.addLine("Chthonian Move Func")
        for player in self.Environment.Investigators:
            result = self.Environment.RollDie()
            if(result >= 4 and result <= 6):
                self.Environment.MapScreen.log.addLine(
                    "Chthonian did sanity loss to: " + player.Name)
                player.Stats["Sanity"] -= 1

    def TimeandspaceAttack(self):
        self.Environment.MapScreen.log.addLine("time and space attack")
        self.Environment.Teleport(self.Environment.CurrentPlayer,
                                  self.Environment.Locations["Lost in Time and Space"])
    def PlayerLosesItem(self):
        List = []
        if(len(self.Environment.CurrentPlayer.ItemList) > 0):
            for item in self.Environment.CurrentPlayer.ItemList:
                List.append(item[1])
            discarded = self.Environment.ListChoose("Discard", "Choose an Item to discard", List)
            
            answer = self.Environment.CurrentPlayer.ItemList[0]
            for item in self.Environment.CurrentPlayer.ItemList:
                if(item[0] == discarded):
                    answer = item
        
            self.Environment.CurrentPlayer.Discard(answer)

    def ManiacSpecial(self):
        if(self.SpecialActivated == 1):
            if(self.Environment.TerrorLevel >= 6):
                self.Environment.MapScreen.log.addLine("Maniac is going crazy!")
                self.Abilities["Endless"] = 1
                self.CombatRating += -2
                self.StaminaDamage = 3
                self.SpecialActivated = 1

    def SuckPlayerThroughGate(self):
        #Sucks the player through nearest gate, if tie then they choose.
        MinDist = 15
        Destination = self.Location
        for gate in self.Environment.Gates:
            dist = len(self.Environment.FindShortestPath(gate.Location, self.Location))
            if(dist <= MinDist):
                MinDist = dist
                Destination = gate.Location
        self.Environment.Teleport(self.Environment.CurrentPlayer, Destination)      
        self.Environment.MapScreen.log.addLine("You are sucked into the nearest gate!")

    def RemoveGive2Clues(self):
        self.CurrentPlayer.Clues += 2
        if self.Location != None:
            self.Location.RemoveMonster(Monster)
        if self in self.Environment.Monsters :
            self.Environment.Monsters.remove(self)

    def GotoNearestInvestigator(self):
        MinDist = 15
        Destination = self.Location
        for player in self.Environment.Investigators:
            if(player.Location.Name != "St Marys Hospital"):
                if(player.Location.Name != "Arkham Asylum"):
                    dist = len(self.Environment.FindShortestPath(player.Location, self.Locatoin))
                    if(dist <= MinDist):
                        MinDist = dist
                        Destination = player.Location
        Destination.AddMonster(self)
        self.Environment.MapScreen.moveMonsterImage(self, Destination)
        self.Environment.MapScreen.log.addLine(self.Name+" has moved to "+self.Location.Name)
        
    
    def FailHorrorandCombat(self):
        check = self.Environment.SkillCheck("Will", self.CurrentPlayer, 1, -2)
        if(check == "Fail"):
            self.Environment.CurrentPlayer.Stats["Sanity"] = self.Enviornment.CurrentPlayer.Stats["Sanity"] - self.SanityDamage
            EventDialog.Run("Failure!", "You failed the horror check.\n You have lost "+str(self.SanityDamage)+" Sanity")
            self.Player.Stats["Stamina"] = self.Player.Stats["Stamina"] - self.Monster.StaminaDamage
            EventDialog.Run("Failure!", "You failed the combat check, the monster attacks!.\n You have lost "+str(self.Monster.StaminaDamage)+" Stamina")
        return check

    def LuckorBeDevoured(self):
        check = self.Environment.SkillCheck("Luck", self.CurrentPlayer, 1, -1)
        if(check == "Pass"):
            self.Environment.CurrentPlayer.Clues += 2
        if(check == "Fail"):
            self.Environment.Devour(self.Environment.CurrentPlayer)
        self.Environment.ReturnMonster(self)
            

    def DefaultBeforeHorror(self):
        return "Pass"

    
                
