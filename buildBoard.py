import mysql
import pandas as pd

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

def buildBoard(hostname, username, password):
    db = mysql.connector.connect(host="f{hostname}",user="f{username}",password="f{password}")
    crsr = db.cursor()

    pathsFromDB = pd.read_sql("SELECT * FROM paths", db)
    paths = dict()
    for index, row in pathsFromDB.iterrows():
        paths[row["nodeA"]] = row["nodeB"]

    territoriesFromDB = pd.read_sql("SELECT * FROM territories", db)
    territories = dict()
    for index, row in territoriesFromDB.iterrows():
        territories[row["name"]] = {"supply":row["supply"],"type":row["type"],"owner":row["owner"]}
    for territory in territories:
        terScore = provinceIndex(territory,territories,paths)
        territories[territory]["score"] = terScore
    
    unitsFromDB = pd.read_sql("SELECT * FROM units", db)
    units = dict()
    for index, row in unitsFromDB.iterrows():
        units[row["id"]] = {"loc":row["territory"],"owner":row["owner"],"type":row["type"]}
    
    return paths, territories, units