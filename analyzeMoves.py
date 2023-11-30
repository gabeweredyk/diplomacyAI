from buildBoard import buildBoard
from country import *
import mysql
import pandas as pd
import sys

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
            if unit.type == "a":
                previousNodes, distToAll = armyDistBetweenTerritories(unit.loc,paths,territories)
            if unit.type == "f":
                previousNodes, distToAll = fleetsDistBetweenTerritories(unit.loc,paths,territories)
            dists = []
            for dist in distToAll:
                if distToAll[dist] != 0:
                    evaluation = territories[dist]["score"] / (distToAll[dist]) ** 2
                    x = (evaluation,dist) # 3-tuple with distance, target province name, target province score
                    dists.append(x)
            dists.sort()
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
        target = targets[0]
        pathToTarget = target[1]
        moveVal = territories[target[2]]["score"]/(target[0] ** 2)
        prelimMove = ("move",pathToTarget[0],pathToTarget[1])

        # calculate current province danger for the unit that might move and consider if it should hold instead of moving
        currentDanger = immediateDanger(target[-1].loc,paths,otherPlayers)
        holdVal = currentDanger*100
        prelimHold = ("hold",target[-1].loc)
        if territories[target[-1].loc]["owner"] != assignedCountry and territories[target[-1].loc]["supply"]:
            holdVal = sys.maxsize

        # calculate province danger + allocate support units
        if moveVal > holdVal:
            nextStepDanger = immediateDanger(pathToTarget[1],paths,otherPlayers)
            finalStepDanger = provDanger(pathToTarget[-1],paths,otherPlayers)
            if nextStepDanger > 0.9:
                for unit in unconsideredUnits:
                    if unit.inSupportingLoc(pathToTarget[1],paths,territories) and unit.loc != pathToTarget[0]:
                        support = ("support move",pathToTarget[0],pathToTarget[1],unit.loc)
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
                support = ("move",pathToSupport[0],pathToSupport[1])
                moves.append(support)
                unconsideredUnits.remove(supportPath[-1])
        
        if holdVal >= moveVal:
            currentDanger = int(currentDanger)
            for i in range(currentDanger):
                for unit in unconsideredUnits:
                    if unit.inSupportingLoc(prelimHold[1],paths,territories):
                        support = ("support hold",prelimHold[1],unit.loc)
                        unconsideredUnits.remove(unit)
                        break
        
        # adds the move or hold to the moves list and removes the unit from the unconsidered units
        if holdVal >= moveVal:
            move = prelimHold
        if moveVal > holdVal:
            move = prelimMove
        moves.append(move)
        unconsideredUnits.remove(players[assignedCountry].unitAtLocation(move[1]))
    return moves