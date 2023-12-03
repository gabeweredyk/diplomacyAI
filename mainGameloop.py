from readJDIP import *
from analyzeRetreats import *
from placeUnits import *
from gabeAnalyzeMoves import *
from messageAnalysis import *
from trustFactor import *
import random

active = True

while active:
    # takes the current turn and uses that to decide what it should be doing
    # example turn input - "Fall 1902, Moves"
    turn = input("Turn: ")
    turn = turn.split()
    buildBoard()
    print(promisedMoves)
    match turn[-1]:
        case "movement":
            updateTrust("TUR")
            promisedMoves = {}
            requestedMoves = {}
            interpretMessage()
            analyzeMoves("TUR")
        case "retreat":
            terrsToRetreat = input("Units in these territories need to retreat (separate by commas, no spaces): ")
            analyzeRetreats(terrsToRetreat)
        case "adjustment":
            placeUnits("TUR")

        # the following are placeholder game-ending states
        case "Lose":
            active = False
            print("A shame.")
        case "Win":
            active = False
            winMessages = ["Gadzooks!","Bless my collar button!","Gnarly!","Yeehaw!","Most cool!","Yippee!","Great!","Aye carumba!",
                           "Swell!","Extreme!","Give me some skin!","Raise the roof!","Wonderful!","Holy smokes!","Egads!","Deluxe!"]
            print(random.choice(winMessages))
        case "Draw":
            active = False
            print("Good game.")

    
