import random
import pygame
import time
import keyboard

pygame.mixer.init()
musique = pygame.mixer.music.load('musique.mp3')

ARMES = {

    "AK-47": (53, 0.11, 2, 60),

    "Minigun": (13, 0.011, 5, 120),

    "Lance-roquettes": (1000, 30, 0, float('inf'))

}

PERSONNAGES = {

    "AMIR": {"arme": "Minigun", "armure": 5},

    "ABDOU": {"arme": "AK-47", "armure": 15},

    "AHMED": {"arme": "Lance-roquettes", "armure": 10}

}

fonctions_affines = {
    "f1": {"fonction": "2x + 4 = 0", "solution": -2},
    "f2": {"fonction": "-2x + 6 = 0", "solution": -3},
    "f3": {"fonction": "4x - 24 = 0", "solution": -6},
    "f4": {"fonction": "-7x + 14 = 0", "solution": 2},
    "f5": {"fonction": "x - 999 = 0", "solution": -999},
    "f6": {"fonction": "11x + 88 = 0", "solution": -8
           }}

class Joueur:

    def __init__(self, nom, arme, armure):

        self.nom = nom

        self.pv = 100

        self.arme = arme

        self.armure = armure

        self.degats, self.cadence, self.recharge, self.munitions_max = ARMES[self.arme]

        self.munitions = self.munitions_max

        self.revivre = True

    def attaquer(self, boss):

        choix = input("\n💥 Appuie sur 'p' pour attaquer !")

        tirs = 0

        while choix == 'p' and self.munitions > 0:

            boss.pv -= self.degats

            self.munitions -= 1

            tirs += 1

            print(f"💣 {self.nom} tire ! Boss: {boss.pv} PV restants")

            time.sleep(self.cadence)

            if self.munitions == 0 or keyboard.is_pressed('m'):
                print("⚠️ Plus de munitions ! Recharge...")

                time.sleep(self.recharge)

                self.munitions = self.munitions_max

                print("🔄 Rechargé !")

                break

            if boss.pv <= 0:
                break

        else:

            print("\n💥 Appuie sur 'p' pour attaquer !")

    def math(self, boss):
        while boss.pv <= 3000:
            print("Vous n'avez plus d'armes !!! Mais le boss déteste les maths.")
            fonction_choisie = random.choice(list(fonctions_affines.values()))
            print(
                f"\n🧮 Résous l'équation suivante  : {fonction_choisie['fonction']}")
            reponse = int(input("> "))


            if reponse == fonction_choisie["solution"]:
                print("\n✅ Bonne réponse ! Le boss perd 750 PV.")
                boss.pv -= 750
            else:
                print("\n❌ Mauvaise réponse ! Tu perds 10 PV.")
                self.pv -= 10

            if boss.pv <= 0:
                break

    def cacher(self):

        choix = input("\nChoisis un point où te cacher (A, B, C, D) : ").upper()

        while choix not in ["A", "B", "C", "D"]:
            choix = input("❌ Entrée invalide ! Choisis entre A, B, C ou D : ").upper()

        return choix

    def subir_degats(self, boss):

        if boss.pv > 5000:
            cible = boss.attaquer()
            cible2 = None
        else:
            cible = None
            cible2 = boss.attaquer2()


        cachette = self.cacher()

        if cible:
            if cachette == cible:
                degats_subis = max(25 - self.armure, 0)
                self.pv -= degats_subis
                print(f"\n💀 Mauvais choix ! Le boss t’a touché (-{degats_subis} PV, grâce à ton armure).")
            else:
                print(f"\n✅ Tu as esquivé l’attaque ! Le boss a attaqué le point {cible}")
        elif cible2:
            if cachette == cible2[0] or cachette == cible2[1]:
                degats_subis = max(25 - self.armure, 0)
                self.pv -= degats_subis
                print(f"\n💀 Mauvais choix ! Le boss t’a touché (-{degats_subis} PV, grâce à ton armure).")
            else:
                print(f"\n✅ Tu as esquivé l’attaque ! Le boss a attaqué les points {cible2[0]} et {cible2[1]}")


class Boss:
        def __init__(self):
            self.pv = 10000



        def attaquer2(self):
            if self.pv <= 5000:
                cible2 = random.sample(["A", "B", "C", "D"], 2)
                print("\n🔥 Le boss attaque deux points aléatoires ! Cache-toi vite !")
                return cible2



        def attaquer(self):
            if self.pv > 5000:
                cible = random.choice(["A", "B", "C", "D"])
                print("\n🔥 Le boss attaque un point aléatoire ! Cache-toi vite !")
                return cible



print("\n👥 **Choisis ton personnage** :")

for nom, details in PERSONNAGES.items():
    print(f"- {nom} (Arme : {details['arme']}, Armure réduit les dégâts de {details['armure']})")

choix_perso = input("\n> ").upper()

while choix_perso not in PERSONNAGES:
    choix_perso = input("❌ Personnage invalide ! Choisis Amir, Abdou ou Ahmed : ").upper()

details_perso = PERSONNAGES[choix_perso]

joueur = Joueur(choix_perso, details_perso["arme"], details_perso["armure"])

boss = Boss()

print(f"\n🎭 **{joueur.nom} est prêt au combat avec {joueur.arme} et une armure absorbant {joueur.armure} dégâts !**")
pygame.mixer.music.play()

while boss.pv > 0:

    print(f"\n🩸 **PV Boss** : {boss.pv} | ❤️ **Tes PV** : {joueur.pv}")
    if boss.pv >= 3000 :
         joueur.attaquer(boss)
    else :
         joueur.math(boss)


    if not pygame.mixer.music.get_busy():
        print("\nLe temps est passé , vous êtes mort !")
        break

    if boss.pv <= 0:
        print("\n🏆 **Félicitations ! Tu as vaincu le boss et libéré le lycée !**")
        break

    if joueur.pv<=0:
        print("\n Vous avez perdu ")
        break

    joueur.subir_degats(boss)


