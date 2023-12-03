
tNames = ['nao', 'nwg', 'bar', 'cly', 'lvp', 'edi', 'yor', 'wal', 'iri', 'mao', 'eng', 'lon', 'nth', 'nwy', 'stp', 'fin', 'swe', 'ska', 'bot', 'den', 'lvn', 'bal', 'hel', 'bre', 'pic', 'bel', 'hol', 'kie', 'par', 'bur', 'ruh', 'ber', 'pru', 'mos', 'war', 'ukr', 'sev', 'mun', 'sil', 'gas', 'spa', 'por', 'mar', 'pie', 'tyr', 'boh', 'gal', 'vie', 'tri', 'ven', 'lyo', 'tus', 'wes', 'naf', 'tun', 'tys', 'rom', 'nap', 'apu', 'adr', 'alb', 'bud', 'ser', 'gre', 'rum', 'bla', 'ank', 'arm', 'syr', 'eas', 'ion', 'bul', 'con', 'aeg', 'smy']

tObjects = [ { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "ENG" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "ENG" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "RUS" }, { "supply": 1, "type": "L", "owner": "ENG" }, { "supply": 1, "type": "C", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "FRA" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "GER" }, { "supply": 1, "type": "L", "owner": "GER" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "FRA" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "RUS" }, { "supply": 1, "type": "L", "owner": "RUS" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "GER" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "FRA" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "RUS" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "AUS" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "AUS" }, { "supply": 1, "type": "L", "owner": "AUS" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 1, "type": "L", "owner": "ITL" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 1, "type": "C", "owner": "TUR" }, { "supply": 1, "type": "L", "owner": "TUR" }, { "supply": 1, "type": "L", "owner": "ITL" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 1, "type": "L", "owner": "TUR" }, { "supply": 1, "type": "L", "owner": "ITL" }, { "supply": 0, "type": "L", "owner": "" }, { "supply": 1, "type": "L", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "W", "owner": "" }, { "supply": 0, "type": "L", "owner": "" } ]

def provinceIndex(territory,territories,paths):
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

def buildBoard():

    paths = dict()
    for i in territories:
        paths[i] = []

    neigh = f.read().split("\n")
    for i in neigh:
        arr = i.split(",")
        paths[arr[0]].append(arr[1])

    territories = dict()

    for i in range(75):
        territories[tNames[i]] = tObjects[i]
    for territory in territories:
        terScore = provinceIndex(territory,territories,paths)
        territories[territory]["score"] = terScore
    


    units = dict()
    units = [ { "loc": "lvp", "owner": "ENG", "type": "A" }, { "loc": "edi", "owner": "ENG", "type": "F" }, { "loc": "lon", "owner": "ENG", "type": "F" }, { "loc": "bre", "owner": "FRA", "type": "F" }, { "loc": "par", "owner": "FRA", "type": "A" }, { "loc": "mar", "owner": "FRA", "type": "A" }, { "loc": "kie", "owner": "GER", "type": "F" }, { "loc": "ber", "owner": "GER", "type": "A" }, { "loc": "mun", "owner": "GER", "type": "A" }, { "loc": "war", "owner": "RUS", "type": "A" }, { "loc": "mos", "owner": "RUS", "type": "A" }, { "loc": "sev", "owner": "RUS", "type": "F" }, { "loc": "stp", "owner": "RUS", "type": "F" }, { "loc": "con", "owner": "TUR", "type": "A" }, { "loc": "ank", "owner": "TUR", "type": "F" }, { "loc": "amy", "owner": "TUR", "type": "A" }, { "loc": "ven", "owner": "ITL", "type": "A" }, { "loc": "rom", "owner": "ITL", "type": "A" }, { "loc": "nap", "owner": "ITL", "type": "F" }, { "loc": "vie", "owner": "AUS", "type": "A" }, { "loc": "bud", "owner": "AUS", "type": "A" }, { "loc": "tri", "owner": "AUS", "type": "F" } ]

    
    return paths, territories, units

