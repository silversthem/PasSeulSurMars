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
            if coord['x'] == x and coord['y'] == y:
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

# Returns a dict of (x,y,type,data) for a dictionnary containing the list of all the ressources
def generateRessources(bounds,ressourcesDict):
    r = []
    d = int(sqrt(sum([sum([c**2 for c in p]) for p in bounds])))
    for rs in ressourcesDict:
        ressource = ressourcesDict[rs].get('ressource',{})
        n = int(d*ressource.get('density',1)) # Amount of the ressource to display
        for k in range(n):
            x,y = getRandomCoords(bounds,r)
            data = {'quality':getRandomQuality(ressource.get('quality',[1,1])),
                    'total'  :randrange(*ressource.get('quantity',[0,0]))}
            r.append({'x':x,'y':y,'type':rs,'data':data})
    return r
