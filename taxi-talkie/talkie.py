#!/usr/bin/env python

import asyncio
import websockets
import uuid

car_id = uuid.uuid4()


async def hello():
    print(f"registering for id {car_id}")
    uri = f"ws://localhost:9876/{car_id}"
    async with websockets.connect(uri) as websocket:
        await websocket.send("register")
        result = await websocket.recv()
        print(f"{result}")
        while True:
            try:
                msg = str(await websocket.recv()).strip()
                print(msg)
                if msg == "kill":
                    await websocket.send("kill confirm")
                    break
            except websockets.ConnectionClosed:
                print(f"Terminated")
                break


asyncio.get_event_loop().run_until_complete(hello())
