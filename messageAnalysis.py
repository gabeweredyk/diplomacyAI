from buildBoard import buildBoard
from country import *
from analyzeMoves import *

def messageAnalysis(prelimMoves,players,assignedCountry,territories,paths,trustDict):
    expectations = []
    for player in players:
        pass
    
    while True:
        incomingMessage = input("Incoming Message: ").strip()
        incomingMessage = incomingMessage.split()
        match incomingMessage[0]:
            case "You":
                match incomingMessage[1]:
                    case "might":
                        pass
                    case "should":
                        pass
                    case "must":
                        pass
            case "We":
                match incomingMessage[1]:
                    case "might":
                        pass
                    case "should":
                        pass
                    case "must":
                        pass
            case "I":
                match incomingMessage[1]:
                    case "might":
                        pass
                    case "should":
                        pass
                    case "must":
                        pass
    return expectations