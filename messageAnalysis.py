from readJDIP import *
from trustFactor import *
from gabeAnalyzeMoves import analyzeMoves

promisedMoves = {"FRA":[],"ENG":[],"BUR":[]}
requestedMoves = {"FRA":[],"ENG":[],"BUR":[]}

for i in countries:
    promisedMoves[i] = []
    requestedMoves[i] = []


def ownsTerritory(player, territory):
    global units
    if territory not in units.keys(): return False
    return units[territory]["owner"] == player

def interpretMessage(movesToSend):
    global countries, messagesToSend
    usedUnits = {}
    player = ""
    print("Now consider other players' messages: ")
    while player != "BREAK":
        player = input("From: ").strip()
        if player not in countries: continue
        message = input("Incoming Message: ").strip()
        message = message.split(" ")
        for i in range(len(message)):
            if message[i][-1] == ".":
                message[i] = message[i][:-1]
        demand = 0
        selfActor = True
        otherActor = True
        stage = 0
        # Player = "AUS" or something like that
        for i in range(len(message)):
            word = message[i]
            match i:
                case 0:
                    if word == "Affirmative":
                        if movesToSend[player]["Type"] != "Support": continue
                        promisedMoves[player].append(movesToSend[player])
                        usedUnits[ movesToSend[player]["terr"][1] ] = movesToSend[player]["terr"][2]
                    selfActor = word != "I"
                    otherActor = word != "You"
                case 1:
                    demand = {"might":0, "should":1, "must":2, "want":1, "will":2}[word]
            match word:
                case "so":
                    stage = 1
                case "return":
                    stage = 2
            if stage == 1: continue
            match word:
                case "move":
                    move = {"type":"Move","terr":[message[i + 4], message[i + 6]]}
                    storeMove(player, move)
                case "hold":
                    move = {"type":"Hold","terr":[message[i + 4]]}
                    storeMove(player, move)
                case "support":
                    move = {"type":"Support","terr":[message[i + 12], message[i + 4], message[i + 7]]}
                    storeMove(player, move)
                case "convoy":
                    move = {"type":"Convoy","terr":[message[i + 12], message[i + 4], message[i + 6]]}
                    storeMove(player, move)
        print(usedUnits)
        analyzeMoves(self, usedUnits)
        # print(promisedMoves)
        


def evaluateRequest(country, move):
    global moves, trust, self, territories
    for i in moves:
        if equalMoves(move, i): return True
    if move["type"] == "Convoy":
        return False
    attackingTerr = move["terr"][-1]
    if (attackingTerr in units.keys() and units[attackingTerr] == self) or territories[attackingTerr]["owner"] == self: return False
    return trustPlayer(country)

def trustPlayer(country):
    global trust
    rng = np.random.default_rng()
    X = rng.normal(1 + R/2, R)
    return trust[country] > X

def storeMove(country, move):
    global promisedMoves, requestedMoves, self
    if (ownsTerritory(country, move["terr"][0])):
        promisedMoves[country].append( move)
    elif (ownsTerritory(self, move["terr"][0])):
        response = {True:"Affirmative", False:"Negative"}[evaluateRequest(country, move)]
        print("Reply to " + country + ": " + response)
        if (response == "Negative"): return
        requestedMoves[country].append(move)

