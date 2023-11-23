import mysql
import pandas as pd

def buildBoard(hostname, username, password):
    db = mysql.connector.connect(host="f{hostname}",user="f{username}",password="f{password}")
    crsr = db.cursor()

    pathsFromDB = pd.read_sql("SELECT * FROM paths", db):
    paths = dict()
    for index, row in pathsFromDB.iterrows():
        paths[row["nodeA"]] = paths[row["nodeB"]]

    territoriesFromDB = pd.read_sql("SELECT * FROM territories", db)
    territories = dict()
    for index, row in territoriesFromDB.iterrows():
        territories[row["name"]] = {"supply":row["supply"],"type":row["type"],"owner":row["owner"]}
    
    unitsFromDB = pd.read_sql("SELECT * FROM units", db)
    units = dict()
    for index, row in unitsFromDB.iterrows():
        units[row["id"]] = {"loc":row["territory"],"owner":row["owner"],"type":row["type"]}
    
    return paths, territories, units