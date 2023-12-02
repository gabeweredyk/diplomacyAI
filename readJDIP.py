units = dict()
paths = dict()
previousMoves = dict()

countries = ["AUS", "ENG", "FRA", "GER", "ITL", "RUS", "TUR"]

territories = {
        "nao": {"supply":False,"type":"Sea","owner":""},
        "nwg": {"supply":False,"type":"Sea","owner":""},
        "bar": {"supply":False,"type":"Sea","owner":""},
        "cly": {"supply":False,"type":"Coast","owner":""},
        "edi": {"supply":True,"type":"Coast","owner":"ENG"},
        "nth": {"supply":False,"type":"Sea","owner":""},
        "nwy": {"supply":True,"type":"Coast","owner":""},
        "lvp": {"supply":True,"type":"Coast","owner":"ENG"},
        "iri": {"supply":False,"type":"Sea","owner":""},
        "yor": {"supply":False,"type":"Coast","owner":""},
        "wal": {"supply":False,"type":"Coast","owner":""},
        "ska": {"supply":False,"type":"Sea","owner":""},
        "swe": {"supply":True,"type":"Coast","owner":""},
        "fin": {"supply":False,"type":"Coast","owner":""},
        "stp": {"supply":True,"type":"Coast","owner":"RUS"},
        "lon": {"supply":True,"type":"Coast","owner":"ENG"},
        "den": {"supply":True,"type":"Coast","owner":""},
        "eng": {"supply":False,"type":"Sea","owner":""},
        "hel": {"supply":False,"type":"Sea","owner":""},
        "bal": {"supply":False,"type":"Sea","owner":""},
        "bot": {"supply":False,"type":"Sea","owner":""},
        "bel": {"supply":True,"type":"Coast","owner":""},
        "hol": {"supply":True,"type":"Coast","owner":""},
        "bre": {"supply":True,"type":"Coast","owner":"FRA"},
        "pic": {"supply":False,"type":"Coast","owner":""},
        "ruh": {"supply":False,"type":"Land","owner":""},
        "kie": {"supply":True,"type":"Coast","owner":"GER"},
        "ber": {"supply":True,"type":"Coast","owner":"GER"},
        "pru": {"supply":False,"type":"Coast","owner":""},
        "lvn": {"supply":False,"type":"Coast","owner":""},
        "par": {"supply":True,"type":"Land","owner":"FRA"},
        "bur": {"supply":False,"type":"Land","owner":""},
        "war": {"supply":True,"type":"Land","owner":"RUS"},
        "mos": {"supply":True,"type":"Land","owner":"RUS"},
        "gas": {"supply":False,"type":"Coast","owner":""},
        "mun": {"supply":True,"type":"Land","owner":"GER"},
        "sil": {"supply":False,"type":"Land","owner":""},
        "mar": {"supply":True,"type":"Coast","owner":"FRA"},
        "tyr": {"supply":False,"type":"Land","owner":""},
        "boh": {"supply":False,"type":"Land","owner":""},
        "gal": {"supply":False,"type":"Land","owner":""},
        "ukr": {"supply":False,"type":"Land","owner":""},
        "sev": {"supply":True,"type":"Coast","owner":"RUS"},
        "pie": {"supply":False,"type":"Coast","owner":""},
        "vie": {"supply":True,"type":"Land","owner":"AUS"},
        "rum": {"supply":True,"type":"Coast","owner":""},
        "bla": {"supply":False,"type":"Sea","owner":""},
        "arm": {"supply":False,"type":"Coast","owner":""},
        "por": {"supply":True,"type":"Coast","owner":""},
        "spa": {"supply":True,"type":"Coast","owner":""},
        "tri": {"supply":True,"type":"Coast","owner":"AUS"},
        "bud": {"supply":True,"type":"Land","owner":"AUS"},
        "lyo": {"supply":False,"type":"Sea","owner":""},
        "ven": {"supply":True,"type":"Coast","owner":"ITL"},
        "ser": {"supply":True,"type":"Land","owner":""},
        "tus": {"supply":False,"type":"Coast","owner":""},
        "bul": {"supply":True,"type":"Coast","owner":""},
        "mao": {"supply":False,"type":"Sea","owner":""},
        "wes": {"supply":False,"type":"Sea","owner":""},
        "adr": {"supply":False,"type":"Sea","owner":""},
        "alb": {"supply":False,"type":"Coast","owner":""},
        "gre": {"supply":True,"type":"Coast","owner":""},
        "con": {"supply":True,"type":"Coast","owner":"TUR"},
        "ank": {"supply":True,"type":"Coast","owner":"TUR"},
        "rom": {"supply":True,"type":"Coast","owner":"ITL"},
        "apu": {"supply":False,"type":"Coast","owner":""},
        "tys": {"supply":False,"type":"Sea","owner":""},
        "aeg": {"supply":False,"type":"Sea","owner":""},
        "smy": {"supply":True,"type":"Coast","owner":"TUR"},
        "nap": {"supply":True,"type":"Coast","owner":"ITL"},
        "naf": {"supply":False,"type":"Coast","owner":""},
        "tun": {"supply":True,"type":"Coast","owner":""},
        "ion": {"supply":False,"type":"Sea","owner":""},
        "eas": {"supply":False,"type":"Sea","owner":""},
        "syr": {"supply":False,"type":"Coast","owner":""}
    }

def provinceIndex(territory):
    global territories, paths
    score = 0
    # additive/subtractive effects
    if territories[territory]["supply"]:
        score += 200
    if territories[territory]["owner"] == "None":
        score += 100
    for neighbor in paths[territory]:
        if territories[neighbor]["supply"]:
            score += 100
        if territories[neighbor]["owner"] == "None":
            score += 50
        for neighborNeighbor in paths[neighbor]:
            if territories[neighborNeighbor]["supply"]:
                score += 50
            if territories[neighborNeighbor]["owner"] == "None":
                score += 25
            for neighborNeighborNeighbor in paths[neighborNeighbor]:
                if territories[neighborNeighborNeighbor]["supply"]:
                    score += 25
                if territories[neighborNeighborNeighbor]["owner"] == "None":
                    score += 10
    return score

def initPaths():
    global paths
    for i in territories.keys():
        paths[i] = []
    f = open('neighbors.txt')
    neigh = f.read().split("\n")
    for i in neigh:
        arr = i.split(",")
        paths[arr[0]].append(arr[1])
    f.close()

def buildBoard():
    global units, territories, paths
    fillPreviousMoves()
    fillUnits()
    fillTerritories()
    return paths, territories, units

initPaths()


def fillPreviousMoves():
    global previousMoves, countries
    for i in countries:
        previousMoves[i] = []
    f = open('previousMoves.txt')
    potMoves = f.read().split("\n")
    for i in potMoves:
        if (i[0:3] not in countries or len(i) == 4) : continue
        moveType = ""
        terr = []
        terr.append(i[7:10])
        if ("Holds" in i):
            moveType = "Hold"
        elif ("Supports" in i):
            moveType = "Support"
            terr.append(i[-10:-7])
            terr.append(i[-3:])
        elif ("Convoys" in i):
            moveType = "Convoy"
            terr.append(i[-10:-7])
            terr.append(i[-3:])
        else:
            moveType = "Move"
            terr.append(i[-3:])
        previousMoves[i[0:3]].append({"type":moveType,"terr":terr})        
    f.close()

def fillUnits():
    global units
    f = open('units.txt')
    perCountryUnit = f.read().split("\n")
    n = 0
    for i in perCountryUnit:
        unitStrings = i.split("\t")
        for j in range(1, len(unitStrings)):
            if unitStrings[j] == '': break
            units[n] = {"loc":unitStrings[j][2:5],"owner":unitStrings[0],"type":unitStrings[j][0].lower()}
            n += 1
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
    for i in units.values():
        territories[i["loc"]]["owner"] = i["owner"]
    
    for i in territories.keys():
        territories[i]["score"] = provinceIndex(i)

buildBoard()

print(units)