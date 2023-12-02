from readJDIP import *
from country import *
from analyzeMoves import *

self = "TUR"
promisedMoves = {}
for i in countries:
    promisedMoves[i] = []

def ownsTerritory(player, territory):
    global units
    for i in units.values():
        if i["owner"] == player and i["loc"] == territory:
            return True
    return False


def messageAnalysis():
    global promisedMoves
    while True:
        player = input("From: ").strip()
        message = input("Incoming Message: ").strip()
        message = message.split(" ")
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
                    if (selfActor and not otherActor):
                        demand = {"might":0, "want":1, "will":2}[word]
                    else:
                        demand = {"might":0, "should":1, "must":2}[word]
            match word:
                case "so":
                    stage = 1
                case "return":
                    stage = 2
            match word:
                case "move":
                    terr = message[i + 4]
                    if (ownsTerritory(player, terr)):
                        promisedMoves[player].append( {"type":"Move","terr":[terr, message[i + 6]]})
                case "hold":
                    terr = message[i + 4]
                    if (ownsTerritory(player, terr)):
                        promisedMoves[player].append( {"type":"Hold","terr":[terr]})
                case "support":
                    terr = message[i + 12]
                    if (ownsTerritory(player, terr)):
                        promisedMoves[player].append( {"type":"Support","terr":[terr, message[i + 4], message[i + 7]]})
                case "convoy":
                    terr = message[i + 12]
                    if (ownsTerritory(player, terr)):
                        promisedMoves[player].append( {"type":"Convoy","terr":[terr, message[i + 4], message[i + 6]]})
        print(promisedMoves)    

messageAnalysis()