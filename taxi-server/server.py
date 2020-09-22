#!/usr/bin/env python

import asyncio
import aioconsole
import websockets


car_sockets: dict = {}


async def hello(websocket: websockets.WebSocketServerProtocol, path: str):
    global car_sockets
    car_id = path[-36:]
    while True:
        try:
            name = await websocket.recv()
            print(name)
            if name == 'register':
                car_sockets[car_id] = websocket
                await websocket.send("OK")
            elif name == 'kill confirm':
                car_sockets.pop(car_id)
                break
        except websockets.ConnectionClosed:
            print("Terminated by client")
            break


async def send_car_command(car_id: str, command: str):
    global car_sockets
    if car_sockets[car_id] is not None:
        await car_sockets[car_id].send(command)


async def read_command():
    global car_sockets
    stdin, stdout = await aioconsole.get_standard_streams()
    async for line in stdin:
        for car_id in car_sockets:
            try:
                await car_sockets[car_id].ensure_open()
                await car_sockets[car_id].send(str(line, encoding="utf-8", errors="strict"))
            except websockets.exceptions.ConnectionClosed:
                print(f"socket for id {car_id} is closed")


start_server = websockets.serve(hello, "localhost", 9876)

asyncio.get_event_loop().run_until_complete(start_server)
print("running server done")
asyncio.get_event_loop().run_until_complete(read_command())
asyncio.get_event_loop().run_forever()
