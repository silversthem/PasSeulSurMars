# Builds database

import sqlite3

db = sqlite3.connect('db.sqlite')

db.execute('''
CREATE TABLE Player (
    token INTEGER PRIMARY KEY AUTOINCREMENT,
    x int,
    y int,
    food int,
    thirst int,
    oxygen int,
    stamina int,
    stress int,
    status text,
    Days int,
    inventory text
)''')

db.commit()

db.execute('''
CREATE TABLE Object (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token int,
    x int,
    y int,
    type int,
    attr int,
    FOREIGN KEY(token) REFERENCES Player(token)
)''')

db.execute('''
CREATE TABLE Ressource (
    id int PRIMARY KEY,
    token int,
    x int,
    y int,
    total int,
    type int,
    FOREIGN KEY(token) REFERENCES Player(token)
)
''')

db.commit()

db.close()
