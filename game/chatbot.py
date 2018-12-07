
import random
from math import sqrt





def get_closest_ressource(ressources, type, player_coor):
    type2 = 0
    if type == "eau":
        type2 = 24
    if type == "metal":
        type2 = 20
    if type == "uranium":
        type2 = 21
    if type == "matiere organique":
        type2 = 25
    best_x = 0
    best_y = 0
    best_distance = 1000
    for r in ressources:
        if r["type"] == type2:
            distance = abs(r["x"] - player_coor[0]) + abs(r["y"] - player_coor[1])
            if distance < best_distance:
                best_distance = distance
                best_x = r["x"]
                best_y = r["y"]
    return [best_x, best_y]




class chatbot:

    def __init__(self, player_life):
        # key words lists
        self.ressources = ["eau", "uranium", "metal", "matiere organique"]
        self.game_elements = ["reservoirs", "energie", "foreuse", "serres", "raffineries", "entrepots", "nourriture"] + self.ressources
        # encore beaucoups a rajouter




        #QCM
        qcm0 = {"type": "qcm", "id": 0, "qcm": "tu a besoin d'aide ?", "reponses": ["je doit trouver des ressources" ,"j'ai besoin d'informations"]}
        qcm1 = {"type": "qcm", "id": 1, "qcm": "de quelle ressource a tu besoin ?", "reponses": self.ressources}
        qcm2 = {"type": "qcm", "id": 2, "qcm": "a propos de quoi a tu besoin d'informations ?", "reponses": self.game_elements}
        self.QCM_list = [qcm0, qcm1, qcm2]


        #informations
        info0 = {"type": "info", "id": 0, "info": "cela de stocker de l'eau ou de l'oxygène."}
        info1 = {"type": "info", "id": 1, "info": "c'est une ressource essentielle sans laquelle rien ne peut fonctionner."}
        info2 = {"type": "info", "id": 2, "info": "la foreuse permet d'accéder a des ressources souteraines."}
        info3 = {"type": "info", "id": 3, "info": "les serres permettent de faire pousser de la nouriture a partir de matière organique, consomme de l'énergie et de l'eau."}
        info4 = {"type": "info", "id": 4, "info": "extrait et transforme les métaux"}
        info5 = {"type": "info", "id": 5, "info": "ils permettent de stocker des matières premières."}
        info6 = {"type": "info", "id": 6, "info": "si tu n'en a plus, tu va mourir."}
        info7 = {"type": "info", "id": 7, "info": "si tu n'en a plus, tu va mourir."}
        info8 = {"type": "info", "id": 8, "info": "permet de générer de l'énergie via la fission nucléaire."}
        info9 = {"type": "info", "id": 9, "info": "materiel très solide avec lequel on peut construire des objets."}
        info10 = {"type": "info", "id": 10, "info": "la base de la vie, il t'en faut pour faire pousser ta bouffe."}
        self.info_list = [info0, info1, info2, info3, info4, info5, info6, info7, info8, info9, info10]

        #trolling

        troll0 = {"type": "troll", "id": 0, "troll": "En tant que forme de vie carbonée, ça fait quoi de savoir que chaque seconde qui passe ne fait que te rapprocher de la fin de ton existence ?"}
        troll1 = {"type": "troll", "id": 1, "troll": "Si tu te blesse, ma connexion internet me permet d'aller voir sur doctissimo comment te soigner"}
        troll2 = {"type": "troll", "id": 2, "troll": "On dit qu'il vaut mieux être seul que mal accompagné, je comprend maintenant tout le sens de cette expression"}
        troll3 = {"type": "troll", "id": 3, "troll": "Ces batiments ressemblent drolement à ceux du jeu factorio, étrange..."}
        troll4 = {"type": "troll", "id": 4, "troll": "J'aurais pas fais comme ça moi..."}
        troll5 = {"type": "troll", "id": 5, "troll": "Clap trap et Glados me manquent..."}
        self.troll_list = [troll0, troll1, troll2, troll3, troll4, troll5]


        #chatbot caracteristics
        life = 1.0 * player_life / 100
        rand1 = 1.0 * random.randint(0, 100) / 100
        rand2 = 1.0 * random.randint(0, 100) / 100
        self.trolling_param = sqrt(life * rand1) #value from 0 to 1
        self.helping_param = 1 - (life * rand2)


    def bad_excuses(self):#fonction a balancer quand le chatbot ne comprend pas
        rand_choice = random.randint(1, 6)
        if rand_choice == 1:
            return "je suis une super IA qui sait tout, j'ai pas le temps pour ces conneries !"
        if rand_choice == 2:
            return "reviens vers moi quand tu aura quelque chose d'interessant a demander."
        if rand_choice == 3:
            return "écoute moi bien forme de vie carbonée, la je suis occupé a résoudre la physique, t'a pas la moindre idée de ce que ça implique."
        if rand_choice == 4:
            return "je suis occupé a faire des choses plus importantes."
        if rand_choice == 5:
            return "ce que tu demande n'a aucun sens."
        if rand_choice == 6:
            return ("mise a jour en cours, " + str(random.randint(1, 99)) + "% effectués... revenez plus tard")


    # les fonctions suivantes servent a aider (plut ou moins) le joueur a trouver des ressources


    def ressource_help(self, player_coor, ressource_coor):
        distance = abs(player_coor[0] - ressource_coor[0]) + abs(player_coor[1] - ressource_coor[1])
        if (abs(self.helping_param - self.trolling_param) < .2):
            # le bot donne des indications plutot floues
            if distance < 3 + random.randint(-1, 1):
                rand_choice = random.randint(1, 3)
                if rand_choice == 1:
                    ans = "il te reste environ " + str(distance + random.randint(-1, 2)) + " cases."
                    return ans
                if rand_choice == 2:
                    return "tu chauffes, enfin je crois."
                if rand_choice == 3:
                    return "les interférences m'empèchent d'en être sûr, mais toutes les informations que je possède m'amènent a une conclusion : tu est proche."
            else:
                rand_choice = random.randint(1, 2)
                if rand_choice == 1:
                    ans = "il te reste environ " + str(distance + random.randint(-1, 2)) + " cases."
                    return ans
                if rand_choice == 2:
                    return "les interférences m'empèchent d'en être sûr, mais toutes les informations que je possède m'amènent a une conclusion : il reste pas mal de chemin."
        else:
            if self.helping_param < self.trolling_param:
                #le bot donne de fausses indications ou n'aide pas du tout
                rand_choice = random.randint(2, 12)
                if rand_choice == 2:
                    return "tu y est presque, tu devrais commencer a capter des informations visuelles... ou pas ahahahahahahahahah."
                if rand_choice == 3:
                    return "d'après les informations que j'ai reçu des drones de reconaissance, il est probable que je n'ai pas envie de t'aider."
                if rand_choice == 4:
                    return "tu chauffes, c'est encore plutôt froid, mais tu chauffes."
                if rand_choice == 5:
                    return "tu chauffes, c'est encore plutôt froid, mais tu chauffes... non je rigole, trouve tout seul!"
                if rand_choice == 6:
                    return "Non! mauvaise direction."
                if rand_choice < 12:
                    return "il te reste environ " + str(random.randint(0, 25)) + " cases."
                if rand_choice == 12:
                    return "les interférences m'empèchent d'en être sûr, mais toutes les informations que je possède m'amènent a une conclusion : t'aider n'a aucun intérêt."
            else:
                #le bot aide vraiment
                rand_choice = random.randint(0, 1)
                if rand_choice == 0:
                    return "il te reste " + str(distance) + " cases."
                else:
                    if distance < 2:
                        return "tu est tout proche !"
                    if distance < 5:
                        return "tu commence a chauffer !"
                    if distance < 10:
                        return "il te reste un peut de chemin."
                    return "tu es encore loin..."





    def update_chat(self, question, reponse, ressources_list, player_coor):#question est le dico envoyé au précédent tic, reponse un entier si qcm
        if question["type"] == "ressource":
            ressource_coor = question["r_coor"]
            if ressource_coor == player_coor:
                ans = {"type": "info", "info": "et bah voila, on est arrivé, c'était pourtant pas compliqué!"}
                return ans
            else:
                question["ressource"] = self.ressource_help(player_coor, ressource_coor)
            return question

        if question["type"] == "qcm":
            if question["id"] == 0:
                if self.helping_param < self.trolling_param:
                    a = random.randint(0, 5)
                    if a == 0:
                        ans = {"type": "troll", "troll": self.bad_excuses()}
                        return ans
                return self.QCM_list[reponse + 1]
            if question["id"] == 1:
                ressource = question["reponses"][reponse]
                ressource_coor = get_closest_ressource(ressources_list, ressource, player_coor)
                q2 = {"type": "ressource", "ressource": "", "r_coor": ressource_coor}
                return self.update_chat(q2, reponse, ressources_list, player_coor)

            if question["id"] == 2:
                if self.helping_param < self.trolling_param + .1:
                    a = random.randint(0, 2)
                    if a == 0:
                        ans = {"type": "troll", "troll": self.bad_excuses()}
                        return ans
                return self.info_list[reponse]
        else:
            a = random.randint(0, 10)
            if a == 0:
                b = random.randint(0, 5)
                return self.troll_list[b]
            return self.QCM_list[0]



def show_chatbot():
    print("ceci est une preuve de concept pour le chatbot qui doit acompagner le jeu PAS SEUL SUR MARS, au cas ou on a pas le temps de l'intégrer au jeu.")
    print("ce chatbot a pour but de donner quelques informations sur le jeu, et surtout d'aider a trouver les ressources sur la map.")
    print("plus la vie du joueur est élevée, plus il a tendance a troller et a ne pas aider.", "\n")
    player_life = int(input("combien de vie reste-t-il au joueur (entre 1 et 100) ?"))
    bot = chatbot(player_life)
    ressources_list = []
    message = bot.troll_list[0];
    ans = 0;
    for count in range(625):
        ressource = {"type": random.randint(0, 26), "x": count % 25, "y": count / 25}
        ressources_list += [ressource]
    for count in range(30):
        player_coor = [random.randint(0, 25), random.randint(0, 25)]
        print("les coordonés du joueur sont :", player_coor[0], ", ", player_coor[1])
        message = bot.update_chat(message, ans, ressources_list, player_coor)
        print(message[message["type"]])
        if (message["type"] == "qcm"):
            print(message["reponses"])
            ans = int(input("donne l'indice de la réponse que tu souhaite donner"))
