from readJDIP import *
import numpy as np
from collections import OrderedDict
import copy

#Credit for this algorithm: https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
def sortByValues(dict):
    keys = list(dict.keys())
    values = list(dict.values())
    sorted_value_index = np.argsort(values)[::-1]
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    return sorted_dict

# Probablity moves to the best territoy (as deemed by the bot)
predProbability = {"AUS":0.5,"ENG":0.5,"FRA":0.5,"GER":0.5,"ITL":0.5,"RUS":0.5,"TUR":0,"BUR":0.5}

#used units is populated with a dictionary that points a usedUnit to where it gives strength
def analyzeMoves(country, usedUnits):
    global units, paths, countries, territories, trust, predProbability, messagesToSend, movesToSend

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

    #Indicator variable setup. ExpectedIndStrength is a dictionary that states for each country, the expected strength it would output to every space
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
        
        #This loop gets all feasible attacks one could make with their unit, and notes its evaluation score (determined in readJDIP.py)
        for j in paths[i]:
            # If the unit can't move there, quit
            if units[i]["type"] == "a" and territories[j]["type"] == "Sea" or units[i]["type"] == "f" and territories[j]["type"] == "Land": continue
            # If considering an attack on its own unit, quit
            if j in units.keys() and units[j]["owner"] == owner: continue
            eUnit[j] = territories[j]["score"]
        
        # The probabilistic model underlying the AI relies on the following:
        # A player will do their best move with probability p, their second best move with probability (1- p)p, and their third best as (1-p)^2p and so on
        # This reasoning is based off how one arrives at making decisions with trade-offs:
        # A player will ultimately like to do their best move, but could gain more in the long run for a weaker move now, so there is a chance they do that
        eUnit = sortByValues(eUnit)
        for j in range(len(eUnit.keys())):
            terr = list(eUnit.keys())[j]
            expectedIndStrength[owner][ terr ] += predProbability[owner] * ((1 - predProbability[owner]) ** j)
            if terr == i: expectedIndStrength[owner][ terr ] += 0.5 * predProbability[owner] * ((1 - predProbability[owner]) ** j)


    #Combine each individual country into one value for expected strengths because E(X + Y) = E(X) + E(Y) for any r. vars X, Y
    expectedStrengths = {}
    for i in territories:
        expectedStrengths[i] = 0
    for i in expectedIndStrength.values():
        for j in i.keys():
            expectedStrengths[j] += i[j]

    #accounts for agreed upon moves
    for i in usedUnits.keys():
        expectedStrengths[usedUnits[i]] -= 2
        if i == usedUnits[i]: expectedStrengths[usedUnits[i]] -= 0.5

    # sortByValues here sorts the dictionary by the expected strengths of each territory, giving us a list of the most dangerous territories
    expectedStrengths = sortByValues(expectedStrengths)

    #Needed strengths is the ceiling of the expected strengths, except when the expected strength is leq than 0 (No other player can reach it)
    neededStrengths = {}
    for i in neighbors:
        if expectedStrengths[i] <= 0: neededStrengths[i] = 0
        else: neededStrengths[i] =  int( expectedStrengths[i] + 1)

    #For every territory in neighbor, get all the units that could possibly assist in an attack/defense on that territory
    availableUnits = {}
    for i in neighbors:
        availableUnits[i] = []
        if i in units.keys() and units[i]["owner"] == country and i not in usedUnits.keys(): availableUnits[i].append(i)
        for j in paths[i]:
            if j not in units.keys() or units[j]["owner"] != country or i in usedUnits.keys(): continue
            if units[j]["type"] == "a" and territories[i]["type"] == "Sea" or units[j]["type"] == "f" and territories[i]["type"] == "Land": continue
            availableUnits[i].append(j)

    #Sorts neighbors by value determined by heatmap
    neighborsValued = {}
    for i in neighbors:
        neighborsValued[i] = territories[i]["score"]
    neighborsValued = sortByValues(neighborsValued)
    neighbors = list(neighborsValued.keys())


    #Insufficient support keeps track of all territories it doesn't currently feel confident in taking, and saves them for later when it asks players for assistance
    insufficientSupport = {}
    #deltaPosition tracks where each unit ideally ends up at the end of the round. Implemented to help with move notation
    deltaPosition = {}
    pickableUnits = copy.deepcopy(availableUnits)
    #Immobile units are units that are stationary because the bot has decided it's better to hold that territory than to move, but are still free to support other attacks
    #The bot minimizes the amount of moves that are simply "Hold ter"
    immobileUnits = []
    moves = []

    #note neighbors is now ordered by value, meaning it starts with territories it wants the most
    for i in neighbors:
        #If there are no more units left, forget about it. unitCount decrements with every move assigned
        if unitCount <= 0: break
        #If you are considering an attack on a territory with a stationary unit, dont
        
        if i in deltaPosition.keys(): 
            if  deltaPosition[i] == i : continue
        #hold is true iff the considered territory has a unit inside of it. Prioritizes holds since holds have 1.5 strength while movements have 1 strength
        hold = i in pickableUnits[i]
        # selfStrength is the max strength the bot can put on a territory with its unused units
        selfStrength = len(pickableUnits[i])
        if hold: selfStrength += 0.5

        #mobile makes sure that all the remaining units are not immobile units
        #this prevents the bot from thinking it can attack a territory with units that are free to support but not move
        mobile = False
        for j in pickableUnits[i]:
            if j not in immobileUnits:
                mobile = True

        #If the bot has no units that can move or not as much strengh as it thinks it needs, it keeps the territory in mind for later
        if selfStrength < neededStrengths[i] or not mobile: 
            insufficientSupport[i] = neededStrengths[i] - selfStrength
            continue


        n = neededStrengths[i]
        first = ""
        #The algorithm this while loop performs:
        """
        If I'm allocating units to a territory with a unit on it currently
            Then make that unit hold and have as many as I need support it
        Else
            Make the unit in the least valuable territory move to the new territory
            Then have all the other available units support it
        
        Also, If I have deemed a unit fit to remain in place, I keep it around so it can
        support a valuable attack.
        """
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

    # This part of the code address the double-movements of re-allocated stationary units
    # and checks if any other hold moves can spend their turn supporting
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

    #Then bamn! moves
    print("Moves:")
    for i in moves:
        match i["Type"]:
            case "Hold":
                print("Hold " + i["terr"][0] )
            case "Move":
                print(i["terr"][0] + " -> " + i["terr"][1] )
            case "Support":
                print(i["terr"][0] + " supports " + i["terr"][1] + " -> " + i["terr"][2])

    #Goes through the territories it didnt feel confident in claiming
    for i in insufficientSupport.keys():
        #The bot shouldn't be proposing attacks on territories it currently has
        if i in deltaPosition.keys(): continue
        if i not in units.keys() and territories[i]["owner"] == "" : continue
        #The bot looks for the player it trusts the most to carry out this cooperative move, this person is the recipient
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
        
        #If the bot couldn't find anyone around to help or has already reached out, it quits
        if recipient == "" or recipient == country or messagesToSend[recipient] != "": continue
        #If the bot is suggesting taking one of the recipient's territories or attacking one of its units, it quits (Learned our lesson)
        if (i in units.keys() and units[i]["owner"] == recipient) or territories[i]["owner"] == recipient : continue
        #Suggests doing this with the bots least valuable unit, might want to tweak this algorithm so it uses its agent in its last move instead
        #But this seems to be working fine
        unit = leastValuableUnit(availableUnits, i, [recipientUnit])
        #If it can't find a unit to suggest the move with, it
        if unit == '': continue
        #Determines what tone it should take with the recipeint
        demand = 0
        T = externalTrust[recipient]
        if T > 0.75: demand = 1
        if T > 1.5: demand = 2
        #Constructs a string seen in stringbuilder and abuses dictionaries
        message = "We " + {0:"might want to",1:"should",2:"must"}[demand] + " support the " + {'a':'Army','f':'Fleet'}[units[unit]["type"]] + " in **" + unit + "** advancing into **" + i + "** with the unit in **" + recipientUnit + "**." 
        movesToSend[recipient] = {"Type":"Support","terr":[recipientUnit, unit, i]}
        messagesToSend[recipient] = message

    print("Messages:")
    for i, message in messagesToSend.items():
        if message == "": continue
        print("To " + i + ": " + message)

    return movesToSend

    
            
#Function for determining the least valuable unit given the availableUnits of every territory.
#immobileUnits is the array itself when considering a movement move, but is an empty array when considering supports
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

