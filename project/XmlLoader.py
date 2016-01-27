"""
XmlLoader class
Written by: Aaron Phillips
Reads in XML from files

This class has methods that load in specific parts of the XML related to the game
After running a method, there will be a corresponding class property (eg self.Items or self.AncientOnes)
These properties are lists of dictionaries that contain the xml data
"""

import xml.dom.minidom as xmlLib
import os

class XmlLoader:
    
    def __init__(self):
         self.Investigators = []
         self.Items = []
         self.AncientOnes = []
         self.Monsters = []
         self.Locations = []
         self.Gates = []
         self.Skills = []
         self.Spells = []
         self.Encounters = dict() #{Downtown, EastTown, FrenchHill, MerchantDistrict, Miskatonicu, etc..}
         self.Mythos = []
         self.MapCoordinates = []

    """
     -this method loads in XML related to map coordinates
     -takes the mythos XML path as an argument
     -after completion, self.Encounters will be a list of dicts of the following form:
       {
         Name, Startpointx, Startpointy, BoxWidth,BoxHeight
       }
    """
    def LoadMapCoordinates(self, path):
        try:
            filepointer = open(path, 'r')
            alllines = filepointer.readlines()
        except:
            print "Error Loading Coordinates"
        for coord in alllines:
            mDict = dict()

            parts = coord.split(',')
            mDict["Name"] = parts[0]
            mDict["Startpointx"] = int(parts[1])
            mDict["Startpointy"] = int(parts[2])
            mDict["BoxWidth"] = int(parts[3])
            mDict["BoxHeight"] = int(parts[4])
            
            self.MapCoordinates.append(mDict)

    """
    -this method loads in XML related to Mythos
     -takes the mythos XML path as an argument
     -after completion, self.Encounters will be a list of dicts of the following form:
       {
         Name, Description, WhiteMovementShapes, BlackMovementShapes, Category, ClueAppears, MovementImage
         MonsterArea, CloseArea
       }
     -NOTE:not all of these keys will exist in every mythos card dictionary
    """
    def LoadMythos(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Mythos"
        for mythos in doc.getElementsByTagName("Mythos"):
            mDict = dict()

            #Name
            node = mythos.getElementsByTagName("name")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                mDict["Name"] = str(node.data.strip())

            #Description
            nodes = mythos.getElementsByTagName("description")
            if nodes.length > 0:
                node = mythos.getElementsByTagName("description")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    mDict["Description"] = node.data.strip()

            #white movement shapes
            nodes = mythos.getElementsByTagName("whiteMovementShapes")
            if nodes.length > 0:
                node = mythos.getElementsByTagName("whiteMovementShapes")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    mDict["WhiteMovementShapes"] = node.data.strip()

            #black movement shapes
            nodes = mythos.getElementsByTagName("blackMovementShapes")
            if nodes.length > 0:
                node = mythos.getElementsByTagName("blackMovementShapes")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    mDict["BlackMovementShapes"] = node.data.strip()

            #category
            nodes = mythos.getElementsByTagName("category")
            if nodes.length > 0:
                node = mythos.getElementsByTagName("category")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    mDict["Category"] = node.data.strip()

            #clueAppears
            nodes = mythos.getElementsByTagName("clueAppears")
            if nodes.length > 0:
                node = mythos.getElementsByTagName("clueAppears")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    mDict["ClueAppears"] = node.data.strip()

            #movementImage
            nodes = mythos.getElementsByTagName("movementImage")
            if nodes.length > 0:
                node = mythos.getElementsByTagName("movementImage")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    mDict["MovementImage"] = self.findImagePath("Mythos", node.data.strip())

            #monsterArea
            nodes = mythos.getElementsByTagName("monsterArea")
            if nodes.length > 0:
                node = mythos.getElementsByTagName("monsterArea")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    mDict["MonsterArea"] = node.data.strip()

            #closeArea
            nodes = mythos.getElementsByTagName("closeAreas")
            if nodes.length > 0:
                node = mythos.getElementsByTagName("closeAreas")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    mDict["CloseAreas"] = node.data.strip()


            self.Mythos.append(mDict)


    """
     -this method loads in XML related to Encounters
     -takes the src/data/Encounter directory (WITH '\\ or '/' ON THE END) as an arg
     -after completion, self.Encounters will be a list of dicts of the following form:
       {
         downtown, easttown, frenchhill, merchantdistrict, miskatonicu, northside, rivertown, uptown
       }
     - each entry in the dict is an array of dicts, each of which represents an encounter
       {
         Location, Text
       }
     - both of these are strings
    """
    def LoadEncounters(self, encounterFolder): #NOTE: NO XML PATH ARGS!!
        path = encounterFolder
        xmlPaths = []
        if(path[len(path)-1] == "\\"):
            currentOS = "windows"
            xmlPaths.append(path + "Downtown\\downtownencounters.xml")
            xmlPaths.append(path + "EastTown\\easttownenctounters.xml")
            xmlPaths.append(path + "FrenchHill\\frenchhillenctounters.xml")
            xmlPaths.append(path + "MerchantDistrict\\merchantdistrictenctounters.xml")
            xmlPaths.append(path + "Miskatonicu\\miskatonicuencounters.xml")
            xmlPaths.append(path + "Northside\\northsideencounters.xml")
            xmlPaths.append(path + "Rivertown\\rivertownencounters.xml")
            xmlPaths.append(path + "Uptown\\uptownencounters.xml")
        if(path[len(path)-1] == "/"):
            currentOS = "unix"
            xmlPaths.append(path + "Downtown/downtownencounters.xml")
            xmlPaths.append(path + "EastTown/easttownenctounters.xml")
            xmlPaths.append(path + "FrenchHill/frenchhillenctounters.xml")
            xmlPaths.append(path + "MerchantDistrict/merchantdistrictenctounters.xml")
            xmlPaths.append(path + "Miskatonicu/miskatonicuencounters.xml")
            xmlPaths.append(path + "Northside/northsideencounters.xml")
            xmlPaths.append(path + "Rivertown/rivertownencounters.xml")
            xmlPaths.append(path + "Uptown/uptownencounters.xml")


        for xmlPath in xmlPaths:
            listOfDicts = []
            try:
                filepointer = open(xmlPath, 'r')
                allxml = filepointer.read()
                doc = xmlLib.parseString(allxml)
            except:
                print "Error Loading Encounters"
            encounters = doc.firstChild.childNodes
            for encounter in encounters:
                if encounter.localName != None:
                    eDict = dict()
                    for encounterLocation in encounter.childNodes:
                        if encounterLocation.localName != None:
                            #name
                            eDict["Location"] = encounterLocation.localName
                            
                            #text
                            node = encounterLocation.getElementsByTagName("text")[0].firstChild
                            if node.nodeType == node.TEXT_NODE:
                                eDict["Text"] = str(node.data.strip())
                    
                    location = encounter.localName.lower().replace("encounter", "")
                    listOfDicts.append(eDict)

            self.Encounters[location] = listOfDicts


    """
     -this method loads in XML related to spells
     -takes a path to the XML file to load
     -after completion, self.Gates will be a list of dicts of the following form:
       {
         Picture, PostCast, Name, SanityCost, Effect, Amount, Hands, Phase, CastingModifier, Description
       }
    """
    def LoadSpells(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Spells"
            return
        for skill in doc.getElementsByTagName("Spell"):
            sDict = dict()

            #picture
            node = skill.getElementsByTagName("picture")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Picture"] = self.findImagePath("Spells", node.data.strip())

            #post cast action
            node = skill.getElementsByTagName("postCast")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["PostCast"] = node.data.strip()

            #name
            node = skill.getElementsByTagName("name")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Name"] = node.data.strip()

            #SanityCost
            node = skill.getElementsByTagName("sanityCost")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["SanityCost"] = node.data.strip()

            #effect
            node = skill.getElementsByTagName("effect")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Effect"] = node.data.strip()

            #amount
            node = skill.getElementsByTagName("amount")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Amount"] = int(node.data.strip())

            #hands
            node = skill.getElementsByTagName("hands")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Hands"] = int(node.data.strip())

            #phase
            node = skill.getElementsByTagName("phase")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Phase"] = node.data.strip()

            #castingModifier
            node = skill.getElementsByTagName("castingModifier")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["CastingModifier"] = node.data.strip()

            #description
            node = skill.getElementsByTagName("description")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Description"] = node.data.strip()

                
            self.Spells.append(sDict)

    """
     -this method loads in XML related to spells
     -takes a path to the XML file to load
     -after completion, self.Gates will be a list of dicts of the following form:
       {
         Picture, BackPicture, Name
       }
    """
    def LoadSkills(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Skills"
            return
        for skill in doc.getElementsByTagName("skill"):
            sDict = dict()

            #picture
            node = skill.getElementsByTagName("picture")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Picture"] = self.findImagePath("Skills", node.data.strip())

            #Back picture
            node = skill.getElementsByTagName("backpic")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["BackPicture"] = self.findImagePath("Skills", node.data.strip())

            #Name
            node = skill.getElementsByTagName("name")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                sDict["Name"] = node.data.strip()

            self.Skills.append(sDict)


    """
     -this method loads in XML related to gates
     -takes a path to the XML file to load
     -after completion, self.Gates will be a list of dicts of the following form:
       {
         Picture, Symbol, Modifier, Location, FrontPicture
       }
    """
    def LoadGates(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Gates"
            return
        for gate in doc.getElementsByTagName("otherworldGateMarker"):
            gDict = dict()

            #picture
            node = gate.getElementsByTagName("picture")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                gDict["Picture"] = self.findImagePath("Otherworld",node.data.strip())

            #symbol
            node = gate.getElementsByTagName("symbol")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                gDict["Symbol"] = node.data.strip()

            #modifier
            node = gate.getElementsByTagName("modifier")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                gDict["Modifier"] = node.data.strip()

            #location
            node = gate.getElementsByTagName("location")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                gDict["Location"] = node.data.strip()

            #front picture
            node = gate.getElementsByTagName("frontpicture")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                gDict["FrontPicture"] = node.data.strip()

            self.Gates.append(gDict)
                
            
            
    """
     -this method loads in XML related to locations
     -takes a path to the XML file to load
     -after completion, self.Locations will be a list of dicts of the following form:
       {
         name, neighborhood, location, stable, expected, decription,
        action, Map:{white, black, other}
       }
     -Map is a dictionary with up to three keys, white, black, and other
     -all other values in the dictionaries that make up self.Locations are strings
    """
    def LoadLocations(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Locations"
            return
        mapnode = doc.getElementsByTagName("Map")[0]
        for location in mapnode.childNodes:
            if location.localName != None:
                lDict = dict()
                
                #name (insert spaces)
                i = 0
                nospaces = location.localName
                spaces = ""
                for c in nospaces:
                    if i!= 0 and c.isupper():
                        spaces = spaces + ' ' + c
                    else:
                        spaces = spaces + c
                    i = i + 1
                spaces = spaces.strip()
                lDict["Name"] = str(spaces)

                #neighborhood
                node = location.getElementsByTagName("neighborhood")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    lDict["Neighborhood"] = node.data.strip()

                #location
                node = location.getElementsByTagName("location")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    lDict["Location"] = node.data.strip()

                #stable
                node = location.getElementsByTagName("stable")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    lDict["Stable"] = node.data.strip()


                #expected
                nodes = location.getElementsByTagName("expected")
                if nodes.length > 0:
                    node = location.getElementsByTagName("expected")[0].firstChild
                    if node != None and node.nodeType == node.TEXT_NODE:
                        lDict["Expected"] = node.data.strip()

                #description
                nodes = location.getElementsByTagName("description")
                if nodes.length > 0:
                    node = location.getElementsByTagName("description")[0].firstChild
                    if node != None and node.nodeType == node.TEXT_NODE:
                        lDict["Description"] = node.data.strip()

                #action
                nodes = location.getElementsByTagName("action")
                if nodes.length > 0:
                    node = location.getElementsByTagName("action")[0].firstChild
                    if node != None and node.nodeType == node.TEXT_NODE:
                        lDict["Action"] = node.data.strip()

                #map
                directionList = dict()
                dirs = location.getElementsByTagName("map")[0]
                #white
                nodes = dirs.getElementsByTagName("white")
                if nodes.length > 0:
                    node = location.getElementsByTagName("white")[0].firstChild
                    if node != None and node.nodeType == node.TEXT_NODE:
                        directionList["White"] = node.data.strip()
                #black
                nodes = dirs.getElementsByTagName("black")
                if nodes.length > 0:
                    node = location.getElementsByTagName("black")[0].firstChild
                    if node != None and node.nodeType == node.TEXT_NODE:
                        directionList["Black"] = node.data.strip()
                #other
                nodes = dirs.getElementsByTagName("other")
                if nodes.length > 0:
                    node = location.getElementsByTagName("other")[0].firstChild
                    if node != None and node.nodeType == node.TEXT_NODE:
                        directionList["Other"] = node.data.strip()
                lDict["Map"] = directionList
                    

                self.Locations.append(lDict)

    """            
     -this method loads in XML related to monsters
     -takes a path to the XML file to load
     -after completion, self.Monsters will be a list of dicts of the following form:
       {
         Picture, Toughness, Description, CombatDamage, Symbol, Name, Amount, CombatCheck,
         SanityDamage, SneakCheck, HorrorCheck, Movement, PhysicalResistance, Nightmarish,
         Overwhelming, MagicalResistance, Ambush, PhysicalImmunity, Undead, Endless, Mask, MagicalImmunity
       }
    """
    def LoadMonsters(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Monsters"
            return
        for monster in doc.getElementsByTagName("monster"):
            monsterDict = dict()

            #picture
            node = monster.getElementsByTagName("picture")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                monsterDict["Picture"] = self.findImagePath("Monster", node.data.strip())

            #toughness
            node = monster.getElementsByTagName("toughness")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                monsterDict["Toughness"] = int(node.data.strip())

            #description
            nodes = monster.getElementsByTagName("description")
            if nodes.length > 0:
                node = monster.getElementsByTagName("description")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["Description"] = str(node.data.strip())

            #combatDamage
            nodes = monster.getElementsByTagName("combatDamage")
            if nodes.length > 0:
                node = monster.getElementsByTagName("combatDamage")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["CombatDamage"] = node.data.strip()

            #symbol
            node = monster.getElementsByTagName("symbol")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                monsterDict["Symbol"] = node.data.strip()

            #name
            node = monster.getElementsByTagName("name")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                monsterDict["Name"] = node.data.strip()

            #amount
            node = monster.getElementsByTagName("amount")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                monsterDict["Amount"] = node.data.strip()

            #combatCheck
            nodes = monster.getElementsByTagName("combatCheck")
            if nodes.length > 0:
                node = monster.getElementsByTagName("combatCheck")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["CombatCheck"] = node.data.strip()

            #sanityDamage
            nodes = monster.getElementsByTagName("sanityDamage")
            if nodes.length > 0:
                node = monster.getElementsByTagName("sanityDamage")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["SanityDamage"] = node.data.strip()

            #sneakCheck
            nodes = monster.getElementsByTagName("sneakCheck")
            if nodes.length > 0:
                node = monster.getElementsByTagName("sneakCheck")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["SneakCheck"] = node.data.strip()

            #horrorCheck
            nodes = monster.getElementsByTagName("horrorCheck")
            if nodes.length > 0:
                node = monster.getElementsByTagName("horrorCheck")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["HorrorCheck"] = node.data.strip()

            #movement
            node = monster.getElementsByTagName("movement")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                monsterDict["Movement"] = node.data.strip()

            #physicalResistance
            nodes = monster.getElementsByTagName("physicalResistance")
            if nodes.length > 0:
                node = monster.getElementsByTagName("physicalResistance")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["PhysicalResistance"] = node.data.strip()

            #nightmarish
            nodes = monster.getElementsByTagName("nightmarish")
            if nodes.length > 0:
                node = monster.getElementsByTagName("nightmarish")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["Nightmarish"] = node.data.strip()

            #overwhelming
            nodes = monster.getElementsByTagName("overwhelming")
            if nodes.length > 0:
                node = monster.getElementsByTagName("overwhelming")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["Overwhelming"] = node.data.strip()

            #magicalResistance
            nodes = monster.getElementsByTagName("magicalResistance")
            if nodes.length > 0:
                node = monster.getElementsByTagName("magicalResistance")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["MagicalResistance"] = node.data.strip()

            #ambush
            nodes = monster.getElementsByTagName("ambush")
            if nodes.length > 0:
                node = monster.getElementsByTagName("amount")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["Ambush"] = node.data.strip()

            #physicalImmunity
            nodes = monster.getElementsByTagName("physicalImmunity")
            if nodes.length > 0:
                node = monster.getElementsByTagName("physicalImmunity")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["PhysicalImmunity"] = node.data.strip()

            #undead
            nodes = monster.getElementsByTagName("undead")
            if nodes.length > 0:
                node = monster.getElementsByTagName("undead")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["Undead"] = node.data.strip()

            #endless
            nodes = monster.getElementsByTagName("endless")
            if nodes.length > 0:
                node = monster.getElementsByTagName("endless")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["Endless"] = node.data.strip()

            #mask
            nodes = monster.getElementsByTagName("mask")
            if nodes.length > 0:
                node = monster.getElementsByTagName("mask")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["Mask"] = node.data.strip()

            #magicalImmunity
            nodes = monster.getElementsByTagName("magicalImmunity")
            if nodes.length > 0:
                node = monster.getElementsByTagName("magicalImmunity")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["MagicalImmunity"] = node.data.strip()

            #Special Attack Function
            nodes = monster.getElementsByTagName("attackfunction")
            if nodes.length > 0:
                node = monster.getElementsByTagName("attackfunction")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["AttackFunction"] = node.data.strip()

            
            #Special Move Function
            nodes = monster.getElementsByTagName("movefunction")
            if nodes.length > 0:
                node = monster.getElementsByTagName("movefunction")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["MoveFunction"] = node.data.strip()

            #After Horror Function
            nodes = monster.getElementsByTagName("afterhorror")
            if nodes.length > 0:
                node = monster.getElementsByTagName("afterhorror")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["AfterHorror"] = node.data.strip()

            #Before Horror Function
            nodes = monster.getElementsByTagName("beforehorror")
            if nodes.length > 0:
                node = monster.getElementsByTagName("beforehorror")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    monsterDict["BeforeHorror"] = node.data.strip()

            self.Monsters.append(monsterDict)
            
    """
     -this method loads in XML related to Ancient Ones
     -takes a path to the XML file to load
     -after completion, self.AncientOnes will be a list of dicts of the following form:
       {
         Picture, Name, Combat, Title, Attack, Defense, Doom
       }
    """
    def LoadAncientOnes(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Ancient Ones"
            return
        for ancientOne in doc.getElementsByTagName("AncientOne"):
            aOneDict = dict()

            #Picture
            node = ancientOne.getElementsByTagName("picture")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                aOneDict["Picture"] = self.findImagePath("AncientOnes", node.data.strip())

            #Name
            node = ancientOne.getElementsByTagName("name")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                aOneDict["Name"] = str(node.data.strip())

            #Combat
            node = ancientOne.getElementsByTagName("combat")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                aOneDict["Combat"] = int(node.data.strip())

            #Title
            node = ancientOne.getElementsByTagName("title")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                aOneDict["Title"] = str(node.data.strip())

            #Attack
            nodes = ancientOne.getElementsByTagName("attack")
            if nodes.length > 0:
                node = ancientOne.getElementsByTagName("attack")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    aOneDict["Attack"] = node.data.strip()
            #Awaken
            nodes = ancientOne.getElementsByTagName("awaken")
            if nodes.length > 0:
                node = ancientOne.getElementsByTagName("awaken")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    aOneDict["Awaken"] = node.data.strip()

            #Power
            nodes = ancientOne.getElementsByTagName("power")
            if nodes.length > 0:
                node = ancientOne.getElementsByTagName("power")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    aOneDict["Power"] = node.data.strip()
            #Worshippers
            nodes = ancientOne.getElementsByTagName("worshippers")
            if nodes.length > 0:
                node = ancientOne.getElementsByTagName("worshippers")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    aOneDict["Worshippers"] = node.data.strip()

            #Defense
            nodes = ancientOne.getElementsByTagName("defense")
            if nodes.length > 0:
                node = ancientOne.getElementsByTagName("defense")[0].firstChild
                if node != None and node.nodeType == node.TEXT_NODE:
                    aOneDict["Defense"] = str(node.data.strip())

            #Doom
            node = ancientOne.getElementsByTagName("doom")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                aOneDict["Doom"] = int(node.data.strip())



            self.AncientOnes.append(aOneDict)

    """        
     -this method loads in XML related to Items
     -takes a path to the XML file to load
     -after completion, self.Items will be a list of dicts of the following form:
       {
         Picture, Description, Price, Rarity, ItemType, Amount, Hands, Discard, Type, Name
       }
    """
    def LoadItems(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Items"
            return
        for item in doc.getElementsByTagName("Item"):
            itemdict = dict()

            #picture
            node = item.getElementsByTagName("picture")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                itemdict["Picture"] = self.findImagePath("Item", node.data.strip())

            #description
            node = item.getElementsByTagName("description")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                itemdict["Description"] = node.data.strip()

            #price
            node = item.getElementsByTagName("price")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                itemdict["Price"] = int(node.data.strip())

            #rarity
            node = item.getElementsByTagName("rarity")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                itemdict["Rarity"] = str(node.data.strip())

            #itemtype
            node = item.getElementsByTagName("itemtype")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                itemdict["Itemtype"] = str(node.data.strip())

            #amount
            node = item.getElementsByTagName("amount")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                itemdict["Amount"] = int(node.data.strip())

            #hands
            nodes = item.getElementsByTagName("hands")
            if nodes.length > 0:
                node = item.getElementsByTagName("hands")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    itemdict["Hands"] = str(node.data.strip())

            #discard
            nodes = item.getElementsByTagName("discard")
            if nodes.length > 0:
                node = item.getElementsByTagName("discard")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    itemdict["Discard"] = str(node.data.strip())

            #type
            node = item.getElementsByTagName("type")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                itemdict["Type"] = str(node.data.strip())

            #name
            node = item.getElementsByTagName("name")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                itemdict["Name"] = str(node.data.strip())

            #combatcheck
            #nodes = item.getElementsByTagName("combatcheck")
            #if nodes.length > 0:
                #node = item.getElementsByTagName("combatcheck")[0].firstChild
                #if node.nodeType == node.TEXT_NODE:
                    #itemdict["Combatcheck"] = int(node.data.strip())
                    #print itemdict["Combatcheck"]
            

            self.Items.append(itemdict)

    """
    This method will give Gary access to the item pictures for the item class
    Takes a string representing the item name
    returns the path of the image for the item
    """
    def GetItemImagePath(self, itemName):
        path = os.getcwd()
        length = len(os.getcwd())
        path = path[0:(length - 7)]
        xmlPaths = []
        if(path[len(path)-1] == "\\"):
            currentOS = "windows"
            path = path + "data\\Item\\items.xml"
        if(path[len(path)-1] == "/"):
            currentOS = "unix"
            path = path + "data/Item/items.xml"

        self.LoadItems(path)

        for item in self.Items:
            if item["Name"].lower() == itemName.lower():
                return str(item["Picture"])

        return ""

    """
     -this method loads in XML related to gates
     -takes a path to the XML file to load
     -after completion, self.Gates will be a list of dicts of the following form:
       {
         Stamina, Picture, Story, Name, Title, Fight, Skill, Spell, Unique, Common,
         Focus, Sneak, Sanity, Will, Lore, Speed, Luck, Home, Money, clue, ally, spell
       }
    """
    def LoadInvestigators(self, xmlPath):
        try:
            filepointer = open(xmlPath, 'r')
            allxml = filepointer.read()
            doc = xmlLib.parseString(allxml)
        except:
            print "Error Loading Investigators"
            return
        for investigator in doc.getElementsByTagName("Investigator"):
            inv = dict()

            #stamina
            node = investigator.getElementsByTagName("stamina")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Stamina"] = node.data.strip()
                inv["Stamina"] = int(inv["Stamina"])
                
            #picture
            node = investigator.getElementsByTagName("picture")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Picture"] = node.data.strip()
                inv["Picture"] = str(inv["Picture"])
                

            #story
            node = investigator.getElementsByTagName("story")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Story"] = node.data.strip()
                inv["Story"] = str(inv["Story"])
                                     
            #name
            node = investigator.getElementsByTagName("name")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Name"] = node.data.strip()
                inv["Name"] = str(inv["Name"])

            #title
            node = investigator.getElementsByTagName("title")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Title"] = node.data.strip()
                inv["Title"] = str(inv["Title"])

            #fight
            node = investigator.getElementsByTagName("fight")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Fight"] = node.data.strip()
                inv["Fight"] = int(inv["Fight"])

        #RANDOM 
            rdict = dict()
            random = investigator.getElementsByTagName("random")[0]
            #skill cards
            nodes = random.getElementsByTagName("skill")
            if nodes.length > 0:
                node = random.getElementsByTagName("skill")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    rdict["skill"] = node.data.strip()

            #spell cards
            nodes = random.getElementsByTagName("spell")
            if nodes.length > 0:
                node = random.getElementsByTagName("spell")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                   rdict["spell"] = node.data.strip()

            #unique cards
            nodes = random.getElementsByTagName("unique")
            if nodes.length > 0:
                node = random.getElementsByTagName("unique")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    rdict["unique"] = node.data.strip()

            #common cards
            nodes = random.getElementsByTagName("common")
            if nodes.length > 0:
                node = random.getElementsByTagName("common")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                     rdict["common"] = node.data.strip()
            inv["Random"] = rdict

         #SLIDER STATS

            #focus
            node = investigator.getElementsByTagName("focus")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Focus"] = node.data.strip()
                inv["Focus"] = int(inv["Focus"])

            #sneak
            node = investigator.getElementsByTagName("sneak")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Sneak"] = node.data.strip()
                inv["Sneak"] = int(inv["Sneak"])

            #sanity
            node = investigator.getElementsByTagName("sanity")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Sanity"] = node.data.strip()
                inv["Sanity"] = int(inv["Sanity"])

            #will
            node = investigator.getElementsByTagName("will")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Will"] = node.data.strip()
                inv["Will"] = int(inv["Will"])

            #lore
            node = investigator.getElementsByTagName("lore")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Lore"] = node.data.strip()
                inv["Lore"] = int(inv["Lore"])

            #speed
            node = investigator.getElementsByTagName("speed")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Speed"] = node.data.strip()
                inv["Speed"] = int(inv["Speed"])

            #luck
            node = investigator.getElementsByTagName("luck")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Luck"] = node.data.strip()
                inv["Luck"] = int(inv["Luck"])

            #home
            node = investigator.getElementsByTagName("home")[0].firstChild
            if node.nodeType == node.TEXT_NODE:
                inv["Home"] = node.data.strip()
                

        #FIXED 

            fixed = investigator.getElementsByTagName("fixed")[0]
            fdict = dict()

            fdict["money"] = 0
            fdict["clue"] = 0

            #money
            nodes = fixed.getElementsByTagName("money")
            if nodes.length > 0:
                node = fixed.getElementsByTagName("money")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    fdict["money"] = node.data.strip()
                    fdict["money"] = int(str(fdict["money"]))
                    


            #clue
            nodes = fixed.getElementsByTagName("clue")
            if nodes.length > 0:
                node = fixed.getElementsByTagName("clue")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    fdict["clue"] = node.data.strip()
                    fdict["clue"] = int(str(fdict["clue"]))

            #ally
            nodes = fixed.getElementsByTagName("ally")
            if nodes.length > 0:
                node = fixed.getElementsByTagName("ally")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    fdict["ally"] = node.data.strip()

            #spell
            nodes = fixed.getElementsByTagName("spell")
            if nodes.length > 0:
                node = fixed.getElementsByTagName("spell")[0].firstChild
                if node.nodeType == node.TEXT_NODE:
                    fdict["spell"] = node.data.strip()

            inv["Fixed"] = fdict

            self.Investigators.append(inv)
        
    """
    This method returns image paths, given a folder and file name
    """
    def findImagePath(self, folder, fileName):
        #\ needs to have two because the first one escapes
        #the second one "\n" is newline and "\\n" is "\n"

        

        ItemPath = os.getcwd()
        #ItemPath is current dir
        length = len(os.getcwd())
        ItemPath = ItemPath[0:(length - 7)]
        #cut off \\project

        #ItemPath is now the path but it's in the src folder

        if(ItemPath[len(ItemPath)-1] == "\\"):
            ItemPath = ItemPath + "data\\" + folder + "\\Images\\"
        if(ItemPath[len(ItemPath)-1] == "/"):
            ItemPath = ItemPath + "data/" + folder + "/Images/"

        #find out which way the slashes go, then add on whatever directories I want

        ItemPath = ItemPath + fileName

        #Add on the specific file name

        return ItemPath

    
