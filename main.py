from flask import Flask
from flask import request
from flask import render_template
from flask import redirect,url_for
import sqlite3

from server import Session

app = Flask(__name__)

@app.route("/") # Main page
def index():
    return render_template('assets/html/index.html')

@app.route("/new") # Creates new session
def new():
    db = sqlite3.connect('db.sqlite')
    session = Session(db)
    id = session.create()
    return redirect(url_for('session',session=id))

@app.route("/session/<session>") # Loads game
def main(token):
    db = sqlite3.connect('db.sqlite')
    session = Session(db,token)
    game = session.load()
    return render_template('assets/html/game.html')

@app.route("/update/<session>") # Updates game on user input
def update(token, methods=['POST']):
    db = sqlite3.connect('db.sqlite')
    session = Session(db,token)
    game = session.load()
    update = request.form.get('action') # TODO : dict
    changes = game.update(update)
    session.update(changes)
    return changes # @TODO : Json formatted

@app.route('tick/<session>/<time>') # Updates game every X seconds
def tick(token,time):
    db = sqlite3.connect('db.sqlite')
    session = Session(db,token)
    game = session.load()
    changes = game.tick(int(time))
    return changes
