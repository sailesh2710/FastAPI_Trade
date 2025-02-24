import asyncio
import websockets

async def listen():
    async with websockets.connect("ws://localhost:8000/ws/orders") as websocket:
        while True:
            message = await websocket.recv()
            print(f"🔔 New Order Received: {message}")

asyncio.run(listen())