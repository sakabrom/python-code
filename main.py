import pygame
import time
import random
import curses
from colorama import init, Fore, Style
import keyboard

init(autoreset=True)
pygame.mixer.init()
bip = pygame.mixer.Sound("beep.mp3")
select = pygame.mixer.Sound("select.mp3")
boom = pygame.mixer.Sound("boom.wav")

import keyboard
import time

class Arme:
    def __init__(self, nom, degats, cadence, recharge, munitions_max):
        self.nom = nom
        self.degats = degats
        self.cadence = cadence
        self.recharge = recharge
        self.munitions_max = munitions_max
        self.munitions_restantes = munitions_max

    def tirer(self):
        if self.munitions_restantes > 0:
            print(f"{self.nom} tire ! Dégâts: {self.degats}")
            self.munitions_restantes -= 1
            time.sleep(self.cadence)
        else:
            print(f"{self.nom} est vide ! Rechargement en cours...")
            time.sleep(self.recharge)
            self.munitions_restantes = self.munitions_max

ak47 = Arme("AK-47", 53, 0.35, 2, 60)
minigun = Arme("Minigun", 13, 0.11, 5, 120)
lance_roquettes = Arme("Lance-roquettes", 1000, 5.5, 0, 1)
mjolnir = Arme("mjolnir", 25, 1, 0, 1)
epee_legere = Arme("epee legere", 5, 0.5, 1, 1)
epee_legeree = Arme("epee legere", 2, 0.5, 1, 1)

# --- CLASSES ---
class Personnage:
    def __init__(self, nom, vie, arme):
        self.nom = nom
        self.vie = vie
        self.arme = arme
        self.argent = 0
        self.inventaire = []

    def attaquer(self, cible):
        degats = self.arme.degats
        cible.perdre_vie(degats)

    def perdre_vie(self, degats):
        self.vie -= degats
        if self.vie < 0:
            self.vie = 0

    def gagner_argent(self, montant):
        self.argent += montant

    def acheter(self, objet, prix):
        if self.argent >= prix:
            self.argent -= prix
            self.inventaire.append(objet)
            print("Vous avez acheté", objet, ". Argent restant :", self.argent, "€.")
            return True
        else:
            print("Argent insuffisant !")
            return False

class Sarpoulet:
    def __init__(self, nom):
        self.prix_info = 50
        self.prix_potion = 70
        self.nom = nom

    def info(self):
        return self.prix_info

    def potion(self):
        return self.prix_potion

class Professeur:
    def __init__(self, nom, salle):
        self.nom = nom
        self.salle = salle
        self.questions = [
            {"fonction": "2x + 3 = 0", "solution": -1.5},
            {"fonction": "3x - 5 = 0", "solution": 5/3},
            {"fonction": "x/2 + 4 = 0", "solution": -8},
        ]
        self.derniere_question = None

    def poser_question(self):
        self.derniere_question = random.choice(self.questions)
        return self.derniere_question["fonction"]

    def verifier_reponse(self, reponse):
        if self.derniere_question is not None:
            return reponse == self.derniere_question["solution"]
        return False

joueur = Personnage("Héros", 100, epee_legere)
mini_monstre = Personnage("Mini-monstre", 15, epee_legeree)
zarzor = Personnage("Zarzor", 100000, mjolnir)
sarpoulet = Sarpoulet("M. Sarpoulet")
professeur = Professeur("Mme Bristol", 118)

# --- FONCTIONS ---
def printec(phrase, color):
    if color == 2:
        color_code = Fore.RED
    elif color == 3:
        color_code = Fore.GREEN
    else:
        color_code = Fore.WHITE

    for lettre in phrase:
        nb = random.randint(1, 10)
        try:
            son = pygame.mixer.Sound(f"key{nb}.mp3")
            son.play()
        except Exception:
            pass
        print(f"{color_code}{lettre}{Style.RESET_ALL}", end="", flush=True)
        time.sleep(0.07)
    print()

def trailer():
    print("\n" * 3)
    printec("BIENVENUE AU LYCEE CHARLES BAUDELAIRE", 2)
    print("\n" * 3)
    time.sleep(1.7)
    print("Votre mission : sauver le lycée et vaincre Zarzor")
    boom.play()
    time.sleep(2.5)


def epreuve_maths():
    print("\nÉpreuve de Maths avec Mme Bristol!")
    question = professeur.poser_question()
    print("Résolvez l'équation:", question)

    rep = input("Votre réponse: ")
    rep = float(rep)  # Conversion manuelle en float

    if professeur.verifier_reponse(rep):
        print("Bonne réponse! Choisissez une arme légendaire:")
        print("1 - AK-47\n2 - Minigun\n3 - Lance-roquettes")

        choix = input("Entrez le numéro de l'arme: ")

        if choix == "1":
            joueur.arme = ak47
        elif choix == "2":
            joueur.arme = minigun
        elif choix == "3":
            joueur.arme = lance_roquettes
        else:
            print("Choix invalide, vous n'obtenez pas d'arme légendaire.")

        print(f"Vous avez choisi: {joueur.arme.nom}")
    else:
        print("Mauvaise réponse. Vous n'obtenez pas l'arme légendaire.")


def combat_final():
    print("\nCombat final contre Zarzor!")
    time.sleep(1)

    while zarzor.vie > 0 and joueur.vie > 0:
        print("\nZarzor attaque! Choisissez un point (A, B, C ou D):")
        point = input().upper()
        correct = random.choice(["A", "B", "C", "D"])

        if point != correct:
            joueur.perdre_vie(25)
            print("Vous n'avez pas esquivé, -25 PV. Votre vie:", joueur.vie)
        else:
            print("Vous avez esquivé l'attaque !")

        if zarzor.vie <= 50000:
            print("\nZarzor attaque deux points à la fois!")
            point = input("Choisissez un point (A, B, C ou D): ").upper()
            corrects = random.sample(["A", "B", "C", "D"], 2)
            print(f"Zarzor attaque les points {corrects[0]} et {corrects[1]}!")

            if point in corrects:
                joueur.perdre_vie(25)
                print("Vous avez été touché ! -25 PV. Votre vie:", joueur.vie)
            else:
                print("Vous avez esquivé l'attaque !")

        print("\nMaintenez 'p' pour tirer, appuyez sur 'q' pour arrêter.")
        while True:
            if keyboard.is_pressed("p"):
                joueur.arme.tirer()
                zarzor.perdre_vie(joueur.arme.degats)
                print("Vous attaquez Zarzor et lui infligez", joueur.arme.degats, "dégâts. Vie restante de Zarzor:",
                      zarzor.vie)
            if keyboard.is_pressed("q"):
                print("Fin du tir.")
                break

    if joueur.vie > 0:
        print("\nZarzor est vaincu, le lycée est sauvé!")
    else:
        print("\nVous êtes mort. Game Over!")

    time.sleep(2)


def m_sarpoulet():
    printec("Bonjour, je suis M. Sarpoulet, un très bon prof, que voulez-vous ?", 2)
    choice_count = 0
    while True:
        print("\n1 - Chocolat (Potion) - {}€".format(sarpoulet.potion()))
        print("2 - Autre chose (information sur Mme Bristol) - {}€".format(sarpoulet.info()))
        print("3 - Quitter le menu")
        choix = input("Votre choix: ")

        if choix == "1":
            printec("Vous avez choisi le chocolat (Potion).", 3)
            if joueur.argent >= sarpoulet.potion():
                joueur.inventaire.append(50)

            else:
                printec("Argent insuffisant !", 2)


        elif choix == "2":
            if choice_count == 0:
                printec("M. Sarpoulet : Je n'ai rien d'autre.", 2)
                choice_count += 1
            elif choice_count == 1:
                printec("M. Sarpoulet : Vous me fatiguez, je n'ai rien d'autre !", 2)
                choice_count += 1
            else:
                message = f"M. Sarpoulet : Pour {sarpoulet.info()}€, je vous dis où est Mme Bristol."
                printec(message, 2)
                rep = input("Souhaitez-vous acheter l'information ? (oui/non): ")
                if rep.lower() == "oui":
                    if joueur.argent >= sarpoulet.info():
                        joueur.acheter( sarpoulet.info(), 20)
                        printec(f"M. Sarpoulet : madame bristol est caché dans la salle {professeur.salle}", 2)

                    else:
                        printec("Argent insuffisant !", 2)
                else:
                    printec("M. Sarpoulet : Très bien, alors repartez !", 2)


        elif choix == "3":
            printec("Vous avez choisi de quitter le menu de M. Sarpoulet. ", 2)

            room = input("Dans quelle salle voulez-vous aller ? (Entrez 110 pour Sarpoulet, autre pour Bristol) : ")
            if room == "110":
                return "sarpoulet"

            elif room == "157":
                return "bristol"
            else:
                return "combat"
        else:
            print("Action non valide. Réessayez.")



def combat_mini_monstre():
    print("\nCombat contre des mini-monstres infinis!")

    while True:
        action = input("Choisissez votre action : [p] Attaquer, [f] Finir le combat : ").lower()
        if action == "p":
            while joueur.vie > 0 and  mini_monstre.vie > 0:

                print(f"Vous infligez {joueur.arme.degats} dégâts.")
                mini_monstre.vie -= joueur.arme.degats
                if mini_monstre.vie <= 0:
                    print("Mini-monstre vaincu! Vous gagnez 10€.")
                    joueur.gagner_argent(10)

                print("Le mini-monstre vous attaque!")
                joueur.perdre_vie(mini_monstre.arme.degats)
                print(f"Votre vie: {joueur.vie}")
                if joueur.vie <= 0:
                    print("Vous êtes mort.")
                    return None
        elif action == "f":
            room = input("Dans quelle salle voulez-vous aller ? (Entrez 110 pour Sarpoulet, autre pour Bristol) : ")
            if room == "110":
                return "sarpoulet"
            elif room == "157" :
                return "bristol"
        else:
            print("Action non valide. Réessayez.")

def jeu():
    printec("Vous êtes dans la cour, attention il y a des monstres partout", 3)
    salle = combat_mini_monstre()
    if salle == "sarpoulet":
        m_sarpoulet()

    salle2 = m_sarpoulet()
    if salle2 == "bristol":
        epreuve_maths()

    elif salle2 == "combat":
        combat_mini_monstre()

    else:
        print("choix non validé")

    if joueur.vie <= 0:
        return
    combat_final()

def afficher_menu(stdscr, menu):
    curses.curs_set(0)
    ligne_actuelle = 0
    while True:
        stdscr.clear()
        for index, ligne in enumerate(menu):
            if index == ligne_actuelle:
                stdscr.addstr(index + 1, 0, "> " + ligne)
            else:
                stdscr.addstr(index + 1, 0, "  " + ligne)
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

def main_menu(stdscr):
    choix = afficher_menu(stdscr, ["Jeu", "Trailer", "Quitter"])
    return choix

def main():
    choix = curses.wrapper(main_menu)
    if choix == "Quitter":
        return
    elif choix == "Trailer":
        trailer()
        input("Appuyez sur Entrée pour revenir au menu.")
        main()
    elif choix == "Jeu":
        trailer()
        jeu()
        input("Fin du jeu. Appuyez sur Entrée pour quitter.")

if __name__ == "__main__":
    main()
