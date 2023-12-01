units = dict()
paths = dict()

territories = {
        "nao": {"supply":False,"type":"W","owner":""},
        "nwg": {"supply":False,"type":"W","owner":""},
        "bar": {"supply":False,"type":"W","owner":""},
        "cly": {"supply":False,"type":"L","owner":""},
        "edi": {"supply":True,"type":"L","owner":"ENG"},
        "nth": {"supply":False,"type":"W","owner":""},
        "nwy": {"supply":True,"type":"L","owner":""},
        "lvp": {"supply":True,"type":"L","owner":"ENG"},
        "iri": {"supply":False,"type":"W","owner":""},
        "yor": {"supply":False,"type":"L","owner":""},
        "wal": {"supply":False,"type":"L","owner":""},
        "ska": {"supply":False,"type":"W","owner":""},
        "swe": {"supply":True,"type":"L","owner":""},
        "fin": {"supply":False,"type":"L","owner":""},
        "stp": {"supply":True,"type":"L","owner":"RUS"},
        "lon": {"supply":True,"type":"L","owner":"ENG"},
        "den": {"supply":True,"type":"C","owner":""},
        "eng": {"supply":False,"type":"W","owner":""},
        "hel": {"supply":False,"type":"W","owner":""},
        "bal": {"supply":False,"type":"W","owner":""},
        "bot": {"supply":False,"type":"W","owner":""},
        "bel": {"supply":True,"type":"L","owner":""},
        "hol": {"supply":True,"type":"L","owner":""},
        "bre": {"supply":True,"type":"L","owner":"FRA"},
        "pic": {"supply":False,"type":"L","owner":""},
        "ruh": {"supply":False,"type":"L","owner":""},
        "kie": {"supply":True,"type":"L","owner":"GER"},
        "ber": {"supply":True,"type":"L","owner":"GER"},
        "pru": {"supply":False,"type":"L","owner":""},
        "lvn": {"supply":False,"type":"L","owner":""},
        "par": {"supply":True,"type":"L","owner":"FRA"},
        "bur": {"supply":False,"type":"L","owner":""},
        "war": {"supply":True,"type":"L","owner":"RUS"},
        "mos": {"supply":True,"type":"L","owner":"RUS"},
        "gas": {"supply":False,"type":"L","owner":""},
        "mun": {"supply":True,"type":"L","owner":"GER"},
        "sil": {"supply":False,"type":"L","owner":""},
        "mar": {"supply":True,"type":"L","owner":"FRA"},
        "tyr": {"supply":False,"type":"L","owner":""},
        "boh": {"supply":False,"type":"L","owner":""},
        "gal": {"supply":False,"type":"L","owner":""},
        "ukr": {"supply":False,"type":"L","owner":""},
        "sev": {"supply":True,"type":"L","owner":"RUS"},
        "pie": {"supply":False,"type":"L","owner":""},
        "vie": {"supply":True,"type":"L","owner":"AUS"},
        "rum": {"supply":True,"type":"L","owner":""},
        "bla": {"supply":False,"type":"W","owner":""},
        "arm": {"supply":False,"type":"L","owner":""},
        "por": {"supply":True,"type":"L","owner":""},
        "spa": {"supply":True,"type":"L","owner":""},
        "tri": {"supply":True,"type":"L","owner":"AUS"},
        "bud": {"supply":True,"type":"L","owner":"AUS"},
        "lyo": {"supply":False,"type":"W","owner":""},
        "ven": {"supply":True,"type":"L","owner":"ITL"},
        "ser": {"supply":True,"type":"L","owner":""},
        "tus": {"supply":False,"type":"L","owner":""},
        "bul": {"supply":True,"type":"L","owner":""},
        "mao": {"supply":False,"type":"W","owner":""},
        "wes": {"supply":False,"type":"W","owner":""},
        "adr": {"supply":False,"type":"W","owner":""},
        "alb": {"supply":False,"type":"L","owner":""},
        "gre": {"supply":True,"type":"L","owner":""},
        "con": {"supply":True,"type":"C","owner":"TUR"},
        "ank": {"supply":True,"type":"L","owner":"TUR"},
        "rom": {"supply":True,"type":"L","owner":"ITL"},
        "apu": {"supply":False,"type":"L","owner":""},
        "tys": {"supply":False,"type":"W","owner":""},
        "aeg": {"supply":False,"type":"W","owner":""},
        "smy": {"supply":True,"type":"L","owner":"TUR"},
        "nap": {"supply":True,"type":"L","owner":"ITL"},
        "naf": {"supply":False,"type":"L","owner":""},
        "tun": {"supply":True,"type":"L","owner":""},
        "ion": {"supply":False,"type":"W","owner":""},
        "eas": {"supply":False,"type":"W","owner":""},
        "syr": {"supply":False,"type":"L","owner":""}
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
    f = open('units.txt')
    perCountryUnit = f.read().split("\n")
    n = 0
    for i in perCountryUnit:
        unitStrings = i.split("\t")
        for j in range(1, len(unitStrings)):
            if unitStrings[j] == '': break
            units[n] = {"loc":unitStrings[j][2:5],"owner":unitStrings[0],"type":unitStrings[j][0]}
            n += 1
    f.close()

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

    return paths, territories, units

initPaths()

print(buildBoard())