from buildBoard import buildBoard
from country import Country, Fleet, Army

def buildCountries(trustDict,units,countries):
    players = dict()
    for country in countries:
        fleets = []
        armies = []
        for unit in units:
            if units[unit]["owner"] == country and units[unit]["type"] == "f":
                unit = Fleet(units[unit]["loc"],country)
                fleets.append(unit)
            elif units[unit]["owner"] == country and units[unit]["type"] == "a":
                unit = Army(units[unit]["loc"],country)
                armies.append(unit)
        players[country] = Country(country,armies,fleets,trustDict[country])
    
    return players