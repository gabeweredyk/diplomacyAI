from readJDIP import *
trustDict = {"FRA":1,"ENG":1,"GER":1,"ITL":1,"AUS":1,"RUS":1,"TUR":1}
promisedMoves = {}
R = 1.2



promisedMoves = {
    "RUS":[{"type":"Hold","terr":['sev']}],
    "AUS":[{"type":"Move","terr":['bud', 'rum']}],
    "ENG":[],
    "FRA":[],
    "GER":[],
    "ITL":[], 
    "TUR":[]
}

for i in countries:
    for j in promisedMoves[i]:
        if (j in previousMoves[i]):
            trustDict[i] *= R
        else:
            trustDict[i] /= R

print(trustDict)
