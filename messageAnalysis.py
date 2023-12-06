from readJDIP import *
self = "TUR"
promisedMoves = {}
requestedMoves = {}
replies = {}



for i in countries:
    promisedMoves[i] = []
    requestedMoves[i] = []




def ownsTerritory(player, territory):
    global units
    if territory not in units.keys(): return False
    return units[territory]["owner"] == player

def interpretMessage():
    global countries
    player = ""
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
            if word[-1] == ".":
                word = word[:-1]
            match i:
                case 0:
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
        # print(promisedMoves)


def storeMove(country, move):
    global promisedMoves, requestedMoves, self
    if (ownsTerritory(country, move["terr"][0])):
        promisedMoves[country].append( move)
    elif (ownsTerritory(self, move["terr"][0])):
        requestedMoves[country].append( move)
