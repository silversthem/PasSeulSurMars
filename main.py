from flask import Flask
from flask import request
from flask import render_template
from flask import redirect,url_for, send_from_directory
import sqlite3
import os

from game.Game import Game
from server.Session import Session
from game.chatbot import chatbot

app = Flask(__name__,template_folder='assets/html',static_url_path='')

from json import dumps, loads

@app.route("/") # Main page
def index():
    return render_template('index.html')

@app.route("/new") # Creates new session
def new():
    db = sqlite3.connect('db.sqlite')
    session = Session(db)
    id = session.create()
    return redirect('/session/' + str(id))

@app.route("/session/<token>") # Loads game
def main(token):
    db = sqlite3.connect('db.sqlite')
    session = Session(db,token)
    game = Game(*session.load())
    print game.map
    return render_template('game.html',map=dumps(game.map),player=dumps(game.player),ressources=dumps(game.ressources),token=token)

@app.route("/update/<token>",methods=['POST']) # Updates game on user input
def update(token):
    db = sqlite3.connect('db.sqlite')
    session = Session(db,token)
    game = Game(*session.load())
    update = request.form
    changes = game.update(update)
    session.update(changes)
    return dumps(changes) # Json formatted

@app.route('/tick/<token>/<time>') # Updates game every X seconds
def tick(token,time):
    db = sqlite3.connect('db.sqlite')
    session = Session(db,token)
    game = Game(*session.load())
    changes = game.tick(int(time))
    session.update(changes)
    return dumps(changes) # Json formatted

@app.route('/chatbot/<token>/<pid>/<qcmid>')
def chat(token,pid,qcmid):
    db = sqlite3.connect('db.sqlite')
    session = Session(db,token)
    game = Game(*session.load())
    cbot = chatbot(100 - game.Player["stress"])
    message = cbot.update_chat(pid, qcmid, game.Ressource, [game.Player["x"], game.Player["y"]])
    return dumps(message)

@app.route('/js/<path:jsfile>')
def loadjs(jsfile):
    return send_from_directory('assets/js', jsfile)

@app.route('/textures/<path:text>')
def loadtexture(text):
    return send_from_directory('assets/textures', text)
