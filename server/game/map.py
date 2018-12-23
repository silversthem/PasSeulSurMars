from json import dumps, loads
from math import sqrt
from random import randrange

# Returns a map segment centered around a x/y couple
def generateMap(x,y):
    map = [0 for i in range(25*25)]
    return map

# Returns random coord in interval bounds excluding taken
def getRandomCoords(bounds,taken = []):
    good,x,y = (False,0,0)
    while not good:
        x = randrange(bounds[0][0],bounds[1][0])
        y = randrange(bounds[0][1],bounds[1][1])
        good = True
        for coord in taken:
            if coord[0] == x and coord[1] == y:
                good = False
                break
    return (x,y)

# Returns random quality from interval and distribution function
def getRandomQuality(interval, f = (lambda x : x**3)):
    n = randrange(f(interval[0]),f(interval[1]) + 1)
    for i in range(interval[0],interval[1] + 1):
        if n <= f(i):
            return interval[1] - i + 1
    return interval[0]

# Returns a list of (x,y,type,data)
# types of ressources :
# 0 - Water
# 1 - Metal
# 2 - Organic Matter
# 3 - Nuclear Matter
def generateRessources(bounds,density = 25,
        typeDensity = {0:1,1:0.5,2:0.25,3:0.125},
        fillInterval = {0:[1000,10000],1:[250,5000],2:[4000,20000],3:[400,5000]},
        qualityInterval = {0:[1,3],1:[1,3],2:[1,5],3:[1,10]}):
    r = []
    d = int(sqrt(sum([sum([c**2 for c in p]) for p in bounds])))
    for rs in typeDensity:
        n = int(typeDensity[rs]*d) # Amount of the ressource to display
        for k in range(n):
            x,y = getRandomCoords(bounds,r)
            data = {'quality':getRandomQuality(qualityInterval[rs]),
                    'total'  :randrange(fillInterval[rs][0],fillInterval[rs][1] + 1)}
            r.append((x,y,rs,data))
    return r
