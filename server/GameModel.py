# Represents the game's datamodel in the database
# This is the link between the server and the database

import json

from .SessionModel import SessionModel
from .sql import *

readDataField  = {'data':lambda x : json.loads(x)}
writeDataField = {'data':lambda x : json.dumps(x)}

class GameModel:
    # Initialize the game model
    def __init__(self,db):
        self.db = db

    # User Related

    # Returns user id, or -1 if no match is found in database
    def login(self,session,login,password):
        r = select(self.db,'SELECT id FROM Player WHERE session = ? AND name = ? AND password = ?',(session,login,password))
        return -1 if len(r) == 0 else r[0]['id']
    # Creates a new user in db, returns new user as dict
    def newUser(self,session,login,password):
        d = SessionModel.playerDict(session,login,password)
        d['id'] = insertDict(self.db,'Player',d,formatField=writeDataField)
        return d

    # Session Related

    # Creates a new session in db and returns session as model
    def newSession(self):
        d = SessionModel.sessionDict()
        d['id'] = insertDict(self.db,'Session',d)
        return SessionModel(d)
    # Checks for session's existence in db
    def sessionExists(self,session):
        s = select(self.db,'SELECT * FROM Session WHERE id = ?',[session])
        return len(s) == 1

    # Returns a new SessionModel model object for the session
    def createSessionModel(self,sessionid):
        sessionid = int(sessionid)
        sessiondata = select(self.db,'SELECT * FROM Session WHERE id = ?',[sessionid])[0]
        players     = select(self.db,'SELECT * FROM Player WHERE session = ?',[sessionid],readDataField)
        ressources  = select(self.db,'SELECT * FROM Ressource WHERE session = ?',[sessionid],readDataField)
        objects     = select(self.db,'SELECT * FROM Object WHERE session = ?',[sessionid],readDataField)
        return SessionModel(sessiondata,players,ressources,objects)
    # Writes session to the database
    def writeSession(self,session):
        sid = session.session.get('id')
        # Updating session data
        update(self.db,'Session','id = ?',[sid],session.session,commit=False)
        # Add session tag to each table
        fixFieldsInsert = {'session':sid}
        kwargs = {'formatField':writeDataField,'commit':False,'fixedFields':fixFieldsInsert}
        # Writing sessions to database
        writeToTable(self.db,'Player',session.players,'id',**kwargs)
        writeToTable(self.db,'Ressource',session.ressources,'id',**kwargs)
        writeToTable(self.db,'Object',session.objects,'id',**kwargs)
        # Commit changes into database
        self.db.commit() # committing once instead of every time
