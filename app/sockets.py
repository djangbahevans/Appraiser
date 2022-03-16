from fastapi import WebSocket
from typing import List

# DEFINE CONNECTION MANAGER CLASS
class ConnectionManager:
    def __init__(self):
        self.active_connections:List[WebSocket] = []

    async def connect(self, websocket:WebSocket, client_id:int): # CONNECT CLIENT TO WEBSOCKET
        websocket.cookies.update({'client_id':client_id})
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket:WebSocket): # DISCONNECT CLIENT FROM WEBSOCKET
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message:str, websocket:WebSocket):
        await websocket.send_text(message)

    async def send_personal_json(self, message:dict, websocket:WebSocket):
        await websocket.send_json(message)

    async def send_private_message(self, message:str, client_id:int):
        websocket = await self.get_client_websocket(self, client_id)
        if websocket:
            await websocket.send_text(message)
    
    async def send_private_json(self, message:dict, client_id:int):
        websocket = await self.get_client_websocket(self, client_id)
        if websocket:
            await websocket.send_json(message)

    async def broadcast(self, message:str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, message:dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def get_client_websocket(self, client_id:int):
        socket = [websocket for websocket in self.active_connections if websocket.cookies.get('client_id')==client_id]
        return socket[0] if len(socket) else None

manager = ConnectionManager()
