
# Inserts a value tuple into a table
def insert(db,table,values):
    ins = 'INSERT INTO ' + table + ' VALUES (' + ','.join(['?' for i in range(len(values))]) + ')'
    db.execute(ins,values)
    db.commit()

# Queries the database and yield each row as dict of colname:rowvalue
def select(db,query,args = (),formatField = {}):
    noFormat = lambda x : x
    cur = db.cursor()
    cur.execute(query,args)
    cols = [k[0] for k in cur.description]
    rows = cur.fetchall()
    if len(rows) == 0:
        return []
    else:
        r = []
        for row in rows:
            r.append({cols[i]:(formatField.get(cols[i],noFormat)(row[i])) for i in range(len(cols))})
        return r

# Returns sql syntax for an update query
def update_query(table,where,where_args,setv,formatField = {}):
    noFormat = lambda x : x
    q = 'UPDATE ' + table + ' SET '
    q += ','.join([k + ' = ?' for k in setv])
    q += ' WHERE ' + where
    a = [formatField.get(k,noFormat)(setv[k]) for k in setv]
    a.extend(where_args)
    return (q,a)

# Updates a row in database
def update(db,table,where,args,setv,formatField = {}):
    q,a = update_query(table,where,args,setv,formatField)
    db.execute(q,a)
    db.commit()

# Updates multiple rows in one commit
def updateMultiple(db,table,where,args,setv,formatField = {}):
    if len(args) != len(setv):
        raise Exception('Wrong pair of row id/rows',table,len(args),leng(setv))
    for i in range(len(args)):
        q,a = update_query(table,where,args[i],setv[i],formatField)
        db.execute(q,a)
    db.commit()
