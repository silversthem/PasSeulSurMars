from testing.context import *
from json import loads, dumps

testsGrid = [
    {'send':registerNewValid11,'receive':registerNewValid11Response,'name':'Registration & new session (Session : 1, pid : 1)'},
    {'send':loginValid11,'receive':loginValid11Response,'name':'Login (Session : 1, pid 1)'},
    {'send':loginWrong111,'receive':loginWrongResponse,'name':'Login : Wrong password (Session : 1, pid : 1)'},
    {'send':loginWrong112,'receive':loginWrongResponse,'name':'Login : Wrong username (Session : 1, pid : 1)'},
    {'send':registerValid12,'receive':registerValid12Response,'name':'Registration in Session 1 (Session : 1, pid : 2)'},
    {'send':loginValid12,'receive':loginValid12Response,'name':'Login (Session : 1, pid 2)'},
    {'send':registerNewValid21,'receive':registerNewValid21Response,'name':'Registration & new session (Session : 2, pid : 3)'},
    {'send':loginValid21,'receive':loginValid21Response,'name':'Login (Session : 2, pid 3)'},
    {'send':registerValid22,'receive':registerValid22Response,'name':'Registration in Session 2 (Session : 2, pid : 4)'},
    {'send':loginValid22,'receive':loginValid22Response,'name':'Login (Session : 2, pid 4)'},
    {'send':registerWrong2,'receive':registerWrongResponse,'name':'Registration in Session 2 : Username already taken'}
]

for test in testsGrid:
    try:
        r = runTestsSequence([test['send']],[test['receive']])
        if r[0] == 1:
            print('=== Success === ' + test['name'])
        else:
            print('/!\\ Failed  /!\\ ' + test['name'])
    except websockets.exceptions.ConnectionClosed:
        print('§§§ Serverside internal exception §§§')
        break
