# Represents a game session
# Bridges the gap between game logic and database

from time import time # timestamp
from json import dumps, loads # Json encode/decode

from .sql import select, insert, update, updateMultiple
from .utils import merge_dicts, sha
from .game.chatbot import chatbot
from .game.map import generateMap,generateRessources
from .game.objects import cycle
from .game.player import generatePlayer,updatePlayer

formatDataField = {'data':(lambda x : loads(x))}

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
        insert(self.db,'Player',(None,self.token,username,sha(password),0,0,dumps(generatePlayer())))
        return select(self.db,'SELECT id FROM Player ORDER BY id DESC LIMIT 1')[0].get('id')
    def fill_session(self,session,pid): # Fills a flask session to maintain connexion
        session["player_id"] = pid
    # Game database reading
    def get_session_data(self,table,cols = '*'): # Returns a table from a session
        return select(self.db,'SELECT ' + cols + ' FROM ' + table + ' WHERE session = ?',(self.token),formatDataField)
    # Game database writing
    def update_last_update(self):
        update(self.db,'Session','id = ?',[self.token],{'last_update':int(time())})
    def write_ressources(self,rs):
        for r in rs:
            insert(self.db,'Ressource',(None,self.token,r[2],r[0],r[1],dumps(r[3])))
    # Game database updating
    def update_ressources(self,ressources): # Updates ressources in database
        pass
    def update_objects(self,objects): # Updates objects in database
        pass
    def update_players(self,players): # Updates players in database
        for pl in players: # Json format data field
            pl['data'] = dumps(pl['data'])
        updateMultiple(self.db,'Player','id = ?',[[pl['id']] for pl in players],players)
    def update_player_data(self,pid,udata): # Updates player data in database
        players = self.get_session_data('Player')
        for pl in players:
            if pl['id'] == pid:
                pl['data'] = merge_dicts(pl['data'],udata)
                update(self.db,'Player','id = ?',[pid],{'data':dumps(pl['data'])})
    # Main sesssion functions
    def load(self,pid): # Loads game
        s = select(self.db,'SELECT * FROM Session WHERE id = ?',(self.token))[0]
        if len(s):
            c = {"players":[],"objects":[],"ressources":[],"map":[],"status":1}
            if int(s['last_update']) is 0: # generate game data
                self.write_ressources(generateRessources([(-100,-100),(100,100)]))
                self.update_last_update()
            else: # fetch game data
                self.tick(pid)
                c['objects'] = self.get_session_data('Object')
            c['players'] = self.get_session_data('Player','name,id,x,y,data')
            c['ressources'] = self.get_session_data('Ressource')
            for p in c['players']:
                if int(p['id']) == int(pid):
                    c['map'] = generateMap(int(p['x']),int(p['y'])) # Returns map around this player
                    self.update_player_data(pid,{'online':True})
            return c
        return {"status":-1}
    def update(self,pid,change): # Updates game from client input
        if change['action'] == 'move':
            # Changes player data to reflect new movement
            self.update_player_data(pid,{'inMotion':True,'toward':{'x':int(change['x']),'y':int(change['y'])}})
            return '{"status":1}'
        return '{"status":0}'
    def tick(self,pid): # Updates game
        d = int(time()) - int(self.last_update)
        c = {"players":self.get_session_data('Player','name,id,x,y,data'),"objects":[],"ressources":[],"map":[],"status":0}
        if d > 0:
            c['status'] = 1
            # Updates players
            for pl in c['players']:
                updatePlayer(d,pl)
                if pl['id'] == pid: # Updates map for session player
                    c['map'] = generateMap(pl['x'],pl['y'])
            # Updates objects & ressources
            changed_objects, changed_ressources = cycle(d,self.get_session_data('Object'),self.get_session_data('Ressource'))
            c['objects'] = changed_objects
            c['ressources'] = changed_ressources
            # Write change into db
            self.update_ressources(changed_ressources)
            self.update_objects(changed_objects)
            self.update_players(c['players'])
            # Updates last database update
            self.update_last_update()
        return c
