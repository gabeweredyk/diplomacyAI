#    for player in requestedMoves.keys():
#         for request in requestedMoves[country]:
#             if request in moves:
#                 replies[player].append("Affirmative")
#                 externalTrust[player] *= 1.2
#                 continue
#             if request["type"] == "Convoy":
#                 replies[player].append("Negative")
#                 externalTrust[player] /= 1.2
#                 continue
#             if request["type"] == "Support":
#                 attacked = request["terr"][2]
#                 if territories[attacked]["owner"] == country or trust[territories[attacked]["owner"]] > trust[player]:
#                     replies[player].append("Negative")
#                     externalTrust[player] /= 1.2
#                 else:
#                     replies[player].append("Affirmative")
#                     externalTrust[player] *= 1.2
    
#     messagesToSend = {}
#     for i in countries:
#         messagesToSend[i] = ""

#     for i in otherStrengths.keys():
#         if territories[i]["owner"] == "" or territories[i]["owner"] == country: continue
#         if messagesToSend[territories[i]["owner"]] != "": continue
#         unitType = ''
        
#         for j in units.values():
#             if j["owner"] == territories[i]["owner"] and j["loc"] == i:
#                 unitType = j["type"]
#         if unitType == '': continue
#         unitType = {"a":"Army", "f":"Fleet"}[unitType]
#         for j in paths[i]:
#             if j in otherStrengths.keys(): continue
#             if (territories[j]["type"] == "Land" and unitType == "Fleet") or (territories[j]["type"] == "Sea" and unitType == "Army"): continue
#             messagesToSend[territories[i]["owner"]] = "You should move your " + unitType + " from **" + i + "** to **" + j + "**." 
#             for k in range(len(moves)):
#                 if moves[k]["type"] != "Hold": continue
#                 if moves[k]["terr"][0] not in paths[j]: continue
#                 messagesToSend[territories[i]["owner"]] += " In return, I'll support your " + unitType + " in **" + i + "** advancing into **" + j + "** with the unit in **" + k + "**."
#                 moves[k] == {"type":"Support","terr":[moves[k]["terr"][0],i, j]}

#     needsSupport = {}
#     for i in moves:
#         if i["type"] != "Move": continue
#         unitType = ""
#         for j in units.values():
#             if j["loc"] != i["terr"][0]: continue
#             unitType = j["type"]
#         unitType = {"a":"Army", "f":"Fleet"}[unitType]
#         needsSupport[i["terr"][1]] = {"type":unitType,"from":i["terr"][0]}


#     for i in needsSupport.keys():
#         for j in units.values():
#             if j["loc"] not in paths[i]: continue
#             if j["owner"] == country: continue
#             if messagesToSend[j["owner"]] != "": continue
#             messagesToSend[j["owner"]] = "We should support the " + needsSupport[i]["type"] + " in **" + needsSupport[i]["from"] + "** advancing into **" + i + "** with the unit in **" + j["loc"] + "**."
#     print(netStrengths)

#     print("Moves: " + str(moves)) 
#     print("Messages: " + str(messagesToSend))
#     print("Replies: " +  str(replies))

    

# def resolveMoves(moves):
#     terr = {}
#     for i in range(len(moves)):
#         if moves[i]["terr"][0] == moves[i]["terr"][1]:
#             moves[i] = {"type":"Hold","terr":[ moves[i]["terr"][0] ]}
#             terr[ moves[i]["terr"][0] ] = moves[i]["terr"][0] 
#     for i in range(len(moves)):
#         if moves[i]["type"] != "Move": continue
#         if moves[i]["terr"][1] in list(terr.keys()):
#             moves[i] = {"type":"Support","terr":[moves[i]["terr"][0], terr[moves[i]["terr"][1]], moves[i]["terr"][1]]}
#         else:
#             terr[moves[i]["terr"][1]] = moves[i]["terr"][0]
#     return moves