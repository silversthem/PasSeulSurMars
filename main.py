from flask import Flask
from flask import request,session
from flask import render_template
from flask import redirect,url_for, send_from_directory
import sqlite3
import os

from game.Game import Game
from server.Session import Session
from game.chatbot import chatbot

app = Flask(__name__,template_folder='assets/html',static_url_path='')
app.secret_key = 'EHEHEHE'

def get_db():
    return sqlite3.connect('db.sqlite')

from json import dumps, loads

# App routes

@app.route("/") # Main page
def index():
    return render_template('index.html')

@app.route("/logout")
def logout():
    #@TODO : destroy session variables
    return 'Successfully logged out. Bye !'

@app.route("/join",methods=['POST']) # Joins existing session
def join():
    login,password,sid = (request.form.get('login'),request.form.get('password'),request.form.get('session'))
    if login != None and password != None and sid != None:
        game = Session(get_db(),sid)
        pid = game.login(login,password)
        if pid == -1:
            pid = game.add_new_player(login,password)
        game.fill_session(session,pid)
        return redirect('/session/' + str(sid))
    else:
        return 'Form incomplete'

@app.route("/new",methods=['POST']) # Creates new session
def new():
    game = Session(get_db())
    login,password = (request.form.get('login'),request.form.get('password'))
    if login != None and password != None:
        id = game.create()
        pid = game.add_new_player(login,password)
        game.set_admin(pid)
        game.fill_session(session,pid)
        return redirect('/session/' + str(id))
    else:
        return 'Form incomplete'

# Game routes

@app.route("/session/<token>") # Loads game
def main(token):
    if 'player_id' in session:
        return render_template('game.html',token=token,player_id=session['player_id'])
    else:
        return 'Not logged in'

@app.route("/update/<token>",methods=['POST']) # Updates game on user input
def update(token):
    if 'player_id' in session:
        pass

@app.route('/load/<token>') # Returns game state
def load(token):
    if 'player_id' in session:
        # @TODO : other players, all objects and ressources in a json object
        pass

@app.route('/tick/<token>') # Updates game
def tick(token):
    if 'player_id' in session:
        # @TODO : Update about other users
        # @TODO : Check timestamp for last update in session
        # @TODO : update everything by elapsed time & update last update in session
        pass

@app.route('/chatbot/<token>/<pid>/<qcmid>')
def chat(token,pid,qcmid):
    if 'player_id' in session:
        #cbot = chatbot(100 - game.Player["stress"])
        #message = cbot.update_chat(pid, qcmid, game.Ressource, [game.Player["x"], game.Player["y"]])
        pass

# Static files routes

@app.route('/js/<path:jsfile>')
def loadjs(jsfile):
    return send_from_directory('assets/js', jsfile)

@app.route('/textures/<path:text>')
def loadtexture(text):
    return send_from_directory('assets/textures', text)

@app.route('/css/<path:cssfile>')
def loadcssfile(cssfile):
    return send_from_directory('assets/css',cssfile)
