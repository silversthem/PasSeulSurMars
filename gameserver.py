# Game Server using websockets

import sys
import asyncio
import websockets
import sqlite3
import logging
from time import sleep
from logging.handlers import RotatingFileHandler

from server.GameServer import GameServer

DBNAME = 'db.sqlite'
TICKRATE = 200 # Amount of time between 2 cycles in sessions
LOG = logging.getLogger()

# Logger config
LOG.setLevel(logging.INFO)
logformatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
LOGFILE = RotatingFileHandler('server.log', 'a', 1000000, 1)
# Log file
LOGFILE.setLevel(logging.INFO)
LOGFILE.setFormatter(logformatter)
# Log Stream
LOGSTREAM = logging.StreamHandler()
LOGSTREAM.setLevel(logging.INFO)
# Adding handlers
LOG.addHandler(LOGFILE)
LOG.addHandler(LOGSTREAM)

if len(sys.argv) > 1:
    DBNAME = sys.argv[1] + '.sqlite'

DB = sqlite3.connect(DBNAME)

gameServer = GameServer(DB,LOG,TICKRATE)

# Main Server Feedback Loop
async def main(sock, path):
    authed = await gameServer.auth(sock) # Auths new user
    if authed: # User successfully authed
        while True: # Main User Feedback loop
            try:
                await gameServer.update(sock) # handle update
            except websockets.exceptions.ConnectionClosed: # Socket closed -> disconnect user
                gameServer.logout(sock)
                break
            except (KeyboardInterrupt, SystemExit): # Server stopped
                break # @TODO : handle exit

# Main Cycle Loop
async def cycle():
    while True:
        try:
            await gameServer.cycle()
            await asyncio.sleep(0.02) # Sleeps for a lil bit to free cpu
        except (KeyboardInterrupt, SystemExit): # Server stopped
            break # @TODO : handle exit

# Server starts running here
asyncio.get_event_loop().run_until_complete(websockets.serve(main, 'localhost', 55555))
asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(cycle()))
asyncio.get_event_loop().run_forever()
