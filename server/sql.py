
# Inserts a value tuple into a table
def insert(db,table,values,**kwargs):
    doCommit = kwargs.get('commit',True)
    ins = 'INSERT INTO ' + table + ' VALUES (' + ','.join(['?' for i in range(len(values))]) + ')'
    db.execute(ins,values)
    if doCommit:
        db.commit()

# Inserts a dict into a table and returns the primary key of the new row
def insertDict(db,table,d,**kwargs):
    formatField = kwargs.get('formatField',{})
    doCommit = kwargs.get('commit',True)
    pl  = ','.join(['?' for i in range(len(d))])
    ins = 'INSERT INTO ' + table + ' (' + ','.join(d.keys()) + ') VALUES (' + pl + ')'
    cur = db.cursor()
    vals = [formatField.get(k,lambda x : x)(d[k]) for k in d]
    cur.execute(ins,vals)
    if doCommit:
        db.commit()
    id = cur.lastrowid
    return id

# Queries the database and calls action on each row
def doSelect(db,query,args,formatField,action):
    noFormat = lambda x : x
    cur = db.cursor()
    cur.execute(query,args)
    cols = [k[0] for k in cur.description]
    rows = cur.fetchall()
    if len(rows) == 0:
        return
    else:
        for row in rows:
            if len(cols) == len(row):
                r = {cols[i]:formatField.get(cols[i],noFormat)(row[i]) for i in range(len(cols))}
                action(r)

# Queries the database and returns each row as a dict of colname:rowvalue
def select(db,query,args = (),formatField = {}):
    r = []
    doSelect(db,query,args,formatField,lambda x:r.append(x))
    return r

# Same as select, but stores results in a dict sorted by a key field
def selectAsDict(db,query,key,args = (),formatField = {}):
    r = {}
    doSelect(db,query,key,args,formatField,lambda x:r.update({x.get(key):x}))
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
def update(db,table,where,args,setv,**kwargs):
    formatField = kwargs.get('formatField',{})
    doCommit = kwargs.get('commit',True)
    q,a = update_query(table,where,args,setv,formatField)
    db.execute(q,a)
    if doCommit:
        db.commit()

# Updates multiple rows in one commit
def updateMultiple(db,table,where,args,setv,**kwargs):
    formatField = kwargs.get('formatField',{})
    doCommit = kwargs.get('commit',True)
    if len(args) != len(setv):
        raise Exception('Wrong pair of row id/rows',table,len(args),leng(setv))
    for i in range(len(args)):
        q,a = update_query(table,where,args[i],setv[i],formatField)
        db.execute(q,a)
    if doCommit:
        db.commit()

# Writes an array of dicts to the right table in database, updates col if id is in the dict, inserts otherwise and updates id in the dict array
def writeToTable(db,table,datalist,keyfield,**kwargs):
    fixedFields = kwargs.get('fixedFields',{})
    for data in datalist:
        id = data.get(keyfield)
        if id is None:
            data.update(fixedFields)
            id = insertDict(db,table,data,**kwargs)
            data[keyfield] = id
        else: # Updates row
            update(db,table,keyfield + ' = ?',[id],data,**kwargs)
