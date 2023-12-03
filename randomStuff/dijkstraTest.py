'''
this entire file is just a test for the Dijkstra algorithm, don't worry about it!
'''

from analyzeMoves import absDistBetweenTerritories
from analyzeMoves import shortestPath


italyPaths = {"tyr":set(["pie","ven","tri"]),"pie":set(["tus","ven","tyr"]),"tri":set(["tyr","ven","adr","alb"]),
              "ven":set(["pie","tyr","tri","adr","rom","tus"]),"tus":set(["pie","ven","rom"]),
              "adr":set(["tri","ven","apu","ion","alb"]),"alb":set(["ion","adr","tri"]),
              "ion":set(["nap","apu","adr","alb","rom"]),"apu":set(["ven","adr","ion","nap","rom"]),
              "rom":set(["nap","apu","ven","tus"]),"nap":set(["rom","apu","ion"])}
italyTers = italyPaths.keys()

while True:
    terA = input("Starting territory's three-letter code (stop to stop): ").strip().lower()
    if terA.lower() == "stop":
        break
    terB = input("Target territory's three-letter code: ").strip().lower()
    if terA not in italyTers or terB not in italyTers:
        print("Invalid, try again")
        continue
    previousNodes, shortPath = absDistBetweenTerritories(terA,italyPaths,italyTers)
    goodPath = shortestPath(terA,terB,previousNodes)

    print(shortPath)

    print("Best path has a value of {}".format(shortPath[terB]))
    print("Best path:", goodPath)