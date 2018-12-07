class Session:
    def __init__(self,db,token = None):
        self.db = db
        self.token = token
    def create(self): # Create new token
        self.db.execute('INSERT INTO Player VALUES (NULL,13,13,100,100,100,100,100,"fine",0,"[]")')
        self.db.commit()
        cursor = self.db.cursor()
        cursor.execute('SELECT token FROM Player ORDER BY token DESC LIMIT 1')
        session = cursor.fetchone()
        self.token = session[0]
        return self.token
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
