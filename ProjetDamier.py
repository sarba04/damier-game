import random
import time

class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def adjacentes(self, jeu):
        cases_adjacentes = []
        for case in jeu.listeDesCases:
            if self != case and abs(self.x - case.x) <= 1 and abs(self.y - case.y) <= 1:
                cases_adjacentes.append(case)
        return cases_adjacentes

class Creature:
    def __init__(self, nom, position):
        self.nom = nom
        self.position = position

    def __str__(self):
        return f"{self.nom} - Position : {self.position}"

    def choisirCible(self, jeu):
        cases_adjacentes = self.position.adjacentes(jeu)
        cases_occupees = [case for case in cases_adjacentes if jeu.est_occupee(case)]
        if cases_occupees:
            return random.choice(cases_occupees)
        else:
            return random.choice(cases_adjacentes)

class Jeu:
    def __init__(self, taille):
        self.listeDesCases = [Case(x, y) for x in range(taille) for y in range(taille)]
        self.listeDesCreatures = []
        self.tour = 0
        self.actif = None

    def __str__(self):
        return f"Tour : {self.tour}, Actif : {self.actif}\n{', '.join(str(creature) for creature in self.listeDesCreatures)}"

    def est_occupee(self, case):
        return any(creature.position.x == case.x and creature.position.y == case.y for creature in self.listeDesCreatures)

    def creer_creature(self, nom, position):
        creature = Creature(nom, position)
        self.listeDesCreatures.append(creature)
        self.actif = creature

    def deplacer(self, creature, case):
        if creature in self.listeDesCreatures:
            if case in creature.position.adjacentes(self):
                if self.est_occupee(case):
                    captured_creature = next(c for c in self.listeDesCreatures if c.position.x == case.x and c.position.y == case.y)
                    print(f"Tour {self.tour} : {creature.nom} a capturé {captured_creature.nom} à la position {case}")
                    self.listeDesCreatures.remove(captured_creature)
                else:
                    creature.position = case
                    self.tour += 1
                    self.actif = self.listeDesCreatures[(self.tour % len(self.listeDesCreatures))]
                    print(f"Tour {self.tour} : {creature.nom} s'est déplacé vers {case}\n")
            else:
                print("Déplacement non autorisé.")
        else:
            print("Cette créature n'existe pas dans le jeu.")

    def joueur_suivant(self):
        """
        Change le joueur actif pour le prochain joueur dans la liste des créatures.
        """
        self.actif = self.listeDesCreatures[(self.listeDesCreatures.index(self.actif) + 1) % len(self.listeDesCreatures)]

# Affichage des joueurs et de leurs positions
def afficher_joueurs(jeu):
    print("Les joueurs sont prêts :")
    for creature in jeu.listeDesCreatures:
        print(creature)

# Animation de démarrage du jeu
def animation_demarrage():
    print("Début de la partie...")
    time.sleep(2)
    print("Préparez-vous !")
    time.sleep(2)
    print("Que le jeu commence !\n")


# Création d'une instance de jeu
jeu = Jeu(4)

# Ajout de créatures au jeu
jeu.creer_creature("Creature1", jeu.listeDesCases[0])
jeu.creer_creature("Creature2", jeu.listeDesCases[-1])

# Affichage des joueurs avant de commencer le jeu
afficher_joueurs(jeu)

# Animation de démarrage du jeu
animation_demarrage()

# Boucle principale du jeu
while len(jeu.listeDesCreatures) > 1:


    # Tour du joueur actif
    print(f"c’est désormais le tour de {jeu.actif.nom} de se déplacer ")
    cible = jeu.actif.choisirCible(jeu)
    jeu.deplacer(jeu.actif, cible)

    # Passer au joueur suivant
    jeu.joueur_suivant()

    # Pause de 3 seconde entre les tours
    time.sleep(3)

# Affichage du message de fin du jeu
print("Fin du jeu.")

# Détermination du vainqueur et affichage du message de félicitations
vainqueur = jeu.listeDesCreatures[0]
print(f"Félicitations! {vainqueur.nom} est le vainqueur!")
