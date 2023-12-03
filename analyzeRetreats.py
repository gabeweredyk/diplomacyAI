from readJDIP import *
from random import randint

def analyzeRetreats(inputStr):
    terrs = inputStr.split()
    global units,paths,countries,territories
    retreats = []
    for terr in terrs:
        validRetreatLocs = paths[terr]
        for unit in units:
            if units[unit]["loc"] in validRetreatLocs:
                validRetreatLocs.remove(units[unit]["loc"])

        retreatLoc = validRetreatLocs[randint(0,len(validRetreatLocs)-1)]
        retreats.append({"type":"Move","terr":[terr,retreatLoc]})
    
    print(retreats)