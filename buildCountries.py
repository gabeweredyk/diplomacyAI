from buildBoard import buildBoard
from country import Country, Fleet, Army

def buildCountries(trustDict,units,countries):
    players = dict()
    for country in countries:
        fleets = dict()
        armies = dict()
        for unit in units:
            if unit["owner"] == country and unit["type"] == "Fleet":
                unit = Fleet(unit["territory"])
                fleets.add(unit)
            elif unit["owner"] == country and unit["type"] == "Army":
                unit = Army(unit["territory"])
                armies.add(unit)
        players[country] = Country(country,armies,fleets,trustDict[country])
    
    return players