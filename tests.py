import sys
from sqlite3 import connect
from testing.Tester import Tester
# Tested files
from server.Session import Session

# Creating a context
if len(sys.argv) > 1:
    dbname = sys.argv[1] + '.sqlite'
    # init
    db = connect(dbname)
    ss = Session(db)
    # Creating new session
    sid = ss.create()
    # Creating new test player as session admin
    pid = ss.add_new_player('test1','password')
    ss.set_admin(pid)
