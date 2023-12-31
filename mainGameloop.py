from readJDIP import *
from gabeAnalyzeMoves import *
from messageAnalysis import *

# from trustFactor import *
from gameLearning import updateSocialValues

from analyzeRetreats import *
from placeUnits import *


import random

active = True
initialTerritoryScore()

while active:
    # takes the current turn and uses that to decide what it should be doing
    # example turn input - "Fall 1902, Moves"
    turn = input("Turn: ")
    turn = turn.split()
    buildBoard()
    # print(promisedMoves)
    match turn[-1]:
        case "movement":
            messagesToSend = {"ENG":"","FRA":"","BUR":""}
            movesToSend = analyzeMoves(self, {})
            interpretMessage(movesToSend)
            previousMoves = moves
        case "retreat":
            terrsToRetreat = input("Units in these territories need to retreat (separate by commas, no spaces): ")
            analyzeRetreats(terrsToRetreat)
        case "adjustment":
            placeUnits(self)
        case "learn":
            updateSocialValues()

        # the following are placeholder game-ending states
        case "Lose":
            active = False
            print(":( .")
        case "Win":
            active = False
            winMessages = ["Gadzooks!","Bless my collar button!","Gnarly!","Yeehaw!","Most cool!","Yippee!","Great!","Aye carumba!",
                           "Swell!","Extreme!","Give me some skin!","Raise the roof!","Wonderful!","Holy smokes!","Egads!","Deluxe!"]
            print(random.choice(winMessages))
        case "Draw":
            active = False
            print("Good game.")

    
