import asyncio
import websocket
from buildBoard import buildBoard
from analyzeMoves import *

countries = ["FRA","ENG","GER","ITL","AUS","RUS","TUR"]
trustDict = {"FRA":1,"ENG":1,"GER":1,"ITL":1,"AUS":1,"RUS":1,"TUR":1}

async def gameloop(socket, created):
    active = True

    while active:
        


if __name__ == "__main__":
    