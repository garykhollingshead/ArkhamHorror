"""Class Structure to deal with board locations
   When a location is called much of the information is passed to the 
constructor.
   Might need IsOutworld and IsStreet
 
By: Ben and Doug

zack:
Stabability, ElderSign are missing

Type can be: Arkham, Street, Otherworld, LITAS, Sky, Outskirts
zack: BREAKING NEWS
I opted to remove all the arguments for location's init
The problem arose from needing to create all locations before
connecting them.

Sorry if this broke some test that was mimicking the locations but it is now working in environment
and everything is set up regardless.
"""
import EventDialog

class Location:
    def __init__ (self):
        self.Name = ""
        self.Type = ""      #<---this is needed for knowing if its street/otherworld
        self.Stability = ""
        self.Neighborhood = ""
        self.ClueTokens = 0
        self.Expected = ""  #This is what kind of thing could be expected from events/etc
        self.Connections = list()
        self.WhiteStreet = None
        self.BlackStreet = None
        self.PlayerList = []
        self.MonsterList = []
        self.IsSealed = 0
        self.Gate = None
        self.ElderSign = 0
        self.FlavorText = ""
        self.OptionalEncounter = None
        self.MaxTerrorLevel = 0 
        self.IsClosed = 0
        self.DistanceFromActivePlayer = 100
        self.Type = "Location"
        """ self.MovementID = 1 """
    
    def AddClue(self):
        self.ClueTokens = self.ClueTokens + 1
    
    def RemoveClues(self):
        self.ClueTokens = 0

    def AddElderSign(self):
        if self.ElderSign == 1:
            return 1
        else:
            self.ElderSign = 1

    def RemoveElderSign(self):
        if self.ElderSign == 0:
            return 1
        else:
            self.ElderSign = 0

    def CollectClues(self, Player):
    
        Player.Clues = Player.Clues + self.ClueTokens
        if self.ClueTokens > 0:
            EventDialog.Run("Clues!",Player.Name+" has stumbled upon clues to the cause of disturbances in Arkham. Clues gained : "+str(self.ClueTokens))
        self.RemoveClues()
        
            
    def CalcDistanceFromPlayer(self, PlayerLoc):
        Path = self.CalcShortestPath(self, PlayerLoc)
        return len(Path)
    
    def AddMonster(self, Monster):
        try:
            Monster.Location.RemoveMonster(Monster)
        except (ValueError,AttributeError):
            print "no previous location"
        Monster.Location = self
        self.MonsterList.append(Monster)
        
    def RemoveMonster(self, Monster):
        try:
            self.MonsterList.remove(Monster)
        except (ValueError,AttributeError):
            print "no previous location"

    def AddPlayer(self, Player):
        try:
            Player.Location.RemovePlayer(Location)
        except (ValueError,AttributeError):
            print "no previous location"
        Player.Location = self
        self.PlayerList.append(Player)

    def RemovePlayer(self, Player):
        try:
            self.PlayerList.remove(Location)
        except (ValueError,AttributeError):
            print "no previous location"

        
    def AddGate(self, Gate):
        if self.Gate is not None :
            return 1
        try:
            Gate.Location.RemoveGate(Gate)
        except (ValueError,AttributeError):
            print "no previous location"    
        self.Gate = Gate
        Gate.Location = self
        self.RemoveClues()
        return 0

    def RemoveGate(self,Gate):
        if self.Gate is None :
            return 1
        self.Gate.Location = None
        self.Gate = None
        return 0
    
    def AddConnection(self, Location):
        if Location == self :
            return      #Disallow loops
        if Location not in self.Connections :
            self.Connections.append(Location)
        if self not in Location.Connections :
            Location.Connections.append(self)

    def RemoveConnection(self, Location):
        if(self.Connections.count(Location) != 0):
            self.Connections.remove(Location)
            Location.Connections.remove(self)
        return 0

    def NumberOfPlayers(self):
        len(self.PlayerList)

    def NumberOfMonsters(self):
        len(self.MonsterList)

    def IsInArkham(self):
        if self.Type == "Arkham" or self.Type == "Street" :
            return 1    #true
        else:
            return 0    #false

    def GetStability(self):
        for player in self.PlayerList:
            if(player.Name == "Kate Winthrop"):
                return "Stable"
        return self.Stability
