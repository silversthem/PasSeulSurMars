from json import dumps, loads
from math import fabs

RUNSPEED = 5 # Run speed in seconds

# Generates player
def generatePlayer():
    return {'online':True,'inMotion':False,'toward':{'x':0,'y':0}}

# Updates player data
def updatePlayer(delta,pl):
    # Handles motion
    if pl['data']['inMotion']:
        dx = int(pl['data']['toward']['x']) - int(pl['x'])
        dy = int(pl['data']['toward']['y']) - int(pl['y'])
        ix = 0 if (dx == 0) else (dx/fabs(dx))
        iy = 0 if (dy == 0) else (dy/fabs(dy))
        pl['x'] = (int(pl['x']) + RUNSPEED*ix) if (fabs(dx) > RUNSPEED) else (int(pl['x']) + dx)
        pl['y'] = (int(pl['y']) + RUNSPEED*iy) if (fabs(dy) > RUNSPEED) else (int(pl['y']) + dy)
        pl['data']['inMotion'] = not (int(pl['x']) == int(pl['data']['toward']['x']) and int(pl['y']) == int(pl['data']['toward']['y']))
