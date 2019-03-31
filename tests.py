import asyncio
import websockets

from json import loads, dumps

register = {'login':'admin','password':'admin','register':1,'newSession':1}
load = {'load':1}

async def testSequence():
    async with websockets.connect('ws://localhost:55555') as websocket:

        await websocket.send(dumps(register))
        print("Sent : " + dumps(register))

        rep = await websocket.recv()
        print("Received : " + rep)

        await websocket.send(dumps(load))
        print("Sent : " + dumps(load))

        rep = await websocket.recv()
        print("Received : " + rep)

        print('\n\nTICKING TEST\n\n')
        while True:
            tick = await websocket.recv()
            print(tick)

asyncio.get_event_loop().run_until_complete(testSequence())
