import asyncio
import websocket
from buildBoard import buildBoard

async def gameloop(socket, created):
    active = True

    while active:
        


if __name__ == "__main__":
    server = input("Server IP: ").strip()
    protocol = input("Join game or create game? (j/c): ").strip()