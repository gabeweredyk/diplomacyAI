from readJDIP import *
# trust = {"FRA":1,"ENG":1,"GER":1,"ITL":1,"AUS":1,"RUS":1,"TUR":1}
R = 1.2

def updateSocialValues():
    global previousMoves, self
    fillPreviousMoves()
    increaseTerrValues(previousMoves)
    updateTrust(self)    

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

def updateTrust(country):
    global promisedMoves, previousMoves, trust
    previousMoves = fillPreviousMoves()
    for i in countries:
        if i == country: continue
        for j in promisedMoves[i]:
            if (j in previousMoves[i]):
                trust[i] *= R
            else:
                trust[i] /= R
    # print("Updated trust: " + str(trust))

def increaseTerrValues(moves):
    global territories, self, attemptedMoves
    interests = {}
    for i in territories:
        interests[i] = 0
    for i in moves:
        interests[i["terr"][-1]] += 1
    for i in attemptedMoves:
        interests[i["terr"][-1]] -= 1
    for terr, intertest in interests.items():
        territories[terr]["score"] *= 1 + intertest/20