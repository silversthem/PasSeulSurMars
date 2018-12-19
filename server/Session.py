# Represents a game session
# Bridges the gap between game logic and database

from time import time # timestamp
import hashlib # hashing passwords in database

def sha(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

class Session:
    def __init__(self,db,token = None): # Creates a session
        self.db = db
        self.token = token
    # Session & User related
    def login(self,username,pwd): # Logs in user and returns player id, returns -1 if unable to
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM Player WHERE session = ? AND name = ? AND password = ?', \
            (self.token,username,sha(pwd)))
        pid = cursor.fetchone()
        return pid[0] if pid is not None else -1
    def create(self): # Create new session
        # Creating new session in db
        self.db.execute('INSERT INTO Session VALUES (NULL,'+ str(int(time())) +',NULL)')
        self.db.commit()
        # Fetching session id
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM Session ORDER BY id DESC LIMIT 1')
        session = cursor.fetchone()
        self.token = session[0]
        return self.token
    def set_admin(self,pid): # Sets player with id pid as admin of this session
        self.db.execute('UPDATE Session SET admin = ? WHERE id = ?',(pid,self.token))
        self.db.commit()
    def add_new_player(self,username,password): # Adds a new player to this session, returns player id
        self.db.execute('INSERT INTO Player VALUES (NULL,?,?,?,"{}")',(self.token,username,sha(password)))
        self.db.commit()
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM Player ORDER BY id DESC LIMIT 1')
        player = cursor.fetchone()
        return player[0]
    def fill_session(self,session,pid): # Fills a flask session to maintain connexion
        session["player_id"] = pid
    # Game database related
    def load(self):
        # Player data
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM Player WHERE token = ' + str(int(self.token)))
        dt = cursor.fetchone()
        pid, x, y, food, thirst, ox, stamina, stress, status, days, inv = dt
        player = {'id':pid,'x':int(x),'y':int(y),'food':int(food),'thirst':int(thirst),'ox':int(ox)}
        # Map data
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM Object WHERE token = ' + str(int(self.token)))
        rows = cursor.fetchall()
        # Empty map
        mp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,1,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,1,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,1,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for row in rows:
            bid, token, x, y, btype, Attr = row
            mp[int(y)*25 + x] = {'type':int(btype),'id':int(bid), 'attr':Attr}
        # Ressources
        ressources = []
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM Ressource WHERE token = ' + str(int(self.token)))
        rows = cursor.fetchall()
        for row in rows:
            rid, token, x, y, total, rtype = row
            ressources.append({'id':rid,'token':token,'x':x,'y':y,'total':total,'type':rtype})
        return (mp,player,ressources)
    def update(self,changes):
        for c in changes:
            if "move" in c: # Moves player
                self.db.execute('UPDATE Player SET x = ' + c["x"] + ', y = ' + c['y'] + ' WHERE token = ' + str(int(self.token)))
                self.db.commit()
            elif "construct" in c: # Adds object
                self.db.execute('INSERT INTO Object VALUES (NULL,'+str(int(self.token))+','+ str(c['x']) +','+ str(c['y']) +', '+ str(c['type']) +',0)')
                self.db.commit()
                cursor = self.db.cursor()
                cursor.execute('SELECT id FROM Object ORDER BY id DESC LIMIT 1')
                cid = cursor.fetchone()
                c["id"] = cid
                c["attr"] = 0
            elif "type" in c: # Changes value
                if c["type"] == "ressource":
                    self.db.execute('UPDATE Ressource SET total = ' + str(c["attr"]) + ' WHERE id = ' + str(int(c["id"])))
                    self.db.commit()
                elif c["type"] == "object":
                    self.db.execute('UPDATE Object SET attr = ' + str(c["attr"]) + ' WHERE id = ' + str(int(c["id"])))
                    self.db.commit()
