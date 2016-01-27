class AncientOne :
    def __init__(self, AODict):
        self.Name = AODict["Name"]
        self.Environment = ""
        if "Title" in AODict :
            self.Title = AODict["Title"]
        else :
            self.Title = ""               
        self.Picture = AODict["Picture"]
        
        self.SelectionPicture = self.Picture
        
        self.Abilities = {'PhysicalResistance': 0,
                          'PhysicalImmunity': 0,
                          'MagicalResistance': 0,
                          'MagicalImmunity': 0}
        self.SkillCheckNumber = 1
        
        if "Combat" in AODict:
            self.CombatRating = AODict["Combat"]
        else:
            self.CombatRating = 0
        if "Defense" in AODict:
            self.Defenses = AODict["Defense"]
        else:
            self.Defenses = None
        
        if "Attack" in AODict:
            self.Attack = AODict["Attack"]
        else:
            self.Attack = "i = 1"
        self.CurrentDoom = 0
        if "Doom" in AODict:
            self.MaxDoom = int(AODict["Doom"])
        else:
            self.MaxDoom = 0
        if "Worshippers" in AODict:
            self.Worshippers = AODict["Worshippers"]
        else:
            self.Worhshippers = "i = 1"
        if "Awaken" in AODict:
            self.Awaken = AODict["Awaken"]
        else:
            self.Awaken = "i = 1"
        if "Power" in AODict:
            self.Power = AODict["Power"]

        if (self.Defenses == "PhysicalResistance"):
            self.Abilities["PhysicalResistance"] = 1
                                
        if (self.Defenses == "PhysicalImmunity"):
            self.Abilities["PhysicalImmunity"] = 1
                                
        if (self.Defenses == "MagicalResistance"):
            self.Abilities["MagicalResistance"] = 1
                                
        if (self.Defenses == "MagicalImmunity"):
            self.Abilities["MagicalImmunity"] = 1

    def AttackFunction(self):
        exec(self.Attack)
    def AwakenFunction(self):
        exec(self.Awaken)
    def IncrementDoomTrack(self):
        self.CurrentDoom += 1
    def DecrementDoomTrack(self):
        self.CurrentDoom -= 1
    def UsePower(self):
        exec(self.Power)

#Ancient One Attacks
    def AzathothAttack(self):
        self.Environment.PrintEvent("Azathoth Attack","Azathoth Attacks!")
        #Shouldn't ever occur.
        
    def CthulhuAttack(self):
        self.Environment.PrintEvent("Cthulhu Attack","Cthulhu Attacks!")

        #Every attack Cthulu heals one, unless he is max health.
        if (self.CurrentDoom < self.MaxDoom):
            self.CurrentDoom = self.CurrentDoom + 1

        #Cthulhu drains one max stam or sanity no matter what.
        for player in self.Environment.Investigators:
            PlayerChoice = self.Environment.ListChoose("Lose One", "Lose Either One Max Sanity or One Max Stamina", ["Sanity","Stamina"])

            if (PlayerChoice == "Sanity"):
                player.Stats["MaxSanity"] = player.Stats["MaxSanity"] - 1
                player.ModSanity(0)
                #ModSanity is to make sure it bring sanity down to max if its higher

            elif (PlayerChoice == "Stamina"):
                player.Stats["MaxStam"] = player.Stats["MaxStam"] - 1
                player.ModHealth(0)
                #ModSHealth is to make sure it bring health down to max if its higher
                
    def HasturAttack(self):
        self.Environment.PrintEvent("Hastur Attack","Hastur Attacks!")
                
        for player in self.Environment.Investigators:
            SkillCheckResult = player.Environment.SkillCheck("Luck", player, 1, self.SkillCheckNumber)

            if SkillCheckResult == "Fail":
                player.ModSanity(-2)
                Comment = "Hastur hits " + player.Name + " for two Sanity Damage!"
                self.Environment.PrintEvent("Hastur Attacks", Comment)

        self.SkillCheckNumber =  self.SkillCheckNumber - 1

        
    def IthaquaAttack(self):
        self.Environment.PrintEvent("Ithaqua Attack","Ithaqua Attacks!")
         
        for player in self.Environment.Investigators:
            SkillCheckResult = player.Environment.SkillCheck("Fight", player, 1, self.SkillCheckNumber)

            if SkillCheckResult == "Fail":
                player.ModHealth(-2)
                Comment = "Ithaqua hits " + player.Name + " for two Stamina Damage!"
                self.Environment.PrintEvent("Ithaqua Attack", Comment)

        self.SkillCheckNumber =  self.SkillCheckNumber - 1
        
    def NyarlathotepAttack(self):
        self.Environment.PrintEvent("Nyarlathotep Attack","Nyarlathotep Attacks!")
        
        for player in self.Environment.Investigators:
            SkillCheckResult = player.Environment.SkillCheck("Lore", player, 1, self.SkillCheckNumber)
            
            if (SkillCheckResult == "Fail"):
                player.Clues = player.Clues - 1
                Comment = "Nyarlathotep hits " + player.Name + " and takes a Clue Token!"
                self.Environment.PrintEvent("Nyarlathotep Attack", Comment)

        #Devour them if they are out of clues
        templist = list()
        for player in self.Environment.Investigators:
            if (player.Clues == 0):
                templist.append(player)

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)
            
        self.SkillCheckNumber =  self.SkillCheckNumber - 1
        
    def ShubNiggurathAttack(self):
        self.Environment.PrintEvent("Shub-Niggurath Attack","Shub-Niggurath Attacks!")

        for player in self.Environment.Investigators:
            SkillCheckResult = player.Environment.SkillCheck("Sneak", player, 1, self.SkillCheckNumber)
            
            if (SkillCheckResult == "Fail"):
                player.MonsterTrophies.pop()
                Comment = "Shub-Niggurath hits " + player.Name + " and takes a Monster Trophy!"
                self.Environment.PrintEvent("Shub-Niggurath Attack", Comment)

        #Devour them if they are out of monster trophies
        templist = list()

        for player in self.Environment.Investigators:
            if len(player.MonsterTrophies) == 0:
                templist.append(player)

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)
            
        self.SkillCheckNumber =  self.SkillCheckNumber - 1
        
    def YigAttack(self):
        self.Environment.PrintEvent("Yig Attack","Yig Attacks!")
                
        for player in self.Environment.Investigators:
            SkillCheckResult = player.Environment.SkillCheck("Speed", player, 1, self.SkillCheckNumber)

            if SkillCheckResult == "Fail":
                player.ModHealth(-1)
                player.ModSanity(-1)
                Comment = "Yug hits " + player.Name + " and damages both Sanity and Stamina for 1 damage!"
                self.Environment.PrintEvent("Yig Attack", Comment)

        self.SkillCheckNumber =  self.SkillCheckNumber - 1
        
    def YogSothothAttack(self):
        self.Environment.PrintEvent("Yog-Sothoth Attack","Yog-Sothoth Attacks!")

        for player in self.Environment.Investigators:
            SkillCheckResult = player.Environment.SkillCheck("Will", player, 1, self.SkillCheckNumber)
            
            if (SkillCheckResult == "Fail"):
                player.GateTrophies.pop()
                Comment = "Yog-Sothoth hits " + player.Name + " and takes a Gate Trophy!"
                self.Environment.PrintEvent("Yog-Sothoth Attack", Comment)

        #Devour them if they are out of gate trophies
        templist = list()

        for player in self.Environment.Investigators:
            if len(player.GateTrophies) == 0:
                templist.append(player)

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)
            
        self.SkillCheckNumber =  self.SkillCheckNumber - 1

#Ancient One Awakens
    def AzathothAwaken(self):
        while (len(self.Environment.Investigators) > 0):
            self.Environment.Devour(self.Environment.Investigators[0])
            
    def CthulhuAwaken(self):
        print "Cthulhu has awakened"
        
    def HasturAwaken(self):
        self.CombatRating = self.Environment.TerrorLevel
        
    def IthaquaAwaken(self):
        self.Environment.PrintEvent("Ithaqua Item Roll","Ithaqua awakens and forces each player to make a die roll for each of his items or lose that item.")
        templist = list()
        for player in self.Environment.Investigators:
            
            for item in player.ItemList:
                
                Blessed = player.Status["Blessed"]
                Cursed = player.Status["Cursed"]

                DieResult = self.Environment.RollDie()
                
                if (DieResult <= (5  - Blessed + Cursed)):
                    templist.append(item)
                #Else don't kill the item
            while templist != []:
                temp = templist.pop()
                player.Discard(temp)
        
    def NyarlathotepAwaken(self):
        templist = list()
        for player in self.Environment.Investigators:
            if (player.Clues == 0):
                templist.append(player)

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)
        
    def ShubNiggurathAwaken(self):
        templist = list()
        for player in self.Environment.Investigators:
            if len(player.MonsterTrophies) == 0:
                templist.append(player)

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)
        
    def YigAwaken(self):
        templist = list()
        for player in self.Environment.Investigators:
            if (player.Status["Cursed"] == 1):
                templist.append(player)
            else:
                player.Status["Cursed"] = 1

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)
        

        
    def YogSothothAwaken(self):       
        templist = list()
        for player in self.Environment.Investigators:
            if len(player.GateTrophies) == 0:
                templist.append(player)

        while templist != []:
            temp = templist.pop()
            self.Environment.Devour(temp)
        


        
#Ancient One Powers
    def AzathothPower(self):
        print "OMG ITS A POWER"
        
    def CthulhuPower(self):
        print "OMG ITS A POWER"
        
    def HasturPower(self):
        print "OMG ITS A POWER"
        
    def IthaquaPower(self):
        print "OMG ITS A POWER"
        
    def NyarlathotepPower(self):
        print "OMG ITS A POWER"
        
    def ShubNiggurathPower(self):
        print "OMG ITS A POWER"
        
    def YigPower(self):
        print "OMG ITS A POWER"
        
    def YogSothothPower(self):
        print "OMG ITS A POWER"

#Ancient One Worshippers
    def AzathothWorshippers(self):
        print "Maniacs get 1 toughness"
        
    def CthulhuWorshippers(self):
        print "cultists get a bonus"
        
    def HasturWorshippers(self):
        print "worshippers get some combat rating flying things"
        
    def IthaquaWorshippers(self):
        print "cultists get tougher"
        
    def NyarlathotepWorshippers(self):
        print "cultists get endless"
        
    def ShubNiggurathWorshippers(self):
        print "worshippers get a bigger toughness"
        
    def YigWorshippers(self):
        print "increase worshipper stam dmg"
        
    def YogSothothWorshippers(self):        
        print "worshippers get magical immunity"
        
