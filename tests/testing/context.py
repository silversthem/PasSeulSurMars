# Stores dicts used for testing and default socket functions

import asyncio
import websockets
from json import loads, dumps

# Users

loginValid11 = {'login':'newUserAdmin1','password':'shouldbehashed','session':1}
registerNewValid11 = {'login':'newUserAdmin1','password':'shouldbehashed','register':1,'newSession':1}

loginValid11Response = {'auth':1,'pid':1}
registerNewValid11Response = {'register':1,'session':1,'pid':1}

loginWrong111 = {'login':'newUserAdmin1','password':'shouldbehashedandwrong','session':1}
loginWrong112 = {'login':'notNewUserAdmin1','password':'shouldbehashed','session':1}

loginWrongResponse = {'auth':0}

loginValid12 = {'login':'newUser1','password':'shouldbehashed','session':1}
registerValid12 = {'login':'newUser1','password':'shouldbehashed','register':1,'session':1}

loginValid12Response = {'auth':1,'pid':2}
registerValid12Response = {'register':1,'session':1,'pid':2}

loginValid21 = {'login':'newUserAdmin2','password':'shouldbehashed','session':2}
registerNewValid21 = {'login':'newUserAdmin2','password':'shouldbehashed','register':1,'newSession':1}

loginValid21Response = {'auth':1,'pid':3}
registerNewValid21Response = {'register':1,'session':2,'pid':3}

loginValid22 = {'login':'newUser2','password':'shouldbehashed','session':2}
registerValid22 = {'login':'newUser2','password':'shouldbehashed','register':1,'session':2}

loginValid22Response = {'auth':1,'pid':4}
registerValid22Response = {'register':1,'session':2,'pid':4}

registerWrong2 = {'login':'newUser2','password':'shouldbehashed','session':2,'register':1}

registerWrongResponse = {'register':0}

# Commands

loadCommand = {'load':1}

# Functions

def getSocket():
    return websockets.connect('ws://localhost:55555')

def runTestsSequence(dataIn,expectedDataOut):
    r = []
    async def testSequence():
        async with getSocket() as websocket:
            for i in range(len(dataIn)):
                await websocket.send(dumps(dataIn[i]))
                rep = await websocket.recv()
                if loads(rep) == expectedDataOut[i]:
                    r.append(1)
                else:
                    r.append(0)
    asyncio.get_event_loop().run_until_complete(testSequence())
    return r
