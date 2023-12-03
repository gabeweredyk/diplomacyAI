
from country import *
import sys
import random

def allArmiesAllFleets(players):
    allArmies = []
    allFleets = []
    for player in players:
        allArmies.append(player.armies)
        allFleets.append(player.fleets)
    return allArmies,allFleets

def armyInProvince(territory,allArmies):
    for army in allArmies:
        if army.location == territory:
            return True
    return False

def fleetInProvince(territory,allFleets):
    for fleet in allFleets:
        if fleet.location == territory:
            return True
    return False

def unitsInSupportingPositions(territory,paths,assignedCountry,players):
    vals = 0
    for neighbor in paths[territory]:
        if players[assignedCountry].fleetInProvince(neighbor) or players[assignedCountry].armyInProvince(neighbor):
            vals += 1
    return vals

def absDistBetweenTerritories(terA,paths,territories):
    unvisitedNodes = list(territories)
    shortestPath = dict()
    previousNodes = dict()
    maxVal = sys.maxsize
    for node in unvisitedNodes:
        shortestPath[node] = maxVal
    shortestPath[terA] = 0
    
    while unvisitedNodes:
        currentMinNode = None
        for node in unvisitedNodes:
            if currentMinNode == None:
                currentMinNode = node
            elif shortestPath[node] < shortestPath[currentMinNode]:
                currentMinNode = node

        neighbors = paths[currentMinNode]
        for neighbor in neighbors:
            tentativeVal = shortestPath[currentMinNode] + 1
            if tentativeVal < shortestPath[neighbor]:
                shortestPath[neighbor] = tentativeVal
                previousNodes[neighbor] = currentMinNode
        
        unvisitedNodes.remove(currentMinNode)

    return previousNodes, shortestPath

def shortestPath(terA,terB,previousNodes):
    path = []
    node = terB

    while node != terA:
        path.append(node)
        node = previousNodes[node]
    
    path.append(terA)
    path = path[::-1]

    return path

def armyDistBetweenTerritories(terA,paths,territories):
    validTers = dict()
    for ter in territories:
        if territories[ter]["type"] == "Coast" or territories[ter]["type"] == "Land":
            validTers[ter] = territories[ter]
    validPaths = dict()
    for path in paths:
        validNeighbors = []
        for neighbor in paths[path]:
            if territories[neighbor]["type"] == "Coast" or territories[neighbor]["type"] == "Land":
                validNeighbors.append(neighbor)
        validNeighbors = set(validNeighbors)
        validPaths[path] = validNeighbors
    previousNodes, shortestPath = absDistBetweenTerritories(terA,validPaths,validTers)
    return previousNodes, shortestPath

def fleetsDistBetweenTerritories(terA,paths,territories):
    validTers = dict()
    for ter in territories:
        if territories[ter]["type"] == "Coast" or territories[ter]["type"] == "Sea":
            validTers[ter] = territories[ter]
    validPaths = dict()
    for path in paths:
        validNeighbors = []
        for neighbor in paths[path]:
            if territories[neighbor]["type"] == "Coast" or territories[neighbor]["type"] == "Sea":
                validNeighbors.append(neighbor)
        validNeighbors = set(validNeighbors)
        validPaths[path] = validNeighbors
    previousNodes, shortestPath = absDistBetweenTerritories(terA,validPaths,validTers)
    return previousNodes, shortestPath

def provDanger(ter,paths,players):
    danger = 0.0
    for player in players.values():
        for neighbor in paths[ter]:
            if player.armyInProvince(neighbor) or player.fleetInProvince(neighbor):
                danger += 1.0 * player.trust
            for neighborNeighbor in paths[neighbor]:
                if player.armyInProvince(neighborNeighbor) or player.fleetInProvince(neighborNeighbor):
                    danger += 0.4 * 1/player.trust
    return danger

def immediateDanger(ter,paths,players):
    danger = 0.0
    for player in players.values():
        for neighbor in paths[ter]:
            if player.armyInProvince(neighbor) or player.fleetInProvince(neighbor):
                danger += 1.0 * 1/player.trust
    return danger

def factorial(n):
    if n == 0: return 1
    return factorial(n - 1) * n

def getRandomMove(mu, N):
    distribution = []
    r = 0.4
    for i in range(N):
        distribution.append(  r ** abs(i - mu)  )
    x = random.choices(range(N), distribution, k=1)[0]
    return x

def analyzeMovesInitial(players,assignedCountry,territories,paths):
    otherPlayers = dict()
    for player in players:
        if player != assignedCountry:
            otherPlayers[player] = players[player]
    
    unconsideredUnits = players[assignedCountry].armies + players[assignedCountry].fleets
    moves = []
    while unconsideredUnits:
        targets = []
        # find nearest valuable province for each unit
        
        for unit in unconsideredUnits:
            nearestValProv = unit.loc

            # finds the distance from the unit to all territories on the
            if unit.type == "a":
                previousNodes, distToAll = armyDistBetweenTerritories(unit.loc,paths,territories)
            if unit.type == "f":
                previousNodes, distToAll = fleetsDistBetweenTerritories(unit.loc,paths,territories)

            # creates a list of 2-tuples of the evaluation score and the name of each province that it could move
            dists = []
            for dist in distToAll:
                if distToAll[dist] != 0:
                    evaluation = territories[dist]["score"] / (distToAll[dist] ** 2)
                    x = (evaluation,dist) # 2-tuple with movementEval,provinceName
                    dists.append(x)

            # sorts that by the evaluation score
            dists.sort(reverse=True)

            # goes through that list, chooses the first where the next step along the path isn't occupied by another unit as its target
            for prelimTarget in dists:
                prelimTarget = prelimTarget[1]
                pathTo = shortestPath(unit.loc,prelimTarget,previousNodes)
                if not players[assignedCountry].unitInProvince(pathTo[1]):
                    nearestValProv = prelimTarget
                    break
            pathToTarget = shortestPath(unit.loc,nearestValProv,previousNodes)
            target = (distToAll[nearestValProv],pathToTarget,nearestValProv,unit)
            targets.append(target)

        # narrow down to nearest target and finds the value of the movement
        targets.sort()
        print(targets)
        target = targets[getRandomMove(1, len(targets))]
        pathToTarget = target[1]
        moveVal = territories[target[2]]["score"]/(target[0] ** 2)
        prelimMove = {"type":"Move","terr":[pathToTarget[0],pathToTarget[1]]}

        # calculate current province danger for the unit that might move and consider if it should hold instead of moving
        currentDanger = immediateDanger(target[-1].loc,paths,otherPlayers)
        holdVal = currentDanger*100
        prelimHold = {"type":"Hold","terr":[target[-1].loc]}
        if territories[target[-1].loc]["owner"] != assignedCountry and territories[target[-1].loc]["supply"]:
            holdVal = sys.maxsize

        # calculate province danger + allocate support units
        if moveVal > holdVal:
            nextStepDanger = immediateDanger(pathToTarget[1],paths,otherPlayers)
            finalStepDanger = provDanger(pathToTarget[-1],paths,otherPlayers)
            if nextStepDanger > 0.9:
                for unit in unconsideredUnits:
                    if unit.inSupportingLoc(pathToTarget[1],paths,territories) and unit.loc != pathToTarget[0]:
                        support = {"type":"Support","terr":[[unit.loc,pathToTarget[0],pathToTarget[1]]]}
                        moves.append(support)
                        unconsideredUnits.remove(unit)
                        break

            elif finalStepDanger > 0.5:
                supportPaths = []
                for unit in unconsideredUnits:
                    if unit.loc != pathToTarget[0]:
                        goalProv = unit.loc
                        if unit.type == "a":
                            previousNodes, distToAll = armyDistBetweenTerritories(unit.loc,paths,territories)
                        if unit.type == "f":
                            previousNodes, distToAll = fleetsDistBetweenTerritories(unit.loc,paths,territories)
                        dists = []
                        for dist in distToAll:
                            if dist in paths[pathToTarget[-1]]:
                                x = (distToAll[dist],dist)
                                dists.append(x)
                        dists.sort()
                        goalProv = dists[0][1]
                        pathToSupport = shortestPath(unit.loc,goalProv,previousNodes)
                        supportPath = (distToAll[goalProv],pathToSupport,goalProv,unit)
                        supportPaths.append(supportPath)
                        break
                supportPaths.sort()
                supportPath = supportPaths[0]
                pathToSupport = supportPath[1]
                # print(supportPaths)
                support = {"type":"Move","terr":[unit.loc,pathToSupport[0]]}
                moves.append(support)
                unconsideredUnits.remove(supportPath[-1])
        
        if holdVal >= moveVal:
            currentDanger = int(currentDanger)
            for i in range(currentDanger):
                for unit in unconsideredUnits:
                    if unit.inSupportingLoc(prelimHold[1],paths,territories):
                        support = {"type":"Support","terr":[prelimHold[1],unit.loc]}
                        unconsideredUnits.remove(unit)
                        break
        
        # adds the move or hold to the moves list and removes the unit from the unconsidered units
        if holdVal >= moveVal:
            move = prelimHold
        if moveVal > holdVal:
            move = prelimMove
        moves.append(move)
        # print(move)
        unconsideredUnits.remove(players[assignedCountry].unitAtLocation(move["terr"][0]))
    moves = reevaluateMoves(moves)
    return moves


# Prevents two units from moving into the same territory instead of supporting each other
def reevaluateMoves(moves):
    terr = {}
    for i in range(len(moves)):
        if moves[i]["type"] != "Move": continue
        if moves[i]["terr"][0] == moves[i]["terr"][1]:
            moves[i] = {"type":"Hold","terr":[ moves[i]["terr"][0] ]}
            terr[moves[i]["terr"][1]] = moves[i]["terr"][0]
        if moves[i]["terr"][1] in terr.keys():
            moves[i] = {"type":"Support","terr":[moves[i]["terr"][0], terr[moves[i]["terr"][1]], moves[i]["terr"][1]]}
        else:
            terr[moves[i]["terr"][1]] = moves[i]["terr"][0]
    return moves

def alternateMovesInitial(players,assignedCountry,territories,paths):
    otherPlayers = dict()
    for player in players:
        if player != assignedCountry:
            otherPlayers[player] = players[player]
    
    unconsideredUnits = players[assignedCountry].armies + players[assignedCountry].fleets
    moves = []
    home = ["con", "ank", "smy"]
    for unit in unconsideredUnits:
        # finds the distance from the unit to all territories on the
        if unit.type == "a":
            previousNodes, distToAll = armyDistBetweenTerritories(unit.loc,paths,territories)
        if unit.type == "f":
            previousNodes, distToAll = fleetsDistBetweenTerritories(unit.loc,paths,territories)

        # creates a list of 2-tuples of the evaluation score and the name of each province that it could move
        dists = []
        for dist in distToAll:
            if distToAll[dist] != 0:
                evaluation = territories[dist]["score"] / (distToAll[dist] ** 3)
                # if dist in home:
                #     evaluation *= 1.2
                x = (evaluation,dist) # 2-tuple with movementEval,provinceName
                dists.append(x)

        # sorts that by the evaluation score
        dists.sort(reverse=True)

        moves.append({"type":"Move","terr":[unit.loc, dists[getRandomMove(1, len(dists))][1]]})
        # unconsideredUnits.remove(unit)
        
    moves = reevaluateMoves(moves)
    return moves
        