"""
Miguel, 05/03/2010: Implemented all card functions for cards in the Common Items deck.

Miguel, 05/04/2010: Implemented first 5 card functions for cards in the Ally deck.
"""


#####################################
#READ ME
"""
If a card says discard after use.  don't do DiscardCard(card) in the use part.
Have it call card[4](card, "Discard)


Cards that make a player lose health or sanity:
player.ModHealth(Value)  where value is 1, 2, ,3 for gain.   -1 ,-2 for loss
player.ModSanity(Value)  value is positive for gain, neg for loss

Reducing stamina or sanity loss:
Absorb one time only:
player.ActiveAbsorb["Stamina"] += 1
player.ActiveAbsorb["Stamina"] += 1

Absorb every time:
player.PassiveAbsorb["Stamina"] += 1
player.PassiveAbsorb["Stamina"] += 1

Choosing a Player:
ChosenPlayer = Player.Envrionment.PickPlayer()

Choosing a monster:
Is usually the monster the player is fighting

Items that cannot be lost or stolen unless you choose:
Before discarding, ask them by using the following function
ConfirmDiscard(Nameofthingwewanttodiscard)        returns Pass or Fail


ITEMS with hands should work similar to deputy's revolver (without the discard check)

Checking to see if an item is equipped:
IsEquipped(card)

If an item gets bonuses or does something on equip, reversing its bonuses should
be done on unequip instead of discard

Equipping one handed:
Most likely the bonuses are given on equip instead of draw

Equipping two handed:         Unequip both hands

card[iLoc][iOwner].UnequipItems()
card[iLoc][iOwner].LeftHandItem = card

Exhausting items
To exhaust use:  Exhaust(card)
To check to see if an item is exhausted IsExhaust(card)


"""
#####################################

import XmlLoader
import os
import ChooseDialog

iLoc = 5
iName = 0
iOwner = 2

def StartDecks(Env):
    #setup decks
    Env.AddDeck("Common")
    Env.AddDeck("Spell")
    Env.AddDeck("Skill")
    Env.AddDeck("Unique")
    Env.AddDeck("Ally")
    Env.AddDeck("Special")
    
    LookUpTable = []
    LookUpTable.append({'name':"Find Gate", 'number':4, 'function':FindGate, 'deck':"Spell", 
                        'description':"Returns caster to Arkham from Other World"})
    LookUpTable.append({'name':"Deputy of Arkham", 'number':1, 'function':DeputyOfArkham, 'deck':"Special",
                        'description':"Player is a Deputy of Arkham"})
    LookUpTable.append({'name':"No Items", 'number':16, 'function':NoItem, 'deck':"Special",
                        'description':"Not an Item"})
    LookUpTable.append({'name':"Deputy's Revolver", 'number':1, 'function':DeputysRevolver, 'deck':"Special",
                        'description':"One handed weapon"})
    LookUpTable.append({'name':"Patrol Wagon", 'number':1, 'function':PatrolWagon, 'deck':"Special",
                        'description':"Transportation anywhere in Arkham"})
    LookUpTable.append({'name':"Red Sign Of Shudde M'ell", 'number':2, 'function':RedSignOfShuddeMell, 'deck':"Spell",
                        'description':"A spell to weaken an enemy"})
    LookUpTable.append({'name':"Enchant Weapon", 'number':3, 'function':EnchantWeapon, 'deck':"Spell",
                        'description':"A spell to magically enchant a weapon"})
    LookUpTable.append({'name':"Mists of Releh", 'number':4, 'function':MistsOfReleh, 'deck':"Spell",
                        'description':"A spell to hide the caster for a time"})
    LookUpTable.append({'name':"Heal", 'number':3, 'function':Heal, 'deck':"Spell",
                        'description':"A spell to heal a players stamina"})
    LookUpTable.append({'name':"Silver Twilight Lodge Membership", 'number':8, 'function':SilverTwilightLodgeMembership, 'deck':"Special",
                        'description':"Provides membership to the Silver Twilight Lodge"})
    LookUpTable.append({'name':"Bank Loan", 'number':8, 'function':BankLoan, 'deck':"Special",
                        'description':"A Loan from the Bank"})
    LookUpTable.append({'name':"Retainer", 'number':8, 'function':Retainer, 'deck':"Special",
                        'description':"A Retainer"})
    LookUpTable.append({'name':"Blessing", 'number':8, 'function':Blessing, 'deck':"Special",
                        'description':"A blessing has come upon you!"})
    LookUpTable.append({'name':"Curse", 'number':8, 'function':Curse, 'deck':"Special",
                        'description':"A curse has befallen you!"})


    LookUpTable.append({'name':"18 Derringer", 'number':2, 'function': Derringer18, 'deck':"Common",
                        'description':".18 Derringer"})
    LookUpTable.append({'name':"38 Revolver", 'number':2, 'function': Revolver38, 'deck':"Common",
                        'description':"An .38 Revolvel"})
    LookUpTable.append({'name':"45 Automatic", 'number':2, 'function': Automatic45, 'deck':"Common",
                        'description':"An .45 Automatic"})
    LookUpTable.append({'name':"Ancient Tome", 'number':2, 'function': AncientTome, 'deck':"Common",
                        'description':"Ancient Tome"})
    LookUpTable.append({'name':"Axe", 'number':2, 'function': Axe, 'deck':"Common",
                        'description':"An axe"})
    LookUpTable.append({'name':"Bullwhip", 'number':2, 'function':Bullwhip, 'deck':"Common",
                        'description':"Bull whip"})
    LookUpTable.append({'name':"Cavalry Saber", 'number':2, 'function': CavalrySaber, 'deck':"Common",
                        'description':"Cavalry Saber"})
    LookUpTable.append({'name':"Cross", 'number':2, 'function': Cross, 'deck':"Common",
                        'description':"A Cross"})
    LookUpTable.append({'name':"Dark Cloak", 'number':2, 'function': DarkCloak, 'deck':"Common",
                        'description':"A Dark Cloak"})
    LookUpTable.append({'name':"Dynamite", 'number':2, 'function': Dynamite, 'deck':"Common",
                        'description':"Dynamite"})
    LookUpTable.append({'name':"Food", 'number':2, 'function': Food, 'deck':"Common",
                        'description':"Just some food"})
    LookUpTable.append({'name':"Knife", 'number':2, 'function': Knife, 'deck':"Common",
                        'description':"A Knife"})
    LookUpTable.append({'name':"Lantern", 'number':2, 'function': Lantern, 'deck':"Common",
                        'description':"A Lantern"})
    LookUpTable.append({'name':"Lucky Cigarette Case", 'number':2, 'function': LuckyCigaretteCase, 'deck':"Common",
                        'description':"A Lucky Cigarette Case"})
    LookUpTable.append({'name':"Map of Arkham", 'number':2, 'function': MapOfArkham, 'deck':"Common",
                        'description':"The map of Arkham"})
    LookUpTable.append({'name':"Motorcycle", 'number':2, 'function': Motorcycle, 'deck':"Common",
                        'description':"A Motorcycle"})
    LookUpTable.append({'name':"Old Journal", 'number':2, 'function': OldJournal, 'deck':"Common",
                        'description':"An Old Journal"})
    LookUpTable.append({'name':"Research Materials", 'number':2, 'function': ResearchMaterials, 'deck':"Common",
                        'description':"Research Materials"})
    LookUpTable.append({'name':"Rifle", 'number':2, 'function': Rifle, 'deck':"Common",
                        'description':"A Rifle"})
    LookUpTable.append({'name':"Shotgun", 'number':2, 'function': Shotgun, 'deck':"Common",
                        'description':"A Shotgun"})
    LookUpTable.append({'name':"Tommy Gun", 'number':2, 'function': TommyGun, 'deck':"Common",
                        'description':"Tommy Gun"})
    LookUpTable.append({'name':"Whiskey", 'number':2, 'function': Whiskey, 'deck':"Common",
                        'description':"A bottle of Whiskey"})
    
    
   


    
    LookUpTable.append({'name':"Elder Sign", 'number':4, 'function':ElderSign, 'deck':"Unique",
                        'description':"A mistical sign"})
    LookUpTable.append({'name':"Holy Water", 'number':4, 'function':HolyWater, 'deck':"Unique",
                        'description':"Water blessed by God"})
    LookUpTable.append({'name':"The King In Yellow", 'number':2, 'function':TheKingInYellow, 'deck':"Unique",
                        'description':"A book of old"})
    LookUpTable.append({'name':"Marksman", 'number':2, 'function':Marksman, 'deck':"Skill",
                        'description':"A good skill for combat"})
    LookUpTable.append({'name':"Lore", 'number':2, 'function':Lore, 'deck':"Skill",
                        'description':"You sure know a lot"})



    #
    #Allies
    #
    LookUpTable.append({'name':"Sir William Brinton", 'number':1, 'function':SirWilliamBrinton, 'deck':"Ally",
                        'description':"Discard to immediately restore your Stamina to its maximum"})
    LookUpTable.append({'name':"Eric Colt", 'number':1, 'function':EricColt, 'deck':"Ally",
                        'description':"You take no Sanity loss from the Nightmarish ability"})
    LookUpTable.append({'name':'Tom "Mountain" Murphy', 'number':1, 'function':TomMountainMurphy, 'deck':"Ally",
                        'description':"You take no Stamina loss from the Overwhelming ability"})
    LookUpTable.append({'name':"Professor Armitage", 'number':1, 'function':ProfessorArmitage, 'deck':"Ally",
                        'description':"Your attacks are not affected by Magical Resistance"})
    LookUpTable.append({'name':"Richard Upton Pickman", 'number':1, 'function':RichardUptonPickman, 'deck':"Ally",
                        'description':"Your attacks are not affected by Physical Resistance"})
    LookUpTable.append({'name':"John Legrasse", 'number':1, 'function':JohnLegrasse, 'deck':"Ally",
                        'description':"You can claim monsters with the Endless ability as trophies"})
    LookUpTable.append({'name':"Basil Elton", 'number':1, 'function':BasilElton, 'deck':"Ally",
                        'description':"Discard to cancel the Ancient One's entire attack for one turn"})
    LookUpTable.append({'name':"Ruby Standish", 'number':1, 'function':RubyStandish, 'deck':"Ally",
                        'description':"Draw 1 Unique item when Ruby Standish joins you"})
    LookUpTable.append({'name':"Anna Kaslow", 'number':1, 'function':AnnaKaslow, 'deck':"Ally",
                        'description':"Gain 2 Clue tokens when Anna Kaslow joins you"})
    LookUpTable.append({'name':"Thomas F. Malone", 'number':1, 'function':ThomasFMalone, 'deck':"Ally",
                        'description':"Draw 1 Spell when Thomas F. Malone joins you"})
    LookUpTable.append({'name':"Ryan Dean", 'number':1, 'function':RyanDean, 'deck':"Ally",
                        'description':"Draw 1 Common item when Ryan Dean joins you"})
    

    


    while (len(LookUpTable) != 0):
        #Loader = XmlLoader.XmlLoader()
        nextc = LookUpTable.pop(0)
        
        path = os.getcwd()
        length = len(os.getcwd())
        path = path[0:(length - 7)]
        xmlPaths = []
        if(nextc['deck'] == "Skill"):
            if(path[len(path)-1] == "\\"):
                path = path + "data\\Skills\\Images\\"
            if(path[len(path)-1] == "/"):
                path = path + "data/Skills/Images/"
        if(nextc['deck'] == "Spell"):
            if(path[len(path)-1] == "\\"):
                path = path + "data\\Spells\\Images\\"
            if(path[len(path)-1] == "/"):
                path = path + "data/Spells/Images/"
        if(nextc['deck'] == "Common" or nextc['deck'] == "Unique" or nextc['deck'] == "Special"):
            if(path[len(path)-1] == "\\"):
                path = path + "data\\Item\\Images\\"
            if(path[len(path)-1] == "/"):
                path = path + "data/Item/Images/"
        picf = path + nextc['name'] + ".jpg"
        if nextc['name'] == "No Items":
            picf = path + "NoItem.jpg"
        #DecLoc = Env.Decks[nextc['deck']]
        counter = nextc['number']
        while (counter > 0):
            Env.DeckDictionary[nextc['deck']].AddCard([nextc['name'], 
                                                     nextc['description'], 
                                                     picf,
                                                     " ",
                                                     nextc['function'],
                                                     "location",
                                                     0])
            counter = counter - 1





#######################
### Special ###########
#######################

def NoItem(card, usage):
    return

def SilverTwilightLodgeMembership(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        card[iLoc][iOwner].Status['SilverLodgeMember'] = 1
        return
    if (usage == "use"):
        card[iLoc][iOwner].Status['SilverLodgeMember'] = 0
                    
def BankLoan(card, usage):
    if (usage == "discard"):
        if (card[iLoc][iOwner].Money >= 10):
            DiscardCard(card)
            card[iLoc][iOwner].Money -= 10
            card[iLoc][iOwner].Status['BankLoan'] = 0
            return
        card[iLoc][iOwner].Environment.PrintEvent("Pay Up", "You do not have the money to pay off your loan")
        return
    if (usage == "draw"):
        card[iLoc][iOwner].Status['BankLoan'] = 1
        card[iLoc][iOwner].Money += 10
# 8
# gain $10
# every upkeep, roll 1 dice, on 1-3 pay $1 or discard all items and this card
# any phase, pay $10 and discard this card
# if card not paid back, no further loans allowed(including current loan card)

def Retainer(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        card[iLoc][iOwner].Status['Retainer'] -= 0
        return
    if (usage == "draw"):
        card[iLoc][iOwner].Status['Retainer'] += 1
# 8
# upkeep phase, gain $2 then roll 1 dice, on a 1, discard retainer

def Blessing(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        card[iLoc][iOwner].Status['Blessed'] = 0
        return
    if (usage == "draw"):
        temp = card[iLoc][iOwner].Status['Cursed']
        if temp == 1:
            temp = 0
        elif temp == 0:
            card[iLoc][iOwner].Status['Blessed'] = 1
# 8
# successes are 4, 5, and 6 for all rolls, if cursed discard this card,
# every upkeep, roll 1 dice, on a 1, discard this card

def Curse(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        card[iLoc][iOwner].Status['Cursed'] = 0
        return
    if (usage == "draw"):
        temp = card[iLoc][iOwner].Status['Blessed']
        if temp == 1:
            temp = 0
        elif temp == 0:
            card[iLoc][iOwner].Status['Cursed'] = 1
# 8
# successes are only 6 for all rolls, if blessed discard this card,
# every upkeep, roll 1 dice, on a 6, discard this card

def DeputyOfArkham(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].MoneyPerUpkeep -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].MoneyPerUpkeep += 1
        AddToPlayer(card[iLoc][iOwner], "Special", "Deputy's Revolver")
        AddToPlayer(card[iLoc][iOwner], "Special", "Patrol Wagon")
        

def AddToPlayer(Player, Dec, Item):
    Drawn = Player.Environment.DeckDictionary[Dec].DrawCard(Player, Item)
    Player.AddItem(Drawn)


def DeputysRevolver(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        if (ConfirmDiscard(card[iName]) == "false"):
            return
        else:
            if(IsEquipped(card)):
                card[4](card, "unequip")
                DiscardCard(card)
            else:
                DiscardCard(card)
        return
    if(usage == "use"):
        pass
    if(usage == "equip"):
        player.CheckBonus["Combat"] += 3
    if(usage == "unequip"):
        player.CheckBonus["Combat"] -= 3

#FIX ME
def PatrolWagon(card, usage):
    Player = card[iLoc][iOwner]
    if(usage == "discard"):
        DiscardCard(card)
        return
    if(usage == "use"):
        if(Player.Environment.CurrentPhase == "Movement"):
            Player.CurrentMovementPoints = 10
            #Needs to check for discard at end of combat and end of gate suck
        
####################
### Spells   #######
####################

def FindGate(card, usage):
    Player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if (CastSpell(-1, 1, Player) == True):
            DestinationList = []
            for Gate in Player.Environment.Gates :
                if str(Gate.Destination+"2") == Player.Location.Name and Gate.Location != None :
                        DestinationList.append(Gate.Location.Name)
                if DestinationList == [] :
                    #No portals open to your zone, you are lost in time and space
                    Player.Environment.PrintEvent("No where to go!","There are no active gates connecting to your dimension.")
                    
                else :
                    Target = Player.Environment.ListChoose( "Choose a destination.", "You can exit this dimension to any location with a gate open to it.",DestinationList )
                    Target = Player.Environment.Locations[Target]
                    Player.Environment.Teleport(Player,Target) 
                    Target.Gate.ExploredBy(Player)

def Teleport(Player, Destination):
    Player.Environment.Teleport(Player, Destination)
    
#CHECK ME
def RedSignOfShuddeMell(card, usage):
    player = card[iLoc][iOwner]
    if(usage == "discard"):
        DiscardCard(card)
        return
    if(usage == "use"):
        if (IsExhaust(card) == False):
            Exhaust(card)
            if (CastSpell(-1, 1, card[iLoc][iOwner]) == True):



                monster = player.FightingMonster

                if(monster.Toughness > 1):
                    monster.Toughness -= 1

                List = ["PhysicalResistance","PhysicalImmunity","MagicalResistance"
                        ,"Ambush","Endless","Mask","Nightmarish",
                        "Overwhelming","Undead"]
                
                answer = player.Environment.ListChoose("Red Sign of Shudde M'ell","Choose an attribute to ignore",List)
                if(player.CancelAbilities[answer] == 0):
                    player.CancelAbilities[answer] = -1
                    player.ExecEOCStack.append("self.CancelAbilities['"+ answer +
                                               "'] += 1; stack.remove(element)")

            

#OH GOD NO. PLEASE NO
def EnchantWeapon(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if (CastSpell(0, 1, card[iLoc][iOwner]) == True):
            Choice = PickWeapon(card[iLoc][iOwner])
            ChangeModifier(Choice, "Damage", 0, "magical")
        
# 3
# 0 casting modifier, 1 sanity cost
# any phase, exhaust and make physical weapon magical till end of next combat


def MistsOfReleh(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if(IsExhaust(card) == False):
            #It shouldn't pick a monster. It should be the monster he is currently fighting
            Choice = card[iLoc][iOwner].FightingMonster

            if type(Choice) != type(None):
                Exhaust(card)
                if (CastSpell(Choice.Awareness, 0, card[iLoc][iOwner]) > 0):
                    card[iLoc][iOwner].AutoPass['Evade'] = 1
                    card[iLoc][iOwner].ExecEOCStack.append("self.AutoPass['Evade'] = 0; stack.remove(element)")
                
        pass
   



def Heal(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if(IsExhaust(card) == False):
            Exhaust(card)
            Total = CastSpell(1, 1, player)
            if (Total > 0):
                Text = []
                Answer = player
                Players = player.Location.PlayerList
                for playa in Players:
                    Text.append(playa.Name)
                Choice = player.Environment.ListChoose("Heal","Choose a target to heal",Text)
                for invest in player.Location.PlayerList:
                    if invest.Name == Choice:
                        Answer = invest
                Answer.ModHealth(Total)
            


def VoiceOfRa(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 3
# -1 casting modifier, 1 sanity cost
# Upkeep phase only, exhaust to gain +1 to all skill checks this turn

def FleshWard(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 4
# -2 casting modifier, 1 sanity cost
# any phase, exhaust to ignore all stamina loss being delt to you form one source
# discard if ancient one awakens

def Wither(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 6
# 0 casting modifier, 0 sanity cost
# any phase, exhaust to gain +3 to combat checks till end of next combat, 1 hand

def Shrivelling(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 5
# -1 casting modifier, 1 sanity cost
# any phase, exhaust and gain +6 to combat checks till end of next combat, 1 hand

def DreadCurseOfAzathoth(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 4
# -2 casting modifier, 2 sanity cost
# any phase, exhaust and gain +9 to combat checks till end of next combat, 2 hands

def BindMonster(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 2
# +4 casting modifier, 2 sanity cost
# discard and pass 1 combat check, must have successes equal to monsters toughness,
# doesn't work on ancient ones, 2 hands



#####################
### Allies ##########
#####################

def EricColt(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Speed"] -= 2
        card[iLoc][iOwner].CancelAbilities["Nightmarish"] += 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Speed"] += 2
        card[iLoc][iOwner].CancelAbilities["Nightmarish"] -= 1
        return
# 1
# +2 speed, no sanity loss from nightmarish ability



def TomMountainMurphy(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Fight"] -= 2
        card[iLoc][iOwner].CancelAbilities["Overwhelming"] += 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Fight"] += 2
        card[iLoc][iOwner].CancelAbilities["Overwhelming"] -= 1
        return
# 1
# +2 fight, no stamina loss from overwhelming ability


def ProfessorArmitage(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Lore"] -= 2
        card[iLoc][iOwner].CancelAbilities["MagicalResistance"] += 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Lore"] += 2 
        card[iLoc][iOwner].CancelAbilities["MagicalResistance"] -= 1
        return
# 1
# +2 lore, not affected by magical resistance


def RichardUptonPickman(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Luck"] -= 1
        card[iLoc][iOwner].BonusStats["Speed"] -= 1
        card[iLoc][iOwner].CancelAbilities["MagicalResistance"] += 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Luck"] += 1
        card[iLoc][iOwner].BonusStats["Speed"] += 1
        card[iLoc][iOwner].CancelAbilities["MagicalResistance"] -= 1
        return
# 1
# +1 luck, +1 speed, not affected by magical resistance


def JohnLegrasse(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Will"] -= 2
        card[iLoc][iOwner].CancelAbilities["Endless"] += 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Will"] += 2
        card[iLoc][iOwner].CancelAbilities["Endless"] -= 1
        return

# 1
# +2 will, can claim mosters with endless ability as trophies


def BasilElton(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Will"] += 1
        card[iLoc][iOwner].BonusStats["Fight"] += 1
        #sacrifice to cancel an ancient ones attack for one turn
        DiscardCard(card)
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Will"] += 1
        card[iLoc][iOwner].BonusStats["Fight"] += 1

    if (usage == "use"):
        #Cancel ancient ones attack
        card[4](card, "discard")
    return
# 1
# +1 fight, +1 will, sacrifice to cancel an ancient ones attack for one turn


def SirWilliamBrinton(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        player.Stats["MaxStam"] -= 1
        player.ModHealth(1000)
        DiscardCard(card)        
        return
    if (usage == "draw"):
        player.Stats["MaxStam"] += 1
    return
# 1
# +1 maximum stamina, discard to restore stamina to full


def RubyStandish(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        player.Stats["Sneak"] -= 2
        DiscardCard(card)        
        return
    if (usage == "draw"):
        player.Stats["Sneak"] += 2
        AddToPlayer(player, "Unique", "none")
        return
# 1
# +2 sneak, draw 1 unique item when this card is gained

def AnnaKaslow(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        player.Stats["Luck"] -= 2
        DiscardCard(card)
        return
    if (usage == "draw"):
        player.Stats["Luck"] += 2
        player.Clues += 2
        return
# 1
# +2 luck, gain 2 clue tokens when this card is gained

def ThomasFMalone(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):        
        player.Stats["Lore"] -= 1
        player.Stats["Fight"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        player.Stats["Lore"] += 1
        player.Stats["Fight"] += 1
        AddToPlayer(player, "Spell", "none")
        return
# 1
# +1 lore, +1 fight, draw 1 spell when this card is gained

def RyanDean(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):        
        player.Stats["Will"] -= 1
        player.Stats["Sneak"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        player.Stats["Will"] += 1
        player.Stats["Sneak"] += 1
        AddToPlayer(player, "Common", "none")
        return
# 1
# +1 will, +1 sneak, draw 1 common item when this card is gained

#######################
### Skills  ###########
#######################

def Lore(card, usage):
    if (usage == "discard"):
        
        card[iLoc][iOwner].BonusStats["Lore"] -= 1
        card[iLoc][iOwner].CluetoDie["Lore"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):        
        card[iLoc][iOwner].BonusStats["Lore"] += 1
        card[iLoc][iOwner].CluetoDie["Lore"] += 1
        
# 2
# +1 lore, roll 2 dice for ever 1 clue token spent on lore check

def Sneak(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Sneak"] -= 1
        card[iLoc][iOwner].CluetoDie["Sneak"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Sneak"] += 1
        card[iLoc][iOwner].CluetoDie["Sneak"] += 1
# 2
# +1 sneak, roll 2 dice for ever 1 clue token spent on sneak check

def Will(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Will"] -= 1
        card[iLoc][iOwner].CluetoDie["Will"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Will"] += 1
        card[iLoc][iOwner].CluetoDie["Will"] += 1
# 2
# +1 will, roll 2 dice for ever 1 clue token spent on will check

def Fight(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Fight"] -= 1
        card[iLoc][iOwner].CluetoDie["Fight"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Fight"] += 1
        card[iLoc][iOwner].CluetoDie["Fight"] += 1
# 2
# +1 fight, roll 2 dice for ever 1 clue token spent on fight check

def Luck(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Luck"] -= 1
        card[iLoc][iOwner].CluetoDie["Luck"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Luck"] += 1
        card[iLoc][iOwner].CluetoDie["Luck"] += 1
# 2
# +1 luck, roll 2 dice for ever 1 clue token spent on luck check

def Speed(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].BonusStats["Speed"] -= 1
        card[iLoc][iOwner].CluetoDie["Speed"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].BonusStats["Speed"] += 1
        card[iLoc][iOwner].CluetoDie["Speed"] += 1
# 2
# +1 speed, roll 2 dice for ever 1 clue token spent on speed check

def Marksman(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    if (usage == "draw"):
        card[iLoc][iOwner].Reroll["Combat"].append(card)
    if (usage == "use"):
        Exhaust(card)
    if (usage == "refresh"):
        card[iLoc][iOwner].Reroll["Combat"].append(card)
# 2
# exhaust to reroll a combat check

def ExpertOccultist(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    if (usage == "draw"):
        card[iLoc][iOwner].Reroll["Spell"].append(card)
    if (usage == "use"):
        Exhaust(card)
    if (usage == "refresh"):
        card[iLoc][iOwner].Reroll["Spell"].append(card)
        
# 2
# exhaust to reroll a spell check

def Stealth(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    if (usage == "draw"):
        card[iLoc][iOwner].Reroll["Evade"].append(card)
    if (usage == "use"):
        Exhaust(card)
    if (usage == "refresh"):
        card[iLoc][iOwner].Reroll["Evade"].append(card)

# 2
# exhaust to reroll an evade check

def Bravery(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    if (usage == "draw"):
        card[iLoc][iOwner].Reroll["Horror"].append(card)
    if (usage == "use"):
        Exhaust(card)
    if (usage == "refresh"):
        card[iLoc][iOwner].Reroll["Horror"].append(card)
# 2
# exhaust to reroll a horror check

######################
### Common ###########
######################
def Derringer18(card, usage):
    if (usage == "discard"):
        if (ConfirmDiscard(card[iName]) == "false"):
            return
        else:
            if(IsEquipped(card)):
                card[4](card, "unequip")
                DiscardCard(card)
            else:
                DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 2
        return
    if (usage == "equip"):
        card[iLoc][iOwner].BonusStats["Physical"] += 2
        return
    if (usage == "price"):
        return 3
# 2
# +2 combat, 1 hand, $3, can't be lost or stolen

def Revolver38(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] += 3
        return
    
    if (usage == "equip"):
        card[iLoc][iOwner].BonusStats["Physical"] += 3
        return
    if (usage == "price"):
        return 4
# 2
# +3 combat, 1 hand, $4

def Automatic45(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 4
        return
    if (usage == "equip"):
        card[iLoc][iOwner].BonusStats["Physical"] += 4
        return
    if (usage == "price"):
        return 5
# 2
# +4 combat, 1 hand, $5

def AncientTome(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "price"):
        return 4
    if (usage == "use"):
        if (IsExhaust(card) == False and player.CurrentMovementPoints > 2):
            player.CurrentMovementPoints -= 2
            Exhaust(card)
            if(player.Environment.SkillCheck("Lore", player, 1, -1)):
                AddToPlayer(player, "Spell", "none")

        player.Environment.PrintEvent("Failed",
                                      "You do not meet the requirements to use this card")
        
            
        return
# 2
# $4, exhaust +2 movement, lore -1 check, draw a spell and discard this card

#NOt done
def Axe(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if(usage == "price"):
        return 3
    if (usage == "equip"):
        card[iLoc][iOwner].BonusStats["Physical"] += 2
        #if your other hand has something already you only get a +2 Combat check
        #if((card[iLoc][iOwner].LeftHandItem == []) or (card[iLoc][iOwner].RightHandItem == [])): 
        #    card[iLoc][iOwner].BonusStats["Fight"] += 2
        #    return
        #if both of your hands are empty you get a +3 Combat check
        #if((card[iLoc][iOwner].LeftHandItem == []) and (card[iLoc][iOwner].RightHandItem == [])): 
        #    card[iLoc][iOwner].BonusStats["Fight"] += 3
        #    return

    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 2
# 2
# 1 handed, $3, +2 combat or +3 if 2 handed

#Special is not coded yet
def Bullwhip(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 1
        return
    if (usage == "equip"):
        card[iLoc][iOwner].BonusStats["Physical"] += 1
        return
    if(usage == "price"):
        return 2
            
# 2
# +1 combat, 1 hand, $2

def CavalrySaber(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 2
        return
    if (usage == "equip"):
        card[iLoc][iOwner].BonusStats["Physical"] += 2
        return
    if(usage == "price"):
        return 3
# 2
# +2 combat, 1 hand, $3

def Cross(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].CheckBonus["Horror"] -= 1
        player.ExecSOCStack.remove("if(self.FightingMonster.Abilities['Undead']): self.BonusStats['Magical'] += 3")
        player.ExecEOCStack.remove("if(self.FightingMonster.Abilities['Undead']): self.BonusStats['Magical'] -= 3")
        return
    if (usage == "equip"):
        card[iLoc][iOwner].CheckBonus["Horror"] += 1
        player.ExecSOCStack.append("if(self.FightingMonster.Abilities['Undead']): self.BonusStats['Magical'] += 3")
        player.ExecEOCStack.append("if(self.FightingMonster.Abilities['Undead']): self.BonusStats['Magical'] -= 3")
    if (usage == "price"):
        return 3
        
        #Put on SOC and EOC stacks, if fightingmonster is undead
        #add 3 to combat
        return
# 2
# magical, 1 hand +3 combat vs undead, +1 horror checks, $3

def DarkCloak(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].CheckBonus["Evade"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].CheckBonus["Evade"] += 1
        return
    if (usage == "price"):
        return 2
# 2
# +1 evade check, $2

def Dynamite(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        card[iLoc][iOwner].ExecEOCStack.append("self.BonusStats['Physical'] -= 8; stack.remove(element)")
        DiscardCard(card)
        return
    if (usage == "equip"):
        #Two handed
        card[iLoc][iOwner].UnequipItems()
        card[iLoc][iOwner].LeftHandItem = card
        return

    #this card needs to be discarded after used
    if (usage == "use"):
        if(IsEquipped(card)):
            card[iLoc][iOwner].BonusStats["Physical"] += 8
            card[4](card, "discard")
            return
        return
    if (usage == "price"):
        return 4
# 2
# +8 combat, 2 hands, $4, discard after use

def Food(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        return
    
    if (usage == "use"):
        #ABSORB
        card[iLoc][iOwner].ActiveAbsorb["Stamina"](1)
        card[4](card, "discard")
        return

    if (usage == "price"):
        return 1
    
# 2
# discard and reduce stam loss by 1

def Knife(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 1
        return
    if (usage == "equip"):
        card[iLoc][iOwner].BonusStats["Physical"] += 1
        return
    if (usage == "price"):
        return 2
# 2
# +1 combat, one hand, $2

def Lantern(card, usage):
    if (usage == "discard"):
        card[iLoc][iOwner].CheckBonus["Luck"] -= 1
        DiscardCard(card)
        return
    if (usage == "draw"):
        card[iLoc][iOwner].CheckBonus["Luck"] += 1
        return
    if (usage == "price"):
        return 3
# 2
# +1 to luck check, $3

def LuckyCigaretteCase(card, usage):
    if (usage == "draw"):
        card[iLoc][iOwner].Reroll["Any"].append(card)
        return
    if (usage == "use"):
        card[4](card, "discard")
        return
    if (usage == "discard"):
        card[iLoc][iOwner].Reroll["Any"].remove(card)
        DiscardCard(card)
    if (usage == "price"):
        return 1

# 2
# discard and reroll any 1 skill check

def MapOfArkham(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if(IsExhaust(card) == False):
            card[iLoc][iOwner].CurrentMovementPoints += 1
            Exhaust(card)
        return
    if (usage == "price"):
        return 2
# 2
# exhaust and get 1 movement, $2

def Motorcycle(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if(IsExhaust(card) == False):
            card[iLoc][iOwner].CurrentMovementPoints += 2
            Exhaust(card)
        return
    if (usage == "price"):
        return 4
# 2     
# exhaust and get 2 extra movement, $4

def OldJournal(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "price"):
        return 1
    if (usage == "use"):
        if (IsExhaust(card) == False and player.CurrentMovementPoints > 1):
            Exhaust(card)
            player.CurrentMovementPoints -= 1
            if(player.Environment.SkillCheck("Lore", player, 1, -1)):
                player.Clues += 3
                card[4](card, "discard")

        player.Environment.PrintEvent("Failed",
                                      "You do not meet the requirements to use this card")
        
            
        return
# 2
# $1, exhaust +1 movement, lore -1 check, gain 3 clue tokens and discard this card

def ResearchMaterials(card, usage):
    if(usage == "discard"):
        DiscardCard(card)
    if(usage == "price"):
        return 1
    return
# 2                    
# discard instead of a clue token, $1 

def Rifle(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 5
        return
    if (usage == "equip"):
        #Two handed
        card[iLoc][iOwner].UnequipItems()
        card[iLoc][iOwner].LeftHandItem = card
        
        card[iLoc][iOwner].BonusStats["Physical"] += 5
        return
    if (usage == "price"):
        return 6
# 2
# +5 combat, 2 hands, $6


#Bonus is not done
def Shotgun(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 4
        return
    if (usage == "equip"):
        #Two handed
        card[iLoc][iOwner].UnequipItems()
        card[iLoc][iOwner].LeftHandItem = card
        
        card[iLoc][iOwner].BonusStats["Physical"] += 4
        return
    if (usage == "price"):
        return 6
# 2
# +4 combat, 2 hands, $6, 6s count as 2 successes

def TommyGun(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "unequip"):
        card[iLoc][iOwner].BonusStats["Physical"] -= 6
        return
    if (usage == "equip"):
        #Two handed
        card[iLoc][iOwner].UnequipItems()
        card[iLoc][iOwner].LeftHandItem = card
        
        card[iLoc][iOwner].BonusStats["Physical"] += 6
        return
    if (usage == "price"):
        return 7
# 2
# +6 combat, 2 hands, $7

def Whiskey(card, usage):
    if (usage == "discard"):
        #ABSORB
        card[iLoc][iOwner].ActiveAbsorb["Sanity"] += 1
        DiscardCard(card)
        return
    if (usage == "use"):
        card[4](card, "discard")
    if (usage == "price"):
        return 1
# 2
# discard to reduce sanity loss by 1, $1





                   

######################
### Unique  ##########
######################

def PallidMask(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        player.CheckBonus["Evade"] -= 2
        DiscardCard(card)
        return
    if (usage == "use"):
        player.CheckBonus["Evade"] += 2
    if (usage == "price"):
        return 4
# 1
# +2 to evade checks, $4

def WardingStatue(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        player.ModHealth(+player.FightingMonster.StaminaDamage)
        card[4](card, "discard")
# 1
# discard to reduce combat damage to 0 or cancel an ancient one's turn, $6

def FluteOfTheOuterGods(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        player.ModHealth(-3)
        player.ModSanity(-3)        
        for monster in player.Location.MonsterList:
            player.DefeatMonster(monster)
        card[4](card, "discard")
    if (usage == "price"):
        return 8
        
# 1
# lose 3 stam and sanity and defeat all monsters in your area, $8

def EnchantedJewelry(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        player.ActiveAbsorb["Stamina"] = 3
        card[4](card, "discard")
    if (usage == "price"):
        return 3
            
# 1
# absorbs up to 3 stamina, discard after third one, $3

def BlueWatcherOfThePyramid(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 1
# lose 2 stam and discard card to auto pass a fight, combat, or lore check, $4

def ObsidianStatue(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 1
# discard to cancel stam or san loss being dealt to you from one source, $4

def SilverKey(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    return
# 1
# automaticlly pass up to 3 evade checks, $4

def AlienStatue(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if(player.Environment.CurrentPhase == "Movement" and
           IsExhaust(card) == False):
            if(player.CurrentMovementPoints >= 2):
                Exhaust(card)
                player.CurrentMovementPoints -= 2
                player.ModSanity(-1)
                if player.Status["Cursed"] > 0 :
                    ReqSuccess = 6
                elif player.Status["Blessed"] > 0 :
                    ReqSuccess = 4
                else :
                    ReqSuccess = 5
                result = Player.Environment.RollDie()
                if (result >= ReqSuccess):
                    temp = player.Environment.Choose("AlienStatue", "Choose gain 1 spell or 3 clue tokens!", "Spell", "Clue tokens", "AlienStatue can only be used in movement phase!")
                    if (temp == "Spell"):
                        player.AddItem(player.Environment.DeckDictionary["Spell"].DrawCard(player, "none"))
                    if (temp == "Clue tokens"):
                        player.Clues += 3
                else:
                    player.ModStamina(-2)
        else:
            player.Environment.PrintEvent("Phase", "It is not your movement phase!")
    if (usage == "price"):
        return 5
        
# 1
# durring movement, exhaust and spend 2 movement and 1 san, roll die, if success gain 1 spell
# or 3 clue tokens, if fail lose 2 stam, $5

#Dunwich horror??!?
def HealingStone(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if(player.Environment.CurrentPhase == "Final"):
            card[4](card, "discard")
            return
        if(player.Environment.CurrentPhase == "Upkeep"):
            temp = player.Environment.Choose("HealingStone", "Choose plus stamina or plus sanity!", "Stam", "Sanity", "HealingStone can only be used in upkeep phase!")
            if (temp == "Stam"):
                player.ModHealth(1)
            if (temp == "Sanity"):
                player.ModSanity(1)
            Exhaust(card)
            return
        player.Environment.PrintEvent("Error", "It is not upkeep phase, you cannot use healingstone!")
    if (usage == "price"):
        return 8
# 1
# upkeep, exhaust to gain 1 stam or san, discard when ancient one awakens, $8

def AncientTablet(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if(player.Environment.CurrentPhase == "Movement" and
           player.CurrentMovementPoints >= 3):
            player.CurrentMovementPoints -= 3
            if player.Status["Cursed"] > 0 :
                ReqSuccess = 6
            elif player.Status["Blessed"] > 0 :
                ReqSuccess = 4
            else :
                ReqSuccess = 5
            for i in range(2):
                result = Player.Environment.RollDie()
                if (result >= ReqSuccess):
                    player.AddItem(player.Environment.DeckDictionary["Spell"].DrawCard(player, "none"))
                else:
                    player.Clues += 2
            DiscardCard(card)
        else:
            player.Environment.PrintEvent("Phase", "It is not your movement phase!")
    if (usage == "price"):
        return 8

# 1
# movement phase, spend 3 movement and discard, roll 2 dice, gain 1 spell for each success and
# 2 clue tokens for each failure, $8

def RubyOfRlyeh(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        player.BonusStats["Movement"] -= 3
        DiscardCard(card)
        return
    if (usage == "draw"):
        if(player.Environment.CurrentPhase == "Movement"):
            player.BonusStats["Movement"] += 3
    if (usage == "price"):
        return 8
# 1
# movement phase, gain 3 movement points, $8

def Necronomicon(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        DiscardCard(card)
        return
    if (usage == "use"):
        if(player.Environment.CurrentPhase == "Movement" and
           IsExhaust(card) == False):
            if (player.CurrentMovementPoints - 2 >= 0):
                player.CurrentMovementPoints -= 2
                temp = player.Environment.SkillCheck("Lore", player, 1, -2)
                if (temp == "Pass"):
                    player.AddItem(player.Environment.DeckDictionary["Spell"].DrawCard(player, "none"))
                    player.ModSanity(-2)
                Exhaust(card)
            else:
                player.Environment.PrintEvent("Movement", "You do not have enough movement points; you need 2 at least")
        else:
            player.Environment.PrintEvent("Phase", "It is not your movement phase!")
    if (usage == "price"):
        return 6
# 1
# movement phase, exhaust and spend 2 movement, lore(-2) check, pass draw 1 spell and lose 2 sanity, $6

def BookOfDzyan(card, usage):
    return
# 1
# movement phase, exhaust and spend 2 movement, lore(-1) check, pass draw 1 spell and lose 1 sanity,
# usable twice, $3

def PowderOfIbnGhazi(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        player.ExecEOCStack.append("self.BonusStats['Magical'] -= 9; stack.remove(element)")
        DiscardCard(card)
        return
    if (usage == "equip"):
        #Two handed
        player.UnequipItems()
        player.LeftHandItem = card
        return
    if (usage == "price"):
        return 6

    #this card needs to be discarded after used
    if (usage == "use"):
        if(IsEquipped(card)):
            player.BonusStats["Magical"] += 9
            player.ModSanity(-1)
            card[4](card, "discard")
        return
# 2
# +9 to combat, magical, 2 hands, lose 1 sanity, discard after use

def HolyWater(card, usage):
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        card[iLoc][iOwner].ExecEOCStack.append("self.BonusStats['Magical'] -= 6; stack.remove(element)")
        DiscardCard(card)
        return
    if (usage == "equip"):
        #Two handed
        card[iLoc][iOwner].UnequipItems()
        card[iLoc][iOwner].LeftHandItem = card
        return

    #this card needs to be discarded after used
    if (usage == "use"):
        if(IsEquipped(card)):
            card[iLoc][iOwner].BonusStats["Magical"] += 6
            card[4](card, "discard")
            return
        return
    if (usage == "price"):
        return 4
    # 4
    # +6 combat check, 2 hands, discard after use

def ElderSign(card, usage):
    if (usage == "discard"):
        DiscardCard(card)
    # 4
    # lose 1 san and 1 stam, discard card, seals gate, removes 1 doom token from doom track

def CabalaOfSaboth(card, usage):
    player = card[iLoc][iOwner]
    if(usage == "use"):
        if(IsExhaust(card) == False):
            if(player.Environment.CurrentPhase == "Movement" and
                player.CurrentMovementPoints >= 2):
                Exhaust(card)
                player.CurrentMovementPoints -= 2
                temp = player.Environment.SkillCheck("Lore", player, 1, -2)
                if (temp == "Pass"):
                    player.AddItem(player.Environment.DeckDictionary["Skill"].DrawCard(player, "none"))
                    card[4](card, "discard")
            else:
                player.Environment.PrintEvent("Phase", "It is not your movement phase!")
    if (usage == "discard"):
        DiscardCard(card)
    if (usage == "price"):
        return 5
# 2
# movement phase, exhaust and spend 2 movement, lore(-2) check, pass and draw a skill and discard

def NamelessCult(card, usage):
    player = card[iLoc][iOwner]
    if(usage == "price"):
        return 3
    if(usage == "discard"):
        DiscardCard(card)
    if(usage == "use"):
        if(IsExhaust(card) == False):
            if(player.Environment.CurrentPhase == "Movement" and
               player.CurrentMovementPoints >= 1):
                Exhaust(card)
                player.CurrentMovementPoints -= 1
                temp = player.Environment.SkillCheck("Lore", player, 1, -1)
                if (temp == "Pass"):
                    player.AddItem(player.Environment.DeckDictionary["Spell"].DrawCard(player, "none"))
                    player.ModSanity(-1)
                    card[4](card, "discard")
            else:
                player.Environment.PrintEvent("Phase", "It is not your movement phase!")
    # 2
    # movement phase, exhaust and spend 1 movement, lore(-1) check, pass and draw a spell, lose a sanity, and discard

def CultesDesGoules(card, usage):
    player = card[iLoc][iOwner]
    if(usage == "price"):
        return 3
    if(usage == "discard"):
        DiscardCard(card)
    if(usage == "use"):
        if(player.Environment.CurrentPhase == "Movement" and
           IsExhaust(card) == False and
           player.CurrentMovementPoints >= 2):
            Exhaust(card)
            player.CurrentMovementPoints -= 2
            temp = player.Environment.SkillCheck("Lore", player, 1, -2)
            if (temp == "Pass"):
                player.AddItem(player.Environment.DeckDictionary["Spell"].DrawCard(player, "none"))
                player.Clues += 1
                player.ModSanity(-2)
                card[4](card, "discard")
        else:
            player.Environment.PrintEvent("Phase", "You do not meet the conditions to use this card")
    # 2
    # movement, exhaust and spend 2 movement, lore(-2) check, pass and draw spell and clue token, lose 2 sanity
    # and discard

def EnchantedKnife(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "equip"):
        player.BonusStats["Magical"] += 3
        return
    if (usage == "unequip"):
        player.BonusStats["Magical"] -= 3
        return
    if (usage == "price"):
        return 5
    # 2
    # +3 combat, 1 hand, magical

def EnchantedBlade(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "equip"):
        player.BonusStats["Magical"] += 4
        return
    if (usage == "unequip"):
        player.BonusStats["Magical"] -= 4
        return
    if (usage == "price"):
        return 6
    # 2
    # +4 combat, 1 hand, magical

def TheKingInYellow(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "price"):
        return 2
    if (usage == "discard"):
        DiscardCard(card)
    if(usage == "use"):
        if(player.Environment.CurrentPhase == "Movement"):
            if(player.CurrentMovementPoints >= 2 and IsExhaust(card) == False):
                Exhaust(card)
                player.CurrentMovementPoints -= 2
                temp = player.Environment.SkillCheck("Lore", player, 1, -2)
                if (temp == "Pass"):
                    player.Clues += 4
                    player.ModSanity(-1)
                    card[4](card, "discard")
        else:
            player.Environment.PrintEvent("Phase", "It is not your movement phase!")
    # 2
    # movement phase, exhaust and spend 2 movement, lore(-2) check, pass and gain 4 clue tokens, lose 1 sanity, and discard

def SwordOfGlory(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "equip"):
        card[iLoc][iOwner].UnequipItems()
        card[iLoc][iOwner].LeftHandItem = card
        player.BonusStats["Magical"] += 6
        return
    if (usage == "unequip"):
        player.BonusStats["Magical"] -= 6
        return
    if (usage == "price"):
        return 8
    # 1
    # +6 to combat, 2 handed, magical

def DragonsEye(card, usage):
    return
    # 1
    # exhaust, lose 1 sanity, draw new gate or location card

def GateBox(card, usage):
    return
    # 1
    # can return to any arkham location from other world that has an open gate, not just the one leading to the other world
    # you were in

def LampOfAlhazred(card, usage):
    player = card[iLoc][iOwner]
    if (usage == "discard"):
        if(IsEquipped(card)):
            card[4](card, "unequip")
        DiscardCard(card)
        return
    if (usage == "equip"):
        card[iLoc][iOwner].UnequipItems()
        card[iLoc][iOwner].LeftHandItem = card
        player.BonusStats["Magical"] += 5
        return
    if (usage == "unequip"):
        player.BonusStats["Magical"] -= 5
        return
    if (usage == "price"):
        return 7
    # 1
    # +5 combat, 2 handed, magical
    

#######################################
####
#### Dougs Defs
#######################################

def CastSpell(fourth, third, second):
    second.ModSanity(third)
    check = second.Environment.SuccessCheck("Spell",second,1,fourth)
    return check

def DiscardCard(card):
    if(type(card[iLoc][iOwner] != "str")):
        if(card[iLoc][iOwner].Type == "Player"):
            """
            counter = 0
            DiscardCounter = 0
            for cc in card[iLoc][iOwner].ItemList:
                if cc == card:
                    DiscardCounter = counter
                counter += 1
            if card[iLoc][iOwner].ItemList != []:
                card[iLoc][iOwner].ItemList.pop(DiscardCounter)

            Why did someone put this overly complicated code in?
            To stop the game from blowing up when it trys to discard a
            card that's not in the card owners ItemList.
            That if statement is a far better solution.
            """
            if card in card[iLoc][iOwner].ItemList:
                card[iLoc][iOwner].ItemList.remove(card)
    card[iLoc][iOwner] = "Discard"


def Exhaust(card):
    card[iLoc][iOwner].Environment.ExhaustedCardList.append(card)

def IsExhaust(card):
    ExhaustList = card[iLoc][iOwner].Environment.ExhaustedCardList
    if(ExhaustList.count(card) > 0):
        return True
    else:
        return False
    
def NoItemCard(card, usage):
    return

def ConfirmDiscard(Name):
    ans = ChooseDialog.Run("Discard?", "Are you sure you want to discard " + Name + "?",
                     "Yes", "No", "Clicking yes means you want to discard it")
    if (ans == "Yes"):
        return "Pass"
    if (ans == "No"):
        return "Fail"
    return "No"

def IsEquipped(card):
    print card[iLoc][iOwner]
    if(card[iLoc][iOwner].LeftHandItem == card or card[iLoc][iOwner].RightHandItem == card):
        return True
    else:
        return False
    
