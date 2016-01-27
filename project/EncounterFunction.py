"""
Encounter Functions: By Zack

These functions will be called from within encounter turn by their appropriate encounters


ALL FUNCTIONS WILL BE PASSED:

def functionname( Environment , Player )


"""
import random

#Built in Encounters

#
#+1 sanity for free or all sanity for $2
#

def ArkhamAsylum(Environment,Player):
    Choice = Environment.Choose("Arkham Asylum","Would you like to gain +1 sanity for free or pay $2 for full sanity recovery","Free","$2","Your current sanity: "+str(Player.Stats["Sanity"])+" / "+str(Player.Stats["MaxSanity"]+Player.BonusStats["MaxSanity"]))
    if Choice == "Free":
        Player.ModSanity(1)
    elif Choice =="$2":
        if Player.Money >= 2:
            Player.Money -= 2
            Player.ModSanity(100)

#
#Pay $8 to draw 2 skills, keep one discard other
#

def Administration(Environment,Player):
    Environment.PrintEvent( "Classes","Instead of having an encounter here, you may pay $8 to draw 2 Skills. Keep one of them and discard the other.")
    if Player.Money < 8:
        return
    if Environment.Choose("Skills","Would you like to pay $8 for a skill?","Yes","No"," ") == "Yes":
        Player.Money -= 8
        templist = list()
        templist.append( Environment.DeckDictionary["Skill"].DrawCard(Player,"none"))               
        templist.append( Environment.DeckDictionary["Skill"].DrawCard(Player,"none"))
        result = Environment.ItemChoose( "Choose an item ", templist )
        for item in templist :
            if item[0] == result[0] :
                Player.AddItem( item )
            else:
                Environment.DeckDictionary["Skill"].DiscardCard(item)

#   
#Take out a bank loan
#

def BankArkham(Environment,Player):
    Environment.PrintEvent( "Bank Loan","Instead of having an encounter here, you may take out a Bank Loan if you don't have one yet.")
    if Environment.Choose("Bank Loan","Would you like to take out a bank loan?","Yes","No"," ") == "Yes" and Player.Status["Bank Loan"] == 0:
        Player.AddItem( Environment.DeckDictionary["Special"].DrawCard(Player,"Bank Loan"))
        return


#Draw 3 unique, buy 1 for full price
#

def CuriositieShoppe(Environment,Player):
    Environment.PrintEvent( "Shop"," Instead of having an encounter here, you may draw 3 Unique Items and purchase one of them for its list price. Discard the other two items.")
    if Environment.Choose("Unique Items","Would you like to shop for a Unique item?","Yes","No"," ") == "Yes":
        templist = list()
        templist.append( Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
        templist.append( Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
        templist.append( Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
        result = Environment.ItemChoose( "Choose an item ", templist )
        for item in templist :
            if item[0] == result[0] and Environment.Choose("Confirm","Buy this item?","Yes","No", " ") == "Yes":
                price = item[4](item,"price")
                if Player.Money >= price : #need a way to know cost 
                    Player.AddItem( item )
                    Player.Money -= price
            else:
                Environment.DeckDictionary["Unique"].DiscardCard(item)
#
#draw 3 common, buy 1 for full price
#
def GeneralStore(Environment,Player):
    Environment.PrintEvent( "Shop"," Instead of having an encounter here, you may draw 3 Common Items and purchase one of them for its list price. Discard the other two items.")
    if Environment.Choose("Common Items","Would you like to shop for a common item?","Yes","No"," ") == "Yes":
        templist = list()
        templist.append( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
        templist.append( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
        templist.append( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
        result = Environment.ItemChoose( "Choose an item ", templist )
        for item in templist :
            if item[0] == result[0] and Environment.Choose("Confirm","Buy this item?","Yes","No", " ") == "Yes":
                price = item[4](item,"price")
                if Player.Money >= price : #need a way to know cost 
                    Player.AddItem( item )
                    Player.Money -= price
            else:
                Environment.DeckDictionary["Common"].DiscardCard(item)
#
#spend 10 monster toughness or 2 gates or 5 toughness of monster and 1 gate to 
#draw an ally
def BoardingHouse(Environment,Player):
    Environment.PrintEvent( "Recruit","Instead of having an encounter here, you may spend 10 toughness worth of monster trophies, 2 gate trophies, or 5 toughness worth of monster trophies and 1 gate trophy to take 1 Ally of your choice from the Ally deck.")
    if Environment.Choose("Ally","Would you like to spend trophies to draw an ally?","Yes","No"," ") == "No":
        return
    toughnesscounter = 0
    VisualList = []
    DiscardList = []
    for montrophy in Player.MonsterTrophies :
        VisualList.append( " ("+str(montrophy.Toughness)+") "+montrophy.Name)
    for gatetrophy in Player.GateTrophies :
        VisualList.append( "(5)"+gatetrophy.Name)
    while toughnesscounter < 10:
        result = Environment.ListChoose("Choose a Trophy", "Choose a trophy to spend." , VisualList)
        if VisualList == []:
            return
        VisualList.remove(result)
        if result.Name == "Gate":
            toughnesscounter += 5
            DiscardList.append(result)
        else:
            toughnesscounter += result.Toughness
            DiscardList.append(result)
    Player.AddItem( Environment.DeckDictionary["Ally"].DrawCard(Player, "none"))
    while DiscardList != []:
        temp = DiscardList.pop()
        if temp.Name == "Gate":
            Player.GateTrophies.remove(temp)
            Environment.ReturnGate(temp)
        else:
            Player.MonsterTrophies.remove(temp)
            Environment.ReturnMonster(temp)            
                            
                         
        
#
#spend 10 monster toughness or 2 gates or 5 toughness of monster and 1 gate to 
#be deputy of arkham
def PoliceStation(Environment,Player):
    Environment.PrintEvent( "Deputized","Instead of having an encounter here, you may spend 10 toughness worth of monster trophies, 2 gate trophies, or 5 toughness worth of monster trophies and 1 gate trophy to become the Deputy of Arkham. Take the Deputy of Arkham card.")
    if Environment.Choose("Deputized","Would you like to spend trophies to become a Deputy?","Yes","No"," ") == "No":
        return
    toughnesscounter = 0
    VisualList = []
    DiscardList = []
    for montrophy in Player.MonsterTrophies :
        VisualList.append( " ("+str(montrophy.Toughness)+") "+montrophy.Name)
    for gatetrophy in Player.GateTrophies :
        VisualList.append( "(5)"+gatetrophy.Name)
    while toughnesscounter < 10 :
        result = Environment.ListChoose("Choose a Trophy", "Choose a trophy to spend." , VisualList)
        if VisualList == []:
            return
        VisualList.remove(result)
        if result.Name == "Gate":
            toughnesscounter += 5
            DiscardList.append(result)
        else:
            toughnesscounter += result.Toughness
            DiscardList.append(result)
    Player.AddItem( Environment.DeckDictionary["Special"].DrawCard(Player, "Deputy of Arkham"))
    while DiscardList != []:
        temp = DiscardList.pop()
        if temp.Name == "Gate":
            Player.GateTrophies.remove(temp)
            Environment.ReturnGate(temp)
        else:
            Player.MonsterTrophies.remove(temp)
            Environment.ReturnMonster(temp) 

#
#spend 5 toughness trophies or 1 gate to gain $5
#
def RiverDocks(Environment,Player):
    Environment.PrintEvent( "Shady Character","Instead of having an encounter here, you may spend 5 toughness worth of monster trophies or 1 gate trophy to gain $5.")
    if Environment.Choose("Shady Character","Would you like to spend trophies for $5?","Yes","No"," ") == "No":
        return
    toughnesscounter = 0
    VisualList = []
    DiscardList = []
    for montrophy in Player.MonsterTrophies :
        VisualList.append( " ("+str(montrophy.Toughness)+") "+montrophy.Name)
    for gatetrophy in Player.GateTrophies :
        VisualList.append( "(5)"+gatetrophy.Name)
    while toughnesscounter < 5 :
        result = Environment.ListChoose("Choose a Trophy", "Choose a trophy to spend." , VisualList)
        if VisualList == []:
            return
        VisualList.remove(result)
        if result.Name == "Gate":
            toughnesscounter += 5
            DiscardList.append(result)
        else:
            toughnesscounter += result.Toughness
            DiscardList.append(result)
    Player.Money += 5
    while DiscardList != []:
        temp = DiscardList.pop()
        if temp.Name == "Gate":
            Player.GateTrophies.remove(temp)
            Environment.ReturnGate(temp)
        else:
            Player.MonsterTrophies.remove(temp)
            Environment.ReturnMonster(temp) 

#
#spend 5 toughness trophies or 1 gate to gain 2 clues
#
def ScienceBuilding(Environment,Player):
    Environment.PrintEvent( "Dissection","Instead of having an encounter here, you may spend 5 toughness worth of monster trophies or 1 gate trophy to gain 2 Clue tokens.")
    if Environment.Choose("Dissection","Would you like to dissect a trophy?","Yes","No"," ") == "No":
        return
    toughnesscounter = 0
    VisualList = []
    DiscardList = []
    for montrophy in Player.MonsterTrophies :
        VisualList.append( " ("+str(montrophy.Toughness)+") "+montrophy.Name)
    for gatetrophy in Player.GateTrophies :
        VisualList.append( "(5)"+gatetrophy.Name)
    while toughnesscounter < 5 :
        if VisualList == []:
            return
        result = Environment.ListChoose("Choose a Trophy", "Choose a trophy to spend." , VisualList)
        VisualList.remove(result)
        if result.Name == "Gate":
            toughnesscounter += 5
            DiscardList.append(result)
        else:
            toughnesscounter += result.Toughness
            DiscardList.append(result)
    Player.Clues += 2
    while DiscardList != []:
        temp = DiscardList.pop()
        if temp.Name == "Gate":
            Player.GateTrophies.remove(temp)
            Environment.ReturnGate(temp)
        else:
            Player.MonsterTrophies.remove(temp)
            Environment.ReturnMonster(temp) 
#
#spend 5 toughness trophies or 1 gate to bless any investigator
#
def SouthChurch(Environment,Player):
    Environment.PrintEvent( "Blessing ","Instead of having an encounter here, you may spend 5 toughness worth of monster trophies or 1 gate trophy to have any investigator you choose be Blessed.")
    if Environment.Choose("Blessing","Would you like to spend trophies to bless an investigator?","Yes","No"," ") == "No":
        return
    toughnesscounter = 0
    VisualList = []
    DiscardList = []
    for montrophy in Player.MonsterTrophies :
        VisualList.append( " ("+str(montrophy.Toughness)+") "+montrophy.Name)
    for gatetrophy in Player.GateTrophies :
        VisualList.append( "(5)"+gatetrophy.Name)
    while toughnesscounter < 5:
        result = Environment.ListChoose("Choose a Trophy", "Choose a trophy to spend." , VisualList)
        if VisualList == []:
            return
        VisualList.remove(result)
        if result.Name == "Gate":
            toughnesscounter += 5
            DiscardList.append(result)
        else:
            toughnesscounter += result.Toughness
            DiscardList.append(result)
    templist = list()
    for inv in Environment.Investigators :
        templist.append( inv.Name )
    result = Environment.ListChoose("Blessing","Choose an Investigator to bless",templist)
    for inv in Environment.Investigators :
        if result == inv.Name:
            inv.Bless()
    while DiscardList != []:
        temp = DiscardList.pop()
        if temp.Name == "Gate":
            Player.GateTrophies.remove(temp)
            Environment.ReturnGate(temp)
        else:
            Player.MonsterTrophies.remove(temp)
            Environment.ReturnMonster(temp) 


#
#+1 stam or pay $2 for all stam recovered
#
def Hospital(Environment,Player):
    Choice = Environment.Choose("St Marys Hospital","Would you like to gain +1 Stamina for free or pay $2 for full Stamina recovery","Free","$2","Your current Stamina: "+str(Player.Stats["Stamina"])+" / "+str(Player.Stats["MaxStam"]+Player.BonusStats["MaxStam"]))
    if Choice == "Free":
        if Player.Stats["Stamina"] < Player.Stats["MaxStam"]+Player.BonusStats["MaxStam"] :
            Player.ModHealth(1)
    elif Choice =="$2":
        if Player.Money >= 2:
            Player.Money -= 2
            Player.ModHealth(100)
#pay $5 to draw 2 spells, discard one
#
def MagickShoppe(Environment,Player):
    Environment.PrintEvent( "Magic Lessons"," Instead of having an encounter here, you may pay $5 to draw 2 Spells. Keep one of them and discard the other.")
    if Player.Money < 5:
        return
    if Environment.Choose("Spells","Would you like to shop for a spell?","Yes","No"," ") == "Yes":
        Player.Money -= 5
        templist = list()
        templist.append( Environment.DeckDictionary["Spell"].DrawCard(Player,"none"))
        templist.append( Environment.DeckDictionary["Spell"].DrawCard(Player,"none"))
        result = Environment.ItemChoose( "Choose an item ", templist )
        for item in templist :
            if item == result and Environment.Choose("Confirm","Buy this item?","Yes","No", " ") == "Yes":
                Player.AddItem( item )
            else:
                Environment.DeckDictionary["Spell"].DiscardCard(item)

#Map Board Events
LocationEncounterDict = {'Arkham Asylum' : "ArkhamAsylum",
                        'Bank Of Arkham': "BankArkham",
                        'Administration': "Administration",
                        'Curiositie Shoppe':"CuriositieShoppe",
                        'General Store':"GeneralStore",
                        'Mas Boarding House':"BoardingHouse",
                        'Police Station':"PoliceStation",
                        'River Docks':"RiverDocks",
                        'Science Building':"ScienceBuilding",
                        'South Church':"SouthChurch",
                        'St Marys Hospital':"Hospital",
                        'Ye Olde Magick Shoppe':"MagickShoppe"}

# concat EncountDict+ random 1 to MaxEncounterSize to get function
EncounterDict = {'Arkham Asylum' : "Asylum",
                'Bank Of Arkham': "BankOfArkham",
                'Independence Square':"IndependenceSquare",
                'Administration': "Administration",
                'Curiositie Shoppe':"CuriositieShoppe",
                'General Store':"GeneralStore",
                'Mas Boarding House':"BoardingHouse",
                'Police Station':"PoliceStation",
                'Velmas Diner': "VelmasDiner",
                'Hibbs Roadhouse':"HibbsRoadhouse",
                'The Witch House': "WitchHouse",
                'Silver Twilight Lodge': "SilverTwilightLodge",
                'River Docks':"RiverDocks",
                'Unvisited Isle':"Unvisited",
                'The Unnameable':"Unnameable",
                'Science Building':"ScienceBuilding",
                'South Church':"SouthChurch",
                'St Marys Hospital':"Hospital",
                'Ye Olde Magick Shoppe':"MagickShoppe",
                'Black Cave': "BlackCave",
                'Historical Society': "HistoricalSociety",
                'Graveyard': "Graveyard",
                'Train Station':"TrainStation",
                'Newspaper': "Newspaper",
                'Woods': "Woods",
                'Library':"Library"}

################################################################
#Downtown Section


#Make lore(+0) check
#0 success: Lose 1 sanity and gain 1 clue
#1-2: Gain 2 clue
#3+: Gain 3 clue
def Asylum1(Environment,Player):
    Environment.PrintEvent( "title","In the Doctors study, you find a book of helpful notes gathered from inmate interviews. Make a Lore (+0) check and consult the following chart:\n Successes:\n 0) Their stories fill you with horror even as you learn a few bits of knowledge. Lose 1 Sanity and gain 1 Clue token.\n 1-2) You find several pieces of useful information. Gain 2 Clue tokens.\n 3+) One of the interviews contains vital information. Gain 3 Clue tokens.")
    success = Environment.SuccessCheck("Lore",Player, 0, 0)
    if success == 0:
        Environment.PrintEvent("Encounter","You lose 1 Sanity and gain 1 Clue")
        Player.ModSanity(-1)
        Player.Clues += 1
        if Player.Stats["Sanity"] == 0:
            Environment.Insane(Player)
    elif success <= 2:
        Player.Clues += 2
        Environment.PrintEvent("Encounter","You gain 2 Clues")
    elif success <= 2:
        Player.Clues += 3
        Environment.PrintEvent("Encounter","You gain 3 Clues")        
        

#find something, choose to use
#if yes do Lore(-1) check
#pass: draw spell
def Asylum2(Environment,Player):
    Environment.PrintEvent( "title","You find some strange medicine labeled Dream Enhancers in a dusty cabinet. If you choose to take it, make a Lore (-1) check. if you pass, your visions show you how to perform a ritual. Draw 1 Spell. Otherwise, nothing happens." )   
    if Environment.Choose("Encounter","Take the strange medicine?","Yes","No"," ") == "Yes":
        result = Environment.SkillCheck("Lore",Player,1,-1)
        if result == "Pass":
            Environment.PrintEvent("Encounter","Success! Draw a spell.")
            Player.AddItem( Environment.DeckDictionary["Spell"].DrawCard(Player,"none"))

#Forced Will(-1) [2] check
#pass: draw 1 skill
#fail: choose to discard ( 4clues or 2 spells or 1 skill)
def Asylum3(Environment,Player):
    Environment.PrintEvent( "title","You are mistaken for an inmate. Doctor Mintz has the guards subdue you and conducts an experimental. Make a Will (-1) [2] check to discover the results. If you pass, the injections seem to increase your capacity for learning. Draw 1 Skill. If you fail, his memory drug fails miserably, resulting in lost knowledge. You must discard one of the following (your choice), if able: 4 Clue tokens, or 2 Spells, or 1 Skill." )   
    result = Environment.SkillCheck("Will",Player,2,-1)
    if result == "Pass":
        Player.AddItem( Environment.DeckDictionary["Skill"].DrawCard(Player,"none"))
    elif result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You must discard 4 clues or 2 spells or 1 skill.")#need to add detection of # of skills
        choice = Environment.ListChoose("Choose Discard", "Choose what you wish to discard", [ "4 Clues","2 Spells", "1 Skill"])
        if choice == "4 Clues":
            print "discard 4 clues"
        elif choice == "2 Spells":
            print "discard 2 spells"
        elif choice == "1 Skill":
            print "discard 1 skill"


#Lore(-2) 
#pass: 2 clues
#fail: -1 stam
def Asylum4(Environment,Player):
    Environment.PrintEvent( "title","You hear screaming. When you open a heavy cell door to investigate, a dark shape leaps out at you! It's an insane man in a straightjacket babbling about invisible horrors. Make a Lore (-2) check to glean some useful information from him. If you pass, gain 2 Clue tokens. If you fail, lose 1 Stamina as he attacks you.")
    result = Environment.SkillCheck("Lore",Player,1,-2)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have gained 2 clues.")
        Player.Clues += 2
    elif result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You lose 1 sanity.")
        Player.ModSanity(-1)

#forced Speed(-1) 
#pass: draw 1 unique
#fail: move to street
def Asylum5(Environment,Player):
    Environment.PrintEvent( "title","Nurse Heather is coming! Make a Speed (-1) check to hide in time. If you pass you see her drop something as she walks by. Draw 1 Unique Item. If you fail, she throws you out. Move to the street."    )
    result = Environment.SkillCheck("Speed",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! Draw 1 unique card.")
        Player.AddItem( Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
    elif result == "Fail":
        Environment.PrintEvent("Encounter","Failure! You have been forced to the streets.")
        Environment.Teleport(Player, Player.Location.Connections[0])

#optional fight(-2) 
#pass: 
#fail: delay, +2 sanity
def Asylum6(Environment,Player):
    Environment.PrintEvent( "title","Nurse Heather accidentally injects you with a sleeping draught. You may make a Fight (-2) check to resist. If you fail or choose not to resist, lose your next turn and gain 2 Sanity from the prolonged rest. If you pass, nothing happens.")
    if Environment.Choose("Encounter","Resist the medicine?","Yes","No"," ") == "Yes":
        result = Environment.SkillCheck("Fight",Player,1,-2)
        if result == "Pass":
            return
    Environment.MapScreen.log.addLine(Player.Name+" is now delayed and recovers 2 sanity.")
    Player.Status["Delayed"] = 1
    Player.ModSanity(2)

#sneak(-1)
#pass: move to street
#fail: arrested -> police station
def Asylum7(Environment,Player):
    Environment.PrintEvent( "title","The guards of the sanitarium are aware that there is an intruder. Make a Sneak (-1) check to escape. If you pass, move to the street. If you fail, you are arrested and taken to the Police Station.")
    result = Environment.SkillCheck("Sneak",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have fled to the street.")
        Environment.Teleport(Player, Player.Location.Connections[0])
    elif result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You have been arrested and taken to the police station.")
        Environment.Teleport(Player, Environment.Locations["Police Station"])
        Environment.MapScreen.log.addLine(Player.Name+" is now delayed.")
        Player.Status["Delayed"] = 1


#Gain 1 stamina
def IndependenceSquare1(Environment,Player):
    Environment.PrintEvent( "title","A pair of friendly picnickers share their lunch with you. Gain 1 Stamina.")
    Player.ModHealth(1)

#forced luck(-2) check
#fail: lose 1 item
def IndependenceSquare2(Environment,Player):
    Environment.PrintEvent( "title","There are gypsies camped out in the park. They are master thieves and you are their target. Pass a Luck (-2) check or lose 1 item of your choice.")
    result = Environment.SkillCheck("Luck",Player,1,-2)
    if result == "Fail":
        Environment.PrintEvent("Encounter","Failed! One of your items have been stolen.")
        print "PlaceHolder"
#forced fight(-1) 
#fail: go to the street
def IndependenceSquare3(Environment,Player):
    Environment.PrintEvent( "title","Pass a Fight (-1) check to intimidate a policeman or he rousts you from the park. Move to the street.")
    result = Environment.SkillCheck("Fight",Player,1,-1)
    if result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You have been forced to the street.")
        Environment.Teleport(Player, Player.Location.Connections[0])

#choose luck(-1)
#pass: draw 1 unique card, and you can buy it for cost - 1
#fail: -1 stam and cursed
def IndependenceSquare4(Environment,Player):
    Environment.PrintEvent( "title","There are gypsies camped in the park. Make a Luck (-1) check if you wish to interact with them. If you pass, an old man has spread several items on a blanket for sale. Draw 1 Unique Item and you may buy it for $1 less than the list price. If you fail, a hag comes up to you and tells you that death shadows you. You scoff at her and she cuts the side of your face with her fingernail, drawing blood. Lose 1 Stamina and you are Cursed.")
    if Environment.Choose("Encounter","Interact with the gypsies?","Yes","No"," ") == "Yes":
        result = Environment.SkillCheck("Luck",Player,1,-1)
        if result == "Pass":
            Environment.PrintEvent("Encounter","Success! You can buy the unique item for $1 below list price.")
            item = Environment.DeckDictionary["Unique"].DrawCard(Player,"none")
            price = item[4](item,"price") - 1
            if Player.Money >= price and Environment.Choose("Encounter","Buy the unique item?","Yes","No"," ") == "Yes":
                Player.AddItem( item )
                Player.Money -= price
            else:
                Environment.DeckDictionary["Unique"].DiscardCard(item)
        elif result == "Fail":
            Environment.PrintEvent("Encounter","Failed! You lose one stamina and are cursed")
            Player.ModHealth(-1)
            Player.Curse()
            
#will(-1) check
#pass: gain Anna Kaslow ally
def IndependenceSquare5(Environment,Player):
    Environment.PrintEvent( "title","Make a Will (-1) check. If you pass it, Anna Kaslow the fortune teller offers her help in your investigation. Take her Ally card if it is still available. Otherwise, gain 2 Clue tokens. If you fail, nothing happens.")
    result = Environment.SkillCheck("Will",Player,1,-1)
    if result == "Pass":
        allydraw = Environment.DeckDictionary["Ally"].DrawCard(Player,"Anna Kaslow")
        if allydraw[0] == "No cards to draw":
            Environment.PrintEvent("Encounter","Success! However, Anna Kaslow is unavailable and gives you 2 clues instead.")
            Player.Clues += 2
        else:
            Environment.PrintEvent("Encounter","Success! You gain Anna Kaslow as an ally.")
            Player.AddItem( allydraw )
#will(-1) check
#fail: -1 stam -san
def IndependenceSquare6(Environment,Player):
    Environment.PrintEvent( "title","A shadow falls across you from no apparent source and you shiver with more than just cold. Pass a Will (-1) check or lose 1 Stamina and 1 Sanity.")
    result = Environment.SkillCheck("Will",Player,1,-1)
    if result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You lose one stamina and one sanity")
        Player.ModHealth(-1)
        Player.ModSanity(-1)
# luck(-1)
# pass: -1 stam +2 clue draw 1 spell
#fail: gate opens here and draws you through
def IndependenceSquare7(Environment,Player):
    Environment.PrintEvent( "title","You touch Founder's Rock. Make a Luck (-1) check. If you pass, there is an electrifying shock that opens your mind to the elder things of eons past. Lose 1 Stamina, but gain 2 Clue tokens and draw 1 Spell. If you fail, you find a strange carving. As you finger the grooves, a gate opens here and you are drawn through it.")
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have lost one stamina, but have gained 2 clues and a spell")
        Player.ModHealth(-1)
        Player.Clues += 2
        Player.AddItem( Environment.DeckDictionary["Spell"].DrawCard(Player,"none"))
    if result == "Fail":
        Environment.PrintEvent("Encounter","Failed! A Gate is opening around you!")
        Environment.NewGate( Environment.DrawGate() , Player.Location )
        
#Move to any location, then have encounter there
def BankOfArkham1(Environment,Player):
    Environment.PrintEvent( "title","One of the other customers in the bank recognizes you and offers you a lift. Move to any location or street area in Arkham. If you move to a location, immediately have an encounter there.")
    templist = list()
    for loc in Environment.Locations :
        if Environment.Locations[loc].IsInArkham() == 1:
            templist.append( Environment.Locations[loc].Name )
    result = Environment.ListChoose("Choose a Destination","Choose a Destination", templist)
    Environment.Teleport(Player, Environment.Locations[result])
    Environment.PrintEvent("Encounter","You are now at"+Player.Location.Name)
    if Player.Location.Name in EncounterDict :
        exec (EncounterDict[Player.Location.Name]+str(random.randint(1,7))+"(Environment,Player)")
    
    

#flip a coin, then Luck(-2) check
#if pass & heads : blessed
#if fail & tails : cursed
def BankOfArkham2(Environment,Player):
    Environment.PrintEvent( "title","You find a penny with a strange sigil carved into it. Amused, you flip it in the air, then gasp as you feel the sudden gathering of magical forces around you. Make a Luck (-2) check. If you pass, the penny comes up heads. You are Blessed. If you fail, it comes up tails. You are Cursed." )   
    coin = random.choice(["Heads","Tails"])
    result = Environment.SkillCheck("Luck",Player,1,-2)
    if result == "Pass" and coin == "Heads" :
        Player.Bless()
        Environment.PrintEvent("Encounter","You are now blessed")
    if result == "Fail" and coin == "Tails" :
        Player.Curse()
        Environment.PrintEvent("Encounter","You are now cursed")
   
    
    
#do speed(-1)
#pass: +$2
def BankOfArkham3(Environment,Player):
    Environment.PrintEvent( "title","You see a richly dressed man making a large withdrawal. On the way out, he lights his cigar with a piece of green paper which he then drops on the ground. Pass a Speed (-1) check to stub it out with your toe before it burns up. You discover it to be a slightly singed two dollar bill. Gain $2.")    
    result = Environment.SkillCheck("Speed",Player,1,-1)
    if result == "Pass":
        Player.Money += 2
        Environment.PrintEvent("Encounter","Success, you gain $2!")
    else:
        Environment.PrintEvent("Encounter","Too slow, the bill is too badly burned!")
        
# -1 sanity
#
def BankOfArkham4(Environment,Player):
    Environment.PrintEvent( "title","A little old lady stands in front of you in line counting out a bag of pennies to deposit. Lose 1 Sanity.")
    Player.ModSanity(-1)
# choose: pay $2 and luck(-1)
# pass: draw 1 unique
# fail: draw 1 common
def BankOfArkham5(Environment,Player):
    Environment.PrintEvent( "title","A man wearing dirty and tattered clothing is loitering outside the bank. He offers to sell you his last possession to get some food money for him and his family. If you accept, pay $2 and make a Luck (-1) check. If you pass, draw 1 Unique Item. If you fail, draw 1 Common Item.")
    if Environment.Choose("Encounter","Give the man $2 for his last possession?","Yes","No"," ") == "Yes" :
        result = Environment.SkillCheck("Luck",Player,1,-1)
        if result == "Pass":
            Player.AddItem( Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
            Environment.PrintEvent("Encounter","Success, you get a unique item!")
        elif result == "Fail":
            Player.AddItem( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
            Environment.PrintEvent("Encounter","Failed, you get a common item!")
        
#combat(-1) fail: lose all money
def BankOfArkham6(Environment,Player):
    Environment.PrintEvent( "title","This is a stick-up, see? Nobody move! Three men armed with tommy guns rob the bank while you're standing in line. Make a Combat (-1) check. If you pass, you drive them off. Nothing happens. If you fail, lose all of your money.	")
    result = Environment.SkillCheck("Combat",Player,1,-1)
    if result == "Fail":
        Player.Money = 0
        Environment.PrintEvent("Encounter","Failed! You have lost all your money")

# -1 sanity +5 dollars
def BankOfArkham7(Environment,Player):
    Environment.PrintEvent( "title","A teller you've never seen before insists she just saw you come in and make a deposit the day before. She proves it by showing you your signature. Gain $5, but lose 1 Sanity.")
    Player.ModSanity(-1)
    Player.Money += 5

#####################################################################################################
#EastTown Section



#force:  luck(-1)
#pass: Nothing
#fail: -2 stam
def PoliceStation1(Environment,Player):
    Environment.PrintEvent( "title","Deputy Dingby, excitedly cleaning his gun, fires a bullet from the chamber in your direction. Pass a Luck (-1) check to avoid getting shot. If you fail, lose 2 Stamina. ")
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You have lost 2 stamina")
        Player.ModHealth(-2)
# luck(-1)
#pass: Search common item deck for .45 revolver card
#
def PoliceStation2(Environment,Player):
    Environment.PrintEvent( "title","If you succeed at a Luck (-1) check, then Deputy Dingby absentmindedly leaves you holding his gun. You may search the Common Item deck for a .38 Revolver card and take it."   ) 
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You keep the .38 Revolver")
        Player.AddItem( Environment.DeckDictionary["Common"].DrawCard(Player, ".38 Revolver"))
# will(-1)
#pass: +1 clue
#fail -1 sanity and move to street
def PoliceStation3(Environment,Player):
    Environment.PrintEvent( "title","One of the men in the holding cells tries to intimidate you with stories about the things he's seen. Make a Will (-1) check. If you pass, gain 1 Clue Token. If you fail, move to the street and lose 1 Sanity as the man laughs at your retreating back." )
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain 1 clue.")
        Player.Clues += 1
    if result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You move to the street and lose 1 sanity.")
        Environment.Teleport(Player, Player.Location.Connections[0])
        Player.ModSanity(-1)
# luck(-2)
#pass: 1 unique item
#
def PoliceStation4(Environment,Player):
    Environment.PrintEvent( "title","Sheriff Engle trusts you and asks you to step into his office to discuss the recent strange events. Pass a Luck (-2) check to convince him to take you into his confidence and give you something to help you out. Draw 1 Unique Item.")
    result = Environment.SkillCheck("Luck",Player,1,-2)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain 1 unique item.")
        Player.AddItem( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
        

# sneak(0)
#pass: search common item deck for research materials (zack:maybe just turn it to 1 clue)
#
def PoliceStation5(Environment,Player):
    Environment.PrintEvent( "title","Deputy Dingby accidently drops a case file as he makes his way past you. Pass a Sneak (+0) check to search the Common Item deck for a Research Materials card and take it.")
    result = Environment.SkillCheck("Sneak",Player,1,0)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain 1 clue.")
        Player.Clue += 1
      
        
#Pay 5 dollars or discard all weapons
#
#
def PoliceStation6(Environment,Player):
    Environment.PrintEvent( "title","Sheriff Engle notes that you're carrying an awful lot of Weapons. Either pay him $5 or discard all of your Weapons.")
    Choice = Environment.Choose("Encounter","Pay 5 dollars or lose all your weapons","Pay $5","Refuse"," ")
    if Choice == "Pay $5" and Player.Money >= 5:
        Environment.PrintEvent("Encounter","Success! You keep your weapons, but lose 5 dollars.")
        Player.Money -= 5
    else:
        Environment.PrintEvent("Encounter","All of your weapons have been confiscated.")
        print "PLACEHOLDER-PoliceStation6"
        

#will(-1)
#pass: +2 clues
#
def PoliceStation7(Environment,Player):
    Environment.PrintEvent( "title","Pass a Will (-1) check to convince Deputy Dingby to share some files with you that are very interesting. Gain 2 Clue Tokens." )   
    result = Environment.SkillCheck("Will",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain 2 clues.")
        Player.Clues += 2
            


#force:  luck(-1)
#pass: +$5
#fail: -$3 & if you cant pay move to street and -1 stam
def HibbsRoadhouse1(Environment,Player):
    Environment.PrintEvent( "title","You enter a friendly card game. Make a Luck (-1) check. If you pass, you win $5. If you fail, you lose $3. If you lose and can't pay, the boys rough you up and throw you outside. Lose 1 Stamina and move to the street.")
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have won $5.")
        Player.Money += 5
    elif result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You have lost the card game and must pay up $3.")
        if Player.Money < 3:
            Environment.PrintEvent("Encounter","You didn't have enough money to cover your debt, You have been beaten and thrown into the streets.")
            Environment.Teleport(Player,Player.Location.Connections[0])
            Player.ModHealth(-1)
        else:
            Player.Money -= 3
            

# look at top 3 common item cards, buy any for cost +1
#
#
def HibbsRoadhouse2(Environment,Player):
    Environment.PrintEvent( "title","Joey The Rat Vigil slips into an empty chair at your table and whispers, Pssst! Wanna buy something? Look at the top 3 cards of the Common Item deck. You may purchase any or all of them for $1 above the list price. Hey, Ive got overhead! the Rat explains"    )
    if Environment.Choose("Common Items","Would you like to shop for a common item?","Yes","No"," ") == "Yes":
        templist = list()
        templist.append( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
        templist.append( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
        templist.append( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
        result = Environment.ItemChoose( "Choose an item ", templist )
        for item in templist :
            if item[0] == result[0] and Environment.Choose("Confirm","Buy this item?","Yes","No", " ") == "Yes":
                price = item[4](item,"price") + 1
                if Player.Money >= price : #need a way to know cost 
                    Player.AddItem( item )
                    Player.Money -= price
            else:
                Environment.DeckDictionary["Common"].DiscardCard(item)


#If you spend 3 clues, add Ryan Dean Ally card
#if hes unavailable draw 2 common items
#
def HibbsRoadhouse3(Environment,Player):
    Environment.PrintEvent( "title","So, whats your story, friend? A smiling man inquires about your adventures over a glass of gin. You tell him your story. If you spend 3 Clue Tokens, he introduces himself as Ryan Dean and asks to join you. Take his Ally card. If its not available, he gives you some useful items instead. Draw 2 Common Items."    )
    if Player.Clues >= 3 and Environment.Choose("Encounter","Do you want to spend 3 clues to convince Ryan Dean to join you as an Ally?","Yes","No"," ") == "Yes":
        Player.Clues -= 3
        Environment.PrintEvent("Encounter","Ryan Dean agrees to join your party.")
        allydraw = Environment.DeckDictionary["Ally"].DrawCard(Player,"Ryan Dean")
        if allydraw[0] == "No cards to draw":
            Environment.PrintEvent("Encounter","Success! However, Ryan Dean is unavailable and gives you 2 common items instead.")
            Player.AddItem( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
            Player.AddItem( Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
        else:
            Player.AddItem( allydraw )

#will(-1) check
#pass: 2 clues
#fail: move to street either (you choose) lose 1 item or all money
def HibbsRoadhouse4(Environment,Player):
    Environment.PrintEvent( "title","Prohibition failed to influence the proprietor of Hibb's You drink heavily while quizzing the locals about the strange goings-on in Arkham. Make a Will (-1) check. If you pass, you hold your liquor and learn something. Gain 2 Clue tokens. If you fail, you pass out. Move to the street and either have 1 item (your choice) or all of your money stolen."    )
    result = Environment.SkillCheck("Will",Player,1,-1)
    if result == "Pass" :
        Environment.PrintEvent("Encounter","Success! You gain 2 clues.")
        Player.Clues +=2
    elif result == "Fail":
        Environment.Teleport(Player,Player.Location.Connections[0])
        choice = Environment.Choose("Encounter","Failed! You have passed out and have been thrown to the street. You must have lost either all your money or 1 of your items", "Money","1 Item"," ")
        if choice == "Money":
            Player.Money = 0
        elif choice == "1 Item":
            print "placeholder- HibbsRoadHouse4"

#force: luck(-1)
#
#fail: lose all money
def HibbsRoadhouse5(Environment,Player):
    Environment.PrintEvent( "title","Pass a Luck (-1) check or a pickpocket cleans you out! Lose all your money.")
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "fail":
        Environment.PrintEvent("Encounter","Failed! All of your money has been stolen.")
        Player.Money = 0
         
#
#A monster appears (remember to disapear it after battle if not trophy)
#Location.MonsterList
def HibbsRoadhouse6(Environment,Player):
    Environment.PrintEvent( "title","A horrible monster appears!"  )  
    EventMonster = Environment.DrawMonster()
    EventMonster.Location = Player.Location
    EventMonsterList = list()
    EventMonsterList.append(EventMonster)
    Environment.Combat(Player, EventMonsterList )
    if EventMonster in EventMonsterList:
        Environment.ReturnMonster(EventMonster)
    

#
#Search common deck for wiskey card and take it
#
def HibbsRoadhouse7(Environment,Player):
    Environment.PrintEvent( "title","A stranger buys you a drink. You may search the Common Item deck for a Whiskey card and take it.")
    Player.AddItem( Environment.DeckDictionary["Common"].DrawCard(Player,"Whiskey"))   


#Search common item deck for food card and take it
#
#
def VelmasDiner1(Environment,Player):
    Environment.PrintEvent( "title","Velma comments on how skinny you look and gives you a sandwich on the house. You may search the Common Item deck for a Food and take it." )   
    print "Place holder"

#Will(-2)
#pass: +$5
#
def VelmasDiner2(Environment,Player):
    Environment.PrintEvent( "title","You spot a rat leaving the kitchen. Pass a Will (-2) check to convince Velma to bribe you $5 not to tell anyone." )   
    result = Environment.SkillCheck("Will",Player,1,-2)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gained $5.")
        Player.Money += 5

#Pay up to $6 to gain
# that many sanity or stamina (in any amount)
#
def VelmasDiner3(Environment,Player):
    Environment.PrintEvent( "title","What'll it be, hon? Velma takes your order. Pay up to $6 to gain that many points split between Sanity and Stamina however you like.")
    choice = Environment.ListChoose("Encounter","Buy up to $6 worth of food and restore Stamina/Sanity equal to the amount bought.", ["0","1","2","3","4","5","6"])
    payment = int(choice)
    while payment > 0:
        option1 = "None"
        option2 = "None"
        if Player.Stats["Stamina"] < (Player.Stats["MaxStam"]+Player.BonusStats["MaxStam"]):
            option1 = "Stamina"
        if Player.Stats["Sanity"] < (Player.Stats["MaxSanity"]+Player.BonusStats["MaxSanity"]):
            option2 = "Sanity"
        if option1 == option2:
            return
        choice = Environment.Choose("Encounter","Which stat do you wish to restore?",option1,option2, "")
        if choice == "Stamina":
            payment -= 1
            Player.ModHealth(1)
        elif choice == "Sanity":
            payment -= 1
            Player.ModSanity(1)
            
#forced luck(-1)
#fail: -2 stam
#
def VelmasDiner4(Environment,Player):
    Environment.PrintEvent( "title","You get food poisoning! Pass a Luck (-1) check or lose 2 Stamina.")
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You lose 2 stamina.")    

#choose: sneak(-1) check
#pass: roll die and get that much money
#fail: move to street
def VelmasDiner5(Environment,Player):
    Environment.PrintEvent( "title","You find some Money on the floor under the back booth. If you take it, make a Sneak (-1) check. If you pass, roll a die and gain that much money. If you fail, Velma sees you pick up the money. She comes over and swipes it out of your hands screaming, Stealing my tips! so loudly that you flee the diner. Move to the Street")
    if Environment.Choose("Encounter","Try and take the money?","Yes","No", "") == "Yes":
        result = Environment.SkillCheck("Sneak",Player,1,-1)
        if result == "Pass":
            Environment.PrintEvent("Encounter","Success! Now look at how much money you have collected.")    
            cash = int(Environment.RollDie())
            Player.Money += cash
        elif result == "Fail":
            Environment.PrintEvent("Encounter","Failed! You have been noticed and flee to the street.")
            Environment.Teleport(Player,Player.Location.Connections[0])
            
#luck(-1)
#pass: blessed
#fail: cursed
def VelmasDiner6(Environment,Player):
    Environment.PrintEvent( "title","Velma reads the tea leaves left in your cup. Make a Luck (-1) check. If you pass, the formation of the leaves indicates hope, you are Blessed. If you fail, the future looks bleak, you are Cursed."    )
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You are blessed.")
        Player.Bless()
    elif result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You are cursed.")
        Player.Curse()


#pay $1 for +2 stam
#
#
def VelmasDiner7(Environment,Player):
    Environment.PrintEvent( "title","This must be where pies go when they die. If you want, pay $1 to enjoy a fine slice of cherry pie. If you do, gain 2 Stamina")
    if Environment.Choose("Encounter","Pay $1 to restore 2 stamina?","Yes","No", "") == "Yes":
        Player.Money -= 1
        Player.ModHealth(2)


#####################################################################################################
#Frenchhill Section
#
#BIG NOTE: if you are twilight member, you're encounters are INNER SANCTUM instead of lodge
#if Player.Status["SilverLodgeMember"] > 0 :

#
#Gate and Monster Appear
#
def WitchHouse1(Environment,Player):
    Environment.PrintEvent( "title","A gate and a monster appear!")
    Environment.NewGate(Environment.DrawGate(),Player.Location)
    
# make Luck(0) check  >>>successes :
#0) You suddenly realize what you've been eating. Lose 3 Sanity.
#1) You gorge yourself, unable to stop eating. Stay here next turn.
#2) The food makes you feel sick. Lose 1 Stamina.
#3+) The meal refreshes you. Gain 3 Stamina.
#
def WitchHouse2(Environment,Player):
    Environment.PrintEvent( "title","You find a banquet laid out in the dining room and feel compelled to sit down and eat. Make a Luck (+0) check and consult the following chart:\n Successes:\n 0) You suddenly realize what youve been eating. Lose 3 Sanity.\n 1) You gorge yourself, unable to stop eating. Stay here next turn.\n 2) The food makes you feel sick. Lose 1 Stamina.\n 3+) The meal refreshes you. Gain 3 Stamina.")
    success = Environment.SuccessCheck("Luck",Player, 0, 0)
    if success == 0:
        Environment.PrintEvent("Encounter","You suddenly realize what you've been eating. Lose 3 Sanity.")
        Player.ModSanity(-3)
    elif success == 1:
        Player.Status["Delayed"] = 1
        Environment.PrintEvent("Encounter","You gorge yourself and become delayed.")
    elif success == 2:
        Environment.PrintEvent("Encounter","You feel sick. Lose 1 Stamina")
        Player.ModHealth(-1)
    elif success <= 3:
        Environment.PrintEvent("Encounter","You feel refreshed. Gain 3 Stamina")
        Player.ModHealth(3)

#lore(-1)
#pass:  Thomas F. Malone joins your party (or +2 clues)
#
def WitchHouse3(Environment,Player):
    Environment.PrintEvent( "title","Excuse me, stranger, but have you ever seen this symbol before? A man standing near the house holds up an occult symbol. Make a Lore (-1) check. If you pass, the man introduces himself as Thomas F. Malone, a police detective visiting Arkham on a case. He's impressed with you and offers to join you. Take his Ally card. If it's not available, he tells you some valuable information instead. Gain 2 Clue tokens. If you fail, nothing happens.")
    result = Environment.SkillCheck("Lore",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! Thomas F. Malone joins your party.")
        allydraw = Environment.DeckDictionary["Ally"].DrawCard(Player,"Thomas F. Malone")
        if allydraw[0] == "No cards to draw":
            Environment.PrintEvent("Encounter","Success! However, Thomas F. Malone is unavailable and gives you 2 clues instead.")
            Player.Clues += 2
        else:
            Player.AddItem( allydraw )


#will(-2)
#pass: draw 1 spell
#fail: discard half your items, rounding down
def WitchHouse4(Environment,Player):
    Environment.PrintEvent( "title","You are overcome by the echoing chants of the long-gone witches who have lived and died here - you pass out. Make a Will (-2) check. If you pass, you learn an ancient spell in your dreams. Draw 1 Spell. If you fail, you are missing half your items when you wake up. Discard half of your items (your choice, round down).")
    result = Environment.SkillCheck("Will",Player,1,-2)
    if result == "Pass":
        Player.AddItem( Environment.DeckDictionary["Spell"].DrawCard(Player,"none"))   
    elif result == "Fail":
        print "WitchHouse4---Discard half items"

#roll die, lose that many sanity but gain that many clues
#
#
def WitchHouse5(Environment,Player):
    Environment.PrintEvent( "title","In an old journal you learn some horrible eldritch secrets. Roll a die. Lose that much Sanity and gain that many Clue tokens.")
    result = Environment.RollDie()
    Environment.PrintEvent("Encounter","You gain "+str(result)+ " but lose "+str(result)+" sanity.")
    Player.Clues += result
    Player.ModSanity(-result)
    
    
#Luck(-1)
#pass: draw 1 unique
#
def WitchHouse6(Environment,Player):
    Environment.PrintEvent( "title","Pass a Luck (-1) check to find an odd-looking item in an old dusty display case. Draw 1 Unique Item." )   
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain 1 unique item.")    
        Player.AddItem( Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))   
    else:
        Environment.PrintEvent("Encounter","Failed! Nothing happens.")    


#
#lose 1 sanity
#
def WitchHouse7(Environment,Player):
    Environment.PrintEvent( "title","You feel the house actually breathe and speak your name. Lose 1 Sanity.")    
    Player.ModSanity(-1)


#Luck(-2)
#fail: cursed
#
def InnerSanctum1(Environment,Player):
    Environment.PrintEvent( "title","Carl Sanford does not trust you and at the climax of the monthly ceremony spits a spell at you. Pass a Luck (-2) check or you are Cursed.")
    result = Environment.SkillCheck("Luck",Player,1,-2)
    if result == "Fail":
        Environment.PrintEvent("Encounter","Failed! You are now cursed.")    
        Player.Curse()
#Lose up to 3 sanity and gain that many clues
#
#
def InnerSanctum2(Environment,Player):
    Environment.PrintEvent( "title","Participating in the monthly ceremony, you witness great power and great evil. Lose up to 3 Sanity and gain that many Clue tokens.")
    choice = Environment.ListChoose("Encounter","How many Sanity would you like to lose.",["1","2","3"])
    Player.Clues += int(choice)
    Player.ModSanity(-int(choice))

#Luck(-2)
#pass: Draw any unique item
#
def InnerSanctum3(Environment,Player):
    Environment.PrintEvent( "title","You are allowed into the vault of Silver Secrets. Pass a Luck (-2) check to steal a very unusual item. Search the Unique Item deck and take any one Unique Item you want.")
    result = Environment.SkillCheck("Luck",Player,1,-2)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain 1 unique item.")    
        Player.AddItem( Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
    else:
        Environment.PrintEvent("Encounter","Failed! Nothing happens.")    
        
    
#Choose : spend 2 clues and 1 sanity to make lore(-2)check
#pass: close one gate of your choice
#
def InnerSanctum4(Environment,Player):
    Environment.PrintEvent( "title","You're invited to take part in a Gating ceremony. If you agree, spend 2 Clue tokens and 1 Sanity to make a Lore (-2) check. If you pass, close one gate of your choice. If you fail, nothing happens.")
    if Environment.Choose("Encounter","Go to the gating ceremony?","Yes","No", "It will cost 2 clues and 1 sanity.") == "Yes":
        if Player.Clues >= 2:
            Player.Clues -= 2
        else:
            return
        Player.ModSanity(-1)
        if Player.Location.Name != "Silver Twilight Lodge":
            return
        result = Environment.SkillCheck("Lore",Player,1,-2)
        if result == "Pass":
            Environment.PrintEvent("Encounter","Success! You may close any gate.")
            listchoose = list()
            for gate in self.Gates:
                listchoose.append(gate.Location.Name)
            if not listchoose:
                return
            choice3 = Environment.ListChoose("Encounter","Choose a location to close the gate.",listchoose)
            Gate = Environment.Locations[choice3].Gate
            self.MapScreen.deleteGateImage(Gate)
            try:
                self.Gates.remove(Gate)
            except(ValueError,AttributeError,KeyError):
                print "non threatening exception"
            
            Gate.Location.RemoveGate(Gate)
            for Monster in self.Monsters :
                if Monster.HomeDimension == Gate.DimensionalShape :
                    self.MapScreen.deleteMonster(Monster)
                    self.ReturnMonster(Monster)
        else:
            Environment.PrintEvent("Encounter","Failed! Nothing happens.")
            
        

#
#a monster appears
#
def InnerSanctum5(Environment,Player):
    Environment.PrintEvent( "title","You attend a ceremony in which the order opens a gate and a monster bursts out of it before the gate closes once more. A monster appears!")
    EventMonster = Environment.DrawMonster()
    EventMonster.Location = Player.Location
    EventMonsterList = list()
    EventMonsterList.append(EventMonster)
    Environment.Combat(Player, EventMonsterList )
    if EventMonster in EventMonsterList:
        Environment.ReturnMonster(EventMonster)
#spend 1 sanity to Luck(-1)
#pass: claim any monster as trophy
#
def InnerSanctum6(Environment,Player):
    Environment.PrintEvent( "title","The Order of the Silver Twilight casts a banishment spell in their monthly ceremony. Spend 1 Sanity to make a Luck (-1) check. If you pass, claim any one monster on the board as a trophy. If you fail, nothing happens")
    if Environment.Choose("Encounter","Participate in the banishment spell?","Yes","No", "It will cost 1 sanity.") == "Yes":
        Player.ModSanity(-1)
        if Player.Location.Name != "Silver Twilight Lodge":
            return
        result = Environment.SkillCheck("Luck",Player,1,-1)
        if result == "Pass":
            Environment.PrintEvent("Encounter","Success! You may claim a monster as your trophy.")
            listchoose = list()
            for mon in self.Monsters:
                if mon.Location.Name != "Outskirts":
                    listchoose.append(mon.Name)
            if not listchoose:
                return
            choice3 = Environment.ListChoose("Encounter","Choose a location to close the gate.",listchoose)
            for Monster in self.Monsters :
                if Monster.Name == choice3 :
                    Environment.PrintEvent("Encounter","You have taken "+str(Monster.Name)+" as your trophy.")
                    self.MapScreen.deleteMonster(Monster)
                    self.AddMonsterTrophy(Monster)
                    return
        else:
            Environment.PrintEvent("Encounter","Failed! Nothing happens.")            

#Pay monthly dues $3 or
#lose 2 sanity and membership
#
def InnerSanctum7(Environment,Player):
    Environment.PrintEvent( "title","Pay your monthly dues of $3 or lose 2 Sanity from strange dreams sent to you by Carl Sanford when he kicks you out of the Order. If you are kicked out, lose your Silver Twilight Lodge Membership.")
    if Player.Money >= 3 and Environment.Choose("Encounter","Pay monthly dues?","Yes","No", " ") == "Yes":
        Player.money -= 3
    else:
        Environment.PrintEvent("Encounter","You have been kicked out of the Silver Twilight Order and have lost 2 sanity from strange dreams sent by Carl Sanford.")
        Player.Status["SilverLodgeMember"] = 0
        Player.ModSanity(-2)

        

#Lore(-1)
#fail: lose all clues and move to street
#pass: +3 clues
def SilverTwilightLodge1(Environment,Player):
    if Player.Status["SilverLodgeMember"] > 0 :
        exec InnerSanctum1(Environment,Player)
        return
    Environment.PrintEvent( "title","Carl Sanford draws you into the study to talk and you feel the cold creep of dread listening to him. Make a Lore (-1) check. If you pass, your willpower stands up to the test of the ancient wizard and you even learn something of value. Gain 3 Clue tokens. If you fail, his hypnotic tones lull you into a trance. The conversation seems short, but when you leave the study, much time has passed and your thoughts are confused. Lose all of your Clue tokens and move to the street.")
    result = Environment.SkillCheck("Lore",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain 3 clues.")
        Player.Clues += 3
    else:
        Environment.PrintEvent("Encounter","Failed! You lose all clues and move to the street.")
        Player.Clues = 0
        Environment.Teleport(Player,Player.Location.Connections[0])
        


#luck(-1)
#fail: cursed
#
def SilverTwilightLodge2(Environment,Player):
    if Player.Status["SilverLodgeMember"] > 0 :
        exec InnerSanctum2(Environment,Player)
        return
    Environment.PrintEvent( "title","Brushing up against a strange object in the hall, you feel stretched and thin, like your skin is too tight. Pass a Luck (-1) check or you are Cursed.")
    result = Environment.SkillCheck("Luck",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! Nothing happens.")
    else:
        Environment.PrintEvent("Encounter","Failed! You are cursed.")
        Player.Curse()
#Lore(-1)
#fail: 
#pass: draw 2 spells, keep one
def SilverTwilightLodge3(Environment,Player):
    if Player.Status["SilverLodgeMember"] > 0 :
        exec InnerSanctum3(Environment,Player)
        return
    Environment.PrintEvent( "title","You find an old parchment in the study. Pass a Lore (-1) check to draw 2 Spells and keep one of your choice.")
    result = Environment.SkillCheck("Lore",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You learn a new spell.")
        templist = list()
        templist.append( Environment.DeckDictionary["Spell"].DrawCard(Player,"none"))               
        templist.append( Environment.DeckDictionary["Spell"].DrawCard(Player,"none"))
        result = Environment.ItemChoose( "Choose a spell to learn ", templist )
        for item in templist :
            if item[0] == result[0] :
                Player.AddItem( item )
            else:
                Environment.DeckDictionary["Spell"].DiscardCard(item)        
    else:
        Environment.PrintEvent("Encounter","Failed! Nothing happens.")


#Sneak(-2)
#pass: roll 2 die , success = draw unique fail = draw common
#fail:
def SilverTwilightLodge4(Environment,Player):
    if Player.Status["SilverLodgeMember"] > 0 :
        exec InnerSanctum4(Environment,Player)
        return
    Environment.PrintEvent( "title","Make a Sneak (-2) check. If you pass, you slip into the temple area of the Lodge and find 2 items of interest. Roll a die for each item. On a success, draw a Unique Item, otherwise draw a Common Item.")
    result = Environment.SkillCheck("Sneak",Player,1,-2)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You find 2 items of interest.")
        if Player.Status["Cursed"] == 1:
            suc = 6
        elif Player.Status["Blessed"] == 1:
            suc = 4
        else:
            suc = 5
        if Environment.RollDie() >= suc:
            Environment.PrintEvent("Encounter","Success! You find a unique item.")
            Player.AddItem(Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
        else:
            Environment.PrintEvent("Encounter","Failed! You find a common item.")
            Player.AddItem(Environment.DeckDictionary["Common"].DrawCard(Player,"none"))            
        if Environment.RollDie() >= suc:
            Environment.PrintEvent("Encounter","Success! You find a unique item.")
            Player.AddItem(Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
        else:
            Environment.PrintEvent("Encounter","Failed! You find a common item.")
            Player.AddItem(Environment.DeckDictionary["Common"].DrawCard(Player,"none"))   
    else:
        Environment.PrintEvent("Encounter","Failed! Nothin happens.")
        
#choose pay $3 for twilight membership
#if no: will(-1) ->fail: lose 3 stam 
#move to street
def SilverTwilightLodge5(Environment,Player):
    if Player.Status["SilverLodgeMember"] > 0 :
        exec InnerSanctum5(Environment,Player)
        return
    Environment.PrintEvent( "title","Care to join the Order? Carl Sanford and several of his henchmen ask. If you accept, pay $3 and take a Silver Twilight Membership. If you decline, pass a Will (-1) check or lose 3 Stamina as the henchmen assist you out the door. Whether you pass or not, move to the street.")
    if Player.Money >= 3 and Environment.Choose("Encounter","Join the Silver Twilight Order?","Yes","No", " ") == "Yes":
        Player.Money -= 3
        Player.Status["SilverLodgeMember"] = 1
    else:
        result = Environment.SkillCheck("Will",Player,1,-1)
        if result == "Fail":
            Environment.PrintEvent("Encounter","Failed! You have been forcefully removed from the location and have lost 3 stamina.")
        else:
            Environment.PrintEvent("Encounter","Success! You have been asked to leave.")
        Environment.Teleport(Player,Player.Location.Connections[0])
        
#fight(-1)
#pass: gain ally Ruby Standish or if unavail 1 unique
#
def SilverTwilightLodge6(Environment,Player):
    if Player.Status["SilverLodgeMember"] > 0 :
        exec InnerSanctum6(Environment,Player)
        return
    Environment.PrintEvent( "title","You hear the quiet sounds of an intruder. If you investigate, you find a woman dressed in black. She attacks you as soon as she sees you. Pass a Fight (-1) check to subdue her long enough to explain your investigation. You find out that her name is Ruby Standish and that she was robbing the Lodge. However, upon hearing your tale, she agrees to join you. Take her Ally card. If it is not available, draw a Unique Item instead.")
    result = Environment.SkillCheck("Fight",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain Ruby Standish as an ally.")
        allydraw = Environment.DeckDictionary["Ally"].DrawCard(Player,"Ruby Standish")
        if allydraw[0] == "No cards to draw":
            Environment.PrintEvent("Encounter","Success! However, Ruby Standish is unavailable and gives you 1 unique item instead.")
            Player.AddItem(Environment.DeckDictionary["Unique"].DrawCard(Player,"none"))
        else:
            Player.AddItem( allydraw )
    else:
        Environment.PrintEvent("Encounter","Failed! The woman escapes.")
    
    


#choose pay $3 for twilight membership
#if no: will(-1) ->fail: lose 3 stam 
#move to street
def SilverTwilightLodge7(Environment,Player):
    if Player.Status["SilverLodgeMember"] > 0 :
        exec InnerSanctum7(Environment,Player)
        return
    Environment.PrintEvent( "title","Care to join the Order? Carl Sanford and several of his henchmen ask. If you accept, pay $3 and take a Silver Twilight Membership. If you decline, pass a Will (-1) check or lose 3 Stamina as the henchmen assist you out the door. Whether you pass or not, move to the street.")
    if Player.Money >= 3 and Environment.Choose("Encounter","Join the Silver Twilight Order?","Yes","No", " ") == "Yes":
        Player.Money -= 3
        Player.Status["SilverLodgeMember"] = 1
    else:
        result = Environment.SkillCheck("Will",Player,1,-1)
        if result == "Fail":
            Environment.PrintEvent("Encounter","Failed! You have been forcefully removed from the premises and have lost 3 stamina.")
        else:
            Environment.PrintEvent("Encounter","Success! You have been asked to leave.")
        Environment.Teleport(Player,Player.Location.Connections[0])


##################################################################
#Merchant District

#choose: lore(-1)
#pass: draw 1 spell
#fail: delay , +2 clues
def Unnameable1(Environment,Player):
    Environment.PrintEvent( "title","In a dusty and decaying roll-top desk, you find a mysterious manuscript. If you read it, make a Lore (-1) check. If you pass, draw 1 Spell. If you fail, the manuscript is nothing but the insane babbling of a previous renter. Stay here next turn reading it, but gain 2 Clue Tokens. ")
    if Environment.Choose("Encounter","Read the manuscript?","Yes","No", " ") == "Yes":
        result = Environment.SkillCheck("Lore",Player,1,-1)
        if result == "Pass":
            Environment.PrintEvent("Encounter","Success! You have learned a new spell .")
            Player.AddItem(Environment.DeckDictionary["Spell"].DrawCard(Player,"none")) 
        else:
            Environment.PrintEvent("Encounter","Failed! You waste your time reading the manuscript are delayed and gain 3 clues.")
            Player.Status["Delayed"] = 1
            Player.Clues += 2
    
       



#choose: Luck(-1)
#pass: draw 1 unique
#fail: -2 stam -1 san
def Unnameable2(Environment,Player):
    Environment.PrintEvent( "title","You notice a glint of light in a crevice. If you reach in, make a Luck (-1) check. If you pass, draw 1 Unique Item. If you fail, you feel a sharp pain as teeth clamp down on your hand. You manage to pull free, but you lose 2 Stamina and 1 Sanity.")
    if Environment.Choose("Encounter","Read the manuscript?","Yes","No", " ") == "Yes":
        result = Environment.SkillCheck("Luck",Player,1,-1)
        if result == "Pass":
            Environment.PrintEvent("Encounter","Success! You have retrieved a unique item.")
            Player.AddItem(Environment.DeckDictionary["Unique"].DrawCard(Player,"none")) 
        else:
            Environment.PrintEvent("Encounter","Failed! You have been bitten by an unknown creature and lose 2 stamina and 1 sanity.")
            Player.ModHealth(-2)
            Player.ModSanity(-1)
    
   

#choose: lose 2 sanity if sane take Eric Colt ally card
#if unavail -> 3 clues
#
def Unnameable3(Environment,Player):
    Environment.PrintEvent( "title","You bump into Eric Colt. He tells you a horrible tale of the Mythos to test your nerve. If you listen, lose 2 Sanity. If this doesn't drive you insane, take his Ally card if it is available. If it is not available, you may pump him for information instead. Gain 3 Clue Tokens.")
    Player.ModSanity(-2)
    if Player.Location.Name == "Unameable":
            Environment.PrintEvent("Encounter","Success! You have passed Eric Colt's test and gain him as an ally.")
            allydraw = Environment.DeckDictionary["Ally"].DrawCard(Player,"Eric Colt")
            if allydraw[0] == "No cards to draw":
                Environment.PrintEvent("Encounter","Success! However, Eric Colt is unavailable and gives you 3 clues instead.")
                Player.Clues += 3
            else:
                Player.AddItem( allydraw )
        


#speed(-1)
#fail: LITAS
#
def Unnameable4(Environment,Player):
    Environment.PrintEvent( "title","You hear scurrying and squeaking of a horde of rats from inside the walls. Abruptly, you realize that they are moving to surround you. Pass a Speed (-1) check to make it to the front door first. If you fail, you are Lost in time and space.  ")
    result = Environment.SkillCheck("Speed",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have escaped the horde of rats.")

    else:
        Environment.PrintEvent("Encounter","Failed! You are lost in time and space.")
        Environment.Teleport(Player,Environment.Locations["Lost in Time and Space"])

#Luck(-1)
#pass: draw 1 unique
#
def Unnameable5(Environment,Player):
    Environment.PrintEvent( "title","Pass a Luck (-1) check to find a hidden cache concealed in the wall of an upstairs bedroom. Draw 1 Unique Item.")
    result = Environment.SkillCheck("Speed",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have found the cache and gained a unique item.")
        Player.AddItem(Environment.DeckDictionary["Unique"].DrawCard(Player,"none")) 
    else:
        Environment.PrintEvent("Encounter","Failed! You find nothing.")

#
#a monster and gate appear
#
def Unnameable6(Environment,Player):
    Environment.PrintEvent( "title","A monster and a gate appear!")
    Environment.NewGate(Environment.DrawGate(),Player.Location)


#speed(-1)
#pass: move to street
#fail: -2 stam
def Unnameable7(Environment,Player):
    Environment.PrintEvent( "title","The ceiling beam suddenly buckles. Make a Speed (-1) check. If you pass, move to the street. If you fail, lose 2 Stamina.")
    result = Environment.SkillCheck("Speed",Player,1,-1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have escaped peril and returned to the street.")
        Environment.Teleport(Player,Player.Location.Connections[0])
    else:
        Environment.PrintEvent("Encounter","Failed! You get bonked on the head and lose 2 stamina.")
        Player.ModHealth(-2)

#draw 2 common items
#luck(-1) 
#fail: arrested, go to police station
def RiverDocks1(Environment,Player):
    Environment.PrintEvent( "title","You open some crates on the dock. Inside you find some useful things. Draw 2 Common Items. Next, make a Luck (-1) check. If you pass, you get away without being seen. If you fail, you are arrested and taken to the Police Station.")
    Player.AddItem(Environment.DeckDictionary["Common"].DrawCard(Player,"none")) 
    Player.AddItem(Environment.DeckDictionary["Common"].DrawCard(Player,"none"))
    result = Environment.SkillCheck("Luck",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You get away without being seen.")
    else:
        Environment.PrintEvent("Encounter","Failed! You have been caught by the police and arrested.")
        Environment.Teleport(Player,Environment.Locations["Police Station"])
        Player.Status["Delayed"] = 1
    

#speed(-1)
#fail: -1 sanitiy
#
def RiverDocks2(Environment,Player):
    Environment.PrintEvent( "title","You notice a piece of wood floating in the water; carved into it is the name of a ship long since sunk. As you touch it, visions of the drowning passengers' last moments of life flood through your mind. Pass a Speed (-1) check to hurl it away from you. If you fail, you fall to the ground with a cry. Lose 1 Sanity.")
    result = Environment.SkillCheck("Speed",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! No harm was inflicted.")
    else:
        Environment.PrintEvent("Encounter","Failed! You lose 1 sanity.")
        Player.ModSanity(-1)
#luck(-1)
#pass: draw 1 spell
#
def RiverDocks3(Environment,Player):
    Environment.PrintEvent( "title","You bump into Abner Weems, the local drunk. You help him find a place to sleep for the night, and he mumbles something to you over and over. Make a Luck (-1) check. If you pass, his mumbling is a magical chant. Draw 1 Spell. If you fail, it's gibberish. Nothing happens.")
    result = Environment.SkillCheck("Luck",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You learn a new spell.")
        Player.AddItem(Environment.DeckDictionary["Spell"].DrawCard(Player,"none")) 
    else:
        Environment.PrintEvent("Encounter","Failed! Nothing happens.")

#will(+1)
#fail: LITAS
#
def RiverDocks4(Environment,Player):
    Environment.PrintEvent( "title","As you look out across the waves, you feel strangely compelled to throw yourself into the ocean's watery embrace. Pass a Will (+1) check or you are Lost in time and space.")
    result = Environment.SkillCheck("Will",Player,1,1)
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have resisted the urge.")

    else:
        Environment.PrintEvent("Encounter","Failed! You are lost in time and space.")
        Environment.Teleport(Player,Environment.Locations["Lost in Time and Space"])
#luck(-1)
#pass: 1 common item
#fail: -1 sanity -3stamina
def RiverDocks5(Environment,Player):
    Environment.PrintEvent( "title","Walking along the dock you see something floating in the water near the edge of the dock. You reach for it - make a Luck (-1) check. If you pass, you dredge up something useful. Draw 1 Common Item. If you fail, you pull to the surface the tentacle that immediately wraps around your neck and drags you under the water and out to sea. Lose 1 Sanity and 3 Stamina before you break free. ")
    result = Environment.SkillCheck("Luck",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You have recovered a common item.")
        Player.AddItem(Environment.DeckDictionary["Common"].DrawCard(Player,"none")) 
    else:
        Environment.PrintEvent("Encounter","Failed! You picked up the tentacle of a monster and lose 1 sanity and 3 stamina in the struggle.")
        Player.ModHealth(-3)
        Player.ModSanity(-1)
    
#fight(+0)
#+$3 for every success
#fail: -1 stam, move to street
def RiverDocks6(Environment,Player):
    Environment.PrintEvent( "title","The dock workers are short-handed and offer you a job as a stevedore for the day. Make a Fight (+0) check. If you pass, gain $3 for every success you rolled. If you fail, the boss gets tired of your lollygagging and throws you out. Lose 1 Stamina and move to the street.")
    if Environment.Choose("Encounter","Accept the Job?","Yes","No", " ") == "Yes":
        result = Environment.SuccessCheck("Fight",Player,0,0)
        if result == 0:
            Environment.PrintEvent("Encounter","Failed! You were fired and thrown out. Lose 1 stamina and move to the streets.")
            Environment.Teleport(Player,Player.Location.Connections[0])
            Player.ModHealth(-1)
        else:
            Environment.PrintEvent("Encounter","Success! You worked hard and were payed $"+str(3*result))
            Player.Money += 3* result
            
        
            

#will(-1) check
#pass: -1 sanity
#fail, -2 sanity
# if not insane draw 1 unique
def RiverDocks7(Environment,Player):
    Environment.PrintEvent( "title","A horrific stench draws your attention to the body of some bizarre marine creature, rotting on the edge of the docks. As you move towards it, an uneasy feeling grows in the pit of your stomach, as though you are meddling with something best left alone. Make a Will (-1) check. If you pass, lose 1 Sanity. If you fail, lose 2 Sanity. In either event, if you are not reduced to 0 Sanity, you find something clutched in its webbed hands. Draw 1 Unique Item.")
    result = Environment.SkillCheck("Will",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You hold yourself together and only lose 1 sanity.")
        Player.ModSanity(-1)
    else:
        Environment.PrintEvent("Encounter","Failed! You lose 2 sanity.")
        Player.ModSanity(-2)
    if Player.Location.Name == "River Docks":
        Environment.PrintEvent("Encounter","You retrieve the unique item from the grasp of the monsterous corpse.")
        Player.AddItem(Environment.DeckDictionary["Unique"].DrawCard(Player,"none")) 
        
#Sneak(-1)
#pass: take ally John Legrasse, otherwise stam and sanity fully restored
#
def Unvisited1(Environment,Player):
    Environment.PrintEvent( "title","You come across a man examining some old bones. Pass a Sneak (-1) check to get close enough to see what he's doing. He finally notices you and is impressed with your skills, introducing himself as John Legrasse. Take his Ally card if it's available, otherwise he shares a meal with you. Restore your Sanity and Stamina to their maximum value.")
    result = Environment.SkillCheck("Sneak",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You gain John Legrasse as an ally.")
        allydraw = Environment.DeckDictionary["Ally"].DrawCard(Player,"John Legrasse")
        if allydraw[0] == "No cards to draw":
            Environment.PrintEvent("Encounter","Success! However, John Legrasse is unavailable and restores your health and sanity instead.")
            Player.ModHealth(100)
            Player.ModSanity(100)
        else:
            Player.AddItem( allydraw )
    else:
        Environment.PrintEvent("Encounter","Failed! Nothing happens.")
        

#will(-2)
#fail: -3 sanity
#
def Unvisited2(Environment,Player):
    Environment.PrintEvent( "title","The willows sway in a wind that you cannot hear or feel, and for a moment, the hatred of these ancient trees for the invader who has come to their island drives you to your knees. Pass a Will (-2) check or lose 3 Sanity.")
    result = Environment.SkillCheck("Will",Player,1,-2)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You resist the supernatural force, nothing happens.")
    else:
        Environment.PrintEvent("Encounter","Failed! You lose 3 sanity as the maddening supernatural force assaults your psyche.")
        Player.ModSanity(-3)
#
#-1 sanity , draw 1 spell
#
def Unvisited3(Environment,Player):
    Environment.PrintEvent( "title","You come across a large pile of human bones under the boughs of one of the willows on the isle. Lose 1 Sanity, but find a scroll among the bones. Draw 1 Spell.")
    Player.ModSanity(-1)
    if Player.Location.Name == "Unvisited Isle":
        Player.AddItem(Environment.DeckDictionary["Spell"].DrawCard(Player,"none"))
        
#
#-1 sanity +1 clue
#
def Unvisited4(Environment,Player):
    Environment.PrintEvent( "title","Looking up at the night sky from the island, you see constellations that you've never seen before. The entire sky is different here! Lose 1 Sanity and gain 1 Clue Token.")
    Player.ModSanity(-1)
    if Player.Location.Name == "Unvisited Isle":
        Player.Clues += 1
#
#sneak(-1)
#pass: +2 clue
def Unvisited5(Environment,Player):
    Environment.PrintEvent( "title","A group of hooded Cultists are having a meeting among the standing stones on the island. Pass a Sneak (-1) check to overhear some of what they have to say. Gain 2 Clue Tokens.  ")
    result = Environment.SkillCheck("Sneak",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You overhear valuable information and gain 2 clues.")
        Player.Clues += 2
    else:
        Environment.PrintEvent("Encounter","Failed! You cannot get close enough to overhear their conversation.")

#-1 stam and will(-1)
#fail: -1 sanity
#
def Unvisited6(Environment,Player):
    Environment.PrintEvent( "title","A silent man brushes past you on the trail. Your arm goes numb with cold from the brief contact, and you whirl around to look at him, but he has disappeared. Lose 1 Stamina and pass a Will (-1) check or lose 1 Sanity as well.")
    Player.ModHealth(-1)
    if Player.Location.Name != "Unvisited Isle":
        return
    result = Environment.SkillCheck("Will",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You hold yourself together.")
    else:
        Environment.PrintEvent("Encounter","Failed! Your mind is running a mile a minute, lose 1 sanity.")
        Player.ModSanity(-1)

#will(-1)
#fail: cursed
#
def Unvisited7(Environment,Player):
    Environment.PrintEvent( "title","As you start to climb back into your canoe and row to shore, you see a huge, shadowy shape disturb the water near the island. Waves of intense dread grip you, and you must pass a Will (-1) check or be Cursed.")
    result = Environment.SkillCheck("Will",Player,1,-1)    
    if result == "Pass":
        Environment.PrintEvent("Encounter","Success! You hold yourself together.")
    else:
        Environment.PrintEvent("Encounter","Failed! You have been cursed.")
        Player.Curse()

#################################################
#Miskatonic University

#choose: will(-2)
#pass: +$8
#fail: arrested -> Police station
def Administration1(Environment,Player):
    Environment.PrintEvent( "title","A student mistakes you for the bursar. If you want to carry on the deception, make a Will (-2) check. If you pass, gain $8 in ill-gotten tuition money. If you fail, you're arrested and taken to the Police Station.")

#Lore(-1)
#pass: $5
#
def Administration2(Environment,Player):
    Environment.PrintEvent( "title","Discuss the opportunity to sell a monograph with the President of the University. Pass a Lore (-1) check to make the sale and gain $5.")

#Lore(-1)
#pass: $5
#
def Administration3(Environment,Player):
    Environment.PrintEvent( "title","Discuss the opportunity to sell a monograph with the President of the University. Pass a Lore (-1) check to make the sale and gain $5.")


#will(-1)
#pass: retainer
#
def Administration4(Environment,Player):
    Environment.PrintEvent( "title","Pass a Will (-1) check to get the Dean to offer you a retainer to write a manuscript for the college. Gain a Retainer card.")

#
#+1 clue
#
def Administration5(Environment,Player):
    Environment.PrintEvent( "title","The Dean introduces you to an anthropology professor who gives you some insight into your investigation. Gain 1 Clue token.")

#choose: Lore(-2)
#pass: draw 1 spell
#fail: cursed
def Administration6(Environment,Player):
    Environment.PrintEvent( "title","You may choose to help an anthropology professor and his students decipher an ancient stone tablet. If so, make a Lore (-2) check. If you pass, you correctly interpret it, draw 1 Spell. If you fail, you mispronounce a word and are Cursed.")

#
#Move to arkham asylum and have encounter there
#
def Administration7(Environment,Player):
    Environment.PrintEvent( "title","Your discussions on the Mythos lead campus security to conclude that you are off your rocker, and they escort you off campus. Move to Arkham Asylum and immediately have an encounter there.")

#
#-1 sanity
#
def Library1(Environment,Player):
    Environment.PrintEvent( "title","A book in a shadowy corner of the library begins to whisper terrible things to you. Lose 1 Sanity.")

#will(+0) successes
#0) move to street
#1) draw 2 spells discard one
#2+) draw 1 unique
#
def Library2(Environment,Player):
    Environment.PrintEvent( "title","Make a Will (+0) check and consult the chart below:\n Successes:\n 0) Abigail tosses you out. Move to the street.\n 1) Abigail lets you into a private section of the library where you find an ancient tome. Draw 2 Spells and keep whichever one of them you want.\n 2+) Abigail loans you one of the strange items in the library's display case. Draw 1 Unique Item.")
#
#pay $4 or move to street
#
def Library3(Environment,Player):
    Environment.PrintEvent( "title","Overdue book fines of $4. Pay up, or move to the street! ")
#Luck(-2)
#pass: $5
#
def Library4(Environment,Player):
    Environment.PrintEvent( "title","Pass a Luck (-2) check to find $5 someone was using as a bookmark.")
#
#Teleport to dreamlands, do encounter
#then teleport back
def Library5(Environment,Player):
    Environment.PrintEvent( "title","You doze off and enter the Dreamlands. Have an encounter there, then immediately return here.")
#Lore(-2)
#pass: roll die and get that many clues
#fail: -2 stam and sanity
def Library6(Environment,Player):
    Environment.PrintEvent( "title","You find an unusual book that radiates evil at the touch. You begin to read and are drawn to it. Make a Lore (-2) check. If you pass, you obtain vast knowledge of the eldritch threat. Roll a die and gain that many Clue tokens. If you fail, the book consumes you-- mind and soul-- lose 2 Sanity and 2 Stamina.")
#Will(-1) check
#pass: Take first tome from unique
#fail: move to street
def Library7(Environment,Player):
    Environment.PrintEvent( "title","You look up to see Abigail Foreman leaning over you with hands on hips and a frustrated look on her face. Make a Will (-1) check. If you pass, she helps you find the book you were looking for. Take the first Tome from the Unique Item deck. If you fail, you've made too much noise. She escorts you out of the Library. Move to the street.	")
#choose: luck(+0)
#pass: roll die and get sanity or stam equal to the roll
#fail: +1 stam
def ScienceBuilding1(Environment,Player):
    Environment.PrintEvent( "title","A chemical brew bubbles on a nearby Bunsen burner. It smells delicious. If you drink it, make a Luck (+0) check. If you pass, the strange liquid fortifies you. Roll a die and gain that many points, split between your Stamina and Sanity however you like. If you fail, the liquid turns out to be coffee. Gain 1 Stamina.")


#Luck(-1)
#pass: CHOOSE NEW INVESTIGATOR (Keep all variables)
#
def ScienceBuilding2(Environment,Player):
    Environment.PrintEvent( "title","A professor of the occult asks you to hold a hideous statue that he believes to have strange powers while he reads a scroll. Energy shoots through your body. Make a Luck (-1) check. If you pass, your spirit rises from your body and you feel that you have the power to switch bodies with another investigator. You may choose another investigator from the pile of unused investigators and bring it into play as a new character, discarding your current investigator (along with all of his items, skills, trophies, etc.). If you fail, nothing happens.")


#if less than 2 spells :
#choose: gain 1 unique and move to street
#if >2 spells: nothing
def ScienceBuilding3(Environment,Player):
    Environment.PrintEvent( "title","An archaeology professor shows you an item he recovered in an Egyptian pyramid. If you have 2 or fewer Spells, it glows in your hands and you find yourself outside, still holding it. Not wanting to confront the professor again, you decide to keep it. Gain 1 Unique Item and move to the street. If you have more than 2 Spells, nothing happens.")


#
#Blessed (or get rid of curse)
#
def ScienceBuilding4(Environment,Player):
    Environment.PrintEvent( "title","As you enter the Department of Alchemy, a professor looks up in horror. He grabs an ancient artifact from a locked drawer in his desk and holds it up before your face, chanting and making symbolic motions with the item. If you areCursed, discard the Curse. If you are not Cursed, then you are Blessed.")


#Draw 1 spell
#fight(-1)
#fail: lose 1 of your choice items
def ScienceBuilding5(Environment,Player):
    Environment.PrintEvent( "title","Assisting a professor in his research, you find a valuable Spell. Draw 1 Spell. However, you must make a Fight (-1) check or some sticky-fingered student steals one of your items. Lose 1 Item of your choice.")


# choose: yes = -2 stam
# if not knocked out: ally joins you Sir William Brinton
#if not avail: +$5
def ScienceBuilding6(Environment,Player):
    Environment.PrintEvent( "title","You find a muscular, bored-looking man who challenges you to an arm wrestling match. Lose 2 Stamina if you accept. If this does not knock you unconscious, Sir William Brinton laughs and slaps your shoulder, offering to join your investigation. Take his Ally card. If it is not available, gain $5 instead.")


#choose: lore(-2)
#pass: for every gate open, roll die, if success close and return to deck
#fail: roll die and lose that many stam, then move to hospital
def ScienceBuilding7(Environment,Player):
    Environment.PrintEvent( "title","You find a student pounding on a strange device that he has hooked up to massive machinery. He states that it is a dimensional beam machine. If you offer to help him, make a Lore (-2) check. If you pass, beams shoot out in all directions, disrupting the gates open throughout the board. Roll a die for each open gate one at a time. On a success the gate is closed. However, you may not take it as a trophy, but instead return it to the pile of gate markers. If you fail, the machinery overheats and explodes. Roll a die and lose that much Stamina, then move to St. Mary's Hospital.")


##############################################################
#Northside

#Turn over 3 common items and unique item
#Any player in location can attempt to buy, however you choose
#all not sold are discarded
def CuriositieShoppe1(Environment,Player):
    Environment.PrintEvent( "title","A sale takes place. All players may participate. Turn over the top 3 Common Item cards and the top Unique Item card. Any player may buy one or more of these cards for their list price. If there is a disagreement over who gets to buy a certain card, you decide. Any items not sold are discarded.")
#speed(-1)
#fail: draw mythos card, go to where the gate should open, then have encounter there.
#
def CuriositieShoppe2(Environment,Player):
    Environment.PrintEvent( "title","As you wander into the back of the shop, you hear a noise. Pass a Speed (-1) check or you look up just in time to see a descending club. Everything goes black. When you awaken, you are somewhere else. Draw a mythos card and move to the gate location shown on it, then immediately have an encounter there. ")

#fight(-1)
#fail: go to abyss, have encounter, then return here
#
def CuriositieShoppe3(Environment,Player):
    Environment.PrintEvent( "title","A pulsing void gapes behind a bookshelf, sending out waves of heat. Pass a Fight (-1) check or it sucks you in, hurling you into the Abyss. Have one encounter there, then immediately return.")

#Search either common or unique item deck for any item
#then buy it at list price
#
def CuriositieShoppe4(Environment,Player):
    Environment.PrintEvent( "title","Jackpot! You find just what you've been looking for. Search either the Common or Unique Item deck and purchase any one item of your choice at list price.")

#luck(-1) or you drop an item of your choice
#if you have no items draw another encounter
#
def CuriositieShoppe5(Environment,Player):
    Environment.PrintEvent( "title","Pass a Luck (-1) check or you accidentally drop an item. Discard 1 item of your choice. If you have no items to drop, then draw again for a different encounter.")

#Luck(-2)
#fail: cursed
#
def CuriositieShoppe6(Environment,Player):
    Environment.PrintEvent( "title","You examine an obscene statue. Pass a Luck (-2) check or else you feel a cold dread spread through your body as you hold it. You are Cursed.")

#luck(-1)
#pass: look at top of common and unique. purchase any at list price
#fail: look at top of common and can purchase it
def CuriositieShoppe7(Environment,Player):
    Environment.PrintEvent( "title","You weed through piles of junk looking for something useful. Make a Luck (-1) check to see what you find. If you pass, your search has resulted in success. You may look at the top cards of both the Common and Unique Item decks. You may purchase one, both, or neither at list price. If you fail, there is little of interest here, but you may look at the top card of the Common Item deck and purchase it for its list price.")


#
#+$5
#
def Newspaper1(Environment,Player):
    Environment.PrintEvent( "title","Earn $5 for a story.")

#
#+retainer
#
def Newspaper2(Environment,Player):
    Environment.PrintEvent( "title","Editor Doyle Jefferies offers you a Retainer in return for your fascinating stories. Take a Retainer card.")


#
#+retainer
#
def Newspaper3(Environment,Player):
    Environment.PrintEvent( "title","Editor Doyle Jefferies offers you a Retainer in return for your fascinating stories. Take a Retainer card.")


#lore(-1)
#pass: 3 clues
#
def Newspaper4(Environment,Player):
    Environment.PrintEvent( "title","Flipping through the early edition, you are surprised to see that one of the classified ads begins with your name. Reading it, you realize that it contains several coded clues to the nature of the threat that faces Arkham. Pass a Lore (-1) check to gain 3 Clue tokens.")


#
#- 1 sanity
#
def Newspaper5(Environment,Player):
    Environment.PrintEvent( "title","You accidentally tip over a bottle of ink and are aghast at the patter the ink forms on the newsroom floor. Lose 1 Sanity.")


#
#Gain $2 and move anywhere in arkham
#if location encounter there
def Newspaper6(Environment,Player):
    Environment.PrintEvent( "title","You earn a hefty fee for a story and get a ride with Doyle Jefferies, the editior. Gain $2 and move to any location or street area in Arkham. If you move to a location, immediately have an encounter there.")


#luck(-1)
#pass: 1 clue
#
def Newspaper7(Environment,Player):
    Environment.PrintEvent( "title","Pass a Luck (-1) check to find an article that a local citizen told you would shed light on the recent strange activities. Gain 1 Clue token.")


#luck(-1)
#pass: draw 1 unique
#fail: roll die and lose that many stamina
def TrainStation1(Environment,Player):
    Environment.PrintEvent( "title","A stranger in a turban steps off the Boston local train with a crazed look on his face. Make a Luck (-1) check. If you pass, the man pulls a strange object from beneath his cloak and gives it to you. Draw 1 Unique Item. If you fail, he pulls a poisoned blade out of his cloak and stabs you. Roll a die and lose that much Stamina.")


#speed(-1)
#pass: gain 1 spell
#fail: roll die and lose that much sanity
def TrainStation2(Environment,Player):
    Environment.PrintEvent( "title","A well-dressed man is standing on the platform. He turns and greets you by name. Although he seems oddly familiar, you don't remember ever meeting him before. Then he steps off the platform into the path of a speeding train. Make a Speed (-1) check. If you pass, he vanishes as you leap right through him. On the ground, you find yourself clutching a scrap of paper. Gain 1 Spell. If you fail, he is obliterated before your eyes. Roll a die and lose that much Sanity.")


#
#move anywhere in arkham and have encounter there
#
def TrainStation3(Environment,Player):
    Environment.PrintEvent( "title","Bill Washington moves the last of the baggage from his cart onto a truck and offers you a ride as he opens the driver's door. If you accept, move to any location or street area in Arkham. If you move to a location, immediately have an encounter there.")


#draw top common item
#pay 1 over list price to keep it
#
def TrainStation4(Environment,Player):
    Environment.PrintEvent( "title","Joey the Rat is huddled in the shadows of the train station and motions for you to come over. He has an item for sale. Draw the top Common Item card and pay $1 more than list price if you wish to keep it.")


#sneak(-1)
#pass: draw 1 unique
#fail: arrested
def TrainStation5(Environment,Player):
    Environment.PrintEvent( "title","On the loading dock you investigate a large crate with strange markings. Make Sneak (-1) check. If you pass, you find a very unusual item in the crate. Gain 1 Unique Item. If you fail, Deputy Dingby catches you breaking it open. You are arrested and taken to the Police Station.")


#pay $3 for luck(-2)
#pass: unique
#fail: common
def TrainStation6(Environment,Player):
    Environment.PrintEvent( "title","Pay $3 at the Railroad Office to claim an item left in Lost and Found. If you do so, make a Luck (-2) check. If you pass, draw a Unique Item. If you fail, draw a Common Item.")


#Gain +2 points divided among stam/sanity
#
#
def TrainStation7(Environment,Player):
    Environment.PrintEvent( "title","The old train hand Bill Washington sits on the train platform playing his guitar as he awaits the next train. As you listen to his singing you feel yourself healing inside. Gain 2 points divided between Stamina and Sanity however you choose.")

##########################################################
#Rivertown

#
#A monster appears!	
#
def BlackCave1(Environment,Player):
    Environment.PrintEvent( "title","A monster appears!")
#speed(-1)
#fail: -1 stam
#
def BlackCave2(Environment,Player):
    Environment.PrintEvent( "title","Bats! Hundreds of them! Pass a Speed (-1) check to get out of the cave safely. If you fail, lose 1 Stamina.")
#luck(0) count successes
#0) lose 1 sanity, monster appears
#1) lose 1 sanity
#2+) draw 1 common item
#
def BlackCave3(Environment,Player):
    Environment.PrintEvent( "title","In the darkness you happen upon the remains of a previous spelunker. Make a Luck (+0) check and consult the chart below:\n Successes:\n 0) The body begins to bloat and splits open, releasing the horror within. Lose 1 Sanity and a monster appears!\n 1) The body has been ripped apart as if shredded by a powerful monster. Lose 1 Sanity.\n 2+) Searching the body you find something intersting. Draw 1 Common Item.")
#make luck(-2) or discard whiskey
#pass: Tom Mountain Murphy as ally (or if unavail take first weapon from common item)
#
def BlackCave4(Environment,Player):
    Environment.PrintEvent( "title","You are attacked by a shadowy being, but a large man leaps out of the darkness and drives it off. He introduces himself as Tom Mountain Murphy Make a Luck (-2) check, or discard a Whiskey card to pass it automatically. If you pass, he joins your investigation. Take his Ally card if it's available, otherwise he gives you something to protect yourself with. Search the Common Item deck and take the first Weapon you find. If you fail, nothing happens.")
#
# Lose 1 Sanity.
#
def BlackCave5(Environment,Player):
    Environment.PrintEvent( "title","The moaning winds in the cave whisper your name. Lose 1 Sanity.")
#lore(-2)
#fail: -1 stam and delayed
#
def BlackCave6(Environment,Player):
    Environment.PrintEvent( "title","You are in a maze of twisty passages, all alike. Pass a Lore (-2) check or become lost. If you fail, lose 1 Stamina and stay here next turn.")
#choose:Lore(0)
#0) -1 stam and sanity
#1) -1 sanity and +1 clue
#2+) spell book, take first tome from unique item deck
#
def BlackCave7(Environment,Player):
    Environment.PrintEvent( "title","You find an old book. If you read it, make a Lore (+0) check and consult the chart below:\n Successes:\n 0) Evil forces assault you. Lose 1 Sanity and 1 Stamina.\n 1) You find the diary of a lost soul who died in the caves long ago. Lose 1 Sanity and gain 1 Clue token as you read his horrible tale.\n 2+) The book is a spellbook. Take the first Tome from the Unique Item deck.")
#
#draw 1 common item
#
def GeneralStore1(Environment,Player):
    Environment.PrintEvent( "title","Hey, you dropped this! A young street urchin hands you an item and then scampers off. You don't recognize the item, but the boy is already gone. Draw 1 Common Item.")
#choose: pay $1
#lore(-2) check pass: +$5
#
def GeneralStore2(Environment,Player):
    Environment.PrintEvent( "title","A jar on the counter bears a sign proclaiming, Guess how many marbles are in the jar and win a prize! $1 entry fee. If you want, you may pay $1 to make a Lore (-2) check. If you pass, you gain $5. If you fail, nothing happens.	")
#Will(-2)
#pass: draw 3 commmon items, take 1 for free
#
def GeneralStore3(Environment,Player):
    Environment.PrintEvent( "title","Make a Will (-2) check. If you pass, you gain the ear of the shopkeeper. Seeing your valiant cause, he takes you into the back room and offers some special equipment. Draw 3 Common Items. You may take 1 of them for free as a gift help thwart the evil in Arkham! Discard the other 2. If you fail, nothing happens  ")
#
#+$1 
#
def GeneralStore4(Environment,Player):
    Environment.PrintEvent( "title","Noticing a glint on the floor, you discover a silver dollar someon must have dropped. Gain $1.")
#Choose:
#Sell any of your common items for twice listed price
#
def GeneralStore5(Environment,Player):
    Environment.PrintEvent( "title","The shopkeeper notices one of the items you're carrying and his face lights up. Say, Ive been looking for one of those. You wouldn't mind parting with it, would ya? I can pay well. You may sell any of your Common Items for twice its listed price.")
#
#-1 sanity
#
def GeneralStore6(Environment,Player):
    Environment.PrintEvent( "title","You notice that some of the locals have an odd, fish-like quality that sets your teeth on edge. The shopkeeper notices your gaze and nods. Marsh stock, from over in Innsmouth. Watch yourself around them. Shivering, you lose 1 Sanity.	")
#
#nothing happens
#
def GeneralStore7(Environment,Player):
    Environment.PrintEvent( "title","You try talking to the elderly locals gathered around the potbellied stove playing checkers, but you gain nothing but stares and few befuddled grunts for your trouble. Apparently they don't like outsiders. No encounter.")

#lore(-1)
#pass: 1 clue -1 sanity
#fail -1 sanity and move to street
def Graveyard1(Environment,Player):
    Environment.PrintEvent( "title","Testifying Cooter Falwell latches onto you and rambles on about his spiritual beliefs. Make a Lore (-1) check. If you pass, then somewhere in Cooter's words you find a clue to the Mythos threat. Gain 1 Clue token, but lose 1 Sanity. If you fail, move to the street while you listen to Cooter ramble on about pure nonsense.	")
#combat(-2) check
#pass: 1 clue 1 unique item
#fail: roll die and lose that much stam
def Graveyard2(Environment,Player):
    Environment.PrintEvent( "title","Descending into a dark mausoleum, you discover a vampire rising to feed. You quickly find yourself fighting for your life. Make a Combat (-2) check. If you pass, you defeat the vampire, gaining 1 Clue token and drawing 1 Unique Item. If you fail, roll a die and lose that much Stamina.")
#
#+2 sanity
#
def Graveyard3(Environment,Player):
    Environment.PrintEvent( "title","Entering a stone crypt, you are surprised to find a beautiful fresco and some inspirational words upon the wall. There is an almost magical peace within the chamber. Gain 2 Sanity.")
#luck(-2)
#pass:+ 2 clues and move to any arkham location and have an encounter
#
def Graveyard4(Environment,Player):
    Environment.PrintEvent( "title","Pass a Luck (-2) check to find a valuable clue within your tombstone rubbings. Gain 2 Clue tokens and you may move to any location or street area in Arkham. If you move to a location, immediately have an encounter there.")
#
#spend 5 monster toughness to take Richard upton pickman as an ally
#(if unavail draw 1 spell)
def Graveyard5(Environment,Player):
    Environment.PrintEvent( "title","You find a man painting a picture on one of the horrible gargoyles lining the walls of the graveyard. Seeing you, he introduces himself as Richard Upton Pickman, a painter visiting from Boston. If you spend monster trophies that have a total of 5 toughness, Pickman takes a liking to you. Take his Ally card. If it is not available, he teaches you an incantation instead. Draw 1 Spell.")
#
#a monster appears
#
def Graveyard6(Environment,Player):
    Environment.PrintEvent( "title","A monster appears!	")
#
#Take a monster as a trophy (even if endless)
#
def Graveyard7(Environment,Player):
    Environment.PrintEvent( "title","You find a half-buried corpse of a strange being. Draw a monster from the cup and take it as a monster trophy, even if it has the Endless ability.")

###############################################################
#Southside



#Luck(-1) [2] 
#pass: draw 1 skill, delay
#
def HistoricalSociety1(Environment,Player):
    Environment.PrintEvent( "title","Pass a Luck (-1) [2] check to gain insight into a skill while studying the old volumes of books. Draw 1 Skill, but stay here next turn.  ")

#choose: pay $3  or move to street
#if pay: luck(-1)
#pass: draw 1 spell
#fail: teleport to dreamlands, do encounter there, teleport back
def HistoricalSociety2(Environment,Player):
    Environment.PrintEvent( "title","Pay $3 fee to gain access to the private library. If you refuse, move to the street. If you pay, make a Luck (-1) check. If you pass, you learn an ancient spell from a dusty ledger. Draw 1 Spell. If you fail, you doze off and enter The Dreamlands. Have an encounter there, then immediately return here.")

#
# - 1 sanity
#
def HistoricalSociety3(Environment,Player):
    Environment.PrintEvent( "title","Perusing the county records, you discover something horrifying about your family tree. Lose 1 Sanity.")

#choose: go to woods and draw 2 encounters
#use one of them
#
def HistoricalSociety4(Environment,Player):
    Environment.PrintEvent( "title","The Society members are bird watching in the woods. The janitor offers you a ride there. If you accept, move to the Woods and draw 2 cards, encountering one card of your choice and discarding the other.")

#Spend 1 gate trophy.  Take Professor Armitage as ally (otherwise 1 unique item)
#
#
def HistoricalSociety5(Environment,Player):
    Environment.PrintEvent( "title","You encounter a friendly old professor from Miskatonic University. If you spend 1 gate trophy, he introduces himself as Professor Armitage and offers to join forces with you. Take his Ally card if it is available, otherwise draw 1 Unique Item.")

#choose: go to black cave and draw 2 encounters
#use one of them
#
def HistoricalSociety6(Environment,Player):
    Environment.PrintEvent( "title","You meet Cindy Fleming, a young geology professor at the University. She offers to show you some interesting formations at the Black Cave. If you accept, move to the Black Cave and draw 2 cards, encountering one card of your choice and discarding the other.")

#Sneak(-1)
#pass: nothing
#fail: -2 stam , move to street, cursed
def HistoricalSociety7(Environment,Player):
    Environment.PrintEvent( "title","You notice a creepy man watching you as you peruse the books. With a feeling of dread you try to slip out without being followed. Make a Sneak (-1) check. If you pass, you lose the man. If you fail, you are accosted in the street. He is a wizard and he casts a dark spell on you as you flee. Lose 2 Stamina, move to the street, and you are Cursed.")

#choose: will(+0)
#pass: draw 1 common or unique and purchase it for list
#
def BoardingHouse1(Environment,Player):
    Environment.PrintEvent( "title","After supper while sitting on the porch you strike up a conversation with another guest: Ryan Dean, a traveling salesman. You may make a Will (+0) check. If you pass, Ryan has a deal for you. You may draw either 1 Common Item or 1 Unique Item and purchase it at list price. If you fail, stay here next turn listening to bawdy stories and tall tales.")

#Luck(-1)
#fail: lose 1 sanity or stam
#
def BoardingHouse2(Environment,Player):
    Environment.PrintEvent( "title","Chanting neighbors keep you up all night. Pass a Luck (-1) check or lose your choice of 1 Stamina or 1 Sanity")

#
#Roll die and gain that much stam
#
def BoardingHouse3(Environment,Player):
    Environment.PrintEvent( "title","Ma Mathison serves her special soup at supper. Roll a die and gain that much Stamina.")

#
#pay $3 for 4pts added to stam/or/sanity
#
def BoardingHouse4(Environment,Player):
    Environment.PrintEvent( "title","Ma Mathison tells you that the best room on the house is available for the night. If you want, pay $3 to spend the night there. Gain 4 points split between Sanity and Stamina however you choose.")

#Luck(0)
#pass: go to dream lands, do encounter, then return
#fail: go to the abyss, do encounter, then return
def BoardingHouse5(Environment,Player):
    Environment.PrintEvent( "title","Staring at a painting in one of the rooms, you find yourself drawn into it. Make a Luck (+0) check. If you pass, move to The Dreamlands. Have one encounter there and immediately return here. If you fail, move to the Abyss. Have one encounter there and immediately return here.")

#
#draw 1 common item
#
def BoardingHouse6(Environment,Player):
    Environment.PrintEvent( "title","The last guest to stay in your room had to leave in a hurry and left something behind. Draw 1 Common Item.")

#Choose: Go to silver twilight lodge, draw 2 cards and encounter one of choice
#
#
def BoardingHouse7(Environment,Player):
    Environment.PrintEvent( "title","You find a poorly boarded-up passage in the basement that opens into a winding tunnel. If you venture into it, you exit in the Silver Twilight Lodge Draw 2 cards and encounter one card of your choice, discarding the other.")

#
#-1 sanity
#
def SouthChurch1(Environment,Player):
    Environment.PrintEvent( "title","You could swear a drain pipe gargoyle moved. Lose 1 Sanity")

#
#blessed
#
def SouthChurch2(Environment,Player):
    Environment.PrintEvent( "title","Knowing that you are engaged in God's work, Father Michael blesses you.")

#
#lose half money or half items
#
def SouthChurch3(Environment,Player):
    Environment.PrintEvent( "title","Father Michael convinces you that there are members of his congregation in greater need than you. Donate either half you money or half your items to the poor. (Both rounded up)")

#
#Draw holy water from unique
#
def SouthChurch4(Environment,Player):
    Environment.PrintEvent( "title","Noticing you eyeing the holy water, Father Michael tells you, Take what you need my child.  You may search the Unique Item deck for a holy Water card and take it.")

#Luck(0)
#0) -3 sanity move to street
#1) move to street
#2+) restore all sanity
def SouthChurch5(Environment,Player):
    Environment.PrintEvent( "title","You enter the confessional. Bless me Father, for I have sinned.  Make a Luck(+0) check and consult the chart below. \n Successes: \n 0) Father? are you there? You hear a scream in the next compartment! Lose 3 Sanity and move to the street. \n 1) Father? There is no answer. Sighing you leave. Move to the street. \n 2+) I dont remember my last confession. Raise your Sanity to its maximum value.")

#
#spend 1 clue to roll die , if success remove 1 doom
#
def SouthChurch6(Environment,Player):
    Environment.PrintEvent( "title","You join in the morning mass. Spend 1 Clue token to ask for heavenly aid. If you do so roll a die. On a success, your prayers are answered. Remove 1 doom token from the Ancient One's doom track.")

#Speed(-1)
#fail: -2 stamina
# move to street
def SouthChurch7(Environment,Player):
    Environment.PrintEvent( "title","Upon entering the church, you are attacked by Father Michael with a giant cross, who believes for some reason you to be in league with the devil. Make a Speed(-1) check. If you pass, you escape. If you fail, lose 2 Stamina. Either way move to the street.")

######################################

#luck(-1)
#pass: +$3 and +2 sanity
#fail: -2 sanity move to street
def Hospital1(Environment,Player):
    Environment.PrintEvent( "title","Make a Luck (-1) check. If you pass, you realize that Dr. Mortimore is sneaking up behind you with a hypodermic needle filled with a phosphorescent gel. You avoid his experiment and subdue the mad doctor. The city awards you $3 and you gain 2 Sanity in the process. If you fail, lose 2 Sanity, then you are dumped in the street. ")

#Sneak(-1)
#pass: draw 1 spell
#
def Hospital2(Environment,Player):
    Environment.PrintEvent( "title","Nurse Sharon slips something into your hand when the doctor isn't looking. Pass a Sneak (-1) check to keep anyone else from noticing. If you do, you later examine the object and find it to be an old parchment with a spell scratched on it. Draw 1 Spell. If you fail, an orderly takes it away from you and you gain nothing.")

#
#-1 clue
#
def Hospital3(Environment,Player):
    Environment.PrintEvent( "title","One of the staff physicians talks some sense into you. You are disabused of certain crazy but accurate notions. Lose 1 Clue token.")

#-1 sanity
#combat(-1)
#pass: +1 clue
#fail: move to street
def Hospital4(Environment,Player):
    Environment.PrintEvent( "title","The corpse you are examining isn't quite dead yet. It reaches out and grabs you by the throat. Lose 1 Sanity. Then, you must fight the corpse. If you pass a Combat (-1) check, you defeat it and gain 1 Clue token. Otherwise, move to the street.")

#Will(-1) or lose 1 sanity
#pass: draw 1 unique
#fail: go to street
def Hospital5(Environment,Player):
    Environment.PrintEvent( "title","The Doctor escorts you behind a curtain where the body of some other unfortunate investigator has been laid. The corpse has been torn to shreds. Pass a Will (-1) check or lose 1 Sanity. If you pass, you may also search the body and find a helpful item. Draw 1 Unique Item. If you fail, you run away screaming. Move to the street.")

#Roll a die
#1-3) gain that many stamina
#else nothing
def Hospital6(Environment,Player):
    Environment.PrintEvent( "title","You agree to undergo an experimental treatment. Roll a die. On a 1-3, gain that many Stamina. On a 4-6, nothing happens.")

#Lore(0)
#pass: 1 clue
#
def Hospital7(Environment,Player):
    Environment.PrintEvent( "title","You sneak a peek at the medical records for a recent admission who was involved in a cult ritual. Pass a Lore (+0) check to learn something about the cult's methods Gain 1 Clue token.")

#
#A gate and a monster appear!	
#
def Woods1(Environment,Player):
    Environment.PrintEvent( "title","A gate and a monster appear!	")

#Luck(-1)
#fail: lose 2 items and 2 stam
#
def Woods2(Environment,Player):
    Environment.PrintEvent( "title","You are bushwhacked by the Sheldon Gang. Pass a Luck (-1) check to avoid their trap. If you fail, lose 2 items of your choice and 2 Stamina.")

#Speed(-2) OR give him food item
#pass: take Duke as ally
#(unavail----+$3)
def Woods3(Environment,Player):
    Environment.PrintEvent( "title","You come across a cringing dog. Pass a Speed (-2) check to catch and calm him. If you have Food, you can discard that to automatically pass the check instead of rolling. You see by his collar that he is named Duke. Take his Ally card. If it isn't available, gain $3 as a reward for returning him to his owner, instead.")

#choose: Sneak(-2)
#pass: draw shotgun 
#fail: -2 stam , move to street
def Woods4(Environment,Player):
    Environment.PrintEvent( "title","You find a sleeping Sheldon Gang member near the still. Make a Sneak (-2) check to try to swipe the shotgun he has dropped on the ground. If you pass, take a Shotgun from the Common Item deck if there is one. If you fail, the guard awakens. You are caught and beaten, losing 2 Stamina, but you escape with your life. Move to the street. ")

#sneak(-1)
#fail: -2 stam
#move to street
def Woods5(Environment,Player):
    Environment.PrintEvent( "title","You have stumbled on a still owned by the Sheldon Gang. Make a Sneak (-1) check. If you pass, sKulk away without being seen. If you fail, lose 2 Stamina as the Sheldon Gang works you over while escorting you from the woods. In either case, move to the street.")

#Choose: Lore(-2)
#pass: draw 1 skill or 2 spells or 4 clues
#
def Woods6(Environment,Player):
    Environment.PrintEvent( "title","You meet an old wise man in the grove who offers to share his wisdom with you. If you accept, lose your next turn and make a Lore (-2) check. If you pass, you may draw 1 Skill, or draw 2 Spells, or gain 4 Clue tokens. If you fail, nothing happens.")

#lcuk(0)
#0: -1 san
#1) draw 1 common
#2) draw 1 unique
#3) +$10
def Woods7(Environment,Player):
    Environment.PrintEvent( "title","You trip over an object which turns out to be a rusty lockbox. If you open it, make a Luck (+0) check and consult the following chart:\n Successes: \n 0) A rotted human foot. Lose 1 Sanity. \n 1) Draw 1 Common Item. \n 2) Draw 1 Unique Item. \n 3+) $10 in jewelry.")

#
#nothing
#
def MagickShoppe1(Environment,Player):
    Environment.PrintEvent( "title","Looking into a glass ball, you receive a vision of things to come. Turn the top card of one location deck of your choice face up. The next investigator to have an encounter at that location draws that encounter card. ")
    
#
#-1 sanity
#
def MagickShoppe2(Environment,Player):
    Environment.PrintEvent( "title","Looking closely at a mummified head in the shop, you are horrified to find it looking back at you! Lose 1 Sanity.	")

#
#+1 clue
#
def MagickShoppe3(Environment,Player):
    Environment.PrintEvent( "title","Miriam Beecher talks to you for awhile, explaining some very interesting theories she has concerning the Mythos. Gain 1 Clue token.")

#
#move to street, -1 sanity
#
def MagickShoppe4(Environment,Player):
    Environment.PrintEvent( "title","Miriam Beecher, the shopkeeper, peers closely at your face, then screams, Theyve marked you! Get out! Get out! and throws you out. Move to the street and lose 1 Sanity from this unsettling incident.")

#lore(-1)
#pass: draw 1 unique and purchase for half (roundup)
#
def MagickShoppe5(Environment,Player):
    Environment.PrintEvent( "title","Pass a Lore (-1) check to recognize an item that Miriam Beecher has underpriced. If you do so, draw 1 Unique Item. You may purchase it for half its list price (rounded up).")

#choose: pay $5
#Luck(0)
#0) nothing
#1) roll 2 die -> add money equal to result 
#2+) draw 2 unique items
def MagickShoppe6(Environment,Player):
    Environment.PrintEvent( "title","There is an old, locked trunk for sale for $5. If you buy it, make a Luck (+0) check and consult the chart below:\n Successes: \n 0) Empty! \n  1) Gold coins! Roll 2 dice, add them together, and gain that much money. \n 2+) Jackpot! Draw 2 Unique Items!")

#
#Lore(-1)
#fail: cursed
def MagickShoppe7(Environment,Player):
    Environment.PrintEvent( "title","You see an interesting book sitting open on Miriam Beecher's desk. Pass a Lore (-1) check or you peer closely at its pages only to realize too late that the book is Cursed... and now, so are you.")










