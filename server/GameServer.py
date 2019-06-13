import json

from .GameModel import GameModel
from .SessionModel import SessionModel
from .utils import loadjsonfiles

class GameServer:
    LOG = None
    # Creates a game server
    def __init__(self,db,log,tickrate):
        self.model = GameModel(db) # Game database access class
        self.sessions = {} # Games data as SessionModel, stored by session id
        self.users = {} # Current user sockets
        GameServer.LOG = log
        SessionModel.TickTime = tickrate
        self.loadGameConfig()

    # Initialization Related

    # Loads assets/config into SessionModel class
    def loadGameConfig(self):
        SessionModel.GameEnv = loadjsonfiles('assets/config',['ressources','items','objects','starter'])

    # Session Related

    # Access session in server, loading it up from db if not in self.sessions
    def accessSession(self,session):
        if session in self.sessions:
            return self.sessions[session]
        elif self.model.sessionExists(session):
            self.sessions[session] = self.model.createSessionModel(session)
            GameServer.LOG.info('- Loaded session {}'.format(session))
            return self.sessions[session]
        else:
            # @TODO : Big Error Time
            return
    # Returns boolean indicating session's existence
    def sessionExists(self,session):
        if not (session in self.sessions): # this session is not loaded currently
            return self.model.sessionExists(session) # Checks in db
        else: # The session is loaded
            return True

    # User Related

    # Adds user to active users
    def addActiveUser(self,sock,ss,id):
        self.users[sock] = {'socket':sock,'id':id,'session':int(ss),'last_update':0}

    # Auth Related

    # Auth an user into the server
    async def auth(self,sock):
        auth = await sock.recv()
        msg = json.loads(auth)
        ss,lg,pw = (int(msg.get('session',-1)),msg.get('login'),msg.get('password'))
        GameServer.LOG.info(' > New user connected {} ({},{})'.format(sock,lg,ss))
        if 'register' in msg: # Registering new user
            if 'newSession' in msg: # Creating a new session as well
                session = self.model.newSession() # Creating new session
                session.generate() # Filling session up
                ss = session.session['id'] # Reading new session id
                self.sessions[ss] = session # Adding it to newly created session
                user = self.model.newUser(ss,lg,pw) # Creating new user in db
                self.sessions[ss].insertNewPlayer(user) # Inserting new user in session
                self.sessions[ss].setAdmin(user['id']) # Setting user as session admin
                GameServer.LOG.info('  >> New user (id : {}) created new session {}'.format(user['id'],ss))
                self.addActiveUser(sock,ss,user['id']) # Adding socket to active user pool
                await sock.send('{"register":1,"session":'+ str(ss) +',"pid":'+ str(user['id']) +'}')
            elif self.sessionExists(ss): # check for session existence
                user = self.model.newUser(ss,lg,pw) # Creating new user in db
                self.accessSession(ss).insertNewPlayer(user) # Adding it to session
                self.addActiveUser(sock,ss,user['id']) # Adding socket to active user pool
                GameServer.LOG.info('  >> New user (id : {}) joined session {}'.format(user['id'],ss))
                await sock.send('{"register":1,"session":'+ str(ss) +',"pid":'+ str(user['id']) +'}')
            else: # Auth Failed
                GameServer.LOG.info('  /!\\ Couldnt register user')
                await sock.send('{"register":0}')
                return False
        else: # Loging in user
            userid = self.model.login(ss,lg,pw)
            if userid != -1: # Successful auth
                GameServer.LOG.info('  >> User successfully logged in (id : {})'.format(userid))
                self.addActiveUser(sock,ss,userid) # Adding socket to active user pool
                await sock.send('{"auth":1,"pid":'+ str(userid) +'}') # Successful auth message
            else: # Failed auth
                GameServer.LOG.info('  /!\\ Couldnt auth user')
                await sock.send('{"auth":0}') # Failed auth message
                return False
        return True
    # Logouts an user
    def logout(self,sock):
        if sock in self.users:
            session = int(self.users[sock]['session'])
            pid = int(self.users[sock]['id'])
            self.accessSession(session).isOffline(pid) # Sets user status to offline
            GameServer.LOG.info(' > User {} successfully disconnected from session {}, Bye !'.format(pid,session))
            del self.users[sock] # Deletes user from active users
            # check if session is still active (if there's still players in the session)
            stillActive = False
            for i in self.users:
                if self.users[i].get('session',-1) == session:
                    stillActive = True
                    break
            if not stillActive: # Session not active
                GameServer.LOG.info('-=- Session {} no longer active'.format(session))
                self.model.writeSession(self.sessions[session]) # Write session to db
                GameServer.LOG.info('=-= Session {} no longer active and written to database'.format(session))
                del self.sessions[session] # Deleting session data

    # Game Related

    # Updates user data from server cycle
    async def doTick(self,sock):
        if sock in self.users: # Authentified user
            usr = self.users[sock]
            if usr['session'] in self.sessions: # Loaded Session
                self.accessSession(usr['session']).tick()
                usr['last_update'],data = self.accessSession(usr['session']).toTick(usr['id'],usr['last_update'])
                if data is not None: # Send update data
                    data['tick'] = 1
                    await sock.send(json.dumps(data))
    # Udpates server data from user data
    async def update(self,sock):
        if sock in self.users: # Authentified user
            data = json.loads(await sock.recv())
            session = self.users.get(sock,{}).get('session',-1)
            if data.get('load',0) is 1: # Client asked for game to load
                self.accessSession(session).tick() # Update game if needed
                self.accessSession(session).isOnline(self.users[sock]['id']) # Sets user status to online
                clientdata = self.accessSession(session).toLoad(self.users[sock]['id'])
                clientdata['load'] = 1
                await sock.send(json.dumps(clientdata))
            elif 'action' in data: # Command Type update
                # register action : player : move , objects : build/destroy
                if session in self.sessions:
                    rep = self.sessions[session].update(data)
                    await sock.send(json.dumps(rep))
    # Cycles through users and updates clients
    async def cycle(self):
        for sock in self.users:
            await self.doTick(sock)
