from readJDIP import *
import copy



def placeUnits(country):
    global units, paths, countries, territories
    placements = []
    unitsNeeded = 0
    tempUnits = copy.deepcopy(units)
    validLocs = []
    for terr in territories:
        if territories[terr]["owner"] != country: continue
        if terr in units.keys(): continue
        validLocs.append(terr)
    
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
            ownUnits.append(unit)

    for unit in units:
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

            # Territories are sorted by value by default
            for i in territories.keys():
                if i not in validLocs: continue
                if territories[i]["type"] == "Land" and typeToBuild == "F": continue
                validLocs.remove(i)
                placement = {"type":"Build","loc":i,"unitType":typeToBuild}
                break
            
            if not placement:
                typeToBuild = "A"
                for i in territories.keys():
                    if i not in validLocs: continue
                    validLocs.remove(i)
                    placement = {"type":"Build","loc":i,"unitType":typeToBuild}
                    break

            if placement:
                placements.append(placement) 

    elif unitsNeeded < 0:
        unitsNeeded *= -1
        for i in range(unitsNeeded):
            unitsDangers = []
            for unit in ownUnits:
                dangerScore = 0
                for newUnit in units:
                    if (newUnit in paths[unit]) and units[newUnit]["owner"] != country:
                        dangerScore += 1
                unitsDangers.append((dangerScore,unit))
            unitsDangers.sort()
            unitToRem = unitsDangers[0][1]
            placements.append({"type":"Destroy","loc":unitToRem})
            ownUnits.remove(unitToRem)

    print(placements)