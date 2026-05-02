import asyncio
import json
import websockets
from gep.main import run_simulation_async

class WebSocketManager:
    def __init__(self):
        self.active_connections = set()
        self.loop = None
        self.simulation_running = False
    
    async def connect(self, websocket):
        self.active_connections.add(websocket)
        print(f"Nuevo cliente conectado. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Cliente desconectado. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
            
        disconnected = set()
        msg_str = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send(msg_str)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(connection)
                
        for d in disconnected:
            self.disconnect(d)

    def broadcast_from_sync(self, message: dict):
        """Called from a sync thread to broadcast to async websockets"""
        if not self.loop:
            return
        asyncio.run_coroutine_threadsafe(self.broadcast(message), self.loop)

manager = WebSocketManager()

async def handler(websocket):
    await manager.connect(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data.get("type") == "START_SIMULATION":
                if not manager.simulation_running:
                    print("Comando de inicio recibido desde frontend.")
                    manager.simulation_running = True
                    # Run simulation in a background thread so we don't block the async loop
                    asyncio.get_running_loop().run_in_executor(None, run_simulation_async, manager)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        manager.disconnect(websocket)

async def main_server():
    manager.loop = asyncio.get_running_loop()
    print("Iniciando servidor WebSocket en ws://0.0.0.0:8080")
    async with websockets.serve(handler, "0.0.0.0", 8080):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main_server())
