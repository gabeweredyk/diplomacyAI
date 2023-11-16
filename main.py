import asyncio
import websocket

if __name__ == "__main__":
    server = input("Server IP: ").strip()
    protocol = input("Join game or create game? (j/c): ").strip()