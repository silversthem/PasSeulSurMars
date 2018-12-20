# Builds database

import sqlite3

db = sqlite3.connect('db.sqlite')

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
    type int,
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
    type int,
    x int,
    y int,
    data text,
    FOREIGN KEY(session) REFERENCES Session(id)
)''')
db.commit()

db.close()
