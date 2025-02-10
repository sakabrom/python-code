import random
import time
import keyboard


ARMES = {
    "AK-47": (53, 0.11, 2, 60),
    "Minigun": (13, 0.011, 5, 120),
    "Lance-roquettes": (1000, 30, 0, float('inf'))
}


PERSONNAGES = {
    "AMIR": {"arme": "Minigun", "armure": 5},
    "ABDOU": {"arme": "AK-47", "armure": 10},
    "AHMED": {"arme": "Lance-roquettes", "armure": 15}
}


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

            if self.munitions == 0 :
                print("⚠️ Plus de munitions ! Recharge...")
                time.sleep(self.recharge)
                self.munitions = self.munitions_max
                print("🔄 Rechargé !")
                break


        else :
            print("\n💥 Appuie sur 'p' pour attaquer !")


    def cacher(self):
        choix = input("\nChoisis un point où te cacher (A, B, C, D) : ").upper()
        while choix not in ["A", "B", "C", "D"]:
            choix = input("❌ Entrée invalide ! Choisis entre A, B, C ou D : ").upper()
        return choix

    def subir_degats(self, boss):
        cible = boss.attaquer()
        cachette = self.cacher()

        if cachette == cible:
            degats_subis = max(25 - self.armure, 0)
            self.pv -= degats_subis
            print(f"\n💀 Mauvais choix ! Le boss t’a touché (-{degats_subis} PV, grâce à ton armure).")
            if self.pv <= 0:
                self.mourir()
        else:
            print("\n✅ Tu as esquivé l’attaque !")

    def mourir(self):
        if self.revivre:
            self.revivre = False
            self.pv = 50
            print("\n✨ Tu es revenu à la vie avec 50 PV !")
        else:
            print("\n💀 Tu es mort... Le boss t'a vaincu.")
            exit()


class Boss:
    def __init__(self):
        self.pv = 10000

    def attaquer(self):
        cible = random.choice(["A", "B", "C", "D"])
        print(f"\n🔥 Le boss attaque le point {cible} ! Cache-toi vite !")
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


while boss.pv > 0:
    print(f"\n🩸 **PV Boss** : {boss.pv} | ❤️ **Tes PV** : {joueur.pv}")

    joueur.attaquer(boss)

    if boss.pv <= 0:
        break

    joueur.subir_degats(boss)

print("\n🏆 **Félicitations ! Tu as vaincu le boss et libéré le lycée !**")
