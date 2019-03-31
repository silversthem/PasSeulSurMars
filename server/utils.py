import hashlib # sha hashing
import json

def merge_dicts(d,d2):
    for k in d2:
        if k in d and isinstance(d[k],dict) and isinstance(d2[k],dict):
            d[k] = merge_dicts(d[k],d2[k])
        else:
            d[k] = d2[k]
    return d

def sha(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def loadjsonfile(file):
    with open(file) as f:
        return json.load(f)
    return {}

def loadjsonfiles(dir,files):
    r = {}
    for f in files:
        filename = dir + '/' + f + '.json'
        r[f] = loadjsonfile(filename)
    return r
