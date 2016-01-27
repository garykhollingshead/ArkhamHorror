#Area[(location), (connected locations), (path taken to get there)]
import copy 

def MapSolver(start, goal, env):
#sets the goal and start locations
    Start = [start.Name, GetCons(start.Name, env), []]
    Goal = goal.Name
#+starts a list that contains the start
#+while the list isn't empty, go through it and keep expanding locations till we either run out of
#locations or find the goal
#+The first location gets popped off and checked to see if it is the goal
#if the current location popped off is the goal, we return the list of locations that we took to get there
#+here we are getting the list of all locations connected to the current one, we pop them off the list and 
#check to see if they are already in the current list. This prevents movements back and forth. if it isn't
#in the list, we push it on the end of the list of unexplored locations
    Fringe = []
    ILocation = 0
    IConnectedLocations = 1
    IVisitedPath = 2
    Fringe.append(Start)
    while (Fringe):
        Current = Fringe.pop(0)
        if (Current[ILocation] == Goal):
            Current[IVisitedPath].append(Current[ILocation])
            return Current[IVisitedPath]
        ConArea = Current[IConnectedLocations]
        while (ConArea):
            Temp = ConArea.pop(0)
            if not(Temp in Current[IVisitedPath]):
                TempList = copy.deepcopy(Current[IVisitedPath])
                TempList.append(Current[ILocation])
                Fringe.append([copy.copy(Temp), GetCons(Temp, env), copy.deepcopy(TempList)])
    return []
#if we make it to the end, we return an empty list to say that no path exists


def GetCons(con, env):
    cons = []
    loc = env.Locations[con]
    for cc in loc.Connections:
        cons.append(cc.Name)
    return cons
