from readJDIP import *
import copy

def placeUnits(country):
    global units, paths, countries, territories, home
    placements = []
    unitsNeeded = 0
    tempUnits = copy.deepcopy(units)
    validLocs = home
    coastsCount = 0
    landsCount = 0
    for terr in territories:
        if territories[terr]["supply"] and territories[terr]["owner"] == country:
            unitsNeeded += 1
            if territories[terr]["type"] == "Coast":
                coastsCount += 1
            elif territories[terr]["type"] == "Land":
                landsCount += 1
    coastsLandsRatio = coastsCount / (landsCount+ 1)

    ownUnits = []
    for unit in units:
        if units[unit]["owner"] == country:
            ownUnits.append(units[unit]["loc"])

    for unit in units:
        if units[unit]["loc"] in validLocs:
            validLocs.remove(units[unit]["loc"])
        if units[unit]["owner"] == country:
            unitsNeeded -= 1
    
    if unitsNeeded == 0:
        return "No builds needed"

    elif unitsNeeded > 0:
        for i in range(unitsNeeded):
            placement = False
            fleetsCount = 0
            armiesCount = 0
            for unit in tempUnits:
                if tempUnits[unit]["type"] == "F":
                    fleetsCount += 1
                if tempUnits[unit]["type"] == "A":
                    armiesCount += 1
            fleetsToArmies = fleetsCount/(armiesCount + 1)
            fEval = fleetsToArmies + (coastsLandsRatio/10)
            typeToBuild = "A"
            if fEval < 0.6:
                typeToBuild = "F"
            if "con" in validLocs:
                placement = {"type":"Build","loc":"con","unitType":typeToBuild}
                validLocs.remove("con")
            elif "ank" in validLocs:
                placement = {"type":"Build","loc":"ank","unitType":typeToBuild}
                validLocs.remove("ank")
            elif "smy" in validLocs:
                placement = {"type":"Build","loc":"smy","unitType":typeToBuild}
                validLocs.remove("smy")
            if placement:
                placements.append(placement) 

    elif unitsNeeded < 0:
        unitsNeeded *= -1
        for i in range(unitsNeeded):
            unitsDangers = []
            for unit in ownUnits:
                dangerScore = 0
                for newUnit in units:
                    if (units[newUnit]["loc"] in paths[unit]) and units[newUnit]["owner"] != country:
                        dangerScore += 1
                unitsDangers.append(dangerScore,unit)
            unitsDangers.sort()
            unitToRem = unitsDangers[0][1]
            placements.append({"type":"Destroy","loc":unitToRem})
            ownUnits.remove(unitToRem)

    print(placements)