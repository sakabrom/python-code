import random


class Personnage:
    def __init__(self, PV, weap, armor):
        self.vie = PV
        self.liste_armes = [("épée en legere", 1), ("épée en acier", 5), ("bâton", 3), ("tronçonneuse", 10)]
        self.liste_armures = [("tunique", 1), ("armure légère", 2), ("armure lourde", 3)]
        self.liste_sorts = [("Boule de Feu", 2, 3), ("Soin mini", 1, -2), ("Soin maxi", 3, -10)]
        if weap > len(self.liste_armes):
            self.arme = 0
        else:
            self.arme = weap
        if armor > len(self.liste_armures):
            self.armure = 0
        else:
            self.armure = armor
        self.inventaire = []

    def afficheVie(self):
        return self.vie

    def afficheMana(self):
        return self.mana

    def afficheArme(self):
        return self.liste_armes[self.arme]

    def valeurArme(self):
        return self.liste_armes[self.arme][1]

    def afficheArmure(self):
        return self.liste_armures[self.armure]

    def valeurArmure(self):
        return self.liste_armures[self.armure][1]

    def afficheListeArmes(self):
        return self.liste_armes

    def afficheListeArmures(self):
        return self.liste_armures

    def afficheListeSorts(self):
        return self.liste_sorts

    def perdVie(self, nombre):
        self.vie = self.vie - nombre

    def perdMana(self, nombre):
        self.mana = self.mana - nombre

    def ramasseButin(self, item):
        self.inventaire.append(item)

    def afficheInventaire(self):
        return self.inventaire


def attaque(attaquant, defenseur):
    defenseur.perdVie(max(attaquant.valeurArme() - defenseur.valeurArmure(), 0))


def sort(lanceur, sort, cible):
    lanceur.perdMana(lanceur.liste_sorts[sort][1])
    cible.perdVie(lanceur.liste_sorts[sort][2])


def ouvrePorte(perso):
    print("Vous ouvrez une nouvelle porte...")
    combatMonstre(perso)


def combatMonstre(perso):
    print("-----")
    pv = random.randint(1, 10)
    arme = random.randint(0, 2)
    armure = random.randint(0, 1)
    monstre = Personnage(pv, arme, armure)
    print("Un monstre apparaît !")
    finTour = 0
    while monstre.afficheVie() > 0:
        print("-----")
        print("A : attaquer")
        print("B : lancer un sort")
        print("C : fuir")
        print("D : inspecter l'ennemi")
        print("E : inspecter votre personnage")
        print("-----")
        a = input("Que voulez-vous faire ? ")
        while a not in ["A", "B", "C", "D", "E", "a", "b", "c", "d", "e"]:
            print()
            print("--Action incorrecte--")
            print("A : attaquer")
            print("B : lancer un sort")
            print("C : fuir")
            print("D : inspecter l'ennemi")
            print("E : inspecter votre personnage")
            a = input("Que voulez-vous faire ? ")

        if a in ["A", "a"]:
            print("----")
            print("Vous frappez le monstre.")
            attaque(perso, monstre)
            finTour = 1
        if a in ["B", "b"]:
            # [Demander quel sort utiliser, sur quelle cible, ..]
            sort(perso, sort, cible)
            finTour = 1
        if a in ["D", "d"]:
            print("----")
            print("Inspection de l'ennemi :")
            print("- Points de vie : ", monstre.afficheVie())
            print("- Arme : ", monstre.afficheArme())
            print("- Armure : ", monstre.afficheArmure())
    print("----")
    print(
        "Le monstre s'écroule. Vous avez réussi à le tuer alors que vous ne saviez même pas ce qu'il voulait, et qu'il ne se défendait pas. Félicitations, quel exploit !")
    a = random.randint(1, 2)
    if a == 1:
        perso.ramasseButin(monstre.afficheArme())
        print("Vous ramassez l'arme du monstre.")
    else:
        perso.ramasseButin(monstre.afficheArmure())
        print("Vous ramassez l'armure du monstre.")


perso = Personnage(random.randint(15, 25), random.randint(1, 3), random.randint(0, 2), random.randint(5, 15))

