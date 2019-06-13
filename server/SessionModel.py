# Represents a Session in the game server

from time import time
from .game.map import generateMap,generateRessources

def timestamp():
    return time() * 1000

class SessionModel:
    GameEnv = {} # Contains all game elements, loaded from assets/config at runtime in GameServer
    PeriodicWriting = 100 # Data will be written to database every 100th cycle
    TickTime = 200 # Time between to game cycles, in ms
    # Creates a session model, representing a game session on the server
    def __init__(self,sessiondata,players = [],ressources = [],objects = []):
        self.session = sessiondata
        self.players = players
        self.ressources = ressources
        self.objects = objects

    # Static Methods

    # Returns a database ready dict for inserting a new player
    @staticmethod
    def playerDict(ss,lg,pw):
        return {'session':ss,'name':lg,'password':pw,'data':{},'x':0,'y':0}

    # Returns a database ready dict for inserting a new session
    @staticmethod
    def sessionDict():
        return {'last_update':0,'admin':""}

    # Methods

    # Generates new session data, at the creation of a new session
    def generate(self):
        # Generates ressources on the map
        self.ressources = generateRessources([(-100,-100),(100,100)],SessionModel.GameEnv.get('ressources',{}),timestamp())

    # Players Related

    # Returns player dict
    def getPlayer(self,userid):
        for pl in self.players:
            if pl['id'] == userid:
                return pl
        return {}
    # Adds new player to session
    def insertNewPlayer(self,user):
        # Give player starter kit
        user['data']['inventory'] = SessionModel.GameEnv.get('starter')
        # init player data
        user['data']['creation'] = timestamp()
        user['data']['last_update'] = user['data']['creation']
        user['data']['health'] = 100
        user['data']['status'] = {'oxygen':100,'food':100,'stamina':100}
        self.players.append(user)
    # Sets player as server admin
    def setAdmin(self,userid):
        self.session['admin'] = userid
    # Sets a player status to online
    def isOnline(self,playerid):
        self.getPlayer(playerid).get('data',{})['online'] = True
    # Sets a player status to offline
    def isOffline(self,playerid):
        self.getPlayer(playerid).get('data',{})['online'] = False

    # SessionModel data related

    # Packages all session info to send to client loading the game
    def toLoad(self,userid):
        player = self.getPlayer(userid)
        return {
            'players':self.players, # Players
            'objects':self.objects, # Objects
            'ressources':self.ressources, # Ressources
            'map':generateMap(player.get('x',0),player.get('y',0)) # Map around player
        }
    # Packages all session info to update client by one gametick
    def toTick(self,userid,userlastupdate):
        if userlastupdate < self.session['last_update']: # User needs an update
            data = {}
            # return changed elements since user last user update
            data['players']    = [player for player in self.players if player['data']['last_update'] > userlastupdate]
            data['ressources'] = [rs for rs in self.ressources if rs['data']['last_update'] > userlastupdate]
            data['objects']    = [object for object in self.objects if object['data']['last_update'] > userlastupdate]
            return (self.session['last_update'],data) # return updated user data
        return (userlastupdate,None) # User's already updated
    # Updates the session by one or more cycles, depending on last update registered in self.session['last_update']
    def tick(self):
        t = timestamp()
        if self.session['last_update'] == 0:
            self.session['last_update'] = t
        elif self.session['last_update'] < t:
            dt = t - self.session['last_update']
            if dt >= SessionModel.TickTime:
                ticks = (dt - (dt % SessionModel.TickTime))/SessionModel.TickTime
                # Update game by n ticks
                self.session['last_update'] = t

    # Updates the session by a command, and returns update status and changes to client
    def update(self,command):
        pass
