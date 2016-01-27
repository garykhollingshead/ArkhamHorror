"""Class controlling dimensional gates in Arkham.  Update Class diagram 
with new methods.

By: Ben and Doug

4/22:
Zack- integrating gateclass, changed init's input.
"""

class Gate:
    def __init__(self, GateDeck):
        
	self.Location = None
	self.Destination = GateDeck["Location"]
	self.Difficulty = int(GateDeck["Modifier"])
	self.DimensionalShape = GateDeck["Symbol"]
	self.Name = "Gate"
	self.UniqueID = self.Name
	self.IsDiscovered = 0
	self.Explorers = []
	self.Picture = GateDeck["Picture"]
	self.FrontPicture = GateDeck["FrontPicture"]
	self.Type = "Gate"
    def DiscoverGate(self):
        self.IsDiscovered = 1
    def ExploredBy(self, Player):
        self.Explorers.append(Player)
    def RemoveExplorer(self,Player):
        if Player in self.Explorers :
            self.Explorers.remove(Player)
    def ChangeLocation(self, Location):
        self.Location = Location
    def EmptyExplored(self):
        self.Explorers = []
