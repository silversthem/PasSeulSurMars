# Builds database

import sqlite3

db = sqlite3.connect('db.sqlite')

db.execute('''
CREATE TABLE Player (
    token int PRIMARY KEY AUTOINCREMENT,
    x int,
    y int,
    food int,
    thirst int,
    oxygene int,
    stamina int,
    stress int,
    status text,
    Days int,
    inventory text
)''')

db.commit()

db.execute('''
CREATE TABLE Object (
    id int PRIMARY KEY,
    token int,
    x int,
    y int,
    type int,
    Attr text,
    FOREIGN KEY(token) REFERENCES Player(token)
);
CREATE TABLE Ressource (
    id int PRIMARY KEY,
    token int,
    x int,
    y int,
    mined int
    FOREIGN KEY(token) REFERENCES Player(token)
)
''')

db.commit()

db.close()
