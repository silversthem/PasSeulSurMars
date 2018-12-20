# Represents a game session
# Bridges the gap between game logic and database

from time import time # timestamp
import hashlib # hashing passwords in database

from .sql import select, insert, update
from .game.Game import Game
from .game.chatbot import chatbot
from .game.map import generateMap,generateRessources
from .game.objects import cycle
from .game.player import update_player

def sha(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

class Session:
    def __init__(self,db,token = None): # Creates a session
        self.db = db
        self.token = token
        if token is not None:
            s = select(self.db,'SELECT * FROM Session WHERE id = ?',(self.token))[0]
            self.last_update = s['last_update']
            self.session_admin = s['admin']
    # Session & User related
    def login(self,username,pwd): # Logs in user and returns player id, returns -1 if unable to
        return select(self.db,'SELECT id FROM Player WHERE session = ? AND name = ? AND password = ?',(self.token,username,sha(pwd)))[0].get('id',-1)
    def create(self): # Create new session
        # Creating new session in db
        insert(self.db,'Session',(None,0,None))
        # Fetching session id
        self.token = select(self.db,'SELECT id FROM Session ORDER BY id DESC LIMIT 1')[0].get('id')
        self.last_update = 0
        self.session_admin = None
        return self.token
    def set_admin(self,pid): # Sets player with id pid as admin of this session
        update(self.db,'Session','id = ?',[self.token],{'admin':pid})
        self.session_admin = pid
    def add_new_player(self,username,password): # Adds a new player to this session, returns player id
        insert(self.db,'Player',(None,self.token,username,sha(password),0,0,"{}"))
        return select(self.db,'SELECT id FROM Player ORDER BY id DESC LIMIT 1')[0].get('id')
    def fill_session(self,session,pid): # Fills a flask session to maintain connexion
        session["player_id"] = pid
    # Game database reading
    def get_session_data(self,table,cols = '*'): # Returns a table from a session
        return select(self.db,'SELECT ' + cols + ' FROM ' + table + ' WHERE session = ?',(self.token))
    # Game database writing
    def update_last_update(self):
        update(self.db,'Session','id = ?',[self.token],{'last_update':int(time())})
    def write_ressources(self,rs):
        for r in rs:
            insert(self.db,'Ressource',(None,self.token,r[2],r[0],r[1],r[3]))
    # Main sesssion functions
    def load(self,pid): # Loads game
        s = select(self.db,'SELECT * FROM Session WHERE id = ?',(self.token))[0]
        if len(s):
            c = {"players":[],"objects":[],"ressources":[],"map":[],"status":1}
            if int(s['last_update']) is 0: # generate game data
                self.write_ressources(generateRessources([(-100,-100),(100,100)]))
                self.update_last_update()
            else: # fetch game data
                self.tick()
                c['objects'] = self.get_session_data('Object')
            c['players'] = self.get_session_data('Player','name,id,x,y,data')
            c['ressources'] = self.get_session_data('Ressource')
            for p in c['players']:
                if int(p['id']) == int(pid):
                    c['map'] = generateMap(int(p['x']),int(p['y']))
            return c
        return {"status":-1}
    def update(self,pid,change): # Updates game from client input
        pass
    def tick(self): # Updates game
        d = int(time()) - int(self.last_update)
        c = {"players":self.get_session_data('Player','name,id,x,y,data'),"objects":[],"ressources":[],"map":[],"status":0}
        if d > 0:
            c['status'] = 1
            changed_objects, changed_ressources = cycle(d,self.get_session_data('Object'),self.get_session_data('Ressource'))
            c['objects'] = changed_objects
            c['ressources'] = changed_ressources
            self.update_last_update()
        return c
