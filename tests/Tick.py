from testing.context import *
from json import loads, dumps
import asyncio
from sys import argv

c = 0 if len(argv) == 1 else 1

async def testSeq(client,login):
    await client.send(dumps(login))
    rep = await client.recv()
    await client.send(dumps(loadCommand))
    loadedGame = loads(await client.recv())
    # ...

async def testSeq1():
    client1 = await getSocket()
    await testSeq(client1,loginValid11)

async def testSeq2():
    client2 = await getSocket()
    await testSeq(client2,loginValid12)

asyncio.get_event_loop().run_until_complete(testSeq1())
asyncio.get_event_loop().run_until_complete(testSeq2())
