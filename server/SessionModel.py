# Represents a Session in the game server

from time import time
from .game.map import generateMap,generateRessources

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
        self.ressources = generateRessources([(-100,-100),(100,100)],SessionModel.GameEnv.get('ressources',{})) 

    # Players Related

    # Returns player dict
    def getPlayer(self,userid):
        for pl in self.players:
            if pl['id'] == userid:
                return pl
        return {}
    # Adds new player to session
    def insertNewPlayer(self,user):
        # @TODO : Give player starter kit
        # @TODO : init player data right
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
            # @TODO : update players, objects and entities
            return (self.session['last_update'],data) # return updated user data
        return (userlastupdate,None) # User's already updated
    # Updates the session by one or more cycles, depending on last update registered in self.session['last_update']
    def tick(self):
        t = time() * 1000
        if self.session['last_update'] == 0:
            self.session['last_update'] = t
        elif self.session['last_update'] < t:
            dt = t - self.session['last_update']
            if dt >= SessionModel.TickTime:
                ticks = (dt - (dt % SessionModel.TickTime))/SessionModel.TickTime
                # @TODO : Update game by x ticks
                self.session['last_update'] = t

    # Updates the session by a command, and returns update status and changes to client
    def update(self,command):
        pass
