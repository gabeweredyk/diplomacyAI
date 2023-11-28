from analyzeMoves import *
from buildBoard import provinceIndex
from buildCountries import buildCountries

countries = ["AUS","RUS","TUR"]
trustDict = {"FRA":1,"ENG":1,"GER":1,"ITL":1,"AUS":1,"RUS":1,"TUR":1}

boardSectorTers = {"mos":{"supply":True,"type":"Land","owner":"RUS"},"war":{"supply":True,"type":"Land","owner":"RUS"},
                   "gal":{"supply":False,"type":"Land","owner":"AUS"},"ukr":{"supply":False,"type":"Land","owner":"RUS"},
                   "sev":{"supply":True,"type":"Coast","owner":"RUS"},"arm":{"supply":False,"type":"Coast","owner":"None"},
                   "bla":{"supply":False,"type":"Sea","owner":"None"},"rum":{"supply":True,"type":"Coast","owner":"None"},
                   "bud":{"supply":True,"type":"Land","owner":"AUS"},"ser":{"supply":True,"type":"Land","owner":"None"},
                   "alb":{"supply":False,"type":"Coast","owner":"None"},"gre":{"supply":True,"type":"Coast","owner":"None"},
                   "bul":{"supply":True,"type":"Coast","owner":"None"},"con":{"supply":True,"type":"Coast","owner":"TUR"},
                   "ank":{"supply":True,"type":"Coast","owner":"None"},"ion":{"supply":False,"type":"Sea","owner":"None"},
                   "aeg":{"supply":False,"type":"Sea","owner":"None"},"smy":{"supply":True,"type":"Coast","owner":"None"},
                   "syr":{"supply":False,"type":"Coast","owner":"None"},"eas":{"supply":False,"type":"Sea","owner":"None"}}

boardSectorPaths = {"mos":set(["war","ukr","sev"]),"war":set(["mos","ukr","gal"]),"gal":set(["war","ukr","rum","bud"]),
                    "ukr":set(["war","mos","sev","rum","gal"]),"sev":set(["mos","ukr","rum","bla","arm"]),
                    "arm":set(["sev","bla","ank","smy","syr"]),"bla":set(["sev","arm","ank","con","bul","rum"]),
                    "rum":set(["gal","bud","ser","bul","bla","sev","ukr"]),"bud":set(["gal","rum","ser"]),
                    "ser":set(["bud","rum","bul","gre","alb"]),"alb":set(["ser","gre","ion"]),"gre":set(["ser","alb","ion","aeg","bul"]),
                    "bul":set(["rum","bla","con","aeg","gre","ser"]),"con":set(["bul","bla","ank","smy","aeg"]),
                    "ank":set(["bla","arm","smy","con"]),"ion":set(["alb","gre","aeg","eas"]),"aeg":set(["ion","gre","bul","con","smy","eas"]),
                    "smy":set(["eas","aeg","con","ank","arm","syr"]),"syr":set(["arm","smy","eas"]),"eas":set(["syr","smy","aeg","ion"])}

for territory in boardSectorTers:
        terScore = provinceIndex(territory,boardSectorTers,boardSectorPaths)
        boardSectorTers[territory]["score"] = terScore

units = {"1":{"loc":"war","owner":"RUS","type":"a"},"2":{"loc":"mos","owner":"RUS","type":"a"},
         "3":{"loc":"sev","owner":"RUS","type":"f"},"4":{"loc":"bud","owner":"AUS","type":"a"},
         "5":{"loc":"con","owner":"TUR","type":"a"},"6":{"loc":"ank","owner":"TUR","type":"f"},
         "7":{"loc":"smy","owner":"TUR","type":"a"}}

players = buildCountries(trustDict,units,countries)

moves = analyzeMovesInitial(players,"TUR",boardSectorTers,boardSectorPaths)
print(moves)