import hashlib # sha hashing

def merge_dicts(d,d2):
    for k in d2:
        if k in d and isinstance(d[k],dict) and isinstance(d2[k],dict):
            d[k] = merge_dicts(d[k],d2[k])
        else:
            d[k] = d2[k]
    return d

def sha(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()
