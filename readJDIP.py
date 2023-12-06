import numpy as np

units = dict()
paths = dict()
previousMoves = dict()

def sortByValues(dict, value):
    keys = list(dict.keys())
    realValues = list(dict.values())
    values = []
    for i in dict.values():
        values.append(i[value])
    sorted_value_index = np.argsort(values)[::-1]
    sorted_dict = {keys[i]: realValues[i] for i in sorted_value_index}
    return sorted_dict

trust = {"FRA":1,"ENG":1,"GER":1,"ITL":1,"AUS":1,"RUS":1,"TUR":-1,"BUR":1}
externalTrust = {"FRA":1,"ENG":1,"GER":1,"ITL":1,"AUS":1,"RUS":1,"TUR":-1,"BUR":1}
# countries = ["AUS", "ENG", "FRA", "GER", "ITL", "RUS", "TUR"]
countries = ["ENG", "FRA", "BUR"]

self = "FRA"
# home = ["ank", "con", "smy"]

# territories = {'rum': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 2400}, 'nth': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 2300}, 'ser': {'supply': True, 'type': 'Land', 'owner': '', 'score': 2150}, 'bul': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 2100}, 'tri': {'supply': True, 'type': 'Coast', 'owner': 'AUS', 'score': 2100}, 'kie': {'supply': True, 'type': 'Coast', 'owner': 'GER', 'score': 1950}, 'mun': {'supply': True, 'type': 'Land', 'owner': 'GER', 'score': 1850}, 'bud': {'supply': True, 'type': 'Land', 'owner': 'AUS', 'score': 1850}, 'den': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 1750}, 'bla': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1700}, 'nwy': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 1700}, 'gal': {'supply': False, 'type': 'Land', 'owner': '', 'score': 1700}, 'ven': {'supply': True, 'type': 'Coast', 'owner': 'ITL', 'score': 1650}, 'con': {'supply': True, 'type': 'Coast', 'owner': 'TUR', 'score': 1600}, 'bel': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 1600}, 'gre': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 1550}, 'sev': {'supply': True, 'type': 'Coast', 'owner': 'RUS', 'score': 1550}, 'bal': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1550}, 'vie': {'supply': True, 'type': 'Land', 'owner': 'AUS', 'score': 1500}, 'ion': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1500}, 'bur': {'supply': False, 'type': 'Land', 'owner': '', 'score': 1500}, 'hol': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 1500}, 'swe': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 1450}, 'war': {'supply': True, 'type': 'Land', 'owner': 'RUS', 'score': 1450}, 'eng': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1450}, 'mao': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1450}, 'stp': {'supply': True, 'type': 'Coast', 'owner': 'RUS', 'score': 1400}, 'aeg': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1400}, 'tyr': {'supply': False, 'type': 'Land', 'owner': '', 'score': 1350}, 'ber': {'supply': True, 'type': 'Coast', 'owner': 'GER', 'score': 1350}, 'mos': {'supply': True, 'type': 'Land', 'owner': 'RUS', 'score': 1350}, 'smy': {'supply': True, 'type': 'Coast', 'owner': 'TUR', 'score': 1350}, 'ukr': {'supply': False, 'type': 'Land', 'owner': '', 'score': 1300}, 'spa': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 1300}, 'ank': {'supply': True, 'type': 'Coast', 'owner': 'TUR', 'score': 1300}, 'ruh': {'supply': False, 'type': 'Land', 'owner': '', 'score': 1250}, 'alb': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 1250}, 'gas': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 1250}, 'hel': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1200}, 'lvn': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 1200}, 'bre': {'supply': True, 'type': 'Coast', 'owner': 'FRA', 'score': 1150}, 'mar': {'supply': True, 'type': 'Coast', 'owner': 'FRA', 'score': 1150}, 'edi': {'supply': True, 'type': 'Coast', 'owner': 'ENG', 'score': 1150}, 'sil': {'supply': False, 'type': 'Land', 'owner': '', 'score': 1150}, 'tys': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1150}, 'rom': {'supply': True, 'type': 'Coast', 'owner': 'ITL', 'score': 1150}, 'par': {'supply': True, 'type': 'Land', 'owner': 'FRA', 'score': 1100}, 'ska': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1100}, 'boh': {'supply': False, 'type': 'Land', 'owner': '', 'score': 1050}, 'nwg': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1050}, 'arm': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 1050}, 'nap': {'supply': True, 'type': 'Coast', 'owner': 'ITL', 'score': 1050}, 'lon': {'supply': True, 'type': 'Coast', 'owner': 'ENG', 'score': 1050}, 'adr': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1050}, 'lvp': {'supply': True, 'type': 'Coast', 'owner': 'ENG', 'score': 1000}, 'bot': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 1000}, 'yor': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 950}, 'pru': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 950}, 'lyo': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 950}, 'pic': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 950}, 'apu': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 950}, 'wes': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 900}, 'fin': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 900}, 'tus': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 850}, 'por': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 850}, 'pie': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 850}, 'tun': {'supply': True, 'type': 'Coast', 'owner': '', 'score': 800}, 'bar': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 700}, 'eas': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 700}, 'wal': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 700}, 'iri': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 650}, 'nao': {'supply': False, 'type': 'Sea', 'owner': '', 'score': 600}, 'cly': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 600}, 'syr': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 550}, 'naf': {'supply': False, 'type': 'Coast', 'owner': '', 'score': 500}}

territories = {"min":{"type":"Sea","supply":False,"owner":""},"nth":{"type":"Sea","supply":False,"owner":""},"sco":{"type":"Coast","supply":True,"owner":""},"was":{"type":"Sea","supply":False,"owner":""},"num":{"type":"Coast","supply":False,"owner":""},"pal":{"type":"Coast","supply":False,"owner":""},"iri":{"type":"Sea","supply":False,"owner":""},"bch":{"type":"Sea","supply":False,"owner":""},"ech":{"type":"Sea","supply":False,"owner":""},"dov":{"type":"Sea","supply":False,"owner":""},"atl":{"type":"Sea","supply":False,"owner":""},"med":{"type":"Sea","supply":False,"owner":""},"bis":{"type":"Sea","supply":False,"owner":""},"sav":{"type":"Coast","supply":False,"owner":""},"pro":{"type":"Coast","supply":False,"owner":""},"tou":{"type":"Coast","supply":True,"owner":"FRA"},"ara":{"type":"Coast","supply":False,"owner":""},"cas":{"type":"Coast","supply":True,"owner":""},"guy":{"type":"Coast","supply":True,"owner":"ENG"},"brt":{"type":"Coast","supply":True,"owner":""},"nmd":{"type":"Coast","supply":True,"owner":"ENG"},"cal":{"type":"Coast","supply":True,"owner":"ENG"},"fla":{"type":"Coast","supply":True,"owner":"BUR"},"hol":{"type":"Coast","supply":True,"owner":"BUR"},"fri":{"type":"Coast","supply":False,"owner":""},"wal":{"type":"Coast","supply":False,"owner":""},"dev":{"type":"Coast","supply":True,"owner":"ENG"},"lon":{"type":"Coast","supply":True,"owner":"ENG"},"ang":{"type":"Coast","supply":False,"owner":""},"lux":{"type":"Land","supply":True,"owner":"BUR"},"dij":{"type":"Land","supply":True,"owner":"BUR"},"par":{"type":"Land","supply":True,"owner":"FRA"},"orl":{"type":"Land","supply":True,"owner":"FRA"},"dau":{"type":"Land","supply":True,"owner":"FRA"},"can":{"type":"Land","supply":True,"owner":""},"anj":{"type":"Land","supply":False,"owner":""},"poi":{"type":"Land","supply":False,"owner":""},"lim":{"type":"Land","supply":False,"owner":""},"cha":{"type":"Land","supply":False,"owner":""},"lor":{"type":"Land","supply":False,"owner":""},"als":{"type":"Land","supply":False,"owner":""}}


def provinceIndex(territory):
    global territories, paths
    score = 0
    # additive/subtractive effects
    if territories[territory]["supply"]:
        score += 300
    for neighbor in paths[territory]:
        if territories[neighbor]["supply"]:
            score += 150
        for neighborNeighbor in paths[neighbor]:
            if territories[neighborNeighbor]["supply"]:
                score += 50
    
    score += 50 * abs( len(paths[territory]) - 5 )

    return score

def initPaths():
    global paths
    for i in territories.keys():
        paths[i] = []
    f = open('paths3.txt')
    neigh = f.read().split("\n")
    for i in neigh:
        arr = i.split(",")
        paths[arr[0]].append(arr[1])
    f.close()

def buildBoard():
    global units, territories, paths
    # fillPreviousMoves()
    fillUnits()
    fillTerritories()
    # return paths, territories, units

initPaths()

def fillUnits():
    global units
    f = open('units.txt')
    perCountryUnit = f.read().split("\n")
    for i in perCountryUnit:
        unitStrings = i.split("\t")
        for j in range(1, len(unitStrings)):
            if unitStrings[j] == '': break
            units[unitStrings[j][2:5]] = {"owner":unitStrings[0],"type":unitStrings[j][0].lower()}
    f.close()

def fillTerritories():
    global units, territories
    g = open('territories.txt')
    for i in territories.keys():
        territories[i]["owner"] = ""
    perCountryTerr = g.read().split("\n")
    for i in perCountryTerr:
        country = i[0:3]
        terrStrings = i.split(" ")
        for j in range(1, len(terrStrings) - 2):
            territories[terrStrings[j][0:3]]["owner"] = country
    for i in territories.keys():
        territories[i]["score"] = provinceIndex(i)
    # for i in units.keys():
        # territories[i]["owner"] = units[i]["owner"]
    territories = sortByValues(territories, "score")

buildBoard()