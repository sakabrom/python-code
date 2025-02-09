import curses
import pygame
import time
import random

pygame.mixer.init()
bip = pygame.mixer.Sound("beep.mp3")
select = pygame.mixer.Sound("select.mp3")
stdscr = curses.initscr()
milieu_x = stdscr.getmaxyx()[1]// 2
milieu_y = stdscr.getmaxyx()[0]//2
curses.start_color()
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
"""_________________________________________________________DEBUT-TRAILER___________________________________________________________________"""



def trailer(stdscr):
    boom = pygame.mixer.Sound("boom.wav")
    printec(stdscr, 10, milieu_x, "BIENVENUE AU LYCEE CHARLES BAUDELAIRE", 2 )
    time.sleep(1.7)
    stdscr.addstr(milieu_y, (milieu_x - 40), "Votre mission : sauver le lycée et vaincre Zarzor")
    stdscr.refresh()
    boom.play()
    time.sleep(2.5)



"""_________________________________________________________FIN-TRAILER___________________________________________________________________"""




"""_________________________________________________________DEBUT-JEU___________________________________________________________________"""

class Personnage:
    def __init__(self, nom, vie, arme):
        self.nom = nom
        self.vie = vie
        self.arme = arme
        self.argent = 0
        self.inventaire = []

    def attaquer(self, cible):
        degats = self.arme["dégâts"]
        cible.perdre_vie(degats)

    def perdre_vie(self, degats):
        self.vie -= degats
        if self.vie <= 0:
            print("GAME OVER !!!")

    def gagner_argent(self, montant):
        self.argent += montant

    def acheter(self, objet, prix):
        if self.argent >= prix:
            self.argent -= prix
            self.inventaire.append(objet)
            print(f"Vous avez acheté {self.objet}. Argent restant : {self.argent}€.")
        else:
            print("Argent insuffisant !")

class Sarpoulet:
    def __init__(self, nom):
        self.prix_info = 100
        self.prix_potion = 150
        self.nom = nom

    def info(self):
        return self.prix_info

    def potion(self):
        return self.prix_potion

class Professeur:
    def __init__(self, nom):
        self.nom = nom
        self.questions = [
            {"fonction": "2x + 3 = 0", "solution": -1.5},
            {"fonction": "3x - 5 = 0", "solution": 5/3},
            {"fonction": "x/2 + 4 = 0", "solution": -8},
        ]

    def test_maths(self):
        question = random.choice(self.questions)
        return question["fonction"]

    def solution_equation(self):
        return self.questions["solution"]

armes = {
    "Épée légère": {"nom": "Épée légère", "dégats": 5},
    "AK-47": {"nom": "AK-47", "dégats": 53},
    "Minigun": {"nom": "Minigun", "dégats": 13},
    "Lance-roquettes": {"nom": "Lance-roquettes", "dégats": 1000},
    "MjÖllnir" : {"nom": "MjÖllnir", "dégats": 25}
}


joueur = Personnage("Héros", 100, armes["Épée légère"])
mini_monstre = Personnage("Mini-monstre", 15, armes["Épée légère"])
Zarzour = Personnage("Zarzour", 100000, armes["MjÖllnir"])
sarpoulet = Sarpoulet("m.sarpoulet")
professeur = Professeur("copyright")


def jeu():
    print("Attention il  y a des monstres partout !!!")



"""_________________________________________________________FIN-JEU___________________________________________________________________"""

def afficher_menu(stdscr, menu):
    curses.curs_set(0)
    ligne_actuelle = 0

    while True:
        stdscr.clear()

        for index, ligne in enumerate(menu):
            if index == ligne_actuelle:
                stdscr.addstr(index + 1, 0, f"> {ligne}", curses.color_pair(1))
            else:
                stdscr.addstr(index + 1, 0, f"  {ligne}")

        stdscr.refresh()


        touche = stdscr.getch()
        if touche == curses.KEY_UP and ligne_actuelle > 0:
            ligne_actuelle -= 1
            bip.play()
        elif touche == curses.KEY_DOWN and ligne_actuelle < len(menu) - 1:
            ligne_actuelle += 1
            bip.play()
        elif touche == ord("\n"):
            select.play()
            return menu[ligne_actuelle]


def printec(stdscr, y, x, phrase, color):

    curses.start_color()
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    for lettre in phrase:
        nb = random.randint(1, 10)
        son = pygame.mixer.Sound(f"key{nb}.mp3")
        if color == 2 :
            stdscr.addstr(y, x, lettre, curses.color_pair(2) )
            son.play()
            stdscr.refresh()  # Met à jour l'écran
            x += 1  # Avance d'une position horizontale
            time.sleep(0.07)
        elif color == 3:
            stdscr.addstr(y, x, lettre, curses.color_pair(3))
            son.play()
            x += 1  # Avance d'une position horizontale
            time.sleep(0.07)
        else:
            stdscr.addstr(y, x, lettre, curses.color_pair(1))  # Affiche une lettre
            stdscr.refresh()  # Met à jour l'écran
            x += 1  # Avance d'une position horizontale
            time.sleep(0.07)



def commencé(stdscr):
            choix = afficher_menu(stdscr, ["Jeu", "Trailer", "Quitter"])
            if choix == "Quitter":
                return

            elif choix == "Trailer":
                stdscr.clear()
                trailer(stdscr)

            elif choix == "Jeu":
                stdscr.clear()
                trailer(stdscr)
                stdscr.clear()
                jeu(stdscr)



# Lancement de l'application avec `curses`
curses.wrapper(commencé)
curses.endwin()
