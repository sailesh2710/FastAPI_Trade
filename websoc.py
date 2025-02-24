import asyncio
import websockets

async def listen():
    async with websockets.connect("ws://3.93.163.119:8000/ws/orders") as websocket:
        while True:
            message = await websocket.recv()
            print(f"🔔 New Order Received: {message}")

asyncio.run(listen())