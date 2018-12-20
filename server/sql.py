
# Inserts a value tuple into a table
def insert(db,table,values):
    ins = 'INSERT INTO ' + table + ' VALUES (' + ','.join(['?' for i in range(len(values))]) + ')'
    db.execute(ins,values)
    db.commit()

# Queries the database and yield each row as dict of colname:rowvalue
def select(db,query,args = ()):
    cur = db.cursor()
    cur.execute(query,args)
    cols = [k[0] for k in cur.description]
    rows = cur.fetchall()
    if len(rows) == 0:
        return []
    else:
        r = []
        for row in rows:
            r.append({cols[i]:row[i] for i in range(len(cols))})
        return r

# Updates database
def update(db,table,where,args,setv):
    q = 'UPDATE ' + table + ' SET '
    for k in setv:
        q += k + '= ? '
    q += 'WHERE ' + where
    a = [setv[k] for k in setv]
    a.extend(args)
    db.execute(q,a)
    db.commit()
