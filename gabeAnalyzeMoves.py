from readJDIP import *
import numpy as np
from collections import OrderedDict
from messageAnalysis import requestedMoves, replies

#Credit for this algorithim: https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
def sortByValues(dict):
    keys = list(dict.keys())
    values = list(dict.values())
    sorted_value_index = np.argsort(values)[::-1]
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    return sorted_dict


def analyzeMoves(country):
    # Country strengths is a dictionary giving the strength
    global units, paths, countries, territories, trust, requestedMoves, replies
    # Step 1: Consider all territories that the bot has influence over
    neighbors = []
    unitTerritories = {}
    unitCount = 0
    for i in units.values():
        if (i["owner"] != country): continue
        unitCount += 1
        unitTerritories[i["loc"]]= {"type":i["type"]}
        if i["loc"] not in neighbors:
            neighbors.append(i["loc"])
        for j in paths[i["loc"]]:
            if j not in neighbors:
                neighbors.append(j)

    print(neighbors)

    # Step two, calculate the maximum amount of "strength" each country can exert on each territory
    strengths = {}
    for i in countries:
        strengths[i] = {}
        for j in neighbors:
            strengths[i][j] = 0
    for unit in units.values():
        terr = unit["loc"]
        coun = unit["owner"]
        if terr in neighbors:
            strengths[coun][terr] += 1.5
        for i in paths[terr]:
            if i in neighbors:
                strengths[coun][i] += 1

    #Personal Strengths only for bot
    personalStrengths = strengths[country]
    personalStrengths = sortByValues(personalStrengths)

    #Net Strengths is essentially for every territory, a dot product of the actual strength and the trust value. This is why Turkey has trust -1
    #Other Strengths is every territory that isn't Turkey
    netStrengths = {}
    otherStrengths = {}
    for i in neighbors:
        netStrengths[i] = 0
        otherStrengths[i] = 0
        for j in countries:
            factor = -1 * trust[j]
            netStrengths[i] += strengths[j][i] * factor
            if j == country: continue
            otherStrengths[i] += strengths[j][i] * factor

    netStrengths = sortByValues(netStrengths)
    otherStrengths = sortByValues(otherStrengths)

    # print(netStrengths)

    #Dictionary of territories then their evaluation. Considers all territories it currently owns and all adjacent to it

    newTerritories = {}
    for i in netStrengths.keys():
        # if territories[i]["owner"] == country: continue
        evaluation = territories[i]["score"] + 200 * netStrengths[i] ** 3
        # if netStrengths[i] < 0: continue
        newTerritories[i] = evaluation
                
    newTerritories = sortByValues(newTerritories)

    # print(newTerritories)

    # print(unitTerritories.keys())


    #So now that the bot has prioritized what territories it wants, it starts assigning units to each of them
    moves = []
    i = 0
    while i < len(newTerritories.keys()):
        arr = list(newTerritories.keys())
        terr = arr[i]
        if (otherStrengths[terr] == 0):
            i += 1
            continue
        tileType = {"Coast":"c","Land":"a","Sea":"f"}[territories[terr]["type"]]
        attackStrength = 0
        availableUnits = []
        for j in unitTerritories.keys():
            if (j in paths[terr] or j == terr) and (unitTerritories[j]["type"] == tileType or tileType == "c"):
                availableUnits.append(j)
        print(terr)
        print(availableUnits)
        attackingUnits = []
        while len(attackingUnits) <= -otherStrengths[terr] and len(moves) != unitCount and len(availableUnits) != 0:
            # if len(attackingUnits) > 0:
            #     arr = []
            #     for j in availableUnits:
            #         if j in paths[attackingUnits[0]]:
            #             arr.append(j)
            #     availableUnits = arr
            #     continue      
            maxProtected = availableUnits[0]
            for j in availableUnits:
                if personalStrengths[j] > personalStrengths[maxProtected]:
                    maxProtected = j
            moves.append({"type":"Move","terr":[maxProtected,terr]})
            availableUnits.remove(maxProtected)
            unitTerritories.pop(maxProtected)
            attackingUnits.append( maxProtected )

        i += 1
    
    for i in unitTerritories.keys():
        best = paths[i][0]
        for j in paths[i]:
            if territories[best]["score"] < territories[j]["score"] :
                best = j
        moves.append({"type":"Move","terr":[i,best]})

    
    
    moves = resolveMoves(moves)

    attackingMoves = []
    for i in moves:
        if i["type"] != "Move": continue
        attackingMoves.append(i)
    for i in range(len(moves)):
        if moves[i]["type"] != "Hold": continue
        possibleSupports = {}
        for j in attackingMoves:
            if j["terr"][1] in paths[moves[i]["terr"][0]]:
                possibleSupports[j["terr"][1]] = j["terr"][0]
        if len(possibleSupports.keys()) == 0: continue
        best = list(possibleSupports.keys())[0]
        for j in possibleSupports.keys():
            if otherStrengths[j] < otherStrengths[best]:
                best = j
            print(otherStrengths[best])
        otherStrengths[best] += 1
        moves[i] = {"type":"Support","terr":[moves[i]["terr"][0],possibleSupports[best],best]}

    for player in requestedMoves.keys():
        for request in requestedMoves[country]:
            if request in moves:
                replies[player].append("Affirmative")
                externalTrust[player] *= 1.2
                continue
            if request["type"] == "Convoy":
                replies[player].append("Negative")
                externalTrust[player] /= 1.2
                continue
            if request["type"] == "Support":
                attacked = request["terr"][2]
                if territories[attacked]["owner"] == country or trust[territories[attacked]["owner"]] > trust[player]:
                    replies[player].append("Negative")
                    externalTrust[player] /= 1.2
                else:
                    replies[player].append("Affirmative")
                    externalTrust[player] *= 1.2
    
    messagesToSend = {}
    for i in countries:
        messagesToSend[i] = ""

    for i in otherStrengths.keys():
        if territories[i]["owner"] == "" or territories[i]["owner"] == country: continue
        if messagesToSend[territories[i]["owner"]] != "": continue
        unitType = ''
        
        for j in units.values():
            if j["owner"] == territories[i]["owner"] and j["loc"] == i:
                unitType = j["type"]
        unitType = {"a":"Army", "f":"Fleet"}[unitType]
        for j in paths[i]:
            if j in otherStrengths.keys(): continue
            messagesToSend[territories[i]["owner"]] = "You should move your " + unitType + " from **" + i + "** to **" + j + "**." 


    
    print(netStrengths)

    return moves, messagesToSend

    

def resolveMoves(moves):
    terr = {}
    for i in range(len(moves)):
        if moves[i]["terr"][0] == moves[i]["terr"][1]:
            moves[i] = {"type":"Hold","terr":[ moves[i]["terr"][0] ]}
            terr[ moves[i]["terr"][0] ] = moves[i]["terr"][0] 
    for i in range(len(moves)):
        if moves[i]["type"] != "Move": continue
        if moves[i]["terr"][1] in list(terr.keys()):
            moves[i] = {"type":"Support","terr":[moves[i]["terr"][0], terr[moves[i]["terr"][1]], moves[i]["terr"][1]]}
        else:
            terr[moves[i]["terr"][1]] = moves[i]["terr"][0]
    return moves

    

print(analyzeMoves("TUR"))