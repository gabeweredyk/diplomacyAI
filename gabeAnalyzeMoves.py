from readJDIP import *
import numpy as np
from collections import OrderedDict
import copy

messagesToSend = {"AUS":"","ENG":"","FRA":"","GER":"","ITL":"","RUS":"","TUR":"","BUR":""}

#Credit for this algorithim: https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
def sortByValues(dict):
    keys = list(dict.keys())
    values = list(dict.values())
    sorted_value_index = np.argsort(values)[::-1]
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    return sorted_dict

# Probablity moves to the best territoy (as deemed by the bot)
predProbability = {"AUS":0.5,"ENG":0.5,"FRA":0.5,"GER":0.5,"ITL":0.5,"RUS":0.5,"TUR":0,"BUR":0.5}

def analyzeMoves(country):
    global units, paths, countries, territories, trust, requestedMoves, replies, predProbability, messagesToSend

    # Unit count counts the total number of units the bot has at any given time
    unitCount = 0

    #Get an array of every possible territory the bot could move to, this includes territories its units currently reside on
    neighbors = []
    for i in units.keys():
        if (units[i]["owner"] != country): continue
        unitCount += 1
        if i not in neighbors: neighbors.append(i)
        for j in paths[i]:
            if j not in neighbors: neighbors.append(j)


    #Them the bot uses probability theory to calculate the minimum strength it thinks it will need to attack any given territory

    #Indicator variables
    expectedIndStrength = {}
    for i in countries:
        if i == country: continue
        expectedIndStrength[i] = {}
        for j in territories:
            expectedIndStrength[i][j] = 0

    for i in units.keys():
        owner = units[i]["owner"]
        if owner == country: continue
        eUnit = {}
        eUnit[i] = territories[i]["score"] 
        for j in paths[i]:
            # If the unit can't move there, quit
            if units[i]["type"] == "a" and territories[j]["type"] == "Sea" or units[i]["type"] == "f" and territories[j]["type"] == "Land": continue
            # If considering an attack on its own unit, quit
            if j in units.keys() and units[j]["owner"] == owner: continue

            eUnit[j] = territories[j]["score"]
        # total = sum(eUnit.values())
        eUnit = sortByValues(eUnit)
        for j in range(len(eUnit.keys())):
            terr = list(eUnit.keys())[j]
            expectedIndStrength[owner][ terr ] += predProbability[owner] * ((1 - predProbability[owner]) ** j)
            if terr == i: expectedIndStrength[owner][ terr ] += 0.5 * predProbability[owner] * ((1 - predProbability[owner]) ** j)

    expectedStrengths = {}
    for i in territories:
        expectedStrengths[i] = 0
    for i in expectedIndStrength.values():
        for j in i.keys():
            expectedStrengths[j] += i[j]

    expectedStrengths = sortByValues(expectedStrengths)

    neededStrengths = {}
    for i in neighbors:
        if expectedStrengths[i] == 0: neededStrengths[i] = 0
        else: neededStrengths[i] =  int( expectedStrengths[i] + 1)

    #
    availableUnits = {}
    for i in neighbors:
        availableUnits[i] = []
        if i in units.keys() and units[i]["owner"] == country: availableUnits[i].append(i)
        for j in paths[i]:
            if j not in units.keys() or units[j]["owner"] != country: continue
            if units[j]["type"] == "a" and territories[i]["type"] == "Sea" or units[j]["type"] == "f" and territories[i]["type"] == "Land": continue
            availableUnits[i].append(j)

    neighborsValued = {}
    for i in neighbors:
        neighborsValued[i] = territories[i]["score"]
    neighborsValued = sortByValues(neighborsValued)

    neighbors = list(neighborsValued.keys())

    insufficientSupport = {}
    deltaPosition = {}
    pickableUnits =  copy.deepcopy(availableUnits)
    immobileUnits = []
    moves = []

    for i in neighbors:
        if unitCount <= 0: break
        hold = i in pickableUnits[i]
        selfStrength = len(pickableUnits[i])
        if hold: selfStrength += 0.5
        mobile = False
        for j in pickableUnits[i]:
            if j not in immobileUnits:
                mobile = True
        if selfStrength < neededStrengths[i] or not mobile: 
            insufficientSupport[i] = neededStrengths[i] - selfStrength
            continue
        n = neededStrengths[i]
        first = ""
        while n > 0:
            n -= 1
            if first == "":
                if hold:
                    moves.append({"Type":"Hold","terr":[i]})
                    deltaPosition[i] = i
                    immobileUnits.append(i)
                    first = i
                    continue
                first = leastValuableUnit(pickableUnits, i, immobileUnits)
                terr = first
                moves.append({"Type":"Move","terr":[first,i]})
                deltaPosition[first] = i
            else:
                terr = leastValuableUnit(pickableUnits, i, [])
                moves.append({"Type":"Support","terr":[terr,first,i]})
                deltaPosition[terr] = terr
            unitCount -= 1
            for j in neighbors:
                    if terr in pickableUnits[j]:
                        pickableUnits[j].remove(terr)

    #Do something with "useless holds"

    toPop = []
    for i in range(len(moves)):
        if moves[i]["Type"] != "Hold": continue
        terr = moves[i]["terr"][0]
        for j in moves:
            if j ["Type"] == "Hold": continue
            if j["terr"][0] == terr:
                toPop.append(i)
                break
        for j in deltaPosition.keys():
            if deltaPosition[j] in paths[terr]:
                moves[i] = {"Type":"Support","terr":[terr, j, deltaPosition[j]]}
                break
    for i in toPop:
        moves.pop(i)

    print(moves)
    

    for i in insufficientSupport.keys():
        if i in deltaPosition.values() or i in deltaPosition.keys(): continue
        recipient = ""
        recipientUnit = ""
        maxTrust = 0
        for j in paths[i]:
            if j not in units.keys(): continue
            r = units[j]["owner"]
            if maxTrust > trust[r]: continue
            recipient = r
            recipientUnit = j
            maxTrust = trust[r]
        if recipient == "" or messagesToSend[recipient] != "": continue
        if (i in units.keys() and units[i]["owner"] == recipient) or territories[i]["owner"] == recipient : continue
        demand = 0
        unit = leastValuableUnit(availableUnits, i, [])
        if unit == '': continue
        T = externalTrust[recipient]
        if T > 0.75: demand = 1
        if T > 1.5: demand = 2
        message = "We " + {0:"might want to",1:"should",2:"must"}[demand] + " support the " + {'a':'Army','f':'Fleet'}[units[unit]["type"]] + " in **" + unit + "** advancing into **" + i + "** with the unit in **" + recipientUnit + "**." 
        messagesToSend[recipient] = message

    print(messagesToSend)
    return

    
            
def leastValuableUnit(availableUnits, terr, immobileUnits):
    minReliance = ""
    minScore = 75
    for i in availableUnits[terr]:
        if i in immobileUnits: continue
        score = 0
        for j in availableUnits.values():
            if i in j:
                score += 1
        if score < minScore:
            minReliance = i 
    return minReliance

    # for player in requestedMoves.keys():
    #     for request in requestedMoves[country]:
    #         if request in moves:
    #             replies[player].append("Affirmative")
    #             externalTrust[player] *= 1.2
    #             continue
    #         if request["type"] == "Convoy":
    #             replies[player].append("Negative")
    #             externalTrust[player] /= 1.2
    #             continue
    #         if request["type"] == "Support":
    #             attacked = request["terr"][2]
    #             if territories[attacked]["owner"] == country or trust[territories[attacked]["owner"]] > trust[player]:
    #                 replies[player].append("Negative")
    #                 externalTrust[player] /= 1.2
    #             else:
    #                 replies[player].append("Affirmative")
    #                 externalTrust[player] *= 1.2
    
    # messagesToSend = {}
    # for i in countries:
    #     messagesToSend[i] = ""

    # for i in otherStrengths.keys():
    #     if territories[i]["owner"] == "" or territories[i]["owner"] == country: continue
    #     if messagesToSend[territories[i]["owner"]] != "": continue
    #     unitType = ''
        
    #     for j in units.values():
    #         if j["owner"] == territories[i]["owner"] and j["loc"] == i:
    #             unitType = j["type"]
    #     if unitType == '': continue
    #     unitType = {"a":"Army", "f":"Fleet"}[unitType]
    #     for j in paths[i]:
    #         if j in otherStrengths.keys(): continue
    #         if (territories[j]["type"] == "Land" and unitType == "Fleet") or (territories[j]["type"] == "Sea" and unitType == "Army"): continue
    #         messagesToSend[territories[i]["owner"]] = "You should move your " + unitType + " from **" + i + "** to **" + j + "**." 
    #         for k in range(len(moves)):
    #             if moves[k]["type"] != "Hold": continue
    #             if moves[k]["terr"][0] not in paths[j]: continue
    #             messagesToSend[territories[i]["owner"]] += " In return, I'll support your " + unitType + " in **" + i + "** advancing into **" + j + "** with the unit in **" + k + "**."
    #             moves[k] == {"type":"Support","terr":[moves[k]["terr"][0],i, j]}

    # needsSupport = {}
    # for i in moves:
    #     if i["type"] != "Move": continue
    #     unitType = ""
    #     for j in units.values():
    #         if j["loc"] != i["terr"][0]: continue
    #         unitType = j["type"]
    #     unitType = {"a":"Army", "f":"Fleet"}[unitType]
    #     needsSupport[i["terr"][1]] = {"type":unitType,"from":i["terr"][0]}


    # for i in needsSupport.keys():
    #     for j in units.values():
    #         if j["loc"] not in paths[i]: continue
    #         if j["owner"] == country: continue
    #         if messagesToSend[j["owner"]] != "": continue
    #         messagesToSend[j["owner"]] = "We should support the " + needsSupport[i]["type"] + " in **" + needsSupport[i]["from"] + "** advancing into **" + i + "** with the unit in **" + j["loc"] + "**."
    # print(netStrengths)

    # print("Moves: " + str(moves)) 
    # print("Messages: " + str(messagesToSend))
    # print("Replies: " +  str(replies))

    

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
print("For France:")
analyzeMoves("FRA")
print("For England:")
analyzeMoves("ENG")
print("For Burgandy:")
analyzeMoves("BUR")
