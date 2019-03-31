# Builds database

import sys
import sqlite3

name = sys.argv[1] + '.sqlite' if len(sys.argv) > 1 else 'db.sqlite'
db = sqlite3.connect(name)

db.execute('''
CREATE TABLE Session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_update int,
    admin int
)''')
db.commit()

db.execute('''
CREATE TABLE Player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session  int,
    name     varchar(128),
    password varchar(256),
    x int,
    y int,
    data     text,
    FOREIGN KEY(session) REFERENCES Session(id)
)''')
db.commit()

db.execute('''
CREATE TABLE Object (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session int,
    type varchar(64),
    x int,
    y int,
    data text,
    FOREIGN KEY(session) REFERENCES Session(id)
)''')
db.commit()

db.execute('''
CREATE TABLE Ressource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session int,
    type varchar(64),
    x int,
    y int,
    data text,
    FOREIGN KEY(session) REFERENCES Session(id)
)''')
db.commit()

# @TODO : Add entity table

db.close()
