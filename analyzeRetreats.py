from readJDIP import *
from random import randint

def analyzeRetreats(inputStr):
    terrs = inputStr.split()
    global units,paths,countries,territories
    retreats = []
    for terr in terrs:
        validRetreatLocs = paths[terr]
        for unit in units.keys():
            if unit in validRetreatLocs:
                validRetreatLocs.remove(unit)

        retreatLoc = validRetreatLocs[randint(0,len(validRetreatLocs)-1)]
        retreats.append({"type":"Move","terr":[terr,retreatLoc]})
    
    print(retreats)