from buildBoard import buildBoard
from country import *
import mysql
import pandas as pd

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

def unitsInSupportingPositions(territory,paths,assignedCountry):
    vals = 0
    for neighbor in paths[territory]:
        if assignedCountry.fleetInProvince(neighbor) or assignedCountry.armyInProvince(neighbor):
            vals += 1
    return vals

def provinceIndex(territory,territories,paths,allArmies,allFleets,assignedCountry):
    score = 0
    supportingPlayers = []
    # additive/subtractive effects
    for neighbor in paths[territory]:
        if territories[neighbor]["supply"]:
            score += 100
        if (armyInProvince(neighbor,allArmies) or fleetInProvince(neighbor,allFleets)) and not (assignedCountry.armyInProvince(territory) or assignedCountry.fleetInProvince(neighbor) or unitsInSupportingPositions(neighbor,paths,assignedCountry.armies,assignedCountry.fleets)):
            score *= (2/3)
        for neighborNeighbor in paths[neighbor]:
            if territories[neighborNeighbor]["supply"]:
                score += 50
            for neighborNeighborNeighbor in paths[neighborNeighbor]:
                if territories[neighborNeighborNeighbor]["supply"]:
                    score += 25

def analyzeMoves(players,assignedCountry,territories,paths,allArmies,allFleets):
    moves = []
    for army in assignedCountry.armies:
        for neighbor in paths[army.location]:
            score = provinceIndex(neighbor,territories,paths,allArmies,allFleets,assignedCountry)
            # disqualifying things that reset score to 0 because it's an impossible move
            if territories[neighbor]["type"] == "Sea":
                score = 0