# -*- coding: utf-8 -*
# num des construct  : 1=tuyau 2=cable 3=resevoir oxy 4=generateur nuc 5=panneau solaire 6= resevoir eau 7=Serre  8= raffinerie 9=foreuse 10=abris 11=entrepot 12=station oxy
# num des ressources : 20=metal 21=uranium 22=nouriture 23=oxygene 24=eau 24=electricité 25=matiere organique
# chaque tick = -1 bouffe -2 eau -40 oxy pour le perso
#chaque tick par raffinerie = -50 elec                         raffinerie = cable rerlié a central ou PS
# chaque tick par serres = -5 eau  -20 oxy    -20 elec         serres = serres mutlibloc -- cable vers elec  tuyaux vers eau et oxy
#chaque tick par  station d'oxy = -2 eau  -30 elec             station = cable vers elec -- tuyant vers eau



def isAlentour(map,x,y, lst,  dir = [(0,0)]):
    directions = [k for k in [(1,0),(-1,0),(0,1),(0,-1)] if not (k in dir)]
    cases = [(y + k[0])*25 + x + k[1] for k in directions]
    rep = []
    for c in cases:
        if isinstance(map[c],dict):
            if map[c] in lst:
                rep.append(c)
    return rep


def followTuyau(map, x, y, dir):
    directions = [k for k in [(1,0),(-1,0),(0,1),(0,-1)] if k != dir]
    cases = [(y + k[0])*25 + x + k[1] for k in directions]
    for c in cases:
        if isinstance(map[c],dict):
            if map[c] == 1:
                return followTuyau(map, xx, yy, (xx - x,yy - y))
            if map[c] == 3 or map[c] == 6 or map[c] == 11 or map[c] == 12 or map[c] == 4 or map[c] == 7:
                return c
    return -1

def followCable(map, x, y, dir):
    directions = [k for k in [(1,0),(-1,0),(0,1),(0,-1)] if k != dir]
    cases = [(y + k[0])*25 + x + k[1] for k in directions]
    for c in cases:
        if isinstance(map[c],dict):
            xx,yy = IndexToCoord(c)
            if map[c] == 2:
                return followCable(map, xx, yy, (xx - x,yy - y))
            if map[c] == 4 or map[c] == 5 or map[c] == 7 or map[c] == 8 or map[c] == 9 or map[c] == 12:
                return c
    return -1

def isRessource(ressources, x, y):
    for r in ressources:
        if x == int(r['x']) and y == int(r['y']):
            return ressources['type']
    return False

def getRessource(ressources, x, y):
    for r in ressources:
        if x == int(r['x']) and y == int(r['y']):
            return r
    return None

def isConstructAble(map, ressources, x ,y, construct):
    if not isinstance(map[(x*25)+y], dict):
        if construct == 9: # foreuse
            return isRessource(ressources,x,y)
        if constuct == 8:
            tmp=isAlentour(map,x,y,[9])
            for i in tmp:
                if isRessource(ressources, i % 25, i // 25) in [20,21,25]:
                    return True
        else:
            return True

    return False

def IndexToCoord(num):
    y=num%25
    x=num-y*25
    return (x,y)

class Game:
    def __init__(self, map, player, ressources): # Creates a game object from a map and a player
        self.map = map
        self.player = player
        self.ressources = ressources
    def update(self,action):
        # Updates game from user input, returns changes
        changes = []
        if "move" in action :
            if action['move']=='left' and (self.player['x']-1) >= 0:
                changes.append({'x':self.player['x']-1,'y':self.player['y']})
            if action['move']=='right' and (self.player['x']+1) < 25:
                changes.append({'x':self.player['x']+1,'y':self.player['y']})
            if action['move']=='UP' and (self.player['y']-1) >= 0:
                changes.append({'x':self.player['x'],'y':self.player['y']-1})
            if action['move']=='DOWN' and (self.player['y']+1) < 25:
                changes.append({'x':self.player['x'],'y':self.player['y']+1})
        if "construct" in action :
            if isConstructAble(self.map, self.ressources,action['x'], action['y'], action['type']):
                changes.append({'can':True, 'x':action['x'], 'y':action['y'],  'type': action['type']})
            else:
                changes.append({'can':False})
        return changes
    def tick(self,seconds): # Updates game, returns changes
        changes = []
        for i in range(0,25):
            for j in range(0,25):
                case = i*25 + j
                if isinstance(self.map[case],dict):
                    if self.map[case]["type"] == 3: # Station
                        a = (None, None, None)
                        conn = isAlentour(self.map, i, j, [1]) # Entrée d'eau
                        entreeElec = isAlentour(self.map, i, j, [2])
                        if len(conn) != 0 and len(entreeElec) != 0:
                            for c in conn:
                                x,y = IndexToCoord(c)
                                if (self.map[c]["type"] == 1):
                                    g = followTuyau(self.map,j,i,(x-j,y-i))
                                    if self.map[g]["type"] == 3: # Oxy
                                        a[0]=self.map[g]["type"]
                                    elif self.map[g]["type"] == 6: # Eau
                                        a[1]=self.map[g]["type"]
                            for c in entreeElec:
                                x,y = IndexToCoord(c)
                                h = followCable(self.map,entreeElec[x],i,(x-j,y-i))
                                if self.map[h]["type"] == 4 or self.map[h]["type"] == 5: # Elec
                                    a[2] = self.map[h]
                            if not (None in a):
                                changes.append({'attr':a[0]['attr']+100,'id':a[0]['id'],"type":"object"})
                                changes.append({'attr':a[1]['attr']-200,'id':a[1]['id'],"type":"object"})
                                changes.append({'attr':a[2]['attr']-200,'id':a[2]['id'],"type":"object"})
                    if self.map[case]["type"] == 9: # foreuse
                        r = getRessource(ressources, j, i)
                        if r is not None and int(r['total']) != 0:
                            if r['type']== 24:
                                a = (None,None)
                                entreeEau=isAlentour(self.map,i,j,[1])
                                entreeElec=isAlentour(self.map,i,j,[2])
                                if len(entreeEau) != 0 and len(entreeElec) !=0:
                                    for c in entreeEau :
                                        x,y = IndexToCoord(c)
                                        g = followTuyau(self.map,j,i,(x-j,y-i))
                                        if self.map[g]["type"] == 6: # Eau
                                            a[0]=self.map[g]["type"]
                                    for c in entreeElec:
                                        x,y = IndexToCoord(c)
                                        h = followCable(self.map,entreeElec[x],i,(x-j,y-i))
                                        if self.map[h]["type"] == 4 or self.map[h]["type"] == 5: # Elec
                                            a[2] = self.map[h]
                                    if not (None in a):
                                            changes.append({'attr':a[0]['attr']+100,'id':a[0]['id']})
                                            changes.append({'attr':a[1]['attr']-125,'id':a[1]['id']})
                            if r['type']== 20:
                                a = (None,None)
                                entrepot=isAlentour(self.map,i,j,[1])
                                entreeElec=isAlentour(self.map,i,j,[2])
                                if len(entrepot) != 0 and len(entreeElec) !=0:
                                    for c in entrepot :
                                        x,y = IndexToCoord(c)
                                        g = followTuyau(self.map,j,i,(x-j,y-i))
                                        if self.map[g]["type"] == 11: # Entrepot
                                            a[0]=self.map[g]["type"]
                                    for c in entreeElec:
                                        x,y = IndexToCoord(c)
                                        h = followCable(self.map,entreeElec[x],i,(x-j,y-i))
                                        if self.map[h]["type"] == 4 or self.map[h]["type"] == 5: # Elec
                                            a[2] = self.map[h]
                                    if not (None in a):
                                            changes.append({'attr':a[0]['attr']+500,'id':a[0]['id']})
                                            changes.append({'attr':a[1]['attr']-200,'id':a[1]['id']})
                            if r['type']== 21:
                                a = (None,None)
                                centralNuc=isAlentour(self.map,i,j,[4])
                                entreeElec=isAlentour(self.map,i,j,[2])
                                if len(centralNuc) != 0 and len(entreeElec) !=0:
                                    for c in centralNuc :
                                        x,y = IndexToCoord(c)
                                        g = followTuyau(self.map,j,i,(x-j,y-i))
                                        if self.map[g]["type"] == 4: # Entrepot
                                            a[0]=self.map[g]["type"]
                                    for c in entreeElec:
                                        x,y = IndexToCoord(c)
                                        h = followCable(self.map,entreeElec[x],i,(x-j,y-i))
                                        if self.map[h]["type"] == 4 or self.map[h]["type"] == 5: # Elec
                                            a[2] = self.map[h]
                                    if not (None in a):
                                            changes.append({'attr':a[0]['attr']+5000,'id':a[0]['id']})
                                            changes.append({'attr':a[1]['attr']-500,'id':a[1]['id']})
                    if self.map[case]["type"] == 7: # Serres
                        a = (None, None, None,None)
                        connEau = isAlentour(self.map, i, j, [1]) # Entrée d'eau
                        entreeElec = isAlentour(self.map, i, j, [2])
                        entreterre = isAlentour(self.map, i, j, [1])
                        entreox = isAlentour(self.map, i, j, [1])

                        if len(connEau) != 0 and len(entreeElec) != 0  and len(entreterre) != 0  and len(entreox) != 0:
                            for c in connEau:
                                x,y = IndexToCoord(c)
                                if (self.map[c]["type"] == 1):
                                    g = followTuyau(self.map,j,i,(x-j,y-i))
                                    if self.map[g]["type"] == 3: # Oxy
                                        a[0]=self.map[g]["type"]
                                    elif self.map[g]["type"] == 6: # Eau
                                        a[1]=self.map[g]["type"]
                                    elif self.map[g]["type"] == 11: # Entrepot
                                        a[4]=self.map[g]["type"]
                            for c in entreeElec:
                                x,y = IndexToCoord(c)
                                h = followCable(self.map,entreeElec[x],i,(x-j,y-i))
                                if self.map[h]["type"] == 4 or self.map[h]["type"] == 5: # Elec
                                    a[2] = self.map[h]
                            if not (None in a):
                                changes.append({'attr':a[0]['attr']-200,'id':a[0]['id'],"type":"object"})
                                changes.append({'attr':a[1]['attr']-200,'id':a[1]['id'],"type":"object"})
                                changes.append({'attr':a[2]['attr']-200,'id':a[2]['id'],"type":"object"})
                                changes.append({'attr':a[3]['attr']+400,'id':a[3]['id'],"type":"ressources"})

        return changes
